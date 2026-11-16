"""Identity, checkout, inventory, publishing and operational regression coverage."""
import secrets
from pathlib import Path
import unittest
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy import create_engine, inspect, text
from fastapi import HTTPException
import test_flow_regressions as regression
from app.models import Order, Product, User, Article
from app.models.promotion import Promotion
from app.api import admin, articles, banners, pages, settings as settings_api, upload, returns
from app.api.orders import quote_order, place_order, get_order_by_number, list_all_orders, cancel_customer_order, claim_guest_order
from app.api.deps import require_admin, get_current_user
from app.services.order_lifecycle import check_order_access, cancel_order, expire_pending_orders, transition_order, settle_payment, utcnow
from app.core.database import Base
from app.core.config import settings
from app.core.migrations import migrate_schema
from app.api.promotions import PromotionPayload, update_promotion, validate_promotion
from app.api.reviews import ReviewSubmission, submit_review, vote_helpful
from app.api.articles import create_article, get_article_by_slug, update_article
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.api.returns import update_return_status
from app.schemas.return_request import ReturnRequestUpdateStatus
from app.api.payments import check_khqr_payment, KHQRCheckRequest, generate_khqr, KHQRGenerateRequest
from app.api.contact import create_inquiry, ContactPayload, SupportMessage

class AdditionalFlows(regression.CommerceFlows):
    def other_user(self):
        user=User(name='Other',email='other@example.test',hashed_password='unused',role='customer')
        self.db.add(user); self.db.commit(); return user
    def test_admin_permission(self):
        with self.assertRaises(HTTPException): require_admin(self.user)
        self.user.role='admin'
        self.assertEqual(require_admin(self.user).id,self.user.id)
    def test_admin_routes_and_content_mutations_have_permission_dependencies(self):
        self.assertIn(require_admin, [d.dependency for d in admin.router.dependencies])
        for router in (articles.router,banners.router,pages.router,settings_api.router):
            for route in router.routes:
                if route.methods.intersection({'POST','PUT','PATCH','DELETE'}):
                    self.assertIn(require_admin,[d.call for d in route.dependant.dependencies],route.path)
        for route in upload.router.routes:
            self.assertIn(get_current_user,[d.call for d in route.dependant.dependencies])
    def test_customer_list_cannot_select_another_customers_email(self):
        order=self.place(self.payload())
        other=self.other_user()
        self.assertEqual(list_all_orders(self.user.email,50,self.db,other),[])
        self.assertEqual(list_all_orders(other.email,50,self.db,self.user)[0].id,order.id)
    def test_guessing_order_reference_does_not_grant_access(self):
        order=self.place(self.payload()); other=self.other_user()
        with self.assertRaises(HTTPException): get_order_by_number(order.order_number,self.db,other,None)
        with self.assertRaises(HTTPException): get_order_by_number(order.order_number,self.db,None,None)
    def test_guest_token_and_claim(self):
        data=place_order(self.payload(checkout_key=secrets.token_urlsafe(24)),self.db,None)['data']
        number=data['order_number']; token=data['access_token']
        self.assertEqual(get_order_by_number(number,self.db,None,token)['data'].order_number,number)
        with self.assertRaises(HTTPException): get_order_by_number(number,self.db,None,'wrong-token')
        with self.assertRaises(HTTPException): claim_guest_order(number,self.db,self.other_user(),token)
        claim_guest_order(number,self.db,self.user,token)
        self.assertEqual(list_all_orders(None,50,self.db,self.user)[0].order_number,number)
    def test_checkout_retry_is_idempotent_and_reserves_stock_once(self):
        payload=self.payload(checkout_key=secrets.token_urlsafe(24))
        first=place_order(payload,self.db,self.user)['data']
        second=place_order(payload,self.db,self.user)['data']
        self.assertEqual(first['id'],second['id'])
        self.assertEqual(first['access_token'],second['access_token'])
        self.assertEqual(self.db.get(Product,1).stock,9)
        self.assertEqual(self.db.query(Order).count(),1)
    def test_retry_quote_accepts_its_own_last_unit_reservation(self):
        self.db.get(Product,1).stock=1; self.db.commit()
        payload=self.payload(payment_method='khqr',checkout_key=secrets.token_urlsafe(24))
        self.place(payload)
        self.assertEqual(quote_order(payload,self.db,self.user)['data']['total'],50)
        self.assertEqual(self.db.get(Product,1).stock,0)
    def test_reusing_key_for_different_bag_is_rejected(self):
        key=secrets.token_urlsafe(24)
        place_order(self.payload(checkout_key=key),self.db,self.user)
        with self.assertRaises(HTTPException): place_order(self.payload(checkout_key=key,items=[{'product_id':1,'quantity':2}],expected_total=100),self.db,self.user)
        self.assertEqual(self.db.get(Product,1).stock,9)
    def test_last_unit_cannot_be_ordered_twice(self):
        self.db.get(Product,1).stock=1; self.db.commit()
        self.place(self.payload())
        with self.assertRaises(HTTPException): self.place(self.payload())
        self.assertEqual(self.db.get(Product,1).stock,0)
        self.assertEqual(self.db.query(Order).count(),1)
    def test_cancel_releases_stock_once_and_does_not_lie_about_paid_order(self):
        order=self.place(self.payload())
        cancel_order(self.db,order); self.db.commit(); cancel_order(self.db,order); self.db.commit()
        self.assertEqual(self.db.get(Product,1).stock,10)
        paid=self.place(self.payload()); paid.payment_status='Paid'; self.db.commit()
        with self.assertRaises(HTTPException): cancel_order(self.db,paid)
        self.assertEqual(paid.status,'Confirmed')
    def test_expiry_releases_inventory_and_promo_capacity_once(self):
        order=self.place(self.payload(payment_method='khqr',discount_code='LUMEA20',expected_total=40))
        order.expires_at=utcnow()-timedelta(seconds=1); self.db.commit()
        self.assertEqual(self.db.query(Promotion).filter_by(code='LUMEA20').one().used,1)
        expire_pending_orders(self.db); self.db.commit(); expire_pending_orders(self.db); self.db.commit()
        self.assertEqual(order.status,'Expired')
        self.assertEqual(self.db.get(Product,1).stock,10)
        self.assertEqual(self.db.query(Promotion).filter_by(code='LUMEA20').one().used,0)
    def test_late_payment_requires_review_and_duplicate_event_does_not_rewind(self):
        order=self.place(self.payload(payment_method='khqr'))
        order.expires_at=utcnow()-timedelta(seconds=1); self.db.commit()
        settle_payment(self.db,order,'bank-ref'); self.db.commit()
        self.assertEqual(order.status,'Payment Review')
        self.assertEqual(self.db.get(Product,1).stock,10)
        second=self.place(self.payload(payment_method='khqr'))
        settle_payment(self.db,second,'bank-ref-2'); self.db.commit()
        transition_order(self.db,second,'Processing'); transition_order(self.db,second,'Shipped'); self.db.commit()
        settle_payment(self.db,second,'duplicate'); self.db.commit()
        self.assertEqual(second.status,'Shipped')
        self.assertEqual(second.transaction_ref,'bank-ref-2')
    def test_unverifiable_qr_is_not_offered_as_an_automatic_payment(self):
        order=self.place(self.payload(payment_method='khqr'))
        async def fallback(**kwargs): return {'source':'instant_emvco','qr_string':'unverified'}
        old = settings.ENABLE_DEMO_PAYMENTS
        settings.ENABLE_DEMO_PAYMENTS = False
        try:
            with patch('app.api.payments.get_bakong_khqr_data',new=fallback):
                with self.assertRaises(HTTPException) as error:
                    generate_khqr(KHQRGenerateRequest(order_number=order.order_number,amount=50),self.db,self.user,None).send(None)
                self.assertEqual(error.exception.status_code,503)
        finally:
            settings.ENABLE_DEMO_PAYMENTS = old
    def test_qr_generation_cannot_reset_a_payment_received_during_extraction(self):
        order=self.place(self.payload(payment_method='khqr'))
        async def settled(**kwargs):
            settle_payment(self.db,order,'bank-during-generation'); self.db.commit()
            return {'source':'live_aba_payway','qr_string':'verified'}
        with patch('app.api.payments.get_bakong_khqr_data',new=settled):
            with self.assertRaises(HTTPException):
                generate_khqr(KHQRGenerateRequest(order_number=order.order_number,amount=50),self.db,self.user,None).send(None)
        self.assertEqual(order.payment_status,'Paid')
        self.assertEqual(order.status,'Confirmed')
    def test_late_payment_poll_does_not_report_checkout_success(self):
        order=self.place(self.payload(payment_method='khqr'))
        order.expires_at=utcnow()-timedelta(seconds=1); self.db.commit()
        settle_payment(self.db,order,'late-bank-ref'); self.db.commit()
        try:
            check_khqr_payment(KHQRCheckRequest(order_number=order.order_number),self.db,self.user,None).send(None)
        except StopIteration as result:
            self.assertFalse(result.value['paid'])
            self.assertEqual(result.value['action'],'review')
    def test_fulfillment_cannot_skip_stages_and_cod_collection_is_recorded(self):
        order=self.place(self.payload())
        with self.assertRaises(HTTPException): transition_order(self.db,order,'Delivered')
        for stage in ('Processing','Shipped','Out for Delivery','Delivered'): transition_order(self.db,order,stage)
        self.db.commit()
        self.assertEqual(order.payment_status,'Paid'); self.assertIsNotNone(order.delivered_at)
    def test_promotion_edit_changes_validation_and_quote(self):
        promo=self.db.query(Promotion).filter_by(code='LUMEA20').one()
        update_promotion(promo.id,PromotionPayload(name='New value',code='LUMEA20',percent=30,max_uses=10),self.db)
        self.assertEqual(validate_promotion('lumea20',self.db)['rate'],0.3)
        order=self.place(self.payload(discount_code='LUMEA20',expected_total=35))
        self.assertEqual(order.total,35)
        update_promotion(promo.id,PromotionPayload(name='Paused',code='LUMEA20',percent=30,max_uses=10,status='Paused'),self.db)
        with self.assertRaises(HTTPException): validate_promotion('LUMEA20',self.db)
    def test_draft_private_and_publication_survives_new_session(self):
        article=create_article(ArticleCreate(slug='audit-article',title='Draft',category='Tips',hero_image='/test.jpg',status='Draft',content='Saved body'),self.db)
        with self.assertRaises(HTTPException): get_article_by_slug(article.slug,self.db,None)
        self.user.role='admin'
        self.assertEqual(get_article_by_slug(article.slug,self.db,self.user).data.content,'Saved body')
        update_article(article.slug,ArticleUpdate(status='Published',content='Published body'),self.db)
        self.db.expire_all()
        self.assertEqual(get_article_by_slug(article.slug,self.db,None).data.content,'Published body')
    def test_review_verification_moderation_and_helpful_dedup(self):
        review=submit_review(ReviewSubmission(product_id=1,rating=5,title='Good',comment='Test review comment'),self.db,self.user)['data']
        self.assertFalse(review.verified_purchase); self.assertEqual(review.status,'pending')
        self.delivered()
        purchased=submit_review(ReviewSubmission(product_id=1,rating=4,title='Good',comment='Another review comment'),self.db,self.user)['data']
        self.assertTrue(purchased.verified_purchase)
        purchased.status='approved'; self.db.commit()
        self.assertEqual(vote_helpful(purchased.id,self.db,self.user)['helpful_count'],1)
        self.assertEqual(vote_helpful(purchased.id,self.db,self.user)['helpful_count'],1)
    def test_return_transition_timeline_and_manual_refund_reference(self):
        order=self.delivered()
        request=returns.submit_return_request(self.return_payload(order),self.db,self.user)
        with self.assertRaises(HTTPException): update_return_status(request.request_number,ReturnRequestUpdateStatus(status='refunded'),self.db)
        for stage in ('Approved','Return in Transit','Item Received','Refund Processing'):
            request=update_return_status(request.request_number,ReturnRequestUpdateStatus(status=stage),self.db)
        request=update_return_status(request.request_number,ReturnRequestUpdateStatus(status='Refund Completed',refund_reference='manual-refund-123'),self.db)
        self.assertEqual(request.current_step,7)
        self.assertEqual(request.timeline[-1]['title'],'Refund Completed')
        self.assertEqual(request.refund_reference,'manual-refund-123')
    def test_contact_form_creates_durable_reference(self):
        result=create_inquiry(ContactPayload(firstName='Test',lastName='User',email='test@example.com',subject='Order help',message='Need assistance with delivery',consent=True),self.db)
        self.db.expire_all()
        self.assertEqual(self.db.query(SupportMessage).filter_by(reference=result['reference']).one().subject,'Order help')

