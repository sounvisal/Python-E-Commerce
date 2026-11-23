"""Shared order ownership, inventory and fulfillment rules."""
import hashlib
import hmac
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import update
from app.models.order import Order
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.user import User
from app.core.config import settings

def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)

def guest_token(order):
    return hmac.new(settings.SECRET_KEY.encode(), f"{order.order_number}:{order.checkout_key}".encode(), hashlib.sha256).hexdigest()

def check_order_access(order, user=None, token=None):
    if not order:
        raise HTTPException(404, "Order not found")
    if user and (user.role == "admin" or order.user_id == user.id):
        return order
    # Cryptographic access token required for guest orders to prevent unverified email matching
    if token and order.access_token_hash and hmac.compare_digest(hashlib.sha256(token.encode()).hexdigest(), order.access_token_hash):
        return order
    raise HTTPException(404, "Order not found for this session")

def add_event(order, status):
    order.events = [*(order.events or []), {"status": status, "at": utcnow().isoformat() + "Z"}]

def release_stock(db, order):
    """
    Safely releases inventory and promotional usage exactly once.
    - If stock_reserved is True: restores stock to Product inventory and resets stock_reserved.
    - If stock_reserved is False: does NOT touch product stock.
    - If promo_claimed is True: decrements Promotion.used and resets promo_claimed.
    A conditional update ensures cancelling/expiring twice cannot restock twice.
    """
    changed = db.execute(
        update(Order)
        .where(Order.id == order.id, Order.stock_reserved.is_(True))
        .values(stock_reserved=False)
        .execution_options(synchronize_session=False)
    ).rowcount
    if changed:
        for line in order.items:
            if line.product_id:
                db.execute(
                    update(Product)
                    .where(Product.id == line.product_id)
                    .values(stock=Product.stock + line.quantity)
                )
        order.stock_reserved = False

    if order.discount_code:
        promo_changed = db.execute(
            update(Order)
            .where(Order.id == order.id, Order.promo_claimed.is_(True))
            .values(promo_claimed=False)
            .execution_options(synchronize_session=False)
        ).rowcount
        if promo_changed:
            db.execute(
                update(Promotion)
                .where(Promotion.code == order.discount_code, Promotion.used > 0)
                .values(used=Promotion.used - 1)
            )
            order.promo_claimed = False

def expire_pending_orders(db):
    """
    Expires orders past their deadline:
    - KHQR orders (status == 'Pending', expires in 5m)
    - Unconfirmed COD orders (status == 'Awaiting Confirmation', expires in 24h)
    """
    now = utcnow()
    expirable = ["Pending", "Awaiting Confirmation"]
    for order in db.query(Order).filter(Order.status.in_(expirable), Order.expires_at.isnot(None), Order.expires_at <= now).all():
        changed = db.execute(
            update(Order)
            .where(Order.id == order.id, Order.status.in_(expirable), Order.expires_at <= now)
            .values(status='Expired', payment_status='Expired')
            .execution_options(synchronize_session=False)
        ).rowcount
        db.refresh(order)
        if changed:
            add_event(order, "Expired")
            release_stock(db, order)
    db.flush()

def cancel_order(db, order):
    if order.status in ("Cancelled", "Expired"):
        return order
    if order.status not in ("Pending", "Awaiting Confirmation", "Confirmed", "Processing"):
        raise HTTPException(409, "This order has already been dispatched")
    if order.payment_status == "Paid":
        raise HTTPException(409, "A paid order needs a refund review. Contact support before cancellation.")
    changed = db.execute(
        update(Order)
        .where(
            Order.id == order.id,
            Order.status.in_(['Pending', 'Awaiting Confirmation', 'Confirmed', 'Processing']),
            Order.payment_status != 'Paid'
        )
        .values(status='Cancelled', payment_status='Cancelled')
        .execution_options(synchronize_session=False)
    ).rowcount
    db.refresh(order)
    if not changed:
        if order.status == "Cancelled":
            return order
        raise HTTPException(409, 'The order changed. Reload before cancelling.')
    add_event(order, "Cancelled")
    release_stock(db, order)
    return order

