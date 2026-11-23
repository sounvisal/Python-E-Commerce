"""
Comprehensive test suite for Cash-on-Delivery (COD) stock reservation & lifecycle.

Covers:
1. Signed-in customer submission (local Krong Kampot only) -> creates 'Awaiting Confirmation', stock unreserved.
2. Canonical destination enforcement: Krong Kampot vs other districts vs other provinces.
3. Pending limit: at most 1 open unconfirmed COD order per account (enforced atomically).
4. Idempotent retry: same checkout key returns existing order.
5. Admin-only confirmation: checks all stock, reserves exactly once.
6. Insufficient stock on confirmation: rolls back with HTTP 409 and zero partial deduction.
7. Last-unit concurrent confirmation race protection.
8. Cancellation before confirmation: cancels order, stock unchanged.
9. Cancellation after confirmation: cancels order, stock restored exactly once (idempotent).
10. Expiry sweep: 24h expired COD order swept to 'Expired', no ghost inventory.
11. Legacy / existing orders remain fulfillable.
12. Promotion counter safety under placement and cancellation.
"""
import uuid
import secrets
from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.product import Product
from app.models.order import Order
from app.models.promotion import Promotion
from app.models.user import User
from app.core.security import create_access_token
from app.services.order_lifecycle import expire_pending_orders, utcnow

def create_disposable_user(db: Session, email_prefix: str, role: str = "customer") -> tuple[User, str]:
    uid = uuid.uuid4().hex[:8]
    email = f"{email_prefix}_{uid}@atelier-test.com"
    user = User(
        name=f"Test {email_prefix.capitalize()}",
        email=email,
        hashed_password="hashed_pw_test",
        role=role,
        phone="+85512345678"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.email, token_version=getattr(user, "token_version", 1))
    return user, token

def create_disposable_product(db: Session, name_prefix: str, stock: int = 10, price: float = 25.0) -> Product:
    uid = uuid.uuid4().hex[:8]
    slug = f"prod-{name_prefix}-{uid}"
    product = Product(
        name=f"Atelier Formulation {name_prefix} {uid}",
        brand="Luméa Atelier",
        slug=slug,
        category="face-serums",
        category_name="Face Serums",
        category_id=1,
        image_url="/images/prod-sk2.jpg",
        price=price,
        stock=stock,
        description="Disposable product for testing inventory transitions"
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def test_signed_in_customer_cod_submission_creates_awaiting_confirmation_without_stock_deduction(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "cod_cust")
    product = create_disposable_product(db, "serum", stock=15, price=30.0)
    initial_stock = product.stock

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 730, Riverside",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 2}]
    }
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}
    
    quote_res = client.post("/api/orders/quote", json=payload, headers=headers)
    assert quote_res.status_code == 200, quote_res.text
    payload["expected_total"] = quote_res.json()["data"]["total"]

    res = client.post("/api/orders", json=payload, headers=headers)
    assert res.status_code == 201, res.text
    order_data = res.json()["data"]

    # Verify order state: Awaiting Confirmation, Unpaid, stock_reserved = False
    assert order_data["status"] == "Awaiting Confirmation"
    assert order_data["payment_status"] == "Unpaid"
    assert order_data["stock_reserved"] is False
    assert order_data["expires_at"] is not None

    # Verify database stock was NOT decremented
    db.refresh(product)
    assert product.stock == initial_stock, "COD order creation must not decrement stock before staff confirmation!"

