from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel

class PageBase(BaseModel):
    slug: str
    title: str
    subtitle: Optional[str] = None
    badge_text: Optional[str] = None
    script_text: Optional[str] = None
    hero_image: Optional[str] = None
    last_updated: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    is_published: bool = True

class PageCreate(PageBase):
    pass

class PageUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    badge_text: Optional[str] = None
    script_text: Optional[str] = None
    hero_image: Optional[str] = None
    last_updated: Optional[str] = None
    content_json: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None

class PageResponse(PageBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PageListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[PageResponse]