class SchemaMigrations(unittest.TestCase):
    def test_additive_schema_migration_is_repeatable(self):
        engine=create_engine('sqlite://')
        with engine.begin() as conn: conn.execute(text('CREATE TABLE orders (id INTEGER PRIMARY KEY, order_number VARCHAR(50))'))
        migrate_schema(engine); migrate_schema(engine)
        self.assertIn('checkout_key',{c['name'] for c in inspect(engine).get_columns('orders')})
        engine.dispose()
    def test_concurrent_checkouts_cannot_both_buy_the_last_unit(self):
        with tempfile.TemporaryDirectory(prefix='lumea-flow-') as directory:
            engine=create_engine('sqlite:///'+str(Path(directory)/'race.db'),connect_args={'check_same_thread':False,'timeout':10})
            Base.metadata.create_all(engine)
            with Session(engine) as db:
                from app.models import Category
                db.add(Category(id=1,name='Test',slug='test'))
                db.add(Product(id=1,category_id=1,name='Last item',brand='Test',slug='last',category='test',category_name='Test',price=50,stock=1,image_url='/test.jpg'))
                db.commit()
            from app.api import orders as orders_api
            original_quote=orders_api.calculate_quote
            barrier=threading.Barrier(2)
            def simultaneous_quote(payload, db):
                result=original_quote(payload, db)
                barrier.wait(timeout=5)
                return result
            def buy():
                from app.schemas.order import OrderCreate
                with Session(engine) as db:
                    payload=OrderCreate(customer_name='Test',customer_email='test@example.com',shipping_address='Test',shipping_city='Test',payment_method='cod',expected_total=50,items=[{'product_id':1,'quantity':1}])
                    try:
                        place_order(payload,db,None)
                        return 'created'
                    except HTTPException as error:
                        return error.status_code
            with patch.object(orders_api,'calculate_quote',side_effect=simultaneous_quote):
                with ThreadPoolExecutor(max_workers=2) as pool: outcomes=list(pool.map(lambda _:buy(),range(2)))
            self.assertCountEqual(outcomes,['created',409])
            with Session(engine) as db:
                self.assertEqual(db.get(Product,1).stock,0)
                self.assertEqual(db.query(Order).count(),1)
            engine.dispose()
    def test_initial_promotion_seed_does_not_reactivate_paused_codes(self):
        engine=create_engine('sqlite://'); Base.metadata.create_all(engine); migrate_schema(engine)
        with engine.begin() as conn: conn.execute(text("UPDATE promotions SET status='Paused' WHERE code='LUMEA20'"))
        migrate_schema(engine)
        with engine.connect() as conn: self.assertEqual(conn.execute(text("SELECT status FROM promotions WHERE code='LUMEA20'")).scalar(),'Paused')
        engine.dispose()

if __name__=='__main__': unittest.main(verbosity=2)
