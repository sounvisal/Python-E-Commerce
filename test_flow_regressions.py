"""Regression tests: disposable SQLite; no real orders, payments or external calls."""
import sys
import unittest
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).parent / 'python-backend'))
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import ValidationError
from app.core.database import Base
from app.models import Category, Product, Order, OrderItem, User
from app.models.promotion import Promotion
from app.api.orders import place_order, calculate_quote
from app.schemas.order import OrderCreate
from app.schemas.return_request import ReturnRequestCreate
from app.api.returns import submit_return_request
from app.api.payments import generate_khqr, KHQRGenerateRequest, simulate_khqr_approval, KHQRSimulateRequest
from app.core.config import settings

class CommerceFlows(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)
        self.db.add(Category(id=1, name='Cleanser', slug='cleansers'))
        self.db.add(Product(id=1, category_id=1, name='Cleanser', brand='Test', slug='cleanser', category='cleansers', category_name='Cleanser', price=50, stock=10, image_url='/test.jpg'))
        self.db.commit()
        self.user = User(email='test@example.test', name='Test', hashed_password='unused', role='customer')
        self.db.add(self.user)
        self.db.add(Promotion(name='Test promo', code='LUMEA20', percent=20, max_uses=1000))
        self.db.commit()
    def tearDown(self):
        self.db.close()
        self.engine.dispose()
    def payload(self, **overrides):
        value = dict(customer_name='Test', customer_email=self.user.email, shipping_address='Test street', shipping_city='Test', payment_method='cod', expected_total=50, items=[{'product_id':1,'quantity':1}])
        value.update(overrides)
        return OrderCreate(**value)
    def place(self, payload):
        data = place_order(payload, self.db, self.user)['data']
        return self.db.get(Order, data['id'])
    def delivered(self):
        order = self.place(self.payload())
        order.status='Delivered'; order.payment_status='Paid'; self.db.commit()
        return order
    def return_payload(self, order, **overrides):
        value=dict(order_number=order.order_number, order_item_id=order.items[0].id, product_name='Forged name', price=999, quantity=1, reason='Damaged', resolution='Refund to original payment method')
        value.update(overrides)
        return ReturnRequestCreate(**value)
    def test_client_price_and_name_do_not_override_catalog(self):
        quote, lines=calculate_quote(self.payload(items=[{'product_id':1,'price':0.01,'product_name':'Fake','quantity':1}]),self.db)
        self.assertEqual(quote['total'],50)
        self.assertEqual(lines[0]['product_name'],'Cleanser')
    def test_missing_product_rejected(self):
        with self.assertRaises(HTTPException): calculate_quote(self.payload(items=[{'product_id':999,'quantity':1}]),self.db)
    def test_quantity_must_be_positive(self):
        with self.assertRaises(ValidationError): self.payload(items=[{'product_id':1,'quantity':0}])
    def test_cumulative_stock_checked(self):
        with self.assertRaises(HTTPException): calculate_quote(self.payload(items=[{'product_id':1,'quantity':6},{'product_id':1,'quantity':6}]),self.db)
    def test_coupon_shipping_threshold_matches_display(self):
        q,_=calculate_quote(self.payload(discount_code='LUMEA20'),self.db)
        self.assertEqual(q['total'],40)
        self.assertEqual(q['shipping_fee'],0)
    def test_invented_coupon_rejected(self):
        with self.assertRaises(HTTPException): calculate_quote(self.payload(discount_code='NOTREAL20'),self.db)
    def test_total_change_requires_review(self):
        with self.assertRaises(HTTPException) as error: place_order(self.payload(expected_total=0.01),self.db,self.user)
        self.assertEqual(error.exception.status_code,409)
        self.assertEqual(self.db.query(Order).count(),0)
    def test_cod_unpaid_and_khqr_pending(self):
        self.assertEqual(self.place(self.payload()).payment_status,'Unpaid')
        order=self.place(self.payload(payment_method='khqr'))
        self.assertEqual((order.status,order.payment_status),('Pending','Pending'))
    def test_unsupported_gateways_rejected(self):
        for method in ('card','apple_pay'):
            with self.assertRaises(HTTPException): place_order(self.payload(payment_method=method),self.db,self.user)
    def test_qr_amount_and_paid_order_guarded(self):
        order=self.place(self.payload(payment_method='khqr'))
        with self.assertRaises(HTTPException): generate_khqr(KHQRGenerateRequest(order_number=order.order_number,amount=0.01),self.db,self.user,None).send(None)
        order.payment_status='Paid'; self.db.commit()
        with self.assertRaises(HTTPException): generate_khqr(KHQRGenerateRequest(order_number=order.order_number,amount=50),self.db,self.user,None).send(None)
        self.assertEqual(order.payment_status,'Paid')
    def test_demo_approval_disabled(self):
        order=self.delivered()
        old=settings.ENABLE_DEMO_PAYMENTS
        settings.ENABLE_DEMO_PAYMENTS=False
        try:
            with self.assertRaises(HTTPException): simulate_khqr_approval(KHQRSimulateRequest(order_number=order.order_number),self.db,self.user)
            self.assertEqual(order.status,'Delivered')
        finally: settings.ENABLE_DEMO_PAYMENTS=old
    def test_return_price_ownership_and_duplicate(self):
        order=self.delivered()
        with self.assertRaises(HTTPException): submit_return_request(self.return_payload(order),self.db,SimpleNamespace(id=999,email='other@example.test',role='customer'))
        request=submit_return_request(self.return_payload(order),self.db,self.user)
        self.assertEqual(request.price,50)
        self.assertEqual(request.product_name,'Cleanser')
        with self.assertRaises(HTTPException): submit_return_request(self.return_payload(order),self.db,self.user)
    def test_nonexistent_and_undelivered_returns_rejected(self):
        order=self.place(self.payload())
        with self.assertRaises(HTTPException): submit_return_request(self.return_payload(order),self.db,self.user)
        with self.assertRaises(HTTPException): submit_return_request(self.return_payload(order,order_number='missing'),self.db,self.user)
    def test_expired_return_rejected(self):
        order=self.delivered(); order.created_at=datetime.now(timezone.utc)-timedelta(days=31); self.db.commit()
        with self.assertRaises(HTTPException): submit_return_request(self.return_payload(order),self.db,self.user)

if __name__=='__main__': unittest.main(verbosity=2)
