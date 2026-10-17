from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False, index=True) # category slug for easy querying
    category_name = Column(String(100), nullable=False)
    subcategory = Column(String(100), nullable=True)
    product_type = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float, nullable=True)
    rating = Column(Float, default=5.0)
    reviews = Column(Integer, default=0)
    badge = Column(String(50), nullable=True)
    badge_type = Column(String(50), nullable=True)
    stock = Column(Integer, default=50)
    image_url = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_featured = Column(Boolean, default=False)
    
    # JSON columns for multi-select attributes
    skin_type = Column(JSON, default=list)       # e.g. ["Normal", "Dry", "Sensitive"]
    skin_concern = Column(JSON, default=list)    # e.g. ["Acne & Blemishes", "Dullness"]
    gallery = Column(JSON, default=list)         # List of additional image URLs

    category_rel = relationship("Category", back_populates="products")
