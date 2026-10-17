from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from typing import Optional, List
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductListResponse, SingleProductResponse, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=ProductListResponse)
def list_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = "popular",
    skin_type: Optional[str] = None,
    skin_concern: Optional[str] = None,
    featured: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Search, filter, and paginate products.
    Matches all filter criteria from Luméa Vue frontend.
    """
    query = db.query(Product)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.brand.ilike(search_pattern),
                Product.description.ilike(search_pattern),
            )
        )

    if category and category != "all":
        query = query.filter(Product.category == category)

    if brand:
        brands_list = [b.strip() for b in brand.split(",") if b.strip()]
        if brands_list:
            query = query.filter(Product.brand.in_(brands_list))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if featured is not None:
        query = query.filter(Product.is_featured == featured)

    # Sorting
    if sort == "price-asc" or sort == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort == "price-desc" or sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "rating":
        query = query.order_by(desc(Product.rating), desc(Product.reviews))
    elif sort == "newest":
        query = query.order_by(desc(Product.id))
    else:  # popular / default
        query = query.order_by(desc(Product.reviews), desc(Product.rating))

    total = query.count()
    products = query.offset(offset).limit(limit).all()

    # Filter client-side JSON attributes if requested (for SQLite JSON compatibility)
    result = []
    for p in products:
        if skin_type and p.skin_type and skin_type not in p.skin_type:
            continue
        if skin_concern and p.skin_concern and skin_concern not in p.skin_concern:
            continue
        result.append(p)

    return {
        "status": "success",
        "count": len(result),
        "data": result
    }

@router.get("/featured", response_model=ProductListResponse)
def get_featured_products(limit: int = 8, db: Session = Depends(get_db)):
    """Retrieve signature / featured products for homepage."""
    products = db.query(Product).filter(Product.is_featured == True).limit(limit).all()
    if not products:
        products = db.query(Product).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(products),
        "data": products
    }

@router.get("/{slug}", response_model=SingleProductResponse)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    """Retrieve full product details by slug, including 4 related products."""
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Find related products in the same category
    related = (
        db.query(Product)
        .filter(Product.category == product.category, Product.id != product.id)
        .limit(4)
        .all()
    )

    return {
        "status": "success",
        "data": product,
        "related": related
    }
