import hashlib
import secrets
import json
from datetime import timedelta
from sqlalchemy import update, or_
from sqlalchemy.exc import IntegrityError
from fastapi import Header
from app.api.deps import get_optional_user, get_current_user, require_admin
from app.models.user import User
from app.services.order_lifecycle import (utcnow, guest_token, check_order_access, expire_pending_orders, cancel_order, transition_order, add_event)
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.api.settings import load_settings
from app.core.config import settings
from app.api.promotions import active_promotion
from app.models.promotion import Promotion
from decimal import Decimal, ROUND_HALF_UP
from app.schemas.order import OrderCreate, OrderOut, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

class OrderStatusUpdatePayload(BaseModel):
    status: str

def generate_order_number() -> str:
    """Generates unique alphanumeric order reference like LUM-849201."""
    digits = secrets.token_hex(6).upper()
    return f"LUM-{digits}"


def checkout_fingerprint(payload, user):
    data = payload.model_dump(exclude={"checkout_key", "expected_total"})
    data["user_id"] = user.id if user else None
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

CARRIER_RATES = {
    "vet_express": {"name": "Vireak Buntham (VET Logistics)", "fee": 1.50, "transit": "1–2 Business Days", "free_over_threshold": True},
    "jt_express": {"name": "J&T Express Cambodia", "fee": 1.75, "transit": "Next-Day Delivery", "free_over_threshold": True},
    "grab_express": {"name": "GrabExpress On-Demand", "fee": 3.50, "transit": "60–90 Mins (Phnom Penh)", "free_over_threshold": False},
    "lumea_concierge": {"name": "Luméa Atelier Concierge", "fee": 3.00, "transit": "White-Glove Scheduled", "free_over_threshold": True},
}

def money(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def calculate_quote(order_in: OrderCreate, db: Session):
    """Resolve all line prices from the catalog. Tax is included in catalog prices."""
    if not order_in.items:
        raise HTTPException(400, "Your bag is empty")
    lines = []
    requested = {}
    for item in order_in.items:
        prod = db.get(Product, item.product_id)
        if not prod or prod.price <= 0:
            raise HTTPException(400, "A product is no longer available. Remove it from your bag.")
        requested[prod.id] = requested.get(prod.id, 0) + item.quantity
        if requested[prod.id] > prod.stock:
            raise HTTPException(409, f"Only {prod.stock} units of {prod.name} are available")
        lines.append(dict(product_id=prod.id, product_name=prod.name, image_url=prod.image_url,
                          price=money(prod.price), quantity=item.quantity, total=money(prod.price * item.quantity)))
    subtotal = money(sum(line["total"] for line in lines))
    code = (order_in.discount_code or "").strip().upper()
    promotion = active_promotion(db, code) if code else None
    discount = money(subtotal * (promotion.percent / 100 if promotion else 0))
    settings = load_settings()
    free_threshold = float(settings.get("free_shipping_threshold", 50.0))
    
    carrier_key = (getattr(order_in, "shipping_carrier", None) or "vet_express").lower()
    carrier = CARRIER_RATES.get(carrier_key, CARRIER_RATES["vet_express"])
    if subtotal >= free_threshold and carrier["free_over_threshold"]:
        shipping = 0.0
    else:
        shipping = carrier["fee"]
        
    return dict(subtotal=subtotal, discount=discount, shipping_fee=shipping,
                total=money(subtotal - discount + shipping)), lines

@router.get("/carriers")
def list_carriers():
    """Returns available Cambodian delivery carriers and current tariffs."""
    return {
        "status": "success",
        "data": [
            {
                "id": "vet_express",
                "name": "Vireak Buntham (VET Logistics)",
                "description": "Cambodia's #1 nationwide courier service. Direct delivery to all 25 provinces.",
                "fee": 1.50,
                "transit": "1–2 Business Days",
                "badge": "Nationwide",
                "icon": "truck"
            },
            {
                "id": "jt_express",
                "name": "J&T Express Cambodia",
                "description": "High-speed door-to-door express parcel courier with real-time van tracking.",
                "fee": 1.75,
                "transit": "Next-Day Delivery",
                "badge": "Popular",
                "icon": "package"
            },
            {
                "id": "grab_express",
                "name": "GrabExpress On-Demand",
                "description": "Dedicated motorbike courier. Immediate dispatch for urgent beauty orders.",
                "fee": 3.50,
                "transit": "60–90 Mins (Phnom Penh)",
                "badge": "Instant Express",
                "icon": "zap"
            },
            {
                "id": "lumea_concierge",
                "name": "Luméa Atelier Concierge",
                "description": "Hand-delivered luxury package with signature ribbon, tissue, and samples.",
                "fee": 3.00,
                "transit": "White-Glove Scheduled",
                "badge": "Luxury Signature",
                "icon": "sparkles"
            }
        ]
    }

@router.post("/quote")
def quote_order(payload: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_optional_user)):
    expire_pending_orders(db)
    db.commit()
    if payload.checkout_key:
        existing = db.query(Order).filter(Order.checkout_key == payload.checkout_key).first()
        if existing:
            if existing.checkout_fingerprint != checkout_fingerprint(payload, current_user):
                raise HTTPException(409, 'Checkout changed. Start a new attempt.')
            if existing.status in ('Expired', 'Cancelled'):
                raise HTTPException(409, 'This checkout has expired or was cancelled. Start a new attempt.')
            return {'data': {'subtotal': existing.subtotal, 'discount': existing.discount,
                'shipping_fee': existing.shipping_fee, 'total': existing.total,
                'items': [dict(product_id=i.product_id, price=i.price, quantity=i.quantity, total=i.total) for i in existing.items]}}
    quote, lines = calculate_quote(payload, db)
    return {"data": {**quote, "items": lines}}

