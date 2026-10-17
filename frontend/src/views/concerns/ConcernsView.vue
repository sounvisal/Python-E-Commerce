<template>
  <div class="concerns-page">
    <!-- Breadcrumbs matching Skin Concern-Skin Type.png -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <router-link to="/concerns" class="breadcrumb-link">Skin Concerns</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">{{ currentConcern.name }}</span>
      </nav>
    </div>

    <!-- Hero Banner matching Skin Concern-Skin Type.png -->
    <section class="container banner-container">
      <div class="concerns-hero-card">
        <div class="hero-left-content">
          <h1 class="hero-title">{{ currentConcern.name }}</h1>
          <h2 class="hero-tagline">{{ currentConcern.subtitle }}</h2>
          <p class="hero-desc">
            {{ currentConcern.desc }}
          </p>

          <!-- 4 Benefit Items in a Horizontal Row -->
          <div class="hero-benefits-row">
            <div class="benefit-item">
              <Leaf :size="18" class="benefit-icon" />
              <span class="benefit-text">{{ currentConcern.benefits[0] }}</span>
            </div>
            <div class="benefit-item">
              <ShieldCheck :size="18" class="benefit-icon" />
              <span class="benefit-text">{{ currentConcern.benefits[1] }}</span>
            </div>
            <div class="benefit-item">
              <Droplet :size="18" class="benefit-icon" />
              <span class="benefit-text">{{ currentConcern.benefits[2] }}</span>
            </div>
            <div class="benefit-item">
              <Sparkles :size="18" class="benefit-icon" />
              <span class="benefit-text">{{ currentConcern.benefits[3] }}</span>
            </div>
          </div>
        </div>

        <div class="hero-right-visual">
          <div class="hero-stage-wrap">
            <img
              src="/images/banners/banner-skin-concerns-clean.jpg"
              alt="Luméa Skin Concerns"
              class="hero-packshot-img"
            />
            <div class="hero-callout-oval">
              <span class="callout-text">Healthy<br />Skin<br />Happier<br />You.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Dual Horizontal Selector Bar: Explore Concerns & Explore Types matching format -->
    <section class="container dual-selector-container">
      <div class="dual-selector-bar">
        <!-- Left Section: Explore Skin Concerns -->
        <div class="selector-section-left">
          <div class="selector-section-label">
            <span>Explore<br />Skin Concerns</span>
            <ChevronRight :size="14" class="label-arrow" />
          </div>
          <div class="selector-items-scroll">
            <button
              v-for="concern in concernsList"
              :key="concern.id"
              class="chip-selector-btn"
              :class="{ active: activeConcernId === concern.id }"
              @click="activeConcernId = concern.id"
            >
              <div class="chip-circle-icon">
                <component :is="concern.icon" :size="18" />
              </div>
              <span class="chip-title">{{ concern.shortName }}</span>
            </button>
          </div>
        </div>

        <div class="selector-divider-vertical"></div>

        <!-- Right Section: Explore Skin Types -->
        <div class="selector-section-right">
          <div class="selector-section-label">
            <span>Explore<br />Skin Types</span>
            <ChevronRight :size="14" class="label-arrow" />
          </div>
          <div class="selector-items-scroll">
            <button
              v-for="type in typesList"
              :key="type.id"
              class="chip-selector-btn"
              :class="{ active: activeTypeId === type.id }"
              @click="activeTypeId = activeTypeId === type.id ? 'all' : type.id"
            >
              <div class="chip-circle-icon">
                <component :is="type.icon" :size="18" />
              </div>
              <span class="chip-title">{{ type.name }}</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 3-Column Layout: Left Filters + Center Catalog + Right Routine Guidance -->
    <section class="container catalog-section">
      <div class="concerns-3col-layout">
        <!-- LEFT FILTER SIDEBAR matching format -->
        <aside class="filters-sidebar">
          <div class="filters-panel">
            <div class="filters-header">
              <span class="filters-title">Filters</span>
              <button class="clear-all-link" @click="clearAllFilters">Clear All</button>
            </div>

            <!-- Brand Accordion with Search Input -->
            <div class="accordion-group">
              <div class="accordion-header">
                <span class="accordion-title">Brand</span>
                <ChevronUp :size="14" />
              </div>
              <div class="search-brands-box">
                <Search :size="13" class="search-brands-icon" />
                <input
                  type="text"
                  placeholder="Search brands..."
                  v-model="brandSearchQuery"
                  class="search-brands-input"
                />
              </div>
              <div class="checkbox-options-list">
                <label
                  v-for="b in filteredBrandList"
                  :key="b.name"
                  class="filter-checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="b.name"
                    v-model="selectedBrands"
                  />
                  <span class="checkbox-label">{{ b.name }} ({{ b.count }})</span>
                </label>
              </div>
            </div>

            <!-- Price Range Accordion with Dual Range -->
            <div class="accordion-group">
              <div class="accordion-header">
                <span class="accordion-title">Price Range</span>
                <ChevronUp :size="14" />
              </div>
              <div class="price-slider-wrap">
                <div class="slider-track-visual">
                  <div class="slider-fill-visual" :style="{ width: `${(maxPrice / 200) * 100}%` }"></div>
                </div>
                <input
                  type="range"
                  min="0"
                  max="200"
                  v-model.number="maxPrice"
                  class="price-range-native"
                />
                <div class="price-scale-labels">
                  <span>$0</span>
                  <span>$200+</span>
                </div>
                <div class="price-inputs-row">
                  <div class="price-input-box">
                    <span class="currency-sym">$</span>
                    <input type="number" v-model.number="minPrice" min="0" max="200" />
                  </div>
                  <span class="price-sep">-</span>
                  <div class="price-input-box">
                    <span class="currency-sym">$</span>
                    <input type="number" v-model.number="maxPrice" min="0" max="200" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Product Type Accordion -->
            <div class="accordion-group">
              <div class="accordion-header">
                <span class="accordion-title">Product Type</span>
                <ChevronUp :size="14" />
              </div>
              <div class="checkbox-options-list">
                <label
                  v-for="pt in productTypesList"
                  :key="pt.name"
                  class="filter-checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="pt.slug"
                    v-model="selectedCategories"
                  />
                  <span class="checkbox-label">{{ pt.name }} ({{ pt.count }})</span>
                </label>
              </div>
            </div>

            <!-- Key Ingredients Accordion -->
            <div class="accordion-group">
              <div class="accordion-header">
                <span class="accordion-title">Key Ingredients</span>
                <ChevronUp :size="14" />
              </div>
              <div class="checkbox-options-list">
                <label
                  v-for="ing in keyIngredientsList"
                  :key="ing.name"
                  class="filter-checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="ing.name"
                    v-model="selectedIngredients"
                  />
                  <span class="checkbox-label">{{ ing.name }} ({{ ing.count }})</span>
                </label>
              </div>
            </div>
          </div>
        </aside>

        <!-- CENTER CATALOG GRID matching format -->
        <main class="catalog-main-area">
          <div class="catalog-toolbar-row">
            <span class="products-total-count">
              {{ filteredProducts.length }} products for {{ currentConcern.name }}
            </span>

            <div class="toolbar-controls-right">
              <div class="sort-dropdown-wrap">
                <span class="sort-by-lbl">Sort by:</span>
                <select v-model="sortBy" class="format-sort-select">
                  <option value="bestselling">Best Selling</option>
                  <option value="rating">Top Rated</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                  <option value="newest">Newest First</option>
                </select>
              </div>
              <div class="view-mode-toggle">
                <button
                  class="view-toggle-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  aria-label="Grid view"
                >
                  <LayoutGrid :size="15" />
                </button>
                <button
                  class="view-toggle-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  aria-label="List view"
                >
                  <List :size="15" />
                </button>
              </div>
            </div>
          </div>

          <!-- Product Grid: 4 Columns using standardized ProductCard matching HomeView -->
          <div class="concerns-products-grid">
            <div
              v-for="(product, idx) in paginatedProducts"
              :key="product.id"
              class="concern-card-stagger-item"
              :style="{ animationDelay: `${idx * 50}ms` }"
            >
              <ProductCard :product="product" />
            </div>
          </div>

          <!-- Pagination matching Skin Concern-Skin Type.png -->
          <div class="pagination-bar">
            <button class="page-nav-btn" :disabled="currentPage === 1" @click="currentPage--">&lt;</button>
            <button
              v-for="p in totalPages"
              :key="p"
              class="page-num-btn"
              :class="{ active: currentPage === p }"
              @click="currentPage = p"
            >
              {{ p }}
            </button>
            <span v-if="totalPages > 5" class="page-ellipsis">...</span>
            <button v-if="totalPages > 5" class="page-num-btn" @click="currentPage = 11">11</button>
            <button class="page-nav-btn" :disabled="currentPage === totalPages" @click="currentPage++">&gt;</button>
          </div>
        </main>

        <!-- RIGHT SIDEBAR: Recommended Routine, Key Ingredients, Expert Tips matching format -->
        <aside class="routine-editorial-sidebar">
          <!-- Card 1: Recommended Routine Sequence -->
          <div class="editorial-card routine-card">
            <div class="editorial-card-header">
              <h3 class="editorial-card-title">Recommended Routine<br />For {{ currentConcern.name }}</h3>
              <router-link to="/shop" class="header-link-red">
                View Full Routine &rarr;
              </router-link>
            </div>

            <!-- 4 Step Routine Packshots with Arrow Dividers -->
            <div class="routine-flow-row">
              <div class="routine-step-col">
                <div class="step-bottle-wrap">
                  <img src="/images/prod-laroche-effaclar.jpg" alt="Cleanser" class="step-bottle-img" />
                </div>
                <span class="step-label">Cleanser</span>
              </div>
              <ChevronRight :size="14" class="step-arrow" />

              <div class="routine-step-col">
                <div class="step-bottle-wrap">
                  <img src="/images/prod-ordinary.jpg" alt="Treatment" class="step-bottle-img" />
                </div>
                <span class="step-label">Treatment</span>
              </div>
              <ChevronRight :size="14" class="step-arrow" />

              <div class="routine-step-col">
                <div class="step-bottle-wrap">
                  <img src="/images/prod-laneige.jpg" alt="Moisturizer" class="step-bottle-img" />
                </div>
                <span class="step-label">Moisturizer</span>
              </div>
              <ChevronRight :size="14" class="step-arrow" />

              <div class="routine-step-col">
                <div class="step-bottle-wrap">
                  <img src="/images/prod-cerave-cleanser.jpg" alt="Sunscreen" class="step-bottle-img" />
                </div>
                <span class="step-label">Sunscreen</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Key Ingredients for Clearer Skin -->
          <div class="editorial-card ingredients-card">
            <div class="editorial-card-header">
              <h3 class="editorial-card-title">Key Ingredients for<br />Clearer Skin</h3>
              <router-link to="/shop" class="header-link-red">
                Learn More &rarr;
              </router-link>
            </div>

            <!-- 4 Circular Ingredient Swatches matching format -->
            <div class="ingredients-swatch-grid">
              <div class="ingredient-swatch-col">
                <div class="swatch-circle-wrap">
                  <img src="/images/search-droplet-macro.jpg" alt="Salicylic Acid" class="swatch-circle-img" />
                </div>
                <span class="swatch-name">Salicylic Acid</span>
                <span class="swatch-desc">Exfoliates pores</span>
              </div>

              <div class="ingredient-swatch-col">
                <div class="swatch-circle-wrap">
                  <img src="/images/search-gel-swatch.jpg" alt="Niacinamide" class="swatch-circle-img" />
                </div>
                <span class="swatch-name">Niacinamide</span>
                <span class="swatch-desc">Controls oil</span>
              </div>

              <div class="ingredient-swatch-col">
                <div class="swatch-circle-wrap">
                  <img src="/images/prod-innisfree-cleanser.jpg" alt="Tea Tree" class="swatch-circle-img" />
                </div>
                <span class="swatch-name">Tea Tree</span>
                <span class="swatch-desc">Soothes skin</span>
              </div>

              <div class="ingredient-swatch-col">
                <div class="swatch-circle-wrap">
                  <img src="/images/cat-masks.jpg" alt="Centella Asiatica" class="swatch-circle-img" />
                </div>
                <span class="swatch-name">Centella Asiatica</span>
                <span class="swatch-desc">Calms irritation</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Expert Tips Articles matching format -->
          <div class="editorial-card articles-card">
            <div class="editorial-card-header">
              <h3 class="editorial-card-title">Expert Tips</h3>
              <router-link to="/shop" class="header-link-red">
                View All Tips &rarr;
              </router-link>
            </div>

            <!-- 3 Editorial Articles with Thumbnails & Read Times -->
            <div class="expert-articles-list">
              <div class="article-item-row">
                <img src="/images/pdp-model-radiant.jpg" alt="Article 1" class="article-thumb" />
                <div class="article-info">
                  <h4 class="article-title">How to Build a Skincare Routine for Acne-Prone Skin</h4>
                  <span class="article-time">5 min read</span>
                </div>
              </div>

              <div class="article-item-row">
                <img src="/images/quiz-model.jpg" alt="Article 2" class="article-thumb" />
                <div class="article-info">
                  <h4 class="article-title">Common Causes of Acne (and How to Prevent Them)</h4>
                  <span class="article-time">4 min read</span>
                </div>
              </div>

              <div class="article-item-row">
                <img src="/images/banner-skin-quiz.jpg" alt="Article 3" class="article-thumb" />
                <div class="article-info">
                  <h4 class="article-title">The Best Ingredients for Blemish-Prone Skin</h4>
                  <span class="article-time">6 min read</span>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import ProductCard from '@/components/ProductCard.vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { useWishlistStore } from '@/stores/wishlist'
