from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order
from app.models.promotion import Promotion
from app.models.banner import Banner
from app.models.article import Article

router = APIRouter(prefix="/notifications", tags=["Notifications"])

def format_relative_time(dt: datetime) -> str:
    if not dt:
        return "Recent"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = datetime.now(timezone.utc) - dt
    total_seconds = max(0, int(diff.total_seconds()))
    if total_seconds < 60:
        return "Just now"
    minutes = total_seconds // 60
    if minutes < 60:
        return f"{minutes} min{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days == 1:
        return "Yesterday"
    return f"{days} days ago"

def privacy_name(full_name: str) -> str:
    if not full_name:
        return "Clientele"
    parts = full_name.strip().split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1][0]}."
    return parts[0]

@router.get("")
def get_notifications(db: Session = Depends(get_db)):
    """
    Fetches real live notifications from admin data:
    1. Active promotional events & discounts created by the admin.
    2. Active promotional banners and featured announcements.
    3. Real live customer orders placed in the atelier.
    4. Latest dermatological masterclasses and published articles.
    """
    notifications = []

    # 1. Real Active Promotions from Admin
    active_promos = (
        db.query(Promotion)
        .filter(Promotion.status == "Active")
        .order_by(Promotion.is_featured.desc(), Promotion.id.desc())
        .limit(3)
        .all()
    )
    for promo in active_promos:
        notifications.append({
            "id": f"notif-promo-{promo.id}",
            "type": "event",
            "tag": "Official Event" if promo.is_featured else "Atelier Privilege",
            "badgeColor": "terracotta" if promo.is_featured else "gold",
            "title": promo.name,
            "message": f"Special {int(promo.percent)}% off entire order with code {promo.code}. Apply code at checkout.",
            "time": "Active Now",
            "link": "/deals",
            "linkText": "Explore Event Deals"
        })

    # 2. Real Active Banners / Announcements from Admin
    active_banners = (
        db.query(Banner)
        .filter(Banner.is_active == True)
        .order_by(Banner.display_order.asc())
        .limit(2)
        .all()
    )
    for b in active_banners:
        notifications.append({
            "id": f"notif-banner-{b.id}",
            "type": "event",
            "tag": b.badge_text or "Atelier Spotlight",
            "badgeColor": "terracotta",
            "title": b.title,
            "message": b.subtitle or f"Discover our newest curated formulation releases.",
            "time": "Featured",
            "link": b.cta_link or "/shop",
            "linkText": b.cta_text or "Explore Formulation",
            "productImage": b.image_url
        })

    # 3. Real Recent Customer Orders from Database
    recent_orders = (
        db.query(Order)
        .filter(Order.status != "Cancelled")
        .order_by(Order.created_at.desc())
        .limit(10)
        .all()
    )
    for order in recent_orders:
        if not order.items:
            continue
        first_item = order.items[0]
        p_name = first_item.product_name or "Curated Botanical Formulation"
        p_img = first_item.image_url or "/images/prod-essence.jpg"
        p_slug = ""
        if first_item.product_id:
            from app.models.product import Product
            prod = db.get(Product, first_item.product_id)
            if prod:
                p_slug = prod.slug or ""
                p_img = prod.image_url or p_img

        client_name = privacy_name(order.customer_name)
        city = order.shipping_city or "Cambodia"
        item_count = len(order.items)
        extra_text = f" and {item_count - 1} other item{'s' if item_count > 2 else ''}" if item_count > 1 else ""

        notifications.append({
            "id": f"notif-order-{order.id}",
            "type": "purchase",
            "tag": "Just Purchased",
            "badgeColor": "emerald",
            "title": f"Recent Purchase · {city}",
            "message": f"{client_name} just ordered {p_name}{extra_text}.",
            "time": format_relative_time(order.created_at),
            "link": f"/product/{p_slug}" if p_slug else "/shop",
            "linkText": "View Formulation",
            "productImage": p_img
        })

    # 4. Real Published Masterclasses / Articles
    recent_articles = (
        db.query(Article)
        .filter(Article.status == "Published")
        .order_by(Article.created_at.desc())
        .limit(2)
        .all()
    )
    for art in recent_articles:
        notifications.append({
            "id": f"notif-article-{art.id}",
            "type": "event",
            "tag": art.category or "Atelier Journal",
            "badgeColor": "gold",
            "title": art.title,
            "message": art.subtitle or art.excerpt or "Read the clinical ingredient breakdown and routine recommendations.",
            "time": art.published_at or "Published",
            "link": f"/articles/{art.slug}",
            "linkText": "Read Masterclass",
            "productImage": art.thumbnail or art.hero_image
        })

    return {
        "status": "success",
        "data": notifications,
        "total": len(notifications)
    }
