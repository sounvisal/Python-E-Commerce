from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    first_name = Column(String(75), nullable=True)
    last_name = Column(String(75), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True, default="/images/avatars/avatar-default.png")
    role = Column(String(30), default="customer")  # customer, admin
    tier = Column(String(50), default="Member")
    reward_points = Column(Integer, default=0)
    profile_data = Column(JSON, default=dict)
    token_version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="user_rel")
