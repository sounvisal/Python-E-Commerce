<template>
  <div class="search-results-page">
    <!-- Breadcrumbs matching Search Results.png -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">Search</span>
      </nav>
    </div>

    <!-- Hero Banner matching Search Results.png -->
    <section class="container banner-container">
      <div class="search-hero-card">
        <div class="search-hero-left">
          <h1 class="search-hero-title">Search Results</h1>
          <p class="search-hero-subtitle">
            Showing results for <strong>“{{ activeQuery }}”</strong>
          </p>

          <!-- Scope Tabs INSIDE Hero Banner matching Search Results.png -->
          <div class="hero-scope-tabs">
            <button
              class="hero-scope-tab"
              :class="{ active: activeScope === 'all' }"
              @click="activeScope = 'all'"
            >
              All Results ({{ allResultsCount }})
            </button>
            <button
              class="hero-scope-tab"
              :class="{ active: activeScope === 'products' }"
              @click="activeScope = 'products'"
            >
              Products ({{ productsCount }})
            </button>
            <button
              class="hero-scope-tab"
              :class="{ active: activeScope === 'brands' }"
              @click="activeScope = 'brands'"
            >
              Brands ({{ brandsCount }})
            </button>
            <button
              class="hero-scope-tab"
              :class="{ active: activeScope === 'articles' }"
              @click="activeScope = 'articles'"
            >
              Articles (20)
            </button>
          </div>
        </div>

        <div class="search-hero-right">
          <div class="hero-stage-wrapper">
            <img
              src="/images/banners/banner-search-clean.jpg"
              alt="Search Discovery Stage"
              class="search-stage-hero-img"
            />
            <div class="hero-circular-callout">
              <span>Real<br />Ingredients.<br />Real Results.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3-Column Search Layout matching Search Results.png -->
    <section class="container search-main-container">
      <div class="search-three-columns">
        <!-- 1. Left Column: Filters Accordion -->
        <aside class="search-filters-col">
          <div class="filters-panel">
            <div class="filters-panel-header">
              <span class="filters-panel-title">Filters</span>
              <button @click="resetFilters" class="clear-all-link">Clear All</button>
            </div>

            <!-- Group 1: Category -->
            <div class="filter-group">
              <div class="filter-group-header" @click="catOpen = !catOpen">
                <span class="fg-title">Category</span>
                <ChevronUp v-if="catOpen" :size="16" />
                <ChevronDown v-else :size="16" />
              </div>
              <div v-show="catOpen" class="filter-checklist">
                <label v-for="cat in categoryCounts" :key="cat.name" class="filter-check-row">
                  <input type="checkbox" :value="cat.name" v-model="selectedCategories" class="f-check" />
                  <span class="f-label">{{ cat.name }} ({{ cat.count }})</span>
                </label>
              </div>
            </div>

            <!-- Group 2: Brand with Search Input -->
            <div class="filter-group">
              <div class="filter-group-header" @click="brandOpen = !brandOpen">
                <span class="fg-title">Brand</span>
                <ChevronUp v-if="brandOpen" :size="16" />
                <ChevronDown v-else :size="16" />
              </div>
              <div v-show="brandOpen" class="filter-brand-content">
                <div class="brand-filter-search">
                  <Search :size="13" class="bfs-icon" />
                  <input
                    type="text"
                    v-model="brandSearchInput"
                    placeholder="Search brands..."
                    class="bfs-input"
                  />
                </div>
                <div class="filter-checklist brand-list-scroll">
                  <label v-for="b in filteredBrandChecklist" :key="b.name" class="filter-check-row">
                    <input type="checkbox" :value="b.name" v-model="selectedBrands" class="f-check" />
                    <span class="f-label">{{ b.name }} ({{ b.count }})</span>
                  </label>
                </div>
                <button class="show-more-brands-btn">Show More</button>
              </div>
            </div>

            <!-- Group 3: Price Range with inputs -->
            <div class="filter-group">
              <div class="filter-group-header" @click="priceOpen = !priceOpen">
                <span class="fg-title">Price Range</span>
                <ChevronUp v-if="priceOpen" :size="16" />
                <ChevronDown v-else :size="16" />
              </div>
              <div v-show="priceOpen" class="price-slider-content">
                <div class="price-slider-track">
                  <span class="p-min-lbl">$0</span>
                  <div class="p-bar"><div class="p-fill"></div></div>
                  <span class="p-max-lbl">$200+</span>
                </div>
                <div class="price-boxes-row">
                  <div class="price-box">
                    <span>$</span>
                    <input type="number" v-model.number="minPrice" placeholder="0" />
                  </div>
                  <span class="p-dash">–</span>
                  <div class="price-box">
                    <span>$</span>
                    <input type="number" v-model.number="maxPrice" placeholder="200" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Group 4: Rating -->
            <div class="filter-group">
              <div class="filter-group-header" @click="ratingOpen = !ratingOpen">
                <span class="fg-title">Rating</span>
                <ChevronUp v-if="ratingOpen" :size="16" />
                <ChevronDown v-else :size="16" />
              </div>
              <div v-show="ratingOpen" class="filter-checklist">
                <label v-for="r in [5, 4, 3]" :key="r" class="filter-check-row">
                  <input type="checkbox" :value="r" v-model="selectedRating" class="f-check" />
                  <div class="stars-preview">
                    <Star v-for="i in r" :key="i" :size="12" class="star-gold" />
                    <span class="and-up">&amp; Up</span>
                  </div>
                </label>
              </div>
            </div>

            <!-- Group 5: Availability -->
            <div class="filter-group">
              <div class="filter-group-header" @click="availOpen = !availOpen">
                <span class="fg-title">Availability</span>
                <ChevronUp v-if="availOpen" :size="16" />
                <ChevronDown v-else :size="16" />
              </div>
              <div v-show="availOpen" class="filter-checklist">
                <label class="filter-check-row">
                  <input type="checkbox" v-model="inStockOnly" class="f-check" />
                  <span class="f-label">In Stock (118)</span>
                </label>
                <label class="filter-check-row">
                  <input type="checkbox" v-model="onSaleOnly" class="f-check" />
                  <span class="f-label">On Sale (32)</span>
                </label>
              </div>
            </div>
          </div>
        </aside>

        <!-- 2. Center Column: 4-Column Product Grid -->
        <main class="search-products-col">
          <!-- Toolbar matching Search Results.png -->
          <div class="search-toolbar-strip">
            <div class="toolbar-left">
              <span class="results-text">
                <strong>{{ displayedProducts.length }}</strong> results for “{{ activeQuery }}”
              </span>
            </div>

            <div class="toolbar-right">
              <div class="sort-selector-wrap">
                <label>Sort by:</label>
                <select v-model="sortOption" class="sort-select">
                  <option value="relevance">Relevance</option>
                  <option value="rating">Highest Rated</option>
                  <option value="price_asc">Price: Low to High</option>
                  <option value="price_desc">Price: High to Low</option>
                  <option value="popular">Most Popular</option>
                </select>
              </div>

              <div class="grid-view-toggles">
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  aria-label="Grid View"
                >
                  <LayoutGrid :size="16" />
                </button>
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  aria-label="List View"
                >
                  <List :size="16" />
                </button>
              </div>
            </div>
          </div>

          <!-- 4-Column Product Grid -->
          <div
            v-if="paginatedProducts.length > 0"
            :class="viewMode === 'list' ? 'search-list-container' : 'search-four-grid'"
          >
            <ProductCard
              v-for="product in paginatedProducts"
              :key="product.id"
              :product="product"
              :view-mode="viewMode"
            />
          </div>

          <!-- Empty State -->
          <div v-else class="empty-search-box">
            <p>No products match your selected filters.</p>
            <button @click="resetFilters" class="clear-all-link">Clear Filters</button>
          </div>

          <!-- Real Interactive Pagination Bar -->
          <div class="search-pagination-bar" v-if="totalPages > 1">
            <button class="page-arrow-btn" :disabled="currentPage === 1" @click="currentPage--">
              <ChevronLeft :size="16" />
            </button>
            <button
              v-for="p in totalPages"
              :key="p"
              class="page-num-btn"
              :class="{ active: currentPage === p }"
              @click="currentPage = p"
            >
              {{ p }}
            </button>
            <button class="page-arrow-btn" :disabled="currentPage === totalPages" @click="currentPage++">
              <ChevronRight :size="16" />
            </button>
          </div>
        </main>

        <!-- 3. Right Column: 4 Dynamic Sidebar Cards -->
        <aside class="search-right-col">
          <!-- Card 1: Related Searches -->
          <div class="right-card related-searches-box">
            <h4 class="rc-title">Related Searches</h4>
            <div class="related-pills-wrap">
              <button
                v-for="tag in dynamicRelatedKeywords"
                :key="tag"
                class="rel-pill-btn"
                @click="searchTag(tag)"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <!-- Card 2: Dynamic Editorial Discovery Banner -->
          <div class="right-card promo-droplet-card">
            <div class="droplet-text-col">
              <h4 class="droplet-slogan">Curated.<br />Targeted.<br />Effective.</h4>
              <router-link :to="`/shop?search=${encodeURIComponent(activeQuery)}`" class="droplet-cta-link">
                <span>Explore All {{ activeQuery ? `“${activeQuery}”` : 'Skincare' }}<br />Formulations</span>
                <ArrowRight :size="13" />
              </router-link>
            </div>
            <div class="droplet-img-col">
              <img src="/images/search-gel-swatch.jpg" alt="Active Swatch" class="droplet-macro-img" />
            </div>
          </div>

          <!-- Card 3: Featured Atelier Brands -->
          <div class="right-card popular-brands-box">
            <div class="popular-brands-header">
              <h4 class="rc-title">Featured Brands</h4>
              <router-link to="/brands" class="rc-view-all">View All →</router-link>
            </div>

            <div class="pop-brands-grid">
              <router-link
                v-for="b in popularBrandsList"
                :key="b.slug"
                :to="`/brand/${b.slug}`"
                class="pop-brand-circle-item"
              >
                <div class="pop-brand-circle">
                  <BrandLogo :slug="b.slug" size="circle" />
                </div>
                <span class="pop-brand-name">{{ b.name }}</span>
              </router-link>
            </div>
          </div>

          <!-- Card 4: Helpful Dermatological Articles -->
          <div class="right-card helpful-articles-box">
            <div class="helpful-header">
              <h4 class="rc-title">Dermatological Guides</h4>
              <router-link to="/articles" class="rc-view-all">View All →</router-link>
            </div>

            <div class="helpful-articles-list">
              <router-link to="/articles" class="article-item-row">
                <img src="/images/article-thumb-routine.jpg" alt="Article 1" class="art-thumb" />
                <div class="art-meta">
                  <span class="art-title">The Science of Skin Barrier: How to Restore &amp; Defend</span>
                  <span class="art-read-time">5 min read</span>
                </div>
              </router-link>

              <router-link to="/articles" class="article-item-row">
                <img src="/images/article-thumb-niacinamide.jpg" alt="Article 2" class="art-thumb" />
                <div class="art-meta">
                  <span class="art-title">Active Ingredients: Safe Layering for Acne &amp; Pores</span>
                  <span class="art-read-time">6 min read</span>
                </div>
              </router-link>

              <router-link to="/articles" class="article-item-row">
                <img src="/images/article-thumb-centella.jpg" alt="Article 3" class="art-thumb" />
                <div class="art-meta">
                  <span class="art-title">Morning vs. Evening Regimen for Glass Skin</span>
                  <span class="art-read-time">4 min read</span>
                </div>
              </router-link>
            </div>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ChevronRight,
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  Search,
  Star,
  Heart,
  ShoppingBag,
  Check,
  LayoutGrid,
  List,
  ArrowRight,
} from 'lucide-vue-next'
import BrandLogo from '@/components/BrandLogo.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useProductStore, BRANDS_DIRECTORY } from '@/stores/products'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()

