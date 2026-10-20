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
