from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from app.core.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    target_audience = Column(String(100), default="All Audiences")
    badge = Column(String(50), default="Skin Type")
    level = Column(String(50), default="Beginner")
    cover_image = Column(String(255), default="/images/quiz-model.jpg")
    status = Column(String(50), default="active") # active, draft, archived
    
    questions_count = Column(Integer, default=6)
    completions = Column(Integer, default=0)
    completion_rate = Column(String(20), default="72.3%")
    
    # JSON structure storing questions, choices, and recommendation mappings
    questions_data = Column(JSON, default=list)
    settings = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