import {
  Activity,
  Award,
  ChevronRight,
  ChevronUp,
  Clock,
  Droplet,
  Heart,
  LayoutGrid,
  Leaf,
  List,
  Moon,
  Search,
  ShieldCheck,
  ShoppingCart,
  Smile,
  Sparkles,
  Sun,
  Zap
} from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'

const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const productStore = useProductStore()

// State
const activeConcernId = ref('acne')
const activeTypeId = ref('all')
const brandSearchQuery = ref('')
const selectedBrands = ref([])
const selectedCategories = ref([])
const selectedIngredients = ref([])
const minPrice = ref(0)
const maxPrice = ref(200)
const sortBy = ref('bestselling')
const viewMode = ref('grid')
const currentPage = ref(1)

// Concerns List from format/Skin Concern-Skin Type.png
const concernsList = [
  {
    id: 'acne',
    name: 'Acne & Blemishes',
    shortName: 'Acne & Blemishes',
    icon: Smile,
    subtitle: 'Clearer skin. A more confident you.',
    desc: 'Discover effective skincare solutions from trusted brands to help reduce breakouts, calm inflammation, and prevent future blemishes.',
    benefits: ['Targets Breakouts', 'Soothes & Calms', 'Controls Excess Oil', 'Supports Clearer Skin']
  },
  {
    id: 'dark-spots',
    name: 'Dark Spots & Pigmentation',
    shortName: 'Dark Spots',
    icon: Sun,
    subtitle: 'Brighten discoloration and even skin tone.',
    desc: 'Clinically proven vitamin C, niacinamide, and tranexamic acid formulations that gently fade hyperpigmentation and reveal natural radiance.',
    benefits: ['Fades Pigmentation', 'Evens Skin Tone', 'Protects Cell Matrix', 'Boosts Luminosity']
  },
  {
    id: 'aging',
    name: 'Fine Lines & Elasticity',
    shortName: 'Aging',
    icon: Clock,
    subtitle: 'Firm, plump, and preserve skin vitality.',
    desc: 'Nourishing peptide elixirs, retinol alternatives, and bio-ferments to support collagen synthesis and smooth fine lines.',
    benefits: ['Boosts Collagen', 'Plumps Fine Lines', 'Firms Elasticity', 'Cellular Renewal']
  },
  {
    id: 'dryness',
    name: 'Dryness & Dehydration',
    shortName: 'Dryness',
    icon: Droplet,
    subtitle: 'Quench parched skin with multi-depth moisture.',
    desc: 'Ceramide-rich barrier creams and multi-molecular hyaluronic serums that restore long-lasting hydration and banish flaking.',
    benefits: ['Restores Barrier', 'Locks Moisture', 'Smooths Roughness', 'Zero Flaking']
  },
  {
    id: 'oiliness',
    name: 'Oiliness & Pore Care',
    shortName: 'Oiliness',
    icon: Activity,
    subtitle: 'Balance sebum without stripping essential lipids.',
    desc: 'Lightweight clarifying hydrators and pore-refining extracts that mattify excess shine and keep skin fresh all day.',
    benefits: ['Minimizes Pores', 'Mattifies Shine', 'Balances Sebum', 'Refreshes Skin']
  },
  {
    id: 'sensitivity',
    name: 'Redness & Sensitive Barrier',
    shortName: 'Sensitivity',
    icon: ShieldCheck,
    subtitle: 'Calm reactive skin and strengthen defense.',
    desc: 'Fragrance-free cica and heartleaf therapies designed to comfort compromised skin, quiet irritation, and repair defense.',
    benefits: ['Instant Calming', 'Strengthens Defense', 'Hypoallergenic', 'Reduces Redness']
  },
  {
    id: 'dullness',
    name: 'Dullness & Uneven Tone',
    shortName: 'Dullness',
    icon: Sparkles,
    subtitle: 'Wake up glowing, energized skin.',
    desc: 'Gentle fruit enzyme exfoliants and fermented essences that sweep away dead cells to unveil a lit-from-within glow.',
    benefits: ['Exfoliates Gently', 'Restores Glow', 'Smooths Texture', 'Revitalizes Skin']
  },
  {
    id: 'uneven-texture',
    name: 'Uneven Texture & Bumps',
    shortName: 'Uneven Texture',
    icon: Zap,
    subtitle: 'Smooth roughness and polish skin surface.',
    desc: 'Micro-exfoliating lactic and salicylic solutions that dissolve micro-clogs and refine surface texture for silky touch.',
    benefits: ['Polishes Surface', 'Clears Micro-Clogs', 'Silky Softness', 'Refines Pores']
  }
]

