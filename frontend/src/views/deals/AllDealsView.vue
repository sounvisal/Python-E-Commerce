<template>
  <div class="all-deals-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <router-link to="/deals" class="breadcrumb-link">Deals</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">All Deals</span>
      </nav>
    </div>

    <!-- Hero Banner -->
    <section class="container banner-container">
      <div class="all-deals-hero-card">
        <div class="hero-left-content">
          <span class="hero-eyebrow-pill">LIMITED TIME OFFERS</span>
          <h1 class="hero-title">All Deals &amp; Offers</h1>
          <h2 class="hero-tagline">Authentic Skincare. Maximum Savings.</h2>
          <p class="hero-desc">
            Explore our full catalog of daily specials, flash discounts, brand promotions, and curated bundle sets. Save up to 50% on top dermatological and luxury skincare brands.
          </p>

          <!-- 4 Trust Badges -->
          <div class="hero-trust-row">
            <div class="trust-item">
              <ShieldCheck :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">100% Authentic</span>
                <span class="trust-sub">Direct from Brands</span>
              </div>
            </div>
            <div class="trust-item">
              <Clock :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Flash Savings</span>
                <span class="trust-sub">Updated Daily</span>
              </div>
            </div>
            <div class="trust-item">
              <Gift :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Curated Bundles</span>
                <span class="trust-sub">Extra Routine Value</span>
              </div>
            </div>
            <div class="trust-item">
              <Sparkles :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Free Samples</span>
                <span class="trust-sub">With Every Order</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero-right-visual">
          <div class="hero-stage-wrap">
            <img
              src="/images/banners/banner-deals-clean.jpg"
              alt="All Deals Showcase"
              class="hero-packshot-img"
            />
            <div class="hero-callout-oval">
              <span class="callout-text">Glow<br />More.<br />Spend<br />Less.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filter Pills Bar -->
    <section class="container pills-container">
      <div class="deals-filter-pills-bar">
        <button
          class="deal-filter-pill"
          :class="{ active: currentFilter === 'all' }"
          @click="setFilter('all')"
        >
          <span>All Deals</span>
          <span class="pill-count">({{ allDealsProducts.length }})</span>
        </button>

        <button
          class="deal-filter-pill"
          :class="{ active: currentFilter === 'flash' }"
          @click="setFilter('flash')"
        >
          <Flame :size="14" class="pill-icon" />
          <span>Flash Deals</span>
          <span class="pill-count">({{ flashCount }})</span>
        </button>

        <button
          class="deal-filter-pill"
          :class="{ active: currentFilter === 'brand' }"
          @click="setFilter('brand')"
        >
          <ShoppingBag :size="14" class="pill-icon" />
          <span>Brand Promotions</span>
          <span class="pill-count">({{ brandCount }})</span>
        </button>

        <button
          class="deal-filter-pill"
          :class="{ active: currentFilter === 'bundles' }"
          @click="setFilter('bundles')"
        >
          <Gift :size="14" class="pill-icon" />
          <span>Bundle Sets</span>
          <span class="pill-count">({{ bundleCount }})</span>
        </button>

        <button
          class="deal-filter-pill"
          :class="{ active: currentFilter === 'clearance' }"
          @click="setFilter('clearance')"
        >
          <Tag :size="14" class="pill-icon" />
          <span>Clearance</span>
          <span class="pill-count">({{ clearanceCount }})</span>
        </button>
      </div>
    </section>

    <!-- Main Catalog Layout: Products Grid + Sidebar -->
    <section class="container catalog-section">
      <div class="catalog-layout">
        <!-- Main Products Column -->
        <main class="catalog-main">
          <!-- Toolbar -->
          <div class="catalog-toolbar">
            <div class="results-count-wrap">
              <span class="results-count">
                Showing <strong>{{ filteredProducts.length }}</strong> promotional deals
              </span>
            </div>

            <div class="toolbar-actions">
              <div class="sort-select-wrapper">
                <span class="sort-label">Sort by:</span>
                <select v-model="sortBy" class="sort-select" aria-label="Sort deals">
                  <option value="discount">Highest Discount</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                  <option value="rating">Highest Rated</option>
                  <option value="popular">Most Popular</option>
                </select>
              </div>

              <div class="view-mode-toggle">
                <button
                  class="toggle-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  aria-label="Grid view"
                >
                  <LayoutGrid :size="16" />
                </button>
                <button
                  class="toggle-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  aria-label="List view"
                >
                  <List :size="16" />
                </button>
              </div>
            </div>
          </div>

          <!-- Product Grid using standardized ProductCard matching HomeView -->
          <div
            v-if="filteredProducts.length > 0"
            :class="viewMode === 'list' ? 'deals-list-container' : 'deals-catalog-grid'"
          >
            <ProductCard
              v-for="product in filteredProducts"
              :key="product.id"
              :product="product"
              :view-mode="viewMode"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="empty-deals-box">
            <Tag :size="36" class="empty-icon" />
            <h3 class="empty-title">No deals found in this category</h3>
            <p class="empty-sub">Check back soon or explore our full collection of beauty essentials.</p>
            <button class="empty-reset-btn" @click="setFilter('all')">
              View All Deals
            </button>
          </div>

          <!-- Pagination Bar -->
          <div class="deals-pagination-bar" v-if="filteredProducts.length > 0">
            <button class="page-arrow-btn" :disabled="currentPage === 1" @click="currentPage--">
              <ChevronLeft :size="16" />
            </button>
            <button class="page-num-btn active">1</button>
            <button class="page-num-btn">2</button>
            <button class="page-arrow-btn" @click="currentPage++">
              <ChevronRight :size="16" />
            </button>
          </div>
        </main>

        <!-- Right Sidebar Rails -->
        <aside class="catalog-sidebar">
          <!-- Card 1: Live Flash Deal Spotlight -->
          <div class="sidebar-card spotlight-card">
            <div class="spotlight-badge">
              <Flame :size="14" />
              <span>DEAL OF THE DAY</span>
            </div>
            <div class="spotlight-stage">
              <img src="/images/prod-sk2.jpg" alt="SK-II Facial Treatment Essence" class="spotlight-img" />
              <span class="spotlight-discount-tag">30% OFF</span>
            </div>
            <div class="spotlight-info">
              <span class="spotlight-brand">SK-II</span>
              <h4 class="spotlight-name">Facial Treatment Essence</h4>
              <div class="spotlight-prices">
                <span class="spotlight-now">$99.00</span>
                <span class="spotlight-was">$142.00</span>
              </div>
              <!-- Countdown Mini -->
              <div class="mini-countdown">
                <Clock :size="13" />
                <span>Ends in <strong>12h 34m 11s</strong></span>
              </div>
              <router-link to="/product/sk-ii-facial-treatment-essence" class="spotlight-cta-btn">
                Claim Deal &rarr;
              </router-link>
            </div>
          </div>

          <!-- Card 2: Bundle & Save Extra 15% -->
          <div class="sidebar-card bundle-promo-card">
            <div class="bundle-card-content">
              <div class="bundle-icon-wrap">
                <Gift :size="24" />
              </div>
              <h4 class="bundle-card-title">Bundle &amp; Save Extra</h4>
              <p class="bundle-card-desc">Buy any 2 routine essentials and get an extra 15% off at checkout.</p>
              <div class="coupon-pill">
                <span>Code: <strong>ROUTINE15</strong></span>
              </div>
            </div>
            <div class="bundle-card-visual">
              <img src="/images/deals-bundle-duo.jpg" alt="Routine Bundles" class="bundle-card-img" />
            </div>
          </div>

          <!-- Card 3: Authenticity Guarantee -->
          <div class="sidebar-card trust-sidebar-card">
            <ShieldCheck :size="28" class="trust-shield-icon" />
            <h4 class="trust-card-title">100% Authenticity Guarantee</h4>
            <p class="trust-card-desc">
              Every discounted item is genuine, fresh, and sourced directly from verified manufacturers. No grey market, ever.
            </p>
            <router-link to="/authenticity" class="trust-learn-link">
              Learn How We Verify &rarr;
            </router-link>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ChevronRight,
  ChevronLeft,
  ShieldCheck,
  Clock,
  ShoppingBag,
  Sparkles,
  Flame,
  Gift,
  Tag,
  LayoutGrid,
  List
} from 'lucide-vue-next'
import ProductCard from '@/components/ProductCard.vue'

