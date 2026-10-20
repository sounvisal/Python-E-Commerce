import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserCreate
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token

def test_password_hashing():
    """Verify bcrypt salt & cryptographic hash validation."""
    pwd = "SecurePassword123!"
    hashed = get_password_hash(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False

def test_password_policy_rejection():
    """Verify weak passwords under 8 characters or lacking complexity are rejected."""
    # Under 8 chars
    with pytest.raises(ValidationError):
        UserCreate(name="Test User", email="test@example.com", password="abc")

    # Common weak password
    with pytest.raises(ValidationError):
        UserCreate(name="Test User", email="test@example.com", password="password")

    # Letters only without digits
    with pytest.raises(ValidationError):
        UserCreate(name="Test User", email="test@example.com", password="OnlyLettersHere")

    # Numbers only without letters
    with pytest.raises(ValidationError):
        UserCreate(name="Test User", email="test@example.com", password="123456789012")

def test_password_policy_acceptance():
    """Verify compliant passwords pass validation."""
    user = UserCreate(name="Jane Doe", email="jane@example.com", password="StrongPass2026!")
    assert user.password == "StrongPass2026!"

def test_xss_name_sanitization():
    """Verify HTML script tags are escaped in user input."""
    user = UserCreate(name="<script>alert('xss')</script>Alice", email="alice@example.com", password="ValidPass123")
    assert "<script>" not in user.name
    assert "&lt;script&gt;" in user.name

def test_jwt_tamper_rejection():
    """Verify modified or invalid JWT tokens fail decode."""
    token = create_access_token("user@example.com")
    # Tamper with the signature
    tampered_token = token[:-4] + "xxxx"
    decoded = decode_access_token(tampered_token)
    assert decoded is None

def test_security_headers(client: TestClient):
    """Verify OWASP-recommended security headers are attached to responses."""
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert res.headers.get("X-XSS-Protection") == "1; mode=block"
    assert res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "X-Process-Time" in res.headers

def test_rate_limiting_triggers():
    """Verify rate limiter blocks brute force attacks (HTTP 429)."""
    # Create client without test bypass header
    with TestClient(app) as test_c:
        # Rapidly attempt 15 logins
        responses = []
        for i in range(16):
            r = test_c.post("/api/auth/login", json={
                "email": f"bruteforce_{i}@example.com",
                "password": "wrongpassword123"
            })
            responses.append(r.status_code)
        
        # At least one should be rate limited with HTTP 429
        assert 429 in responses, f"Expected HTTP 429 in responses, got: {responses}"
