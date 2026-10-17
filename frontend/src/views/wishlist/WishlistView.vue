<template>
  <div class="wishlist-page">
    <!-- Breadcrumbs matching Wishlist.png -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">Wishlist</span>
      </nav>
    </div>

    <!-- Hero Banner matching Wishlist.png -->
    <section class="container banner-container">
      <div class="wishlist-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">My Wishlist</h1>
          <h2 class="hero-tagline">Skincare I Love</h2>
          <p class="hero-desc">
            Keep track of your favorite products, save them for later, and never miss out. A healthier, happier you is always within reach.
          </p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banners/banner-wishlist-clean.jpg"
            alt="Luméa Wishlist Curated Products"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Good<br />Skincare<br />Brighter<br />Days.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Wishlist Navigation Tabs matching Wishlist.png -->
    <section class="container tabs-bar-container">
      <div class="wishlist-tabs-row">
        <button
          class="wishlist-tab-link"
          :class="{ active: currentTab === 'wishlist' }"
          @click="currentTab = 'wishlist'"
        >
          <Heart :size="16" class="tab-icon" />
          <span>My Wishlist ({{ wishlistStore.totalItems }})</span>
        </button>
        <button
          class="wishlist-tab-link"
          :class="{ active: currentTab === 'recent' }"
          @click="currentTab = 'recent'"
        >
          <Clock :size="16" class="tab-icon" />
          <span>Recently Viewed ({{ wishlistStore.recentlyViewed.length }})</span>
        </button>
        <button
          class="wishlist-tab-link"
          :class="{ active: currentTab === 'drops' }"
          @click="currentTab = 'drops'"
        >
          <Bell :size="16" class="tab-icon" />
          <span>Price Drops ({{ wishlistStore.priceDrops.length }})</span>
        </button>
        <button
          class="wishlist-tab-link"
          :class="{ active: currentTab === 'stock' }"
          @click="currentTab = 'stock'"
        >
          <ShoppingBag :size="16" class="tab-icon" />
          <span>Back in Stock ({{ wishlistStore.backInStock.length }})</span>
        </button>
      </div>
    </section>

    <!-- Main Content: 2-Column Layout matching Wishlist.png -->
    <section class="container wishlist-layout-section">
      <div class="wishlist-2col-grid">
        <!-- LEFT COLUMN: Saved Items Table -->
        <main class="wishlist-table-col">
          <div class="table-header-toolbar">
            <div class="toolbar-left">
              <span class="total-saved-label">Showing <strong>{{ filteredWishlistItems.length }}</strong> saved items</span>
              <label v-if="viewMode === 'list'" class="select-all-label">
                <input
                  type="checkbox"
                  v-model="allSelected"
                  @change="toggleSelectAll"
                />
                <span>Select All</span>
              </label>
            </div>

            <div class="toolbar-right">
              <div class="sort-by-wrap">
                <span class="sort-label">Sort by:</span>
                <select v-model="sortBy" class="format-sort-select">
                  <option value="newest">Date Added (Newest)</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                  <option value="rating">Top Rated</option>
                </select>
              </div>
              <div class="view-icons-group">
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  title="Grid View"
                  aria-label="Grid View"
                >
                  <LayoutGrid :size="15" />
                </button>
                <button
                  class="view-btn"
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  title="List View"
                  aria-label="List View"
                >
                  <List :size="15" />
                </button>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredWishlistItems.length === 0" class="empty-wishlist-box">
            <div class="empty-icon-circle">
              <Heart :size="32" class="empty-heart-svg" />
            </div>
            <h3 class="empty-wishlist-title">No items found</h3>
            <p class="empty-wishlist-desc">There are no products in this category yet. Explore our bestsellers and tap the heart icon to save your favorites.</p>
            <button class="empty-reset-tab-btn" @click="currentTab = 'wishlist'">
              View All Saved Items
            </button>
          </div>

          <!-- List View: Items Table Rows matching format/Wishlist.png -->
          <div v-else-if="viewMode === 'list'" class="wishlist-table-card">
            <div
              v-for="item in filteredWishlistItems"
              :key="item.id"
              class="wishlist-item-row"
            >
              <!-- Checkbox -->
              <input
                type="checkbox"
                v-model="selectedItemIds"
                :value="item.id"
                class="row-checkbox"
              />

              <!-- Bottle Thumbnail -->
              <router-link :to="`/product/${item.slug}`" class="row-thumb-wrap">
                <img :src="item.image_url" :alt="item.name" class="row-thumb-img" />
              </router-link>

              <!-- Product Info -->
              <div class="row-info-col">
                <span class="row-brand">{{ item.brand }}</span>
                <router-link :to="`/product/${item.slug}`" class="row-title">
                  {{ item.name }}
                </router-link>
                <span class="row-volume">{{ item.volume || '50 ml' }}</span>
                <div class="row-rating">
                  <span class="stars">★★★★★</span>
                  <span class="rating-val">{{ item.rating || 4.8 }}</span>
                  <span class="review-count">({{ item.reviews || '1.2K' }})</span>
                </div>
              </div>

              <!-- Price -->
              <div class="row-price-col">
                <span class="row-price">${{ Number(item.price).toFixed(2) }}</span>
                <span v-if="item.compare_at_price" class="row-compare-price">
                  ${{ Number(item.compare_at_price).toFixed(2) }}
                </span>
              </div>

              <!-- Stock Status Pill -->
              <div class="row-stock-col">
                <span
                  class="stock-pill"
                  :class="item.stockStatus === 'Low Stock' ? 'pill-low-stock' : 'pill-in-stock'"
                >
                  {{ item.stockStatus || 'In Stock' }}
                </span>
              </div>

              <!-- Format Porcelain Add to Cart Button matching HomeView -->
              <div class="row-action-col">
                <button class="row-add-btn" @click="addToCart(item)">
                  <ShoppingCart :size="14" />
                  <span>Add to Cart</span>
                </button>
              </div>

              <!-- Upgraded Interactive Heart & More Icons -->
              <div class="row-tools-col">
                <button
                  class="heart-toggle-btn active"
                  @click="removeItem(item.id)"
                  title="Remove from Wishlist"
                  aria-label="Remove from Wishlist"
                >
                  <Heart :size="16" class="heart-svg-icon" />
                </button>
                <button class="more-opts-btn" title="More Options" aria-label="More Options">
                  <MoreHorizontal :size="17" />
                </button>
              </div>
            </div>
          </div>

          <!-- Grid View: ProductCard 3-Column Grid matching HomeView -->
          <div v-else class="wishlist-cards-grid">
            <ProductCard
              v-for="item in filteredWishlistItems"
              :key="item.id"
              :product="item"
            />
          </div>

          <!-- Bottom Action Bar matching Wishlist.png (List View Only) -->
          <div v-if="viewMode === 'list' && filteredWishlistItems.length > 0" class="table-bottom-bar">
            <div class="bottom-left-actions">
              <label class="select-all-label">
                <input
                  type="checkbox"
                  v-model="allSelected"
                  @change="toggleSelectAll"
                />
                <span>Select All</span>
              </label>
              <button class="remove-selected-btn" @click="removeSelected">
                <Trash2 :size="14" />
                <span>Remove Selected</span>
              </button>
            </div>
            <span class="bottom-items-count">{{ filteredWishlistItems.length }} items</span>
          </div>
        </main>

        <!-- RIGHT COLUMN: Journey, Love What You See, Recommended Grid matching Wishlist.png -->
        <aside class="wishlist-sidebar-col">
          <!-- Card 1: Your Beauty Journey Continues -->
          <div class="sidebar-card journey-card">
            <div class="journey-illustration-wrap">
              <div class="shopping-bag-heart-icon">
                <ShoppingBag :size="32" class="bag-icon-outline" />
                <Heart :size="14" class="bag-heart-inner" fill="#8E4A3E" stroke="#8E4A3E" />
              </div>
            </div>
            <h3 class="journey-title">Your Beauty<br />Journey Continues</h3>
            <p class="journey-sub">Add your favorites to cart<br />before they're gone.</p>
            <button class="journey-add-all-btn" @click="addAllToCart">
              <ShoppingCart :size="15" />
              <span>Add All to Cart ({{ wishlistItems.length }} items)</span>
            </button>
          </div>

          <!-- Card 2: Love what you see? -->
          <div class="sidebar-card love-card">
            <div class="love-content">
              <h3 class="love-title">Love what you see?</h3>
              <p class="love-sub">Discover more skincare<br />you'll love.</p>
              <router-link to="/best-sellers" class="love-btn">
                Shop Best Sellers &rarr;
              </router-link>
            </div>
            <div class="love-visual">
              <img src="/images/feat-sk2-card.jpg" alt="Love Skincare" class="love-img" />
            </div>
          </div>

          <!-- Card 3: Recommended for You (2x3 mini catalog grid matching Wishlist.png) -->
          <div class="sidebar-card recommended-card">
            <div class="recommended-header">
              <h3 class="recommended-title">Recommended for You</h3>
              <router-link to="/shop" class="view-all-link">
                View All &rarr;
              </router-link>
            </div>

            <!-- 2 Columns x 3 Rows Mini Product Grid using standardized ProductCard -->
            <div class="mini-products-grid">
              <ProductCard
                v-for="rec in recommendedProducts"
                :key="rec.id"
                :product="rec"
              />
            </div>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notification'
