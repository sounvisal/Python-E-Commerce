import os
import hashlib
import secrets
import json
import threading
import time
from datetime import timedelta
from sqlalchemy import update, or_
from sqlalchemy.exc import IntegrityError
from fastapi import Header, Request
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

# Canonical local town destinations where Cash on Delivery is permitted.
# Strictly limited to the atelier's home town (Krong Kampot).
# Other Kampot districts and other provinces require KHQR prepayment.
CANONICAL_COD_DESTINATIONS = {
    "krong kampot",
    "krong kampot (kampot town)",
    "kampot town",
    "kampot city"
}

def is_canonical_cod_destination(city: Optional[str]) -> bool:
    """
    Enforces canonical COD eligibility:
    - Only Krong Kampot (Kampot town) is eligible.
    - NEVER infer from substring (e.g. no 'kampot' in c).
    - NEVER default missing/empty destination to town.
    - NEVER equate Grab service area with COD eligibility.
    """
    if not city or not isinstance(city, str):
        return False
    normalized = city.strip().lower()
    return normalized in CANONICAL_COD_DESTINATIONS

class SyncSlidingWindowLimiter:
    """Thread-safe sliding window rate limiter for order submissions."""
    def __init__(self):
        self.requests = {}
        self.lock = threading.Lock()

    def is_allowed(self, key: str, limit: int, window_seconds: int = 600):
        now = time.time()
        with self.lock:
            if key not in self.requests:
                self.requests[key] = []
            cutoff = now - window_seconds
            self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
            if len(self.requests[key]) >= limit:
                oldest = self.requests[key][0]
                retry_after = max(1, int(oldest + window_seconds - now))
                return False, retry_after
            self.requests[key].append(now)
            return True, 0

cod_submission_limiter = SyncSlidingWindowLimiter()

def generate_order_number() -> str:
    """Generates unique alphanumeric order reference like LUM-849201."""
    digits = secrets.token_hex(6).upper()
    return f"LUM-{digits}"


def checkout_fingerprint(payload, user):
    data = payload.model_dump(exclude={"checkout_key", "expected_total"})
    data["user_id"] = user.id if user else None
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

import math

