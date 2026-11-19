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
from typing import List, Optional, Union, Any
from app.core.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.api.settings import load_settings
from app.core.config import settings
from app.services.payway_api import merchant_gateway
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

import math

ATELIER_LAT = 11.5564
ATELIER_LNG = 104.9282

def calculate_haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two GPS coordinates using Haversine formula in kilometers."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def calculate_carrier_shipping_fee(
    carrier_key: str,
    city: str,
    subtotal: float,
    free_threshold: Union[float, dict] = 50.0,
    lat: Optional[float] = None,
    lng: Optional[float] = None
) -> dict:
    """
    Authentic Cambodian Delivery Pricing & Admin-Configurable Free Delivery System:
    - Admin can toggle free delivery ON/OFF, switch modes ('threshold', 'all_orders', 'disabled'),
      and customize threshold amounts ($0, $25, $50, etc.) whenever they want.
    1. VET Logistics (Vireak Buntham): Flat $1.50 Nationwide. Free when qualified.
    2. J&T Express Cambodia: Flat $1.75 Nationwide. Free when qualified.
    3. GrabExpress (Grab): Phnom Penh Only. GPS distance-based fare ($2.00 base + $0.40/km).
       Receives $1.50 delivery credit when free shipping is earned.
    4. Luméa Atelier Concierge: Flat $3.00. Free when qualified.
    """
    carrier_key = (carrier_key or "vet_express").lower()
    c = (city or "Phnom Penh").strip().lower()
    is_phnom_penh = ("phnom penh" in c) or ("khan" in c) or ("bkk" in c) or ("chamkarmon" in c) or ("daun penh" in c) or ("toul kork" in c)

    # Resolve settings configuration
    if isinstance(free_threshold, dict):
        cfg = free_threshold
    else:
        cfg = load_settings()
        if isinstance(free_threshold, (int, float)):
            cfg["free_shipping_threshold"] = float(free_threshold)

    free_enabled = cfg.get("free_shipping_enabled", True)
    free_mode = cfg.get("free_shipping_mode", "threshold")  # "threshold" | "all_orders" | "disabled"
    threshold = float(cfg.get("free_shipping_threshold", 50.0))
    eligible_carriers = cfg.get("free_shipping_carriers", ["vet_express", "jt_express", "lumea_concierge"])
    grab_subsidy = cfg.get("grab_subsidy_enabled", True)

    is_free_qualified = False
    if free_enabled and free_mode != "disabled":
        if free_mode == "all_orders":
            is_free_qualified = True
        elif free_mode == "threshold":
            is_free_qualified = (subtotal >= threshold)

    # 1. Vireak Buntham (VET Logistics) - Flat $1.50 Nationwide
    if carrier_key == "vet_express":
        base_fee = 1.50
        is_free = is_free_qualified and ("vet_express" in eligible_carriers)
        fee = 0.0 if is_free else base_fee
        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": "1–2 Business Days",
            "is_free": is_free,
            "available": True,
            "policy": "Flat nationwide courier: $1.50 to all 25 provinces and Phnom Penh"
        }

    # 2. J&T Express Cambodia - Flat $1.75 Nationwide
    elif carrier_key == "jt_express":
        base_fee = 1.75
        is_free = is_free_qualified and ("jt_express" in eligible_carriers)
        fee = 0.0 if is_free else base_fee
        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": "Next-Day Delivery",
            "is_free": is_free,
            "available": True,
            "policy": "Flat domestic parcel network: $1.75 nationwide"
        }

    # 3. GrabExpress (Grab) - Special distance & Phnom Penh only policy
    elif carrier_key == "grab_express":
        if not is_phnom_penh:
            return {
                "fee": 0.0,
                "base_fee": 0.0,
                "transit": "Phnom Penh Only",
                "is_free": False,
                "available": False,
                "policy": "GrabExpress on-demand motorbike dispatch is available within Phnom Penh only"
            }

        # Dynamic GPS Distance Calculation
        if lat is not None and lng is not None and abs(lat) > 0.001 and abs(lng) > 0.001:
            distance_km = calculate_haversine_km(ATELIER_LAT, ATELIER_LNG, lat, lng)
        else:
            distance_km = 6.5  # Typical Phnom Penh metropolitan radius

        # Base $2.00 up to 3 km, then $0.40 per additional km
        raw_fee = 2.00 + max(0.0, distance_km - 3.0) * 0.40
        base_fee = round(raw_fee, 2)

        # On-demand rush delivery subsidy on qualified orders
        if is_free_qualified and grab_subsidy:
            fee = max(1.50, round(base_fee - 1.50, 2))
            is_free = False
            note = f"Distance: {distance_km} km ($1.50 Free Delivery credit applied)"
        else:
            fee = base_fee
            is_free = False
            note = f"Distance: {distance_km} km (Base $2.00 + $0.40/km)"

        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": f"60–90 Mins ({distance_km} km)",
            "is_free": is_free,
            "available": True,
            "distance_km": distance_km,
            "policy": note
        }

    # 4. Luméa Atelier Concierge - Flat $3.00
    elif carrier_key == "lumea_concierge":
        base_fee = 3.00
        is_free = is_free_qualified and ("lumea_concierge" in eligible_carriers)
        fee = 0.0 if is_free else base_fee
        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": "White-Glove Scheduled",
            "is_free": is_free,
            "available": True,
            "policy": "Signature silk-ribbon presentation"
        }

    else:
        base_fee = 1.50
        is_free = is_free_qualified
        fee = 0.0 if is_free else base_fee
        return {"fee": fee, "base_fee": base_fee, "transit": "1–2 Business Days", "is_free": is_free, "available": True}