import { useWishlistStore } from '@/stores/wishlist'
import {
  Bell,
  ChevronRight,
  Clock,
  Heart,
  LayoutGrid,
  List,
  MoreHorizontal,
  ShoppingBag,
  ShoppingCart,
  Trash2
} from 'lucide-vue-next'
import { computed, ref } from 'vue'
import ProductCard from '@/components/ProductCard.vue'

const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const notificationStore = useNotificationStore()

const currentTab = ref('wishlist')
const sortBy = ref('newest')
const viewMode = ref('list')
const allSelected = ref(false)
const selectedItemIds = ref([])

// 6 Exact Wishlist Items matching format/Wishlist.png table:
// 1. SK-II Facial Treatment Essence 230 ml - $99.00 - In Stock
// 2. The Ordinary Niacinamide 10% + Zinc 1% 30 ml - $8.90 - In Stock
// 3. Laneige Lip Sleeping Mask 20 g - $24.00 - In Stock
// 4. CeraVe Hydrating Facial Cleanser 236 ml - $16.00 - In Stock
// 5. Estee Lauder Advanced Night Repair 50 ml - $78.00 - Low Stock
// 6. Beauty of Joseon Relief Sun: Rice + Probiotics SPF50+ 50 ml - $17.00 - In Stock
const defaultItems = [
  {
    id: 101,
    brand: 'SK-II',
    name: 'Facial Treatment Essence',
    volume: '230 ml',
    price: 99.00,
    compare_at_price: 142.00,
    rating: 4.8,
    reviews: '1.2K',
    stockStatus: 'In Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence'
  },
  {
    id: 102,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1%',
    volume: '30 ml',
    price: 8.90,
    compare_at_price: 11.00,
    rating: 4.7,
    reviews: '9.8K',
    stockStatus: 'In Stock',
    isPriceDrop: true,
    isRecent: false,
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1'
  },
  {
    id: 103,
    brand: 'Laneige',
    name: 'Lip Sleeping Mask',
    volume: '20 g',
    price: 24.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '4.1K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: true,
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask'
  },
  {
    id: 104,
    brand: 'CeraVe',
    name: 'Hydrating Facial Cleanser',
    volume: '236 ml',
    price: 16.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '6.2K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-hydrating-cleanser'
  },
  {
    id: 105,
    brand: 'Estée Lauder',
    name: 'Advanced Night Repair',
    volume: '50 ml',
    price: 78.00,
    compare_at_price: 104.00,
    rating: 4.7,
    reviews: '9.9K',
    stockStatus: 'Low Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/bottle-cerave.jpg',
    slug: 'estee-lauder-advanced-night-repair'
  },
  {
    id: 106,
    brand: 'Beauty of Joseon',
    name: 'Relief Sun: Rice + Probiotics SPF50+ PA++++',
    volume: '50 ml',
    price: 17.00,
    compare_at_price: 22.00,
    rating: 4.8,
    reviews: '5.4K',
    stockStatus: 'Back in Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-relief-sun'
  }
]

