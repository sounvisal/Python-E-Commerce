import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.core.security import create_access_token
from app.models.user import User

@pytest.fixture(scope="session")
def client():
    """
    Shared TestClient fixture configured for API integration tests.
    """
    with TestClient(app, headers={"X-Test-Client": "true"}) as c:
        yield c

@pytest.fixture
def auth_headers():
    """
    Generates valid authorization headers for authenticated testing.
    """
    token = create_access_token("sreynich.chan@example.com")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(client):
    with SessionLocal.begin() as db:
        admin = db.query(User).filter(User.email == "test-admin@example.com").first()
        if not admin:
            admin = User(email="test-admin@example.com", name="Test Admin", role="admin", hashed_password="unused")
            db.add(admin)
            db.flush()
        token = create_access_token(admin.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def place_guest_order(client):
    def place(payment_method="cod"):
        payload = {
            "customer_name": "Test Buyer",
            "customer_email": "buyer@example.com",
            "shipping_address": "123 Norodom Blvd",
            "shipping_city": "Phnom Penh",
            "payment_method": payment_method,
            "items": [{"product_id": 201, "quantity": 1}],
        }
        quote = client.post("/api/orders/quote", json=payload)
        assert quote.status_code == 200, quote.text
        payload["expected_total"] = quote.json()["data"]["total"]
        order = client.post("/api/orders", json=payload)
        assert order.status_code == 201, order.text
        return order.json()["data"]

    return place