// Skin Types List from format
const typesList = [
  { id: 'normal', name: 'Normal', icon: Leaf },
  { id: 'oily', name: 'Oily', icon: Droplet },
  { id: 'dry', name: 'Dry', icon: Sparkles },
  { id: 'combination', name: 'Combination', icon: Sun },
  { id: 'sensitive', name: 'Sensitive', icon: ShieldCheck }
]

const currentConcern = computed(() => {
  return concernsList.find(c => c.id === activeConcernId.value) || concernsList[0]
})

// Brand list from format
const brandList = [
  { name: 'The Ordinary', count: 12 },
  { name: 'CeraVe', count: 10 },
  { name: 'La Roche-Posay', count: 14 },
  { name: 'COSRX', count: 11 },
  { name: 'innisfree', count: 8 },
  { name: 'SK-II', count: 2 },
  { name: 'BIODERMA', count: 9 },
  { name: 'Some By Mi', count: 6 },
  { name: 'Beauty of Joseon', count: 7 }
]

const filteredBrandList = computed(() => {
  if (!brandSearchQuery.value) return brandList
  const q = brandSearchQuery.value.toLowerCase()
  return brandList.filter(b => b.name.toLowerCase().includes(q))
})

const productTypesList = [
  { slug: 'cleansers', name: 'Cleansers', count: 18 },
  { slug: 'toners', name: 'Toners', count: 12 },
  { slug: 'serums', name: 'Serums', count: 24 },
  { slug: 'moisturizers', name: 'Moisturizers', count: 14 },
  { slug: 'treatments', name: 'Treatments', count: 16 },
  { slug: 'masks', name: 'Masks', count: 8 },
  { slug: 'sunscreens', name: 'Sunscreens', count: 6 }
]

