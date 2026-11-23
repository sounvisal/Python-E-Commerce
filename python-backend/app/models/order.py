from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(150), nullable=False)
    customer_phone = Column(String(50), nullable=True)
    shipping_address = Column(String(255), nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_postal_code = Column(String(20), nullable=True)
    shipping_carrier = Column(String(100), default="vet_express", nullable=False)
    delivery_lat = Column(Float, nullable=True)
    delivery_lng = Column(Float, nullable=True)
    delivery_notes = Column(String(500), nullable=True)
    map_url = Column(String(255), nullable=True)
    
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    discount_code = Column(String(64), nullable=True)
    shipping_fee = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    status = Column(String(50), default="Confirmed")  # Confirmed, Processing, Shipped, Delivered, Cancelled
    payment_method = Column(String(50), default="card")
    payment_status = Column(String(50), default="Unpaid")  # Paid, Pending, Failed
    transaction_ref = Column(String(100), nullable=True)
    payway_gateway = Column(String(150), nullable=True)
    payway_started_at = Column(DateTime, nullable=True)
    payway_qr = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    checkout_key = Column(String(64), unique=True, nullable=True)
    checkout_fingerprint = Column(String(64), nullable=True)
    access_token_hash = Column(String(64), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    stock_reserved = Column(Boolean, default=False, nullable=False)
    rewards_credited = Column(Boolean, default=False, nullable=False)
    events = Column(JSON, default=list)

    user_rel = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order_rel", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, nullable=True)
    product_name = Column(String(200), nullable=False)
    image_url = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    returned_quantity = Column(Integer, default=0, nullable=False)
    total = Column(Float, nullable=False)

    order_rel = relationship("Order", back_populates="items")
