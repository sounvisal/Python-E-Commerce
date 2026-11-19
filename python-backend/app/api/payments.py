import datetime
import hmac
import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import update
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order
from app.core.config import settings
from app.api.deps import get_optional_user
from app.services.order_lifecycle import check_order_access, expire_pending_orders, cancel_order, settle_payment, utcnow
from app.models.user import User
from app.services.khqr_service import ACTIVE_PAYMENT_PROCS, get_bakong_khqr_data, cancel_payment_session
from app.services import payway_api

router = APIRouter(prefix="/payments", tags=["Payments"])
logger = logging.getLogger(__name__)

class KHQRGenerateRequest(BaseModel):
    order_number: str
    amount: float = Field(gt=0, allow_inf_nan=False)
    try_live: Optional[bool] = True

class KHQRCheckRequest(BaseModel):
    order_number: str
    client_id: Optional[str] = None

class KHQRSimulateRequest(BaseModel):
    order_number: str

class KHQRCancelRequest(BaseModel):
    order_number: str

class PayWayNotification(BaseModel):
    tran_id: str = Field(pattern=r"^LUM[0-9A-F]{12}$")


def payment_options(current_user=None):
    merchant = bool(payway_api.merchant_gateway())
    demo = not settings.PRODUCTION and settings.ENABLE_DEMO_PAYMENTS and getattr(current_user, "role", None) == "admin"
    local = not settings.PRODUCTION and bool(os.getenv("ABA_PAYWAY_URL"))
    return {"khqr": merchant or local or demo, "demo": demo and not merchant and not local}


@router.get("/methods")
def get_payment_methods(current_user=Depends(get_optional_user)):
    return payment_options(current_user)


async def _merchant_qr(db, order, gateway):
    if order.payway_gateway and order.payway_gateway != gateway:
        raise HTTPException(409, "This order belongs to another payment configuration.")
    if not order.payway_qr:
        lifetime = int((order.expires_at - utcnow()).total_seconds() / 60) if order.expires_at else 0
        if lifetime < 3:
            raise HTTPException(409, "There is insufficient time left to generate a QR for this order.")
        claimed = db.execute(update(Order).where(
            Order.id == order.id, Order.status == "Pending", Order.payway_started_at.is_(None)
        ).values(payway_gateway=gateway, payway_started_at=utcnow())).rowcount
        db.commit()
        if not claimed:
            db.refresh(order)
            if not order.payway_qr:
                raise HTTPException(409, "A payment session already started for this order.")
        else:
            try:
                order.payway_qr = await payway_api.create_qr(order.order_number, order.total, lifetime)
            except payway_api.PayWayError as error:
                logger.warning("Could not obtain PayWay QR for order %s.", order.order_number)
                raise HTTPException(503, "PayWay could not create the QR. Check your order before retrying.") from error
            db.commit()
    return {"qr_string": order.payway_qr, "source": "payway_api", "amount": order.total, "currency": "USD"}


async def _reconcile_merchant_payment(db, order):
    if order.payment_status == "Paid" or order.payway_gateway is None:
        return
    if order.payway_gateway != payway_api.merchant_gateway():
        raise HTTPException(503, "The merchant configuration for this payment is unavailable.")
    try:
        reference = await payway_api.verified_payment(order.order_number, order.total)
    except payway_api.PayWayError as error:
        logger.warning("PayWay verification was unavailable for order %s.", order.order_number)
        raise HTTPException(503, "PayWay verification is temporarily unavailable.") from error
    if reference:
        settle_payment(db, order, reference)
        db.commit()
        db.refresh(order)


@router.post("/khqr/generate")
async def generate_khqr(req: KHQRGenerateRequest, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """Issue a QR for an authorized, pending order at its stored total."""
    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    check_order_access(order, current_user, order_token)
    expire_pending_orders(db)
    db.commit()
    if order.payment_method != "khqr" or order.payment_status == "Paid" or order.status != "Pending":
        raise HTTPException(409, "This order is not awaiting payment")
    if abs(req.amount - order.total) > 0.009:
        raise HTTPException(400, "Payment amount must match the order total")
    gateway = payway_api.merchant_gateway()
    if gateway:
        qr_data = await _merchant_qr(db, order, gateway)
    elif payment_options(current_user)["demo"]:
        qr_data = {"qr_string": f"LUMEA-DEMO:{order.order_number}", "source": "demo", "demo": True}
    elif not settings.PRODUCTION:
        qr_data = await get_bakong_khqr_data(amount=order.total, order_number=order.order_number,
                                           try_live=req.try_live is not False)
    else:
        qr_data = {}
    if qr_data.get("source") not in {"live_aba_payway", "payway_api", "demo"}:
        raise HTTPException(503, "Live payment verification is unavailable for this order. Choose cash on delivery.")
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
    if order.payment_method != "khqr":
        raise HTTPException(409, "This order does not use KHQR.")
    await _reconcile_merchant_payment(db, order)

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
def simulate_khqr_approval(req: KHQRSimulateRequest, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """Record a clearly labeled payment on an internal demo order."""
    if settings.PRODUCTION or not settings.ENABLE_DEMO_PAYMENTS:
        raise HTTPException(403, "Demo payments are disabled in this environment")
    if not current_user:
        raise HTTPException(401, "Authentication required to simulate payment.")
    if current_user.role != "admin":
        raise HTTPException(403, "Administrator access required.")
    if not payment_options(current_user)["demo"]:
        raise HTTPException(403, "Demo payments cannot be used with PayWay enabled.")

    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {req.order_number} not found")
    check_order_access(order, current_user, order_token)

    if (
        order.payment_method != "khqr" or order.status != "Pending" or order.payment_status == "Paid"
        or not order.expires_at or order.expires_at <= utcnow()
        or order.payway_gateway or order.order_number in ACTIVE_PAYMENT_PROCS
    ):
        raise HTTPException(409, "Order is not awaiting payment")
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ref = f"DEMO-BAKONG-{now_str}-{order.id}"
    settle_payment(db, order, ref)
    db.commit()
    db.refresh(order)

    return {
        "status": "success",
        "message": "Demo payment recorded.",
        "paid": True,
        "order_number": order.order_number,
        "transaction_ref": order.transaction_ref
    }

@router.post("/khqr/cancel")
def cancel_khqr_payment(req: KHQRCancelRequest, db: Session = Depends(get_db), current_user=Depends(get_optional_user), order_token: Optional[str] = Header(None, alias="X-Order-Token")):
    """Close checkout and release stock, preserving late bank reconciliation."""
    order = db.query(Order).filter(Order.order_number == req.order_number).first()
    check_order_access(order, current_user, order_token)
    if order.payment_method != "khqr":
        raise HTTPException(409, "This order does not use KHQR.")
    cancel_order(db, order)
    db.commit()
    return {
        "status": "success",
        "paid": False,
        "action": order.status.lower()
    }


@router.post("/khqr/callback", include_in_schema=False)
async def payway_callback(payload: PayWayNotification, token: str = Query(max_length=64), db: Session = Depends(get_db)):
    order_number = f"LUM-{payload.tran_id[3:]}"
    if not hmac.compare_digest(token, payway_api.callback_token(order_number)):
        raise HTTPException(403, "Invalid notification.")
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order or order.payment_method != "khqr" or not order.payway_gateway:
        raise HTTPException(404, "Payment order not found.")
    await _reconcile_merchant_payment(db, order)
    return {"status": "ok"}
