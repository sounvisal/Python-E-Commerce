import axios from 'axios'
import { defineStore } from 'pinia'

const API_BASE = '/api'

// Comprehensive fallback skincare catalog matching Luméa reference wireframes
const FALLBACK_CATEGORIES = [
  { id: 1, name: 'Cleansers', slug: 'cleansers', count: 234, icon: 'Sparkles', desc: 'The first step to healthy, radiant skin. Remove impurities, excess oil, and makeup while keeping your skin balanced and refreshed.' },
  { id: 2, name: 'Toners', slug: 'toners', count: 112, icon: 'Droplets', desc: 'Hydrating, balancing and soothing liquid elixirs that prep skin for optimal nutrient absorption.' },
  { id: 3, name: 'Serums', slug: 'serums', count: 342, icon: 'Flame', desc: 'High-potency active formulations targeting fine lines, hyperpigmentation, hydration, and glow.' },
  { id: 4, name: 'Moisturizers', slug: 'moisturizers', count: 298, icon: 'Shield', desc: 'Rich barrier-replenishing creams and weightless lotions that seal in essential moisture.' },
  { id: 5, name: 'Sunscreens', slug: 'sunscreens', count: 166, icon: 'Sun', desc: 'Broad-spectrum UVA/UVB mineral and chemical sun shields that protect without white cast.' },
  { id: 6, name: 'Masks', slug: 'masks', count: 87, icon: 'Smile', desc: 'Deep-acting wash-off, overnight, and bio-cellulose sheet treatments for intensive replenishment.' },
  { id: 7, name: 'Treatments', slug: 'treatments', count: 121, icon: 'Zap', desc: 'Targeted clinical exfoliants, clarifying peel pads, and corrective spot formulations.' },
  { id: 8, name: 'Kits & Sets', slug: 'kits', count: 98, icon: 'Gift', desc: 'Curated routine rituals and starter discovery bundles for yourself or someone special.' },
]

