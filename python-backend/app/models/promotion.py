from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.core.database import Base

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    code = Column(String(64), unique=True, nullable=False)
    percent = Column(Float, nullable=False)
    max_uses = Column(Integer, default=1000, nullable=False)
    used = Column(Integer, default=0, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(20), default="Active", nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    image_url = Column(String(500), nullable=True)