const wishlistItems = computed(() => wishlistStore.items)

// Reactive filtering by tab and sorting by dropdown
const filteredWishlistItems = computed(() => {
  let list = wishlistStore.items

  if (currentTab.value === 'recent') {
    list = wishlistStore.recentlyViewed
  } else if (currentTab.value === 'drops') {
    list = wishlistStore.priceDrops
  } else if (currentTab.value === 'stock') {
    list = wishlistStore.backInStock
  }

  return [...list].sort((a, b) => {
    if (sortBy.value === 'price-asc') return a.price - b.price
    if (sortBy.value === 'price-desc') return b.price - a.price
    if (sortBy.value === 'rating') return (Number(b.rating) || 0) - (Number(a.rating) || 0)
    return (b.id || 0) - (a.id || 0)
  })
})

// 6 Recommended Products for 2x3 grid matching format/Wishlist.png:
// COSRX Snail 96 ($25.00)
// Innisfree Green Tea Seed Serum ($28.00)
// La Roche-Posay Cicaplast Baume B5 ($18.00)
// TIRTIR Milk Skin Toner ($24.00)
// Medicube Collagen Jelly Cream ($28.00)
// Anua Heartleaf 77% Toner ($26.00)
const recommendedProducts = [
  {
    id: 501,
    brand: 'COSRX',
    name: 'Snail 96 Essence',
    price: 25.00,
    rating: 4.8,
    reviews: '3.9K',
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-snail-96-essence'
  },
  {
    id: 502,
    brand: 'innisfree',
    name: 'Green Tea Seed Serum',
    price: 28.00,
    rating: 4.6,
    reviews: '2.1K',
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum'
  },
  {
    id: 503,
    brand: 'La Roche-Posay',
    name: 'Cicaplast Baume B5',
    price: 18.00,
    rating: 4.7,
    reviews: '3.2K',
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-cicaplast-baume'
  },
  {
    id: 504,
    brand: 'TIRTIR',
    name: 'Milk Skin Toner',
    price: 24.00,
    rating: 4.7,
    reviews: '1.9K',
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'tirtir-milk-skin-toner'
  },
  {
    id: 505,
    brand: 'Medicube',
    name: 'Collagen Jelly Cream',
    price: 28.00,
    rating: 4.6,
    reviews: '1.8K',
    image_url: '/images/prod-laneige.jpg',
    slug: 'medicube-collagen-jelly-cream'
  },
  {
    id: 506,
    brand: 'Anua',
    name: 'Heartleaf 77% Toner',
    price: 26.00,
    rating: 4.7,
    reviews: '3.6K',
    image_url: '/images/prod-anua-cleanser.jpg',
    slug: 'anua-heartleaf-77-toner'
  }
]

