<template>
  <div class="category-view">
    <div class="container">
      <!-- 1. Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="sep">&gt;</span>
        <router-link to="/shop">Shop</router-link>
        <span class="sep">&gt;</span>
        <span class="current">{{ categoryTitle }}</span>
      </nav>

      <!-- 2. Category Hero Banner (Boxed card with format picture) -->
      <section class="category-hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">{{ categoryTitle }}</h1>
          <p class="hero-subtitle">{{ categorySubtitle }}</p>
          <p class="hero-desc">{{ categoryDesc }}</p>

          <!-- 4 Feature Badges -->
          <div class="feature-badges-row">
            <div class="feature-badge">
              <Sparkles :size="16" class="feature-icon" />
              <span>Deep Cleansing</span>
            </div>
            <div class="feature-badge">
              <Leaf :size="16" class="feature-icon" />
              <span>Gentle Formulas</span>
            </div>
            <div class="feature-badge">
              <Droplets :size="16" class="feature-icon" />
              <span>For Every Skin Type</span>
            </div>
            <div class="feature-badge">
              <ShieldCheck :size="16" class="feature-icon" />
              <span>Trusted Brands</span>
            </div>
          </div>
        </div>

        <!-- Right Visual Stage with Format Picture -->
        <div class="hero-visual">
          <img
            src="/images/banners/banner-cleansers-clean.jpg"
            alt="Cleansers on warm travertine stone"
            class="hero-bottles-img"
          />
          <div class="hero-circular-callout">
            <span>Cleanse<br />Refresh<br />Balance<br />Repeat.</span>
          </div>
        </div>
      </section>

      <!-- 3. Subcategory Pills Bar -->
      <div class="subcategories-bar">
        <button
          class="subcat-pill"
          :class="{ active: activeSubcategory === '' }"
          @click="selectSubcategory('')"
        >
          All {{ categoryTitle }}
        </button>
        <button
          v-for="sub in subcategoriesList"
          :key="sub"
          class="subcat-pill"
          :class="{ active: activeSubcategory === sub }"
          @click="selectSubcategory(sub)"
        >
          {{ sub }}
        </button>
      </div>

      <!-- 4. Main Two-Column Layout (Sidebar + Catalog Grid) -->
      <div class="category-layout">
        <!-- Sidebar Filters -->
        <aside class="category-sidebar">
          <div class="sidebar-header">
            <h3>Filters</h3>
            <button
              v-if="hasActiveFilters"
              class="clear-all-btn"
              @click="clearAllFilters"
            >
              Clear All
            </button>
          </div>

          <!-- Filter Section: Brand -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('brand')">
              <span>Brand</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.brand }" />
            </button>
            <div v-show="accordions.brand" class="accordion-body">
              <div class="brand-search-box">
                <Search :size="14" class="search-icon" />
                <input
                  type="text"
                  v-model="brandSearch"
                  placeholder="Search brands..."
                  class="brand-search-input"
                />
              </div>
              <div class="checkbox-list">
                <label
                  v-for="brand in filteredBrandsList"
                  :key="brand.name"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="brand.name"
                    v-model="selectedBrands"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ brand.name }}</span>
                  <span class="count">({{ brand.count }})</span>
                </label>
              </div>
              <button
                v-if="availableBrands.length > 6"
                class="show-more-btn"
                @click="showAllBrands = !showAllBrands"
              >
                {{ showAllBrands ? 'Show Less' : 'Show More' }}
              </button>
            </div>
          </div>

          <!-- Filter Section: Price Range -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('price')">
              <span>Price Range</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.price }" />
            </button>
            <div v-show="accordions.price" class="accordion-body">
              <div class="price-slider-track">
                <input
                  type="range"
                  min="0"
                  max="100"
                  v-model.number="priceMax"
                  @input="onFilterChange"
                  class="range-slider"
                />
              </div>
              <div class="price-inputs-row">
                <div class="price-input-box">
                  <span class="currency">$</span>
                  <input
                    type="number"
                    v-model.number="priceMin"
                    @change="onFilterChange"
                    placeholder="0"
                  />
                </div>
                <span class="price-dash">-</span>
                <div class="price-input-box">
                  <span class="currency">$</span>
                  <input
                    type="number"
                    v-model.number="priceMax"
                    @change="onFilterChange"
                    placeholder="100"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Filter Section: Skin Type -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('skinType')">
              <span>Skin Type</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.skinType }" />
            </button>
            <div v-show="accordions.skinType" class="accordion-body">
              <div class="checkbox-list">
                <label
                  v-for="st in skinTypesList"
                  :key="st.name"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="st.name"
                    v-model="selectedSkinTypes"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ st.name }}</span>
                  <span class="count">({{ st.count }})</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Filter Section: Skin Concern -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('skinConcern')">
              <span>Skin Concern</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.skinConcern }" />
            </button>
            <div v-show="accordions.skinConcern" class="accordion-body">
              <div class="checkbox-list">
                <label
                  v-for="sc in skinConcernsList"
                  :key="sc.name"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="sc.name"
                    v-model="selectedSkinConcerns"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ sc.name }}</span>
                  <span class="count">({{ sc.count }})</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Filter Section: Product Type -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('productType')">
              <span>Product Type</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.productType }" />
            </button>
            <div v-show="accordions.productType" class="accordion-body">
              <div class="checkbox-list">
                <label
                  v-for="pt in productTypesList"
                  :key="pt.name"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="pt.name"
                    v-model="selectedProductTypes"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ pt.name }}</span>
                  <span class="count">({{ pt.count }})</span>
                </label>
              </div>
            </div>
          </div>
        </aside>

        <!-- Main Product Listing Content -->
        <main class="category-main">
          <!-- Top Results Bar -->
          <div class="catalog-top-bar">
            <div class="products-count-label">
              <strong>{{ displayProducts.length }}</strong> products
            </div>

            <div class="catalog-controls">
              <!-- Sort Dropdown -->
              <div class="sort-control">
                <label for="categorySort">Sort by:</label>
                <div class="sort-select-wrapper">
                  <select
                    id="categorySort"
                    v-model="sortBy"
                    @change="onFilterChange"
                    class="sort-dropdown"
                  >
                    <option value="popular">Best Selling</option>
                    <option value="rating">Highest Rated</option>
                    <option value="newest">New Arrivals</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                  </select>
                  <ChevronDown :size="13" class="select-caret" />
                </div>
              </div>

              <!-- View Switcher (Grid / List) -->
              <div class="view-switcher">
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  aria-label="Grid View"
                  title="Grid View"
                >
                  <LayoutGrid :size="16" />
                </button>
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  aria-label="List View"
                  title="List View"
                >
                  <List :size="16" />
                </button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="displayProducts.length === 0" class="no-results-state">
            <div class="no-results-card">
              <h3>No products found</h3>
              <p>We couldn't find any cleansers matching your selected filters.</p>
              <button class="btn btn-pill-dark" @click="clearAllFilters">
                Reset All Filters
              </button>
            </div>
          </div>

          <!-- 5-Column Product Grid -->
          <div
            v-else
            class="category-products-grid"
            :class="{ 'is-list-view': viewMode === 'list' }"
          >
            <ProductCard
              v-for="prod in paginatedProducts"
              :key="prod.id"
              :product="prod"
              :viewMode="viewMode"
            />
          </div>

          <!-- Pagination -->
          <div class="catalog-pagination" v-if="totalPages > 1">
            <button
              class="page-nav-btn"
              :disabled="currentPage === 1"
              @click="currentPage--"
              aria-label="Previous Page"
            >
              <ChevronLeft :size="16" />
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              class="page-num-btn"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>
            <button
              class="page-nav-btn"
              :disabled="currentPage === totalPages"
              @click="currentPage++"
              aria-label="Next Page"
            >
              <ChevronRight :size="16" />
            </button>
          </div>

          <!-- 5. Bottom Skin Quiz Promo Banner -->
          <div class="skin-quiz-card">
            <div class="quiz-content">
              <h2 class="quiz-title">Not Sure Which Cleanser Is Right for You?</h2>
              <p class="quiz-desc">Take a quick quiz and get personalized recommendations.</p>
              <router-link to="/#quiz" class="btn-quiz-cta">
                <span>Start Skin Quiz</span>
                <ArrowRight :size="15" />
              </router-link>
            </div>
            <div class="quiz-visual">
              <img
                src="/images/banner-skin-quiz.jpg"
                alt="Radiant skincare consultation model"
                class="quiz-model-img"
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '@/stores/products'
import ProductCard from '@/components/ProductCard.vue'
import {
  Sparkles,
  Leaf,
  Droplets,
  ShieldCheck,
  Search,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  LayoutGrid,
  List,
  ArrowRight,
} from 'lucide-vue-next'