const viewMode = ref('grid')
const activeScope = ref('all')
const currentPage = ref(1)
const sortOption = ref('relevance')

// Accordion states
const catOpen = ref(true)
const brandOpen = ref(true)
const priceOpen = ref(true)
const ratingOpen = ref(true)
const availOpen = ref(true)

// Filter models
const selectedCategories = ref([])
const selectedBrands = ref([])
const selectedRating = ref([])
const minPrice = ref(null)
const maxPrice = ref(null)
const inStockOnly = ref(false)
const onSaleOnly = ref(false)
const brandSearchInput = ref('')

const activeQuery = computed(() => {
  return (route.query.q || route.query.search || '').toString()
})

onMounted(() => {
  productStore.fetchProducts()
})

// Brand checklist matching wireframe
const brandChecklist = [
  { name: 'The Ordinary', count: 14 },
  { name: 'SK-II', count: 10 },
  { name: 'CeraVe', count: 8 },
  { name: 'La Roche-Posay', count: 8 },
  { name: 'LANEIGE', count: 6 },
  { name: 'innisfree', count: 6 },
  { name: 'COSRX', count: 5 },
  { name: 'Bioderma', count: 4 },
  { name: 'Beauty of Joseon', count: 4 },
]

const filteredBrandChecklist = computed(() => {
  if (!brandSearchInput.value.trim()) return brandChecklist
  const q = brandSearchInput.value.toLowerCase().trim()
  return brandChecklist.filter((b) => b.name.toLowerCase().includes(q))
})

