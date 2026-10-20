import pytest
from fastapi.testclient import TestClient

def test_get_categories(client: TestClient):
    """Verify category list retrieval with product counts."""
    res = client.get("/api/categories")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) >= 8
    assert all("name" in c and "slug" in c for c in data)

def test_get_products_catalog(client: TestClient):
    """Verify product catalog retrieval with pagination."""
    res = client.get("/api/products")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0
    assert "price" in data[0]
    assert "brand" in data[0]

def test_product_search(client: TestClient):
    """Verify search filter functionality."""
    res = client.get("/api/products?search=Ordinary")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0
    assert any("Ordinary" in p["brand"] or "Ordinary" in p["name"] for p in data)

def test_featured_products(client: TestClient):
    """Verify featured showcase products endpoint."""
    res = client.get("/api/products/featured")
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0

def test_product_detail_lookup(client: TestClient):
    """Verify single product lookup by slug."""
    res = client.get("/api/products/sk-ii-facial-treatment-essence")
    assert res.status_code == 200
    body = res.json()
    assert body["data"]["slug"] == "sk-ii-facial-treatment-essence"
    assert "related" in body

def test_nonexistent_product_returns_404(client: TestClient):
    """Verify 404 response for non-existent product slug."""
    res = client.get("/api/products/non-existent-product-slug-xyz")
    assert res.status_code == 404
