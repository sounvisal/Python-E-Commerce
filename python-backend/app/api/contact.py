"""Store customer inquiries durably; never claim an email was sent."""
import secrets
from datetime import datetime, timezone
from typing import Literal, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, text, inspect
from sqlalchemy.orm import Session
from app.core.database import Base, get_db, engine
from app.api.deps import require_admin

class SupportMessage(Base):
    __tablename__ = 'support_messages'
    id = Column(Integer, primary_key=True)
    reference = Column(String(40), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(50), default='pending')
    admin_reply = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

def ensure_support_message_columns():
    """Ensure newly introduced columns exist in SQLite/PostgreSQL."""
    try:
        insp = inspect(engine)
        if 'support_messages' in insp.get_table_names():
            cols = [c['name'] for c in insp.get_columns('support_messages')]
            with engine.connect() as conn:
                if 'status' not in cols:
                    conn.execute(text("ALTER TABLE support_messages ADD COLUMN status VARCHAR(50) DEFAULT 'pending'"))
                if 'admin_reply' not in cols:
                    conn.execute(text("ALTER TABLE support_messages ADD COLUMN admin_reply TEXT"))
                conn.commit()
    except Exception as e:
        print(f"[SupportMessage] Column ensure check note: {e}")

# Run column ensure on module load
ensure_support_message_columns()

class ContactPayload(BaseModel):
    firstName: str = Field(min_length=1, max_length=100)
    lastName: str = Field(default='', max_length=100)
    email: EmailStr
    subject: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=5, max_length=5000)
    consent: Literal[True]

class InquiryStatusPayload(BaseModel):
    status: str = Field(..., pattern="^(pending|replied|resolved)$")
    admin_reply: Optional[str] = None

router = APIRouter(prefix='/contact', tags=['Support'])

@router.post('', status_code=201)
def create_inquiry(payload: ContactPayload, db: Session = Depends(get_db)):
    reference = 'SUP-' + secrets.token_hex(6).upper()
    db.add(SupportMessage(
        reference=reference,
        name=f'{payload.firstName} {payload.lastName}'.strip(),
        email=str(payload.email),
        subject=payload.subject,
        message=payload.message,
        status='pending'
    ))
    db.commit()
    return {'reference': reference, 'message': 'Your inquiry has been received.'}

@router.get('', dependencies=[Depends(require_admin)])
def list_inquiries(db: Session = Depends(get_db)):
    inquiries = db.query(SupportMessage).order_by(SupportMessage.id.desc()).limit(150).all()
    # Normalize null statuses
    return [
        {
            "id": i.id,
            "reference": i.reference,
            "name": i.name,
            "email": i.email,
            "subject": i.subject,
            "message": i.message,
            "status": i.status or "pending",
            "admin_reply": i.admin_reply or "",
            "created_at": i.created_at.isoformat() if i.created_at else datetime.now(timezone.utc).isoformat()
        }
        for i in inquiries
    ]

@router.patch('/{inquiry_id}/status', dependencies=[Depends(require_admin)])
def update_inquiry_status(inquiry_id: int, payload: InquiryStatusPayload, db: Session = Depends(get_db)):
    inquiry = db.query(SupportMessage).filter(SupportMessage.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail=f"Inquiry #{inquiry_id} not found")
    
    inquiry.status = payload.status
    if payload.admin_reply is not None:
        inquiry.admin_reply = payload.admin_reply
    
    db.commit()
    db.refresh(inquiry)
    return {
        "status": "success",
        "message": f"Inquiry status updated to {payload.status}",
        "data": {
            "id": inquiry.id,
            "reference": inquiry.reference,
            "status": inquiry.status,
            "admin_reply": inquiry.admin_reply
        }
    }

@router.delete('/{inquiry_id}', dependencies=[Depends(require_admin)])
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(SupportMessage).filter(SupportMessage.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail=f"Inquiry #{inquiry_id} not found")
    
    db.delete(inquiry)
    db.commit()
    return {"status": "success", "message": f"Inquiry #{inquiry_id} deleted"}

@router.post('/seed-demo', dependencies=[Depends(require_admin)])
def seed_demo_inquiries(db: Session = Depends(get_db)):
    """Seed demo inquiries for testing the concierge admin workspace."""
    demo_samples = [
        SupportMessage(
            reference="SUP-7A19F2",
            name="Sophea Vichea",
            email="sophea.vichea@example.com",
            subject="Skincare Routine Advice: Retinol + Vitamin C Layering",
            message="Hello Luméa Atelier team! I recently ordered the Botanical Dew Elixir and the Vitamin C Illuminating Serum. Should I apply Vitamin C during my morning ritual and reserve Retinol for nighttime, or can I combine them?",
            status="pending"
        ),
        SupportMessage(
            reference="SUP-8C42E1",
            name="Linda Meas",
            email="linda.meas@example.com",
            subject="Delivery Status for Express Phnom Penh Order #LM24081234",
            message="Hi! I chose same-day concierge delivery for my order this morning to BKK1. Could you confirm if the courier will call 15 minutes before arrival at my residence?",
            status="replied",
            admin_reply="Warm greetings Linda! Yes, our Luméa Atelier courier will phone you approximately 15 minutes prior to arrival. Your package is currently out for delivery."
        ),
        SupportMessage(
            reference="SUP-3D90B4",
            name="David Heng",
            email="david.heng@example.com",
            subject="Wedding Atelier Gift Sets & Custom Silk Packaging",
            message="We are planning our wedding favor boxes for next month and would love to prepare 20 bespoke discovery kits with luxury silk packaging and custom gift notes. Do you offer corporate / bridal party concierge packaging?",
            status="pending"
        ),
        SupportMessage(
            reference="SUP-5F11A9",
            name="Thavy Sok",
            email="thavy.sok@example.com",
            subject="Stock Restock Timeline for SK-II Treatment Essence 230ml",
            message="Good afternoon, I wanted to check when the 230ml SK-II Facial Treatment Essence will be replenished? I'm subscribed to the notification alert but wanted to verify if it will arrive before Friday.",
            status="resolved",
            admin_reply="Hello Thavy! Fresh batch stock has just cleared customs and is now available on our storefront with complimentary express delivery."
        ),
        SupportMessage(
            reference="SUP-9B38D7",
            name="Chantou Rath",
            email="chantou.rath@example.com",
            subject="Sensitive Skin Formulation & Fragrance Inquiry",
            message="I have reactive rosacea skin and wanted to verify if your Centella Asiatica Calming Toner contains any artificial fragrance or essential oils before placing my first atelier order?",
            status="pending"
        )
    ]
    db.add_all(demo_samples)
    db.commit()
    return {"status": "success", "message": f"Seeded {len(demo_samples)} demo inquiries"}