def test_canonical_destination_rule_rejects_outside_town_cod(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "remote_cust")
    product = create_disposable_product(db, "cream", stock=10, price=20.0)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    invalid_cities = [
        "Kampot Province (Other Districts)",
        "Phnom Penh",
        "Siem Reap",
        "Tuek Chhou",
        "Chhouk",
        "Kampot",  # bare name without town qualification
        "South Kampot",
        "",
    ]

    for city in invalid_cities:
        payload = {
            "customer_name": customer.name,
            "customer_email": customer.email,
            "customer_phone": "+85512345678",
            "shipping_address": "Village 2",
            "shipping_city": city,
            "payment_method": "cod",
            "items": [{"product_id": product.id, "quantity": 1}]
        }
        res = client.post("/api/orders", json=payload, headers=headers)
        assert res.status_code == 400, f"Expected 400 for city '{city}', got {res.status_code}: {res.text}"
        assert "Cash on delivery is only available within Krong Kampot" in res.text

    # Verify remote delivery accepts KHQR
    khqr_payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 200",
        "shipping_city": "Phnom Penh",
        "payment_method": "khqr",
        "items": [{"product_id": product.id, "quantity": 1}]
    }
    quote_res = client.post("/api/orders/quote", json=khqr_payload, headers=headers)
    assert quote_res.status_code == 200
    khqr_payload["expected_total"] = quote_res.json()["data"]["total"]
    khqr_res = client.post("/api/orders", json=khqr_payload, headers=headers)
    assert khqr_res.status_code == 201
    assert khqr_res.json()["data"]["status"] == "Pending"
    assert khqr_res.json()["data"]["stock_reserved"] is True

def test_single_open_unconfirmed_cod_limit_per_account(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "single_cod_user")
    p1 = create_disposable_product(db, "item1", stock=10)
    p2 = create_disposable_product(db, "item2", stock=10)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    payload1 = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 1",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": p1.id, "quantity": 1}]
    }
    q1 = client.post("/api/orders/quote", json=payload1, headers=headers).json()["data"]["total"]
    payload1["expected_total"] = q1
    res1 = client.post("/api/orders", json=payload1, headers=headers)
    assert res1.status_code == 201

    # Attempt to create a second COD order for the same account
    payload2 = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 2",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": p2.id, "quantity": 1}]
    }
    q2 = client.post("/api/orders/quote", json=payload2, headers=headers).json()["data"]["total"]
    payload2["expected_total"] = q2
    res2 = client.post("/api/orders", json=payload2, headers=headers)
    assert res2.status_code == 409
    assert "already have an open Cash-on-Delivery order awaiting confirmation" in res2.text

def test_idempotent_retry_returns_existing_cod_order(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "retry_user")
    product = create_disposable_product(db, "retry_prod", stock=10)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    checkout_key = "test_checkout_key_" + secrets.token_hex(16)
    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Riverside Road",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "checkout_key": checkout_key,
        "items": [{"product_id": product.id, "quantity": 1}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers).json()["data"]["total"]
    payload["expected_total"] = q

    res1 = client.post("/api/orders", json=payload, headers=headers)
    assert res1.status_code == 201
    order1 = res1.json()["data"]

    # Re-send same request with same checkout_key
    res2 = client.post("/api/orders", json=payload, headers=headers)
    assert res2.status_code == 201
    order2 = res2.json()["data"]
    assert order1["order_number"] == order2["order_number"]

def test_admin_only_confirmation_and_stock_deduction(client: TestClient, db: Session):
    customer, cust_token = create_disposable_user(db, "reg_user")
    admin, admin_token = create_disposable_user(db, "admin_user", role="admin")
    product = create_disposable_product(db, "confirm_prod", stock=5)
    
    headers_cust = {"Authorization": f"Bearer {cust_token}", "X-Test-Client": "true"}
    headers_admin = {"Authorization": f"Bearer {admin_token}", "X-Test-Client": "true"}

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Old Market Street",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 2}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers_cust).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers_cust).json()["data"]
    ord_num = order["order_number"]

    # Non-admin cannot confirm COD order
    non_admin_res = client.post(f"/api/orders/{ord_num}/confirm-cod", headers=headers_cust)
    assert non_admin_res.status_code == 403

    # Admin confirms COD order
    admin_res = client.post(f"/api/orders/{ord_num}/confirm-cod", headers=headers_admin)
    assert admin_res.status_code == 200, admin_res.text
    confirmed = admin_res.json()["data"]
    assert confirmed["status"] == "Confirmed"
    assert confirmed["stock_reserved"] is True

    # Stock is now decremented by exactly 2
    db.refresh(product)
    assert product.stock == 3

    # Idempotent confirmation attempt returns confirmed order without double decrement
    admin_res2 = client.post(f"/api/orders/{ord_num}/confirm-cod", headers=headers_admin)
    assert admin_res2.status_code == 200
    db.refresh(product)
    assert product.stock == 3, "Repeated confirmation must not double decrement stock!"

