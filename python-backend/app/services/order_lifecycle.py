"""Shared order ownership, inventory and fulfillment rules."""
import hashlib
import hmac
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import update
from app.models.order import Order
from app.models.product import Product
from app.models.promotion import Promotion
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
    # Preserve account access for legacy records, without granting access to new
    # guest orders on the strength of an unverified email address alone.
    if user and not order.checkout_key and not order.user_id and order.customer_email.lower() == user.email.lower():
        return order
    if token and order.access_token_hash and hmac.compare_digest(hashlib.sha256(token.encode()).hexdigest(), order.access_token_hash):
        return order
    raise HTTPException(404, "Order not found for this session")

def add_event(order, status):
    order.events = [*(order.events or []), {"status": status, "at": utcnow().isoformat() + "Z"}]

def release_stock(db, order):
    """A conditional flag ensures cancelling/expiring twice cannot restock twice."""
    changed = db.execute(update(Order).where(Order.id == order.id, Order.stock_reserved.is_(True))
                         .values(stock_reserved=False).execution_options(synchronize_session=False)).rowcount
    if changed:
        for line in order.items:
            db.execute(update(Product).where(Product.id == line.product_id)
                       .values(stock=Product.stock + line.quantity))
        order.stock_reserved = False
        if order.discount_code:
            db.execute(update(Promotion).where(Promotion.code == order.discount_code, Promotion.used > 0).values(used=Promotion.used - 1))

def expire_pending_orders(db):
    for order in db.query(Order).filter(Order.status == "Pending", Order.expires_at <= utcnow()).all():
        changed = db.execute(update(Order).where(Order.id == order.id, Order.status == 'Pending',
            Order.payment_status == 'Pending', Order.expires_at <= utcnow())
            .values(status='Expired', payment_status='Expired').execution_options(synchronize_session=False)).rowcount
        db.refresh(order)
        if changed:
            add_event(order, "Expired")
            release_stock(db, order)
    db.flush()

def cancel_order(db, order):
    if order.status in ("Cancelled", "Expired"):
        return order
    if order.status not in ("Pending", "Confirmed", "Processing"):
        raise HTTPException(409, "This order has already been dispatched")
    if order.payment_status == "Paid":
        raise HTTPException(409, "A paid order needs a refund review. Contact support before cancellation.")
    changed = db.execute(update(Order).where(Order.id == order.id, Order.status.in_(['Pending', 'Confirmed', 'Processing']),
        Order.payment_status != 'Paid').values(status='Cancelled', payment_status='Cancelled')
        .execution_options(synchronize_session=False)).rowcount
    db.refresh(order)
    if not changed:
        raise HTTPException(409, 'The order changed. Reload before cancelling.')
    add_event(order, "Cancelled")
    release_stock(db, order)
    return order

def transition_order(db, order, target):
    allowed = {"Confirmed": "Processing", "Processing": "Shipped", "Shipped": "Out for Delivery", "Out for Delivery": "Delivered"}
    if target == order.status:
        return order
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
