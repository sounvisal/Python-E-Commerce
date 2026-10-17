import json
import os
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.banner import Banner
from app.models.page import Page
from app.models.article import Article
from app.models.brand import Brand
from app.models.review import Review
from app.models.quiz import Quiz
from app.models.return_request import ReturnRequest
from app.core.security import get_password_hash

SEED_FILE = os.path.join(os.path.dirname(__file__), "seed_data.json")

def seed_database(db: Session):
    """
    Populates SQLite database with Luméa's categories, products,
    demo user, sample order, and dynamic page banners if empty.
    """
    # 1. Seed Categories
    if db.query(Category).count() == 0:
        if os.path.exists(SEED_FILE):
            with open(SEED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                categories = data.get("categories", [])
                for cat_data in categories:
                    category = Category(
                        id=cat_data["id"],
                        name=cat_data["name"],
                        slug=cat_data["slug"],
                        description=cat_data.get("desc"),
                        icon=cat_data.get("icon", "Sparkles"),
                        image_url=f"/images/cat-{cat_data['slug']}.jpg"
                    )
                    db.add(category)
                db.commit()
                print(f"[Seed] Added {len(categories)} categories.")

    # 2. Seed Products
    if db.query(Product).count() == 0:
        if os.path.exists(SEED_FILE):
            with open(SEED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                products = data.get("products", [])
                
                # Build category slug -> id mapping
                cat_map = {c.slug: c.id for c in db.query(Category).all()}

                for p in products:
                    cat_slug = p.get("category", "serums")
                    cat_id = cat_map.get(cat_slug, 1)

                    prod = Product(
                        id=p["id"],
                        category_id=cat_id,
                        name=p["name"],
                        brand=p["brand"],
                        slug=p["slug"],
                        category=cat_slug,
                        category_name=p.get("category_name", cat_slug.capitalize()),
                        subcategory=p.get("subcategory"),
                        product_type=p.get("product_type", "Skincare"),
                        price=float(p["price"]),
                        compare_at_price=float(p["compare_at_price"]) if p.get("compare_at_price") else None,
                        rating=float(p.get("rating", 4.8)),
                        reviews=int(p.get("reviews", 100)),
                        badge=p.get("badge"),
                        badge_type=p.get("badge_type"),
                        stock=int(p.get("stock", 50)),
                        image_url=p.get("image_url", "/images/prod-sk2.jpg"),
                        description=f"Authentic {p['brand']} {p['name']} formulated with dermatological precision for optimal skin vitality.",
                        is_featured=bool(p.get("is_featured", True)),
                        skin_type=p.get("skin_type", ["All Skin Types"]),
                        skin_concern=p.get("skin_concern", ["Hydration"]),
                        gallery=[p.get("image_url", "/images/prod-sk2.jpg")]
                    )
                    db.add(prod)
                db.commit()
                print(f"[Seed] Added {len(products)} products.")

    # 3. Seed Default User (Sreynich Chan)
    if db.query(User).count() == 0:
        demo_user = User(
            id=1,
            name="Sreynich Chan",
            first_name="Sreynich",
            last_name="Chan",
            email="sreynich.chan@example.com",
            hashed_password=get_password_hash("password123"),
            phone="+855 12 345 678",
            avatar="/images/avatar-sreynich.jpg",
            role="customer",
            tier="Luméa Radiant Gold",
            reward_points=320
        )
        db.add(demo_user)
        db.commit()
        print("[Seed] Created default user: sreynich.chan@example.com (password: password123)")

    # 4. Seed Sample Order
    if db.query(Order).count() == 0:
        sample_order = Order(
            id=1,
            order_number="LUM-849201",
            user_id=1,
            customer_name="Sreynich Chan",
            customer_email="sreynich.chan@example.com",
            customer_phone="+855 12 345 678",
            shipping_address="#123, Street 271, Sangkat Boeung Tumpun",
            shipping_city="Phnom Penh",
            shipping_postal_code="12000",
            subtotal=107.90,
            discount=10.79,
            shipping_fee=0.0,
            total=97.11,
            status="Confirmed",
            payment_method="card"
        )
        db.add(sample_order)
        db.commit()

        sample_item1 = OrderItem(
            order_id=sample_order.id,
            product_id=201,
            product_name="Facial Treatment Essence",
            image_url="/images/prod-sk2.jpg",
            price=99.00,
            quantity=1,
            total=99.00
        )
        sample_item2 = OrderItem(
            order_id=sample_order.id,
            product_id=202,
            product_name="Niacinamide 10% + Zinc 1%",
            image_url="/images/prod-ordinary.jpg",
            price=8.90,
            quantity=1,
            total=8.90
        )
        db.add(sample_item1)
        db.add(sample_item2)
        db.commit()
        print("[Seed] Created sample order: LUM-849201")

    # 5. Seed Dynamic Banners
    if db.query(Banner).count() == 0:
        initial_banners = [
            Banner(
                page="home",
                title="Where Beauty Lives",
                subtitle="Gentle, clinically-proven formulas crafted to nurture your skin barrier and enhance your natural glow.",
                script_text="Good Skin Today. Brighter Tomorrows.",
                badge_text="Clean & Proven",
                image_url="/images/banner-home.jpg",
                cta_text="Explore Atelier",
                cta_link="/shop",
                display_order=1
            ),
            Banner(
                page="shop",
                title="All Skincare Products",
                subtitle="Explore our complete curated selection of authentic skincare solutions from premier laboratories.",
                script_text="Curated with Care",
                badge_text="100% Authentic",
                image_url="/images/banner-all-products.jpg",
                cta_text="Discover Bestsellers",
                cta_link="/best-sellers",
                display_order=2
            ),
            Banner(
                page="best-sellers",
                title="Best Sellers",
                subtitle="Our most-loved skincare essentials, trusted and adored by thousands of beauty lovers worldwide.",
                script_text="Beloved Favorites",
                badge_text="Customer Favorites",
                image_url="/images/banner-best-sellers.jpg",
                cta_text="Shop Top Picks",
                cta_link="/shop",
                display_order=3
            ),
            Banner(
                page="new-arrivals",
                title="New Arrivals",
                subtitle="The latest innovations in Asian beauty, barrier repair, and dermatological breakthroughs.",
                script_text="Fresh Formulations",
                badge_text="Just Landed",
                image_url="/images/banner-new-arrivals.jpg",
                cta_text="Shop New",
                cta_link="/shop",
                display_order=4
            ),
            Banner(
                page="deals",
                title="Special Deals & Bundles",
                subtitle="Exclusive savings on premium skincare kits, discovery sets, and dermatologist favorites.",
                script_text="Exclusive Atelier Offer",
                badge_text="Limited Time",
                image_url="/images/banner-deals.jpg",
                cta_text="View All Deals",
                cta_link="/deals/all",
                display_order=5
            ),
            Banner(
                page="concerns",
                title="Targeted Skin Concerns",
                subtitle="Personalized skincare solutions tailored to acne, dark spots, sensitivity, and aging.",
                script_text="Tailored For You",
                badge_text="Targeted Formulations",
                image_url="/images/banner-concerns.jpg",
                cta_text="Take Skin Quiz",
                cta_link="/quiz",
                display_order=6
            ),
            Banner(
                page="about",
                title="Our Story & Philosophy",
                subtitle="Founded on authenticity, transparency, and a kinder, holistic approach to skincare wellness.",
                script_text="A Healthier You",
                badge_text="The Luméa Promise",
                image_url="/images/banners/banner-about-clean.jpg",
                cta_text="Why Shop With Us",
                cta_link="/authenticity",
                display_order=7
            ),
            Banner(
                page="account",
                title="Welcome to Your Atelier Space",
                subtitle="Track your orders, manage your skincare journal, and view your loyalty rewards.",
                script_text="Small Steps. Real Changes.",
                badge_text="Loyalty Atelier",
                image_url="/images/banner-my-orders.jpg",
                cta_text="View Orders",
                cta_link="/account/orders",
                display_order=8
            )
        ]
        db.add_all(initial_banners)
        db.commit()
        print(f"[Seed] Created {len(initial_banners)} dynamic page banners in database.")

    # 6. Seed CMS & Legal Pages
    if db.query(Page).count() == 0:
        initial_pages = [
            Page(
                slug="privacy-policy",
                title="Privacy Policy",
                subtitle="We respect your privacy and are committed to protecting your personal information.",
                badge_text="LEGAL & PRIVACY",
                script_text="Your Privacy Our Priority",
                hero_image="/images/privacy-header-bottles.jpg",
                last_updated="August 15, 2025",
                content_json={
                    "sections": [
                        {
                            "id": "01",
                            "slug": "introduction",
                            "title": "Introduction",
                            "content": "Luméa (\"we\", \"us\", or \"our\") respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, share, and safeguard your information when you visit our website, create an account, place an order, or use any of our services.\n\nBy using our website and services, you agree to the practices described in this Privacy Policy. If you do not agree, please do not use our website."
                        },
                        {
                            "id": "02",
                            "slug": "information-we-collect",
                            "title": "Information We Collect",
                            "content": "We may collect different types of information depending on how you use our website and services.",
                            "cards": [
                                {
                                    "icon": "User",
                                    "title": "Account Information",
                                    "description": "Name, email address, phone number, and password when you create an account."
                                },
                                {
                                    "icon": "ShoppingCart",
                                    "title": "Order Information",
                                    "description": "Shipping address, billing address, order history, and payment information."
                                },
                                {
                                    "icon": "Leaf",
                                    "title": "Skin Profile Information",
                                    "description": "Skin type, skin concerns, and quiz results when you use our skin quiz feature."
                                },
                                {
                                    "icon": "Laptop",
                                    "title": "Device and Usage Information",
                                    "description": "IP address, device type, browser, pages visited, and other analytics data."
                                }
                            ]
                        },
                        {
                            "id": "03",
                            "slug": "how-we-use-your-information",
                            "title": "How We Use Your Information",
                            "content": "We use your information for the following purposes:",
                            "bullets": [
                                "To create and manage your account",
                                "To process and fulfill your orders",
                                "To provide customer support and respond to your inquiries",
                                "To personalize your shopping experience and product recommendations",
                                "To send transactional notifications, order confirmations, and shipment updates",
                                "To continuously refine our skincare formulas catalog and digital experience"
                            ]
                        },
                        {
                            "id": "04",
                            "slug": "legal-bases",
                            "title": "Legal Bases for Processing (For EU/EEA Users)",
                            "content": "We process personal information under defined legal bases: Contractual Necessity (order delivery and account access), Legitimate Interests (fraud detection, platform stability), Legal Obligation (accounting, taxation records), and Explicit Consent (custom diagnostic quiz and newsletter subscription)."
                        },
                        {
                            "id": "05",
                            "slug": "sharing-information",
                            "title": "How We Share Your Information",
                            "content": "We never sell, rent, or trade your personal information to third parties. We share data solely with verified infrastructure partners who assist in our daily operations (secure payment processors, licensed global couriers like DHL/Cambodia Post, and encrypted cloud hosts) under strict confidentiality agreements."
                        },
                        {
                            "id": "06",
                            "slug": "cookies",
                            "title": "Cookies and Similar Technologies",
                            "content": "We utilize essential cookies to retain cart contents, maintain authentication state, and store user preferences. Analytical cookies help us measure user journeys to improve site speed. You can manage or revoke cookie permissions via your browser controls."
                        },
                        {
                            "id": "07",
                            "slug": "data-security",
                            "title": "Data Security",
                            "content": "All network transactions are secured with TLS 1.3 encryption. Customer passwords and sensitive secrets are stored using cryptographic hashes (bcrypt). Our database backups are encrypted and stored in secure facilities."
                        },
                        {
                            "id": "08",
                            "slug": "your-rights",
                            "title": "Your Rights and Choices",
                            "content": "You retain full control over your personal data. You have the right to request a copy of your records, correct inaccurate details, request account deletion, or opt out of promotional messages at any time directly in your account dashboard."
                        },
                        {
                            "id": "09",
                            "slug": "data-retention",
                            "title": "Data Retention",
                            "content": "We retain your order histories and profile metrics as long as your account remains active or as required by law for taxation and financial audit periods."
                        },
                        {
                            "id": "10",
                            "slug": "children-privacy",
                            "title": "Children's Privacy",
                            "content": "Luméa does not target or knowingly collect data from children under 16 years of age. If we identify that a minor has provided data without guardian consent, we will promptly purge the records."
                        },
                        {
                            "id": "11",
                            "slug": "international-transfers",
                            "title": "International Data Transfers",
                            "content": "Where cross-border data transfer occurs for logistics and cloud hosting, we ensure that adequate protection standards and contractual clauses are maintained."
                        },
                        {
                            "id": "12",
                            "slug": "changes-to-policy",
                            "title": "Changes to This Privacy Policy",
                            "content": "We may update this policy periodically to align with evolving international data laws. Major revisions will be highlighted on our homepage."
                        },
                        {
                            "id": "13",
                            "slug": "contact-us",
                            "title": "Contact Us",
                            "content": "If you have questions regarding this Privacy Policy or wish to exercise your data rights, please contact our concierge team at privacy@lumea.com."
                        }
                    ],
                    "commitments": [
                        { "title": "Secure & Protected", "desc": "We use industry-standard security measures." },
                        { "title": "We Never Sell Your Data", "desc": "We do not sell your personal information to third parties." },
                        { "title": "Transparent Practices", "desc": "We are clear about how we use your information." },
                        { "title": "Your Choices Matter", "desc": "You can manage your preferences at any time." }
                    ],
                    "contact_box": {
                        "email": "privacy@lumea.com",
                        "desc": "If you have any questions about this Privacy Policy or how we handle your data, please contact our privacy team."
                    }
                }
            ),
            Page(
                slug="terms-of-service",
                title="Terms of Service",
                subtitle="These Terms of Service govern your use of the Luméa website and our products and services.",
                badge_text="TERMS OF SERVICE",
                script_text="Beauty Built on Trust",
                hero_image="/images/terms-header-bottles.jpg",
                last_updated="August 15, 2025",
                content_json={
                    "sections": [
                        {
                            "id": "01",
                            "slug": "introduction",
                            "title": "Introduction",
                            "content": "Welcome to Luméa. These Terms of Service (\"Terms\") govern your access to and use of our website, products, and services, including any purchases, content, and features available through our platform.\n\nBy creating an account, browsing our website, or placing an order, you agree to be bound by these Terms. If you do not agree with any part of these Terms, please do not use our website."
                        },
                        {
                            "id": "02",
                            "slug": "your-account",
                            "title": "Your Account",
                            "content": "You may be required to create an account to access certain features, such as placing orders, saving your wishlist, or using the Skin Quiz.",
                            "cards": [
                                {
                                    "icon": "User",
                                    "title": "Accurate Information",
                                    "description": "You agree to provide accurate, complete, and up-to-date information."
                                },
                                {
                                    "icon": "Lock",
                                    "title": "Account Security",
                                    "description": "You are responsible for keeping your login credentials secure."
                                },
                                {
                                    "icon": "Edit3",
                                    "title": "One Account Per User",
                                    "description": "Each user may only maintain one account. We reserve the right to suspend duplicate accounts."
                                },
                                {
                                    "icon": "Users",
                                    "title": "Notify Us of Changes",
                                    "description": "Please update your information if there are any changes (e.g. email address, phone number)."
                                }
                            ]
                        },
                        {
                            "id": "03",
                            "slug": "placing-orders",
                            "title": "Placing Orders",
                            "content": "When you place an order on Luméa, you agree to provide complete and accurate information, including shipping address, contact details, and payment information. All orders are subject to availability and confirmation."
                        },
                        {
                            "id": "04",
                            "slug": "prices-and-payment",
                            "title": "Prices and Payment",
                            "content": "All catalog prices are denominated in USD ($). We accept major credit cards, Apple Pay, and authorized regional payment methods. Prices are subject to revision without prior notice, though pending orders are honored at the checked-out price."
                        },
                        {
                            "id": "05",
                            "slug": "order-confirmation",
                            "title": "Order Confirmation",
                            "content": "Upon submitting checkout, you will receive an automated confirmation with an assigned order reference (e.g. LUM-XXXXXX). Receipt of confirmation indicates your order has entered preparation."
                        },
                        {
                            "id": "06",
                            "slug": "cancellation-and-changes",
                            "title": "Cancellation and Changes",
                            "content": "Orders enter atelier fulfillment swiftly. If you need to revise shipping details or cancel an item, please submit a request within 1 hour of placement."
                        },
                        {
                            "id": "07",
                            "slug": "delivery-and-shipping",
                            "title": "Delivery and Shipping",
                            "content": "Estimated delivery times are calculated upon courier handover. While we aim for prompt dispatch within 24-48 hours, transit schedules may fluctuate due to customs clearance or regional logistics."
                        },
                        {
                            "id": "08",
                            "slug": "returns-and-refunds",
                            "title": "Returns and Refunds",
                            "content": "We offer a 30-day return window for unopened items in original laboratory packaging. Return requests can be filed through our dedicated Return Request Wizard."
                        },
                        {
                            "id": "09",
                            "slug": "product-information",
                            "title": "Product Information",
                            "content": "We curate 100% authentic dermatological formulations. Customers with hyper-reactive skin or allergies are encouraged to check complete ingredient lists and perform patch tests."
                        },
                        {
                            "id": "10",
                            "slug": "intellectual-property",
                            "title": "Intellectual Property",
                            "content": "All logos, photography, formulations catalogs, and editorial journal articles are protected under copyright and trademark treaties."
                        },
                        {
                            "id": "11",
                            "slug": "prohibited-use",
                            "title": "Prohibited Use",
                            "content": "You may not misuse our platform to distribute malware, reverse-engineer proprietary algorithms, conduct unauthorized bulk scraping, or engage in resale speculation."
                        },
                        {
                            "id": "12",
                            "slug": "limitation-of-liability",
                            "title": "Limitation of Liability",
                            "content": "Luméa shall not be held liable for indirect or consequential damages arising from unforeseen platform interruptions or third-party delivery delays."
                        },
                        {
                            "id": "13",
                            "slug": "changes-to-these-terms",
                            "title": "Changes to These Terms",
                            "content": "We reserve the right to amend these Terms to reflect service enhancements. Continued use of our site signifies acceptance of amended terms."
                        },
                        {
                            "id": "14",
                            "slug": "governing-law",
                            "title": "Governing Law",
                            "content": "These Terms are governed by and construed in accordance with the laws of Cambodia and applicable international consumer treaties."
                        },
                        {
                            "id": "15",
                            "slug": "contact-us",
                            "title": "Contact Us",
                            "content": "If you have any questions about these Terms of Service, our customer care team is here to assist at contact@lumea.com."
                        }
                    ],
                    "commitments": [
                        { "title": "Fair and honest policies", "desc": "We keep our terms transparent and easy to read." },
                        { "title": "Clear ordering and return process", "desc": "Every step is laid out with no hidden catches." },
                        { "title": "Respect for customers and brands", "desc": "We honor consumer trust and scientific integrity." }
                    ],
                    "contact_box": {
                        "email": "contact@lumea.com",
                        "desc": "If you have any questions about these Terms of Service, our team is here to help."
                    }
                }
            )
        ]
        db.add_all(initial_pages)
        db.commit()
        print(f"[Seed] Created {len(initial_pages)} CMS & Legal pages in database.")

    # 7. Seed Skincare Journal Articles
    if db.query(Article).count() == 0:
        initial_articles = [
            Article(
                slug="how-to-build-a-skincare-routine-for-your-skin-type",
                title="How to Build a Skincare Routine for Your Skin Type",
                subtitle="A simple guide to finding the right products, in the right order, for healthier, happier skin.",
                category="Skincare Basics",
                read_time="8 min read",
                views_count="12.4K views",
                author_name="Sophea Meas",
                author_role="Skincare Expert",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Jun 15, 2025",
                hero_image="/images/article-details-hero.jpg",
                thumbnail="/images/article-details-hero.jpg",
                excerpt="A good skincare routine doesn't have to be complicated. It's about understanding your skin, choosing the right products, and using them consistently.",
                is_featured=True,
                is_popular=True,
                popular_rank=1,
                toc=[
                    { "id": "matters", "title": "Why a Skincare Routine Matters" },
                    { "id": "step1", "title": "Step 1: Know Your Skin Type" },
                    { "id": "step2", "title": "Step 2: Choose the Right Products" },
                    { "id": "step3", "title": "Step 3: Follow the Right Order" },
                    { "id": "routines", "title": "Sample Routines by Skin Type" },
                    { "id": "mistakes", "title": "Common Mistakes to Avoid" },
                    { "id": "expert-tips", "title": "Expert Tips" },
                    { "id": "final-thoughts", "title": "Final Thoughts" }
                ],
                content="""
A good skincare routine doesn't have to be complicated. It's about understanding your skin, choosing the right products, and using them consistently. Whether you're dealing with dryness, oiliness, or sensitivity, the right routine can help you achieve healthier, brighter skin over time.

## Why a Skincare Routine Matters
Your skin faces many challenges every day — pollution, UV rays, stress, and more. A consistent skincare routine helps to:
- Keep your skin clean and healthy
- Prevent common skin concerns like acne, dryness, and premature aging
- Support your skin barrier against environmental stressors
- Help skincare products work effectively and synergistically

## Step 1: Know Your Skin Type
Before buying any products, it's crucial to identify your skin type:
- **Dry Skin**: Feels tight, flaky, or rough. Craves deep nourishment like ceramides and hyaluronic acid.
- **Oily Skin**: Shiny appearance, enlarged pores, prone to breakouts. Needs gentle foaming cleansers and lightweight niacinamide.
- **Combination Skin**: Oily T-zone (forehead, nose, chin) with normal or dry cheeks.
- **Sensitive Skin**: Easily reddened, itchy, or reacts to harsh fragrance. Requires soothing Centella Asiatica and hypoallergenic botanicals.

## Step 2: Choose the Right Products
Focus on the 3 fundamental pillars: Cleanser, Moisturizer, and Sunscreen. Once your core routine is locked, add targeted treatments like serums and exfoliants.

## Step 3: Follow the Right Order
Always layer products from the thinnest to thickest consistency:
1. Cleanser (Water-based or double cleanse)
2. Toner or Essence
3. Targeted Serums & Ampoules
4. Moisturizer or Emulsion
5. Sunscreen (Morning essential)

## Sample Routines by Skin Type
A morning routine should prioritize protection (antioxidants + SPF), while the evening routine focuses on renewal and barrier restoration (retinoids + ceramides).
"""
            ),
            Article(
                slug="how-to-build-a-simple-skincare-routine-that-actually-works",
                title="How to Build a Simple Skincare Routine That Actually Works",
                subtitle="A beginner-friendly guide to creating an effective skincare routine with the right products for your skin type.",
                category="Skincare Basics",
                read_time="5 min read",
                views_count="9.8K views",
                author_name="Sophea Meas",
                author_role="Skincare Expert",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 28, 2025",
                hero_image="/images/article-thumb-routine.jpg",
                thumbnail="/images/article-thumb-routine.jpg",
                excerpt="Streamline your regimen down to what truly matters. Learn the golden trifecta of daily skincare without wasting money on redundant steps.",
                is_featured=False,
                is_popular=True,
                popular_rank=2,
                content="A stripped-down 3-step routine often yields better results than a chaotic 10-step shelf. Start with gentle cleansing, lightweight hydration, and daily broad-spectrum SPF 50."
            ),
            Article(
                slug="niacinamide-what-it-does-and-why-your-skin-might-love-it",
                title="Niacinamide: What It Does and Why Your Skin Might Love It",
                subtitle="Discover the benefits of niacinamide, how it works, and the best way to add it to your skincare routine.",
                category="Ingredients",
                read_time="6 min read",
                views_count="14.2K views",
                author_name="Dara Kim",
                author_role="Cosmetic Chemist",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 25, 2025",
                hero_image="/images/article-thumb-niacinamide.jpg",
                thumbnail="/images/article-thumb-niacinamide.jpg",
                excerpt="Niacinamide (Vitamin B3) is one of the most versatile and well-tolerated actives in modern dermatological skincare.",
                is_featured=False,
                is_popular=True,
                popular_rank=3,
                content="From minimizing enlarged pores to calming redness and strengthening the lipid barrier, niacinamide is compatible with nearly all skin types."
            ),
            Article(
                slug="the-real-guide-to-sunscreen-spf-pa-and-how-to-apply-it",
                title="The Real Guide to Sunscreen (SPF, PA, and How to Apply It)",
                subtitle="Everything you need to know about sunscreen, from choosing the right SPF to applying it correctly.",
                category="Sun Care",
                read_time="4 min read",
                views_count="11.1K views",
                author_name="Sokchan Put",
                author_role="Dermatology Fellow",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 22, 2025",
                hero_image="/images/article-thumb-sunscreen.jpg",
                thumbnail="/images/article-thumb-sunscreen.jpg",
                excerpt="Understanding the distinction between UVA and UVB protection, chemical vs physical filters, and the two-finger rule.",
                is_featured=False,
                is_popular=True,
                popular_rank=4,
                content="Sunscreen is your number one anti-aging formulation. Learn how to prevent white casts and find non-greasy textures that wear beautifully under makeup."
            ),
            Article(
                slug="how-to-layer-skincare-products-in-the-right-order",
                title="How to Layer Skincare Products in the Right Order",
                subtitle="A simple step-by-step guide to layering your skincare products for maximum results.",
                category="Skincare Tips",
                read_time="5 min read",
                views_count="8.5K views",
                author_name="Visal Suon",
                author_role="Esthetician",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 20, 2025",
                hero_image="/images/article-thumb-layer.jpg",
                thumbnail="/images/article-thumb-layer.jpg",
                excerpt="Ensure high absorption and avoid product pilling by applying formulas from lowest to highest viscosity.",
                is_featured=False,
                is_popular=False,
                content="Water-based formulas first, followed by active serums, richer emulsions, and finally occlusive barrier balms."
            ),
            Article(
                slug="how-sleep-affects-your-skin-and-what-you-can-do-about-it",
                title="How Sleep Affects Your Skin (And What You Can Do About It)",
                subtitle="Better sleep can lead to clearer, brighter, and healthier skin. Here's how it works and practical tips to improve it.",
                category="Skin Health",
                read_time="6 min read",
                views_count="7.9K views",
                author_name="Leangmeng Hai",
                author_role="Wellness Practitioner",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 18, 2025",
                hero_image="/images/article-thumb-sleep.jpg",
                thumbnail="/images/article-thumb-sleep.jpg",
                excerpt="Circadian rhythms regulate cellular mitosis and collagen repair during deep sleep cycles.",
                is_featured=False,
                is_popular=False,
                content="Lack of sleep elevates cortisol, inducing sebum hyper-production and impaired barrier moisture retention."
            ),
            Article(
                slug="centella-asiatica-the-soothing-ingredient-for-sensitive-skin",
                title="Centella Asiatica: The Soothing Ingredient for Sensitive Skin",
                subtitle="Learn why Centella Asiatica is loved for sensitive skin and how it helps calm, repair, and protect the skin barrier.",
                category="Ingredients",
                read_time="5 min read",
                views_count="13.7K views",
                author_name="Pichudom Keat",
                author_role="Botanical Researcher",
                author_avatar="/images/avatar-sreynich.jpg",
                published_at="Aug 15, 2025",
                hero_image="/images/article-thumb-centella.jpg",
                thumbnail="/images/article-thumb-centella.jpg",
                excerpt="Also known as Cica or Tiger Grass, Centella Asiatica contains madecassoside, a powerhouse compound for compromised skin.",
                is_featured=False,
                is_popular=False,
                content="Accelerate wound healing and soothe irritated, red skin with concentrated Centella Asiatica botanical extracts."
            )
        ]
        db.add_all(initial_articles)
        db.commit()
        print(f"[Seed] Created {len(initial_articles)} Skincare Journal articles in database.")

    # 6. Seed Brands
    if db.query(Brand).count() == 0:
        initial_brands = [
            Brand(
                name="The Ordinary",
                slug="the-ordinary",
                tagline="Clinical Formulations with Integrity.",
                country="Canada",
                country_code="CA",
                website="https://theordinary.com",
                description="Science-backed skincare at an honest price.",
                story="The Ordinary is an evolving collection of treatments offering familiar, effective clinical technologies positioned to raise pricing and communication integrity in skincare.",
                logo_url="/images/brand-ordinary.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=True,
                is_active=True
            ),
            Brand(
                name="SKIN1004",
                slug="skin1004",
                tagline="Pure from Nature.",
                country="South Korea",
                country_code="KR",
                website="https://skin1004.com",
                description="Gentle, natural skincare from the untouched nature.",
                story="Centella Asiatica harvested directly from pristine Madagascar soil, crafted for hyper-sensitive skin calming.",
                logo_url="/images/brand-skin1004.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=True,
                is_active=True
            ),
            Brand(
                name="CeraVe",
                slug="cerave",
                tagline="Developed with Dermatologists.",
                country="United States",
                country_code="US",
                website="https://cerave.com",
                description="Essential ceramides for healthy skin.",
                story="Formulated with 3 essential ceramides and Multivesicular Emulsion Technology to restore the protective skin barrier.",
                logo_url="/images/brand-cerave.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=True,
                is_active=True
            ),
            Brand(
                name="La Roche-Posay",
                slug="la-roche-posay",
                tagline="A Better Life for Sensitive Skin.",
                country="France",
                country_code="FR",
                website="https://laroche-posay.com",
                description="Dermatological skincare for sensitive skin.",
                story="Enriched with selenium-rich French thermal spring water, recommended by over 90,000 dermatologists worldwide.",
                logo_url="/images/brand-laroche.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=True,
                is_active=True
            ),
            Brand(
                name="Cetaphil",
                slug="cetaphil",
                tagline="Healthy Skin for Life.",
                country="Canada",
                country_code="CA",
                website="https://cetaphil.com",
                description="Gentle and effective skincare for everyday use.",
                story="Clinically proven gentle formulas designed to defend against 5 signs of skin sensitivity.",
                logo_url="/images/brand-cetaphil.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=False,
                is_active=True
            ),
            Brand(
                name="Innisfree",
                slug="innisfree",
                tagline="Nature for a Better Tomorrow",
                country="South Korea",
                country_code="KR",
                website="https://innisfree.com",
                description="Natural beauty from the pristine island of Jeju.",
                story="Harnessing green tea, volcanic clusters, and Jeju orchid to deliver clean, radiant botanical harmony.",
                logo_url="/images/brand-innisfree.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=False,
                is_active=True
            ),
            Brand(
                name="Paula's Choice",
                slug="paulas-choice",
                tagline="Beauty Begins with Truth.",
                country="United States",
                country_code="US",
                website="https://paulaschoice.com",
                description="Evidence-based skincare for real results.",
                story="Smart, safe beauty backed by published research studies. 100% fragrance-free and non-irritating.",
                logo_url="/images/brand-paulaschoice.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=False,
                is_active=True
            ),
            Brand(
                name="L'Oréal Paris",
                slug="loreal-paris",
                tagline="Because You're Worth It.",
                country="France",
                country_code="FR",
                website="https://lorealparis.com",
                description="Innovative beauty for every woman.",
                story="Pioneering scientific excellence and dermatological discoveries to deliver premium anti-aging results.",
                logo_url="/images/brand-loreal.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=True,
                is_active=True
            ),
            Brand(
                name="Anua",
                slug="anua",
                tagline="Keep Things Simple.",
                country="South Korea",
                country_code="KR",
                website="https://anua.kr",
                description="Minimal, effective skincare for a calm and healthy skin.",
                story="Heartleaf 77% soothing formulations focused on calming troubled skin with minimal non-toxic ingredients.",
                logo_url="/images/brand-anua.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=False,
                is_active=False
            ),
            Brand(
                name="COSRX",
                slug="cosrx",
                tagline="Expecting Tomorrow.",
                country="South Korea",
                country_code="KR",
                website="https://cosrx.com",
                description="Skincare solutions for all.",
                story="Simple, functional ingredients like Snail Mucin and BHA designed to treat problematic skin concerns.",
                logo_url="/images/brand-cosrx.png",
                banner_url="/images/admin-hero-bottles.jpg",
                is_featured=False,
                is_active=True
            )
        ]
        db.add_all(initial_brands)
        db.commit()
        print(f"[Seed] Created {len(initial_brands)} Brands in database.")

    # 8. Seed Reviews
    if db.query(Review).count() == 0:
        sample_reviews = [
            Review(
                product_id=201,
                product_name="Facial Treatment Essence",
                product_image="/images/prod-sk2.jpg",
                customer_name="Sreypov Chhum",
                customer_email="sreypov@gmail.com",
                customer_avatar="/images/customer-1.jpg",
                verified_purchase=True,
                rating=5,
                title="Amazing results!",
                comment="My skin feels so much smoother and brighter after just two weeks. Love this essence so much, truly miraculous texture!",
                status="approved",
                helpful_count=24
            ),
            Review(
                product_id=202,
                product_name="Niacinamide 10% + Zinc 1%",
                product_image="/images/prod-ordinary.jpg",
                customer_name="Visal Suon",
                customer_email="visal@gmail.com",
                customer_avatar="/images/customer-2.jpg",
                verified_purchase=True,
                rating=4,
                title="Good product",
                comment="It's gentle on my sensitive skin. Has a nice texture and absorbs quickly without feeling greasy.",
                status="approved",
                helpful_count=18
            ),
            Review(
                product_id=204,
                product_name="Moisturizing Cream",
                product_image="/images/prod-cerave.jpg",
                customer_name="Dara Kim",
                customer_email="dara@gmail.com",
                customer_avatar="/images/customer-3.jpg",
                verified_purchase=True,
                rating=2,
                title="Not for me",
                comment="I didn't see much difference, maybe it's just not suitable for my skin type. Felt a bit heavy for humid days.",
                status="approved",
                helpful_count=5
            ),
            Review(
                product_id=208,
                product_name="Green Tea Seed Hyaluronic Serum",
                product_image="/images/prod-innisfree-cleanser.jpg",
                customer_name="Takakvitya Tey",
                customer_email="takakvitya@gmail.com",
                customer_avatar="/images/customer-4.jpg",
                verified_purchase=True,
                rating=5,
                title="Love it!",
                comment="This serum really helps with my dark spots. Will definitely repurchase! The golden botanical tone smells lovely.",
                status="pending",
                helpful_count=12
            ),
            Review(
                product_id=203,
                product_name="Lip Sleeping Mask",
                product_image="/images/prod-laneige.jpg",
                customer_name="Leapmeng Hai",
                customer_email="leapmeng@gmail.com",
                customer_avatar="/images/customer-5.jpg",
                verified_purchase=True,
                rating=4,
                title="Great quality",
                comment="Feels luxurious and works well. My lips and skin are more hydrated now in the morning after air-conditioned nights.",
                status="approved",
                helpful_count=15
            ),
            Review(
                product_id=205,
                product_name="Effaclar Duo+ Anti-Imperfections",
                product_image="/images/prod-laroche-effaclar.jpg",
                customer_name="Pichudom Keat",
                customer_email="pichudom@gmail.com",
                customer_avatar="/images/customer-6.jpg",
                verified_purchase=True,
                rating=2,
                title="Caused irritation",
                comment="Unfortunately, it broke me out after a few uses. Make sure to patch test before applying all over.",
                status="pending",
                helpful_count=3
            ),
            Review(
                product_id=206,
                product_name="Advanced Snail 96 Mucin Power Essence",
                product_image="/images/prod-cosrx-snail.jpg",
                customer_name="Sokchan Put",
                customer_email="sokchan@gmail.com",
                customer_avatar="/images/customer-7.jpg",
                verified_purchase=True,
                rating=5,
                title="Holy grail!",
                comment="This is my go-to moisturizer now. Keeps my skin soft all day without clogging my pores.",
                status="approved",
                helpful_count=42
            ),
            Review(
                product_id=107,
                product_name="Sensibio H2O Micellar Water",
                product_image="/images/prod-bioderma-micellar.jpg",
                customer_name="Sothea Ngin",
                customer_email="sothea@gmail.com",
                customer_avatar="/images/customer-8.jpg",
                verified_purchase=True,
                rating=4,
                title="Nice but pricey",
                comment="Good product overall, but a bit expensive for the size. Would love if they offered a value refill bottle.",
                status="rejected",
                helpful_count=8
            )
        ]
        db.add_all(sample_reviews)
        db.commit()
        print(f"[Seed] Created {len(sample_reviews)} initial Reviews in database.")

    # 9. Seed Quizzes
    if db.query(Quiz).count() == 0:
        sample_questions_1 = [
            {
                "id": 1,
                "step": 1,
                "question": "What best describes your skin today?",
                "description": "Choose the option that feels most accurate.",
                "type": "Single Choice",
                "required": True,
                "image": "/images/quiz-model.jpg",
                "help_text": "This helps us recommend the right products for your skin.",
                "options": [
                    { "id": "oily", "title": "Oily", "desc": "Shiny appearance, especially in the T-zone", "image": "/images/texture-oily.jpg", "maps_to": "Oily" },
                    { "id": "dry", "title": "Dry", "desc": "Feels tight or flaky", "image": "/images/texture-dry.jpg", "maps_to": "Dry" },
                    { "id": "combo", "title": "Combination", "desc": "Oily in some areas, dry in others", "image": "/images/texture-combination.jpg", "maps_to": "Combination" },
                    { "id": "normal", "title": "Normal", "desc": "Balanced, not too oily or dry", "image": "/images/texture-normal.jpg", "maps_to": "Normal" },
                    { "id": "sensitive", "title": "Sensitive", "desc": "Easily irritated or red", "image": "/images/texture-sensitive.jpg", "maps_to": "Sensitive" }
                ]
            },
            {
                "id": 2,
                "step": 2,
                "question": "How does your skin feel throughout the day?",
                "description": "Notice how your skin behaves after midday without touch-ups.",
                "type": "Single Choice",
                "required": True,
                "image": "/images/quiz-model.jpg",
                "options": [
                    { "id": "greasy", "title": "Greasy & Slippery", "desc": "Needs frequent blotting", "maps_to": "Oily" },
                    { "id": "tight", "title": "Stretchy & Dehydrated", "desc": "Feels taut around cheekbones", "maps_to": "Dry" },
                    { "id": "comfortable", "title": "Supple & Calm", "desc": "Even hydration and comfortable feel", "maps_to": "Normal" }
                ]
            },
            {
                "id": 3,
                "step": 3,
                "question": "Do you experience any of these skin concerns?",
                "description": "Select all that you would like your routine to target.",
                "type": "Multiple Choice",
                "required": False,
                "image": "/images/quiz-model.jpg",
                "options": [
                    { "id": "pores", "title": "Enlarged Pores & Texture", "desc": "Uneven skin surface", "maps_to": "Oily" },
                    { "id": "dullness", "title": "Dullness & Dark Spots", "desc": "Lack of radiance", "maps_to": "Normal" },
                    { "id": "redness", "title": "Redness & Irritation", "desc": "Sensitive to changes", "maps_to": "Sensitive" },
                    { "id": "fine_lines", "title": "Fine Lines & Elasticity", "desc": "Signs of aging", "maps_to": "Dry" }
                ]
            },
            {
                "id": 4,
                "step": 4,
                "question": "How would you describe your daily sun exposure?",
                "description": "Helps determine the level of SPF and antioxidant protection you need.",
                "type": "Single Choice",
                "required": True,
                "image": "/images/quiz-model.jpg",
                "options": [
                    { "id": "mostly_indoor", "title": "Mostly Indoors", "desc": "Under office air conditioning", "maps_to": "Combination" },
                    { "id": "moderate", "title": "Moderate Daily Sun", "desc": "Commutes and light outdoor walks", "maps_to": "Normal" },
                    { "id": "intense", "title": "Intense Outdoor Exposure", "desc": "Active outdoor lifestyle", "maps_to": "Sensitive" }
                ]
            },
            {
                "id": 5,
                "step": 5,
                "question": "Do you have any specific skin sensitivities?",
                "description": "Essential to keep your routine barrier-friendly.",
                "type": "Multiple Choice",
                "required": False,
                "image": "/images/quiz-model.jpg",
                "options": [
                    { "id": "fragrance", "title": "Synthetic Fragrance", "desc": "Triggers redness or hives", "maps_to": "Sensitive" },
                    { "id": "alcohol", "title": "Drying Alcohols", "desc": "Causes burning sensation", "maps_to": "Sensitive" },
                    { "id": "acids", "title": "High Percentage AHAs", "desc": "Stinging and flaking", "maps_to": "Sensitive" }
                ]
            },
            {
                "id": 6,
                "step": 6,
                "question": "What is your main skincare goal?",
                "description": "The ultimate result you wish to achieve in 30 days.",
                "type": "Single Choice",
                "required": True,
                "image": "/images/quiz-model.jpg",
                "options": [
                    { "id": "glass_skin", "title": "Radiant Porcelain Glow", "desc": "Healthy luminous translucence", "maps_to": "Normal" },
                    { "id": "deep_hydration", "title": "Plump Moisture Barrier", "desc": "Long-lasting hydration reservoir", "maps_to": "Dry" },
                    { "id": "clear_calm", "title": "Clear & Blemish-Free", "desc": "Balanced sebum and calmed pores", "maps_to": "Oily" }
                ]
            }
        ]

        sample_quizzes = [
            Quiz(
                id=1,
                title="Skin Type Quiz",
                slug="skin-type-quiz",
                description="Find your skin type and get personalized product recommendations.",
                target_audience="Beginners",
                badge="Skin Type",
                level="Beginner",
                cover_image="/images/quiz-model.jpg",
                status="active",
                questions_count=8,
                completions=6842,
                completion_rate="72.3%",
                questions_data=sample_questions_1
            ),
            Quiz(
                id=2,
                title="Skin Concern Quiz",
                slug="skin-concern-quiz",
                description="Tell us your main skin concerns and we'll suggest the best solutions.",
                target_audience="General Patrons",
                badge="Skin Concern",
                level="Product Recs",
                cover_image="/images/search-droplet-macro.jpg",
                status="active",
                questions_count=10,
                completions=3921,
                completion_rate="64.8%",
                questions_data=sample_questions_1
            ),
            Quiz(
                id=3,
                title="Personalized Routine Quiz",
                slug="personalized-routine-quiz",
                description="Get a complete skincare routine made just for you.",
                target_audience="Skincare Enthusiasts",
                badge="Full Routine",
                level="Advanced",
                cover_image="/images/pdp-model-radiant.jpg",
                status="active",
                questions_count=12,
                completions=1693,
                completion_rate="58.1%",
                questions_data=sample_questions_1
            ),
            Quiz(
                id=4,
                title="Sensitive Skin Quiz",
                slug="sensitive-skin-quiz",
                description="Find out if you have sensitive skin and get gentle product recommendations.",
                target_audience="Sensitive Skin",
                badge="Sensitive Skin",
                level="Product Recs",
                cover_image="/images/cat-masks.jpg",
                status="draft",
                questions_count=9,
                completions=0,
                completion_rate="0%",
                questions_data=sample_questions_1
            )
        ]
        db.add_all(sample_quizzes)
        db.commit()
        print(f"[Seed] Created {len(sample_quizzes)} initial Quizzes in database.")

    # 10. Seed Return Requests
    if db.query(ReturnRequest).count() <= 1:
        # Clear single existing placeholder if any
        db.query(ReturnRequest).delete()
        sample_returns = [
            ReturnRequest(
                request_number="RR24081234",
                order_number="LM24081234",
                customer_name="Sreypov Chan",
                customer_email="sreypov.chan@example.com",
                product_name="Facial Treatment Essence",
                product_image="/images/prod-sk2.jpg",
                product_variant="230ml",
                price=125.0,
                quantity=1,
                reason="Product is damaged",
                resolution="Refund",
                description="Product arrived with a damaged seal and leaking bottle.",
                status="Approved",
                current_step=3,
                submitted_date="Aug 14, 2024",
                timeline=[
                    {"id": 1, "title": "Submitted", "date": "Aug 14, 2024", "status": "completed"},
                    {"id": 2, "title": "Under Review", "date": "Aug 15, 2024", "status": "completed"},
                    {"id": 3, "title": "Approved", "date": "Aug 16, 2024", "status": "current"},
                    {"id": 4, "title": "Return in Transit", "date": "Pending", "status": "upcoming"},
                    {"id": 5, "title": "Item Received", "date": "Pending", "status": "upcoming"},
                    {"id": 6, "title": "Refund Processing", "date": "Pending", "status": "upcoming"},
                    {"id": 7, "title": "Refund Completed", "date": "Pending", "status": "upcoming"}
                ]
            ),
            ReturnRequest(
                request_number="RR-10028",
                order_number="#10028",
                customer_name="Sreypov Chhum",
                customer_email="sreypov@gmail.com",
                product_name="Brightening Face Serum",
                product_image="/images/prod-sk2.jpg",
                product_variant="30ml · 1 item",
                price=28.00,
                quantity=1,
                reason="Changed Mind",
                resolution="Full Refund",
                description="Decided to stick with my current skincare routine for another month.",
                status="pending",
                current_step=2,
                submitted_date="Aug 28, 2025 10:24 AM"
            ),
            ReturnRequest(
                request_number="RR-10024",
                order_number="#10024",
                customer_name="Visal Suon",
                customer_email="visal@gmail.com",
                product_name="Hydrating Moisturizer",
                product_image="/images/prod-laneige.jpg",
                product_variant="50ml · 1 item",
                price=32.00,
                quantity=1,
                reason="Product Not Suitable",
                resolution="Store Credit",
                description="Texture is a bit heavier than I expected for my oily T-zone.",
                status="approved",
                current_step=3,
                submitted_date="Aug 27, 2025 03:15 PM"
            ),
            ReturnRequest(
                request_number="RR-10021",
                order_number="#10021",
                customer_name="Dara Kim",
                customer_email="dara@gmail.com",
                product_name="Gentle Cleanser",
                product_image="/images/prod-anua-cleanser.jpg",
                product_variant="100ml · 1 item",
                price=18.00,
                quantity=1,
                reason="Skin Irritation",
                resolution="Full Refund",
                description="Experienced slight tingling and redness after evening application.",
                status="pending",
                current_step=2,
                submitted_date="Aug 26, 2025 11:02 AM"
            ),
            ReturnRequest(
                request_number="RR-10018",
                order_number="#10018",
                customer_name="Takakvitya Tey",
                customer_email="takakvitya@gmail.com",
                product_name="Vitamin C Serum",
                product_image="/images/prod-cerave.jpg",
                product_variant="30ml · 1 item",
                price=26.00,
                quantity=1,
                reason="Damaged Item",
                resolution="Replacement Formulation",
                description="Dropper was slightly cracked upon package arrival.",
                status="refunded",
                current_step=7,
                submitted_date="Aug 25, 2025 09:48 AM"
            ),
            ReturnRequest(
                request_number="RR-10016",
                order_number="#10016",
                customer_name="Leapmeng Hai",
                customer_email="leapmeng@gmail.com",
                product_name="Nourishing Night Cream",
                product_image="/images/prod-boj.jpg",
                product_variant="50ml · 1 item",
                price=34.00,
                quantity=1,
                reason="Wrong Item",
                resolution="Exchange",
                description="Received the day moisturizer instead of the night repair cream.",
                status="approved",
                current_step=3,
                submitted_date="Aug 24, 2025 04:20 PM"
            ),
            ReturnRequest(
                request_number="RR-10014",
                order_number="#10014",
                customer_name="Pichudom Keat",
                customer_email="pichudom@gmail.com",
                product_name="Soothing Sheet Mask",
                product_image="/images/cat-masks.jpg",
                product_variant="5 pcs · 1 item",
                price=15.00,
                quantity=1,
                reason="Expired Product",
                resolution="Full Refund",
                description="Box showed expiry date within 30 days of arrival.",
                status="rejected",
                current_step=1,
                submitted_date="Aug 22, 2025 01:10 PM"
            ),
            ReturnRequest(
                request_number="RR-10011",
                order_number="#10011",
                customer_name="Sokchan Put",
                customer_email="sokchan@gmail.com",
                product_name="Daily Sunscreen SPF50",
                product_image="/images/texture-combination.jpg",
                product_variant="50ml · 1 item",
                price=24.00,
                quantity=1,
                reason="Defective Item",
                resolution="Store Credit",
                description="Pump mechanism failed to dispense cream properly.",
                status="approved",
                current_step=3,
                submitted_date="Aug 20, 2025 08:35 AM"
            ),
            ReturnRequest(
                request_number="RR-10009",
                order_number="#10009",
                customer_name="Sothea Ngin",
                customer_email="sothea@gmail.com",
                product_name="Toner Essence",
                product_image="/images/cat-toners.jpg",
                product_variant="150ml · 1 item",
                price=22.00,
                quantity=1,
                reason="Changed Mind",
                resolution="Full Refund",
                description="Ordered two by accident during promotional checkout.",
                status="pending",
                current_step=2,
                submitted_date="Aug 18, 2025 02:12 PM"
            )
        ]
        db.add_all(sample_returns)
        db.commit()
        print(f"[Seed] Created {len(sample_returns)} Return Requests in database.")


