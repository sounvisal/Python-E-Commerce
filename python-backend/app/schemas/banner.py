from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BannerBase(BaseModel):
    page: str
    title: str
    subtitle: Optional[str] = None
    badge_text: Optional[str] = None
    script_text: Optional[str] = None
    image_url: str
    cta_text: Optional[str] = None
    cta_link: Optional[str] = None
    is_active: bool = True
    display_order: int = 0

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    badge_text: Optional[str] = None
    script_text: Optional[str] = None
    image_url: Optional[str] = None
    cta_text: Optional[str] = None
    cta_link: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class BannerOut(BannerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BannerListResponse(BaseModel):
    status: str = "success"
    data: List[BannerOut]

class SingleBannerResponse(BaseModel):
    status: str = "success"
    data: BannerOut
