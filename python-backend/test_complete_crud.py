"""
Complete CRUD & Auth Lifecycle Verification Suite for Luméa E-Commerce Atelier
Tests:
1. Customer Auth Register (POST /api/auth/register)
2. Customer Auth Login (POST /api/auth/login)
3. Admin Auth Login (POST /api/auth/login)
4. Authenticated Profile Fetch (GET /api/auth/me)
5. Binary Image Upload (POST /api/upload)
6. Category CRUD (POST, GET, PUT, DELETE /api/admin/categories or /api/categories)
7. Brand CRUD (POST, GET, PUT, DELETE /api/admin/brands)
8. Product CRUD (POST, GET, PUT, DELETE /api/admin/products)
9. Article CRUD (POST, GET, PUT, DELETE /api/articles)
"""
import io
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("Starting Luméa Complete CRUD & Auth Verification Suite")
    print("=" * 60)
    
    timestamp = int(time.time())
    
    # 1. Customer Register
    reg_email = f"testuser_{timestamp}@lumea.com"
    r = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": reg_email,
        "password": "Password123!",
        "skin_type": "Combination"
    })
    assert r.status_code == 201, f"Register failed: {r.text}"
    print("[PASS] 1. Auth Register: Created customer account", reg_email)
    
    # 2. Customer Login
    r = client.post("/api/auth/login", json={
        "email": reg_email,
        "password": "Password123!"
    })
    assert r.status_code == 200, f"Customer login failed: {r.text}"
    cust_token = r.json()["data"]["access_token"]
    assert cust_token, "No token returned"
    print("[PASS] 2. Customer Login: Successfully authenticated with JWT")
    
    # 3. Admin Login
    r = client.post("/api/auth/login", json={
        "email": "admin@lumea.com",
        "password": "password123"
    })
    assert r.status_code == 200, f"Admin login failed: {r.text}"
    admin_token = r.json()["data"]["access_token"]
    assert admin_token, "No admin token returned"
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    cust_headers = {"Authorization": f"Bearer {cust_token}"}
    print("[PASS] 3. Admin Login: Successfully authenticated as atelier administrator")
    
    # 4. Auth Me
    r = client.get("/api/auth/me", headers=cust_headers)
    assert r.status_code == 200, f"Auth me failed: {r.text}"
    assert r.json()["email"] == reg_email
    print("[PASS] 4. Auth Profile: Verified /auth/me for current user")
    
    # 5. Image File Upload
    fake_img = io.BytesIO(b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xFF\xDB\x00C\x00")
    r = client.post("/api/upload", files={"file": ("test.jpg", fake_img, "image/jpeg")}, headers=admin_headers)
    assert r.status_code == 201, f"Image upload failed: {r.text}"
    uploaded_url = r.json()["data"]["url"]
    assert uploaded_url.startswith("/images/uploads/"), f"Unexpected url: {uploaded_url}"
    print(f"[PASS] 5. Multipart Upload: Image uploaded to {uploaded_url}")
    
    # 6. Category CRUD
    cat_slug = f"test-cat-{timestamp}"
    r = client.post("/api/admin/categories", headers=admin_headers, json={
        "name": f"Test Category {timestamp}",
        "slug": cat_slug,
        "description": "A test category description",
        "image_url": uploaded_url,
        "order": 99,
        "is_active": True
    })
    assert r.status_code in (200, 201), f"Category create failed: {r.text}"
    cat_id = r.json()["data"]["id"]
    print(f"[PASS] 6a. Category CREATE: id={cat_id}, slug={cat_slug}")
    
    r = client.get(f"/api/categories")
    assert r.status_code == 200
    all_cats = r.json()["data"]
    assert any(c["slug"] == cat_slug for c in all_cats)
    print(f"[PASS] 6b. Category READ: Found category in list")
    
    r = client.put(f"/api/admin/categories/{cat_id}", headers=admin_headers, json={
        "name": f"Updated Category {timestamp}",
        "slug": cat_slug,
        "description": "Updated description",
        "image_url": uploaded_url,
        "order": 100,
        "is_active": True
    })
    assert r.status_code == 200
    print(f"[PASS] 6c. Category UPDATE: Modified properties")
    
    r = client.delete(f"/api/admin/categories/{cat_id}", headers=admin_headers)
    assert r.status_code == 200
    print(f"[PASS] 6d. Category DELETE: Successfully removed")
    
    # 7. Brand CRUD
    brand_slug = f"test-brand-{timestamp}"
    r = client.post("/api/admin/brands", headers=admin_headers, json={
        "name": f"Test Brand {timestamp}",
        "slug": brand_slug,
        "origin_country": "Japan",
        "description": "Atelier formulation test brand",
        "logo_url": uploaded_url,
        "banner_url": uploaded_url,
        "is_featured": True
    })
    assert r.status_code in (200, 201), f"Brand create failed: {r.text}"
    brand_id = r.json()["data"]["id"]
    print(f"[PASS] 7a. Brand CREATE: id={brand_id}, slug={brand_slug}")
    
    r = client.get("/api/admin/brands", headers=admin_headers)
    assert r.status_code == 200
    all_brands = r.json()["data"]
    assert any(b["id"] == brand_id for b in all_brands)
    print(f"[PASS] 7b. Brand READ: Found brand in admin list")
    
    r = client.put(f"/api/admin/brands/{brand_id}", headers=admin_headers, json={
        "name": f"Updated Brand {timestamp}",
        "description": "Updated brand bio"
    })
    assert r.status_code == 200
    print(f"[PASS] 7c. Brand UPDATE: Modified brand details")
    
    r = client.delete(f"/api/admin/brands/{brand_id}", headers=admin_headers)
    assert r.status_code == 200
    print(f"[PASS] 7d. Brand DELETE: Removed brand")
    
    # 8. Product CRUD
    prod_slug = f"test-prod-{timestamp}"
    r = client.post("/api/admin/products", headers=admin_headers, json={
        "name": f"Atelier Test Elixir {timestamp}",
        "slug": prod_slug,
        "subtitle": "Radiance Boosting Serum",
        "category_id": 1,
        "brand_id": 1,
        "price": 45.0,
        "stock": 25,
        "skin_type": ["All Skin Types"],
        "skin_concern": ["Radiance", "Anti-Aging"],
        "image_url": uploaded_url,
        "is_active": True
    })
    assert r.status_code in (200, 201), f"Product create failed: {r.text}"
    prod_id = r.json()["data"]["id"]
    print(f"[PASS] 8a. Product CREATE: id={prod_id}, slug={prod_slug}")
    
    r = client.get(f"/api/products/{prod_slug}")
    assert r.status_code == 200
    print(f"[PASS] 8b. Product READ: Retrieved product detail view")
    
    r = client.put(f"/api/admin/products/{prod_id}", headers=admin_headers, json={
        "name": f"Updated Atelier Elixir {timestamp}",
        "price": 52.0,
        "stock": 30
    })
    assert r.status_code == 200
    print(f"[PASS] 8c. Product UPDATE: Updated pricing and inventory")
    
    r = client.delete(f"/api/admin/products/{prod_id}", headers=admin_headers)
    assert r.status_code == 200
    print(f"[PASS] 8d. Product DELETE: Removed product")
    
    # 9. Article CRUD
    art_slug = f"test-article-{timestamp}"
    r = client.post("/api/articles", headers=admin_headers, json={
        "title": f"The Science of Atelier Skincare {timestamp}",
        "slug": art_slug,
        "category": "Dermatology",
        "author_name": "Dr. Luméa",
        "read_time": "5 min",
        "excerpt": "Discover how pure botanicals restore barrier strength.",
        "content": "<p>Detailed editorial skincare guide...</p>",
        "hero_image": uploaded_url,
        "thumbnail": uploaded_url,
        "status": "Published"
    })
    assert r.status_code in (200, 201), f"Article create failed: {r.text}"
    art_data = r.json()
    print(f"[PASS] 9a. Article CREATE: slug={art_slug}")
    
    r = client.get(f"/api/articles/{art_slug}")
    assert r.status_code == 200
    print(f"[PASS] 9b. Article READ: Found published article")
    
    r = client.put(f"/api/articles/{art_slug}", headers=admin_headers, json={
        "title": f"Updated Science of Atelier Skincare {timestamp}",
        "read_time": "6 min"
    })
    assert r.status_code == 200
    print(f"[PASS] 9c. Article UPDATE: Updated read time and title")
    
    r = client.delete(f"/api/articles/{art_slug}", headers=admin_headers)
    assert r.status_code in (200, 204), f"Article delete failed: {r.text}"
    print(f"[PASS] 9d. Article DELETE: Removed article")
    
    print("=" * 60)
    print("ALL AUTH & CRUD OPERATIONS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
