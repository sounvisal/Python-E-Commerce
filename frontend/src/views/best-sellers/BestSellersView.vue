<template>
  <div class="bestsellers-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">Best Sellers</span>
      </nav>
    </div>

    <!-- Hero Banner matching Best Sellers.png -->
    <section class="container banner-container">
      <div class="bestsellers-hero-card">
        <div class="hero-left-content">
          <h1 class="hero-title">Best Sellers</h1>
          <h2 class="hero-tagline">Loved by Real People. Backed by Results.</h2>
          <p class="hero-desc">
            Discover the most popular skincare products, chosen by our community for their proven results, quality, and value.
          </p>

          <div class="trust-badges-grid">
            <div class="trust-badge-item">
              <Users :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Customer Approved</span>
                <span class="trust-sub">High ratings &amp; real reviews</span>
              </div>
            </div>
            <div class="trust-badge-item">
              <ShieldCheck :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Trusted Brands</span>
                <span class="trust-sub">100% authentic</span>
              </div>
            </div>
            <div class="trust-badge-item">
              <Award :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Proven Results</span>
                <span class="trust-sub">Visible difference</span>
              </div>
            </div>
            <div class="trust-badge-item">
              <Sparkles :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Better Skin for Everyone</span>
                <span class="trust-sub">Real people. Real stories.</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero-right-visual">
          <div class="hero-stage-wrap">
            <img
              src="/images/banners/banner-best-sellers-clean.jpg"
              alt="Luméa Best Sellers Skincare Showcase"
              class="hero-packshot-img"
            />
            <div class="hero-callout-circle">
              <span class="callout-italic">Real<br />Favorites.<br />Real<br />Results.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Filter Pills Bar matching Best Sellers.png -->
    <section class="container pills-container">
      <div class="category-pills-bar">
        <button
          class="cat-pill-btn"
          :class="{ active: selectedCategory === 'all' }"
          @click="selectedCategory = 'all'"
        >
          <Award :size="16" />
          <span>All Best Sellers</span>
        </button>
        <button
          v-for="cat in categories"
          :key="cat.slug"
          class="cat-pill-btn"
          :class="{ active: selectedCategory === cat.slug }"
          @click="selectedCategory = cat.slug"
        >
          <span>{{ cat.name }}</span>
        </button>
      </div>
    </section>

    <!-- Main Content: Products Grid + Sidebar -->
    <section class="container catalog-section">
      <div class="catalog-layout">
        <!-- Main Products Column -->
        <div class="catalog-main">
          <!-- Toolbar -->
          <div class="catalog-toolbar">
            <div class="results-count-wrap">
              <span class="results-count">Showing <strong>{{ filteredProducts.length }}</strong> best selling products</span>
            </div>

            <div class="toolbar-actions">
              <div class="sort-select-wrapper">
                <span class="sort-label">Sort by:</span>
                <select v-model="sortBy" class="sort-select" aria-label="Sort best sellers">
                  <option value="rank">Best Selling</option>
                  <option value="rating">Highest Rated</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
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

          <!-- Product Cards Grid with Rank Badges -->
          <div class="bestsellers-grid" :class="{ 'is-list-view': viewMode === 'list' }">
            <div
              v-for="(product, index) in filteredProducts"
              :key="product.id"
              class="ranked-card-wrapper"
            >
              <!-- Ranking Badge 1, 2, 3... matching Best Sellers.png -->
              <div class="rank-circle-badge">
                <span>{{ index + 1 }}</span>
              </div>
              <ProductCard :product="product" :view-mode="viewMode" />
            </div>
          </div>
        </div>

        <!-- Right Sidebar matching Best Sellers.png -->
        <aside class="catalog-sidebar">
          <!-- Card 1: Why These Are Best Sellers? -->
          <div class="sidebar-info-card why-bestsellers-card">
            <div class="why-header">
              <Crown :size="24" class="why-crown-icon" />
              <h3 class="why-title">Why These Are<br />Best Sellers?</h3>
            </div>
            <ul class="why-list">
              <li>
                <Check :size="16" class="why-check" />
                <span>Highly rated by real customers</span>
              </li>
              <li>
                <Check :size="16" class="why-check" />
                <span>Trusted and authentic brands</span>
              </li>
              <li>
                <Check :size="16" class="why-check" />
                <span>Proven skincare results</span>
              </li>
              <li>
                <Check :size="16" class="why-check" />
                <span>Loved by all skin types</span>
              </li>
            </ul>
          </div>

          <!-- Card 2: Shop by Category Mini Grid -->
          <div class="sidebar-info-card shop-cat-card">
            <div class="sidebar-heading-row">
              <h3 class="sidebar-title">Shop by Category</h3>
              <router-link to="/shop" class="sidebar-link">View All &rarr;</router-link>
            </div>
            <div class="cat-mini-grid">
              <router-link
                v-for="cat in categories.slice(0, 8)"
                :key="cat.slug"
                :to="`/category/${cat.slug}`"
                class="cat-mini-tile"
              >
                <div class="cat-mini-avatar">
                  <span class="cat-letter">{{ cat.name.charAt(0) }}</span>
                </div>
                <span class="cat-mini-name">{{ cat.name }}</span>
              </router-link>
            </div>
          </div>

          <!-- Card 3: Real People. Real Results Testimonial Banner -->
          <div class="sidebar-info-card testimonial-promo-card">
            <div class="test-text-col">
              <h3 class="test-promo-title">Real People.<br />Real Results.</h3>
              <p class="test-promo-sub">See why these products are customer favorites.</p>
              <router-link to="/journal" class="btn-read-reviews">Read Reviews &rarr;</router-link>
            </div>
            <div class="test-img-col">
              <img
                src="/images/banner-skin-concerns.jpg"
                alt="Real Customer Reviews"
                class="test-model-img"
              />
            </div>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'
