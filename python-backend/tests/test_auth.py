import pytest
import time
from fastapi.testclient import TestClient

def test_login_successful(client: TestClient):
    """Verify demo customer authentication and JWT issuance."""
    res = client.post("/api/auth/login", json={
        "email": "sreynich.chan@example.com",
        "password": "password123"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == "sreynich.chan@example.com"

def test_login_invalid_password(client: TestClient):
    """Verify 401 Unauthorized returned on wrong credentials."""
    res = client.post("/api/auth/login", json={
        "email": "sreynich.chan@example.com",
        "password": "WrongPassword999"
    })
    assert res.status_code == 401

def test_auth_me_protected(client: TestClient, auth_headers: dict):
    """Verify /api/auth/me returns user profile with valid Bearer token."""
    res = client.get("/api/auth/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "sreynich.chan@example.com"
    assert "tier" in data

def test_auth_me_unauthorized_without_token(client: TestClient):
    """Verify /api/auth/me rejects unauthenticated requests."""
    res = client.get("/api/auth/me")
    assert res.status_code == 401

def test_user_registration(client: TestClient):
    """Verify new user registration with strong password."""
    unique_email = f"test_{int(time.time())}@example.com"
    res = client.post("/api/auth/register", json={
        "name": "Botanical Tester",
        "email": unique_email,
        "password": "ValidStrongPass2026!"
    })
    assert res.status_code in [200, 201]
    data = res.json()
    assert "access_token" in data["data"]
    assert data["data"]["user"]["email"] == unique_email