const keyIngredientsList = [
  { name: 'Salicylic Acid', count: 22 },
  { name: 'Niacinamide', count: 28 },
  { name: 'Tea Tree', count: 12 },
  { name: 'Zinc', count: 10 },
  { name: 'Centella Asiatica', count: 14 },
  { name: 'BHA', count: 18 },
  { name: 'AHA', count: 16 }
]

// 8 Featured Products matching Skin Concern-Skin Type.png grid:
// 1. La Roche-Posay Effaclar ($18.00) Best Seller
// 2. The Ordinary Niacinamide 10% + Zinc ($8.90)
// 3. CeraVe Foaming Facial Cleanser ($16.00)
// 4. COSRX BHA Blackhead Power Liquid ($25.00)
// 5. Innisfree Green Tea Seed Serum ($28.00 / $35.00) 20% OFF
// 6. BIODERMA Sebium H2O Micellar Water ($16.00)
// 7. SK-II Facial Treatment Essence ($99.00)
// 8. Some By Mi AHA.BHA.PHA 30 Days Miracle Toner ($20.00)
const concernProducts = [
  {
    id: 301,
    brand: 'La Roche-Posay',
    name: 'Effaclar Purifying Foaming Gel Cleanser',
    price: 18.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '6.2K',
    badge: 'Best Seller',
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-effaclar-purifying-foaming-gel'
  },
  {
    id: 302,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1% Oil Control',
    price: 8.90,
    compare_at_price: null,
    rating: 4.8,
    reviews: '9.8K',
    badge: null,
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1'
  },
  {
    id: 303,
    brand: 'CeraVe',
    name: 'Foaming Facial Cleanser for Normal to Oily Skin',
    price: 16.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '4.5K',
    badge: null,
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-foaming-facial-cleanser'
  },
  {
    id: 304,
    brand: 'COSRX',
    name: 'BHA Blackhead Power Liquid Exfoliant',
    price: 25.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '3.9K',
    badge: null,
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-bha-blackhead-power-liquid'
  },
  {
    id: 305,
    brand: 'innisfree',
    name: 'Green Tea Seed Serum Moisture Barrier',
    price: 28.00,
    compare_at_price: 35.00,
    rating: 4.6,
    reviews: '2.1K',
    badge: '20% OFF',
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum'
  },
  {
    id: 306,
    brand: 'BIODERMA',
    name: 'Sébium H2O Micellar Water Purifying Cleanser',
    price: 16.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '4.4K',
    badge: null,
    image_url: '/images/prod-bioderma-micellar.jpg',
    slug: 'bioderma-sebium-h2o'
  },
  {
    id: 307,
    brand: 'SK-II',
    name: 'Facial Treatment Essence Pitera Complex',
    price: 99.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '1.2K',
    badge: null,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence'
  },
  {
    id: 308,
    brand: 'Some By Mi',
    name: 'AHA.BHA.PHA 30 Days Miracle Toner Exfoliant',
    price: 20.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: '2.8K',
    badge: null,
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'some-by-mi-miracle-toner'
  }
]

