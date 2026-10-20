import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

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
def admin_headers():
    """
    Generates valid admin authorization headers.
    """
    token = create_access_token("admin@lumea.com")
    return {"Authorization": f"Bearer {token}"}