// Dynamic related keywords based on actual search
const dynamicRelatedKeywords = computed(() => {
  const q = activeQuery.value.trim()
  if (!q) {
    return ['hydrating serum', 'barrier repair', 'mineral sunscreen', 'ceramide cream', 'gentle cleanser', 'vitamin c']
  }
  return [
    `${q} serum`,
    `${q} cleanser`,
    `${q} for sensitive skin`,
    `${q} moisturizer`,
    `${q} toner`,
    `best ${q} products`,
  ]
})

function searchTag(tag) {
  router.push({ path: '/search', query: { q: tag } })
}

// 8 Popular Brands matching wireframe
const popularBrandsList = [
  { name: 'The Ordinary', slug: 'the-ordinary' },
  { name: 'SK-II', slug: 'sk-ii' },
  { name: 'CeraVe', slug: 'cerave' },
  { name: 'La Roche-Posay', slug: 'la-roche-posay' },
  { name: 'innisfree', slug: 'innisfree' },
  { name: 'COSRX', slug: 'cosrx' },
  { name: 'LANEIGE', slug: 'laneige' },
  { name: 'Beauty of Joseon', slug: 'beauty-of-joseon' },
]

// Fallback catalog in case API is delayed
const fallbackProducts = [
  {
    id: 202,
    name: 'Niacinamide 10% + Zinc 1%',
    brand: 'The Ordinary',
    category_name: 'Serums',
    price: 8.90,
    compare_at_price: null,
    rating: 4.7,
    reviews: '980',
    badge: 'Best Seller',
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1',
    stock: 24,
  },
  {
    id: 201,
    name: 'Facial Treatment Essence',
    brand: 'SK-II',
    category_name: 'Toners',
    price: 99.00,
    compare_at_price: 125.00,
    rating: 4.8,
    reviews: '1.2K',
    badge: '20% OFF',
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence',
    stock: 12,
  },
  {
    id: 221,
    name: 'PM Facial Moisturizing Lotion',
    brand: 'CeraVe',
    category_name: 'Moisturizers',
    price: 18.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: '1.1K',
    badge: null,
    image_url: '/images/prod-cerave.jpg',
    slug: 'cerave-pm-facial-moisturizing-lotion',
    stock: 30,
  },
  {
    id: 220,
    name: 'Glow Serum (Propolis + Niacinamide)',
    brand: 'Beauty of Joseon',
    category_name: 'Serums',
    price: 17.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '2.3K',
    badge: null,
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-glow-serum-propolis-niacinamide',
    stock: 18,
  },
  {
    id: 108,
    name: 'Cream Skin Refiner & Toner',
    brand: 'LANEIGE',
    category_name: 'Toners',
    price: 24.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '892',
    badge: null,
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-cream-skin-milk-cleanser',
    stock: 15,
  },
  {
    id: 218,
    name: 'Mela B3 Serum',
    brand: 'La Roche-Posay',
    category_name: 'Serums',
    price: 39.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: '743',
    badge: null,
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-pure-niacinamide-10',
    stock: 10,
  },
  {
    id: 208,
    name: 'Brightening Pore Serum',
    brand: 'innisfree',
    category_name: 'Serums',
    price: 28.00,
    compare_at_price: null,
    rating: 4.5,
    reviews: '620',
    badge: null,
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum',
    stock: 20,
  },
  {
    id: 206,
    name: 'The Niacinamide 15 Serum',
    brand: 'COSRX',
    category_name: 'Serums',
    price: 25.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: '710',
    badge: null,
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-advanced-snail-96-mucin-essence',
    stock: 25,
  },
  {
    id: 107,
    name: 'Sébium Pore Refiner',
    brand: 'Bioderma',
    category_name: 'Treatments',
    price: 22.00,
    compare_at_price: null,
    rating: 4.4,
    reviews: '512',
    badge: null,
    image_url: '/images/prod-bioderma-micellar.jpg',
    slug: 'bioderma-sensibio-h2o-micellar-water',
    stock: 16,
  },
  {
    id: 219,
    name: 'Niacinamide 10% + TXA 4% Serum',
    brand: 'Anua',
    category_name: 'Serums',
    price: 26.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '1.0K',
    badge: null,
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'anua-niacinamide-10-txa-4-serum',
    stock: 14,
  },
]