const route = useRoute()
const router = useRouter()

const currentFilter = ref('all')
const sortBy = ref('discount')
const viewMode = ref('grid')
const currentPage = ref(1)

// 18 High Quality Deal Products strictly using authentic existing /images/prod-*.jpg packshots
const allDealsProducts = [
  {
    id: 101,
    name: 'Facial Treatment Essence 230ml',
    brand: 'SK-II',
    price: 99.00,
    compare_at_price: 142.00,
    rating: 4.8,
    reviews: 1200,
    badge: '30% OFF',
    deal_type: 'flash',
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence',
    stock: 24,
  },
  {
    id: 102,
    name: 'Advanced Night Repair 50ml',
    brand: 'Estée Lauder',
    price: 78.00,
    compare_at_price: 104.00,
    rating: 4.7,
    reviews: 892,
    badge: '25% OFF',
    deal_type: 'flash',
    image_url: '/images/bottle-cerave.jpg',
    slug: 'estee-lauder-advanced-night-repair',
    stock: 18,
  },
  {
    id: 103,
    name: 'Lip Sleeping Mask [Berry]',
    brand: 'LANEIGE',
    price: 18.00,
    compare_at_price: 30.00,
    rating: 4.8,
    reviews: 1500,
    badge: '40% OFF',
    deal_type: 'flash',
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask',
    stock: 50,
  },
  {
    id: 104,
    name: 'Niacinamide 10% + Zinc 1%',
    brand: 'The Ordinary',
    price: 7.20,
    compare_at_price: 9.00,
    rating: 4.7,
    reviews: 9800,
    badge: '20% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1',
    stock: 85,
  },
  {
    id: 105,
    name: 'Moisturizing Cream 454g',
    brand: 'CeraVe',
    price: 16.00,
    compare_at_price: 24.50,
    rating: 4.8,
    reviews: 6200,
    badge: '35% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-cerave.jpg',
    slug: 'cerave-moisturizing-cream',
    stock: 60,
  },
  {
    id: 106,
    name: 'Green Tea Seed Hyaluronic Serum',
    brand: 'innisfree',
    price: 28.00,
    compare_at_price: 56.00,
    rating: 4.6,
    reviews: 2100,
    badge: '50% OFF',
    deal_type: 'flash',
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum',
    stock: 35,
  },
  {
    id: 107,
    name: 'Glow Serum: Propolis + Niacinamide',
    brand: 'Beauty of Joseon',
    price: 14.00,
    compare_at_price: 20.00,
    rating: 4.8,
    reviews: 3400,
    badge: '30% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-glow-serum',
    stock: 40,
  },
  {
    id: 108,
    name: 'Advanced Snail 96 Mucin Power Essence',
    brand: 'COSRX',
    price: 19.00,
    compare_at_price: 25.00,
    rating: 4.8,
    reviews: 4100,
    badge: '24% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-snail-96-essence',
    stock: 75,
  },
  {
    id: 109,
    name: 'Heartleaf 77% Soothing Toner',
    brand: 'Anua',
    price: 19.50,
    compare_at_price: 26.00,
    rating: 4.7,
    reviews: 2800,
    badge: '25% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'anua-heartleaf-77-toner',
    stock: 45,
  },
  {
    id: 110,
    name: 'Effaclar Duo+ Anti-Imperfections',
    brand: 'La Roche-Posay',
    price: 24.00,
    compare_at_price: 32.00,
    rating: 4.6,
    reviews: 1900,
    badge: '25% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-effaclar-duo',
    stock: 30,
  },
  {
    id: 111,
    name: 'Sensibio H2O Soothing Micellar Water',
    brand: 'Bioderma',
    price: 13.50,
    compare_at_price: 18.00,
    rating: 4.8,
    reviews: 5100,
    badge: '25% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-bioderma-micellar.jpg',
    slug: 'bioderma-sensibio-h2o',
    stock: 65,
  },
  {
    id: 112,
    name: 'First Care Activating Serum VI',
    brand: 'Sulwhasoo',
    price: 72.00,
    compare_at_price: 90.00,
    rating: 4.9,
    reviews: 1300,
    badge: '20% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-sulwhasoo.jpg',
    slug: 'sulwhasoo-first-care-activating-serum',
    stock: 20,
  },
  {
    id: 113,
    name: 'Daily Microfoliant Exfoliator',
    brand: 'Dermalogica',
    price: 52.00,
    compare_at_price: 68.00,
    rating: 4.8,
    reviews: 950,
    badge: '24% OFF',
    deal_type: 'brand',
    image_url: '/images/prod-dermalogica.jpg',
    slug: 'dermalogica-daily-microfoliant',
    stock: 22,
  },
  {
    id: 114,
    name: 'Radiant Glow Full 3-Step Routine Set',
    brand: 'Luméa Discovery',
    price: 64.00,
    compare_at_price: 110.00,
    rating: 4.9,
    reviews: 640,
    badge: '42% OFF',
    deal_type: 'bundles',
    image_url: '/images/cat-kits.jpg',
    slug: 'lumea-radiant-glow-routine-set',
    stock: 15,
  },
  {
    id: 115,
    name: 'Deep Barrier Hydration Duo Set',
    brand: 'Luméa Discovery',
    price: 45.00,
    compare_at_price: 75.00,
    rating: 4.8,
    reviews: 420,
    badge: '40% OFF',
    deal_type: 'bundles',
    image_url: '/images/special-offer.jpg',
    slug: 'lumea-barrier-hydration-duo',
    stock: 20,
  },
  {
    id: 116,
    name: 'Green Tea Amino Hydrating Cleanser',
    brand: 'innisfree',
    price: 8.50,
    compare_at_price: 15.00,
    rating: 4.5,
    reviews: 820,
    badge: '43% OFF',
    deal_type: 'clearance',
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-cleanser',
    stock: 12,
  },
  {
    id: 117,
    name: 'Foaming Facial Cleanser 236ml',
    brand: 'CeraVe',
    price: 11.00,
    compare_at_price: 19.00,
    rating: 4.7,
    reviews: 3200,
    badge: '42% OFF',
    deal_type: 'clearance',
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-foaming-cleanser',
    stock: 16,
  },
  {
    id: 118,
    name: 'Heartleaf Pore Control Cleansing Oil',
    brand: 'Anua',
    price: 16.00,
    compare_at_price: 28.00,
    rating: 4.6,
    reviews: 1400,
    badge: '43% OFF',
    deal_type: 'clearance',
    image_url: '/images/prod-anua-cleanser.jpg',
    slug: 'anua-pore-control-cleansing-oil',
    stock: 9,
  },
]

