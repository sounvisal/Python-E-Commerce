from app.core.config import settings
from fastapi.testclient import TestClient
from app.services.khqr_service import crc16_emvco, build_instant_bakong_khqr

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
    order = place_guest_order("khqr")
    payload = {"order_number": order["order_number"]}

    # Avoid contacting a bank or leaving a live polling session during the test.
    monkeypatch.setattr("app.api.payments.cancel_payment_session", lambda order_number: None)
    monkeypatch.setattr(settings, "ENABLE_DEMO_PAYMENTS", False)
    assert client.post("/api/payments/khqr/simulate-approve", json=payload, headers=admin_headers).status_code == 403

    monkeypatch.setattr(settings, "ENABLE_DEMO_PAYMENTS", True)
    assert client.post("/api/payments/khqr/simulate-approve", json=payload).status_code == 401
    res = client.post("/api/payments/khqr/simulate-approve", json=payload, headers=admin_headers)
    assert res.status_code == 200, res.text
    assert res.json()["paid"] is True
    assert res.json()["transaction_ref"].startswith("DEMO-")