const filteredProducts = computed(() => {
  let list = [...concernProducts]

  if (selectedBrands.value.length > 0) {
    list = list.filter(p => selectedBrands.value.some(b => p.brand.toLowerCase() === b.toLowerCase()))
  }

  list = list.filter(p => p.price <= maxPrice.value && p.price >= minPrice.value)

  if (sortBy.value === 'price-asc') {
    list.sort((a, b) => a.price - b.price)
  } else if (sortBy.value === 'price-desc') {
    list.sort((a, b) => b.price - a.price)
  } else if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating)
  }

  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredProducts.value.length / 8)))

const paginatedProducts = computed(() => {
  return filteredProducts.value.slice((currentPage.value - 1) * 8, currentPage.value * 8)
})

function clearAllFilters() {
  selectedBrands.value = []
  selectedCategories.value = []
  selectedIngredients.value = []
  brandSearchQuery.value = ''
  minPrice.value = 0
  maxPrice.value = 200
  activeTypeId.value = 'all'
}

function addToCart(product) {
  cartStore.addItem({
    id: product.id,
    name: product.name,
    brand: product.brand,
    price: product.price,
    compare_at_price: product.compare_at_price,
    image_url: product.image_url,
    slug: product.slug
  })
}
</script>

<style scoped>
/* ==========================================================================
   SKIN CONCERN & SKIN TYPE VIEW (Matches format/Skin Concern-Skin Type.png)
   ========================================================================== */

