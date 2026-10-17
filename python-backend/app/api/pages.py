from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.page import Page
from app.schemas.page import PageResponse, PageCreate, PageUpdate, PageListResponse

router = APIRouter(prefix="/pages", tags=["CMS Pages"])

@router.get("", response_model=PageListResponse)
def get_pages(
    is_published: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """
    Retrieve all published CMS pages.
    """
    query = db.query(Page)
    if is_published is not None:
        query = query.filter(Page.is_published == is_published)
    pages = query.order_by(Page.title.asc()).all()
    return PageListResponse(success=True, total=len(pages), data=pages)

@router.get("/{slug}", response_model=PageResponse)
def get_page_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific CMS page by its slug (e.g., 'privacy-policy', 'terms-of-service', 'sustainability').
    """
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with slug '{slug}' not found."
        )
    return page

@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(payload: PageCreate, db: Session = Depends(get_db)):
    """
    Create a new CMS page (used by Admin Atelier).
    """
    existing = db.query(Page).filter(Page.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Page with slug '{payload.slug}' already exists."
        )
    page = Page(
        slug=payload.slug,
        title=payload.title,
        subtitle=payload.subtitle,
        badge_text=payload.badge_text,
        script_text=payload.script_text,
        hero_image=payload.hero_image,
        last_updated=payload.last_updated,
        content_json=payload.content_json,
        is_published=payload.is_published
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return page

@router.put("/{slug}", response_model=PageResponse)
def update_page(slug: str, payload: PageUpdate, db: Session = Depends(get_db)):
    """
    Update an existing CMS page (used by Admin Atelier).
    """
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with slug '{slug}' not found."
        )
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(page, key, value)
    db.commit()
    db.refresh(page)
    return page

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_page(slug: str, db: Session = Depends(get_db)):
    """
    Delete a CMS page.
    """
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with slug '{slug}' not found."
        )
    db.delete(page)
    db.commit()
    return None