const route = useRoute()
const productStore = useProductStore()

// State
const viewMode = ref('grid')
const brandSearch = ref('')
const showAllBrands = ref(false)
const activeSubcategory = ref('')
const selectedBrands = ref([])
const selectedSkinTypes = ref([])
const selectedSkinConcerns = ref([])
const selectedProductTypes = ref([])
const priceMin = ref(0)
const priceMax = ref(100)
const sortBy = ref('popular')
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Accordions State
const accordions = reactive({
  brand: true,
  price: true,
  skinType: true,
  skinConcern: true,
  productType: true,
})

const toggleAccordion = (key) => {
  accordions[key] = !accordions[key]
}

// Category meta from route or default to cleansers
const categorySlug = computed(() => route.params.slug || 'cleansers')

const currentCategory = computed(() => {
  return productStore.categories.find((c) => c.slug === categorySlug.value) || {
    name: 'Cleansers',
    slug: 'cleansers',
    desc: 'Find the perfect cleanser from top global brands. Remove impurities, excess oil, and makeup while keeping your skin balanced and refreshed.',
  }
})

const categoryTitle = computed(() => currentCategory.value.name || 'Cleansers')
const categorySubtitle = computed(() => 'The first step to healthy, radiant skin.')
const categoryDesc = computed(() => currentCategory.value.desc)