const FALLBACK_PRODUCTS = [
  // --- FEATURED IN SHOP ALL PRODUCTS (Matches Shop All Products.png) ---
  {
    id: 201,
    name: 'Facial Treatment Essence',
    brand: 'SK-II',
    category: 'toners',
    category_name: 'Toners',
    subcategory: 'Essence',
    product_type: 'Essence',
    price: 99.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 1200,
    badge: 'Best Seller',
    badge_type: 'bestseller',
    skin_type: ['Normal', 'Dry', 'Combination', 'Sensitive'],
    skin_concern: ['Dullness', 'Uneven Texture', 'Aging'],
    stock: 25,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence',
    is_featured: true,
  },
  {
    id: 202,
    name: 'Niacinamide 10% + Zinc 1%',
    brand: 'The Ordinary',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Clarifying Serum',
    product_type: 'Serum',
    price: 8.90,
    compare_at_price: 11.00,
    rating: 4.7,
    reviews: 980,
    badge: '20% OFF',
    badge_type: 'sale',
    skin_type: ['Oily', 'Combination', 'Normal'],
    skin_concern: ['Acne & Blemishes', 'Oiliness', 'Uneven Texture'],
    stock: 80,
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1',
    is_featured: true,
  },
  {
    id: 203,
    name: 'Lip Sleeping Mask',
    brand: 'LANEIGE',
    category: 'masks',
    category_name: 'Masks',
    subcategory: 'Lip Treatment',
    product_type: 'Lip Mask',
    price: 24.00,
    compare_at_price: null,
    rating: 4.9,
    reviews: 2100,
    badge: null,
    skin_type: ['Dry', 'Normal', 'Sensitive'],
    skin_concern: ['Dryness'],
    stock: 45,
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask',
    is_featured: true,
  },
  {
    id: 204,
    name: 'Moisturizing Cream',
    brand: 'CeraVe',
    category: 'moisturizers',
    category_name: 'Moisturizers',
    subcategory: 'Barrier Cream',
    product_type: 'Cream',
    price: 24.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 1500,
    badge: null,
    skin_type: ['Dry', 'Sensitive', 'Normal'],
    skin_concern: ['Dryness', 'Sensitivity'],
    stock: 55,
    image_url: '/images/prod-cerave.jpg',
    slug: 'cerave-moisturizing-cream',
    is_featured: true,
  },
  {
    id: 205,
    name: 'Effaclar Duo+ Anti-Imperfections',
    brand: 'La Roche-Posay',
    category: 'treatments',
    category_name: 'Treatments',
    subcategory: 'Spot Treatment',
    product_type: 'Cream',
    price: 22.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: 892,
    badge: null,
    skin_type: ['Oily', 'Combination'],
    skin_concern: ['Acne & Blemishes', 'Dark Spots'],
    stock: 32,
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-effaclar-duo',
    is_featured: true,
  },
  {
    id: 206,
    name: 'Advanced Snail 96 Mucin Power Essence',
    brand: 'COSRX',
    category: 'toners',
    category_name: 'Toners',
    subcategory: 'Essence',
    product_type: 'Essence',
    price: 25.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 1800,
    badge: null,
    skin_type: ['All Skin Types', 'Dry', 'Sensitive'],
    skin_concern: ['Dryness', 'Uneven Texture', 'Dullness'],
    stock: 40,
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-advanced-snail-96-mucin-essence',
    is_featured: true,
  },
  {
    id: 107,
    name: 'Sensibio H2O Micellar Water',
    brand: 'BIODERMA',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Micellar Water',
    product_type: 'Micellar Water',
    price: 18.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 1100,
    badge: null,
    skin_type: ['Sensitive', 'Normal', 'Dry'],
    skin_concern: ['Sensitivity', 'Redness'],
    stock: 40,
    image_url: '/images/prod-bioderma-micellar.jpg',
    slug: 'bioderma-sensibio-h2o-micellar-water',
    is_featured: true,
  },
  {
    id: 208,
    name: 'Green Tea Seed Hyaluronic Serum',
    brand: 'innisfree',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Hydrating Serum',
    product_type: 'Serum',
    price: 28.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 934,
    badge: null,
    skin_type: ['Dry', 'Combination', 'Normal'],
    skin_concern: ['Dryness', 'Dullness'],
    stock: 25,
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum',
    is_featured: true,
  },
  {
    id: 209,
    name: 'Heartleaf 77% Soothing Toner',
    brand: 'Anua',
    category: 'toners',
    category_name: 'Toners',
    subcategory: 'Soothing Toner',
    product_type: 'Toner',
    price: 26.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 2300,
    badge: 'New',
    badge_type: 'new',
    skin_type: ['Sensitive', 'Acne-Prone', 'Combination'],
    skin_concern: ['Sensitivity', 'Redness', 'Acne & Blemishes'],
    stock: 45,
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'anua-heartleaf-77-soothing-toner',
    is_featured: true,
  },
  {
    id: 210,
    name: 'Cicapair Tiger Grass Color Correcting Treatment',
    brand: 'Dr.Jart+',
    category: 'treatments',
    category_name: 'Treatments',
    subcategory: 'Color Corrector',
    product_type: 'Cream',
    price: 38.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 874,
    badge: 'Value Set',
    badge_type: 'value',
    skin_type: ['Sensitive', 'Normal', 'Combination'],
    skin_concern: ['Redness', 'Sensitivity', 'Uneven Texture'],
    stock: 20,
    image_url: '/images/prod-laneige.jpg',
    slug: 'dr-jart-cicapair-tiger-grass-treatment',
    is_featured: true,
  },
  {
    id: 211,
    name: 'AGE-R Booster Pro Cellular Glow Device',
    brand: 'Medicube',
    category: 'treatments',
    category_name: 'Treatments',
    subcategory: 'Beauty Device',
    product_type: 'Device',
    price: 179.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: 620,
    badge: null,
    skin_type: ['All Skin Types'],
    skin_concern: ['Aging', 'Dullness', 'Uneven Texture'],
    stock: 12,
    image_url: '/images/prod-sk2.jpg',
    slug: 'medicube-age-r-booster-pro',
    is_featured: true,
  },
  {
    id: 212,
    name: 'First Care Activating Serum VI',
    brand: 'Sulwhasoo',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Activating Serum',
    product_type: 'Serum',
    price: 89.00,
    compare_at_price: 105.00,
    rating: 4.9,
    reviews: 710,
    badge: '15% OFF',
    badge_type: 'sale',
    skin_type: ['Normal', 'Dry', 'Aging'],
    skin_concern: ['Aging', 'Dullness', 'Dryness'],
    stock: 16,
    image_url: '/images/prod-sulwhasoo.jpg',
    slug: 'sulwhasoo-first-care-activating-serum',
    is_featured: true,
  },

  // --- CLEANSER COLLECTION (Featured in Category Product Listing) ---
  {
    id: 101,
    name: 'Hydrating Facial Cleanser',
    brand: 'CeraVe',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Cream Cleanser',
    product_type: 'Cream',
    price: 16.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 12400,
    badge: 'Best Seller',
    badge_type: 'bestseller',
    skin_type: ['Dry', 'Normal', 'Sensitive'],
    skin_concern: ['Dryness', 'Sensitivity'],
    stock: 45,
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-hydrating-facial-cleanser',
    is_featured: true,
  },
  {
    id: 102,
    name: 'Effaclar Purifying Foaming Gel',
    brand: 'La Roche-Posay',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Gel Cleanser',
    product_type: 'Gel',
    price: 18.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 6200,
    badge: null,
    skin_type: ['Oily', 'Combination'],
    skin_concern: ['Acne & Blemishes', 'Oiliness'],
    stock: 28,
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-effaclar-purifying-foaming-gel',
    is_featured: true,
  },
  {
    id: 103,
    name: 'Facial Treatment Gentle Cleanser',
    brand: 'SK-II',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Cream Cleanser',
    product_type: 'Cream',
    price: 75.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 3100,
    badge: null,
    skin_type: ['Normal', 'Dry', 'Combination', 'Sensitive'],
    skin_concern: ['Dullness', 'Uneven Texture'],
    stock: 14,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-gentle-cleanser',
    is_featured: true,
  },
  {
    id: 104,
    name: 'Green Tea Amino Acid Cleansing Foam',
    brand: 'innisfree',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Foam Cleanser',
    product_type: 'Foam',
    price: 14.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: 1200,
    badge: 'New',
    badge_type: 'new',
    skin_type: ['Combination', 'Normal'],
    skin_concern: ['Dryness', 'Dullness'],
    stock: 35,
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-amino-acid-cleansing-foam',
    is_featured: true,
  },
  {
    id: 105,
    name: 'Squalane Cleanser',
    brand: 'The Ordinary',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Cleansing Balm',
    product_type: 'Balm',
    price: 10.40,
    compare_at_price: 13.00,
    rating: 4.5,
    reviews: 980,
    badge: '20% OFF',
    badge_type: 'sale',
    skin_type: ['Normal', 'Dry', 'Sensitive'],
    skin_concern: ['Dryness', 'Sensitivity'],
    stock: 60,
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-squalane-cleanser',
    is_featured: true,
  },
  {
    id: 106,
    name: 'Low pH Good Morning Gel Cleanser',
    brand: 'COSRX',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Gel Cleanser',
    product_type: 'Gel',
    price: 14.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 8700,
    badge: null,
    skin_type: ['Oily', 'Sensitive', 'Combination'],
    skin_concern: ['Acne & Blemishes', 'Sensitivity'],
    stock: 50,
    image_url: '/images/prod-cosrx-cleanser.jpg',
    slug: 'cosrx-low-ph-good-morning-gel-cleanser',
    is_featured: true,
  },
  {
    id: 108,
    name: 'Cream Skin Milk Cleanser',
    brand: 'LANEIGE',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Cream Cleanser',
    product_type: 'Cream',
    price: 24.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: 1900,
    badge: null,
    skin_type: ['Dry', 'Normal', 'Sensitive'],
    skin_concern: ['Dryness', 'Dullness'],
    stock: 22,
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-cream-skin-milk-cleanser',
    is_featured: true,
  },
  {
    id: 109,
    name: 'Heartleaf Quercetinol Pore Deep Cleansing Foam',
    brand: 'Anua',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Foam Cleanser',
    product_type: 'Foam',
    price: 16.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 2800,
    badge: null,
    skin_type: ['Oily', 'Combination'],
    skin_concern: ['Acne & Blemishes', 'Oiliness', 'Uneven Texture'],
    stock: 30,
    image_url: '/images/prod-anua-cleanser.jpg',
    slug: 'anua-heartleaf-quercetinol-pore-deep-cleansing-foam',
    is_featured: true,
  },
  {
    id: 110,
    name: 'Special Cleansing Gel',
    brand: 'Dermalogica',
    category: 'cleansers',
    category_name: 'Cleansers',
    subcategory: 'Gel Cleanser',
    product_type: 'Gel',
    price: 38.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 1500,
    badge: 'Value Set',
    badge_type: 'value',
    skin_type: ['Normal', 'Combination', 'Oily'],
    skin_concern: ['Oiliness', 'Uneven Texture'],
    stock: 18,
    image_url: '/images/prod-dermalogica.jpg',
    slug: 'dermalogica-special-cleansing-gel',
    is_featured: true,
  },
  {
    id: 213,
    name: 'Relief Sun: Rice + Probiotics SPF 50+',
    brand: 'Beauty of Joseon',
    category: 'sunscreens',
    category_name: 'Sunscreens',
    subcategory: 'Daily SPF',
    product_type: 'Sunscreen',
    price: 22.00,
    compare_at_price: null,
    rating: 4.9,
    reviews: 1900,
    badge: 'Best Seller',
    badge_type: 'bestseller',
    skin_type: ['Dry', 'Sensitive', 'Normal', 'Combination'],
    skin_concern: ['Sensitivity', 'Dullness'],
    stock: 75,
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-relief-sun-spf50',
    is_featured: true,
  },
  // Additional SK-II Brand Store Lineup
  {
    id: 214,
    name: 'Skinpower Advanced Cream',
    brand: 'SK-II',
    category: 'moisturizers',
    category_name: 'Moisturizers',
    subcategory: 'Firming Cream',
    product_type: 'Cream',
    price: 135.00,
    compare_at_price: 155.00,
    rating: 4.9,
    reviews: 840,
    badge: 'Best Seller',
    badge_type: 'bestseller',
    skin_type: ['Dry', 'Normal', 'Aging'],
    skin_concern: ['Aging', 'Dullness', 'Loss of Firmness'],
    stock: 22,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-skinpower-advanced-cream',
    is_featured: true,
  },
  {
    id: 215,
    name: 'GenOptics Ultraura Essence Serum',
    brand: 'SK-II',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Brightening Serum',
    product_type: 'Serum',
    price: 185.00,
    compare_at_price: null,
    rating: 4.9,
    reviews: 620,
    badge: 'Award Winner',
    badge_type: 'value',
    skin_type: ['All Skin Types', 'Dull'],
    skin_concern: ['Dullness', 'Dark Spots', 'Uneven Texture'],
    stock: 18,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-genoptics-ultraura-essence',
    is_featured: true,
  },
  {
    id: 216,
    name: 'Facial Treatment Clear Lotion Toner',
    brand: 'SK-II',
    category: 'toners',
    category_name: 'Toners',
    subcategory: 'Clarifying Toner',
    product_type: 'Toner',
    price: 80.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: 780,
    badge: null,
    skin_type: ['All Skin Types'],
    skin_concern: ['Uneven Texture', 'Pores'],
    stock: 30,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-clear-lotion',
    is_featured: false,
  },
  {
    id: 217,
    name: 'Overnight Miracle Capsule Mask (6-Pack)',
    brand: 'SK-II',
    category: 'masks',
    category_name: 'Masks',
    subcategory: 'Sleeping Mask',
    product_type: 'Mask',
    price: 110.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 430,
    badge: 'Limited Edition',
    badge_type: 'new',
    skin_type: ['All Skin Types', 'Tired Skin'],
    skin_concern: ['Dullness', 'Dryness'],
    stock: 15,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-overnight-miracle-mask',
    is_featured: false,
  },
  // Additional Niacinamide Search Results Lineup
  {
    id: 218,
    name: 'Pure Niacinamide 10 Serum',
    brand: 'La Roche-Posay',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Clarifying Serum',
    product_type: 'Serum',
    price: 39.99,
    compare_at_price: 45.00,
    rating: 4.7,
    reviews: 812,
    badge: 'Editor Pick',
    badge_type: 'value',
    skin_type: ['Sensitive', 'Normal', 'Combination'],
    skin_concern: ['Dark Spots', 'Uneven Texture', 'Sensitivity'],
    stock: 28,
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-pure-niacinamide-10',
    is_featured: true,
  },
  {
    id: 219,
    name: 'Niacinamide 10% + TXA 4% Dark Spot Correcting Serum',
    brand: 'Anua',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Correcting Serum',
    product_type: 'Serum',
    price: 24.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 1450,
    badge: 'Trending',
    badge_type: 'bestseller',
    skin_type: ['All Skin Types', 'Sensitive'],
    skin_concern: ['Dark Spots', 'Hyperpigmentation', 'Dullness'],
    stock: 40,
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'anua-niacinamide-10-txa-4-serum',
    is_featured: true,
  },
  {
    id: 220,
    name: 'Glow Serum: Propolis + Niacinamide',
    brand: 'Beauty of Joseon',
    category: 'serums',
    category_name: 'Serums',
    subcategory: 'Glow Serum',
    product_type: 'Serum',
    price: 17.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: 2400,
    badge: 'Best Seller',
    badge_type: 'bestseller',
    skin_type: ['Acne-Prone', 'Normal', 'Combination'],
    skin_concern: ['Acne & Blemishes', 'Pores', 'Dullness'],
    stock: 65,
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-glow-serum-propolis-niacinamide',
    is_featured: true,
  },
  {
    id: 221,
    name: 'PM Facial Moisturizing Lotion with Niacinamide',
    brand: 'CeraVe',
    category: 'moisturizers',
    category_name: 'Moisturizers',
    subcategory: 'Night Lotion',
    product_type: 'Lotion',
    price: 19.99,
    compare_at_price: null,
    rating: 4.7,
    reviews: 3200,
    badge: null,
    skin_type: ['All Skin Types', 'Sensitive'],
    skin_concern: ['Dryness', 'Barrier Repair'],
    stock: 50,
    image_url: '/images/prod-cerave.jpg',
    slug: 'cerave-pm-facial-moisturizing-lotion',
    is_featured: true,
  },
]