// All active products pool
const allProductsPool = computed(() => {
  if (productStore.products && productStore.products.length > 0) {
    return productStore.products
  }
  return fallbackProducts
})

// Dynamic category counts from pool
const categoryCounts = computed(() => {
  const map = {}
  allProductsPool.value.forEach((p) => {
    const c = p.category_name || p.category || 'Skincare'
    map[c] = (map[c] || 0) + 1
  })
  return Object.keys(map).map((k) => ({ name: k, count: map[k] }))
})

// Filtered products list
const filteredProductsList = computed(() => {
  let list = allProductsPool.value
  const q = activeQuery.value.toLowerCase().trim()

  if (q && q !== 'all') {
    list = list.filter((p) => {
      const name = (p.name || '').toLowerCase()
      const brand = (p.brand || '').toLowerCase()
      const desc = (p.description || p.desc || '').toLowerCase()
      const cat = (p.category_name || p.category || '').toLowerCase()
      const skinType = (p.skin_type || '').toLowerCase()
      const concerns = (p.concerns || '').toLowerCase()
      return (
        name.includes(q) ||
        brand.includes(q) ||
        desc.includes(q) ||
        cat.includes(q) ||
        skinType.includes(q) ||
        concerns.includes(q)
      )
    })
  }

  if (selectedCategories.value.length > 0) {
    list = list.filter((p) =>
      selectedCategories.value.includes(p.category_name || p.category)
    )
  }

  if (selectedBrands.value.length > 0) {
    list = list.filter((p) => selectedBrands.value.includes(p.brand))
  }

  if (minPrice.value) {
    list = list.filter((p) => p.price >= minPrice.value)
  }
  if (maxPrice.value) {
    list = list.filter((p) => p.price <= maxPrice.value)
  }
  if (inStockOnly.value) {
    list = list.filter((p) => p.stock > 0)
  }
  if (onSaleOnly.value) {
    list = list.filter((p) => p.compare_at_price && p.compare_at_price > p.price)
  }

  // Sorting
  if (sortOption.value === 'rating') {
    list = [...list].sort((a, b) => (b.rating || 0) - (a.rating || 0))
  } else if (sortOption.value === 'price_asc') {
    list = [...list].sort((a, b) => a.price - b.price)
  } else if (sortOption.value === 'price_desc') {
    list = [...list].sort((a, b) => b.price - a.price)
  } else if (sortOption.value === 'popular') {
    list = [...list].sort((a, b) => (b.reviews_count || 0) - (a.reviews_count || 0))
  }

  return list
})

