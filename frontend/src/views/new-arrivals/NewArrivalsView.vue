<template>
  <div class="new-arrivals-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">New Arrivals</span>
      </nav>
    </div>

    <!-- Hero Banner matching New Arrivals.png -->
    <section class="container banner-container">
      <div class="new-arrivals-hero-card">
        <div class="hero-left-content">
          <h1 class="hero-title">New Arrivals</h1>
          <h2 class="hero-tagline">Fresh Finds for Healthier, Happier Skin.</h2>
          <p class="hero-desc">
            Be the first to discover the latest skincare launches from your favorite brands. New innovations. New routines. A more radiant you.
          </p>

          <div class="trust-badges-grid">
            <div class="trust-badge-item">
              <Sparkles :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Latest Formulas</span>
                <span class="trust-sub">Be first to try</span>
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
              <Truck :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Fresh Arrivals</span>
                <span class="trust-sub">Updated regularly</span>
              </div>
            </div>
            <div class="trust-badge-item">
              <Gift :size="20" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-title">Exclusive Launches</span>
                <span class="trust-sub">Only at Luméa</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero-right-visual">
          <div class="hero-stage-wrap">
            <img
              src="/images/banners/banner-new-arrivals-clean.jpg"
              alt="Luméa New Arrivals Skincare Showcase"
              class="hero-packshot-img"
            />
            <div class="hero-callout-circle">
              <span class="callout-italic">New<br />Brands.<br />New Beauty<br />Possibilities.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Category Filter Pills Bar matching New Arrivals.png -->
    <section class="container pills-container">
      <div class="category-pills-bar">
        <button
          class="cat-pill-btn"
          :class="{ active: selectedCategory === 'all' }"
          @click="selectedCategory = 'all'"
        >
          <Sparkles :size="16" />
          <span>All New Arrivals</span>
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

    <!-- Main Content: 3-Column Layout (Filters Left, Products Center, Editorial Right) -->
    <section class="container catalog-section">
      <div class="arrivals-three-col-layout">
        <!-- Left Filters Sidebar -->
        <aside class="filters-sidebar">
          <div class="filters-header">
            <h3 class="filters-title">Filters</h3>
            <button @click="resetFilters" class="btn-clear-all">Clear All</button>
          </div>

          <!-- Filter: Brand -->
          <div class="filter-group">
            <h4 class="filter-heading">Brand</h4>
            <div class="filter-search-box">
              <Search :size="14" class="filter-search-icon" />
              <input
                type="text"
                v-model="brandSearch"
                placeholder="Search brands..."
                class="filter-search-input"
              />
            </div>
            <div class="filter-options-list">
              <label
                v-for="brand in filteredBrandOptions"
                :key="brand.name"
                class="filter-checkbox-label"
              >
                <input
                  type="checkbox"
                  :value="brand.name"
                  v-model="selectedBrands"
                  class="filter-checkbox"
                />
                <span class="filter-name">{{ brand.name }}</span>
                <span class="filter-count">({{ brand.count }})</span>
              </label>
            </div>
          </div>

          <!-- Filter: Price Range -->
          <div class="filter-group">
            <h4 class="filter-heading">Price Range</h4>
            <div class="price-slider-wrap">
              <input
                type="range"
                min="0"
                max="200"
                step="5"
                v-model.number="maxPrice"
                class="price-slider"
              />
              <div class="price-inputs-row">
                <span class="price-tag">$0</span>
                <span class="price-tag">Up to ${{ maxPrice }}</span>
              </div>
            </div>
          </div>

          <!-- Filter: Skin Concern -->
          <div class="filter-group">
            <h4 class="filter-heading">Skin Concern</h4>
            <div class="filter-options-list">
              <label
                v-for="concern in concernsList"
                :key="concern"
                class="filter-checkbox-label"
              >
                <input
                  type="checkbox"
                  :value="concern"
                  v-model="selectedConcerns"
                  class="filter-checkbox"
                />
                <span class="filter-name">{{ concern }}</span>
              </label>
            </div>
          </div>
        </aside>

        <!-- Center Catalog Grid -->
        <main class="arrivals-main-catalog">
          <!-- Toolbar -->
          <div class="catalog-toolbar">
            <span class="results-count"><strong>{{ filteredProducts.length }}</strong> new arrivals</span>

            <div class="toolbar-actions">
              <div class="sort-select-wrapper">
                <span class="sort-label">Sort by:</span>
                <select v-model="sortBy" class="sort-select" aria-label="Sort arrivals">
                  <option value="newest">Newest First</option>
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

          <!-- Products Grid -->
          <div class="products-grid" :class="{ 'is-list-view': viewMode === 'list' }">
            <ProductCard
              v-for="product in filteredProducts"
              :key="product.id"
              :product="product"
              :view-mode="viewMode"
            />
          </div>
        </main>

        <!-- Right Promotional Editorial Sidebar matching New Arrivals.png -->
        <aside class="editorial-sidebar">
          <!-- Card 1: Just Launched -->
          <div class="editorial-card just-launched-card">
            <h3 class="ed-title">Just Launched</h3>
            <p class="ed-sub">Discover what's new in luxury skincare formulations.</p>
            <router-link to="/shop" class="btn-ed-terracotta">Explore New Arrivals &rarr;</router-link>
          </div>

          <!-- Card 2: Meet the New Brands -->
          <div class="editorial-card meet-brands-card">
            <h3 class="ed-title">Meet the<br />New Brands</h3>
            <p class="ed-sub">Explore the latest curated global brands now at Luméa.</p>
            <router-link to="/brands" class="btn-ed-terracotta">View All Brands &rarr;</router-link>
          </div>

          <!-- Card 3: Skincare Innovation -->
          <div class="editorial-card innovation-card">
            <h3 class="ed-title">Skincare Innovation<br />Never Stops</h3>
            <p class="ed-sub">New bio-compatible solutions for every skincare journey.</p>
            <router-link to="/journal" class="btn-ed-terracotta">Read Our Journal &rarr;</router-link>
          </div>

          <!-- Card 4: Recently Launched Brands -->
          <div class="editorial-card recent-brands-bubble-card">
            <div class="recent-brands-header">
              <h4 class="bubble-title">Recently Launched Brands</h4>
              <router-link to="/brands" class="bubble-view-all">View All &rarr;</router-link>
            </div>
            <div class="brands-bubble-grid">
              <router-link to="/brand/anua" class="brand-bubble-item">
                <div class="bubble-circle"><span>Anua</span></div>
              </router-link>
              <router-link to="/brand/tirtir" class="brand-bubble-item">
                <div class="bubble-circle"><span>TIRTIR</span></div>
              </router-link>
              <router-link to="/brand/medicube" class="brand-bubble-item">
                <div class="bubble-circle"><span>medicube</span></div>
              </router-link>
              <router-link to="/brand/boj" class="brand-bubble-item">
                <div class="bubble-circle"><span>Beauty of Joseon</span></div>
              </router-link>
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
  Sparkles,
  ShieldCheck,
  Truck,
  Gift,
  Search,
  LayoutGrid,
  List,
} from 'lucide-vue-next'