// Subcategories matching Category Product Listing.png
const subcategoriesList = [
  'Foam Cleanser',
  'Gel Cleanser',
  'Cream Cleanser',
  'Micellar Water',
  'Cleansing Oil',
  'Cleansing Balm',
  'Powder Cleanser',
]

// Brands matching Category Product Listing.png
const availableBrands = [
  { name: 'CeraVe', count: 24 },
  { name: 'La Roche-Posay', count: 18 },
  { name: 'SK-II', count: 12 },
  { name: 'innisfree', count: 16 },
  { name: 'The Ordinary', count: 10 },
  { name: 'COSRX', count: 14 },
  { name: 'LANEIGE', count: 8 },
  { name: 'BIODERMA', count: 11 },
  { name: 'Anua', count: 7 },
  { name: 'Dermalogica', count: 9 },
]

const filteredBrandsList = computed(() => {
  let list = availableBrands
  if (brandSearch.value) {
    const q = brandSearch.value.toLowerCase()
    list = list.filter((b) => b.name.toLowerCase().includes(q))
  }
  if (!showAllBrands.value && !brandSearch.value) {
    return list.slice(0, 8)
  }
  return list
})

const skinTypesList = [
  { name: 'Normal', count: 58 },
  { name: 'Oily', count: 42 },
  { name: 'Dry', count: 36 },
  { name: 'Combination', count: 40 },
  { name: 'Sensitive', count: 38 },
]

const skinConcernsList = [
  { name: 'Acne & Blemishes', count: 28 },
  { name: 'Oiliness', count: 32 },
  { name: 'Dryness', count: 18 },
  { name: 'Sensitivity', count: 24 },
  { name: 'Dullness', count: 16 },
  { name: 'Uneven Texture', count: 14 },
]

const productTypesList = [
  { name: 'Foam', count: 26 },
  { name: 'Gel', count: 30 },
  { name: 'Cream', count: 22 },
  { name: 'Micellar Water', count: 12 },
  { name: 'Oil', count: 8 },
]

// Check if any filter is applied
const hasActiveFilters = computed(() => {
  return (
    activeSubcategory.value !== '' ||
    selectedBrands.value.length > 0 ||
    selectedSkinTypes.value.length > 0 ||
    selectedSkinConcerns.value.length > 0 ||
    selectedProductTypes.value.length > 0 ||
    priceMin.value > 0 ||
    priceMax.value < 100
  )
})

