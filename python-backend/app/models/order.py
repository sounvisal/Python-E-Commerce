from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
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
    
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    shipping_fee = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    status = Column(String(50), default="Confirmed")  # Confirmed, Processing, Shipped, Delivered, Cancelled
    payment_method = Column(String(50), default="card")
    payment_status = Column(String(50), default="Paid")  # Paid, Pending, Failed
    transaction_ref = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
    total = Column(Float, nullable=False)

    order_rel = relationship("Order", back_populates="items")
