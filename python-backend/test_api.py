import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("[TEST] Running Lumea FastAPI Automated Endpoint Verification...")
    print("=" * 60)

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. GET /api/health ->", res.json()["service"])

    # 2. Categories
    res = client.get("/api/categories")
    assert res.status_code == 200, f"Categories failed: {res.text}"
    data = res.json()["data"]
    assert len(data) >= 8, f"Expected 8 categories, got {len(data)}"
    print(f"[PASS] 2. GET /api/categories -> Returned {len(data)} categories (e.g. {data[0]['name']})")

    # 3. Products List & Search
    res = client.get("/api/products")
    assert res.status_code == 200, f"Products failed: {res.text}"
    prods = res.json()["data"]
    assert len(prods) >= 30, f"Expected at least 30 products, got {len(prods)}"
    print(f"[PASS] 3. GET /api/products -> Returned {len(prods)} products in catalog")

    # 4. Search Filter
    res = client.get("/api/products?search=Ordinary")
    assert res.status_code == 200
    ordinary_prods = res.json()["data"]
    assert len(ordinary_prods) > 0
    print(f"[PASS] 4. GET /api/products?search=Ordinary -> Found {len(ordinary_prods)} matching items")

    # 5. Featured Products
    res = client.get("/api/products/featured")
    assert res.status_code == 200
    featured = res.json()["data"]
    print(f"[PASS] 5. GET /api/products/featured -> Found {len(featured)} featured items")

    # 6. Single Product by Slug
    res = client.get("/api/products/sk-ii-facial-treatment-essence")
    assert res.status_code == 200
    single = res.json()
    assert single["data"]["brand"] == "SK-II"
    assert len(single["related"]) > 0
    print(f"[PASS] 6. GET /api/products/sk-ii-facial-treatment-essence -> Loaded: {single['data']['name']} with {len(single['related'])} related items")

    # 7. Authentication: Login with demo credentials
    res = client.post("/api/auth/login", json={
        "email": "sreynich.chan@example.com",
        "password": "password123"
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    token_data = res.json()["data"]
    token = token_data["access_token"]
    user_name = token_data["user"]["name"]
    print(f"[PASS] 7. POST /api/auth/login -> Logged in as: {user_name} (JWT token generated)")

    # 8. Authenticated Route: GET /api/auth/me
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "sreynich.chan@example.com"
    print(f"[PASS] 8. GET /api/auth/me -> Verified user profile: {res.json()['tier']}")

    # 9. Orders: Place new order
    order_payload = {
        "customer_name": "Sreynich Chan",
        "customer_email": "sreynich.chan@example.com",
        "customer_phone": "+855 12 345 678",
        "shipping_address": "Norodom Blvd #45",
        "shipping_city": "Phnom Penh",
        "shipping_postal_code": "12000",
        "payment_method": "aba_pay",
        "discount_code": "LUMEA10",
        "items": [
            {
                "product_id": 201,
                "product_name": "Facial Treatment Essence",
                "price": 99.00,
                "quantity": 1
            },
            {
                "product_id": 202,
                "product_name": "Niacinamide 10% + Zinc 1%",
                "price": 8.90,
                "quantity": 2
            }
        ]
    }
    res = client.post("/api/orders", json=order_payload)
    assert res.status_code == 201, f"Place order failed: {res.text}"
    created_order = res.json()["data"]
    ord_num = created_order["order_number"]
    total = created_order["total"]
    print(f"[PASS] 9. POST /api/orders -> Order {ord_num} placed successfully! Total: ${total}")

    # 10. Track Order by Order Number
    res = client.get(f"/api/orders/{ord_num}")
    assert res.status_code == 200
    tracked = res.json()["data"]
    assert tracked["status"] == "Confirmed"
    assert len(tracked["items"]) == 2
    print(f"[PASS] 10. GET /api/orders/{ord_num} -> Order status: {tracked['status']} with {len(tracked['items'])} items")

    # 11. Banners List
    res = client.get("/api/banners")
    assert res.status_code == 200
    banners_list = res.json()["data"]
    assert len(banners_list) >= 8
    print(f"[PASS] 11. GET /api/banners -> Found {len(banners_list)} active page banners")

    # 12. Single Banner by Page Slug
    res = client.get("/api/banners/home")
    assert res.status_code == 200
    home_banner = res.json()["data"]
    assert home_banner["page"] == "home"
    assert "Beauty" in home_banner["title"]
    # 13. CMS Pages List
    res = client.get("/api/pages")
    assert res.status_code == 200
    pages_list = res.json()["data"]
    assert len(pages_list) >= 2
    print(f"[PASS] 13. GET /api/pages -> Found {len(pages_list)} published CMS pages")

    # 14. Single CMS Page by Slug
    res = client.get("/api/pages/privacy-policy")
    assert res.status_code == 200
    privacy_page = res.json()
    assert privacy_page["slug"] == "privacy-policy"
    assert len(privacy_page["content_json"]["sections"]) == 13
    print(f"[PASS] 14. GET /api/pages/privacy-policy -> Loaded: '{privacy_page['title']}' with 13 sections")

    # 15. Skincare Journal Articles List
    res = client.get("/api/articles")
    assert res.status_code == 200
    articles_resp = res.json()
    assert articles_resp["total"] >= 7
    assert len(articles_resp["data"]) == 6  # 6 per page
    assert len(articles_resp["popular"]) >= 4
    print(f"[PASS] 15. GET /api/articles -> Found {articles_resp['total']} articles, 4 popular items")

    # 16. Single Article by Slug with Related Items
    res = client.get("/api/articles/how-to-build-a-skincare-routine-for-your-skin-type")
    assert res.status_code == 200
    single_art = res.json()
    assert single_art["data"]["title"] == "How to Build a Skincare Routine for Your Skin Type"
    assert len(single_art["data"]["toc"]) == 8
    assert len(single_art["related"]) > 0
    print(f"[PASS] 16. GET /api/articles/how-to-build-a-skincare-routine-for-your-skin-type -> Loaded with {len(single_art['related'])} related articles")

    # 17. Returns List
    res = client.get("/api/returns")
    assert res.status_code == 200
    ret_list = res.json()["data"]
    assert len(ret_list) >= 1
    print(f"[PASS] 17. GET /api/returns -> Found {len(ret_list)} return requests in database")

    # 18. Return Request by ID (RR24081234)
    res = client.get("/api/returns/RR24081234")
    assert res.status_code == 200
    ret_req = res.json()
    assert ret_req["request_number"] == "RR24081234"
    assert ret_req["status"] == "Approved"
    assert len(ret_req["timeline"]) == 7
    print(f"[PASS] 18. GET /api/returns/RR24081234 -> Loaded request: {ret_req['status']} with 7 timeline stages")

    # 19. Admin Atelier Stats (KPIs, revenue, orders breakdown)
    res = client.get("/api/admin/stats")
    assert res.status_code == 200
    stats_data = res.json()["data"]
    assert stats_data["metrics"]["total_products"] >= 30
    assert stats_data["metrics"]["total_orders"] >= 1
    assert "orders_by_status" in stats_data
    assert len(stats_data["categories"]) >= 8
    print(f"[PASS] 19. GET /api/admin/stats -> Revenue: ${stats_data['metrics']['total_revenue']}, {stats_data['metrics']['total_orders']} orders, {stats_data['metrics']['total_products']} products")

    # 20. Admin Orders List
    res = client.get("/api/admin/orders")
    assert res.status_code == 200
    admin_orders = res.json()
    assert admin_orders["status"] == "success"
    assert len(admin_orders["data"]) >= 1
    print(f"[PASS] 20. GET /api/admin/orders -> Loaded {len(admin_orders['data'])} orders with pagination metadata")

    # 21. Admin Customers List
    res = client.get("/api/admin/customers")
    assert res.status_code == 200
    cust_data = res.json()
    assert cust_data["status"] == "success"
    assert len(cust_data["data"]) >= 1
    print(f"[PASS] 21. GET /api/admin/customers -> Found {len(cust_data['data'])} registered clientele records")

    # 22. File Upload API
    test_file_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb"
    res = client.post("/api/upload", files={"file": ("test_upload.jpg", test_file_bytes, "image/jpeg")})
    assert res.status_code == 201, f"Upload failed: {res.text}"
    upload_res = res.json()
    assert upload_res["status"] == "success"
    assert "url" in upload_res["data"]
    print(f"[PASS] 22. POST /api/upload -> Uploaded image: {upload_res['data']['url']}")

    # 23. Public Reviews API
    res = client.get("/api/reviews")
    assert res.status_code == 200
    rev_data = res.json()
    assert rev_data["status"] == "success"
    assert len(rev_data["data"]) >= 1
    print(f"[PASS] 23. GET /api/reviews -> Found {len(rev_data['data'])} approved customer reviews (Avg: {rev_data['metrics']['average_rating']} stars)")

    # 24. Submit Customer Review
    res = client.post("/api/reviews", json={
        "product_id": 201,
        "rating": 5,
        "title": "Unparalleled Radiance",
        "comment": "Absolutely transformative for texture and tone. Worth every single drop!",
        "customer_name": "Sreynich Chan",
        "customer_email": "sreynich.chan@example.com"
    })
    assert res.status_code == 201
    assert res.json()["status"] == "success"
    print("[PASS] 24. POST /api/reviews -> Successfully submitted customer review for product #201")

    # 25. Public Active Skin Quiz API
    res = client.get("/api/quizzes/active")
    assert res.status_code == 200
    quiz_data = res.json()
    assert quiz_data["status"] == "success"
    assert len(quiz_data["data"]["questions"]) >= 1
    print(f"[PASS] 25. GET /api/quizzes/active -> Loaded active quiz: '{quiz_data['data']['title']}' with {len(quiz_data['data']['questions'])} questions")

    # 26. Public Store Settings API
    res = client.get("/api/settings")
    assert res.status_code == 200
    sett_data = res.json()
    assert sett_data["status"] == "success"
    assert "free_shipping_threshold" in sett_data["data"]
    assert "tax_rate" in sett_data["data"]
    print(f"[PASS] 26. GET /api/settings -> Store: '{sett_data['data']['store_name']}', Free Shipping Threshold: ${sett_data['data']['free_shipping_threshold']}, Tax Rate: {sett_data['data']['tax_rate']}%")

    # 27. Video Reviews API
    res = client.get("/api/reviews?has_video=true")
    assert res.status_code == 200
    v_data = res.json()
    assert v_data["status"] == "success"
    assert len(v_data["data"]) >= 1
    assert v_data["data"][0]["video_url"] is not None
    print(f"[PASS] 27. GET /api/reviews?has_video=true -> Found {len(v_data['data'])} UGC video reviews (e.g. {v_data['data'][0]['video_url']})")

    # 28. Video Upload API
    dummy_video_bytes = b"\x00\x00\x00\x18ftypmp42\x00\x00\x00\x00isommp42\x00\x00\x00\x08free"
    res = client.post("/api/upload/video", files={"file": ("sample_reel.mp4", dummy_video_bytes, "video/mp4")})
    assert res.status_code == 201, f"Video upload failed: {res.text}"
    v_upload = res.json()
    assert v_upload["status"] == "success"
    assert "url" in v_upload["data"]
    print(f"[PASS] 28. POST /api/upload/video -> Uploaded streaming video: {v_upload['data']['url']}")

    print("=" * 60)
    print(f"[SUCCESS] ALL 28/28 ENDPOINT TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()

