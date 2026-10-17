from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryOut, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=CategoryResponse)
def list_categories(db: Session = Depends(get_db)):
    """Fetch all product categories with accurate product counts."""
    categories = db.query(Category).all()
    out = []
    for c in categories:
        count = db.query(Product).filter(Product.category_id == c.id).count()
        cat_dict = {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "icon": c.icon,
            "image_url": c.image_url,
            "count": count
        }
        out.append(cat_dict)
    
    return {"status": "success", "data": out}

@router.get("/{slug}")
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    """Retrieve single category detail by slug."""
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    count = db.query(Product).filter(Product.category_id == category.id).count()
    return {
        "status": "success",
        "data": {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "description": category.description,
            "icon": category.icon,
            "image_url": category.image_url,
            "count": count
        }
    }
