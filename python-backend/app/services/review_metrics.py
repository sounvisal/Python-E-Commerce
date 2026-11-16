from sqlalchemy import func
from app.models.review import Review
from app.models.product import Product

def refresh_rating(db, product_id):
    db.flush()
    product = db.get(Product, product_id)
    if product:
        count, average = db.query(func.count(Review.id), func.avg(Review.rating)).filter(Review.product_id == product_id, Review.status == 'approved').one()
        product.reviews = count
        product.rating = round(float(average or 0), 1)