import {
  ChevronRight,
  ShieldCheck,
  Award,
  Sparkles,
  Users,
  LayoutGrid,
  List,
  Crown,
  Check,
} from 'lucide-vue-next'

const productsStore = useProductStore()

const selectedCategory = ref('all')
const sortBy = ref('rank')
const viewMode = ref('grid')

const categories = [
  { name: 'Cleansers', slug: 'cleansers' },
  { name: 'Toners', slug: 'toners' },
  { name: 'Serums', slug: 'serums' },
  { name: 'Moisturizers', slug: 'moisturizers' },
  { name: 'Sunscreens', slug: 'sunscreens' },
  { name: 'Masks', slug: 'masks' },
  { name: 'Treatments', slug: 'treatments' },
  { name: 'Kits & Sets', slug: 'kits' },
]

const bestSellersPool = computed(() => {
  return productsStore.products.filter(
    (p) => p.badge?.toLowerCase().includes('seller') || p.rating >= 4.7 || p.is_featured
  )
})

const filteredProducts = computed(() => {
  let list = [...bestSellersPool.value]

  if (selectedCategory.value !== 'all') {
    list = list.filter((p) => (p.category || '').toLowerCase() === selectedCategory.value.toLowerCase())
  }

  if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating)
  } else if (sortBy.value === 'price-asc') {
    list.sort((a, b) => a.price - b.price)
  } else if (sortBy.value === 'price-desc') {
    list.sort((a, b) => b.price - a.price)
  } else {
    // Default: Best Selling rank by reviews count
    list.sort((a, b) => (b.reviews || 0) - (a.reviews || 0))
  }

  return list
})
</script>

