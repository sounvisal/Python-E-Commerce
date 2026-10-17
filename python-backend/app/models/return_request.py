from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from app.core.database import Base

class ReturnRequest(Base):
    __tablename__ = "return_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(50), unique=True, index=True, nullable=False)
    order_number = Column(String(50), index=True, nullable=False)
    customer_name = Column(String(150), default="Sreynich Chan")
    customer_email = Column(String(150), default="sreynich.chan@example.com")
    product_name = Column(String(255), nullable=False)
    product_image = Column(String(500), default="/images/prod-sk2.jpg")
    product_variant = Column(String(100), default="230ml")
    price = Column(Float, default=125.0)
    quantity = Column(Integer, default=1)
    reason = Column(String(150), nullable=False)
    resolution = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    photos = Column(JSON, nullable=True)
    status = Column(String(50), default="approved")
    current_step = Column(Integer, default=3)
    submitted_date = Column(String(50), default="Aug 14, 2024")
    timeline = Column(JSON, nullable=True)
    return_address = Column(
        Text,
        default="Luméa Returns Center, #12 Street 271, Sangkat Toul Tom Poung, Phnom Penh, Cambodia 120801"
    )
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