// Pagination
const pageSize = 8
const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredProductsList.value.length / pageSize))
)
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProductsList.value.slice(start, start + pageSize)
})

const allResultsCount = computed(() => filteredProductsList.value.length)
const productsCount = computed(() => filteredProductsList.value.length)
const brandsCount = computed(() => {
  const brands = new Set(filteredProductsList.value.map((p) => p.brand).filter(Boolean))
  return brands.size
})

// Cart & Wishlist
const addedMap = ref({})
const wishlistMap = ref({})

function isAdded(id) {
  return !!addedMap.value[id]
}
function handleAddToCart(product) {
  cartStore.addItem(product)
  addedMap.value[product.id] = true
  setTimeout(() => {
    addedMap.value[product.id] = false
  }, 2000)
}

function isWishlisted(id) {
  return !!wishlistMap.value[id]
}
function toggleWishlist(id) {
  wishlistMap.value[id] = !wishlistMap.value[id]
}

function resetFilters() {
  selectedCategories.value = []
  selectedBrands.value = []
  selectedRating.value = []
  minPrice.value = null
  maxPrice.value = null
  inStockOnly.value = false
  onSaleOnly.value = false
}
</script>

<style scoped>
.search-results-page {
  padding-bottom: 5rem;
  background-color: #FAF8F5;
  min-height: 100vh;
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
  transition: color 0.2s ease;
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

/* Hero Banner matching Search Results.png */
.banner-container {
  margin-bottom: 1.25rem;
}

.search-hero-card {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border: 1px solid rgba(196, 98, 60, 0.12);
  border-radius: 16px;
  padding: 1.75rem 2.5rem;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
  position: relative;
  overflow: hidden;
  min-height: 275px;
}

.search-hero-left {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
}

.search-hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.12;
  margin-bottom: 0.35rem;
  letter-spacing: -0.015em;
}

