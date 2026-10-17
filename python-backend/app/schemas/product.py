from pydantic import BaseModel
from typing import Optional, List, Any

class ProductBase(BaseModel):
    name: str
    brand: str
    slug: str
    category: str
    category_name: str
    subcategory: Optional[str] = None
    product_type: Optional[str] = None
    price: float
    compare_at_price: Optional[float] = None
    rating: Optional[float] = 5.0
    reviews: Optional[int] = 0
    badge: Optional[str] = None
    badge_type: Optional[str] = None
    stock: Optional[int] = 50
    image_url: str
    description: Optional[str] = None
    is_featured: Optional[bool] = False
    skin_type: Optional[List[str]] = []
    skin_concern: Optional[List[str]] = []
    gallery: Optional[List[str]] = []
    video_url: Optional[str] = None
    video_thumbnail: Optional[str] = None
    video_title: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    status: str = "success"
    count: int
    data: List[ProductOut]

class SingleProductResponse(BaseModel):
    status: str = "success"
    data: ProductOut
    related: Optional[List[ProductOut]] = []
