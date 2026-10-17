from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = "Sparkles"
    image_url: Optional[str] = None

class CategoryOut(CategoryBase):
    id: int
    count: Optional[int] = 0

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    status: str = "success"
    data: List[CategoryOut]