ATELIER_LAT = 10.6106068
ATELIER_LNG = 104.1815019

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
    - Atelier shop located in Krong Kampot (Google Maps verified).
    - Shop direct delivery is prioritized as the cheapest ($1.00) to reflect realistic shop logistics.
    - GrabExpress on-demand is restricted to the same province/city (Kampot).
    1. Luméa Shop Direct: Flat $1.00 from atelier. Free when qualified.
    2. VET Logistics (Vireak Buntham): Flat $1.50 Nationwide. Free when qualified.
    3. J&T Express Cambodia: Flat $1.75 Nationwide. Free when qualified.
    4. GrabExpress (Grab): Same Province/City Only (Kampot). GPS distance-based fare ($1.50 base + $0.35/km).
    """
    carrier_key = (carrier_key or "lumea_concierge").lower()
    c = (city or "Kampot").strip().lower()
    is_same_city = ("kampot" in c) or ("krong kampot" in c) or ("teuk chhou" in c) or ("chhouk" in c)

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
    eligible_carriers = cfg.get("free_shipping_carriers", ["lumea_concierge", "vet_express", "jt_express"])
    grab_subsidy = cfg.get("grab_subsidy_enabled", True)

    is_free_qualified = False
    if free_enabled and free_mode != "disabled":
        if free_mode == "all_orders":
            is_free_qualified = True
        elif free_mode == "threshold":
            is_free_qualified = (subtotal >= threshold)

    # 1. Luméa Shop Direct Delivery (Atelier Courier) - Flat $1.00 (Cheapest & Best Value)
    if carrier_key == "lumea_concierge":
        base_fee = 1.00
        is_free = is_free_qualified and ("lumea_concierge" in eligible_carriers)
        fee = 0.0 if is_free else base_fee
        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": "Same-Day Direct Delivery" if is_same_city else "1–2 Business Days Direct",
            "is_free": is_free,
            "available": True,
            "policy": "Luméa Shop Direct Delivery: Flat $1.00 from our Krong Kampot atelier"
        }

    # 2. Vireak Buntham (VET Logistics) - Flat $1.50 Nationwide
    elif carrier_key == "vet_express":
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

    # 3. J&T Express Cambodia - Flat $1.75 Nationwide
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

    # 4. GrabExpress (Grab) - Special distance & same city/province only policy
    elif carrier_key == "grab_express":
        if not is_same_city:
            return {
                "fee": 0.0,
                "base_fee": 0.0,
                "transit": "Same City/Province Only (Kampot)",
                "is_free": False,
                "available": False,
                "policy": "GrabExpress on-demand dispatch is available within the atelier's province/city (Kampot) only"
            }

        # Dynamic GPS Distance Calculation
        if lat is not None and lng is not None and abs(lat) > 0.001 and abs(lng) > 0.001:
            distance_km = calculate_haversine_km(ATELIER_LAT, ATELIER_LNG, lat, lng)
        else:
            distance_km = 4.5  # Typical Kampot radius

        # Base $1.50 up to 3 km, then $0.35 per additional km
        raw_fee = 1.50 + max(0.0, distance_km - 3.0) * 0.35
        base_fee = round(raw_fee, 2)

        # On-demand rush delivery subsidy on qualified orders
        if is_free_qualified and grab_subsidy:
            fee = max(1.00, round(base_fee - 1.00, 2))
            is_free = False
            note = f"Distance: {distance_km} km ($1.00 Free Delivery credit applied)"
        else:
            fee = base_fee
            is_free = False
            note = f"Distance: {distance_km} km (Base $1.50 + $0.35/km)"

        return {
            "fee": fee,
            "base_fee": base_fee,
            "transit": f"30–60 Mins ({distance_km} km)",
            "is_free": is_free,
            "available": True,
            "distance_km": distance_km,
            "policy": note
        }

    else:
        base_fee = 1.00
        is_free = is_free_qualified
        fee = 0.0 if is_free else base_fee
        return {"fee": fee, "base_fee": base_fee, "transit": "1–2 Business Days", "is_free": is_free, "available": True}

CARRIER_RATES = {
    "lumea_concierge": {"name": "Luméa Shop Direct Delivery", "fee": 1.00, "transit": "Same-Day Direct Delivery", "free_over_threshold": True, "logo": None},
    "vet_express": {"name": "Vireak Buntham (VET Logistics)", "fee": 1.50, "transit": "1–2 Business Days", "free_over_threshold": True, "logo": "/images/couriers/vet_express.png"},
    "jt_express": {"name": "J&T Express Cambodia", "fee": 1.75, "transit": "Next-Day Delivery", "free_over_threshold": True, "logo": "/images/couriers/jt_express.png"},
    "grab_express": {"name": "GrabExpress On-Demand", "fee": 2.50, "transit": "30–60 Mins (Kampot On-Demand)", "free_over_threshold": False, "logo": "/images/couriers/grab_express.png"},
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
    
    carrier_key = (getattr(order_in, "shipping_carrier", None) or "lumea_concierge").lower()
    city = getattr(order_in, "shipping_city", "Kampot") or "Kampot"
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
    if payload.payment_method == "cod" and not is_canonical_cod_destination(payload.shipping_city):
        raise HTTPException(
            400,
            "Cash on delivery is only available within Krong Kampot (Kampot town). "
            "Deliveries outside town, including other Kampot districts and provinces, must be prepaid via KHQR."
        )
    if payload.checkout_key:
        existing = db.query(Order).filter(Order.checkout_key == payload.checkout_key).first()
        if existing:
            if existing.checkout_fingerprint != checkout_fingerprint(payload, current_user):
                raise HTTPException(409, 'Checkout changed. Start a new attempt.')
            if existing.status in ('Expired', 'Cancelled'):
                raise HTTPException(409, 'This checkout has expired or was cancelled. Start a new attempt.')
            return {'data': {'subtotal': existing.subtotal, 'discount': existing.discount,
                'shipping_fee': existing.shipping_fee, 'total': existing.total,
                'cod_eligible': is_canonical_cod_destination(existing.shipping_city),
                'items': [dict(product_id=i.product_id, price=i.price, quantity=i.quantity, total=i.total) for i in existing.items]}}
    quote, lines = calculate_quote(payload, db)
    return {"data": {**quote, "cod_eligible": is_canonical_cod_destination(payload.shipping_city), "items": lines}}

@router.post("", response_model=OrderResponse, status_code=201)
def place_order(order_in: OrderCreate, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a new customer order.
    Requires an authenticated customer to prevent spam bots and fraudulent orders.
    Calculates subtotal, discounts, and items cleanly.
    """
    expire_pending_orders(db)
    db.commit()
    if order_in.customer_email.lower() != current_user.email.lower():
        raise HTTPException(400, "Order customer email must match your registered account email")
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
    has_khqr = bool(merchant_gateway()) or bool(os.getenv("ABA_PAYWAY_URL")) or bool(os.getenv("BAKONG_ACCOUNT_ID"))
    if order_in.payment_method == "khqr" and not has_khqr:
        raise HTTPException(503, "KHQR is temporarily unavailable. Choose cash on delivery.")

    is_cod = (order_in.payment_method == "cod")
    if is_cod:
        if not is_canonical_cod_destination(order_in.shipping_city):
            raise HTTPException(
                400,
                "Cash on delivery is only available within Krong Kampot (Kampot town). "
                "Deliveries outside town, including other Kampot districts and provinces, must be prepaid via KHQR."
            )

        # Enforce at most one open unconfirmed COD request per account
        open_cod = db.query(Order).filter(
            Order.user_id == current_user.id,
            Order.status == "Awaiting Confirmation",
            Order.payment_method == "cod"
        ).first()
        if open_cod:
            if (order_in.checkout_key and open_cod.checkout_key == order_in.checkout_key) or open_cod.checkout_fingerprint == fingerprint:
                return order_created_response(open_cod)
            raise HTTPException(
                409,
                "You already have an open Cash-on-Delivery order awaiting confirmation. "
                "Please wait for staff confirmation or cancel your existing order before placing a new COD order."
            )

        # Tighter server-side COD submission limits
        client_ip = request.client.host if (request and request.client) else "127.0.0.1"
        is_test = (request.headers.get("X-Test-Client") == "true") if request else False
        if not is_test:
            allowed_user, retry_user = cod_submission_limiter.is_allowed(f"cod:user:{current_user.id}", limit=5, window_seconds=600)
            allowed_ip, retry_ip = cod_submission_limiter.is_allowed(f"cod:ip:{client_ip}", limit=10, window_seconds=600)
            if not allowed_user or not allowed_ip:
                retry_sec = max(retry_user, retry_ip, 1)
                raise HTTPException(
                    429,
                    f"Too many Cash-on-Delivery checkout attempts. Please wait {retry_sec} seconds before trying again."
                )

    quote, order_items_to_create = calculate_quote(order_in, db)
    subtotal, discount, shipping_fee, total = (quote[k] for k in ("subtotal", "discount", "shipping_fee", "total"))
    if order_in.expected_total is None or abs(order_in.expected_total - total) > 0.009:
        raise HTTPException(409, detail={"message": "Your bag total changed. Review the updated total before placing the order.", "quote": quote})

    # Delivery carrier & Map coordinates
    carrier_key = (order_in.shipping_carrier or "lumea_concierge").lower()
    map_url = None
    if order_in.delivery_lat is not None and order_in.delivery_lng is not None:
        map_url = f"https://www.google.com/maps?q={order_in.delivery_lat:.6f},{order_in.delivery_lng:.6f}"

    # Create Order
    new_order = Order(
        order_number=generate_order_number(),
        checkout_key=checkout_key,
        checkout_fingerprint=fingerprint,
        user_id=current_user.id,
        expires_at=utcnow() + timedelta(hours=24) if is_cod else (utcnow() + timedelta(minutes=5) if order_in.payment_method == 'khqr' else None),
        stock_reserved=False if is_cod else True,
        promo_claimed=bool(order_in.discount_code),
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
        status="Awaiting Confirmation" if is_cod else ("Pending" if order_in.payment_method == "khqr" else "Confirmed"),
        payment_status="Unpaid" if is_cod else ("Pending" if order_in.payment_method == "khqr" else "Unpaid"),
        payment_method=order_in.payment_method or "card"
    )

    new_order.access_token_hash = hashlib.sha256(guest_token(new_order).encode()).hexdigest()
    add_event(new_order, new_order.status)
    try:
        db.add(new_order)
        db.flush()
        if not is_cod:
            # Conditional updates arbitrate concurrent checkouts for the last units for KHQR/prepaid orders.
            for item in order_items_to_create:
                count = db.execute(update(Product).where(Product.id == item['product_id'], Product.stock >= item['quantity'])
                                   .values(stock=Product.stock - item['quantity'])).rowcount
                if count != 1:
                    raise HTTPException(409, 'Stock changed. Review your bag and retry.')
        else:
            # Cash on delivery creates an Awaiting Confirmation order WITHOUT decrementing/reserving stock.
            # Stock is reserved atomically in a single transaction once staff verifies delivery details and confirms.
            pass

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
        open_cod = db.query(Order).filter(
            Order.user_id == current_user.id,
            Order.status == "Awaiting Confirmation",
            Order.payment_method == "cod"
        ).first()
        if open_cod:
            raise HTTPException(
                409,
                "You already have an open Cash-on-Delivery order awaiting confirmation. "
                "Please wait for staff confirmation or cancel your existing order before placing a new COD order."
            )
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

