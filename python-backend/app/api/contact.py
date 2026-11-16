"""Store customer inquiries durably; never claim an email was sent."""
import secrets
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Session
from app.core.database import Base, get_db
from app.api.deps import require_admin

class SupportMessage(Base):
    __tablename__ = 'support_messages'
    id = Column(Integer, primary_key=True)
    reference = Column(String(40), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ContactPayload(BaseModel):
    firstName: str = Field(min_length=1, max_length=100)
    lastName: str = Field(default='', max_length=100)
    email: EmailStr
    subject: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=5, max_length=5000)
    consent: Literal[True]

router = APIRouter(prefix='/contact', tags=['Support'])

@router.post('', status_code=201)
def create_inquiry(payload: ContactPayload, db: Session = Depends(get_db)):
    reference = 'SUP-' + secrets.token_hex(6).upper()
    db.add(SupportMessage(reference=reference, name=f'{payload.firstName} {payload.lastName}'.strip(),
        email=str(payload.email), subject=payload.subject, message=payload.message))
    db.commit()
    return {'reference': reference, 'message': 'Your inquiry has been received.'}

@router.get('', dependencies=[Depends(require_admin)])
def list_inquiries(db: Session = Depends(get_db)):
    return db.query(SupportMessage).order_by(SupportMessage.id.desc()).limit(100).all()
