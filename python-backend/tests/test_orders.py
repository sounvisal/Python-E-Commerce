from fastapi.testclient import TestClient


def test_order_creation_and_calculation(place_guest_order):
    order = place_guest_order()
    assert order["order_number"].startswith("LUM-")
    assert order["subtotal"] == 99.00
    assert order["total"] == 99.00
    assert order["status"] == "Confirmed"
    assert order["payment_status"] == "Unpaid"


def test_order_status_lookup(client: TestClient, place_guest_order):
    order = place_guest_order()
    path = f"/api/orders/{order['order_number']}"
    assert client.get(path).status_code == 404

    res = client.get(path, headers={"X-Order-Token": order["access_token"]})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["order_number"] == order["order_number"]
    assert len(data["items"]) == 1


def test_invalid_order_missing_items(client: TestClient, auth_headers):
    """Verify 400 Bad Request when placing empty order by authenticated user."""
    payload = {
        "customer_name": "Sreynich Chan",
        "customer_email": "sreynich.chan@example.com",
        "shipping_address": "123 Street",
        "shipping_city": "Kampot",
        "items": []
    }
    res = client.post("/api/orders", json=payload, headers=auth_headers)
    assert res.status_code == 400


def test_order_without_login_rejected(client: TestClient):
    """Verify 401 Unauthorized when placing order without login (anti-spam / anti-bot)."""
    payload = {
        "customer_name": "Anonymous Spammer",
        "customer_email": "spam@example.com",
        "shipping_address": "Nowhere",
        "shipping_city": "Kampot",
        "items": [{"product_id": 201, "quantity": 1}]
    }
    res = client.post("/api/orders", json=payload)
    assert res.status_code == 401