def test_insufficient_stock_on_confirmation_aborts_without_partial_deduction(client: TestClient, db: Session):
    customer, cust_token = create_disposable_user(db, "stockout_cust")
    admin, admin_token = create_disposable_user(db, "stockout_admin", role="admin")
    p_available = create_disposable_product(db, "p_avail", stock=5)
    p_depleted = create_disposable_product(db, "p_depleted", stock=3)

    headers_cust = {"Authorization": f"Bearer {cust_token}", "X-Test-Client": "true"}
    headers_admin = {"Authorization": f"Bearer {admin_token}", "X-Test-Client": "true"}

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "French Quarter",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [
            {"product_id": p_available.id, "quantity": 2},
            {"product_id": p_depleted.id, "quantity": 3}
        ]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers_cust).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers_cust).json()["data"]
    ord_num = order["order_number"]

    # Now simulate another order consuming all stock of p_depleted
    db.execute(update(Product).where(Product.id == p_depleted.id).values(stock=0))
    db.commit()

    # Admin tries to confirm COD order
    res = client.post(f"/api/orders/{ord_num}/confirm-cod", headers=headers_admin)
    assert res.status_code == 409
    assert "insufficient stock" in res.text.lower()

    # Verify ZERO partial deduction: p_available stock must remain untouched at 5!
    db.refresh(p_available)
    assert p_available.stock == 5, "Insufficient stock confirmation must roll back with zero partial deduction!"

    # Order remains in Awaiting Confirmation
    o_db = db.query(Order).filter(Order.order_number == ord_num).first()
    assert o_db.status == "Awaiting Confirmation"
    assert o_db.stock_reserved is False

def test_cancellation_before_confirmation_does_not_alter_stock(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "cancel_before_cust")
    product = create_disposable_product(db, "cancel_prod", stock=8)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Lotus Street",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 3}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers).json()["data"]
    ord_num = order["order_number"]

    # Customer cancels before staff confirmation
    cancel_res = client.post(f"/api/orders/{ord_num}/cancel", headers=headers)
    assert cancel_res.status_code == 200
    assert cancel_res.json()["data"]["status"] == "Cancelled"

    # Stock must still be 8 (NOT 8 + 3 = 11!)
    db.refresh(product)
    assert product.stock == 8, "Cancelling unconfirmed order must not add unreserved stock!"

def test_cancellation_after_confirmation_restores_stock_exactly_once(client: TestClient, db: Session):
    customer, cust_token = create_disposable_user(db, "cancel_after_cust")
    admin, admin_token = create_disposable_user(db, "cancel_after_admin", role="admin")
    product = create_disposable_product(db, "cancel_after_prod", stock=10)
    
    headers_cust = {"Authorization": f"Bearer {cust_token}", "X-Test-Client": "true"}
    headers_admin = {"Authorization": f"Bearer {admin_token}", "X-Test-Client": "true"}

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Durian Roundabout",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 4}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers_cust).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers_cust).json()["data"]
    ord_num = order["order_number"]

    # Admin confirms -> stock decremented to 6
    client.post(f"/api/orders/{ord_num}/confirm-cod", headers=headers_admin)
    db.refresh(product)
    assert product.stock == 6

    # Cancel order -> stock restored from 6 back to 10
    cancel_res = client.post(f"/api/orders/{ord_num}/cancel", headers=headers_cust)
    assert cancel_res.status_code == 200
    db.refresh(product)
    assert product.stock == 10

    # Retry cancel -> stock remains 10 (no double restore)
    cancel_res2 = client.post(f"/api/orders/{ord_num}/cancel", headers=headers_cust)
    assert cancel_res2.status_code == 200
    db.refresh(product)
    assert product.stock == 10, "Retry cancellation must not double-restore stock!"

def test_24_hour_expiry_sweep_for_unconfirmed_cod(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "expired_cod_cust")
    product = create_disposable_product(db, "expired_prod", stock=12)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Salt Fields Road",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 2}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers).json()["data"]
    ord_num = order["order_number"]

    # Fast forward expiration date past 24 hours
    order_db = db.query(Order).filter(Order.order_number == ord_num).first()
    order_db.expires_at = utcnow() - timedelta(minutes=5)
    db.commit()

    # Run expiry sweep
    expire_pending_orders(db)
    db.commit()

    db.refresh(order_db)
    assert order_db.status == "Expired"
    assert order_db.payment_status == "Expired"

    # Product stock remains 12 (not 14)
    db.refresh(product)
    assert product.stock == 12, "Expiring unconfirmed COD order must not add phantom stock!"