function toggleSelectAll() {
  if (allSelected.value) {
    selectedItemIds.value = filteredWishlistItems.value.map(i => i.id)
  } else {
    selectedItemIds.value = []
  }
}

function removeItem(id) {
  wishlistStore.removeItem(id)
}

function removeSelected() {
  if (selectedItemIds.value.length === 0) return
  wishlistStore.removeMultiple(selectedItemIds.value)
  selectedItemIds.value = []
  allSelected.value = false
}

function addToCart(item) {
  cartStore.addItem({
    id: item.id,
    name: item.name,
    brand: item.brand,
    price: item.price,
    image_url: item.image_url,
    slug: item.slug
  })
}

function addAllToCart() {
  wishlistItems.value.forEach(item => {
    cartStore.addItem({
      id: item.id,
      name: item.name,
      brand: item.brand,
      price: item.price,
      image_url: item.image_url,
      slug: item.slug
    })
  })
  notificationStore.addToast(`Added all ${wishlistItems.value.length} items to cart!`, 'success')
  cartStore.openDrawer()
}
</script>

<style scoped>
/* ==========================================================================
   WISHLIST PAGE (Strictly matches format/Wishlist.png)
   ========================================================================== */

.wishlist-page {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 5rem;
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

.wishlist-hero-banner {
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
  background: transparent;
  padding: 0;
}

.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.12;
  letter-spacing: -0.015em;
  margin-bottom: 0.35rem;
}