@router.post("", response_model=OrderResponse, status_code=201)
def place_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user)):
    """
    Creates a new customer order.
    Calculates subtotal, discounts, and items cleanly.
    """
    expire_pending_orders(db)
    db.commit()
    if current_user and order_in.customer_email.lower() != current_user.email.lower():
        raise HTTPException(400, "Use your account email for this order")
    checkout_key = order_in.checkout_key or secrets.token_urlsafe(32)
    fingerprint = checkout_fingerprint(order_in, current_user)
    existing = db.query(Order).filter(Order.checkout_key == checkout_key).first()
    if existing:
        if existing.checkout_fingerprint != fingerprint:
            raise HTTPException(409, "Checkout changed. Start a new checkout attempt.")
        if existing.status in ("Expired", "Cancelled"):
            raise HTTPException(409, "This checkout expired or was cancelled. Start a new attempt.")
        return order_created_response(existing)
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    if order_in.payment_method not in ("khqr", "cod"):
        raise HTTPException(400, "This payment method is not available. Choose KHQR or cash on delivery.")
    quote, order_items_to_create = calculate_quote(order_in, db)
    subtotal, discount, shipping_fee, total = (quote[k] for k in ("subtotal", "discount", "shipping_fee", "total"))
    if order_in.expected_total is not None and abs(order_in.expected_total - total) > 0.009:
        raise HTTPException(409, detail={"message": "Your bag total changed. Review the updated total before placing the order.", "quote": quote})

    # Delivery carrier & Map coordinates
    carrier_key = (order_in.shipping_carrier or "vet_express").lower()
    map_url = None
    if order_in.delivery_lat is not None and order_in.delivery_lng is not None:
        map_url = f"https://www.google.com/maps?q={order_in.delivery_lat:.6f},{order_in.delivery_lng:.6f}"

    # Create Order
    new_order = Order(
        order_number=generate_order_number(),
        checkout_key=checkout_key,
        checkout_fingerprint=fingerprint,
        user_id=current_user.id if current_user else None,
        expires_at=utcnow() + timedelta(minutes=5) if order_in.payment_method == 'khqr' else None,
        stock_reserved=True,
        customer_name=order_in.customer_name,
        customer_email=order_in.customer_email,
        customer_phone=order_in.customer_phone,
        shipping_address=order_in.shipping_address,
        shipping_city=order_in.shipping_city,
        shipping_postal_code=order_in.shipping_postal_code,
        shipping_carrier=carrier_key,
        delivery_lat=order_in.delivery_lat,
        delivery_lng=order_in.delivery_lng,
        delivery_notes=(order_in.delivery_notes or "").strip() or None,
        map_url=map_url,
        subtotal=subtotal,
        discount=discount,
        discount_code=(order_in.discount_code or '').strip().upper() or None,
        shipping_fee=shipping_fee,
        total=total,
        status="Pending" if order_in.payment_method == "khqr" else "Confirmed",
        payment_status="Pending" if order_in.payment_method == "khqr" else "Unpaid",
        payment_method=order_in.payment_method or "card"
    )

    new_order.access_token_hash = hashlib.sha256(guest_token(new_order).encode()).hexdigest()
    add_event(new_order, new_order.status)
    try:
        db.add(new_order)
        db.flush()
        # Conditional updates arbitrate concurrent checkouts for the last units.
        for item in order_items_to_create:
            count = db.execute(update(Product).where(Product.id == item['product_id'], Product.stock >= item['quantity'])
                               .values(stock=Product.stock - item['quantity'])).rowcount
            if count != 1:
                raise HTTPException(409, 'Stock changed. Review your bag and retry.')
        if new_order.discount_code:
            count = db.execute(update(Promotion).where(Promotion.code == new_order.discount_code, Promotion.used < Promotion.max_uses)
                               .values(used=Promotion.used + 1)).rowcount
            if count != 1:
                raise HTTPException(409, 'This promotion is fully redeemed')
    except IntegrityError:
        db.rollback()
        existing = db.query(Order).filter(Order.checkout_key == checkout_key).first()
        if existing and existing.checkout_fingerprint == fingerprint:
            return order_created_response(existing)
        raise HTTPException(409, 'Checkout conflict. Please retry.')
    except Exception:
        db.rollback()
        raise

    # Add Order Items
    for item_data in order_items_to_create:
        oi = OrderItem(
            order_id=new_order.id,
            product_id=item_data["product_id"],
            product_name=item_data["product_name"],
            image_url=item_data["image_url"],
            price=item_data["price"],
            quantity=item_data["quantity"],
            total=item_data["total"]
        )
        db.add(oi)

    db.commit()
    db.refresh(new_order)

    return order_created_response(new_order)

