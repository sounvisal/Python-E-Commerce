import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order
from app.core.config import settings
from app.api.deps import get_current_user, get_optional_user
from app.services.order_lifecycle import check_order_access, expire_pending_orders, cancel_order, settle_payment
from app.models.user import User
from app.services.khqr_service import get_bakong_khqr_data, cancel_payment_session

router = APIRouter(prefix="/payments", tags=["Payments"])

class KHQRGenerateRequest(BaseModel):
    order_number: str
    amount: float
    try_live: Optional[bool] = True

class KHQRCheckRequest(BaseModel):
    order_number: str
    client_id: Optional[str] = None

class KHQRSimulateRequest(BaseModel):
    order_number: str

class KHQRCancelRequest(BaseModel):
    order_number: str

@router.post("/khqr/generate")
async def generate_khqr(req: KHQRGenerateRequest, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """
    Generates an authentic dynamic Bakong KHQR for an order.
    Extracts real live ABA PayWay link session via Playwright bridge, with instant EMVCo fallback.
    """
    if settings.PRODUCTION:
        raise HTTPException(503, "KHQR is unavailable. Choose cash on delivery.")
    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    check_order_access(order, current_user, order_token)
    expire_pending_orders(db)
    db.commit()
    if order.payment_status == "Paid" or order.status != "Pending":
        raise HTTPException(409, "This order is not awaiting payment")
    if abs(req.amount - order.total) > 0.009:
        raise HTTPException(400, "Payment amount must match the order total")
    qr_data = await get_bakong_khqr_data(amount=order.total, order_number=order.order_number,
                                       try_live=req.try_live if req.try_live is not None else True)
    if qr_data.get('source') != 'live_aba_payway':
        raise HTTPException(503, 'Automatic KHQR verification is unavailable. Close this attempt and choose cash on delivery.')
    # The bank monitor may settle while QR extraction is in progress. Never
    # overwrite that settlement with the earlier Pending snapshot.
    db.refresh(order)
    expire_pending_orders(db)
    db.commit()
    if order.status != 'Pending':
        raise HTTPException(409, 'Checkout is no longer awaiting payment. Check its order status.')

    return {
        "status": "success",
        "data": qr_data
    }

@router.post("/khqr/check")
async def check_khqr_payment(req: KHQRCheckRequest, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """
    Polls payment status. Checks database state and ABA PayWay confirmation.
    """
    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    check_order_access(order, current_user, order_token)
    expire_pending_orders(db)
    db.commit()

    if order.payment_status == "Paid" and order.status == 'Payment Review':
        return {'status': 'success', 'paid': False, 'action': 'review',
                'message': 'Payment was received after checkout closed. Do not pay again. Contact support with your order reference.'}
    if order.payment_status == "Paid":
        # Payment was approved either via live ABA scan or simulation
        cancel_payment_session(req.order_number)
        return {
            "status": "success",
            "paid": True,
            "action": "approved",
            "transaction_ref": order.transaction_ref or f"BAKONG-{order.id}"
        }

    return {
        "status": "success",
        "paid": False,
        "action": "pending" if order.status == "Pending" else order.status.lower()
    }

@router.post("/khqr/simulate-approve")
def simulate_khqr_approval(req: KHQRSimulateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Simulates instantaneous bank approval for academic defense demonstrations.
    Marks order as Paid with authentic Bakong transaction reference.
    """
    if not settings.ENABLE_DEMO_PAYMENTS or current_user.role != "admin":
        raise HTTPException(403, "Demo payments are disabled or require an administrator")
    cancel_payment_session(req.order_number)

    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {req.order_number} not found")

    if order.status != "Pending" or order.payment_status == "Paid":
        raise HTTPException(409, "Order is not awaiting payment")
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    settle_payment(db, order, f"DEMO-{now_str}-{order.id}")
    db.commit()
    db.refresh(order)

    return {
        "status": "success",
        "message": "Payment verified via Bakong KHQR instant clearance",
        "paid": True,
        "order_number": order.order_number,
        "transaction_ref": order.transaction_ref
    }

@router.post("/khqr/cancel")
def cancel_khqr_payment(req: KHQRCancelRequest, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """Cancels active live PayWay polling session for the given order."""
    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    check_order_access(order, current_user, order_token)
    cancel_order(db, order)
    db.commit()
    cancel_payment_session(req.order_number)
    return {
        "status": "success",
        "message": f"Payment session for order {req.order_number} cancelled"
    }