.search-hero-subtitle {
  font-size: 1.15rem;
  color: #1C1917;
  margin-bottom: 1.25rem;
}

.search-hero-subtitle strong {
  color: #8E2B2B;
}

/* Scope Tabs inside hero banner */
.hero-scope-tabs {
  display: flex;
  gap: 1.25rem;
  border-bottom: 1px solid rgba(196, 98, 60, 0.15);
  margin-top: 0.5rem;
}

.hero-scope-tab {
  background: none;
  border: none;
  padding: 0.45rem 0;
  font-size: 0.86rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  position: relative;
  transition: color 0.15s ease;
}

.hero-scope-tab:hover {
  color: #8E2B2B;
}

.hero-scope-tab.active {
  color: #8E2B2B;
  font-weight: 700;
}

.hero-scope-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2.5px;
  background: #8E2B2B;
  border-radius: 2px;
}

.search-hero-right {
  width: 480px;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 1;
}

.hero-stage-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.search-stage-hero-img {
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

/* 3-Column Search Layout */
.search-main-container {
  margin-bottom: 4rem;
}

.search-three-columns {
  display: grid;
  grid-template-columns: 230px 1fr 280px;
  gap: 1.75rem;
  align-items: start;
}

/* 1. Left Filters Accordion */
.search-filters-col {
  display: flex;
  flex-direction: column;
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1.25rem);
  max-height: calc(100vh - var(--navbar-height, 68px) - 2rem);
  overflow-y: auto;
  scrollbar-width: thin;
}

