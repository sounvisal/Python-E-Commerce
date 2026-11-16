"""Review probes using disposable in-memory SQLite; never touches lumea.db."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'python-backend'))
import asyncio
import inspect
from types import SimpleNamespace
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.models import *
from app.models.product import Product
from app.models.category import Category
from app.api import orders, returns, admin, reviews, payments

engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.create_all(engine)
db = Session(engine)
db.add(Category(id=1, name='Test', slug='test'))
db.add(Product(id=1, category_id=1, name='Audit Product', brand='Audit', slug='audit', category='test', category_name='Test', price=50, stock=0, image_url='/test.jpg'))
db.commit()
class DirectClient:
    """Calls route handlers and validates declared responses without HTTP threads."""
    def call(self, method, path, data=None):
        for router in (orders.router, returns.router, admin.router, reviews.router, payments.router):
            for route in router.routes:
                match, scope = route.matches({'type':'http', 'path':path.removeprefix('/api'), 'method':method})
                if match.name != 'FULL':
                    continue
                kwargs = dict(scope.get('path_params', {}))
                for name, param in inspect.signature(route.endpoint).parameters.items():
                    if name == 'db': kwargs[name] = db
                    elif name in kwargs:
                        if param.annotation is int: kwargs[name] = int(kwargs[name])
                    elif inspect.isclass(param.annotation) and hasattr(param.annotation, 'model_validate'):
                        kwargs[name] = param.annotation.model_validate(data)
                result = route.endpoint(**kwargs)
                if inspect.isawaitable(result): result = asyncio.run(result)
                if route.response_model:
                    from pydantic import TypeAdapter
                    adapter = TypeAdapter(route.response_model)
                    result = adapter.dump_python(adapter.validate_python(result), mode='json')
                else:
                    from fastapi.encoders import jsonable_encoder
                    result = jsonable_encoder(result)
                return SimpleNamespace(status_code=route.status_code or 200, json=lambda: result)
        raise RuntimeError(path)
    def get(self, path): return self.call('GET', path)
    def post(self, path, json): return self.call('POST', path, json)
    def patch(self, path, json): return self.call('PATCH', path, json)
client = DirectClient()
results = []
def record(name, response, evidence):
    results.append({'finding': name, 'declared_http_status': response.status_code, 'method':'direct route handler with in-memory DB; authentication absence separately inspected', 'evidence': evidence})

payload = dict(customer_name='Audit', customer_email='audit@example.test', shipping_address='Test', shipping_city='Test', payment_method='cod', items=[{'product_id': 1, 'quantity': 3}])
r = client.post('/api/orders', json=payload)
o = r.json()['data']
record('Zero-stock product accepted and COD marked Paid', r, {'status': o['status'], 'payment_status': o['payment_status'], 'quantity': o['items'][0]['quantity'], 'stock_after': db.get(Product, 1).stock})
r = client.get('/api/orders')
record('Order list readable without authentication', r, {'count': len(r.json())})
r = client.patch('/api/orders/' + o['order_number'] + '/status', json={'status':'Delivered'})
record('Anonymous caller can jump order directly to Delivered', r, {'status': r.json()['data']['status']})
r = client.get('/api/admin/customers')
record('Admin customer endpoint readable without authentication', r, {'response_status': r.json().get('status')})
payload['items'] = [{'product_id':1, 'quantity':1, 'price':0.01}]
r = client.post('/api/orders', json=payload)
record('Caller overrides authoritative product price', r, {'catalog_price':50, 'charged_subtotal':r.json()['data']['subtotal']})
payload['items'] = [{'product_id':1, 'quantity':1}]
payload['discount_code'] = 'NOTREAL20'
r = client.post('/api/orders', json=payload)
record('Invented coupon accepted; shipping threshold changes after discount', r, {'subtotal':r.json()['data']['subtotal'], 'discount':r.json()['data']['discount'], 'shipping':r.json()['data']['shipping_fee'], 'total':r.json()['data']['total'], 'frontend_total_for_same_cart':40})
r = client.post('/api/returns', json={'order_number':'DOES-NOT-EXIST', 'product_name':'Never purchased', 'reason':'Changed mind', 'resolution':'Refund', 'price':999})
ret = r.json()
record('Return accepted for nonexistent order and caller-supplied price', r, {'request_number':ret['request_number'], 'price':ret['price'], 'status':ret['status'], 'contains_success_key':'success' in ret})
r = client.patch('/api/returns/' + ret['request_number'] + '/status', json={'status':'Refunded'})
record('Return status changes without timeline progression or success key', r, {'status':r.json()['status'], 'current_step':r.json()['current_step'], 'contains_success_key':'success' in r.json()})
r = client.post('/api/reviews', json={'product_id':1,'rating':5,'title':'Test review','comment':'Disposable audit review'})
record('Unpurchased anonymous review approved and verified automatically', r, {'status':r.json()['data']['status'], 'verified_purchase':r.json()['data']['verified_purchase']})
r = client.post('/api/payments/khqr/simulate-approve', json={'order_number':o['order_number']})
record('Public simulation marks payment Paid and revives Delivered order as Confirmed', r, {'paid':r.json()['paid'], 'status_after':client.get('/api/orders/' + o['order_number']).json()['data']['status']})
output = Path(__file__).with_name('FLOW_AUDIT_PROBE_RESULTS.json')
output.write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
db.close()
engine.dispose()
