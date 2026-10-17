from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.banner import Banner
from app.schemas.banner import (
    BannerOut,
    BannerCreate,
    BannerUpdate,
    BannerListResponse,
    SingleBannerResponse
)

router = APIRouter(prefix="/banners", tags=["Banners"])

@router.get("", response_model=BannerListResponse)
def list_banners(
    page: Optional[str] = Query(None, description="Filter by page identifier (e.g. 'home', 'deals')"),
    active_only: bool = Query(True, description="Only return active banners"),
    db: Session = Depends(get_db)
):
    """
    Retrieve banner configurations.
    Returns all active banners or filtered by page name.
    """
    query = db.query(Banner)
    if active_only:
        query = query.filter(Banner.is_active == True)
    if page:
        query = query.filter(Banner.page == page)
    
    banners = query.order_by(Banner.display_order.asc(), Banner.id.asc()).all()
    return BannerListResponse(status="success", data=banners)

@router.get("/{identifier}", response_model=SingleBannerResponse)
def get_banner(
    identifier: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific banner either by page slug (e.g. 'home', 'best-sellers')
    or by numeric primary key ID.
    """
    banner = None
    if identifier.isdigit():
        banner = db.query(Banner).filter(Banner.id == int(identifier)).first()
    
    if not banner:
        banner = db.query(Banner).filter(Banner.page == identifier).first()

    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Banner with identifier '{identifier}' was not found"
        )
    return SingleBannerResponse(status="success", data=banner)

@router.post("", response_model=SingleBannerResponse, status_code=status.HTTP_201_CREATED)
def create_banner(
    payload: BannerCreate,
    db: Session = Depends(get_db)
):
    """
    Create or register a new page banner.
    """
    existing = db.query(Banner).filter(Banner.page == payload.page).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A banner for page '{payload.page}' already exists. Use PUT to update it."
        )

    banner = Banner(**payload.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return SingleBannerResponse(status="success", data=banner)

@router.put("/{identifier}", response_model=SingleBannerResponse)
def update_banner(
    identifier: str,
    payload: BannerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update banner configuration (title, subtitle, image_url, etc.) by page slug or ID.
    """
    banner = None
    if identifier.isdigit():
        banner = db.query(Banner).filter(Banner.id == int(identifier)).first()
    
    if not banner:
        banner = db.query(Banner).filter(Banner.page == identifier).first()

    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Banner '{identifier}' was not found"
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(banner, field, value)

    db.commit()
    db.refresh(banner)
    return SingleBannerResponse(status="success", data=banner)

@router.delete("/{identifier}", status_code=status.HTTP_200_OK)
def delete_banner(
    identifier: str,
    db: Session = Depends(get_db)
):
    """
    Remove or deactivate a banner by page slug or ID.
    """
    banner = None
    if identifier.isdigit():
        banner = db.query(Banner).filter(Banner.id == int(identifier)).first()
    if not banner:
        banner = db.query(Banner).filter(Banner.page == identifier).first()

    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Banner '{identifier}' was not found"
        )

    db.delete(banner)
    db.commit()
    return {"status": "success", "message": f"Banner '{identifier}' deleted successfully"}