.filters-panel {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
}

.filters-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #EAE5DF;
  margin-bottom: 1rem;
}

.filters-panel-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1C1917;
}

.clear-all-link {
  background: none;
  border: none;
  font-size: 0.76rem;
  color: #8E4A3E;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
}

.filter-group {
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #F4EFEB;
}

.filter-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  margin-bottom: 0.65rem;
  color: #1C1917;
}

.fg-title {
  font-size: 0.85rem;
  font-weight: 700;
}

.filter-checklist {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.filter-check-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.8rem;
  color: #78716C;
  cursor: pointer;
}

.f-check {
  accent-color: #8E4A3E;
}

.brand-filter-search {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.35rem 0.6rem;
  margin-bottom: 0.65rem;
}

.bfs-icon {
  color: #9C948B;
}

.bfs-input {
  border: none;
  background: transparent;
  font-size: 0.78rem;
  outline: none;
  width: 100%;
}

.brand-list-scroll {
  max-height: 140px;
  overflow-y: auto;
}

.show-more-brands-btn {
  background: none;
  border: none;
  font-size: 0.74rem;
  color: #8E4A3E;
  font-weight: 700;
  cursor: pointer;
  margin-top: 0.4rem;
  padding: 0;
}

.price-slider-track {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.74rem;
  color: #78716C;
  margin-bottom: 0.65rem;
}

.p-bar {
  flex: 1;
  height: 4px;
  background: #EAE5DF;
  border-radius: 2px;
  position: relative;
}

.p-fill {
  width: 70%;
  height: 100%;
  background: #8E4A3E;
  border-radius: 2px;
}

.price-boxes-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.price-box {
  display: flex;
  align-items: center;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.3rem 0.5rem;
  font-size: 0.78rem;
  width: 100%;
  background: #FFFFFF;
}

.price-box input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 0.78rem;
  margin-left: 0.2rem;
}

.p-dash {
  color: #C4B5AA;
}

.stars-preview {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}

.star-gold {
  color: #F59E0B;
  fill: #F59E0B;
}

.and-up {
  font-size: 0.75rem;
  color: #78716C;
  margin-left: 0.25rem;
}

/* 2. Main Center Products Column */
.search-products-col {
  display: flex;
  flex-direction: column;
}

.search-toolbar-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.results-text {
  font-size: 0.9rem;
  color: #1C1917;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.sort-selector-wrap {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: #78716C;
}

.sort-select {
  border: 1px solid #EAE5DF;
  background: #FFFFFF;
  border-radius: 6px;
  padding: 0.3rem 0.65rem;
  font-size: 0.82rem;
  outline: none;
  cursor: pointer;
}

.grid-view-toggles {
  display: flex;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  overflow: hidden;
}

.view-btn {
  background: #FFFFFF;
  border: none;
  padding: 0.35rem 0.55rem;
  cursor: pointer;
  color: #78716C;
  display: flex;
  align-items: center;
}

.view-btn.active {
  background: #FAF8F5;
  color: #1C1917;
}

/* 4-Column Product Grid matching Search Results.png */
.search-four-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-list-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-grid-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.2s ease;
}

.search-grid-card:hover {
  border-color: #8E4A3E;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(40, 20, 10, 0.06);
}

.card-top-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  height: 20px;
}

.search-pill-badge {
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}

.search-pill-badge.bestseller {
  background: #8E4A3E;
  color: #FFFFFF;
}

.search-pill-badge.sale {
  background: #B91C1C;
  color: #FFFFFF;
}

.search-pill-badge.default {
  background: #FAF8F5;
  color: #78716C;
}

.search-wish-btn {
  background: none;
  border: none;
  color: #9C948B;
  cursor: pointer;
}

.search-wish-btn.active {
  color: #DC2626;
  fill: #DC2626;
}

