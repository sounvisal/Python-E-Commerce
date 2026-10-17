import random
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.return_request import ReturnRequest
from app.schemas.return_request import (
    ReturnRequestResponse,
    ReturnRequestCreate,
    ReturnRequestUpdateStatus,
    ReturnRequestListResponse
)

router = APIRouter(prefix="/returns", tags=["Returns & Refunds"])

DEFAULT_TIMELINE_STAGES = [
    { "id": 1, "title": "Submitted", "date": "Aug 14, 2024", "status": "completed" },
    { "id": 2, "title": "Under Review", "date": "Aug 15, 2024", "status": "completed" },
    { "id": 3, "title": "Approved", "date": "Aug 16, 2024", "status": "current" },
    { "id": 4, "title": "Return in Transit", "date": "Pending", "status": "upcoming" },
    { "id": 5, "title": "Item Received", "date": "Pending", "status": "upcoming" },
    { "id": 6, "title": "Refund Processing", "date": "Pending", "status": "upcoming" },
    { "id": 7, "title": "Refund Completed", "date": "Pending", "status": "upcoming" }
]

@router.get("", response_model=ReturnRequestListResponse)
def get_return_requests(
    order_number: Optional[str] = None,
    customer_email: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve all return requests, optionally filtered by order_number or customer_email.
    """
    query = db.query(ReturnRequest)
    if order_number:
        query = query.filter(ReturnRequest.order_number == order_number)
    if customer_email:
        query = query.filter(ReturnRequest.customer_email == customer_email)
    
    requests = query.order_by(desc(ReturnRequest.id)).all()
    return ReturnRequestListResponse(success=True, total=len(requests), data=requests)

@router.get("/{request_id}", response_model=ReturnRequestResponse)
def get_return_request(request_id: str, db: Session = Depends(get_db)):
    """
    Lookup return request progress and timeline by request number (e.g. 'RR24081234') or ID.
    """
    clean_id = request_id.strip()
    if clean_id.startswith("#"):
        clean_id = clean_id[1:]

    req = db.query(ReturnRequest).filter(
        (ReturnRequest.request_number == clean_id) |
        (ReturnRequest.request_number == f"#{clean_id}") |
        (ReturnRequest.id == int(clean_id) if clean_id.isdigit() else False)
    ).first()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Return request '{request_id}' not found."
        )
    return req

@router.post("", response_model=ReturnRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_return_request(payload: ReturnRequestCreate, db: Session = Depends(get_db)):
    """
    Submit an interactive return request from the 5-step wizard.
    Generates a unique #RR reference number and initializes tracking timeline.
    """
    now = datetime.now()
    date_str = now.strftime("%b %d, %Y")
    random_digits = f"{random.randint(100000, 999999)}"
    request_number = f"RR{now.strftime('%y%m')}{random_digits[:4]}"

    initial_timeline = [
        { "id": 1, "title": "Submitted", "date": date_str, "status": "completed" },
        { "id": 2, "title": "Under Review", "date": "In Progress", "status": "current" },
        { "id": 3, "title": "Approved", "date": "Pending", "status": "upcoming" },
        { "id": 4, "title": "Return in Transit", "date": "Pending", "status": "upcoming" },
        { "id": 5, "title": "Item Received", "date": "Pending", "status": "upcoming" },
        { "id": 6, "title": "Refund Processing", "date": "Pending", "status": "upcoming" },
        { "id": 7, "title": "Refund Completed", "date": "Pending", "status": "upcoming" }
    ]

    new_request = ReturnRequest(
        request_number=request_number,
        order_number=payload.order_number,
        customer_name=payload.customer_name or "Sreynich Chan",
        customer_email=payload.customer_email or "sreynich.chan@example.com",
        product_name=payload.product_name,
        product_image=payload.product_image or "/images/prod-sk2.jpg",
        product_variant=payload.product_variant or "230ml",
        price=payload.price or 125.0,
        quantity=payload.quantity or 1,
        reason=payload.reason,
        resolution=payload.resolution,
        description=payload.description or "",
        photos=payload.photos or ["/images/returns-workflow-bottles.jpg"],
        status="Under Review",
        current_step=2,
        submitted_date=date_str,
        timeline=initial_timeline,
        return_address="Luméa Returns Center, #12 Street 271, Sangkat Toul Tom Poung, Phnom Penh, Cambodia 120801"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.patch("/{request_id}/status", response_model=ReturnRequestResponse)
def update_return_status(
    request_id: str,
    payload: ReturnRequestUpdateStatus,
    db: Session = Depends(get_db)
):
    """
    Update return status and progression (used by Admin Atelier).
    """
    clean_id = request_id.strip().lstrip("#")
    req = db.query(ReturnRequest).filter(
        (ReturnRequest.request_number == clean_id) |
        (ReturnRequest.request_number == f"#{clean_id}") |
        (ReturnRequest.id == int(clean_id) if clean_id.isdigit() else False)
    ).first()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Return request '{request_id}' not found."
        )

    req.status = payload.status
    if payload.current_step is not None:
        req.current_step = payload.current_step
    if payload.timeline is not None:
        req.timeline = payload.timeline

    db.commit()
    db.refresh(req)
    return req