const productsStore = useProductStore()

const selectedCategory = ref('all')
const sortBy = ref('newest')
const viewMode = ref('grid')
const maxPrice = ref(200)
const brandSearch = ref('')
const selectedBrands = ref([])
const selectedConcerns = ref([])

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

const concernsList = [
  'Acne & Blemishes',
  'Dark Spots',
  'Aging',
  'Dryness',
  'Oiliness',
  'Sensitivity',
  'Dullness',
  'Uneven Texture',
]

const availableBrands = [
  { name: 'Anua', count: 8 },
  { name: 'Beauty of Joseon', count: 6 },
  { name: 'SK-II', count: 4 },
  { name: 'LANEIGE', count: 5 },
  { name: 'COSRX', count: 7 },
  { name: 'The Ordinary', count: 5 },
  { name: 'innisfree', count: 4 },
  { name: 'La Roche-Posay', count: 4 },
  { name: 'CeraVe', count: 3 },
]

const filteredBrandOptions = computed(() => {
  if (!brandSearch.value) return availableBrands
  const q = brandSearch.value.toLowerCase()
  return availableBrands.filter((b) => b.name.toLowerCase().includes(q))
})

const resetFilters = () => {
  selectedCategory.value = 'all'
  selectedBrands.value = []
  selectedConcerns.value = []
  maxPrice.value = 200
  brandSearch.value = ''
}

