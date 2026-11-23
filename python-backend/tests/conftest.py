import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import engine, Base, SessionLocal
from app.core.migrations import migrate_schema
from app.seed.seed_data import seed_database
from app.core.security import create_access_token
from app.models.user import User
from app.models.product import Product

@pytest.fixture(scope="session", autouse=True)
def initialize_test_database():
    """Ensure test database tables and fixtures exist on clean databases."""
    Base.metadata.create_all(bind=engine)
    migrate_schema(engine, seed_demo_promotions=True)
    with SessionLocal() as db:
        seed_database(db)

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
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == "sreynich.chan@example.com").first()
        version = getattr(user, "token_version", 1) if user else 1
    token = create_access_token("sreynich.chan@example.com", token_version=version)
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
    with SessionLocal.begin() as db:
        prod = db.query(Product).filter(Product.id == 201).first()
        if prod and prod.stock < 10:
            prod.stock = 50
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
