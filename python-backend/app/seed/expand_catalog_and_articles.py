"""
Script to expand Luméa database with 16 new luxury skincare products
and 4 in-depth dermatological journal articles.
"""
import sys
import os
import json
import sqlite3

# Add app to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(BASE_DIR))

from app.core.database import SessionLocal
from app.models.product import Product
from app.models.article import Article
from app.models.category import Category
from app.models.brand import Brand

NEW_PRODUCTS = [
    {
        "id": 301,
        "name": "Relief Sun: Rice + Probiotics SPF50+ PA++++",
        "brand": "Beauty of Joseon",
        "slug": "beauty-of-joseon-relief-sun-rice-probiotics-spf50",
        "category": "sunscreens",
        "category_id": 5,
        "category_name": "Sunscreens",
        "subcategory": "Daily SPF Protection",
        "product_type": "Chemical & Probiotic Sunscreen",
        "price": 18.00,
        "compare_at_price": 22.00,
        "rating": 4.9,
        "reviews": 3240,
        "badge": "Best Seller",
        "badge_type": "bestseller",
        "stock": 65,
        "image_url": "/images/prod-boj.jpg",
        "description": "A lightweight, organic chemical sunscreen enriched with 30% rice extract and grain fermented probiotics. Melts seamlessly into the skin with zero white cast, leaving a hydrated, lit-from-within glow.",
        "is_featured": True,
        "skin_type": ["All Skin Types", "Dry", "Sensitive", "Normal"],
        "skin_concern": ["Sun Protection", "Dehydration", "Dullness"],
        "gallery": ["/images/prod-boj.jpg", "/images/article-thumb-sunscreen.jpg"]
    },
    {
        "id": 302,
        "name": "Birch Juice Moisturizing Sun Cream SPF50+ PA++++",
        "brand": "Round Lab",
        "slug": "round-lab-birch-juice-moisturizing-sun-cream-spf50",
        "category": "sunscreens",
        "category_id": 5,
        "category_name": "Sunscreens",
        "subcategory": "Hydrating Sunscreen",
        "product_type": "Essence Sunscreen",
        "price": 21.00,
        "compare_at_price": 26.00,
        "rating": 4.8,
        "reviews": 1890,
        "badge": "Award Winner",
        "badge_type": "award",
        "stock": 42,
        "image_url": "/images/article-thumb-sunscreen.jpg",
        "description": "Infused with Inje Birch Tree sap and Vita Hyaluronic Acid, this award-winning Korean sunscreen acts as both an intensive hydrating moisturizer and high-spectrum UV shield.",
        "is_featured": True,
        "skin_type": ["Dry", "Combination", "Dehydrated", "Sensitive"],
        "skin_concern": ["Sun Protection", "Dryness", "Barrier Repair"],
        "gallery": ["/images/article-thumb-sunscreen.jpg"]
    },
    {
        "id": 303,
        "name": "Anthelios UVMune 400 Invisible Fluid SPF50+",
        "brand": "La Roche-Posay",
        "slug": "la-roche-posay-anthelios-uvmune-400-invisible-fluid",
        "category": "sunscreens",
        "category_id": 5,
        "category_name": "Sunscreens",
        "subcategory": "Clinical Sun Protection",
        "product_type": "Ultra-Light Sun Fluid",
        "price": 29.50,
        "compare_at_price": 34.00,
        "rating": 4.7,
        "reviews": 2150,
        "badge": "Derm Pick",
        "badge_type": "staff_pick",
        "stock": 50,
        "image_url": "/images/prod-laroche-effaclar.jpg",
        "description": "Powered by the revolutionary Mexoryl 400 filter protecting against ultra-long UVA rays. Non-greasy, non-comedogenic, and water, sweat, and sand resistant.",
        "is_featured": False,
        "skin_type": ["All Skin Types", "Oily", "Sensitive", "Acne-Prone"],
        "skin_concern": ["Sun Protection", "Hyperpigmentation", "Premature Aging"],
        "gallery": ["/images/prod-laroche-effaclar.jpg"]
    },
    {
        "id": 304,
        "name": "Madagascar Centella Hyalu-Cica Water-Fit Sun Serum SPF50+",
        "brand": "SKIN1004",
        "slug": "skin1004-madagascar-centella-hyalu-cica-sun-serum",
        "category": "sunscreens",
        "category_id": 5,
        "category_name": "Sunscreens",
        "subcategory": "Soothing Sun Serum",
        "product_type": "Sun Serum",
        "price": 19.00,
        "compare_at_price": 24.00,
        "rating": 4.9,
        "reviews": 2780,
        "badge": "Trending",
        "badge_type": "trending",
        "stock": 58,
        "image_url": "/images/article-thumb-centella.jpg",
        "description": "A non-nano chemical sun serum that simultaneously calms and hydrates with Madagascar Centella Asiatica and multiple molecular weights of hyaluronic acid.",
        "is_featured": True,
        "skin_type": ["Sensitive", "Combination", "Oily", "Acne-Prone"],
        "skin_concern": ["Redness & Sensitivity", "Sun Protection", "Oil Control"],
        "gallery": ["/images/article-thumb-centella.jpg"]
    },
    {
        "id": 305,
        "name": "Water Bank Blue Hyaluronic Cream",
        "brand": "LANEIGE",
        "slug": "laneige-water-bank-blue-hyaluronic-cream",
        "category": "moisturizers",
        "category_id": 4,
        "category_name": "Moisturizers",
        "subcategory": "Barrier Repair Moisturizer",
        "product_type": "Rich Hydrating Cream",
        "price": 40.00,
        "compare_at_price": 45.00,
        "rating": 4.8,
        "reviews": 1420,
        "badge": "Best Seller",
        "badge_type": "bestseller",
        "stock": 35,
        "image_url": "/images/prod-laneige.jpg",
        "description": "Micro-sized Blue Hyaluronic Acid delivers deep-absorbing 100-hour hydration. Strengthens moisture barrier, relieves redness, and provides lasting comfort without stickiness.",
        "is_featured": True,
        "skin_type": ["Dry", "Normal", "Sensitive", "Dehydrated"],
        "skin_concern": ["Dryness & Flaking", "Barrier Damage", "Dullness"],
        "gallery": ["/images/prod-laneige.jpg"]
    },
    {
        "id": 306,
        "name": "DIVE-IN Low Molecular Hyaluronic Acid Soothing Cream",
        "brand": "Torriden",
        "slug": "torriden-dive-in-low-molecular-hyaluronic-acid-cream",
        "category": "moisturizers",
        "category_id": 4,
        "category_name": "Moisturizers",
        "subcategory": "Water Gel Cream",
        "product_type": "Soothing Gel Cream",
        "price": 23.00,
        "compare_at_price": 28.00,
        "rating": 4.8,
        "reviews": 1670,
        "badge": "Clean Beauty",
        "badge_type": "clean",
        "stock": 48,
        "image_url": "/images/prod-cream.jpg",
        "description": "Formulated with 5D-Complex Hyaluronic Acid and Trehalose to provide instant quenching hydration, forming an airy moisture shield that locks in plump dewy suppleness.",
        "is_featured": False,
        "skin_type": ["Oily", "Combination", "Sensitive", "Dehydrated"],
        "skin_concern": ["Dehydration", "Excess Oil", "Sensitive Barrier"],
        "gallery": ["/images/prod-cream.jpg"]
    },
    {
        "id": 307,
        "name": "Concentrated Ginseng Renewing Cream Classic",
        "brand": "Sulwhasoo",
        "slug": "sulwhasoo-concentrated-ginseng-renewing-cream",
        "category": "moisturizers",
        "category_id": 4,
        "category_name": "Moisturizers",
        "subcategory": "Luxury Prestige Anti-Aging",
        "product_type": "Sculpting Regenerative Cream",
        "price": 260.00,
        "compare_at_price": 290.00,
        "rating": 4.9,
        "reviews": 890,
        "badge": "Atelier Prestige",
        "badge_type": "luxury",
        "stock": 15,
        "image_url": "/images/prod-sulwhasoo.jpg",
        "description": "An ultra-prestige anti-aging masterpiece powered by Ginsenomics™—a rare, concentrated bioactive ginseng saponin that visibly restores skin elasticity, density, and youthful radiance.",
        "is_featured": True,
        "skin_type": ["Mature", "Dry", "Normal"],
        "skin_concern": ["Fine Lines & Wrinkles", "Loss of Elasticity", "Dryness"],
        "gallery": ["/images/prod-sulwhasoo.jpg"]
    },
    {
        "id": 308,
        "name": "Advanced Snail 92 All in One Cream",
        "brand": "COSRX",
        "slug": "cosrx-advanced-snail-92-all-in-one-cream",
        "category": "moisturizers",
        "category_id": 4,
        "category_name": "Moisturizers",
        "subcategory": "Repair & Nourish",
        "product_type": "Gel-Cream",
        "price": 22.00,
        "compare_at_price": 26.00,
        "rating": 4.7,
        "reviews": 2450,
        "badge": "Cult Favorite",
        "badge_type": "bestseller",
        "stock": 60,
        "image_url": "/images/prod-cosrx-snail.jpg",
        "description": "Enriched with 92% pure snail secretion filtrate, this multitasking cream infuses moisture, soothes irritation, and repairs compromised skin barriers after breakouts.",
        "is_featured": False,
        "skin_type": ["All Skin Types", "Acne-Prone", "Sensitive"],
        "skin_concern": ["Acne Scars", "Dehydration", "Redness"],
        "gallery": ["/images/prod-cosrx-snail.jpg"]
    },
    {
        "id": 309,
        "name": "Luméa Glass Skin Ritual Discovery Set (4-Piece Regimen)",
        "brand": "Luméa Atelier",
        "slug": "lumea-glass-skin-ritual-discovery-set",
        "category": "kits",
        "category_id": 8,
        "category_name": "Kits & Sets",
        "subcategory": "Complete Diagnostic Regimen",
        "product_type": "Curated Discovery Bundle",
        "price": 78.00,
        "compare_at_price": 98.00,
        "rating": 5.0,
        "reviews": 340,
        "badge": "Exclusive",
        "badge_type": "exclusive",
        "stock": 25,
        "image_url": "/images/cat-kits.jpg",
        "description": "A complete four-step ritual curated by Luméa dermatologists: Gentle Amino Cleanser, Ferment Essence Toner, Niacinamide Glow Ampoule, and Ceramide Cloud Cream.",
        "is_featured": True,
        "skin_type": ["All Skin Types", "Dry", "Combination", "Normal"],
        "skin_concern": ["Dullness", "Texture Refinement", "Barrier Strengthening"],
        "gallery": ["/images/cat-kits.jpg"]
    },
    {
        "id": 310,
        "name": "Pitera™ First Experience Atelier Discovery Kit",
        "brand": "SK-II",
        "slug": "sk-ii-pitera-first-experience-atelier-discovery-kit",
        "category": "kits",
        "category_id": 8,
        "category_name": "Kits & Sets",
        "subcategory": "Prestige Travel Set",
        "product_type": "Luxury Intro Kit",
        "price": 115.00,
        "compare_at_price": 135.00,
        "rating": 4.9,
        "reviews": 580,
        "badge": "Prestige Pick",
        "badge_type": "luxury",
        "stock": 20,
        "image_url": "/images/prod-sk2.jpg",
        "description": "Experience the transformative magic of PITERA™. Includes Facial Treatment Essence (75ml), Clear Lotion Toner (30ml), and one Facial Treatment Mask for crystal-clear skin.",
        "is_featured": True,
        "skin_type": ["All Skin Types", "Mature", "Dull"],
        "skin_concern": ["Uneven Texture", "Fine Lines", "Loss of Radiance"],
        "gallery": ["/images/prod-sk2.jpg"]
    },
    {
        "id": 311,
        "name": "The Daily Set: Squalane, HA & NMF",
        "brand": "The Ordinary",
        "slug": "the-ordinary-the-daily-set",
        "category": "kits",
        "category_id": 8,
        "category_name": "Kits & Sets",
        "subcategory": "Essential Daily Starter",
        "product_type": "3-Piece Regimen",
        "price": 24.90,
        "compare_at_price": 30.00,
        "rating": 4.6,
        "reviews": 1120,
        "badge": "Value Set",
        "badge_type": "sale",
        "stock": 45,
        "image_url": "/images/prod-ordinary.jpg",
        "description": "A simple, clinical 3-step regimen for daily hydration and barrier maintenance: Squalane Cleanser (50ml), Hyaluronic Acid 2% + B5 (30ml), and Natural Moisturizing Factors + HA (30ml).",
        "is_featured": False,
        "skin_type": ["Normal", "Dry", "Combination"],
        "skin_concern": ["Dehydration", "Daily Maintenance", "Dryness"],
        "gallery": ["/images/prod-ordinary.jpg"]
    },
    {
        "id": 312,
        "name": "Heartleaf Soothing & Calming Barrier Starter Trio",
        "brand": "Anua",
        "slug": "anua-heartleaf-soothing-calming-starter-trio",
        "category": "kits",
        "category_id": 8,
        "category_name": "Kits & Sets",
        "subcategory": "Sensitive Skin Set",
        "product_type": "3-Piece Soothing Kit",
        "price": 54.00,
        "compare_at_price": 65.00,
        "rating": 4.8,
        "reviews": 760,
        "badge": "Trending",
        "badge_type": "trending",
        "stock": 30,
        "image_url": "/images/prod-anua-toner.jpg",
        "description": "The ultimate calming regimen for redness and acne-prone skin: Heartleaf 77% Soothing Toner (150ml), Heartleaf Quercetinol Pore Foam (150ml), and Heartleaf 70% Intense Calming Cream (50ml).",
        "is_featured": True,
        "skin_type": ["Sensitive", "Acne-Prone", "Irritated", "Oily"],
        "skin_concern": ["Redness & Sensitivity", "Acne & Blemishes", "Pore Care"],
        "gallery": ["/images/prod-anua-toner.jpg"]
    },
    {
        "id": 313,
        "name": "Facial Treatment Mask (Box of 6 Restorative Sheets)",
        "brand": "SK-II",
        "slug": "sk-ii-facial-treatment-mask-box-of-6",
        "category": "masks",
        "category_id": 6,
        "category_name": "Masks",
        "subcategory": "Prestige Sheet Masks",
        "product_type": "Intensive Cotton Sheet Mask",
        "price": 105.00,
        "compare_at_price": 120.00,
        "rating": 4.9,
        "reviews": 940,
        "badge": "Luxury Bridal Pick",
        "badge_type": "luxury",
        "stock": 22,
        "image_url": "/images/cat-masks.jpg",
        "description": "A luxurious 100% cotton sheet mask soaked in a generous dose of PITERA™. Delivers intense hydration and instant luminosity for bridal preparations or post-flight revival.",
        "is_featured": True,
        "skin_type": ["All Skin Types", "Dry", "Fatigued"],
        "skin_concern": ["Dullness", "Dehydration", "Rough Texture"],
        "gallery": ["/images/cat-masks.jpg"]
    },
    {
        "id": 314,
        "name": "Overnight Vitalizing Radiance Mask",
        "brand": "Sulwhasoo",
        "slug": "sulwhasoo-overnight-vitalizing-radiance-mask",
        "category": "masks",
        "category_id": 6,
        "category_name": "Masks",
        "subcategory": "Overnight Sleeping Mask",
        "product_type": "Herbal Sleeping Mask",
        "price": 58.00,
        "compare_at_price": 68.00,
        "rating": 4.8,
        "reviews": 810,
        "badge": "Staff Pick",
        "badge_type": "staff_pick",
        "stock": 28,
        "image_url": "/images/prod-nightcream.jpg",
        "description": "A luxurious Hanbang herbal sleeping mask formulated with Nutritive RED Elixir™ (jujube and pomegranate extract). Restores moisture while you sleep so you awaken to plump, translucent glow.",
        "is_featured": False,
        "skin_type": ["Dry", "Normal", "Dull", "Mature"],
        "skin_concern": ["Dullness", "Morning Fatigue", "Dehydration"],
        "gallery": ["/images/prod-nightcream.jpg"]
    },
    {
        "id": 315,
        "name": "Heartleaf 77% Soothing Toner",
        "brand": "Anua",
        "slug": "anua-heartleaf-77-soothing-toner",
        "category": "toners",
        "category_id": 2,
        "category_name": "Toners",
        "subcategory": "Calming Toner",
        "product_type": "Water-Type Soothing Toner",
        "price": 23.00,
        "compare_at_price": 27.00,
        "rating": 4.8,
        "reviews": 3890,
        "badge": "Best Seller",
        "badge_type": "bestseller",
        "stock": 70,
        "image_url": "/images/prod-anua-toner.jpg",
        "description": "South Korea's #1 soothing toner containing 77% Houttuynia Cordata (Heartleaf) extract. Rapidly calms troubled skin, balances sebum, and purifies pores without stripping moisture.",
        "is_featured": True,
        "skin_type": ["Acne-Prone", "Sensitive", "Oily", "Combination"],
        "skin_concern": ["Redness & Sensitivity", "Acne & Blemishes", "Enlarged Pores"],
        "gallery": ["/images/prod-anua-toner.jpg"]
    },
    {
        "id": 316,
        "name": "1025 Dokdo Mineral Water Exfoliating Toner",
        "brand": "Round Lab",
        "slug": "round-lab-1025-dokdo-mineral-toner",
        "category": "toners",
        "category_id": 2,
        "category_name": "Toners",
        "subcategory": "Gentle Exfoliating Toner",
        "product_type": "Mineral Toner",
        "price": 22.00,
        "compare_at_price": 26.00,
        "rating": 4.7,
        "reviews": 2240,
        "badge": "Award Winner",
        "badge_type": "award",
        "stock": 55,
        "image_url": "/images/cat-toners.jpg",
        "description": "Formulated with pure deep seawater from Ulleungdo island, packed with 72 natural minerals. Gently removes dead surface cells with Hatching EX-07 enzyme while drenching skin in soothing moisture.",
        "is_featured": False,
        "skin_type": ["Sensitive", "Dry", "Combination", "Normal"],
        "skin_concern": ["Flakiness & Rough Texture", "Dullness", "Dehydration"],
        "gallery": ["/images/cat-toners.jpg"]
    }
]

