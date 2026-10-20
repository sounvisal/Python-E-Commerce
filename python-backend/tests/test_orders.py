import pytest
from fastapi.testclient import TestClient

def test_order_creation_and_calculation(client: TestClient):
    """Verify order checkout with itemized line items and tax calculation."""
    payload = {
        "customer_name": "Sreynich Chan",
        "customer_email": "sreynich.chan@example.com",
        "shipping_address": "123 Norodom Blvd",
        "shipping_city": "Phnom Penh",
        "shipping_postal_code": "12000",
        "items": [
            {
                "product_id": 201,
                "product_name": "Facial Treatment Essence",
                "price": 99.00,
                "quantity": 1
            }
        ],
        "discount_code": ""
    }
    res = client.post("/api/orders", json=payload)
    assert res.status_code == 201
    data = res.json()["data"]
    assert "order_number" in data
    assert data["order_number"].startswith("LUM-")
    assert data["subtotal"] == 99.00
    assert data["total"] >= 99.00
    assert data["status"] == "Confirmed"

def test_order_status_lookup(client: TestClient):
    """Verify retrieving an order by its unique order number."""
    payload = {
        "customer_name": "Test Lookup",
        "customer_email": "lookup@example.com",
        "shipping_address": "Test Street",
        "shipping_city": "Phnom Penh",
        "items": [
            {
                "product_id": 201,
                "product_name": "Facial Treatment Essence",
                "price": 99.00,
                "quantity": 1
            }
        ]
    }
    create_res = client.post("/api/orders", json=payload)
    order_num = create_res.json()["data"]["order_number"]

    # Fetch it
    res = client.get(f"/api/orders/{order_num}")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["order_number"] == order_num
    assert len(data["items"]) == 1

def test_invalid_order_missing_items(client: TestClient):
    """Verify 400 Bad Request when placing empty order."""
    payload = {
        "customer_name": "Invalid Order",
        "customer_email": "invalid@example.com",
        "shipping_address": "123 Street",
        "shipping_city": "Phnom Penh",
        "items": []
    }
    res = client.post("/api/orders", json=payload)
    assert res.status_code == 400