def order_created_response(order):
    data = OrderOut.model_validate(order).model_dump()
    data['access_token'] = guest_token(order)
    return {"status": "success", "message": "Order created successfully", "data": data}

@router.get("/{orderNumber}", response_model=OrderResponse)
def get_order_by_number(orderNumber: str, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """Retrieve full order details by order reference number."""
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {orderNumber} not found")

    check_order_access(order, current_user, order_token)
    expire_pending_orders(db)
    db.commit()
    return {"status": "success", "data": order}

@router.patch("/{orderNumber}/status", response_model=OrderResponse)
def update_order_status_by_number(orderNumber: str, payload: OrderStatusUpdatePayload, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Updates the fulfillment status of an order by its reference number.
    Used for courier tracking simulation, admin dispatch, and live status progression.
    """
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {orderNumber} not found")

    transition_order(db, order, payload.status)
    db.commit()
    db.refresh(order)

    return {
        "status": "success",
        "message": f"Order #{order.order_number} status updated to {order.status}",
        "data": order
    }

@router.get("", response_model=List[OrderOut])
def list_all_orders(email: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List recent orders, optionally filtered by customer email."""
    query = db.query(Order)
    expire_pending_orders(db)
    db.commit()
    if current_user.role != 'admin':
        query = query.filter(or_(Order.user_id == current_user.id,
            (Order.user_id.is_(None) & Order.checkout_key.is_(None) & (Order.customer_email == current_user.email))))
    elif email:
        query = query.filter(Order.customer_email == email.strip())
    return query.order_by(Order.id.desc()).limit(limit).all()

@router.post("/{orderNumber}/cancel", response_model=OrderResponse)
def cancel_customer_order(orderNumber: str, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    check_order_access(order, current_user, order_token)
    cancel_order(db, order)
    db.commit()
    return {"status": "success", "data": order}

@router.post("/{orderNumber}/claim", response_model=OrderResponse)
def claim_guest_order(orderNumber: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    check_order_access(order, None, order_token)
    if order.customer_email.lower() != current_user.email.lower() or (order.user_id and order.user_id != current_user.id):
        raise HTTPException(403, "Use the account email entered at checkout")
    order.user_id = current_user.id
    db.commit()
    return {"status": "success", "data": order}