// Counts for pill badges
const flashCount = computed(() => allDealsProducts.filter(p => p.deal_type === 'flash').length)
const brandCount = computed(() => allDealsProducts.filter(p => p.deal_type === 'brand').length)
const bundleCount = computed(() => allDealsProducts.filter(p => p.deal_type === 'bundles').length)
const clearanceCount = computed(() => allDealsProducts.filter(p => p.deal_type === 'clearance').length)

function setFilter(filter) {
  currentFilter.value = filter
  router.replace({ query: { ...route.query, filter: filter === 'all' ? undefined : filter } })
}

onMounted(() => {
  if (route.query.filter) {
    currentFilter.value = route.query.filter
  }
})

const filteredProducts = computed(() => {
  let list = allDealsProducts

  if (currentFilter.value !== 'all') {
    list = list.filter(p => p.deal_type === currentFilter.value)
  }

  return [...list].sort((a, b) => {
    if (sortBy.value === 'discount') {
      const discA = a.compare_at_price ? (a.compare_at_price - a.price) / a.compare_at_price : 0
      const discB = b.compare_at_price ? (b.compare_at_price - b.price) / b.compare_at_price : 0
      return discB - discA
    }
    if (sortBy.value === 'price-asc') return a.price - b.price
    if (sortBy.value === 'price-desc') return b.price - a.price
    if (sortBy.value === 'rating') return b.rating - a.rating
    if (sortBy.value === 'popular') return (b.reviews || 0) - (a.reviews || 0)
    return 0
  })
})
</script>