<style scoped>
.bestsellers-page {
  padding-bottom: 5rem;
  background-color: var(--bg-main, #FAF8F5);
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
}

.breadcrumb-link {
  color: #8E4A3E;
  text-decoration: none;
  font-weight: 500;
}

.breadcrumb-link:hover {
  color: #73382E;
  text-decoration: underline;
}

.breadcrumb-sep {
  color: #8E4A3E;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Hero Banner matching Best Sellers.png */
.banner-container {
  margin-bottom: 1.25rem;
}

.bestsellers-hero-card {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border: 1px solid rgba(196, 98, 60, 0.12);
  border-radius: 16px;
  padding: 1.75rem 2.5rem;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 2rem;
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
  position: relative;
  overflow: hidden;
  min-height: 275px;
}

.hero-left-content {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
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

.trust-badges-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.85rem;
  align-items: center;
}

.trust-badge-item {
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

.trust-title {
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

.hero-callout-circle {
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
  animation: ambientFloat 4.5s ease-in-out infinite;
  z-index: 3;
}

@keyframes ambientFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

.callout-italic {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.95rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.25;
}

/* Category Pills Bar */
.pills-container {
  margin-bottom: 2rem;
}

.category-pills-bar {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  scrollbar-width: none;
}

.category-pills-bar::-webkit-scrollbar {
  display: none;
}

.cat-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.15rem;
  border-radius: 9999px;
  font-size: 0.84rem;
  font-weight: 600;
  background: #FFFFFF;
  color: #383533;
  border: 1px solid #EAE5DF;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.cat-pill-btn:hover {
  border-color: #8E4A3E;
  color: #8E4A3E;
}

.cat-pill-btn.active {
  background: #7A2E22;
  color: #FFFFFF;
  border-color: #7A2E22;
}

/* Catalog Layout */
.catalog-section {
  margin-top: 1rem;
}

.catalog-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2.5rem;
  align-items: start;
}

/* Catalog Toolbar */
.catalog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #EAE5DF;
}

.results-count {
  font-size: 0.9rem;
  color: #383533;
}

.results-count strong {
  color: #1C1917;
  font-weight: 700;
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
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 0.4rem 0.85rem;
  background: #FFFFFF;
  font-size: 0.84rem;
  color: #8E4A3E;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}

.view-mode-toggle {
  display: flex;
  align-items: center;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  overflow: hidden;
}

.toggle-btn {
  background: #FFFFFF;
  border: none;
  padding: 0.4rem 0.6rem;
  color: #78716C;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.toggle-btn.active {
  background: #F4EFEB;
  color: #1C1917;
}

/* Ranked Cards Grid */
.bestsellers-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.bestsellers-grid.is-list-view {
  grid-template-columns: 1fr;
}

.ranked-card-wrapper {
  position: relative;
}

.rank-circle-badge {
  position: absolute;
  top: -8px;
  left: -8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #7A2E22;
  color: #FFFFFF;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(122, 46, 34, 0.35);
  z-index: 10;
}

/* Catalog Sidebar */
.catalog-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1.25rem);
}

.sidebar-info-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

/* Card 1: Why Best Sellers */
.why-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.why-crown-icon {
  color: #8E4A3E;
}

.why-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1.2;
}

.why-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.why-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: #383533;
}

.why-check {
  color: #8E4A3E;
  flex-shrink: 0;
}

/* Card 2: Shop by Category */
.sidebar-heading-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.sidebar-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #7A2E22;
}

.sidebar-link {
  font-size: 0.8rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.cat-mini-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.cat-mini-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  gap: 0.35rem;
}

.cat-mini-avatar {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #FAF5F0;
  border: 1px solid #EAE5DF;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.cat-mini-tile:hover .cat-mini-avatar {
  background: #7A2E22;
  border-color: #7A2E22;
}

.cat-letter {
  font-family: 'Playfair Display', Georgia, serif;
  font-weight: 700;
  font-size: 1rem;
  color: #8E4A3E;
  transition: color 0.2s ease;
}

.cat-mini-tile:hover .cat-letter {
  color: #FFFFFF;
}

.cat-mini-name {
  font-size: 0.68rem;
  color: #57534E;
  text-align: center;
  font-weight: 500;
}

/* Card 3: Testimonial Promo Banner */
.testimonial-promo-card {
  background: #F9EFEA;
  border: 1px solid rgba(142, 74, 62, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  overflow: hidden;
  padding: 1.25rem;
}

.test-text-col {
  flex: 1;
}

.test-promo-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1.2;
  margin-bottom: 0.35rem;
}

.test-promo-sub {
  font-size: 0.74rem;
  color: #57534E;
  line-height: 1.35;
  margin-bottom: 0.85rem;
}

.btn-read-reviews {
  display: inline-block;
  background: #7A2E22;
  color: #FFFFFF;
  padding: 0.4rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.76rem;
  font-weight: 700;
  text-decoration: none;
  transition: background-color 0.15s ease;
}

.btn-read-reviews:hover {
  background: #632218;
}

.test-img-col {
  width: 90px;
  height: 90px;
  flex-shrink: 0;
}

.test-model-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #FFFFFF;
}

/* Responsive */
@media (max-width: 992px) {
  .bestsellers-hero-card {
    flex-direction: column;
    padding: 2rem;
    text-align: center;
  }
  .trust-badges-grid {
    grid-template-columns: 1fr;
  }
  .catalog-layout {
    grid-template-columns: 1fr;
  }
  .catalog-sidebar {
    position: static;
  }
}
</style>
