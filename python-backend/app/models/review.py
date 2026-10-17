from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    product_image = Column(String(255), nullable=True)
    
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=True)
    customer_avatar = Column(String(255), nullable=True)
    verified_purchase = Column(Boolean, default=True)
    
    rating = Column(Integer, nullable=False, default=5) # 1 to 5 stars
    title = Column(String(255), nullable=False)
    comment = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="approved", index=True) # approved, pending, rejected
    
    helpful_count = Column(Integer, default=0)
    admin_reply = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    product_rel = relationship("Product", foreign_keys=[product_id])