export const BRANDS_DIRECTORY = [
  // Row 1
  { id: 1, name: 'SK-II', slug: 'sk-ii', origin: 'Japan', founded: 1980, count: 42, featured: true, hero_tagline: 'Timeless Beauty Through Science.', desc: 'Renowned Japanese luxury skincare crafted around PITERA™, unlocking crystal clear skin.' },
  { id: 2, name: 'The Ordinary', slug: 'the-ordinary', origin: 'Canada', founded: 2013, count: 56, featured: true, hero_tagline: 'Clinical Formulations. Real Results.', desc: 'Clinical active skincare formulations with integrity and scientific transparency.' },
  { id: 3, name: 'CeraVe', slug: 'cerave', origin: 'United States', founded: 2005, count: 48, featured: true, hero_tagline: 'Dermatologist Recommended Ceramides', desc: 'Formulated with 3 essential ceramides to restore skin’s natural protective moisture barrier.' },
  { id: 4, name: 'LANEIGE', slug: 'laneige', origin: 'South Korea', founded: 1994, count: 36, featured: true, hero_tagline: 'Water Bank Hydration', desc: 'Pioneering hydration technology and iconic overnight water sleeping masks.' },
  { id: 5, name: 'Bioderma', slug: 'bioderma', origin: 'France', founded: 1977, count: 28, featured: false, hero_tagline: 'Biology at the Service of Dermatology', desc: 'Inventors of micellar cleansing technology preserving skin biology.' },
  { id: 6, name: 'La Roche-Posay', slug: 'la-roche-posay', origin: 'France', founded: 1975, count: 40, featured: true, hero_tagline: 'Thermal Spring Water Solutions', desc: 'Dermatologist-recommended clinical formulations for sensitive skin.' },
  // Row 2
  { id: 7, name: 'innisfree', slug: 'innisfree', origin: 'South Korea', founded: 2000, count: 52, featured: true, hero_tagline: 'Pure Ingredients from Nature.', desc: 'Pure organic green tea seed infusions and volcanic clusters sourced directly from Jeju Island.' },
  { id: 8, name: 'COSRX', slug: 'cosrx', origin: 'South Korea', founded: 2013, count: 46, featured: false, hero_tagline: 'Expecting Tomorrow', desc: 'Minimalist, high-potency formulations with snail mucin and gentle clarifying acids.' },
  { id: 9, name: 'Anua', slug: 'anua', origin: 'South Korea', founded: 2019, count: 38, featured: false, hero_tagline: 'Heartleaf Calming Rituals', desc: 'Skin-soothing Korean formulations powered by concentrated heartleaf and niacinamide.' },
  { id: 10, name: 'Beauty of Joseon', slug: 'beauty-of-joseon', origin: 'South Korea', founded: 2020, count: 34, featured: false, hero_tagline: 'Traditional Hanbang Wisdom', desc: 'Reinterpreting traditional Korean royal herbal remedies with rice and ginseng.' },
  { id: 11, name: 'Sulwhasoo', slug: 'sulwhasoo', origin: 'South Korea', founded: 1966, count: 30, featured: false, hero_tagline: 'Ginseng Heritage Science', desc: 'Prestige Korean herbal skincare formulated with precious ginseng saponins.' },
  { id: 12, name: 'Dr.Jart+', slug: 'dr-jart', origin: 'South Korea', founded: 2004, count: 28, featured: false, hero_tagline: 'Dermatological Science Meets Art', desc: 'High-performance barrier repair treatments including iconic Cicapair solutions.' },
  // Row 3
  { id: 13, name: 'medicube', slug: 'medicube', origin: 'South Korea', founded: 2016, count: 24, featured: false, hero_tagline: 'Clinical Dermocosmetics', desc: 'Targeted clinical skincare and beauty device innovations for pore refinement.' },
  { id: 14, name: 'Estée Lauder', slug: 'estee-lauder', origin: 'United States', founded: 1946, count: 45, featured: false, hero_tagline: 'Luxury Night Repair Science', desc: 'Legendary prestige skincare celebrated for Advanced Night Repair serum technology.' },
  { id: 15, name: 'Clinique', slug: 'clinique', origin: 'United States', founded: 1968, count: 32, featured: false, hero_tagline: 'Allergy Tested. 100% Fragrance Free.', desc: 'Dermatologist-developed custom skincare routines for healthy glowing skin.' },
  { id: 16, name: 'Kiehl\'s', slug: 'kiehls', origin: 'United States', founded: 1851, count: 28, featured: false, hero_tagline: 'Since 1851 New York Apothecary', desc: 'Heritage botanical apothecary formulas targeting barrier hydration and repair.' },
  { id: 17, name: 'Shiseido', slug: 'shiseido', origin: 'Japan', founded: 1872, count: 40, featured: false, hero_tagline: 'Ginza Tokyo Heritage', desc: 'Japanese cosmetic innovation blending cutting-edge cellular science with eastern philosophy.' },
  { id: 18, name: 'Neutrogena', slug: 'neutrogena', origin: 'United States', founded: 1930, count: 26, featured: false, hero_tagline: 'Dermatologist Recommended', desc: 'Accessible hydro-boost hyaluronic acid and retinol skincare essentials.' },
  // Row 4
  { id: 19, name: 'Avène', slug: 'avene', origin: 'France', founded: 1990, count: 24, featured: false, hero_tagline: 'Thermal Spring Water Care', desc: 'French thermal spring water formulations clinically proven to calm sensitive skin.' },
  { id: 20, name: 'Eucerin', slug: 'eucerin', origin: 'Germany', founded: 1900, count: 22, featured: false, hero_tagline: 'Medical Skincare Science', desc: 'Clinically proven dermocosmetics trusted by dermatologists for dry skin.' },
  { id: 21, name: 'Cetaphil', slug: 'cetaphil', origin: 'United States', founded: 1947, count: 28, featured: false, hero_tagline: 'Gentle Cleansing Science', desc: 'Gentle, non-irritating formulas designed for sensitive and vulnerable skin.' },
  { id: 22, name: 'numbuzin', slug: 'numbuzin', origin: 'South Korea', founded: 2019, count: 20, featured: false, hero_tagline: 'What\'s Your Number?', desc: 'Numbered skincare solutions targeting specific skin concerns with precision.' },
  { id: 23, name: 'TIRTIR', slug: 'tirtir', origin: 'South Korea', founded: 2019, count: 18, featured: false, hero_tagline: 'Ceramide Glow Essence', desc: 'Luminous K-beauty skincare formulations creating radiant glass skin.' },
  { id: 24, name: 'SOME BY MI', slug: 'some-by-mi', origin: 'South Korea', founded: 2017, count: 22, featured: false, hero_tagline: 'Miracle Cleanse Solutions', desc: 'Calming AHA/BHA/PHA and tea tree miracle care for clearer skin.' },
]


