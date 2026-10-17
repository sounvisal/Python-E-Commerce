from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.models.review import Review
from app.models.product import Product

router = APIRouter(prefix="/reviews", tags=["Customer Reviews"])

class ReviewSubmission(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=2, max_length=150)
    comment: str = Field(..., min_length=5, max_length=2000)
    customer_name: Optional[str] = "Luméa Patron"
    customer_email: Optional[str] = "patron@example.com"
    customer_avatar: Optional[str] = "/images/avatar-sreynich.jpg"

@router.get("")
def get_public_reviews(
    product_id: Optional[int] = Query(None, description="Filter reviews by product ID"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter reviews by rating"),
    limit: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """
    Public endpoint: Get approved customer reviews with star breakdowns.
    Used by Storefront Product Details page and Reviews widgets.
    """
    query = db.query(Review).filter(Review.status == "approved")

    if product_id is not None:
        query = query.filter(Review.product_id == product_id)
    if rating is not None:
        query = query.filter(Review.rating == rating)

    total_count = query.count()
    skip = (page - 1) * limit
    reviews = query.order_by(desc(Review.created_at)).offset(skip).limit(limit).all()

    # Calculate metrics for the target product (or overall)
    all_approved = db.query(Review).filter(Review.status == "approved")
    if product_id is not None:
        all_approved = all_approved.filter(Review.product_id == product_id)
    
    total_approved = all_approved.count()
    avg_rating = db.query(func.avg(Review.rating)).filter(Review.status == "approved")
    if product_id is not None:
        avg_rating = avg_rating.filter(Review.product_id == product_id)
    avg_rating_val = round(float(avg_rating.scalar() or 5.0), 1)

    # 5-star distribution breakdown
    distribution = {}
    for star in range(5, 0, -1):
        star_count = all_approved.filter(Review.rating == star).count()
        pct = round((star_count / total_approved * 100), 1) if total_approved > 0 else 0
        distribution[str(star)] = {"count": star_count, "percentage": pct}

    return {
        "status": "success",
        "data": reviews,
        "metrics": {
            "total_reviews": total_approved,
            "average_rating": avg_rating_val,
            "distribution": distribution
        },
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total_count,
            "total_pages": max(1, (total_count + limit - 1) // limit)
        }
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_review(payload: ReviewSubmission, db: Session = Depends(get_db)):
    """
    Customer submission from Storefront: Creates a new review pending Atelier moderation.
    """
    # Lookup product details
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    product_name = product.name if product else "Luméa Skincare Formulation"
    product_image = product.image_url if product else "/images/prod-sk2.jpg"

    new_review = Review(
        product_id=payload.product_id,
        product_name=product_name,
        product_image=product_image,
        customer_name=payload.customer_name or "Verified Customer",
        customer_email=payload.customer_email or "customer@lumea.com",
        customer_avatar=payload.customer_avatar or "/images/avatar-sreynich.jpg",
        verified_purchase=True,
        rating=payload.rating,
        title=payload.title,
        comment=payload.comment,
        status="approved",  # auto-approved for instant satisfaction, editable by admin
        helpful_count=0
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "status": "success",
        "message": "Thank you! Your review has been recorded.",
        "data": new_review
    }

@router.post("/{review_id}/helpful")
def vote_helpful(review_id: int, db: Session = Depends(get_db)):
    """
    Mark a review as helpful on the storefront.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.helpful_count = (review.helpful_count or 0) + 1
    db.commit()

    return {
        "status": "success",
        "helpful_count": review.helpful_count
    }
