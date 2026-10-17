from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc

from app.core.database import get_db
from app.models.article import Article
from app.schemas.article import (
    ArticleResponse,
    ArticleCreate,
    ArticleUpdate,
    ArticleListResponse,
    ArticleDetailResponse
)

router = APIRouter(prefix="/articles", tags=["Skincare Journal Articles"])

JOURNAL_CATEGORIES = [
    "All",
    "Skincare Basics",
    "Ingredients",
    "Skincare Tips",
    "Sun Care",
    "Acne Care",
    "Anti-Aging",
    "Sensitive Skin"
]

@router.get("", response_model=ArticleListResponse)
def get_articles(
    search: Optional[str] = Query(None, description="Search query across titles and content"),
    category: Optional[str] = Query(None, description="Filter by category slug or name"),
    sort: Optional[str] = Query("latest", description="Sort order: 'latest', 'popular', 'title'"),
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Retrieve paginated Skincare Journal articles with search, category filtering,
    sort options, and popular sidebar items.
    """
    query = db.query(Article)

    # 1. Search filter
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Article.title.ilike(search_fmt),
                Article.subtitle.ilike(search_fmt),
                Article.category.ilike(search_fmt),
                Article.excerpt.ilike(search_fmt)
            )
        )

    # 2. Category filter
    if category and category.lower() != "all":
        query = query.filter(Article.category.ilike(f"%{category.strip()}%"))

    # 3. Sort options
    if sort == "popular":
        query = query.order_by(desc(Article.is_popular), asc(Article.popular_rank), desc(Article.id))
    elif sort == "title":
        query = query.order_by(asc(Article.title))
    else:  # latest
        query = query.order_by(desc(Article.id))

    total = query.count()
    offset = (page - 1) * limit
    articles = query.offset(offset).limit(limit).all()

    # Retrieve popular articles for sidebar widget
    popular_articles = (
        db.query(Article)
        .filter(Article.is_popular == True)
        .order_by(asc(Article.popular_rank), desc(Article.id))
        .limit(4)
        .all()
    )

    return ArticleListResponse(
        success=True,
        total=total,
        data=articles,
        categories=JOURNAL_CATEGORIES,
        popular=popular_articles
    )

@router.get("/popular", response_model=List[ArticleResponse])
def get_popular_articles(db: Session = Depends(get_db)):
    """
    Retrieve top popular articles for widgets and recommendation strips.
    """
    return (
        db.query(Article)
        .filter(Article.is_popular == True)
        .order_by(asc(Article.popular_rank), desc(Article.id))
        .limit(4)
        .all()
    )

@router.get("/{slug}", response_model=ArticleDetailResponse)
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve full article reader view with related articles by slug.
    """
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with slug '{slug}' not found."
        )

    # Related articles (prioritizing same category, excluding current)
    related = (
        db.query(Article)
        .filter(Article.id != article.id)
        .filter(
            or_(
                Article.category == article.category,
                Article.is_popular == True
            )
        )
        .limit(4)
        .all()
    )

    return ArticleDetailResponse(
        success=True,
        data=article,
        related=related
    )

@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    """
    Create a new journal article (Admin Atelier).
    """
    existing = db.query(Article).filter(Article.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Article with slug '{payload.slug}' already exists."
        )

    article = Article(**payload.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.put("/{slug}", response_model=ArticleResponse)
def update_article(slug: str, payload: ArticleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing journal article (Admin Atelier).
    """
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with slug '{slug}' not found."
        )

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(slug: str, db: Session = Depends(get_db)):
    """
    Delete a journal article.
    """
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with slug '{slug}' not found."
        )
    db.delete(article)
    db.commit()
    return None
