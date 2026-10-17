from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func
from app.core.database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    tagline = Column(String(255), nullable=True)
    country = Column(String(100), default="South Korea")
    country_code = Column(String(10), default="KR")
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    story = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    banner_url = Column(String(255), nullable=True)
    story_video_url = Column(String(500), nullable=True)     # Brand masterclass / heritage film URL
    story_video_title = Column(String(255), nullable=True)   # e.g. "The Art of Fermentation: SK-II Pitera Masterclass"
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