NEW_ARTICLES = [
    {
        "id": 8,
        "slug": "mineral-vs-chemical-sunscreen-the-ultimate-dermatology-guide",
        "title": "Mineral vs. Chemical Sunscreen: The Ultimate Dermatological Comparison",
        "subtitle": "Zinc oxide versus advanced chemical filters: understand UV wavelengths, barrier comfort, white cast avoidance, and how to pick the right daily shield.",
        "category": "Sun Care",
        "read_time": "6 min read",
        "views_count": "14.2K views",
        "author_name": "Dr. Hemi Park",
        "author_role": "Board-Certified Dermatologist",
        "author_avatar": "/images/avatar-sreynich.jpg",
        "published_at": "Oct 12, 2025",
        "hero_image": "/images/article-thumb-sunscreen.jpg",
        "thumbnail": "/images/article-thumb-sunscreen.jpg",
        "excerpt": "Navigating SPF can feel confusing with countless labels. Here is the clinical breakdown of how physical blockers differ from modern chemical filters, and how to choose the right UV shield for your skin.",
        "is_featured": True,
        "is_popular": True,
        "popular_rank": 2,
        "toc": [
            {"id": "uv-spectrum", "title": "Understanding UVA vs. UVB Rays"},
            {"id": "mineral-filters", "title": "How Mineral (Physical) Sunscreens Work"},
            {"id": "chemical-filters", "title": "How Chemical Sunscreens Work"},
            {"id": "comparison", "title": "Head-to-Head Comparison: White Cast & Sensitivity"},
            {"id": "dermatologist-recommendation", "title": "Dermatologist Recommendations"}
        ],
        "content": """
Sunscreen is non-negotiable. Whether it is sunny or overcast, up to 80% of ultraviolet radiation penetrates through cloud cover and glass windows. Understanding the difference between mineral and chemical formulations helps you stay consistent with your daily protection.

## Understanding UVA vs. UVB Rays
- **UVB Rays (Burning)**: Cause immediate surface erythema, sunburn, and direct DNA damage to epidermis cells.
- **UVA Rays (Aging)**: Penetrate deeply into the dermis, breaking down collagen and elastin, leading to premature fine lines, hyperpigmentation, and loss of firmness.

## How Mineral (Physical) Sunscreens Work
Mineral sunscreens utilize natural earth minerals—primarily **Zinc Oxide** and **Titanium Dioxide**. They sit atop the stratum corneum like millions of micro-mirrors, reflecting and scattering ultraviolet rays away from the skin.

### Advantages of Mineral Sunscreens:
- **Immediate Protection**: Effective immediately upon application without waiting 20 minutes.
- **Extremely Hypoallergenic**: Gentle on reactive, rosacea-prone, and post-procedure skin.
- **Naturally Anti-inflammatory**: Zinc oxide actively calms redness and irritation.

## How Chemical Sunscreens Work
Chemical sunscreens use organic carbon-based filters like Avobenzone, Mexoryl SX/XL, Tinosorb S, and Uvinul A Plus. These compounds penetrate into the surface layers of the skin, absorb UV photons, and convert them harmlessly into infrared heat that dissipates from the skin.

### Advantages of Chemical Sunscreens:
- **Zero White Cast**: Completely invisible on all Fitzpatrick skin tones.
- **Cosmetically Elegant**: Lightweight, serum-like textures that layer flawlessly under makeup without pilling.
- **Sweat and Water Resistance**: Ideal for humid climates and outdoor sports.

## Head-to-Head Comparison: White Cast & Sensitivity
| Criteria | Mineral (Zinc Oxide) | Modern Chemical (K-Beauty & European) |
| :--- | :--- | :--- |
| **Texture** | Thicker, velvety finish | Weightless, essence-like |
| **White Cast** | Slight to moderate on deep tones | 100% Invisible |
| **Sensitivity** | Safest for reactive/eczema skin | Excellent if formulated fragrance-free |
| **Reapplication** | Requires patting | Effortless layering |

## Dermatologist Recommendations
1. If your skin is sensitive, inflamed, or pregnant: choose pure **Zinc Oxide** mineral protection.
2. If your skin is oily, combination, or wears daily foundation: choose modern Korean chemical sunscreens like *Beauty of Joseon Relief Sun* or *Round Lab Birch Juice*.
3. Use the **two-finger rule** (squeezing SPF along the index and middle fingers) for your entire face and neck to ensure true SPF 50+ coverage.
"""
    },
    {
        "id": 9,
        "slug": "the-science-of-skin-barrier-repair-ceramides-lipids",
        "title": "The Science of Skin Barrier Repair: Why Ceramides, Fatty Acids & Cholesterol Matter",
        "subtitle": "Discover the 3:1:1 golden ratio of stratum corneum lipids and how to recover quickly from over-exfoliation, irritation, and dryness.",
        "category": "Skincare Basics",
        "read_time": "7 min read",
        "views_count": "16.8K views",
        "author_name": "Sophea Meas",
        "author_role": "Skincare Specialist",
        "author_avatar": "/images/avatar-sreynich.jpg",
        "published_at": "Oct 14, 2025",
        "hero_image": "/images/ai-journal-science.jpg",
        "thumbnail": "/images/ai-journal-science.jpg",
        "excerpt": "When your skin barrier is compromised, moisture escapes and irritants flood in. Learn how clinical lipid repair accelerates recovery within 72 hours.",
        "is_featured": True,
        "is_popular": True,
        "popular_rank": 3,
        "toc": [
            {"id": "brick-and-mortar", "title": "The 'Brick and Mortar' Model of Your Skin"},
            {"id": "lipid-ratio", "title": "The 3:1:1 Golden Ratio: Ceramides, Cholesterol, Fatty Acids"},
            {"id": "symptoms", "title": "Warning Signs of a Compromised Barrier"},
            {"id": "72h-protocol", "title": "The 72-Hour Barrier Reset Protocol"},
            {"id": "ingredients-to-avoid", "title": "What to Pause During Recovery"}
        ],
        "content": """
The skin barrier is your body's frontline defense against environmental pathogens, pollutants, and trans-epidermal water loss (TEWL). When it thrives, skin is radiant, supple, and calm. When it is damaged, even water can cause stinging.

## The 'Brick and Mortar' Model of Your Skin
Dermatologists describe the epidermis using the classic brick-and-mortar analogy:
- **The Bricks**: Corneocyte skin cells packed with keratin and natural moisturizing factors (NMF).
- **The Mortar**: The inter-cellular lipid matrix composed of **50% Ceramides**, **25% Cholesterol**, and **15% Free Fatty Acids**.

When the lipid mortar is stripped by over-cleansing or harsh acids, microscopic fissures open, allowing hydration to evaporate while bacteria penetrate.

## The 3:1:1 Golden Ratio: Ceramides, Cholesterol, Fatty Acids
Clinical research shows that barrier restoration is accelerated when formulations mirror the physiological lipid ratio:
1. **Ceramides (3 Parts)**: Sphingolipid molecules that cement skin cells together and retain water.
2. **Cholesterol (1 Part)**: Stabilizes membrane fluidity, preventing dryness in cold weather.
3. **Free Fatty Acids (1 Part)**: Maintain an optimal acidic skin mantle (pH 4.5 – 5.5) which inhibits bacterial colonization.

## Warning Signs of a Compromised Barrier
- Stinging or burning sensation when applying gentle moisturizers.
- Flaky, crepey texture despite applying facial oils.
- Sudden onset of redness, micro-bumps, or heightened sensitivity.
- Excessive oil production as the skin attempts to compensate for internal dehydration.

## The 72-Hour Barrier Reset Protocol
If your skin barrier is stinging, strip your routine back immediately:
1. **Morning**: Splash with lukewarm water only. Apply a generous layer of a ceramide-rich cream (*CeraVe Moisturizing Cream* or *LANEIGE Water Bank*), followed by a gentle mineral sunscreen.
2. **Evening**: Cleanse once with a non-foaming hydrating milk cleanser. Mist with Centella Asiatica toner. Seal with a lipid balm containing squalane and panthenol.
3. **Avoid**: All AHA/BHA exfoliants, pure vitamin C, retinoids, physical scrubs, and essential oils for at least 7 to 10 days until skin calm is fully restored.
"""
    },
    {
        "id": 10,
        "slug": "korean-glass-skin-ritual-step-by-step",
        "title": "The Authentic Korean 7-Skin Ritual for Luminous Glass Complexion",
        "subtitle": "How layering lightweight hydrating toners and fermented essences builds deep moisture reservoirs without heaviness.",
        "category": "Skincare Tips",
        "read_time": "5 min read",
        "views_count": "19.4K views",
        "author_name": "Elena Rostova",
        "author_role": "Luméa Senior Esthetician",
        "author_avatar": "/images/avatar-sreynich.jpg",
        "published_at": "Oct 15, 2025",
        "hero_image": "/images/article-thumb-routine.jpg",
        "thumbnail": "/images/article-thumb-routine.jpg",
        "excerpt": "Glass skin isn't created by piling on heavy creams; it is cultivated through micro-layers of pure hydration. Here is the step-by-step method practiced in Seoul ateliers.",
        "is_featured": False,
        "is_popular": True,
        "popular_rank": 4,
        "toc": [
            {"id": "what-is-7-skin", "title": "What Exactly is the 7-Skin Method?"},
            {"id": "picking-toner", "title": "Selecting the Right Toner"},
            {"id": "step-by-step", "title": "Step-by-Step Application Protocol"},
            {"id": "frequency", "title": "How Often Should You Practice It?"}
        ],
        "content": """
In Korean skincare, the word *'Skin'* (스킨) translates directly to hydrating toner. The viral **7-Skin Method** involves applying seven thin, successive layers of a hydrating toner or essence to thoroughly hydrate the skin's deeper strata.

## What Exactly is the 7-Skin Method?
Rather than applying one thick layer of lotion that sits on the skin surface, patting seven whisper-light coats of watery essence creates capillary absorption. Each layer draws water into the next, plumping skin cells and creating an authentic translucent glass reflection.

## Selecting the Right Toner
**Critical Rule**: You cannot use an astringent, exfoliating, or alcohol-based toner for this technique. Look for:
- Fermented botanicals like Pitera™ or Bifida Ferment.
- Heartleaf (Houttuynia Cordata) to soothe inflammation (*Anua 77% Toner*).
- Deep sea mineral water and hyaluronic acid (*Round Lab 1025 Dokdo Toner*).
- Zero synthetic fragrance, alcohol denat, or essential oils.

## Step-by-Step Application Protocol
1. **Cleanse**: Start with a clean face using a gentle, pH-balanced cleanser.
2. **Layer 1**: Pour 3 to 4 drops into the palms of clean hands. Gently press into the skin starting from the cheeks, forehead, and neck.
3. **Layers 2 through 4**: While the skin is still slightly damp, repeat the pressing motion. Do not rub; pat gently with fingertips to stimulate lymphatic microcirculation.
4. **Layers 5 through 7**: Focus on areas prone to dryness like cheeks and under-eye contours.
5. **Seal**: Finish with a pea-sized amount of lightweight gel-cream (*Torriden DIVE-IN* or *COSRX Snail Cream*) to trap the hydration within the epidermal matrix.
"""
    },
    {
        "id": 11,
        "slug": "retinol-vs-bakuchiol-gentle-anti-aging-alternatives",
        "title": "Retinol vs. Bakuchiol: How to Choose the Right Collagen-Boosting Molecule",
        "subtitle": "Comparing cellular turnover, sensitivity profiles, and clinical efficacy for fine lines, firmness, and skin elasticity.",
        "category": "Anti-Aging",
        "read_time": "8 min read",
        "views_count": "11.5K views",
        "author_name": "Dr. Hemi Park",
        "author_role": "Board-Certified Dermatologist",
        "author_avatar": "/images/avatar-sreynich.jpg",
        "published_at": "Oct 16, 2025",
        "hero_image": "/images/article-thumb-niacinamide.jpg",
        "thumbnail": "/images/article-thumb-niacinamide.jpg",
        "excerpt": "Retinol has long been the gold standard in cellular longevity, but Bakuchiol has emerged as a plant-derived competitor. Here is what dermatological trials reveal.",
        "is_featured": False,
        "is_popular": False,
        "popular_rank": None,
        "toc": [
            {"id": "how-retinol-works", "title": "How Retinoids Accelerate Cellular Renewal"},
            {"id": "what-is-bakuchiol", "title": "What is Bakuchiol?"},
            {"id": "clinical-trials", "title": "What Head-to-Head Clinical Trials Reveal"},
            {"id": "how-to-start", "title": "How to Integrate Actives Safely"}
        ],
        "content": """
When it comes to addressing fine lines, loss of collagen, and irregular texture, retinoids remain one of the few ingredients with decades of peer-reviewed clinical proof. However, retinol irritation is real. Enter Bakuchiol.

## How Retinoids Accelerate Cellular Renewal
Retinol is a derivative of Vitamin A. Once converted inside the skin to retinoic acid, it binds to cellular retinoic acid receptors (RARs) in skin cells. This signals the skin to:
- Accelerate epidermal turnover from 40+ days back to a youthful 28-day cycle.
- Stimulate fibroblasts to synthesize new Type I and Type III collagen.
- Inhibit matrix metalloproteinases (MMPs)—enzymes that degrade existing collagen when exposed to sunlight.

## What is Bakuchiol?
Bakuchiol is a pure meroterpene phenol extracted from the seeds and leaves of the *Psoralea corylifolia* (Babchi) plant. While chemically distinct from Vitamin A, functional gene expression studies show Bakuchiol modulates many of the same cellular pathways as retinol without triggering retinoic acid dermatitis.

## What Head-to-Head Clinical Trials Reveal
A landmark 12-week double-blind clinical study published in the *British Journal of Dermatology* evaluated 0.5% Retinol versus 0.5% Bakuchiol:
- **Wrinkle Reduction**: Both groups demonstrated statistically significant, equivalent reductions in wrinkle depth and surface area.
- **Hyperpigmentation**: Both groups showed comparable fading of solar lentigines.
- **Tolerance**: The Bakuchiol group experienced significantly less flaking, burning, and stinging compared to the retinol group.

## How to Integrate Actives Safely
- If you have **reactive, rosacea-prone skin, or are pregnant/nursing**: **Bakuchiol** is the superior, safe botanical choice. It can even be used in the morning under sunscreen.
- If you seek **maximum potency for deep wrinkles or stubborn acne**: Choose micro-encapsulated **Retinol**, starting at 0.2% twice weekly using the *sandwich method* (moisturizer, retinol, moisturizer).
"""
    }
]

