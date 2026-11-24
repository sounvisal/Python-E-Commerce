# LUMÉA E-Commerce Evaluation Datasets

This directory contains the canonical evaluation datasets and fixture schemas for the Luméa Contemporary Skincare & Beauty Atelier platform.

---

## 📁 Datasets Overview

| File | Description | Primary Entities | Record Count |
| :--- | :--- | :--- | :--- |
| [`catalog_products.json`](catalog_products.json) | Curated catalog items, categories, brands, clientele accounts, reviews, and diagnostics. | Products, Categories, Brands, Users, Reviews, Quizzes | 100+ Catalog Items, 11 Categories, 15 Brands, 50 Clients |
| [`store_settings.json`](store_settings.json) | Atelier operational settings, free shipping thresholds, tax rates, contact channels, and currency settings. | Store Configuration, Logistics, Policies | 1 Operational Store Profile |

---

## 📊 Entity Schemas

### 1. Products (`catalog_products.json` -> `products`)
Each product record includes dermatological attributes, pricing, stock levels, and formulation specifications:
```json
{
  "id": 101,
  "name": "Facial Treatment Essence",
  "brand": "SK-II",
  "category": "serums",
  "category_name": "Serums & Essences",
  "price": 99.00,
  "compare_at_price": 142.00,
  "stock": 25,
  "rating": 4.9,
  "reviews_count": 128,
  "is_featured": true,
  "is_bestseller": true,
  "is_new": false,
  "slug": "sk-ii-facial-treatment-essence",
  "image_url": "/images/prod-sk2.jpg",
  "texture_video_url": "/videos/reel-sk2-texture.mp4",
  "skin_type": ["Dry", "Combination", "Normal"],
  "skin_concern": ["Dullness", "Texture", "Aging"],
  "ingredients": ["Pitera (Galactomyces Ferment Filtrate)", "Butylene Glycol", "Water"],
  "description": "SK-II signature essence powered by over 90% Pitera...",
  "volume": "160ml / 5.4 fl. oz."
}
```

### 2. Categories (`catalog_products.json` -> `categories`)
11 curated dermatological categories covering cleansers, toners, serums, moisturizers, eye creams, sunscreens, face masks, treatments, body care, lip care, and curated discovery kits.

### 3. Brands (`catalog_products.json` -> `brands`)
Top Asian & international luxury skincare laboratories with country of origin, philosophy, and flagship banner assets (e.g. SK-II, Beauty of Joseon, Laneige, Cosrx, CeraVe, Sulwhasoo, The Ordinary, La Roche-Posay).

### 4. Clientele Accounts (`catalog_products.json` -> `users`)
Pre-configured user accounts with distinct membership tiers (Gold, Silver, Bronze), reward balances, skin diagnostic profiles, and order history for university grading and evaluation.

### 5. Skin Diagnostic Quizzes (`catalog_products.json` -> `quizzes`)
5-step dermatological diagnostic tree mapping skin hydration, barrier sensitivity, sebum activity, lifestyle factors, and goals to personalized morning and evening routine recommendations.

---

## 🔄 Automated Database Seeding

The SQLite / PostgreSQL database automatically ingests and validates this dataset on initial startup via:
```python
# python-backend/app/seed/seed_data.py
from app.seed.seed_data import seed_database
seed_database(db)
```
Seeding is **strictly idempotent**: it verifies existing records before inserting to preserve customer transactions and order audit trails.