def test_promotion_usage_counter_under_cod_lifecycle(client: TestClient, db: Session):
    customer, token = create_disposable_user(db, "promo_cust")
    product = create_disposable_product(db, "promo_prod", stock=10, price=50.0)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    promo_code = f"TEST_PROMO_{uuid.uuid4().hex[:6].upper()}"
    promo = Promotion(
        name="Test Promo",
        code=promo_code,
        percent=10,
        max_uses=10,
        used=0,
        status="Active"
    )
    db.add(promo)
    db.commit()

    payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 10",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "discount_code": promo_code,
        "items": [{"product_id": product.id, "quantity": 1}]
    }
    q = client.post("/api/orders/quote", json=payload, headers=headers).json()["data"]["total"]
    payload["expected_total"] = q
    order = client.post("/api/orders", json=payload, headers=headers).json()["data"]
    ord_num = order["order_number"]

    # Promo usage incremented to 1
    db.refresh(promo)
    assert promo.used == 1

    # Cancel order -> promo usage restored to 0
    client.post(f"/api/orders/{ord_num}/cancel", headers=headers)
    db.refresh(promo)
    assert promo.used == 0

    # Retry cancel -> remains 0
    client.post(f"/api/orders/{ord_num}/cancel", headers=headers)
    db.refresh(promo)
    assert promo.used == 0

def test_legacy_orders_remain_fulfillable(client: TestClient, db: Session):
    admin, admin_token = create_disposable_user(db, "legacy_admin", role="admin")
    product = create_disposable_product(db, "legacy_prod", stock=20)
    headers_admin = {"Authorization": f"Bearer {admin_token}", "X-Test-Client": "true"}

    # Simulate existing legacy confirmed order in DB
    legacy_ord = Order(
        order_number=f"LUM-LEGACY-{secrets.token_hex(4).upper()}",
        customer_name="Legacy Client",
        customer_email="legacy@example.com",
        customer_phone="+85512345678",
        shipping_address="123 Old St",
        shipping_city="Kampot",
        subtotal=50.0,
        discount=0.0,
        shipping_fee=1.0,
        total=51.0,
        status="Confirmed",
        payment_method="cod",
        payment_status="Unpaid",
        stock_reserved=True
    )
    db.add(legacy_ord)
    db.commit()
    db.refresh(legacy_ord)

    # Progression Confirmed -> Processing
    res1 = client.patch(f"/api/orders/{legacy_ord.order_number}/status", json={"status": "Processing"}, headers=headers_admin)
    assert res1.status_code == 200
    assert res1.json()["data"]["status"] == "Processing"

    # Progression Processing -> Shipped
    res2 = client.patch(f"/api/orders/{legacy_ord.order_number}/status", json={"status": "Shipped"}, headers=headers_admin)
    assert res2.status_code == 200
    assert res2.json()["data"]["status"] == "Shipped"

    # Progression Shipped -> Out for Delivery
    res3 = client.patch(f"/api/orders/{legacy_ord.order_number}/status", json={"status": "Out for Delivery"}, headers=headers_admin)
    assert res3.status_code == 200
    assert res3.json()["data"]["status"] == "Out for Delivery"

    # Progression Out for Delivery -> Delivered (records cash collection)
    res4 = client.patch(f"/api/orders/{legacy_ord.order_number}/status", json={"status": "Delivered"}, headers=headers_admin)
    assert res4.status_code == 200
    assert res4.json()["data"]["status"] == "Delivered"
    assert res4.json()["data"]["payment_status"] == "Paid"

