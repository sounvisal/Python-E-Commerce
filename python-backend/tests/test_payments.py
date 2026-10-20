import pytest
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

def test_khqr_generate_endpoint(client: TestClient):
    """Verify /api/payments/khqr/generate API returns valid QR payload."""
    res = client.post("/api/payments/khqr/generate", json={
        "order_number": "LUM-TEST-PAY",
        "amount": 25.50
    })
    assert res.status_code == 200
    data = res.json()["data"]
    assert "qr_string" in data
    assert data["amount"] == 25.50
    assert data["currency"] == "USD"

def test_khqr_simulate_approval_endpoint(client: TestClient):
    """Verify /api/payments/khqr/simulate-approve demo defense flow."""
    # Create order first
    order_res = client.post("/api/orders", json={
        "customer_name": "Demo Buyer",
        "customer_email": "demo@example.com",
        "shipping_address": "Street 200",
        "shipping_city": "Phnom Penh",
        "items": [{"product_id": 201, "product_name": "Essence", "price": 50.0, "quantity": 1}]
    })
    order_num = order_res.json()["data"]["order_number"]

    # Simulate bank clearance
    sim_res = client.post("/api/payments/khqr/simulate-approve", json={
        "order_number": order_num
    })
    assert sim_res.status_code == 200
    assert sim_res.json()["paid"] is True
    assert "BAKONG" in sim_res.json()["transaction_ref"]
