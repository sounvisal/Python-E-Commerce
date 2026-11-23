from fastapi.testclient import TestClient


def test_order_creation_and_calculation(place_guest_order):
    order = place_guest_order()
    assert order["order_number"].startswith("LUM-")
    assert order["subtotal"] == 99.00
    assert order["total"] == 99.00
    assert order["status"] == "Awaiting Confirmation"
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


def test_real_notifications_endpoint(client: TestClient, place_guest_order):
    """Verify GET /api/notifications returns real events and customer purchase feeds."""
    place_guest_order()
    res = client.get("/api/notifications")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    purchases = [n for n in data["data"] if n["type"] == "purchase"]
    assert len(purchases) > 0
    assert "Recent Purchase" in purchases[0]["title"]
    events = [n for n in data["data"] if n["type"] == "event"]
    assert len(events) > 0
