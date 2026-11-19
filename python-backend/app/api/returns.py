import random
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, update

from app.core.database import get_db
from app.models.return_request import ReturnRequest
from app.models.order import Order, OrderItem
from app.models.user import User
from app.api.deps import get_current_user, require_admin
from app.services.order_lifecycle import check_order_access
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all return requests, optionally filtered by order_number or customer_email.
    """
    query = db.query(ReturnRequest)
    if current_user.role != "admin":
        query = query.filter(ReturnRequest.customer_email == current_user.email)
    if order_number:
        query = query.filter(ReturnRequest.order_number == order_number)
    if customer_email:
        query = query.filter(ReturnRequest.customer_email == customer_email)
    
    requests = query.order_by(desc(ReturnRequest.id)).all()
    return ReturnRequestListResponse(success=True, total=len(requests), data=requests)

@router.get("/{request_id}", response_model=ReturnRequestResponse)
def get_return_request(request_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
    if current_user.role != "admin" and req.customer_email.lower() != current_user.email.lower():
        raise HTTPException(404, "Return not found")
    return req

@router.post("", response_model=ReturnRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_return_request(payload: ReturnRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Submit an interactive return request from the 5-step wizard.
    Generates a unique #RR reference number and initializes tracking timeline.
    """
    order = db.query(Order).filter(Order.order_number == payload.order_number).first()
    check_order_access(order, current_user)
    if order.status != "Delivered" or order.payment_status != "Paid":
        raise HTTPException(400, "Only delivered, paid orders can be returned")
    # Until delivery timestamps are recorded, the return window uses the order date.
    created = (order.delivered_at or order.created_at).replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) - created > timedelta(days=30):
        raise HTTPException(400, "This order is outside the 30-day return window")
    item = db.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.id == payload.order_item_id).with_for_update().first()
    if not item:
        raise HTTPException(400, "Select a purchased item from this order")

    # Transactional check of cumulative returns to prevent double-return race conditions
    prior_returned = db.query(func.coalesce(func.sum(ReturnRequest.quantity), 0)).filter(
        ReturnRequest.order_number == order.order_number,
        (
            (ReturnRequest.order_item_id == item.id) |
            ((ReturnRequest.order_item_id.is_(None)) & (ReturnRequest.product_name == item.product_name))
        ),
        ReturnRequest.status.notin_(["Rejected", "rejected"])
    ).scalar() or 0

    requested_qty = payload.quantity or 1
    if requested_qty <= 0:
        raise HTTPException(400, "Return quantity must be greater than zero")
    if requested_qty + prior_returned > item.quantity:
        raise HTTPException(400, f"The requested quantity ({requested_qty}) exceeds the available returnable amount ({item.quantity - prior_returned} of {item.quantity} remaining).")
    
    # Atomic reservation of return quantity on OrderItem to prevent concurrent over-return race conditions
    result = db.execute(
        update(OrderItem)
        .where(
            OrderItem.id == item.id,
            OrderItem.quantity >= OrderItem.returned_quantity + requested_qty
        )
        .values(returned_quantity=OrderItem.returned_quantity + requested_qty)
    )
    if result.rowcount == 0:
        raise HTTPException(400, f"The requested quantity ({requested_qty}) exceeds the available returnable amount ({item.quantity - prior_returned} of {item.quantity} remaining).")
    if payload.resolution != "Refund to original payment method":
        raise HTTPException(400, "Only refunds are currently supported")
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
        order_item_id=item.id,
        customer_name=order.customer_name,
        customer_email=current_user.email,
        product_name=item.product_name,
        product_image=item.image_url,
        product_variant="Standard (Full Size)",
        price=round(item.price * (order.subtotal - order.discount) / order.subtotal, 2),
        quantity=payload.quantity or 1,
        reason=payload.reason,
        resolution=payload.resolution,
        description=payload.description or "",
        photos=payload.photos or [],
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

@router.patch("/{request_id}/status", response_model=ReturnRequestResponse, dependencies=[Depends(require_admin)])
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

    stages = ['Submitted', 'Under Review', 'Approved', 'Return in Transit', 'Item Received', 'Refund Processing', 'Refund Completed']
    aliases = {'pending': 'Under Review', 'refunded': 'Refund Completed'}
    target = aliases.get(payload.status.lower(), next((s for s in stages if s.lower() == payload.status.lower()), payload.status.title()))
    previous = aliases.get(req.status.lower(), next((s for s in stages if s.lower() == req.status.lower()), req.status.title()))
    if target == 'Refund Completed' and not payload.refund_reference:
        raise HTTPException(400, 'Record the completed manual refund reference before marking refunded')
    if target != previous:
        valid = (target == 'Rejected' and previous == 'Under Review') or (previous in stages and stages.index(previous) < 6 and target == stages[stages.index(previous) + 1])
        if not valid:
            raise HTTPException(409, 'Invalid return transition')
    req.status = target
    req.refund_reference = payload.refund_reference or req.refund_reference
    req.current_step = stages.index(target) + 1 if target in stages else 2
    old_dates = {stage['title']: stage['date'] for stage in (req.timeline or [])}
    req.timeline = [{'id': i + 1, 'title': title,
        'date': old_dates.get(title, 'Pending') if i + 1 < req.current_step else (datetime.now().strftime('%b %d, %Y') if i + 1 == req.current_step else 'Pending'),
        'status': 'completed' if i + 1 < req.current_step else ('current' if i + 1 == req.current_step else 'upcoming')}
        for i, title in enumerate(stages)]
    if target == 'Rejected':
        if previous != 'Rejected' and req.order_item_id:
            db.execute(
                update(OrderItem)
                .where(OrderItem.id == req.order_item_id)
                .values(returned_quantity=func.max(0, OrderItem.returned_quantity - req.quantity))
            )
        req.timeline = [{'id': 1, 'title': 'Submitted', 'date': req.submitted_date, 'status': 'completed'},
                        {'id': 2, 'title': 'Rejected', 'date': datetime.now().strftime('%b %d, %Y'), 'status': 'current'}]
    db.commit()
    db.refresh(req)
    return req