.concerns-page {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 5rem;
}

/* Breadcrumbs */
.breadcrumb-container {
  padding: 0.6rem 0 0.5rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.84rem;
  color: #57534E;
}

.breadcrumb-link {
  color: #57534E;
  text-decoration: none;
}

.breadcrumb-link:hover {
  color: #8E4A3E;
}

.breadcrumb-sep {
  color: #8C877F;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Hero Banner */
.banner-container {
  margin-bottom: 1.25rem;
}

.concerns-hero-card {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border-radius: 16px;
  border: 1px solid rgba(196, 98, 60, 0.12);
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  overflow: hidden;
  min-height: 275px;
  padding: 1.75rem 2.5rem;
}

.hero-left-content {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
  padding: 0;
}

.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.12;
  margin-bottom: 0.35rem;
  letter-spacing: -0.015em;
}

.hero-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.45rem;
  line-height: 1.25;
}

.hero-desc {
  font-size: 0.92rem;
  line-height: 1.45;
  color: #57534E;
  margin-bottom: 1.15rem;
  max-width: 530px;
}

/* 4 Benefits Row */
.hero-benefits-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(196, 98, 60, 0.12);
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.benefit-icon {
  color: #8E2B2B;
  flex-shrink: 0;
}

.benefit-text {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
}

/* Hero Right Visual */
.hero-right-visual {
  width: 480px;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 1;
}

.hero-stage-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.hero-packshot-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  mask-image: linear-gradient(to right, transparent 0%, black 18%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 18%);
  box-shadow: 0 8px 24px rgba(40, 20, 10, 0.06);
}

.hero-callout-oval {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 105px;
  height: 105px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.96) 40%, rgba(253, 242, 238, 0.9) 100%);
  border: 1px solid rgba(196, 98, 60, 0.35);
  box-shadow: 0 4px 16px rgba(142, 43, 43, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  z-index: 3;
}

.callout-text {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.2;
}

/* ==========================================================================
   DUAL HORIZONTAL SELECTOR BAR (Matches format)
   ========================================================================== */
