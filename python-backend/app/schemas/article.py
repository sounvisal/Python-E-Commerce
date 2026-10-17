from typing import Optional, Any, Dict, List
from datetime import datetime
from pydantic import BaseModel

class ArticleBase(BaseModel):
    slug: str
    title: str
    subtitle: Optional[str] = None
    category: str
    read_time: Optional[str] = "5 min read"
    views_count: Optional[str] = "10.5K views"
    author_name: Optional[str] = "Sophea Meas"
    author_role: Optional[str] = "Skincare Expert"
    author_avatar: Optional[str] = "/images/avatar-sreynich.jpg"
    published_at: Optional[str] = "Aug 28, 2025"
    hero_image: str
    thumbnail: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    toc: Optional[List[Dict[str, Any]]] = None
    is_featured: bool = False
    is_popular: bool = False
    popular_rank: Optional[int] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    category: Optional[str] = None
    read_time: Optional[str] = None
    views_count: Optional[str] = None
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    author_avatar: Optional[str] = None
    published_at: Optional[str] = None
    hero_image: Optional[str] = None
    thumbnail: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    toc: Optional[List[Dict[str, Any]]] = None
    is_featured: Optional[bool] = None
    is_popular: Optional[bool] = None
    popular_rank: Optional[int] = None

class ArticleResponse(ArticleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ArticleDetailResponse(BaseModel):
    success: bool = True
    data: ArticleResponse
    related: List[ArticleResponse]

class ArticleListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[ArticleResponse]
    categories: List[str]
    popular: List[ArticleResponse]
