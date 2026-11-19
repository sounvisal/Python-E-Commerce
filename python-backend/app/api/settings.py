from app.api.deps import require_admin
import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.dialects.postgresql import insert
from app.core.config import settings
from app.core.database import Base, SessionLocal

router = APIRouter(prefix="/settings", tags=["Store Settings"])

SETTINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "seed", "store_settings.json"))

DEFAULT_SETTINGS = {
    "store_name": "Luméa Atelier",
    "store_email": "support@lumea.com",
    "store_phone": "+855 12 345 678",
    "store_language": "English (Default)",
    "store_description": "Contemporary Skincare & Beauty Atelier. Natural beauty, clinically proven results.",
    "company_name": "Luméa Co., Ltd.",
    "business_reg_number": "KH-123456789",
    "business_address": "#123, Norodom Blvd, Phnom Penh, Cambodia",
    "time_zone": "(UTC+07:00) Phnom Penh",
    "currency": "USD ($)",
    "currency_symbol": "$",
    "free_shipping_enabled": True,
    "free_shipping_mode": "threshold",  # "threshold" | "all_orders" | "disabled"
    "free_shipping_threshold": 50.0,
    "free_shipping_promo_text": "Complimentary nationwide shipping on orders over $50",
    "free_shipping_carriers": ["vet_express", "jt_express", "lumea_concierge"],
    "grab_subsidy_enabled": True,
    "tax_rate": 10.0,
    "online_status": "Online",
    "maintenance_mode": False,
    "last_updated": datetime.now(timezone.utc).strftime("%b %d, %Y %I:%M %p")
}

class StoreConfiguration(Base):
    __tablename__ = "store_configuration"

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)


def load_settings() -> Dict[str, Any]:
    if settings.PRODUCTION:
        with SessionLocal() as db:
            stored = db.get(StoreConfiguration, 1)
            return {**DEFAULT_SETTINGS, **(stored.data if stored else {})}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(data: Dict[str, Any]):
    if settings.PRODUCTION:
        statement = insert(StoreConfiguration).values(id=1, data=data)
        with SessionLocal.begin() as db:
            db.execute(statement.on_conflict_do_update(index_elements=["id"], set_={"data": statement.excluded.data}))
        return
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class SettingsUpdatePayload(BaseModel):
    store_name: Optional[str] = None
    store_email: Optional[str] = None
    store_phone: Optional[str] = None
    store_language: Optional[str] = None
    store_description: Optional[str] = None
    company_name: Optional[str] = None
    business_reg_number: Optional[str] = None
    business_address: Optional[str] = None
    time_zone: Optional[str] = None
    currency: Optional[str] = None
    free_shipping_enabled: Optional[bool] = None
    free_shipping_mode: Optional[str] = None  # "threshold", "all_orders", "disabled"
    free_shipping_threshold: Optional[float] = None
    free_shipping_promo_text: Optional[str] = None
    free_shipping_carriers: Optional[list] = None
    grab_subsidy_enabled: Optional[bool] = None
    tax_rate: Optional[float] = None
    online_status: Optional[str] = None

@router.get("")
def get_public_settings():
    """
    Public endpoint: Get active store configuration.
    Used by Storefront Cart, Checkout, and Header.
    """
    s = load_settings()
    return {
        "status": "success",
        "data": {
            "store_name": s.get("store_name"),
            "store_email": s.get("store_email"),
            "store_phone": s.get("store_phone"),
            "currency": s.get("currency"),
            "currency_symbol": s.get("currency_symbol", "$"),
            "free_shipping_enabled": s.get("free_shipping_enabled", True),
            "free_shipping_mode": s.get("free_shipping_mode", "threshold"),
            "free_shipping_threshold": float(s.get("free_shipping_threshold", 50.0)),
            "free_shipping_promo_text": s.get("free_shipping_promo_text", "Complimentary nationwide shipping on orders over $50"),
            "free_shipping_carriers": s.get("free_shipping_carriers", ["vet_express", "jt_express", "lumea_concierge"]),
            "grab_subsidy_enabled": s.get("grab_subsidy_enabled", True),
            "tax_rate": s.get("tax_rate", 10.0),
            "online_status": s.get("online_status", "Online")
        }
    }

@router.put("", dependencies=[Depends(require_admin)])
def update_settings(payload: SettingsUpdatePayload):
    """
    Update persistent store configuration.
    """
    s = load_settings()
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        if v is not None:
            s[k] = v
    s["last_updated"] = datetime.now(timezone.utc).strftime("%b %d, %Y %I:%M %p")
    save_settings(s)

    return {
        "status": "success",
        "message": "Store configuration saved",
        "data": s
    }