const clearAllFilters = () => {
  activeSubcategory.value = ''
  selectedBrands.value = []
  selectedSkinTypes.value = []
  selectedSkinConcerns.value = []
  selectedProductTypes.value = []
  priceMin.value = 0
  priceMax.value = 100
  brandSearch.value = ''
  currentPage.value = 1
}

const selectSubcategory = (sub) => {
  activeSubcategory.value = sub
  currentPage.value = 1
}

const onFilterChange = () => {
  currentPage.value = 1
}

// Compute filtered cleanser products
const displayProducts = computed(() => {
  // Grab all cleansers from store
  let list = productStore.allCatalogProducts.filter(
    (p) => p.category === categorySlug.value
  )

  // If specific subcategory selected
  if (activeSubcategory.value) {
    list = list.filter(
      (p) => p.subcategory?.toLowerCase() === activeSubcategory.value.toLowerCase()
    )
  }

  // Brands filter
  if (selectedBrands.value.length > 0) {
    list = list.filter((p) => selectedBrands.value.includes(p.brand))
  }

  // Skin Type filter
  if (selectedSkinTypes.value.length > 0) {
    list = list.filter((p) =>
      p.skin_type?.some((st) => selectedSkinTypes.value.includes(st))
    )
  }

  // Skin Concern filter
  if (selectedSkinConcerns.value.length > 0) {
    list = list.filter((p) =>
      p.skin_concern?.some((sc) => selectedSkinConcerns.value.includes(sc))
    )
  }

  // Product Type filter
  if (selectedProductTypes.value.length > 0) {
    list = list.filter((p) => selectedProductTypes.value.includes(p.product_type))
  }

  // Price range
  if (priceMin.value !== null) {
    list = list.filter((p) => p.price >= priceMin.value)
  }
  if (priceMax.value !== null) {
    list = list.filter((p) => p.price <= priceMax.value)
  }

  // Sorting
  switch (sortBy.value) {
    case 'price_asc':
      list.sort((a, b) => a.price - b.price)
      break
    case 'price_desc':
      list.sort((a, b) => b.price - a.price)
      break
    case 'rating':
      list.sort((a, b) => b.rating - a.rating)
      break
    case 'newest':
      list.sort((a, b) => (b.badge === 'New' ? 1 : 0) - (a.badge === 'New' ? 1 : 0))
      break
    case 'popular':
    default:
      // Exact curated sequence matching Category Product Listing reference
      list.sort((a, b) => {
        const order = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
        const idxA = order.indexOf(a.id)
        const idxB = order.indexOf(b.id)
        if (idxA !== -1 && idxB !== -1) return idxA - idxB
        return (a.id || 0) - (b.id || 0)
      })
      break
  }

  return list
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(displayProducts.value.length / itemsPerPage.value))
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return displayProducts.value.slice(start, start + itemsPerPage.value)
})

onMounted(() => {
  productStore.fetchCategories()
  productStore.fetchProducts()
})

watch(
  () => route.params.slug,
  () => {
    clearAllFilters()
  }
)
</script>

<style scoped>
.category-view {
  background-color: var(--bg-main);
  padding-bottom: 4rem;
}

/* ==========================================================================
   1. BREADCRUMBS
   ========================================================================== */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  padding: 0.6rem 0 0.5rem;
}

.breadcrumb-nav a {
  color: #8E4A3E;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-nav a:hover {
  color: #73382E;
  text-decoration: underline;
}

.breadcrumb-nav .sep {
  color: #8E4A3E;
  font-size: 0.75rem;
  font-weight: 600;
}

.breadcrumb-nav .current {
  color: #1C1917;
  font-weight: 600;
}

/* ==========================================================================
   2. CATEGORY HERO BANNER (Boxed card with format travertine stage photo)
   ========================================================================== */
.category-hero-banner {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border-radius: 16px;
  border: 1px solid rgba(196, 98, 60, 0.12);
  padding: 1.75rem 2.5rem;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  min-height: 275px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
}

.hero-content {
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

.hero-subtitle {
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

.feature-badges-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1.25rem;
}

.feature-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
}

.feature-icon {
  color: #8E2B2B;
}

.hero-visual {
  position: relative;
  width: 480px;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
  z-index: 1;
}

.hero-bottles-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  mask-image: linear-gradient(to right, transparent 0%, black 18%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 18%);
  box-shadow: 0 8px 24px rgba(40, 20, 10, 0.06);
}