.hero-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1C1917;
  letter-spacing: -0.01em;
  margin-bottom: 0.45rem;
  line-height: 1.25;
}

.hero-desc {
  font-size: 0.92rem;
  line-height: 1.45;
  color: #57534E;
  max-width: 530px;
}

/* Hero Right Stage - Panoramic uncropped */
.hero-right-stage {
  position: relative;
  width: 480px;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
  overflow: hidden;
  z-index: 1;
}

.hero-banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  mask-image: linear-gradient(to right, transparent 0%, black 18%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 18%);
  box-shadow: 0 8px 24px rgba(40, 20, 10, 0.06);
  display: block;
}

.hero-fade-overlay {
  display: none;
}

.banner-script-overlay {
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

.banner-script-overlay span {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.2;
}

/* ==========================================================================
   WISHIST TABS BAR (Matches format/Wishlist.png)
   ========================================================================== */
.tabs-bar-container {
  margin-bottom: 2rem;
}

.wishlist-tabs-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(28, 25, 23, 0.1);
  padding-bottom: 0;
  gap: 2.5rem;
}

.wishlist-tab-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 0.25rem 0.95rem;
  background: none;
  border: none;
  font-family: var(--font-sans);
  font-size: 0.92rem;
  font-weight: 500;
  color: #57534E;
  cursor: pointer;
  position: relative;
  transition: color 0.15s ease;
}

.wishlist-tab-link:hover {
  color: #8E4A3E;
}

.wishlist-tab-link.active {
  color: #8E4A3E;
  font-weight: 600;
}

.wishlist-tab-link.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2.5px;
  background: #8E4A3E;
  border-radius: 2px 2px 0 0;
}

.tab-icon {
  color: inherit;
}

/* ==========================================================================
   2-COLUMN LAYOUT (Matches format/Wishlist.png)
   ========================================================================== */
.wishlist-layout-section {
  margin-bottom: 4rem;
}

.wishlist-2col-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  align-items: start;
}

/* Table Column */
.table-header-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.15rem;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.total-saved-label {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #1C1917;
}

.select-all-label {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.84rem;
  color: #57534E;
  cursor: pointer;
}