def run_expansion():
    db = SessionLocal()
    try:
        print("[Expansion] Connecting to Luméa database...")

        # 1. Ensure Brand records exist for new products
        brands_to_add = [
            {"name": "Round Lab", "slug": "round-lab", "country": "South Korea", "country_code": "KR", "tagline": "Pure Korean Island Seawater & Birch Sap"},
            {"name": "Sulwhasoo", "slug": "sulwhasoo", "country": "South Korea", "country_code": "KR", "tagline": "Holistic Korean Herbal Medicine Prestige"},
            {"name": "Torriden", "slug": "torriden", "country": "South Korea", "country_code": "KR", "tagline": "Low Molecular 5D Hyaluronic Acid Specialists"},
            {"name": "Luméa Atelier", "slug": "lumea-atelier", "country": "France", "country_code": "FR", "tagline": "Curated Clean Luxury Dermatological Formulations"},
            {"name": "Beauty of Joseon", "slug": "beauty-of-joseon", "country": "South Korea", "country_code": "KR", "tagline": "Hanbang Herbal Wisdom for Radiant Skin"},
            {"name": "SK-II", "slug": "sk-ii", "country": "Japan", "country_code": "JP", "tagline": "Iconic PITERA™ Ferment Science"},
            {"name": "LANEIGE", "slug": "laneige", "country": "South Korea", "country_code": "KR", "tagline": "Water Bank Moisture Barrier Innovation"},
        ]
        
        for b in brands_to_add:
            existing = db.query(Brand).filter((Brand.name == b["name"]) | (Brand.slug == b["slug"])).first()
            if not existing:
                new_brand = Brand(
                    name=b["name"],
                    slug=b["slug"],
                    tagline=b["tagline"],
                    country=b["country"],
                    country_code=b["country_code"],
                    description=f"{b['name']} is an internationally acclaimed skincare atelier brand, celebrated for clinical efficacy and pure botanical formulations.",
                    is_featured=True,
                    is_active=True
                )
                db.add(new_brand)
        db.commit()
        print("[Expansion] Brands verified and updated.")

        # 2. Add New Products
        added_prods = 0
        for p_data in NEW_PRODUCTS:
            existing_prod = db.query(Product).filter((Product.slug == p_data["slug"]) | (Product.id == p_data["id"])).first()
            if not existing_prod:
                prod = Product(
                    id=p_data["id"],
                    category_id=p_data["category_id"],
                    name=p_data["name"],
                    brand=p_data["brand"],
                    slug=p_data["slug"],
                    category=p_data["category"],
                    category_name=p_data["category_name"],
                    subcategory=p_data["subcategory"],
                    product_type=p_data["product_type"],
                    price=p_data["price"],
                    compare_at_price=p_data["compare_at_price"],
                    rating=p_data["rating"],
                    reviews=p_data["reviews"],
                    badge=p_data["badge"],
                    badge_type=p_data["badge_type"],
                    stock=p_data["stock"],
                    image_url=p_data["image_url"],
                    description=p_data["description"],
                    is_featured=p_data["is_featured"],
                    skin_type=p_data["skin_type"],
                    skin_concern=p_data["skin_concern"],
                    gallery=p_data["gallery"]
                )
                db.add(prod)
                added_prods += 1
            else:
                # Update existing
                existing_prod.image_url = p_data["image_url"]
                existing_prod.description = p_data["description"]
                existing_prod.price = p_data["price"]
                existing_prod.compare_at_price = p_data["compare_at_price"]
        db.commit()
        print(f"[Expansion] Successfully added {added_prods} new products! (Total products in DB: {db.query(Product).count()})")

        # 3. Add New Articles
        added_arts = 0
        for a_data in NEW_ARTICLES:
            existing_art = db.query(Article).filter((Article.slug == a_data["slug"]) | (Article.id == a_data["id"])).first()
            if not existing_art:
                art = Article(
                    id=a_data["id"],
                    slug=a_data["slug"],
                    title=a_data["title"],
                    subtitle=a_data["subtitle"],
                    category=a_data["category"],
                    read_time=a_data["read_time"],
                    views_count=a_data["views_count"],
                    author_name=a_data["author_name"],
                    author_role=a_data["author_role"],
                    author_avatar=a_data["author_avatar"],
                    published_at=a_data["published_at"],
                    hero_image=a_data["hero_image"],
                    thumbnail=a_data["thumbnail"],
                    excerpt=a_data["excerpt"],
                    toc=a_data["toc"],
                    content=a_data["content"],
                    is_featured=a_data["is_featured"],
                    is_popular=a_data["is_popular"],
                    popular_rank=a_data["popular_rank"]
                )
                db.add(art)
                added_arts += 1
            else:
                existing_art.content = a_data["content"]
                existing_art.hero_image = a_data["hero_image"]
                existing_art.thumbnail = a_data["thumbnail"]
                existing_art.toc = a_data["toc"]
        db.commit()
        print(f"[Expansion] Successfully added {added_arts} new articles! (Total articles in DB: {db.query(Article).count()})")

    except Exception as e:
        db.rollback()
        print(f"[Error] Expansion failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_expansion()