CARRIER_RATES = {
    "vet_express": {"name": "Vireak Buntham (VET Logistics)", "fee": 1.50, "transit": "1–2 Business Days", "free_over_threshold": True, "logo": "/images/couriers/vet_express.png"},
    "jt_express": {"name": "J&T Express Cambodia", "fee": 1.75, "transit": "Next-Day Delivery", "free_over_threshold": True, "logo": "/images/couriers/jt_express.png"},
    "grab_express": {"name": "GrabExpress On-Demand", "fee": 3.50, "transit": "60–90 Mins (Phnom Penh)", "free_over_threshold": False, "logo": "/images/couriers/grab_express.png"},
    "lumea_concierge": {"name": "Luméa Atelier Concierge", "fee": 3.00, "transit": "White-Glove Scheduled", "free_over_threshold": True, "logo": None},
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
    settings_data = load_settings()
    
    carrier_key = (getattr(order_in, "shipping_carrier", None) or "vet_express").lower()
    city = getattr(order_in, "shipping_city", "Phnom Penh") or "Phnom Penh"
    lat = getattr(order_in, "delivery_lat", None)
    lng = getattr(order_in, "delivery_lng", None)

    carrier_calc = calculate_carrier_shipping_fee(
        carrier_key=carrier_key,
        city=city,
        subtotal=subtotal,
        free_threshold=settings_data,
        lat=lat,
        lng=lng
    )
    if carrier_key not in CARRIER_RATES or not carrier_calc["available"]:
        raise HTTPException(400, "This courier is unavailable for your delivery address.")
    shipping = money(carrier_calc["fee"])
        
    return dict(subtotal=subtotal, discount=discount, shipping_fee=shipping,
                total=money(subtotal - discount + shipping),
                carrier_info=carrier_calc), lines

@router.get("/carriers")
def list_carriers(
    city: Optional[str] = "Phnom Penh",
    subtotal: Optional[float] = 0.0,
    lat: Optional[float] = None,
    lng: Optional[float] = None
):
    """Returns available Cambodian delivery carriers and dynamic tariffs based on destination and policy."""
    settings_data = load_settings()

    carriers_list = []
    configs = [
        ("vet_express", "Vireak Buntham (VET Logistics)", "Cambodia's #1 nationwide courier service. Direct delivery to all 25 provinces.", "NATIONWIDE #1", "/images/couriers/vet_express.png"),
        ("jt_express", "J&T Express Cambodia", "High-speed door-to-door express parcel courier with real-time automated tracking.", "FAST DOMESTIC", "/images/couriers/jt_express.png"),
        ("grab_express", "GrabExpress On-Demand", "Dedicated instant motorbike courier. 60–90 min direct dispatch from atelier.", "INSTANT EXPRESS", "/images/couriers/grab_express.png"),
        ("lumea_concierge", "Luméa Atelier Concierge", "White-glove luxury delivery in signature silk-ribbon boxes with complimentary samples.", "ATELIER SIGNATURE", None),
    ]

    for cid, name, desc, badge, logo in configs:
        calc = calculate_carrier_shipping_fee(cid, city, subtotal, settings_data, lat, lng)
        carriers_list.append({
            "id": cid,
            "name": name,
            "description": desc,
            "badge": badge,
            "logo": logo,
            "fee": calc["fee"],
            "base_fee": calc["base_fee"],
            "transit": calc["transit"],
            "is_free": calc.get("is_free", False),
            "available": calc.get("available", True),
            "distance_km": calc.get("distance_km"),
            "policy": calc.get("policy", "")
        })

    return {
        "status": "success",
        "data": carriers_list
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
    if settings.PRODUCTION and order_in.payment_method == "khqr" and not merchant_gateway():
        raise HTTPException(503, "KHQR is temporarily unavailable. Choose cash on delivery.")
    quote, order_items_to_create = calculate_quote(order_in, db)
    subtotal, discount, shipping_fee, total = (quote[k] for k in ("subtotal", "discount", "shipping_fee", "total"))
    if order_in.expected_total is None or abs(order_in.expected_total - total) > 0.009:
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
        query = query.filter(Order.user_id == current_user.id)
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