.select-all-label input {
  accent-color: #8E4A3E;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-by-wrap {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.sort-label {
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

.view-icons-group {
  display: flex;
  align-items: center;
  border: 1px solid rgba(28, 25, 23, 0.12);
  border-radius: 6px;
  overflow: hidden;
  background: #FFFFFF;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.view-btn {
  background: #FFFFFF;
  border: none;
  padding: 0.42rem 0.65rem;
  color: #78716C;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.view-btn:hover:not(.active) {
  background: #F8F5F0;
  color: #1C1917;
}

.view-btn.active {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* Wishlist Table Card */
.wishlist-table-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 10px;
  overflow: hidden;
}

.wishlist-item-row {
  display: grid;
  grid-template-columns: 24px 80px 1fr 90px 100px 130px 60px;
  align-items: center;
  gap: 1rem;
  padding: 1.15rem 1.25rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
  transition: background 0.15s ease;
}

.wishlist-item-row:last-child {
  border-bottom: none;
}

.wishlist-item-row:hover {
  background: #FAF8F5;
}

.row-checkbox {
  accent-color: #8E4A3E;
  cursor: pointer;
}

.row-thumb-wrap {
  width: 75px;
  height: 75px;
  background: #FAF8F5;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.row-thumb-img {
  max-width: 85%;
  max-height: 85%;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.wishlist-item-row:hover .row-thumb-img {
  transform: scale(1.06);
}

.row-info-col {
  display: flex;
  flex-direction: column;
}

.row-brand {
  font-size: 0.74rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 2px;
}

.row-title {
  font-family: var(--font-serif);
  font-size: 0.95rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
  line-height: 1.25;
  margin-bottom: 2px;
}

.row-title:hover {
  color: #8E4A3E;
}

.row-volume {
  font-size: 0.72rem;
  color: #8C877F;
  margin-bottom: 4px;
}

.row-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
}

.row-rating .stars {
  color: #D97706;
}

.row-rating .rating-val {
  font-weight: 600;
  color: #1C1917;
}

.row-rating .review-count {
  color: #8C877F;
}

.row-price-col {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #1C1917;
}

/* Stock Status Pills */
.stock-pill {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  text-align: center;
}

.pill-in-stock {
  background: #E8F5E9;
  color: #2E7D32;
}

.pill-low-stock {
  background: #FFEBEE;
  color: #C62828;
}

/* Porcelain Row Button matching HomeView */
.row-add-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.52rem 0.95rem;
  background: #F4EFEB;
  color: #1C1917;
  border: 1px solid rgba(28, 25, 23, 0.06);
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.row-add-btn:hover {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(36, 39, 33, 0.15);
}

.row-tools-col {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.heart-toggle-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #FFF5F2;
  border: 1.5px solid #F0B3A8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #8E4A3E;
  padding: 0;
  box-shadow: 0 2px 8px rgba(142, 74, 62, 0.1);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.heart-toggle-btn .heart-svg-icon {
  fill: #8E4A3E;
  stroke: #8E4A3E;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.heart-toggle-btn:hover {
  background: #8E4A3E;
  border-color: #8E4A3E;
  transform: scale(1.18);
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.3);
}

.heart-toggle-btn:hover .heart-svg-icon {
  fill: #FFFFFF;
  stroke: #FFFFFF;
  transform: scale(1.1);
}

.heart-toggle-btn:active {
  transform: scale(0.92);
}

.heart-toggle-btn.active {
  animation: heartPop 0.38s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.more-opts-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: transparent;
  border: 1px solid transparent;
  color: #8C877F;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  transition: all 0.2s ease;
}

.more-opts-btn:hover {
  background: #F4EFEB;
  color: #1C1917;
  border-color: rgba(28, 25, 23, 0.08);
}

/* Wishlist Product Cards Grid (Grid View Mode) */
.wishlist-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
  animation: gridFadeIn 0.35s ease both;
}

@keyframes gridFadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 960px) {
  .wishlist-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .wishlist-cards-grid {
    grid-template-columns: 1fr;
  }
}

/* Empty Wishlist Box */
.empty-wishlist-box {
  background: #FFFFFF;
  border: 1px dashed rgba(28, 25, 23, 0.15);
  border-radius: 12px;
  padding: 3.5rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #FDF2EE;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.empty-heart-svg {
  color: #8E4A3E;
  fill: rgba(142, 74, 62, 0.18);
}

.empty-wishlist-title {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.4rem;
}