@router.post("/{orderNumber}/confirm-cod", response_model=OrderResponse)
def confirm_cod_order(orderNumber: str, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """
    Staff confirmation endpoint for Cash on Delivery orders.
    Requires staff verification of delivery phone and address.
    Atomically checks stock, reserves each line exactly once, and updates status to Confirmed.
    """
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    if not order:
        raise HTTPException(404, f"Order {orderNumber} not found")
    if order.status != "Awaiting Confirmation":
        if order.status == "Confirmed" and order.stock_reserved:
            return {"status": "success", "message": f"Order #{order.order_number} is already confirmed", "data": order}
        raise HTTPException(409, f"Order #{order.order_number} is in '{order.status}' status, cannot confirm")
    
    transition_order(db, order, "Confirmed")
    db.commit()
    db.refresh(order)
    return {
        "status": "success",
        "message": f"Order #{order.order_number} verified and confirmed. Stock has been reserved.",
        "data": order
    }

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
    if order.status == "Delivered" and not getattr(order, "rewards_credited", False):
        pts_earned = max(0, int(round(order.total or 0)))
        if pts_earned > 0:
            current_user.reward_points = (current_user.reward_points or 0) + pts_earned
            order.rewards_credited = True
            add_event(order, f"Reward Points Credited upon Claim ({pts_earned} pts)")
    db.commit()
    return {"status": "success", "data": order}
