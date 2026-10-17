from sqlalchemy import Column, Integer, String, DateTime
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
    avatar = Column(String(255), nullable=True, default="/images/avatar-sreynich.jpg")
    role = Column(String(30), default="customer")  # customer, admin
    tier = Column(String(50), default="Luméa Radiant Gold")
    reward_points = Column(Integer, default=100)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="user_rel")
