import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

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
    "free_shipping_threshold": 50.0,
    "tax_rate": 10.0,
    "online_status": "Online",
    "maintenance_mode": False,
    "last_updated": datetime.now(timezone.utc).strftime("%b %d, %Y %I:%M %p")
}

def load_settings() -> Dict[str, Any]:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()

def save_settings(data: Dict[str, Any]):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Load into memory on module import
current_settings = load_settings()

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
    free_shipping_threshold: Optional[float] = None
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
            "free_shipping_threshold": s.get("free_shipping_threshold", 50.0),
            "tax_rate": s.get("tax_rate", 10.0),
            "online_status": s.get("online_status", "Online")
        }
    }

@router.put("")
def update_settings(payload: SettingsUpdatePayload):
    """
    Update store configuration and persist to disk.
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
        "message": "Store configuration updated and persisted to disk",
        "data": s
    }