def transition_order(db, order, target):
    if target == order.status:
        return order

    # Handle staff reconciliation from Payment Review state
    if order.status == "Payment Review":
        if target == "Confirmed":
            if order.payment_status != "Paid":
                raise HTTPException(409, "Payment must be verified before confirming a review order")
            
            # 1. Aggregate required quantities across line items by product_id
            from collections import defaultdict
            required_by_product = defaultdict(int)
            line_names = {}
            for line in order.items:
                if line.product_id:
                    required_by_product[line.product_id] += (line.quantity or 1)
                    line_names[line.product_id] = line.product_name

            # 2. Lock products in consistent sorted order and verify sufficient stock
            sorted_product_ids = sorted(required_by_product.keys())
            insufficient = []
            for pid in sorted_product_ids:
                req_qty = required_by_product[pid]
                product = db.query(Product).filter(Product.id == pid).with_for_update().first()
                if not product or product.stock < req_qty:
                    avail = product.stock if product else 0
                    pname = line_names.get(pid, f"#{pid}")
                    insufficient.append(f"'{pname}' (available: {avail}, required: {req_qty})")

            if insufficient:
                # Rollback uncommitted queries and abort without reserving stock
                db.rollback()
                raise HTTPException(
                    409,
                    f"Cannot fulfill order: insufficient stock for {', '.join(insufficient)}. Issue a refund or wait for restocking."
                )

            # 3. Conditional order-state claim: ensure only one thread can transition the order and reserve stock
            claim = db.execute(
                update(Order)
                .where(
                    Order.id == order.id,
                    Order.status == "Payment Review",
                    Order.stock_reserved == False
                )
                .values(stock_reserved=True, status="Confirmed")
                .execution_options(synchronize_session=False)
            ).rowcount

            db.refresh(order)
            if not claim:
                # Repeat or stale invocation: return existing confirmed order if already reconciled, else conflict
                if order.status == "Confirmed" and order.stock_reserved:
                    return order
                raise HTTPException(409, f"Order is already '{order.status}', cannot reconcile")

            # 4. Deduct aggregated stock only once
            for pid, req_qty in required_by_product.items():
                db.execute(
                    update(Product)
                    .where(Product.id == pid)
                    .values(stock=Product.stock - req_qty)
                )

            add_event(order, "Reconciled to Confirmed by Staff")
            return order
        elif target == "Cancelled":
            claim = db.execute(
                update(Order)
                .where(Order.id == order.id, Order.status == "Payment Review")
                .values(status="Cancelled", payment_status="Refund Pending")
                .execution_options(synchronize_session=False)
            ).rowcount
            db.refresh(order)
            if not claim:
                if order.status == "Cancelled":
                    return order
                raise HTTPException(409, f"Order is already '{order.status}', cannot cancel")
            add_event(order, "Cancelled by Staff for Refund")
            return order
        else:
            raise HTTPException(409, "Payment Review orders can only be reconciled to Confirmed or Cancelled")

    # Handle staff verification and stock reservation for Cash on Delivery orders
    if order.status == "Awaiting Confirmation":
        if target == "Confirmed":
            if order.payment_method != "cod":
                raise HTTPException(409, "Only Cash-on-Delivery orders can be confirmed from Awaiting Confirmation")
            
            # 1. Aggregate required quantities across line items by product_id
            from collections import defaultdict
            required_by_product = defaultdict(int)
            line_names = {}
            for line in order.items:
                if line.product_id:
                    required_by_product[line.product_id] += (line.quantity or 1)
                    line_names[line.product_id] = line.product_name

            # 2. Lock products in consistent sorted order and verify sufficient stock
            sorted_product_ids = sorted(required_by_product.keys())
            insufficient = []
            for pid in sorted_product_ids:
                req_qty = required_by_product[pid]
                product = db.query(Product).filter(Product.id == pid).with_for_update().first()
                if not product or product.stock < req_qty:
                    avail = product.stock if product else 0
                    pname = line_names.get(pid, f"#{pid}")
                    insufficient.append(f"'{pname}' (available: {avail}, required: {req_qty})")

            if insufficient:
                # Rollback uncommitted queries and abort without reserving stock
                db.rollback()
                raise HTTPException(
                    409,
                    f"Cannot confirm COD order: insufficient stock for {', '.join(insufficient)}. Restock items or contact customer."
                )

            # 3. Conditional order-state claim: ensure only one thread can transition the order and reserve stock
            claim = db.execute(
                update(Order)
                .where(
                    Order.id == order.id,
                    Order.status == "Awaiting Confirmation",
                    Order.stock_reserved == False
                )
                .values(stock_reserved=True, status="Confirmed", expires_at=None)
                .execution_options(synchronize_session=False)
            ).rowcount

            db.refresh(order)
            if not claim:
                # Repeat or stale invocation: return existing confirmed order if already reconciled, else conflict
                if order.status == "Confirmed" and order.stock_reserved:
                    return order
                raise HTTPException(409, f"Order is already '{order.status}', cannot confirm")

            # 4. Deduct aggregated stock only once
            for pid, req_qty in required_by_product.items():
                count = db.execute(
                    update(Product)
                    .where(Product.id == pid, Product.stock >= req_qty)
                    .values(stock=Product.stock - req_qty)
                ).rowcount
                if count != 1:
                    db.rollback()
                    raise HTTPException(409, f"Stock changed concurrently for item #{pid}. Cannot confirm COD order.")

            add_event(order, "Confirmed by Staff (COD)")
            return order
        elif target == "Cancelled":
            return cancel_order(db, order)
        else:
            raise HTTPException(409, "Awaiting Confirmation orders can only be confirmed or cancelled")

    allowed = {"Confirmed": "Processing", "Processing": "Shipped", "Shipped": "Out for Delivery", "Out for Delivery": "Delivered"}
    if target == "Cancelled":
        return cancel_order(db, order)
    if allowed.get(order.status) != target:
        raise HTTPException(409, "Invalid fulfillment transition")
    if order.payment_method != "cod" and order.payment_status != "Paid":
        raise HTTPException(409, "Payment must be verified before fulfillment")
    order.status = target
    if target == "Delivered":
        order.delivered_at = utcnow()
        if order.payment_method == "cod":
            order.payment_status = "Paid"  # staff records collection by completing COD delivery
        pts_earned = max(0, int(round(order.total or 0)))
        if pts_earned > 0 and not getattr(order, "rewards_credited", False):
            customer = None
            if order.user_id:
                customer = db.query(User).filter(User.id == order.user_id).first()
            elif order.customer_email:
                customer = db.query(User).filter(User.email.ilike(order.customer_email.strip())).first()
            if customer:
                customer.reward_points = (customer.reward_points or 0) + pts_earned
                add_event(order, f"Reward Points Credited ({pts_earned} pts)")
            order.rewards_credited = True
    add_event(order, target)
    return order

def settle_payment(db, order, reference):
    """Repeated bank events cannot rewind shipment; late payment requires review."""
    if order.payment_status == "Paid":
        return order
    expire_pending_orders(db)
    changed = db.execute(update(Order).where(Order.id == order.id, Order.status == 'Pending', Order.payment_status == 'Pending',
        Order.expires_at > utcnow()).values(payment_status='Paid', transaction_ref=reference, status='Confirmed')
        .execution_options(synchronize_session=False)).rowcount
    db.refresh(order)
    if not changed:
        if order.payment_status == 'Paid':
            return order
        db.execute(update(Order).where(Order.id == order.id, Order.payment_status != 'Paid')
                   .values(payment_status='Paid', transaction_ref=reference, status='Payment Review')
                   .execution_options(synchronize_session=False))
        db.refresh(order)
    add_event(order, order.status)
    return order
