"""Signed ABA PayWay QR generation and transaction verification."""

import base64
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import os
from urllib.parse import urlsplit

import httpx

from app.core.config import settings
from app.services.khqr_service import matches_order_qr

GATEWAY_HOSTS = {
    "sandbox": "checkout-sandbox.payway.com.kh",
    "live": "checkout.payway.com.kh",
}


class PayWayError(Exception):
    """PayWay did not provide a usable response."""


def public_url():
    candidate = (settings.PAYWAY_PUBLIC_URL or os.getenv("RENDER_EXTERNAL_URL", "")).rstrip("/")
    try:
        url = urlsplit(candidate)
    except ValueError:
        return ""
    return candidate if url.scheme == "https" and url.netloc and not any(
        (url.username, url.password, url.path, url.query, url.fragment)
    ) else ""


def merchant_gateway():
    if settings.PRODUCTION and settings.PAYWAY_ENVIRONMENT != "live":
        return None
    if not (settings.PAYWAY_MERCHANT_ID and settings.PAYWAY_API_KEY and public_url()):
        return None
    return f"{settings.PAYWAY_ENVIRONMENT}:{settings.PAYWAY_MERCHANT_ID}"


def transaction_id(order_number):
    return order_number.replace("-", "")


def callback_token(order_number):
    return hmac.new(settings.SECRET_KEY.encode(), f"payway-callback:{order_number}".encode(), hashlib.sha256).hexdigest()


def _signed_request(order_number):
    return {
        "req_time": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "merchant_id": settings.PAYWAY_MERCHANT_ID,
        "tran_id": transaction_id(order_number),
    }


def _signature(*values):
    content = "".join(map(str, values)).encode()
    return base64.b64encode(hmac.new(settings.PAYWAY_API_KEY.encode(), content, hashlib.sha512).digest()).decode()


async def _post(endpoint, payload):
    url = f"https://{GATEWAY_HOSTS[settings.PAYWAY_ENVIRONMENT]}/api/payment-gateway/v1/payments/{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise PayWayError("PayWay request failed.") from error
    if not isinstance(data, dict) or not isinstance(data.get("status"), dict):
        raise PayWayError("Invalid PayWay response.")
    return data


def _same_amount(actual, expected):
    try:
        return Decimal(str(actual)) == Decimal(str(expected))
    except InvalidOperation:
        return False


async def create_qr(order_number, amount, lifetime):
    payload = _signed_request(order_number)
    callback = f"{public_url()}{settings.API_V1_STR}/payments/khqr/callback?token={callback_token(order_number)}"
    value = Decimal(str(amount)).quantize(Decimal("0.01"))
    payload.update(
        amount=int(value) if value == value.to_integral_value() else float(value),
        purchase_type="purchase",
        payment_option="abapay_khqr",
        callback_url=base64.b64encode(callback.encode()).decode(),
        currency="USD",
        lifetime=lifetime,
        qr_image_template="template3_color",
    )
    # Omitted optional fields contribute empty strings to PayWay's ordered signature.
    payload["hash"] = _signature(*payload.values())
    response = await _post("generate-qr", payload)
    qr = response.get("qrString")
    if (
        str(response["status"].get("code")) not in {"0", "00"}
        or not matches_order_qr(qr, value)
        or response.get("currency") != "USD" or not _same_amount(response.get("amount"), value)
    ):
        raise PayWayError("PayWay did not return a matching QR.")
    return qr


async def verified_payment(order_number, amount):
    payload = _signed_request(order_number)
    payload["hash"] = _signature(*payload.values())
    response = await _post("check-transaction-2", payload)
    status = response["status"]
    data = response.get("data")
    if str(status.get("code")) not in {"0", "00"} or not isinstance(data, dict):
        raise PayWayError("PayWay could not verify the transaction.")
    if str(data.get("payment_status_code")) != "0" or data.get("payment_status") not in {"APPROVED", "PAID"}:
        return None
    if (
        status.get("tran_id") != payload["tran_id"]
        or data.get("payment_currency") != "USD"
        or not _same_amount(data.get("payment_amount"), amount)
        or not _same_amount(data.get("total_amount"), amount)
    ):
        raise PayWayError("PayWay payment does not match the order.")
    return f"PAYWAY-{payload['tran_id']}"