const filteredProducts = computed(() => {
  let list = productsStore.products.map((p) => ({
    ...p,
    badge: p.badge || 'New',
  }))

  if (selectedCategory.value !== 'all') {
    list = list.filter((p) => (p.category || '').toLowerCase() === selectedCategory.value.toLowerCase())
  }

  if (selectedBrands.value.length > 0) {
    list = list.filter((p) => selectedBrands.value.includes(p.brand))
  }

  if (selectedConcerns.value.length > 0) {
    list = list.filter((p) =>
      p.skin_concern?.some((c) => selectedConcerns.value.includes(c))
    )
  }

  list = list.filter((p) => p.price <= maxPrice.value)

  if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating)
  } else if (sortBy.value === 'price-asc') {
    list.sort((a, b) => a.price - b.price)
  } else if (sortBy.value === 'price-desc') {
    list.sort((a, b) => b.price - a.price)
  }

  return list
})
</script>

<style scoped>
.new-arrivals-page {
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

/* Hero Banner matching New Arrivals.png */
.banner-container {
  margin-bottom: 1.25rem;
}

.new-arrivals-hero-card {
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

/* 3-Column Layout */
.catalog-section {
  margin-top: 1rem;
}

.arrivals-three-col-layout {
  display: grid;
  grid-template-columns: 240px 1fr 280px;
  gap: 2rem;
  align-items: start;
}

/* Filters Sidebar */
.filters-sidebar {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1rem);
}

.filters-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #EAE5DF;
}

.filters-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1C1917;
}

.btn-clear-all {
  background: none;
  border: none;
  color: #8E4A3E;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-heading {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.75rem;
}

.filter-search-box {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.35rem 0.6rem;
  margin-bottom: 0.75rem;
}

.filter-search-icon {
  color: #78716C;
}

.filter-search-input {
  border: none;
  background: transparent;
  font-size: 0.78rem;
  outline: none;
  width: 100%;
}

.filter-options-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
}

.filter-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #383533;
  cursor: pointer;
}

.filter-checkbox {
  accent-color: #7A2E22;
}

.filter-count {
  margin-left: auto;
  color: #78716C;
  font-size: 0.75rem;
}

.price-slider-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.price-slider {
  accent-color: #8E4A3E;
  cursor: pointer;
}

.price-inputs-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: #78716C;
}

/* Center Catalog */
.catalog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid #EAE5DF;
}

.results-count {
  font-size: 0.9rem;
  color: #383533;
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
}

.toggle-btn.active {
  background: #F4EFEB;
  color: #1C1917;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.products-grid.is-list-view {
  grid-template-columns: 1fr;
}

/* Editorial Sidebar Right */
.editorial-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1rem);
}

.editorial-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.just-launched-card {
  background: linear-gradient(135deg, #FBF2EE 0%, #F5EAE4 100%);
  border: 1px solid rgba(142, 74, 62, 0.15);
}

.meet-brands-card {
  background: linear-gradient(135deg, #EEF5F0 0%, #E5EEE8 100%);
  border: 1px solid rgba(34, 100, 50, 0.12);
}

.innovation-card {
  background: linear-gradient(135deg, #F8F4F0 0%, #EDE5DC 100%);
  border: 1px solid rgba(142, 74, 62, 0.12);
}

.ed-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #7A2E22;
  margin-bottom: 0.35rem;
  line-height: 1.2;
}

.ed-sub {
  font-size: 0.74rem;
  color: #57534E;
  line-height: 1.35;
  margin-bottom: 0.85rem;
}

.btn-ed-terracotta {
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

.btn-ed-terracotta:hover {
  background: #632218;
}

/* Bubble Card */
.recent-brands-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.bubble-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #7A2E22;
}

.bubble-view-all {
  font-size: 0.74rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.brands-bubble-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.65rem;
}

.brand-bubble-item {
  text-decoration: none;
}

.bubble-circle {
  height: 48px;
  border-radius: 9999px;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 0.5rem;
  text-align: center;
  transition: all 0.2s ease;
}

.bubble-circle span {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
}

.brand-bubble-item:hover .bubble-circle {
  border-color: #8E4A3E;
  background: #F8F4F0;
}

/* Responsive */
@media (max-width: 1200px) {
  .arrivals-three-col-layout {
    grid-template-columns: 220px 1fr;
  }
  .editorial-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .new-arrivals-hero-card {
    flex-direction: column;
    padding: 2rem;
    text-align: center;
  }
  .arrivals-three-col-layout {
    grid-template-columns: 1fr;
  }
  .filters-sidebar {
    position: static;
  }
}
</style>