.dual-selector-container {
  margin-bottom: 2rem;
}

.dual-selector-bar {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 12px;
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.selector-section-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1.4;
  overflow-x: auto;
}

.selector-section-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  overflow-x: auto;
}

.selector-section-label {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-serif);
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
  white-space: nowrap;
  flex-shrink: 0;
}

.label-arrow {
  color: #8E4A3E;
}

.selector-items-scroll {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.chip-selector-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.35rem 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.chip-circle-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #57534E;
  transition: all 0.2s ease;
}

.chip-title {
  font-size: 0.74rem;
  font-weight: 500;
  color: #57534E;
}

.chip-selector-btn:hover .chip-circle-icon {
  background: #F4EFEB;
  border-color: #8E4A3E;
  color: #8E4A3E;
}

.chip-selector-btn.active .chip-circle-icon {
  background: #F8ECE8;
  border-color: #8E4A3E;
  color: #8E4A3E;
  box-shadow: 0 0 0 2px rgba(142, 74, 62, 0.2);
}

.chip-selector-btn.active .chip-title {
  color: #8E4A3E;
  font-weight: 700;
}

.selector-divider-vertical {
  width: 1px;
  height: 46px;
  background: rgba(28, 25, 23, 0.1);
  flex-shrink: 0;
}

/* ==========================================================================
   3-COLUMN CATALOG LAYOUT (Matches format)
   ========================================================================== */
.catalog-section {
  margin-bottom: 4rem;
}

.concerns-3col-layout {
  display: grid;
  grid-template-columns: 210px 1fr 280px;
  gap: 1.5rem;
  align-items: start;
}

/* Left Filter Sidebar */
.filters-panel {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 10px;
  padding: 1.15rem;
}

.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
}

.filters-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: #1C1917;
}

.clear-all-link {
  background: none;
  border: none;
  color: #8E4A3E;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
}

.accordion-group {
  margin-bottom: 1.15rem;
  padding-bottom: 1.15rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
}

.accordion-group:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.accordion-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.65rem;
  cursor: pointer;
}

.accordion-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #1C1917;
}

.search-brands-box {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.1);
  border-radius: 6px;
  padding: 0.35rem 0.55rem;
  margin-bottom: 0.65rem;
}

.search-brands-icon {
  color: #8C877F;
}

.search-brands-input {
  border: none;
  background: transparent;
  font-size: 0.76rem;
  color: #1C1917;
  outline: none;
  width: 100%;
}

.checkbox-options-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  max-height: 160px;
  overflow-y: auto;
}

.filter-checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #44403C;
  cursor: pointer;
}

.filter-checkbox-item input {
  accent-color: #8E4A3E;
}

/* Price Range */
.slider-track-visual {
  width: 100%;
  height: 4px;
  background: #F4EFEB;
  border-radius: 4px;
  position: relative;
  margin: 0.6rem 0;
}

.slider-fill-visual {
  height: 100%;
  background: #8E4A3E;
  border-radius: 4px;
}

.price-range-native {
  width: 100%;
  accent-color: #8E4A3E;
}

.price-scale-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #8C877F;
  margin-top: 0.2rem;
}

.price-inputs-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.6rem;
}

.price-input-box {
  display: flex;
  align-items: center;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 4px;
  padding: 0.25rem 0.4rem;
  background: #FAF8F5;
  width: 100%;
}

.currency-sym {
  font-size: 0.75rem;
  color: #8C877F;
  margin-right: 2px;
}

.price-input-box input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 0.78rem;
  color: #1C1917;
  outline: none;
}

.price-sep {
  color: #8C877F;
}

/* Center Catalog Main Area */
.catalog-toolbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  padding-bottom: 0.65rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
}

.products-total-count {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
}

.toolbar-controls-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-dropdown-wrap {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.sort-by-lbl {
  font-size: 0.8rem;
  color: #57534E;
}

.format-sort-select {
  padding: 0.35rem 0.65rem;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 4px;
  background: #FFFFFF;
  font-size: 0.8rem;
  color: #1C1917;
  outline: none;
  cursor: pointer;
}

.view-mode-toggle {
  display: flex;
  align-items: center;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 4px;
  overflow: hidden;
}

.view-toggle-btn {
  background: #FFFFFF;
  border: none;
  padding: 0.35rem 0.55rem;
  color: #78716C;
  cursor: pointer;
}

.view-toggle-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* 4-Column Product Grid matching format */
.concerns-products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.concern-product-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 8px;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.concern-product-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(28, 25, 23, 0.06);
  border-color: #8E4A3E;
}