<style scoped>
.all-deals-page {
  padding-bottom: 5rem;
  animation: pageFadeIn 0.35s ease both;
}

@keyframes pageFadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Breadcrumbs */
.breadcrumb-container {
  padding-top: 0.6rem;
  padding-bottom: 0.5rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: #8C877F;
}

.breadcrumb-link {
  color: #78716C;
  text-decoration: none;
  transition: color 0.15s ease;
}

.breadcrumb-link:hover {
  color: #8E4A3E;
}

.breadcrumb-sep {
  color: #C7C2BA;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 500;
}

/* Banner Container */
.banner-container {
  margin-bottom: 1.25rem;
}

.all-deals-hero-card {
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

.hero-eyebrow-pill {
  display: inline-block;
  background: #FFFFFF;
  border: 1px solid rgba(142, 74, 62, 0.3);
  color: #8E4A3E;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.35rem;
  width: fit-content;
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

.hero-trust-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(196, 98, 60, 0.12);
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.trust-icon {
  color: #8E2B2B;
  flex-shrink: 0;
}

.trust-text {
  display: flex;
  flex-direction: column;
}

.trust-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
}

.trust-sub {
  font-size: 0.72rem;
  color: #78716C;
  line-height: 1.2;
}

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
  width: 100%;
  height: 100%;
  min-height: 240px;
  position: relative;
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

/* Pills Bar */
.pills-container {
  margin-bottom: 2rem;
}

.deals-filter-pills-bar {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  scrollbar-width: none;
}

.deals-filter-pills-bar::-webkit-scrollbar {
  display: none;
}

.deal-filter-pill {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1.15rem;
  border-radius: 9999px;
  border: 1px solid rgba(28, 25, 23, 0.1);
  background: #FFFFFF;
  color: #44403C;
  font-size: 0.84rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.deal-filter-pill:hover {
  border-color: #8E4A3E;
  color: #8E4A3E;
  transform: translateY(-1px);
}

.deal-filter-pill.active {
  background: #8E4A3E;
  border-color: #8E4A3E;
  color: #FFFFFF;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.2);
}

.pill-count {
  font-size: 0.72rem;
  opacity: 0.85;
}

.deal-filter-pill.active .pill-count {
  color: #FFFFFF;
}

/* Catalog Layout */
.catalog-section {
  margin-bottom: 3.5rem;
}

.catalog-layout {
  display: grid;
  grid-template-columns: 1fr 310px;
  gap: 2.25rem;
}

/* Toolbar */
.catalog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 1.25rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
}

.results-count {
  font-size: 0.88rem;
  color: #78716C;
}

.results-count strong {
  color: #1C1917;
  font-weight: 600;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.sort-select-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-label {
  font-size: 0.84rem;
  color: #78716C;
}

.sort-select {
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  padding: 0.45rem 1.75rem 0.45rem 0.75rem;
  font-size: 0.84rem;
  color: #1C1917;
  background: #FFFFFF;
  cursor: pointer;
}

.view-mode-toggle {
  display: flex;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  overflow: hidden;
}

.toggle-btn {
  background: #FFFFFF;
  border: none;
  padding: 0.45rem 0.65rem;
  color: #78716C;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* Products Grid */
.deals-catalog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 2.5rem;
}

.deals-list-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

/* Empty State */
.empty-deals-box {
  padding: 4rem 2rem;
  text-align: center;
  background: #FFFFFF;
  border: 1px dashed rgba(28, 25, 23, 0.15);
  border-radius: 12px;
}

.empty-icon {
  color: #C7C2BA;
  margin-bottom: 1rem;
}

.empty-title {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.empty-sub {
  font-size: 0.88rem;
  color: #78716C;
  margin-bottom: 1.25rem;
}

.empty-reset-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.6rem 1.25rem;
  border-radius: 6px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
}

/* Pagination */
.deals-pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  margin-top: 2rem;
}

.page-num-btn,
.page-arrow-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(28, 25, 23, 0.1);
  background: #FFFFFF;
  color: #44403C;
  border-radius: 6px;
  font-size: 0.84rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.page-num-btn:hover,
.page-arrow-btn:hover:not(:disabled) {
  border-color: #8E4A3E;
  color: #8E4A3E;
}

.page-num-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
  border-color: #8E4A3E;
}

