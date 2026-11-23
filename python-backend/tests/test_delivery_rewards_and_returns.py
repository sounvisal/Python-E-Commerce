import secrets
from app.core.database import SessionLocal
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.return_request import ReturnRequest
from app.core.security import create_access_token

def test_cod_delivery_credits_reward_points(client):
    db = SessionLocal()
    customer_email = f"rewardscod_{secrets.token_hex(4)}@lumea.com"
    order_num = f"LUM-RWD-{secrets.token_hex(4).upper()}"

    customer = User(
        name="Rewards Customer",
        email=customer_email,
        hashed_password="hash",
        role="customer",
        tier="Luméa Member",
        reward_points=100,
        token_version=1
    )
    db.add(customer)

    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        admin = User(name="Admin User", email="admin_test@lumea.com", role="admin", hashed_password="hash", token_version=1)
        db.add(admin)
    db.commit()
    db.refresh(customer)
    db.refresh(admin)

    # Place a COD order with expected total $50.00
    order = Order(
        order_number=order_num,
        customer_name=customer.name,
        customer_email=customer.email,
        user_id=customer.id,
        shipping_address="Street 240",
        shipping_city="Phnom Penh",
        shipping_carrier="vet_express",
        subtotal=50.0,
        discount=0.0,
        shipping_fee=0.0,
        total=50.0,
        payment_method="cod",
        payment_status="Unpaid",
        status="Confirmed",
        stock_reserved=True
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    admin_token = create_access_token(admin.id, token_version=admin.token_version)

    # Step through fulfillment to Delivered
    r_proc = client.patch(f"/api/orders/{order.order_number}/status", json={"status": "Processing"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert r_proc.status_code == 200

    r_ship = client.patch(f"/api/orders/{order.order_number}/status", json={"status": "Shipped"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert r_ship.status_code == 200

    r_out = client.patch(f"/api/orders/{order.order_number}/status", json={"status": "Out for Delivery"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert r_out.status_code == 200

    # Advance to Delivered
    r_del = client.patch(f"/api/orders/{order.order_number}/status", json={"status": "Delivered"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert r_del.status_code == 200
    assert r_del.json()["data"]["status"] == "Delivered"
    assert r_del.json()["data"]["payment_status"] == "Paid"

    # Refresh customer and verify reward points increased by 50 (from 100 to 150)
    db.refresh(customer)
    assert customer.reward_points == 150, f"Expected 150 reward points, got {customer.reward_points}"

    # Clean up
    db.delete(order)
    db.delete(customer)
    db.commit()
    db.close()

def test_return_rejection_decrements_returned_quantity(client):
    db = SessionLocal()
    order_num = f"LUM-RET-{secrets.token_hex(4).upper()}"
    req_num = f"RR-{secrets.token_hex(4).upper()}"

    order = Order(
        order_number=order_num,
        customer_name="Return Buyer",
        customer_email="returnbuyer@lumea.com",
        shipping_address="Street 1",
        shipping_city="Phnom Penh",
        subtotal=40.0,
        total=40.0,
        status="Delivered",
        payment_status="Paid"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    item = OrderItem(
        order_id=order.id,
        product_id=201,
        product_name="Essence",
        price=40.0,
        quantity=2,
        returned_quantity=1,
        total=40.0
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    req = ReturnRequest(
        request_number=req_num,
        order_number=order.order_number,
        order_item_id=item.id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        product_name="Essence",
        reason="Defective",
        resolution="Refund",
        status="Under Review",
        quantity=1,
        price=40.0
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    admin = db.query(User).filter(User.role == "admin").first()
    if not admin:
        admin = User(name="Admin User", email="admin_test@lumea.com", role="admin", hashed_password="hash", token_version=1)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    admin_token = create_access_token(admin.id, token_version=admin.token_version)

    # Reject return request via admin API
    res = client.patch(f"/api/returns/{req.id}/status", json={"status": "Rejected"}, headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.json()["status"] == "Rejected"

    # Verify OrderItem returned_quantity was decremented back to 0
    db.refresh(item)
    assert item.returned_quantity == 0

    db.delete(req)
    db.delete(item)
    db.delete(order)
    db.commit()
    db.close()
