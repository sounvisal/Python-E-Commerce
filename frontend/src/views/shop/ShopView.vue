<template>
  <div class="shop-view">
    <div class="container">
      <!-- 1. Breadcrumbs -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="sep">&gt;</span>
        <span class="current">Shop</span>
      </nav>

      <!-- 2. Shop All Hero Banner (Boxed card with format picture) -->
      <section class="shop-hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">Shop All Products</h1>
          <p class="hero-subtitle">Explore 100+ trusted skincare brands. Real products. Real results.</p>

          <!-- 4 Value Badges -->
          <div class="feature-badges-row">
            <div class="feature-badge">
              <ShieldCheck :size="16" class="feature-icon" />
              <span>100% Authentic</span>
            </div>
            <div class="feature-badge">
              <Globe :size="16" class="feature-icon" />
              <span>Global & Local Brands</span>
            </div>
            <div class="feature-badge">
              <Sparkles :size="16" class="feature-icon" />
              <span>Skincare Expert Picks</span>
            </div>
            <div class="feature-badge">
              <RotateCcw :size="16" class="feature-icon" />
              <span>Easy Returns</span>
            </div>
          </div>
        </div>

        <!-- Right Visual Stage with Format Picture -->
        <div class="hero-visual">
          <img
            src="/images/banners/banner-best-sellers-clean.jpg"
            alt="Curated skincare on travertine stone"
            class="hero-bottles-img"
          />
          <div class="hero-circular-callout">
            <span>Good<br />Skin Finds<br />Here.</span>
          </div>
        </div>
      </section>

      <!-- 3. Popular Brands Circle Badges Row (Exact Format Match) -->
      <section class="popular-brands-section">
        <div class="section-top-row">
          <h3 class="section-title">Popular Brands</h3>
          <router-link to="/#brands" class="see-all-link">
            <span>See All Brands</span>
            <ArrowRight :size="14" />
          </router-link>
        </div>

        <div class="brands-carousel-wrapper">
          <div class="brands-row" ref="brandsRowRef">
            <button
              v-for="brand in popularBrands"
              :key="brand.name"
              class="brand-circle-badge-btn"
              :class="{ active: selectedBrands.includes(brand.name) }"
              :title="brand.name"
              @click="toggleBrandFilter(brand.name)"
            >
              <BrandLogo :brand="brand.name" size="circle" />
            </button>
          </div>
          <button class="brands-scroll-arrow" @click="scrollBrandsRight" aria-label="More Brands">
            <ChevronRight :size="18" />
          </button>
        </div>
      </section>

      <!-- 4. Two-Column Layout (Sidebar Filters + Catalog Main) -->
      <div class="shop-layout">
        <!-- Sidebar Filters -->
        <aside class="shop-sidebar">
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

          <!-- Category Filter Accordion -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('category')">
              <span>Category</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.category }" />
            </button>
            <div v-show="accordions.category" class="accordion-body">
              <div class="checkbox-list">
                <label
                  v-for="cat in categoriesList"
                  :key="cat.slug"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="cat.slug"
                    v-model="selectedCategories"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ cat.name }}</span>
                  <span class="count">({{ cat.count }})</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Brand Filter Accordion -->
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
                  v-for="b in filteredBrandsList"
                  :key="b.name"
                  class="checkbox-item"
                >
                  <input
                    type="checkbox"
                    :value="b.name"
                    v-model="selectedBrands"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="label-text">{{ b.name }}</span>
                  <span class="count">({{ b.count }})</span>
                </label>
              </div>
              <button
                v-if="availableBrands.length > 8"
                class="show-more-btn"
                @click="showAllBrands = !showAllBrands"
              >
                {{ showAllBrands ? 'Show Less' : 'Show More' }}
              </button>
            </div>
          </div>

          <!-- Skin Concern Filter Accordion -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('concern')">
              <span>Skin Concern</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.concern }" />
            </button>
            <div v-show="accordions.concern" class="accordion-body">
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

          <!-- Skin Type Filter Accordion -->
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

          <!-- Price Range Filter Accordion -->
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
                  max="200"
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
                    placeholder="200"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Rating Filter Accordion -->
          <div class="filter-accordion">
            <button class="accordion-header" @click="toggleAccordion('rating')">
              <span>Rating</span>
              <ChevronDown :size="15" :class="{ rotated: !accordions.rating }" />
            </button>
            <div v-show="accordions.rating" class="accordion-body">
              <div class="checkbox-list">
                <label
                  v-for="r in ratingOptions"
                  :key="r.stars"
                  class="checkbox-item"
                >
                  <input
                    type="radio"
                    name="ratingFilter"
                    :value="r.stars"
                    v-model="selectedRating"
                    @change="onFilterChange"
                  />
                  <span class="custom-checkbox"></span>
                  <span class="stars-gold">{{ '★'.repeat(r.stars) }}{{ '☆'.repeat(5 - r.stars) }}</span>
                  <span class="label-text">&amp; Up</span>
                </label>
                <button
                  v-if="selectedRating"
                  class="clear-rating-btn"
                  @click="selectedRating = null; onFilterChange()"
                >
                  Reset Rating
                </button>
              </div>
            </div>
          </div>
        </aside>

        <!-- Main Product Listing Content -->
        <main class="shop-main">
          <!-- Top Results Bar -->
          <div class="catalog-top-bar">
            <div class="products-count-label">
              <strong>{{ displayProducts.length }}</strong> products
            </div>

            <div class="catalog-controls">
              <!-- Sort Dropdown -->
              <div class="sort-control">
                <label for="shopSort">Sort by:</label>
                <div class="sort-select-wrapper">
                  <select
                    id="shopSort"
                    v-model="sortBy"
                    @change="onFilterChange"
                    class="sort-dropdown"
                  >
                    <option value="popular">Best Match</option>
                    <option value="bestseller">Best Selling</option>
                    <option value="rating">Highest Rated</option>
                    <option value="newest">Newest Arrivals</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                  </select>
                  <ChevronDown :size="13" class="select-caret" />
                </div>
              </div>

              <!-- View Switcher -->
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
              <p>Try adjusting your search criteria or clearing applied filters.</p>
              <button class="btn btn-pill-dark" @click="clearAllFilters">
                Reset All Filters
              </button>
            </div>
          </div>

          <!-- Products Grid (4 Columns) -->
          <div
            v-else
            class="shop-products-grid"
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

          <!-- 5. Bottom Newsletter Beauty Updates Card -->
          <div class="newsletter-card">
            <div class="newsletter-content">
              <h2 class="newsletter-title">Beauty Updates<br>Straight to You.</h2>
              <p class="newsletter-desc">Be the first to know about new arrivals, exclusive offers, and skincare tips.</p>

              <form @submit.prevent="handleSubscribe" class="newsletter-form">
                <div class="email-input-wrapper">
                  <input
                    type="email"
                    v-model="subscriberEmail"
                    placeholder="Your email address"
                    required
                    class="email-input"
                  />
                  <button type="submit" class="newsletter-submit-btn" aria-label="Subscribe">
                    <ArrowRight :size="16" />
                  </button>
                </div>
              </form>
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
import { useNotificationStore } from '@/stores/notification'
import ProductCard from '@/components/ProductCard.vue'
import BrandLogo from '@/components/BrandLogo.vue'
import {
  ShieldCheck,
  Globe,
  Sparkles,
  RotateCcw,
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
const notificationStore = useNotificationStore()

// State
const brandsRowRef = ref(null)
const viewMode = ref('grid')
const brandSearch = ref('')
const showAllBrands = ref(false)
const selectedCategories = ref([])
const selectedBrands = ref([])
const selectedSkinConcerns = ref([])
const selectedSkinTypes = ref([])
const selectedRating = ref(null)
const priceMin = ref(0)
const priceMax = ref(200)
const sortBy = ref('popular')
const currentPage = ref(1)
const itemsPerPage = ref(12)
const subscriberEmail = ref('')

// Accordion open/close state
const accordions = reactive({
  category: true,
  brand: true,
  concern: true,
  skinType: true,
  price: true,
  rating: true,
})

const toggleAccordion = (key) => {
  accordions[key] = !accordions[key]
}

// Popular Brands matching Shop All Products.png
const popularBrands = [
  { name: 'SK-II', short: 'SK-II' },
  { name: 'The Ordinary', short: 'The Ordinary' },
  { name: 'CeraVe', short: 'CeraVe' },
  { name: 'LANEIGE', short: 'LANEIGE' },
  { name: 'BIODERMA', short: 'BIODERMA' },
  { name: 'La Roche-Posay', short: 'La Roche-Posay' },
  { name: 'innisfree', short: 'innisfree' },
  { name: 'COSRX', short: 'COSRX' },
  { name: 'Anua', short: 'Anua' },
  { name: 'Sulwhasoo', short: 'Sulwhasoo' },
]

// Categories List with counts
const categoriesList = [
  { name: 'Cleansers', slug: 'cleansers', count: 234 },
  { name: 'Toners', slug: 'toners', count: 112 },
  { name: 'Serums', slug: 'serums', count: 342 },
  { name: 'Moisturizers', slug: 'moisturizers', count: 298 },
  { name: 'Sunscreens', slug: 'sunscreens', count: 166 },
  { name: 'Masks', slug: 'masks', count: 87 },
  { name: 'Treatments', slug: 'treatments', count: 121 },
  { name: 'Kits & Sets', slug: 'kits', count: 98 },
]

// Available brands matching mockup
const availableBrands = [
  { name: 'SK-II', count: 24 },
  { name: 'The Ordinary', count: 56 },
  { name: 'CeraVe', count: 48 },
  { name: 'LANEIGE', count: 32 },
  { name: 'BIODERMA', count: 28 },
  { name: 'La Roche-Posay', count: 40 },
  { name: 'innisfree', count: 36 },
  { name: 'COSRX', count: 52 },
  { name: 'Anua', count: 18 },
  { name: 'Dr.Jart+', count: 22 },
  { name: 'Sulwhasoo', count: 14 },
  { name: 'Medicube', count: 8 },
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

const skinConcernsList = [
  { name: 'Acne & Blemishes', count: 220 },
  { name: 'Dryness', count: 198 },
  { name: 'Dullness', count: 176 },
  { name: 'Dark Spots', count: 142 },
  { name: 'Aging', count: 164 },
  { name: 'Sensitivity', count: 130 },
  { name: 'Oiliness', count: 168 },
  { name: 'Uneven Texture', count: 98 },
]

const skinTypesList = [
  { name: 'Normal', count: 312 },
  { name: 'Oily', count: 284 },
  { name: 'Dry', count: 276 },
  { name: 'Combination', count: 308 },
  { name: 'Sensitive', count: 212 },
]

const ratingOptions = [
  { stars: 5 },
  { stars: 4 },
  { stars: 3 },
]

const hasActiveFilters = computed(() => {
  return (
    selectedCategories.value.length > 0 ||
    selectedBrands.value.length > 0 ||
    selectedSkinConcerns.value.length > 0 ||
    selectedSkinTypes.value.length > 0 ||
    selectedRating.value !== null ||
    priceMin.value > 0 ||
    priceMax.value < 200
  )
})

const clearAllFilters = () => {
  selectedCategories.value = []
  selectedBrands.value = []
  selectedSkinConcerns.value = []
  selectedSkinTypes.value = []
  selectedRating.value = null
  priceMin.value = 0
  priceMax.value = 200
  brandSearch.value = ''
  currentPage.value = 1
}

const toggleBrandFilter = (brandName) => {
  const idx = selectedBrands.value.indexOf(brandName)
  if (idx > -1) {
    selectedBrands.value.splice(idx, 1)
  } else {
    selectedBrands.value.push(brandName)
  }
  currentPage.value = 1
}

const scrollBrandsRight = () => {
  if (brandsRowRef.value) {
    brandsRowRef.value.scrollBy({ left: 240, behavior: 'smooth' })
  }
}

const onFilterChange = () => {
  currentPage.value = 1
}

// Compute filtered catalog products
const displayProducts = computed(() => {
  let list = [...productStore.allCatalogProducts]

  // Category filter
  if (selectedCategories.value.length > 0) {
    list = list.filter((p) => selectedCategories.value.includes(p.category))
  }

  // Brands filter
  if (selectedBrands.value.length > 0) {
    list = list.filter((p) => selectedBrands.value.includes(p.brand))
  }

  // Skin Concerns filter
  if (selectedSkinConcerns.value.length > 0) {
    list = list.filter((p) =>
      p.skin_concern?.some((sc) => selectedSkinConcerns.value.includes(sc))
    )
  }

  // Skin Types filter
  if (selectedSkinTypes.value.length > 0) {
    list = list.filter((p) =>
      p.skin_type?.some((st) => selectedSkinTypes.value.includes(st))
    )
  }

  // Price min/max
  if (priceMin.value !== null) {
    list = list.filter((p) => p.price >= priceMin.value)
  }
  if (priceMax.value !== null) {
    list = list.filter((p) => p.price <= priceMax.value)
  }

  // Rating filter
  if (selectedRating.value !== null) {
    list = list.filter((p) => p.rating >= selectedRating.value)
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
    case 'bestseller':
      list.sort((a, b) => (b.badge?.includes('Seller') ? 1 : 0) - (a.badge?.includes('Seller') ? 1 : 0))
      break
    case 'popular':
    default:
      // Preserve catalog's curated sequence matching Shop All Products reference
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

const handleSubscribe = () => {
  notificationStore.addToast(`Subscribed! Check ${subscriberEmail.value} for 15% off`, 'success')
  subscriberEmail.value = ''
}

onMounted(() => {
  productStore.fetchCategories()
  productStore.fetchProducts()

  // Handle query params from URL (e.g. ?category=cleansers or ?brand=SK-II)
  if (route.query.category) {
    selectedCategories.value = [route.query.category]
  }
  if (route.query.brand) {
    selectedBrands.value = [route.query.brand]
  }
})

watch(
  () => route.query,
  (q) => {
    if (q.category && !selectedCategories.value.includes(q.category)) {
      selectedCategories.value = [q.category]
    }
    if (q.brand && !selectedBrands.value.includes(q.brand)) {
      selectedBrands.value = [q.brand]
    }
  }
)
</script>

<style scoped>
.shop-view {
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
   2. HERO BANNER (Boxed card layout with format travertine stage photo)
   ========================================================================== */
.shop-hero-banner {
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
  font-size: 1.15rem;
  font-weight: 500;
  color: #1C1917;
  margin-bottom: 1.25rem;
  line-height: 1.35;
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
   3. POPULAR BRANDS SECTION (Matches Shop All Products.png circular badges)
   ========================================================================== */
.popular-brands-section {
  margin-bottom: 1.25rem;
}

.section-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.95rem;
}

.section-title {
  font-family: var(--font-serif);
  font-size: 1.12rem;
  font-weight: 600;
  color: #7A2E22;
}

.see-all-link {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
  transition: transform 0.2s ease;
}

.see-all-link:hover {
  transform: translateX(2px);
}

.brands-carousel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.brands-row {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  overflow-x: auto;
  padding: 0.35rem 0.25rem;
  scrollbar-width: none;
  -ms-overflow-style: none;
  flex: 1;
}

.brands-row::-webkit-scrollbar {
  display: none;
}

.brand-circle-badge-btn {
  width: 74px;
  height: 74px;
  min-width: 74px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 1.2px solid rgba(28, 25, 23, 0.08);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.23, 1, 0.32, 1);
}

.brand-circle-badge-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  border-color: rgba(28, 25, 23, 0.25);
}

.brand-circle-badge-btn.active {
  border-color: #1C1917;
  box-shadow: 0 0 0 2px #1C1917, 0 4px 12px rgba(0, 0, 0, 0.08);
}

.brands-scroll-arrow {
  width: 42px;
  height: 42px;
  min-width: 42px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.12);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7A2E22;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.brands-scroll-arrow:hover {
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #7A2E22;
}

/* ==========================================================================
   4. TWO-COLUMN LAYOUT & STICKY FILTERS SIDEBAR
   ========================================================================== */
.shop-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2.25rem;
  align-items: start;
}

/* Sidebar: Stays still when scrolling products, scrolls on itself when hovering/scrolling */
.shop-sidebar {
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

.stars-gold {
  color: #F59E0B;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.clear-rating-btn {
  background: none;
  border: none;
  color: #8E4A3E;
  font-size: 0.75rem;
  cursor: pointer;
  text-decoration: underline;
  text-align: left;
  padding: 0.25rem 0;
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
.shop-main {
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

/* 4-Column Grid for Shop All */
.shop-products-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.15rem;
  margin-bottom: 2.5rem;
}

.shop-products-grid.is-list-view {
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
   5. BOTTOM NEWSLETTER CARD
   ========================================================================== */
.newsletter-card {
  background: #F4EFEB url('/images/banner-newsletter.jpg') no-repeat right center / cover;
  border-radius: 16px;
  border: 1px solid rgba(28, 25, 23, 0.06);
  padding: 2.75rem 3rem;
  position: relative;
  overflow: hidden;
}

.newsletter-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(244, 239, 235, 0.95) 0%, rgba(244, 239, 235, 0.85) 60%, rgba(244, 239, 235, 0.3) 100%);
  z-index: 1;
}

.newsletter-content {
  position: relative;
  z-index: 2;
  max-width: 540px;
}

.newsletter-title {
  font-family: var(--font-serif);
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
  font-weight: 600;
  color: #1C1917;
  line-height: 1.2;
  margin-bottom: 0.65rem;
}

.newsletter-desc {
  font-size: 0.92rem;
  color: #57534E;
  margin-bottom: 1.75rem;
}

.newsletter-form {
  max-width: 440px;
}

.email-input-wrapper {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 9999px;
  padding: 0.35rem 0.45rem 0.35rem 1.25rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
}

.email-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.85rem;
  color: #1C1917;
  outline: none;
}

.newsletter-submit-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.newsletter-submit-btn:hover {
  background: #242721;
  transform: scale(1.05);
}

/* ==========================================================================
   RESPONSIVE DESIGN
   ========================================================================== */
@media (max-width: 1200px) {
  .shop-products-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .shop-layout {
    grid-template-columns: 1fr;
  }
  .shop-sidebar {
    display: none;
  }
  .shop-products-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .shop-hero-banner {
    flex-direction: column;
    padding: 1.75rem;
  }
  .hero-visual {
    width: 100%;
    height: 200px;
    margin-top: 1rem;
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .shop-products-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
  }
  .feature-badges-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.65rem;
  }
  .newsletter-card {
    padding: 1.75rem;
  }
}
</style>
