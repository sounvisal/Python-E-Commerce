from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from app.core.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    subtitle = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # e.g. "Skincare Basics", "Ingredients", "Sun Care"
    read_time = Column(String(50), default="5 min read")
    views_count = Column(String(50), default="10.5K views")
    author_name = Column(String(150), default="Sophea Meas")
    author_role = Column(String(150), default="Skincare Expert")
    author_avatar = Column(String(500), default="/images/avatar-sreynich.jpg")
    published_at = Column(String(100), default="Aug 28, 2025")
    hero_image = Column(String(500), nullable=False)
    thumbnail = Column(String(500), nullable=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    toc = Column(JSON, nullable=True)
    is_featured = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False)
    popular_rank = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