.empty-wishlist-desc {
  font-size: 0.88rem;
  color: #78716C;
  max-width: 380px;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.empty-reset-tab-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.4rem;
  border-radius: 6px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.18);
}

.empty-reset-tab-btn:hover {
  background: #73382D;
  transform: translateY(-1px);
}

/* Bottom Action Bar */
.table-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.25rem;
}

.bottom-left-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.remove-selected-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border: none;
  color: #57534E;
  font-size: 0.82rem;
  cursor: pointer;
}

.remove-selected-btn:hover {
  color: #8E4A3E;
}

.bottom-items-count {
  font-size: 0.82rem;
  color: #8C877F;
}

/* ==========================================================================
   RIGHT SIDEBAR (Matches format/Wishlist.png)
   ========================================================================== */
.wishlist-sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 10px;
  padding: 1.5rem;
}

/* Journey Card */
.journey-card {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.journey-illustration-wrap {
  margin-bottom: 1rem;
}

.shopping-bag-heart-icon {
  position: relative;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.bag-icon-outline {
  color: #8E4A3E;
}

.bag-heart-inner {
  position: absolute;
  top: 55%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.journey-title {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1.2;
  margin-bottom: 0.4rem;
}

.journey-sub {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.45;
  margin-bottom: 1.25rem;
}

.journey-add-all-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.65rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 4px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}

.journey-add-all-btn:hover {
  background: #73382D;
}

/* Love What You See Card */
.love-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF4F0;
  overflow: hidden;
  padding: 1.35rem;
}

.love-title {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: #7A2E22;
  margin-bottom: 0.25rem;
}

.love-sub {
  font-size: 0.78rem;
  color: #57534E;
  line-height: 1.4;
  margin-bottom: 0.85rem;
}

.love-btn {
  display: inline-block;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.45rem 0.85rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
}

.love-visual {
  width: 75px;
  height: 75px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.love-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Recommended for You 2x3 Grid */
.recommended-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.15rem;
}

.recommended-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 700;
  color: #7A2E22;
}

.view-all-link {
  font-size: 0.76rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
}

.mini-products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.85rem;
}

.mini-rec-card {
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.06);
  border-radius: 6px;
  padding: 0.65rem;
  display: flex;
  flex-direction: column;
}

.mini-card-stage {
  position: relative;
  width: 100%;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.mini-heart-btn {
  position: absolute;
  top: 2px;
  right: 2px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
}

.mini-prod-img {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

.mini-card-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.mini-brand {
  font-size: 0.66rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 1px;
}

.mini-name {
  font-size: 0.74rem;
  font-weight: 500;
  color: #44403C;
  text-decoration: none;
  line-height: 1.3;
  margin-bottom: 0.25rem;
  min-height: 2em;
}

.mini-name:hover {
  color: #8E4A3E;
}

.mini-rating {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.64rem;
  margin-bottom: 0.25rem;
}

.mini-rating .stars {
  color: #D97706;
}

.mini-rating .rating-val {
  font-weight: 600;
  color: #1C1917;
}

.mini-rating .review-count {
  color: #8C877F;
}

.mini-price {
  font-family: var(--font-serif);
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
  margin-top: auto;
}

.mini-add-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.46rem;
  background: #F4EFEB;
  color: #1C1917;
  border: 1px solid rgba(28, 25, 23, 0.06);
  border-radius: 6px;
  font-size: 0.74rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.mini-add-btn:hover {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(36, 39, 33, 0.15);
}

/* Responsive */
@media (max-width: 1080px) {
  .wishlist-2col-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .wishlist-item-row {
    grid-template-columns: 24px 60px 1fr auto;
    gap: 0.75rem;
  }
  .row-volume, .row-rating, .row-stock-col, .row-action-col {
    display: none;
  }
  .wishlist-hero-card {
    grid-template-columns: 1fr;
  }
  .hero-stage-wrap {
    min-height: 240px;
  }
}
</style>
