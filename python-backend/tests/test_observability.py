import pytest
from fastapi.testclient import TestClient

def test_health_check_endpoint(client: TestClient):
    """Verify production health check returns operational database ping and uptime."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "uptime_seconds" in data
    assert data["uptime_seconds"] >= 0
    assert "version" in data

def test_root_redirect_to_swagger_docs(client: TestClient):
    """Verify root / redirects to OpenAPI Swagger UI documentation."""
    res = client.get("/", follow_redirects=False)
    assert res.status_code in [302, 307]
    assert res.headers["location"] == "/docs"

def test_swagger_docs_accessible(client: TestClient):
    """Verify interactive Swagger UI loads successfully."""
    res = client.get("/docs")
    assert res.status_code == 200
    assert "swagger-ui" in res.text.lower() or "html" in res.text.lower()

def test_newsletter_subscription_valid_email(client: TestClient):
    """Verify newsletter subscription registers email with confirmation."""
    res = client.post("/api/newsletter", json={"email": "Patron.Botanical@Example.COM"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["email"] == "patron.botanical@example.com"
    assert "subscribed_at" in data

def test_newsletter_subscription_invalid_email(client: TestClient):
    """Verify newsletter subscription rejects malformed email strings."""
    res = client.post("/api/newsletter", json={"email": "not-a-valid-email"})
    assert res.status_code == 422
