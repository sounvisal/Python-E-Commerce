from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(String(50), unique=True, index=True, nullable=False)  # e.g., 'home', 'shop', 'deals'
    title = Column(String(255), nullable=False)
    subtitle = Column(Text, nullable=True)
    badge_text = Column(String(100), nullable=True)
    script_text = Column(String(150), nullable=True)  # Calligraphy overlay text
    image_url = Column(String(500), nullable=False)
    cta_text = Column(String(100), nullable=True)
    cta_link = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
