from app.core.config import settings
from fastapi.testclient import TestClient
from app.services.khqr_service import crc16_emvco, build_instant_bakong_khqr
from app.services import payway_api

def test_crc16_emvco_calculation():
    """Verify CCITT CRC16 polynomial 0x1021 with init 0xFFFF per EMVCo standard."""
    # Test known string
    test_str = "000201010212"
    crc = crc16_emvco(test_str)
    assert len(crc) == 4
    assert all(c in "0123456789ABCDEF" for c in crc)

def test_bakong_khqr_payload_generation():
    """Verify generated dynamic Bakong KHQR contains required EMVCo TLV tags."""
    qr = build_instant_bakong_khqr(amount=55.00, order_number="LUM-123456", merchant_name="LUMEA ATELIER")
    # Tag 00: Payload Format Indicator (01)
    assert qr.startswith("000201")
    # Tag 53: Currency (840 = USD)
    assert "5303840" in qr
    # Tag 58: Country Code (KH)
    assert "5802KH" in qr
    # Tag 59: Merchant Name
    assert "5913LUMEA ATELIER" in qr
    # Tag 62: Order Reference
    assert "LUM-123456" in qr
    # 4-character CRC at the end
    assert len(qr) > 60

def test_khqr_generate_endpoint(client: TestClient, monkeypatch, place_guest_order):
    order = place_guest_order("khqr")

    async def verified_gateway(amount, order_number, try_live):
        assert order_number == order["order_number"]
        return {"source": "live_aba_payway", "qr_string": "test-qr", "amount": amount, "currency": "USD"}

    monkeypatch.setattr("app.api.payments.get_bakong_khqr_data", verified_gateway)
    payload = {"order_number": order["order_number"], "amount": order["total"]}
    assert client.post("/api/payments/khqr/generate", json=payload).status_code == 404

    res = client.post("/api/payments/khqr/generate", json=payload, headers={"X-Order-Token": order["access_token"]})
    assert res.status_code == 200, res.text
    assert res.json()["data"]["qr_string"] == "test-qr"


def test_khqr_simulate_approval_endpoint(client: TestClient, monkeypatch, admin_headers, place_guest_order):
    monkeypatch.setenv("ABA_PAYWAY_URL", "")
    monkeypatch.setattr(settings, "PAYWAY_MERCHANT_ID", "")
    order = place_guest_order("khqr")
    payload = {"order_number": order["order_number"]}

    # Avoid contacting a bank or leaving a live polling session during the test.
    monkeypatch.setattr("app.api.payments.cancel_payment_session", lambda order_number: None)
    monkeypatch.delenv("ABA_PAYWAY_URL", raising=False)
    monkeypatch.setattr(settings, "ENABLE_DEMO_PAYMENTS", False)
    assert client.post("/api/payments/khqr/simulate-approve", json=payload, headers=admin_headers).status_code == 403

    monkeypatch.setattr(settings, "ENABLE_DEMO_PAYMENTS", True)
    assert client.post("/api/payments/khqr/simulate-approve", json=payload).status_code == 401
    res = client.post("/api/payments/khqr/simulate-approve", json=payload, headers=admin_headers)
    assert res.status_code == 200, res.text
    assert res.json()["paid"] is True
    assert res.json()["transaction_ref"].startswith("DEMO-")


def test_merchant_checkout_verifies_callback_and_reuses_qr(client, monkeypatch, place_guest_order):
    monkeypatch.setattr(settings, "PAYWAY_MERCHANT_ID", "test-merchant")
    monkeypatch.setattr(settings, "PAYWAY_API_KEY", "test-key")
    monkeypatch.setattr(settings, "PAYWAY_PUBLIC_URL", "https://store.example")
    order = place_guest_order("khqr")
    number, total = order["order_number"], order["total"]
    transaction_id = payway_api.transaction_id(number)
    headers = {"X-Order-Token": order["access_token"]}
    qr = build_instant_bakong_khqr(total, number)
    charges = []
    payment_amount = total + 1

    async def bank(endpoint, payload):
        assert payload["tran_id"] == transaction_id
        assert payload["merchant_id"] == "test-merchant"
        assert payload["hash"]
        if endpoint == "generate-qr":
            charges.append(payload)
            return {"status": {"code": "0"}, "qrString": qr, "amount": total, "currency": "USD"}
        return {
            "status": {"code": "00", "tran_id": transaction_id},
            "data": {"payment_status_code": 0, "payment_status": "APPROVED", "payment_currency": "USD",
                     "payment_amount": payment_amount, "total_amount": total},
        }

    monkeypatch.setattr(payway_api, "_post", bank)
    path = "/api/payments/khqr/generate"
    body = {"order_number": number, "amount": total}
    assert client.post(path, json=body).status_code == 404
    assert client.post(path, json={**body, "amount": total + 1}, headers=headers).status_code == 400
    for _ in range(2):
        response = client.post(path, json=body, headers=headers)
        assert response.status_code == 200, response.text
        assert response.json()["data"]["qr_string"] == qr
    assert len(charges) == 1
    callback = "/api/payments/khqr/callback"
    notification = {"tran_id": transaction_id}
    assert client.post(callback, params={"token": "invalid"}, json=notification).status_code == 403
    params = {"token": payway_api.callback_token(number)}
    assert client.post(callback, params=params, json=notification).status_code == 503
    payment_amount = total
    for _ in range(2):
        assert client.post(callback, params=params, json=notification).status_code == 200
    state = client.post("/api/payments/khqr/check", json={"order_number": number}, headers=headers)
    assert state.json()["action"] == "approved"


def test_production_without_merchant_only_exposes_cod(client, monkeypatch, admin_headers):
    monkeypatch.setattr(settings, "PRODUCTION", True)
    monkeypatch.setattr(settings, "ENABLE_DEMO_PAYMENTS", True)
    monkeypatch.setattr(settings, "PAYWAY_MERCHANT_ID", "")
    monkeypatch.setenv("ABA_PAYWAY_URL", "https://link.payway.com.kh")
    assert client.get("/api/payments/methods", headers=admin_headers).json() == {"khqr": False, "demo": False}
    assert client.post("/api/payments/khqr/simulate-approve", json={"order_number": "example"},
                       headers=admin_headers).status_code == 403
