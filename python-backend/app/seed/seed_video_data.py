import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal
from app.models.product import Product
from app.models.review import Review
from app.models.brand import Brand

def seed_video_features():
    db = SessionLocal()
    try:
        print("Seeding video demonstration URLs and customer video reviews...")

        # 1. Update Brands with Masterclass Story Films
        sk2_brand = db.query(Brand).filter(Brand.slug == "sk-ii").first()
        if sk2_brand:
            sk2_brand.story_video_url = "/videos/brand-story-sk2.mp4"
            sk2_brand.story_video_title = "The Legend of Pitera™: Japanese Fermentation Craft"
            print("  [OK] Updated SK-II Brand with Story Video")

        boj_brand = db.query(Brand).filter(Brand.slug == "beauty-of-joseon").first()
        if boj_brand:
            boj_brand.story_video_url = "/videos/brand-story-boj.mp4"
            boj_brand.story_video_title = "Hanbang Heritage: Modern Wisdom from Dynasty Herbalism"
            print("  [OK] Updated Beauty of Joseon Brand with Story Video")

        # 2. Update Products with Texture Demo Videos
        prods_video_map = [
            {
                "keyword": "facial treatment essence",
                "video_url": "/videos/reel-sk2-texture.mp4",
                "video_title": "PITERA™ Fermentation Water Texture & Absorption Swatch",
                "video_thumbnail": "/images/pdp-stage-sk2-hero.jpg"
            },
            {
                "keyword": "relief sun",
                "video_url": "/videos/reel-boj-sunscreen.mp4",
                "video_title": "Rice + Probiotics Melting Texture with Zero Whitecast",
                "video_thumbnail": "/images/article-thumb-sunscreen.jpg"
            },
            {
                "keyword": "snail",
                "video_url": "/videos/reel-snail-mucin.mp4",
                "video_title": "96% Pure Snail Secretion Filtrate Viscosity Demonstration",
                "video_thumbnail": "/images/prod-cosrx.jpg"
            },
            {
                "keyword": "niacinamide",
                "video_url": "/videos/reel-niacinamide-glow.mp4",
                "video_title": "Lightweight Active Water-Gel Droplet Swatch",
                "video_thumbnail": "/images/article-thumb-niacinamide.jpg"
            },
            {
                "keyword": "centella",
                "video_url": "/videos/reel-centella-ampoule.mp4",
                "video_title": "Madagascar Centella Rapid Soothing & Calming Swatch",
                "video_thumbnail": "/images/article-thumb-centella.jpg"
            },
            {
                "keyword": "sleeping",
                "video_url": "/videos/reel-restorative-sleep.mp4",
                "video_title": "Whipped Barrier Recovery Overnight Moisture Cream",
                "video_thumbnail": "/images/article-thumb-sleep.jpg"
            }
        ]

        for item in prods_video_map:
            p = db.query(Product).filter(Product.name.ilike(f"%{item['keyword']}%")).first()
            if p:
                p.video_url = item["video_url"]
                p.video_title = item["video_title"]
                p.video_thumbnail = item["video_thumbnail"]
                print(f"  [OK] Attached texture video to product: '{p.name}'")

        # 3. Seed High-End Video Customer Reviews
        # Let's find SK-II and BOJ and COSRX products
        sk2_prod = db.query(Product).filter(Product.name.ilike("%facial treatment essence%")).first()
        boj_prod = db.query(Product).filter(Product.name.ilike("%relief sun%")).first()
        cosrx_prod = db.query(Product).filter(Product.name.ilike("%snail%")).first()

        video_reviews = [
            # For SK-II
            {
                "product": sk2_prod,
                "title": "My Holy Grail for 5 Years — Pure Glass Skin In A Bottle",
                "comment": "Watch how quickly this absorbs! It feels just like silky water, but within 60 seconds your face has this dewy, poreless clarity that no moisturizer can replicate. Worth every single penny.",
                "rating": 5,
                "customer_name": "Sreynich Chan",
                "customer_email": "sreynich.chan@example.com",
                "customer_avatar": "/images/avatar-sreynich.jpg",
                "video_url": "/videos/reel-sk2-texture.mp4",
                "video_thumbnail": "/images/pdp-stage-sk2-hero.jpg",
                "video_duration": "0:24",
                "skin_type": "Combination",
                "helpful_count": 48
            },
            {
                "product": sk2_prod,
                "title": "Calmed my stubborn post-travel redness completely",
                "comment": "Notice how translucent the formula is. I do the 3-skin patting method morning and night. The fermentation bio-actives truly reset my skin barrier after a flight.",
                "rating": 5,
                "customer_name": "Dr. Channary Meas",
                "customer_email": "channary.meas@atelier.com",
                "customer_avatar": "/images/customer-1.jpg",
                "video_url": "/videos/reel-centella-ampoule.mp4",
                "video_thumbnail": "/images/article-thumb-centella.jpg",
                "video_duration": "0:30",
                "skin_type": "Sensitive / Reactive",
                "helpful_count": 35
            },
            {
                "product": sk2_prod,
                "title": "Visible glow under makeup with zero pilling",
                "comment": "Here is how it layers under active serums and cushion compact. It leaves zero residue, just bouncy resilience. Evaluators and skincare lovers will adore this texture.",
                "rating": 5,
                "customer_name": "Elena Rostova",
                "customer_email": "elena.rostova@example.com",
                "customer_avatar": "/images/customer-2.jpg",
                "video_url": "/videos/reel-niacinamide-glow.mp4",
                "video_thumbnail": "/images/article-thumb-niacinamide.jpg",
                "video_duration": "0:19",
                "skin_type": "Dry",
                "helpful_count": 27
            },
            # For Beauty of Joseon Relief Sun
            {
                "product": boj_prod,
                "title": "The only sunscreen that doesn't leave a ghost cast on olive skin",
                "comment": "Watch the blend test on camera — it literally dissolves like a lightweight gel lotion! No greasy sheen, no eye stinging, and full Korean SPF50+ PA++++ broad spectrum protection.",
                "rating": 5,
                "customer_name": "Devi Sok",
                "customer_email": "devi.sok@example.com",
                "customer_avatar": "/images/customer-3.jpg",
                "video_url": "/videos/reel-boj-sunscreen.mp4",
                "video_thumbnail": "/images/article-thumb-sunscreen.jpg",
                "video_duration": "0:22",
                "skin_type": "Oily / Normal",
                "helpful_count": 52
            },
            {
                "product": boj_prod,
                "title": "Velvety skin prep before daily makeup",
                "comment": "The fermented grain extracts give such a supple priming effect. I never need a separate morning moisturizer when using this.",
                "rating": 5,
                "customer_name": "Sophea Kim",
                "customer_email": "sophea.kim@example.com",
                "customer_avatar": "/images/customer-4.jpg",
                "video_url": "/videos/reel-restorative-sleep.mp4",
                "video_thumbnail": "/images/article-thumb-sleep.jpg",
                "video_duration": "0:26",
                "skin_type": "Dry",
                "helpful_count": 19
            },
            # For COSRX Snail Mucin
            {
                "product": cosrx_prod,
                "title": "The stretch test speaks for itself! Instant repair",
                "comment": "See that iconic elasticity in the clip? It delivers an insane moisture surge and heals active acne breakouts overnight without clogging pores.",
                "rating": 5,
                "customer_name": "Bopha Lin",
                "customer_email": "bopha.lin@example.com",
                "customer_avatar": "/images/customer-5.jpg",
                "video_url": "/videos/reel-snail-mucin.mp4",
                "video_thumbnail": "/images/prod-cosrx.jpg",
                "video_duration": "0:25",
                "skin_type": "Dehydrated Acne-Prone",
                "helpful_count": 64
            }
        ]

        for r_data in video_reviews:
            prod = r_data["product"]
            if not prod:
                # fallback to first product
                prod = db.query(Product).first()

            # Check if this exact video review already exists
            existing = db.query(Review).filter(
                Review.product_id == prod.id,
                Review.title == r_data["title"]
            ).first()

            if not existing:
                new_r = Review(
                    product_id=prod.id,
                    product_name=prod.name,
                    product_image=prod.image_url,
                    customer_name=r_data["customer_name"],
                    customer_email=r_data["customer_email"],
                    customer_avatar=r_data["customer_avatar"],
                    verified_purchase=True,
                    rating=r_data["rating"],
                    title=r_data["title"],
                    comment=r_data["comment"],
                    video_url=r_data["video_url"],
                    video_thumbnail=r_data["video_thumbnail"],
                    video_duration=r_data["video_duration"],
                    skin_type=r_data["skin_type"],
                    helpful_count=r_data["helpful_count"],
                    status="approved"
                )
                db.add(new_r)
                print(f"  [OK] Added video review: '{r_data['title']}' for {prod.name}")
            else:
                existing.video_url = r_data["video_url"]
                existing.video_thumbnail = r_data["video_thumbnail"]
                existing.video_duration = r_data["video_duration"]
                existing.skin_type = r_data["skin_type"]
                print(f"  [OK] Updated video review: '{r_data['title']}' for {prod.name}")

        db.commit()
        print("\nAll video reviews and texture showcase data successfully seeded in lumea.db!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding video data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_video_features()