export const useProductStore = defineStore('products', {
  state: () => ({
    products: FALLBACK_PRODUCTS,
    allCatalogProducts: FALLBACK_PRODUCTS,
    categories: FALLBACK_CATEGORIES,
    featuredProducts: FALLBACK_PRODUCTS.slice(0, 5),
    currentProduct: null,
    relatedProducts: [],
    loading: false,
    error: null,
    pagination: {
      currentPage: 1,
      lastPage: 3,
      perPage: 12,
      total: FALLBACK_PRODUCTS.length,
    },
    brands: BRANDS_DIRECTORY,
    filters: {
      search: '',
      category: '',
      subcategory: '',
      brand: [],
      skinType: [],
      skinConcern: [],
      productType: [],
      minPrice: null,
      maxPrice: null,
      rating: null,
      sort: 'popular', // 'popular', 'best_match', 'newest', 'price_asc', 'price_desc'
    },
  }),

  getters: {
    filteredProducts: (state) => {
      let result = [...state.allCatalogProducts]

      // Search filter
      if (state.filters.search) {
        const q = state.filters.search.toLowerCase().trim()
        result = result.filter(
          (p) =>
            p.name.toLowerCase().includes(q) ||
            p.brand.toLowerCase().includes(q) ||
            p.category.toLowerCase().includes(q) ||
            (p.subcategory && p.subcategory.toLowerCase().includes(q))
        )
      }

      // Category filter
      if (state.filters.category) {
        result = result.filter((p) => p.category.toLowerCase() === state.filters.category.toLowerCase())
      }

      // Subcategory pill filter
      if (state.filters.subcategory) {
        result = result.filter((p) => p.subcategory.toLowerCase() === state.filters.subcategory.toLowerCase())
      }

      // Brand filter
      if (state.filters.brand && state.filters.brand.length > 0) {
        result = result.filter((p) => state.filters.brand.includes(p.brand))
      }

      // Skin Type filter
      if (state.filters.skinType && state.filters.skinType.length > 0) {
        result = result.filter((p) =>
          p.skin_type?.some((st) => state.filters.skinType.includes(st))
        )
      }

      // Skin Concern filter
      if (state.filters.skinConcern && state.filters.skinConcern.length > 0) {
        result = result.filter((p) =>
          p.skin_concern?.some((sc) => state.filters.skinConcern.includes(sc))
        )
      }

      // Product Type filter
      if (state.filters.productType && state.filters.productType.length > 0) {
        result = result.filter((p) => state.filters.productType.includes(p.product_type))
      }

      // Price filter
      if (state.filters.minPrice !== null && state.filters.minPrice !== '') {
        result = result.filter((p) => p.price >= Number(state.filters.minPrice))
      }
      if (state.filters.maxPrice !== null && state.filters.maxPrice !== '') {
        result = result.filter((p) => p.price <= Number(state.filters.maxPrice))
      }

      // Rating filter
      if (state.filters.rating !== null && state.filters.rating !== '') {
        result = result.filter((p) => p.rating >= Number(state.filters.rating))
      }

      // Sorting
      switch (state.filters.sort) {
        case 'price_asc':
          result.sort((a, b) => a.price - b.price)
          break
        case 'price_desc':
          result.sort((a, b) => b.price - a.price)
          break
        case 'rating':
          result.sort((a, b) => b.rating - a.rating)
          break
        case 'newest':
          result.sort((a, b) => (b.badge === 'New' ? 1 : 0) - (a.badge === 'New' ? 1 : 0))
          break
        case 'popular':
        default:
          result.sort((a, b) => b.reviews - a.reviews)
          break
      }

      return result
    },

    totalCount() {
      return this.filteredProducts.length
    },
  },

  actions: {
    async fetchCategories() {
      try {
        const res = await axios.get(`${API_BASE}/categories`)
        if (res.data?.data && res.data.data.length > 0) {
          this.categories = res.data.data
        }
      } catch (err) {
        // Fallback already assigned in state
      }
    },

    async fetchProducts(params = {}) {
      this.loading = true
      this.error = null

      try {
        const queryParams = {
          ...this.filters,
          ...params,
        }
        const res = await axios.get(`${API_BASE}/products`, { params: queryParams })
        if (res.data?.data && res.data.data.length > 0) {
          this.products = res.data.data
          this.loading = false
          return
        }
      } catch (err) {
        console.warn('Could not reach backend /products, falling back to local dataset')
      }
      this.products = this.filteredProducts
      this.loading = false
    },

    async fetchProductBySlug(slug) {
      this.loading = true
      this.error = null
      try {
        const res = await axios.get(`${API_BASE}/products/${slug}`)
        if (res.data?.data) {
          this.currentProduct = res.data.data
          this.relatedProducts = res.data.related || []
          return
        }
      } catch (err) {
        // Fallback
      }

      const match = this.allCatalogProducts.find((p) => p.slug === slug)
      this.currentProduct = match || this.allCatalogProducts[0]
      this.relatedProducts = this.allCatalogProducts
        .filter((p) => p.id !== this.currentProduct.id && p.category === this.currentProduct.category)
        .slice(0, 4)
      this.loading = false
    },

    setFilter(key, val) {
      this.filters[key] = val
      this.fetchProducts()
    },

    toggleBrand(brand) {
      const idx = this.filters.brand.indexOf(brand)
      if (idx > -1) {
        this.filters.brand.splice(idx, 1)
      } else {
        this.filters.brand.push(brand)
      }
      this.fetchProducts()
    },

    toggleSkinType(type) {
      const idx = this.filters.skinType.indexOf(type)
      if (idx > -1) {
        this.filters.skinType.splice(idx, 1)
      } else {
        this.filters.skinType.push(type)
      }
      this.fetchProducts()
    },

    toggleSkinConcern(concern) {
      const idx = this.filters.skinConcern.indexOf(concern)
      if (idx > -1) {
        this.filters.skinConcern.splice(idx, 1)
      } else {
        this.filters.skinConcern.push(concern)
      }
      this.fetchProducts()
    },

    toggleProductType(type) {
      const idx = this.filters.productType.indexOf(type)
      if (idx > -1) {
        this.filters.productType.splice(idx, 1)
      } else {
        this.filters.productType.push(type)
      }
      this.fetchProducts()
    },

    resetFilters() {
      this.filters = {
        search: '',
        category: '',
        subcategory: '',
        brand: [],
        skinType: [],
        skinConcern: [],
        productType: [],
        minPrice: null,
        maxPrice: null,
        rating: null,
        sort: 'popular',
      }
      this.fetchProducts()
    },
  },
})