.card-photo-link {
  height: 140px;
  background: #FAF8F5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.65rem;
  padding: 0.5rem;
}

.search-card-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.card-details-box {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.search-card-brand {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.15rem;
}

.search-title-link {
  text-decoration: none;
  color: inherit;
  margin-bottom: 0.35rem;
}

.search-card-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.1rem;
}

.search-card-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.score-txt {
  font-weight: 700;
}

.rev-txt {
  color: #78716C;
  font-weight: 400;
}

.search-card-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  margin-bottom: 0.65rem;
}

.main-price {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1C1917;
}

.comp-price {
  font-size: 0.78rem;
  color: #9C948B;
  text-decoration: line-through;
}

/* Add to Cart Button matching HomeView product button */
.btn-format-add-cart {
  width: 100%;
  background: #F4EFEB;
  color: #1C1917;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 6px;
  padding: 0.52rem 0.65rem;
  font-size: 0.78rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  cursor: pointer;
  margin-top: auto;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.btn-format-add-cart:hover {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(36, 39, 33, 0.15);
}

.btn-format-add-cart:active {
  transform: scale(0.97);
}

.btn-format-add-cart.is-added {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
}

/* Pagination Bar matching Search Results.png */
.search-pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  margin-top: 1.5rem;
}

.page-arrow-btn {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #78716C;
}

.page-num-btn {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
}

.page-num-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
  border-color: #8E4A3E;
}

.page-dots {
  color: #78716C;
  padding: 0 0.25rem;
}

/* 3. Right Sidebar matching Search Results.png */
.search-right-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.right-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
}

.rc-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.75rem;
}

/* Related Searches Pills Cloud */
.related-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.rel-pill-btn {
  background: #FFFFFF;
  border: 1px solid #D6CEC5;
  border-radius: 9999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.75rem;
  color: #1C1917;
  cursor: pointer;
  transition: all 0.15s ease;
}

.rel-pill-btn:hover {
  border-color: #8E4A3E;
  color: #8E4A3E;
}

/* Promo Droplet Card */
.promo-droplet-card {
  background: linear-gradient(135deg, #FAF2ED 0%, #F5E5DC 100%);
  border-color: rgba(196, 98, 60, 0.18);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.droplet-slogan {
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  font-size: 1.15rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.25;
  margin-bottom: 0.65rem;
}

.droplet-cta-link {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.74rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
  line-height: 1.3;
}

.droplet-img-col {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.15);
}

.droplet-macro-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Popular Brands for Niacinamide */
.popular-brands-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.rc-view-all {
  font-size: 0.74rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.pop-brands-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.65rem;
}

.pop-brand-circle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
}

.pop-brand-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.35rem;
  transition: transform 0.15s ease;
}

.pop-brand-circle-item:hover .pop-brand-circle {
  transform: scale(1.05);
  border-color: #8E4A3E;
}

.pop-brand-name {
  font-size: 0.65rem;
  color: #78716C;
  text-align: center;
}

/* Helpful Articles */
.helpful-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.helpful-articles-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.article-item-row {
  display: flex;
  gap: 0.65rem;
  align-items: center;
}

.art-thumb {
  width: 54px;
  height: 54px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

.art-meta {
  display: flex;
  flex-direction: column;
}

.art-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.35;
  margin-bottom: 0.2rem;
}

.art-read-time {
  font-size: 0.68rem;
  color: #78716C;
}

/* Responsive */
@media (max-width: 1200px) {
  .search-three-columns {
    grid-template-columns: 220px 1fr;
  }
  .search-right-col {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
  .search-four-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .search-hero-card {
    flex-direction: column;
    padding: 2rem;
    text-align: center;
  }
  .hero-scope-tabs {
    justify-content: center;
  }
  .search-three-columns {
    grid-template-columns: 1fr;
  }
  .search-four-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .search-right-col {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .search-four-grid {
    grid-template-columns: 1fr;
  }
}
</style>