.page-arrow-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Sidebar */
.catalog-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 14px;
  padding: 1.5rem;
}

/* Spotlight Card */
.spotlight-card {
  background: linear-gradient(135deg, #FFF9F7 0%, #FAF0EC 100%);
  border-color: rgba(142, 74, 62, 0.2);
}

.spotlight-badge {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: #8E4A3E;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  margin-bottom: 0.85rem;
}

.spotlight-stage {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background: #FFFFFF;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
}

.spotlight-img {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

.spotlight-discount-tag {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}

.spotlight-brand {
  font-size: 0.78rem;
  font-weight: 700;
  color: #78716C;
  display: block;
}

.spotlight-name {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: #1C1917;
  margin-bottom: 0.4rem;
}

.spotlight-prices {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.spotlight-now {
  font-size: 1.25rem;
  font-weight: 700;
  color: #8E4A3E;
}

.spotlight-was {
  font-size: 0.85rem;
  color: #A8A29E;
  text-decoration: line-through;
}

.mini-countdown {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
  color: #57534E;
  margin-bottom: 1rem;
}

.spotlight-cta-btn {
  display: block;
  text-align: center;
  background: #8E4A3E;
  color: #FFFFFF;
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 600;
  padding: 0.65rem;
  border-radius: 6px;
  transition: background 0.15s ease;
}

.spotlight-cta-btn:hover {
  background: #73382D;
}

/* Bundle Card */
.bundle-promo-card {
  background: #FAF7F2;
  border-color: rgba(28, 25, 23, 0.08);
}

.bundle-icon-wrap {
  color: #8E4A3E;
  margin-bottom: 0.5rem;
}

.bundle-card-title {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.bundle-card-desc {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.4;
  margin-bottom: 0.85rem;
}

.coupon-pill {
  display: inline-block;
  background: #FFFFFF;
  border: 1px dashed #8E4A3E;
  color: #8E4A3E;
  font-size: 0.76rem;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.bundle-card-visual {
  width: 100%;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
}

.bundle-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Trust Card */
.trust-sidebar-card {
  text-align: center;
}

.trust-shield-icon {
  color: #8E4A3E;
  margin-bottom: 0.5rem;
}

.trust-card-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: #1C1917;
  margin-bottom: 0.4rem;
}

.trust-card-desc {
  font-size: 0.8rem;
  color: #78716C;
  line-height: 1.45;
  margin-bottom: 0.85rem;
}

.trust-learn-link {
  font-size: 0.82rem;
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
}

.trust-learn-link:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 1024px) {
  .catalog-layout {
    grid-template-columns: 1fr;
  }
  .all-deals-hero-card {
    grid-template-columns: 1fr;
  }
  .hero-trust-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .deals-catalog-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .deals-catalog-grid {
    grid-template-columns: 1fr;
  }
}
</style>
