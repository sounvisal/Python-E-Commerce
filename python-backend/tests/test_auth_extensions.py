import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

def test_phone_login_and_logout_flow():
    db = SessionLocal()
    # Create or update test user with specific phone
    test_email = "phonetest@lumea.com"
    test_phone = "+855 12 345 678"
    existing = db.query(User).filter(User.email == test_email).first()
    if existing:
        db.delete(existing)
        db.commit()

    user = User(
        name="Phone Test User",
        email=test_email,
        phone=test_phone,
        hashed_password=get_password_hash("password123"),
        role="customer",
        tier="Luméa Member",
        reward_points=100,
        token_version=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 1. Login with phone number formatted
    res_phone = client.post("/api/auth/login", json={
        "email": test_phone,
        "password": "password123"
    })
    assert res_phone.status_code == 200, f"Expected 200, got {res_phone.status_code}: {res_phone.text}"
    token = res_phone.json()["data"]["access_token"]
    assert token

    # 2. Login with phone number using stripped digits
    res_digits = client.post("/api/auth/login", json={
        "identifier": "85512345678",
        "password": "password123"
    })
    assert res_digits.status_code == 200

    # 3. Phone login with wrong password returns 401, not 422
    res_wrong = client.post("/api/auth/login", json={
        "email": test_phone,
        "password": "wrongpassword"
    })
    assert res_wrong.status_code == 401

    # 4. Authenticated request using the token works
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200

    # 5. Logout endpoint invalidates the session
    res_logout = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert res_logout.status_code == 200
    assert res_logout.json()["status"] == "success"

    # 6. Verify previous token is now rejected
    res_me_revoked = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me_revoked.status_code == 401

    # 7. Unauthenticated logout also succeeds cleanly
    res_guest_logout = client.post("/api/auth/logout")
    assert res_guest_logout.status_code == 200

    db.delete(user)
    db.commit()
    db.close()
