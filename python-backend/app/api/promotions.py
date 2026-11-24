from datetime import date
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.deps import require_admin
from app.core.database import get_db
from app.models.promotion import Promotion

router = APIRouter(prefix="/promotions", tags=["Promotions"])

class PromotionPayload(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    code: str = Field(min_length=2, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    percent: float = Field(gt=0, le=100)
    max_uses: int = Field(ge=1, default=1000)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Literal['Active', 'Paused'] = 'Active'
    is_featured: bool = False
    image_url: Optional[str] = None

    @field_validator('code')
    @classmethod
    def normalize_code(cls, value):
        return value.strip().replace(' ', '_').upper()

def active_promotion(db, code):
    promo = db.query(Promotion).filter(Promotion.code == code.strip().upper()).first()
    today = date.today()
    if not promo or promo.status != 'Active' or (promo.start_date and today < promo.start_date) or (promo.end_date and today > promo.end_date) or promo.used >= promo.max_uses:
        raise HTTPException(400, 'This promotion is invalid, inactive, expired, or fully redeemed')
    return promo

@router.get('/featured')
def list_featured_promotions(db: Session = Depends(get_db)):
    """Public endpoint to fetch active, featured promotions for storefront hero / deals display."""
    today = date.today()
    promos = db.query(Promotion).filter(
        Promotion.status == 'Active',
        Promotion.is_featured == True
    ).order_by(Promotion.id.desc()).all()
    results = []
    for promo in promos:
        if (promo.start_date and today < promo.start_date) or (promo.end_date and today > promo.end_date) or promo.used >= promo.max_uses:
            continue
        results.append({
            "id": promo.id,
            "name": promo.name,
            "code": promo.code,
            "percent": promo.percent,
            "discount_value": f"{int(promo.percent) if promo.percent.is_integer() else promo.percent}% OFF",
            "image_url": promo.image_url,
            "is_featured": promo.is_featured,
            "max_uses": promo.max_uses,
            "used": promo.used,
            "start_date": promo.start_date.isoformat() if promo.start_date else None,
            "end_date": promo.end_date.isoformat() if promo.end_date else None,
        })
    return {"status": "success", "data": results}

@router.get('/validate/{code}')
def validate_promotion(code: str, db: Session = Depends(get_db)):
    promo = active_promotion(db, code)
    return {'code': promo.code, 'rate': promo.percent / 100}

@router.get('', dependencies=[Depends(require_admin)])
def list_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).order_by(Promotion.id.desc()).all()

def save_promotion(db, payload, promotion=None):
    if payload.start_date and payload.end_date and payload.end_date < payload.start_date:
        raise HTTPException(400, 'End date must follow start date')
    promotion = promotion or Promotion()
    for field, value in payload.model_dump().items():
        setattr(promotion, field, value)
    db.add(promotion)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'This code already exists')
    db.refresh(promotion)
    return promotion

@router.post('', dependencies=[Depends(require_admin)], status_code=201)
def create_promotion(payload: PromotionPayload, db: Session = Depends(get_db)):
    return save_promotion(db, payload)

@router.put('/{promotion_id}', dependencies=[Depends(require_admin)])
def update_promotion(promotion_id: int, payload: PromotionPayload, db: Session = Depends(get_db)):
    promotion = db.get(Promotion, promotion_id)
    if not promotion:
        raise HTTPException(404, 'Promotion not found')
    return save_promotion(db, payload, promotion)

@router.delete('/{promotion_id}', dependencies=[Depends(require_admin)])
def delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = db.get(Promotion, promotion_id)
    if not promotion:
        raise HTTPException(404, 'Promotion not found')
    # Keep redemption history; disable instead of destroying an audited campaign.
    promotion.status = 'Paused'
    db.commit()
    return {'status': 'success'}
