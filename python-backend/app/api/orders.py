import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderOut, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

def generate_order_number() -> str:
    """Generates unique alphanumeric order reference like LUM-849201."""
    digits = "".join(random.choices(string.digits, k=6))
    return f"LUM-{digits}"

@router.post("", response_model=OrderResponse, status_code=201)
def place_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """
    Creates a new customer order.
    Calculates subtotal, discounts, and items cleanly.
    """
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    subtotal = 0.0
    order_items_to_create = []

    for item in order_in.items:
        # Determine product name and price
        prod = None
        if item.product_id:
            prod = db.query(Product).filter(Product.id == item.product_id).first()
        
        name = item.product_name or (prod.name if prod else "Skincare Item")
        price = item.price if item.price is not None else (prod.price if prod else 0.0)
        img = prod.image_url if prod else "/images/prod-sk2.jpg"
        qty = max(1, item.quantity)
        line_total = round(price * qty, 2)
        subtotal += line_total

        order_items_to_create.append({
            "product_id": item.product_id or (prod.id if prod else None),
            "product_name": name,
            "image_url": img,
            "price": price,
            "quantity": qty,
            "total": line_total
        })

    subtotal = round(subtotal, 2)

    # Calculate promo discount
    discount = 0.0
    if order_in.discount_code:
        code_upper = order_in.discount_code.upper().strip()
        if "10" in code_upper:
            discount = round(subtotal * 0.10, 2)
        elif "20" in code_upper:
            discount = round(subtotal * 0.20, 2)
        elif "15" in code_upper:
            discount = round(subtotal * 0.15, 2)

    # Shipping fee (Complimentary over $50 threshold, standard $15 otherwise)
    shipping_fee = 0.0 if (subtotal - discount) >= 50.0 else 15.0
    total = max(0.0, round(subtotal - discount + shipping_fee, 2))

    # Create Order
    new_order = Order(
        order_number=generate_order_number(),
        customer_name=order_in.customer_name,
        customer_email=order_in.customer_email,
        customer_phone=order_in.customer_phone,
        shipping_address=order_in.shipping_address,
        shipping_city=order_in.shipping_city,
        shipping_postal_code=order_in.shipping_postal_code,
        subtotal=subtotal,
        discount=discount,
        shipping_fee=shipping_fee,
        total=total,
        status="Confirmed",
        payment_method=order_in.payment_method or "card"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

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

    return {
        "status": "success",
        "message": "Order created successfully",
        "data": new_order
    }

@router.get("/{orderNumber}", response_model=OrderResponse)
def get_order_by_number(orderNumber: str, db: Session = Depends(get_db)):
    """Retrieve full order details by order reference number."""
    order = db.query(Order).filter(Order.order_number == orderNumber).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {orderNumber} not found")

    return {
        "status": "success",
        "data": order
    }

@router.get("", response_model=List[OrderOut])
def list_all_orders(email: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    """List recent orders, optionally filtered by customer email."""
    query = db.query(Order)
    if email:
        query = query.filter(Order.customer_email.ilike(email.strip()))
    return query.order_by(Order.id.desc()).limit(limit).all()