.hero-circular-callout {
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

.hero-circular-callout span {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.2;
}

/* ==========================================================================
   3. SUBCATEGORY PILLS BAR
   ========================================================================== */
.subcategories-bar {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  margin-bottom: 2rem;
  scrollbar-width: thin;
}

.subcategories-bar::-webkit-scrollbar {
  height: 4px;
}
.subcategories-bar::-webkit-scrollbar-thumb {
  background: rgba(28, 25, 23, 0.15);
  border-radius: 4px;
}

.subcat-pill {
  white-space: nowrap;
  padding: 0.55rem 1.15rem;
  border-radius: 9999px;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.1);
  font-size: 0.82rem;
  font-weight: 500;
  color: #57534E;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.subcat-pill:hover {
  border-color: #1C1917;
  color: #1C1917;
  transform: translateY(-1px);
}

.subcat-pill.active {
  background: #8E4A3E;
  color: #FFFFFF;
  border-color: #8E4A3E;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.2);
}

/* ==========================================================================
   4. TWO-COLUMN LAYOUT & STICKY FILTERS SIDEBAR
   ========================================================================== */
.category-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2.25rem;
  align-items: start;
}

/* Sidebar: Stays still when scrolling products, scrolls on itself when hovering/scrolling */
.category-sidebar {
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1.25rem);
  max-height: calc(100vh - var(--navbar-height, 68px) - 2rem);
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(28, 25, 23, 0.2) transparent;
  background: #FFFFFF;
  border-radius: 14px;
  border: 1px solid rgba(28, 25, 23, 0.08);
  padding: 1.25rem;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
  margin-bottom: 1rem;
}

.sidebar-header h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1C1917;
}

.clear-all-btn {
  background: none;
  border: none;
  font-size: 0.76rem;
  color: #8E4A3E;
  cursor: pointer;
  font-weight: 600;
  text-decoration: underline;
  padding: 0;
}

.clear-all-btn:hover {
  color: #A05246;
}

.filter-accordion {
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.filter-accordion:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.accordion-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: none;
  border: none;
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  cursor: pointer;
  padding: 0.25rem 0;
}

.accordion-header .rotated {
  transform: rotate(-90deg);
  transition: transform 0.2s ease;
}

.accordion-body {
  margin-top: 0.75rem;
}

/* Brand Search */
.brand-search-box {
  position: relative;
  margin-bottom: 0.75rem;
}

.brand-search-box .search-icon {
  position: absolute;
  top: 50%;
  left: 0.65rem;
  transform: translateY(-50%);
  color: #A8A29E;
}

.brand-search-input {
  width: 100%;
  padding: 0.45rem 0.65rem 0.45rem 2rem;
  font-size: 0.78rem;
  border-radius: 6px;
  border: 1px solid rgba(28, 25, 23, 0.12);
  background: #FAF8F5;
  outline: none;
  transition: border-color 0.2s ease;
}

.brand-search-input:focus {
  border-color: #1C1917;
  background: #FFFFFF;
}

/* Checkboxes */
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 220px;
  overflow-y: auto;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-size: 0.8rem;
  color: #57534E;
  cursor: pointer;
  user-select: none;
}

.checkbox-item input {
  display: none;
}

.custom-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid rgba(28, 25, 23, 0.2);
  background: #FFFFFF;
  display: inline-block;
  position: relative;
  transition: all 0.15s ease;
}

.checkbox-item input:checked + .custom-checkbox {
  background: #8E4A3E;
  border-color: #8E4A3E;
}

.checkbox-item input:checked + .custom-checkbox::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 5px;
  width: 4px;
  height: 8px;
  border: solid #FFFFFF;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-item .label-text {
  flex: 1;
}

.checkbox-item .count {
  color: #A8A29E;
  font-size: 0.75rem;
}

.show-more-btn {
  background: none;
  border: none;
  font-size: 0.78rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  margin-top: 0.5rem;
  padding: 0;
  text-decoration: underline;
}

/* Price Slider */
.price-slider-track {
  margin: 0.5rem 0 1rem;
}

.range-slider {
  width: 100%;
  accent-color: #8E4A3E;
  cursor: pointer;
}

.price-inputs-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-input-box {
  display: flex;
  align-items: center;
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  padding: 0.35rem 0.5rem;
  flex: 1;
}

