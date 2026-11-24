from app.api.deps import require_admin
import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import Depends, APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.dialects.postgresql import insert
from app.core.config import settings
from app.core.database import Base, SessionLocal

router = APIRouter(prefix="/settings", tags=["Store Settings"])

SETTINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "seed", "store_settings.json"))

DEFAULT_SETTINGS: Dict[str, Any] = {
    # 1. General Info
    "store_name": "Luméa Botanical Atelier",
    "store_email": "support@lumea.com",
    "store_phone": "+855 12 345 678",
    "store_language": "English (Default)",
    "store_description": "Contemporary Clinical Skincare & Botanical Beauty Atelier. Natural beauty, clinically proven results.",
    "company_name": "Luméa Co., Ltd.",
    "business_reg_number": "KH-123456789",
    "business_address": "#123, Norodom Blvd, Phnom Penh, Cambodia",
    "time_zone": "(UTC+07:00) Phnom Penh",
    "currency": "USD ($)",
    "currency_symbol": "$",
    "store_logo": "/images/logo-lumea.png",
    "store_favicon": "/favicon.ico",
    "online_status": "Online",
    "maintenance_mode": False,

    # 2. Store Operations
    "order_prefix": "LM-",
    "low_stock_threshold": 5,
    "auto_confirm_orders": True,
    "allow_backorders": False,
    "cart_expiration_minutes": 30,

    # 3. Payment Methods
    "payment_methods": {
        "aba_pay": {
            "enabled": True,
            "merchant_name": "LUMEA ATELIER",
            "merchant_id": "lumea_khqr@aba",
            "test_mode": False
        },
        "credit_card": {
            "enabled": True,
            "test_mode": False,
            "require_3ds": True
        },
        "cod": {
            "enabled": True,
            "max_amount": 250.0,
            "area": "all"
        },
        "wing": {
            "enabled": True,
            "account": "+855 12 345 678"
        }
    },

    # 4. Shipping & Delivery
    "free_shipping_enabled": True,
    "free_shipping_mode": "threshold",  # "threshold" | "all_orders" | "disabled"
    "free_shipping_threshold": 50.0,
    "free_shipping_promo_text": "Complimentary nationwide shipping on orders over $50",
    "free_shipping_carriers": ["lumea_concierge", "vet_express", "jt_express"],
    "grab_subsidy_enabled": True,

    # 5. Taxes & Compliance
    "tax_rate": 10.0,
    "tax_inclusive": False,
    "tax_id_number": "K008-902341254",
    "auto_invoice": True,

    # 6. Notifications
    "notifications": {
        "order_confirmation_email": True,
        "shipping_updates_email": True,
        "return_status_email": True,
        "admin_low_stock_email": True,
        "admin_notification_email": "ops@lumea.com",
        "telegram_alerts": True
    },

    # 7. Staff & Permissions
    "staff_members": [
        {
            "id": 1,
            "name": "Sreynich Chan",
            "email": "sreynich.chan@example.com",
            "role": "Super Admin · Full Access",
            "avatar": "/images/avatar-sreynich.jpg",
            "status": "Active"
        },
        {
            "id": 2,
            "name": "Luméa Operations",
            "email": "ops@lumea.com",
            "role": "Store Manager",
            "avatar": "/images/avatars/avatar-default.png",
            "status": "Active"
        },
        {
            "id": 3,
            "name": "Sokunthea Keo",
            "email": "sokunthea@lumea.com",
            "role": "Customer Care Specialist",
            "avatar": "/images/avatar-clientele-2.jpg",
            "status": "Active"
        }
    ],

    # 8. Integrations
    "integrations": {
        "google_analytics_id": "G-LUMEA2026",
        "facebook_pixel_id": "9876543210123",
        "telegram_bot_token": "bot612849102:AAE-lumea-secure-token",
        "telegram_chat_id": "@lumea_atelier_orders",
        "telegram_enabled": True,
        "klaviyo_api_key": "pk_live_lumea_botanical"
    },

    # 9. SEO & Social
    "seo": {
        "meta_title": "Luméa — Luxury Clinical Skincare & Botanical Atelier",
        "meta_description": "Discover pure, clinically backed botanical skincare crafted to nurture skin barrier resilience and reveal radiant luminescence.",
        "og_image": "/images/banner-home.jpg",
        "canonical_url": "https://lumeastore.vercel.app",
        "indexing_enabled": True
    },

    # 10. Appearance & Branding
    "appearance": {
        "announcement_enabled": True,
        "announcement_text": "Complimentary nationwide shipping on orders over $50 | 100% Authentic Guaranteed",
        "primary_brand_color": "#84261B",
        "products_per_page": 12,
        "show_stock_badge": True,
        "show_discount_badge": True
    },

    # 11. Legal & Policies
    "legal": {
        "return_policy_days": 14,
        "warranty_guarantee": "100% Authenticity Guarantee or Full Refund",
        "support_hours": "Mon - Sun: 8:00 AM - 9:00 PM (ICT)"
    },

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
    model_config = ConfigDict(extra="allow")

    store_name: Optional[str] = None
    store_email: Optional[str] = None
    store_phone: Optional[str] = None
    store_language: Optional[str] = None
    store_description: Optional[str] = None
    store_logo: Optional[str] = None
    store_favicon: Optional[str] = None
    company_name: Optional[str] = None
    business_reg_number: Optional[str] = None
    business_address: Optional[str] = None
    time_zone: Optional[str] = None
    currency: Optional[str] = None
    free_shipping_enabled: Optional[bool] = None
    free_shipping_mode: Optional[str] = None
    free_shipping_threshold: Optional[float] = None
    free_shipping_promo_text: Optional[str] = None
    free_shipping_carriers: Optional[list] = None
    grab_subsidy_enabled: Optional[bool] = None
    tax_rate: Optional[float] = None
    online_status: Optional[str] = None
    maintenance_mode: Optional[bool] = None

@router.get("")
def get_public_settings():
    """
    Public endpoint: Get active store configuration.
    Used by Storefront Cart, Header, Checkout, and Footer.
    """
    s = load_settings()
    announcement_cfg = s.get("appearance", {})
    return {
        "status": "success",
        "data": {
            **s,
            "currency_symbol": s.get("currency_symbol", "$"),
            "free_shipping_threshold": float(s.get("free_shipping_threshold", 50.0)),
            "tax_rate": float(s.get("tax_rate", 10.0)),
            "announcement_enabled": announcement_cfg.get("announcement_enabled", True) if isinstance(announcement_cfg, dict) else True,
            "announcement_text": announcement_cfg.get("announcement_text", s.get("free_shipping_promo_text", "")) if isinstance(announcement_cfg, dict) else ""
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