.card-stage {
  position: relative;
  width: 100%;
  height: 150px;
  background: #FAF8F5;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-badge-pill {
  position: absolute;
  top: 6px;
  left: 6px;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  z-index: 2;
}

.card-wishlist-heart {
  position: absolute;
  top: 6px;
  right: 6px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  z-index: 2;
}

.card-image-link {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-image {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.concern-product-card:hover .card-image {
  transform: scale(1.06);
}

.card-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-brand {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.15rem;
}

.card-name {
  font-size: 0.8rem;
  font-weight: 500;
  line-height: 1.35;
  margin-bottom: 0.35rem;
  min-height: 2.2em;
}

.card-name a {
  color: #44403C;
  text-decoration: none;
}

.card-name a:hover {
  color: #8E4A3E;
}

.card-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.68rem;
  margin-bottom: 0.45rem;
}

.card-rating .stars {
  color: #D97706;
}

.rating-val {
  font-weight: 600;
  color: #1C1917;
}

.review-count {
  color: #8C877F;
}

.card-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  margin-bottom: 0.75rem;
  margin-top: auto;
}

.price-current {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.price-compare {
  font-size: 0.76rem;
  color: #8C877F;
  text-decoration: line-through;
}

/* Terracotta Format Button */
.terracotta-add-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.52rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: 1px solid #8E4A3E;
  border-radius: 4px;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.terracotta-add-btn:hover {
  background: #73382D;
  border-color: #73382D;
}

/* Pagination */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding-top: 1rem;
}

.page-nav-btn, .page-num-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid rgba(28, 25, 23, 0.12);
  background: #FFFFFF;
  color: #44403C;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.page-num-btn.active {
  background: #8E4A3E;
  border-color: #8E4A3E;
  color: #FFFFFF;
}

.page-num-btn:hover:not(.active) {
  background: #FAF8F5;
  border-color: #8E4A3E;
  color: #8E4A3E;
}

.page-ellipsis {
  font-size: 0.8rem;
  color: #8C877F;
}

/* ==========================================================================
   RIGHT EDITORIAL SIDEBAR (Matches format)
   ========================================================================== */
.routine-editorial-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.editorial-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 10px;
  padding: 1.25rem;
}

.editorial-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.15rem;
}

.editorial-card-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1.2;
}

.header-link-red {
  font-size: 0.74rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
  white-space: nowrap;
}

.header-link-red:hover {
  text-decoration: underline;
}

/* 4 Step Routine Packshots */
.routine-flow-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.25rem;
}

.routine-step-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
}

.step-bottle-wrap {
  width: 50px;
  height: 65px;
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
}

.step-bottle-img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.step-label {
  font-size: 0.68rem;
  font-weight: 600;
  color: #1C1917;
}

.step-arrow {
  color: #8E4A3E;
  margin-bottom: 1rem;
}

/* Key Ingredients Circular Swatches */
.ingredients-swatch-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.ingredient-swatch-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.swatch-circle-wrap {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid rgba(28, 25, 23, 0.1);
  margin-bottom: 0.35rem;
}

.swatch-circle-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.swatch-name {
  font-size: 0.68rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.15;
  margin-bottom: 2px;
}

.swatch-desc {
  font-size: 0.6rem;
  color: #78716C;
}

/* Expert Tips Articles */
.expert-articles-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.article-item-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.article-thumb {
  width: 58px;
  height: 46px;
  border-radius: 6px;
  object-fit: cover;
}

.article-info {
  display: flex;
  flex-direction: column;
}

.article-title {
  font-size: 0.76rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.3;
  margin-bottom: 2px;
}

.article-time {
  font-size: 0.66rem;
  color: #8C877F;
}

/* Responsive */
@media (max-width: 1200px) {
  .concerns-3col-layout {
    grid-template-columns: 200px 1fr;
  }
  .routine-editorial-sidebar {
    display: none;
  }
}

@media (max-width: 900px) {
  .concerns-3col-layout {
    grid-template-columns: 1fr;
  }
  .concerns-hero-card {
    grid-template-columns: 1fr;
  }
  .hero-benefits-row {
    grid-template-columns: repeat(2, 1fr);
  }
  .dual-selector-bar {
    flex-direction: column;
    align-items: flex-start;
  }
  .selector-divider-vertical {
    display: none;
  }
}

@media (max-width: 600px) {
  .concerns-products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