.price-input-box .currency {
  font-size: 0.8rem;
  color: #8C877F;
  margin-right: 0.25rem;
}

.price-input-box input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  outline: none;
}

.price-dash {
  color: #8C877F;
  font-weight: 600;
}

/* ==========================================================================
   MAIN PRODUCTS CONTENT
   ========================================================================== */
.category-main {
  display: flex;
  flex-direction: column;
}

.catalog-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.products-count-label {
  font-size: 0.92rem;
  color: #57534E;
}

.products-count-label strong {
  color: #1C1917;
  font-weight: 700;
}

.catalog-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: #57534E;
}

.sort-select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.sort-dropdown {
  appearance: none;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  padding: 0.45rem 2rem 0.45rem 0.8rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  outline: none;
}

.select-caret {
  position: absolute;
  right: 0.65rem;
  pointer-events: none;
  color: #78716C;
}

.view-switcher {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  overflow: hidden;
}

.view-btn {
  background: none;
  border: none;
  padding: 0.45rem 0.55rem;
  cursor: pointer;
  color: #8C877F;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.view-btn.active {
  background: #F4EFEB;
  color: #1C1917;
}

/* 5-Column Grid */
.category-products-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.category-products-grid.is-list-view {
  grid-template-columns: 1fr;
  gap: 0.85rem;
}

/* Empty State */
.no-results-state {
  background: #FFFFFF;
  border-radius: 14px;
  border: 1px dashed rgba(28, 25, 23, 0.15);
  padding: 3.5rem 2rem;
  text-align: center;
  margin-bottom: 2.5rem;
}

.no-results-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.no-results-card p {
  color: #78716C;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

/* Pagination */
.catalog-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  margin-bottom: 3.5rem;
}

.page-num-btn,
.page-nav-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(28, 25, 23, 0.08);
  background: #FFFFFF;
  font-size: 0.85rem;
  font-weight: 600;
  color: #57534E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-num-btn:hover:not(:disabled),
.page-nav-btn:hover:not(:disabled) {
  border-color: #1C1917;
  color: #1C1917;
  transform: translateY(-1px);
}

.page-num-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
  border-color: #8E4A3E;
}

.page-nav-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ==========================================================================
   5. SKIN QUIZ PROMO BANNER
   ========================================================================== */
.skin-quiz-card {
  background: linear-gradient(135deg, #F5EAE1 0%, #F1DFD3 100%);
  border-radius: 16px;
  border: 1px solid rgba(28, 25, 23, 0.06);
  padding: 2.25rem 2.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
  position: relative;
}

.quiz-content {
  max-width: 520px;
  z-index: 2;
}

.quiz-title {
  font-family: var(--font-serif);
  font-size: clamp(1.4rem, 2.5vw, 1.85rem);
  font-weight: 600;
  color: #1C1917;
  line-height: 1.25;
  margin-bottom: 0.5rem;
}

.quiz-desc {
  font-size: 0.92rem;
  color: #57534E;
  margin-bottom: 1.5rem;
}

.btn-quiz-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.6rem;
  border-radius: 9999px;
  background: #8E4A3E;
  color: #FFFFFF;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.btn-quiz-cta:hover {
  background: #242721;
  color: #FFFFFF;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(36, 39, 33, 0.15);
}

.quiz-visual {
  position: relative;
  width: 320px;
  height: 180px;
  border-radius: 12px;
  overflow: hidden;
}

.quiz-model-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;
}

/* ==========================================================================
   RESPONSIVE DESIGN
   ========================================================================== */
@media (max-width: 1200px) {
  .category-products-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .category-layout {
    grid-template-columns: 1fr;
  }
  .category-sidebar {
    display: none; /* Can be expanded via a filter drawer */
  }
  .category-products-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .category-hero-banner {
    flex-direction: column;
    padding: 1.75rem;
  }
  .hero-visual {
    width: 100%;
    height: 200px;
    margin-top: 1rem;
    justify-content: center;
  }
  .skin-quiz-card {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  .quiz-visual {
    width: 100%;
    height: 180px;
  }
}

@media (max-width: 640px) {
  .category-products-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
  }
  .feature-badges-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.65rem;
  }
}
</style>