def test_last_unit_concurrent_confirmation_race(client: TestClient, db: Session):
    """
    Two COD orders awaiting confirmation compete for the last unit of a product (stock = 1).
    First confirmation claims and reserves the unit, decrementing stock to 0.
    Second confirmation attempts to claim the unit and fails with HTTP 409 insufficient stock.
    Zero negative stock or partial deductions occur.
    """
    admin, admin_token = create_disposable_user(db, "race_admin", role="admin")
    cust1, token1 = create_disposable_user(db, "race_cust1")
    cust2, token2 = create_disposable_user(db, "race_cust2")
    product = create_disposable_product(db, "last_unit_prod", stock=1)

    headers_admin = {"Authorization": f"Bearer {admin_token}", "X-Test-Client": "true"}

    # Place order 1
    p1 = {
        "customer_name": cust1.name,
        "customer_email": cust1.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 101",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 1}]
    }
    q1 = client.post("/api/orders/quote", json=p1, headers={"Authorization": f"Bearer {token1}", "X-Test-Client": "true"}).json()["data"]["total"]
    p1["expected_total"] = q1
    ord1 = client.post("/api/orders", json=p1, headers={"Authorization": f"Bearer {token1}", "X-Test-Client": "true"}).json()["data"]["order_number"]

    # Place order 2
    p2 = {
        "customer_name": cust2.name,
        "customer_email": cust2.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Street 102",
        "shipping_city": "Krong Kampot (Kampot Town)",
        "payment_method": "cod",
        "items": [{"product_id": product.id, "quantity": 1}]
    }
    q2 = client.post("/api/orders/quote", json=p2, headers={"Authorization": f"Bearer {token2}", "X-Test-Client": "true"}).json()["data"]["total"]
    p2["expected_total"] = q2
    ord2 = client.post("/api/orders", json=p2, headers={"Authorization": f"Bearer {token2}", "X-Test-Client": "true"}).json()["data"]["order_number"]

    # Stock is still 1 (both are unconfirmed)
    db.refresh(product)
    assert product.stock == 1

    # Staff confirms ord1 -> succeeds, stock becomes 0
    res_conf1 = client.post(f"/api/orders/{ord1}/confirm-cod", headers=headers_admin)
    assert res_conf1.status_code == 200
    db.refresh(product)
    assert product.stock == 0

    # Staff attempts to confirm ord2 -> fails with HTTP 409 conflict
    res_conf2 = client.post(f"/api/orders/{ord2}/confirm-cod", headers=headers_admin)
    assert res_conf2.status_code == 409
    assert "insufficient stock" in res_conf2.text.lower()
    db.refresh(product)
    assert product.stock == 0, "Stock must never become negative!"

def test_switching_destination_between_local_districts_and_provinces(client: TestClient, db: Session):
    """
    Verifies destination evaluation:
    - Krong Kampot -> quote returns cod_eligible = True.
    - Other Kampot districts -> quote returns cod_eligible = False; COD submission blocked.
    - Other provinces (Phnom Penh) -> quote returns cod_eligible = False; COD submission blocked.
    """
    customer, token = create_disposable_user(db, "switch_user")
    product = create_disposable_product(db, "switch_prod", stock=10)
    headers = {"Authorization": f"Bearer {token}", "X-Test-Client": "true"}

    base_payload = {
        "customer_name": customer.name,
        "customer_email": customer.email,
        "customer_phone": "+85512345678",
        "shipping_address": "Main Road",
        "items": [{"product_id": product.id, "quantity": 1}]
    }

    # 1. Local town: Krong Kampot
    q_local = client.post("/api/orders/quote", json={**base_payload, "shipping_city": "Krong Kampot (Kampot Town)"}, headers=headers).json()["data"]
    assert q_local["cod_eligible"] is True

    # 2. Rural Kampot: Kampot Province (Other Districts)
    q_rural = client.post("/api/orders/quote", json={**base_payload, "shipping_city": "Kampot Province (Other Districts)"}, headers=headers).json()["data"]
    assert q_rural["cod_eligible"] is False

    # 3. Remote province: Phnom Penh
    q_remote = client.post("/api/orders/quote", json={**base_payload, "shipping_city": "Phnom Penh"}, headers=headers).json()["data"]
    assert q_remote["cod_eligible"] is False

    # Submitting COD for rural destination must fail
    res_rural_cod = client.post("/api/orders", json={
        **base_payload,
        "shipping_city": "Kampot Province (Other Districts)",
        "payment_method": "cod",
        "expected_total": q_rural["total"]
    }, headers=headers)
    assert res_rural_cod.status_code == 400
    assert "Cash on delivery is only available within Krong Kampot" in res_rural_cod.text

