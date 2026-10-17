<template>
  <div class="brand-store-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <router-link to="/brands" class="breadcrumb-link">Brands</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">{{ currentBrand.name }}</span>
      </nav>
    </div>

    <!-- Hero Banner matching Brand Store.png -->
    <section class="container banner-container">
      <div class="store-hero-banner">
        <div class="store-hero-left">
          <div class="hero-brand-title-wrap">
            <span class="hero-big-brand-name">{{ currentBrand.name }}</span>
          </div>

          <h1 class="hero-script-slogan">
            {{ currentBrand.slug === 'sk-ii' ? 'Crystal Clear Skin For A Brighter Tomorrow.' : currentBrand.hero_tagline }}
          </h1>

          <p class="hero-brand-bio">
            {{ currentBrand.name }} is a {{ currentBrand.origin }} luxury skincare house known for its scientifically proven active innovations. Experience radiant, clear, and youthful skin.
          </p>

          <!-- 3 Pillars Row -->
          <div class="hero-pillars-row">
            <div class="pillar-item">
              <div class="pillar-icon">
                <Sparkles :size="16" />
              </div>
              <div class="pillar-text">
                <span class="pillar-bold">Authentic Products</span>
                <span class="pillar-light">Official distributor</span>
              </div>
            </div>

            <div class="pillar-item">
              <div class="pillar-icon">
                <FlaskConical :size="16" />
              </div>
              <div class="pillar-text">
                <span class="pillar-bold">Scientifically Proven</span>
                <span class="pillar-light">Skincare Innovation</span>
              </div>
            </div>

            <div class="pillar-item">
              <div class="pillar-icon">
                <Award :size="16" />
              </div>
              <div class="pillar-text">
                <span class="pillar-bold">{{ currentBrand.origin }} Heritage</span>
                <span class="pillar-light">Est. {{ currentBrand.founded }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="store-hero-right">
          <div class="hero-stage-wrapper">
            <img
              src="/images/banners/banner-deals-clean.jpg"
              :alt="`${currentBrand.name} Showcase`"
              class="store-stage-hero-img"
            />
            <div class="hero-circular-callout">
              <span>Unlock<br />Your Skin's<br />Natural<br />Potential.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- In-Store Sub-Navbar matching Brand Store.png -->
    <section class="container subnav-container">
      <div class="store-subnav-bar">
        <div class="subnav-left-brand">
          <div class="brand-pill-badge">
            <BrandLogo :slug="currentBrand.slug" :size="24" />
          </div>
        </div>

        <div class="subnav-center-tabs">
          <button
            v-for="tab in storeTabs"
            :key="tab.id"
            class="store-tab-link"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="subnav-right-search">
          <div class="in-store-search-box">
            <Search :size="14" class="in-search-icon" />
            <input
              type="text"
              v-model="inStoreQuery"
              :placeholder="`Search ${currentBrand.name} products...`"
              class="in-search-input"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- 9 Category Circle Badges matching Brand Store.png -->
    <section class="container category-badges-container">
      <div class="category-badges-scroll">
        <button
          v-for="cat in brandCategories"
          :key="cat.name"
          class="cat-badge-item"
          :class="{ active: selectedCategory === cat.name }"
          @click="toggleCategory(cat.name)"
        >
          <div class="cat-circle-avatar">
            <img :src="cat.img" :alt="cat.name" class="cat-circle-img" />
          </div>
          <span class="cat-badge-name">{{ cat.name }}</span>
          <span class="cat-badge-count">{{ cat.count }} products</span>
        </button>
      </div>
    </section>

    <!-- Bestsellers Carousel / Row matching Brand Store.png -->
    <section class="container bestsellers-container">
      <div class="bestsellers-header">
        <div class="bestsellers-title-box">
          <h2 class="bestsellers-heading">Bestsellers</h2>
          <p class="bestsellers-sub">Most loved {{ currentBrand.name }} products, chosen by skincare enthusiasts.</p>
        </div>
        <router-link to="/shop" class="view-all-products-link">
          <span>View All Products</span>
          <ArrowRight :size="14" />
        </router-link>
      </div>

      <div class="bestsellers-cards-row">
        <ProductCard
          v-for="product in displayedBestsellers"
          :key="product.id"
          :product="product"
        />
      </div>
    </section>

    <!-- Two Bottom Editorial Cards matching Brand Store.png -->
    <section class="container editorial-cards-container">
      <div class="editorial-cards-grid">
        <!-- Left: The Power of PITERA™ -->
        <div class="editorial-card pitera-banner-card">
          <div class="pitera-text-area">
            <h3 class="pitera-heading">The Power<br />of PITERA™</h3>
            <p class="pitera-copy">
              A natural bio-ingredient derived from yeast fermentation, PITERA™ is rich in vitamins, amino acids, minerals, and organic acids to help reveal crystal clear skin.
            </p>
            <button @click="activeTab = 'about'" class="pitera-cta-btn">
              <span>Learn More About PITERA</span>
              <ArrowRight :size="14" />
            </button>
          </div>
          <div class="pitera-img-area">
            <img src="/images/pdp-model-radiant.jpg" alt="PITERA Radiant Skin" class="pitera-model-img" />
          </div>
        </div>

        <!-- Right: Build Your SK-II Routine -->
        <div class="editorial-card routine-banner-card">
          <div class="routine-header-area">
            <h3 class="routine-heading">Build Your {{ currentBrand.name }} Routine</h3>
            <p class="routine-sub">Discover a complete skincare routine for radiant, youthful skin.</p>
          </div>

          <div class="routine-steps-row">
            <div class="routine-step-item">
              <div class="step-prod-circle">
                <img src="/images/prod-sk2.jpg" alt="Cleanse" />
              </div>
              <div class="step-number-tag"><span>1</span> Cleanse</div>
            </div>

            <ChevronRight :size="16" class="step-arrow" />

            <div class="routine-step-item">
              <div class="step-prod-circle">
                <img src="/images/pdp-stage-sk2-hero.jpg" alt="Essence" />
              </div>
              <div class="step-number-tag"><span>2</span> Essence</div>
            </div>

            <ChevronRight :size="16" class="step-arrow" />

            <div class="routine-step-item">
              <div class="step-prod-circle">
                <img src="/images/brand-store-sk2-hero.jpg" alt="Treat" />
              </div>
              <div class="step-number-tag"><span>3</span> Treat</div>
            </div>

            <ChevronRight :size="16" class="step-arrow" />

            <div class="routine-step-item">
              <div class="step-prod-circle">
                <img src="/images/feat-sk2-card.jpg" alt="Moisturize" />
              </div>
              <div class="step-number-tag"><span>4</span> Moisturize</div>
            </div>

            <ChevronRight :size="16" class="step-arrow" />

            <div class="routine-step-item">
              <div class="step-prod-circle">
                <img src="/images/prod-boj.jpg" alt="Protect" />
              </div>
              <div class="step-number-tag"><span>5</span> Protect</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  ChevronRight,
  Sparkles,
  FlaskConical,
  Award,
  Search,
  Heart,
  Star,
  ShoppingBag,
  Check,
  ArrowRight,
} from 'lucide-vue-next'
import BrandLogo from '@/components/BrandLogo.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useProductStore, BRANDS_DIRECTORY } from '@/stores/products'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const productStore = useProductStore()
const cartStore = useCartStore()

const currentSlug = computed(() => route.params.slug || 'sk-ii')

const currentBrand = computed(() => {
  const match = BRANDS_DIRECTORY.find((b) => b.slug === currentSlug.value)
  if (match) return match
  return {
    id: 1,
    name: 'SK-II',
    slug: 'sk-ii',
    origin: 'Japan',
    founded: 1980,
    count: 42,
    hero_tagline: 'Timeless Beauty Through Science.',
    desc: 'Renowned Japanese luxury skincare crafted around PITERA™.',
  }
})

// Store sub-navbar tabs
const storeTabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'all', label: 'All Products' },
  { id: 'bestsellers', label: 'Bestsellers' },
  { id: 'routine', label: 'Skincare Routine' },
  { id: 'about', label: 'About' },
  { id: 'reviews', label: 'Reviews' },
]
const activeTab = ref('overview')
const inStoreQuery = ref('')
const selectedCategory = ref(null)

// 9 Category badges matching Brand Store.png
const brandCategories = [
  { name: 'Cleansers', count: 12, img: '/images/cat-cleansers-banner-stage.png' },
  { name: 'Toners', count: 8, img: '/images/cat-toners.jpg' },
  { name: 'Essences', count: 15, img: '/images/pdp-stage-sk2-hero.jpg' },
  { name: 'Serums', count: 18, img: '/images/feat-ordinary-card.jpg' },
  { name: 'Moisturizers', count: 14, img: '/images/feat-sk2-card.jpg' },
  { name: 'Masks', count: 10, img: '/images/cat-masks.jpg' },
  { name: 'Sunscreens', count: 8, img: '/images/prod-boj.jpg' },
  { name: 'Special Care', count: 12, img: '/images/search-hero-niacinamide.jpg' },
  { name: 'Kits & Sets', count: 6, img: '/images/cat-kits.jpg' },
]

function toggleCategory(catName) {
  if (selectedCategory.value === catName) {
    selectedCategory.value = null
  } else {
    selectedCategory.value = catName
  }
}

// Bestsellers products matching Brand Store.png
const displayedBestsellers = computed(() => {
  let list = productStore.allCatalogProducts.filter((p) => p.brand === 'SK-II')

  if (selectedCategory.value) {
    list = list.filter((p) => (p.category_name || p.category).toLowerCase().includes(selectedCategory.value.toLowerCase()))
  }

  if (inStoreQuery.value.trim()) {
    const q = inStoreQuery.value.toLowerCase().trim()
    list = list.filter((p) => p.name.toLowerCase().includes(q))
  }

  return list
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
</script>

<style scoped>
.brand-store-page {
  padding-bottom: 5rem;
  background-color: #FAF8F5;
  min-height: 100vh;
}

/* Breadcrumb */
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
  transition: color 0.15s ease;
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

/* Hero Banner matching Brand Store.png */
.banner-container {
  margin-bottom: 1.25rem;
}

.store-hero-banner {
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

.store-hero-left {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
}

.hero-big-brand-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 3rem;
  font-weight: 900;
  color: #991B1B;
  letter-spacing: 0.04em;
  display: inline-block;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.hero-script-slogan {
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.25;
  margin-bottom: 0.45rem;
}

.hero-brand-bio {
  font-size: 0.92rem;
  line-height: 1.45;
  color: #57534E;
  margin-bottom: 1.15rem;
  max-width: 530px;
}

.hero-pillars-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.pillar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pillar-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #FFFFFF;
  color: #8E2B2B;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.pillar-text {
  display: flex;
  flex-direction: column;
}

.pillar-bold {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
}

.pillar-light {
  font-size: 0.72rem;
  color: #78716C;
  line-height: 1.2;
}

.store-hero-right {
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

.store-stage-hero-img {
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

/* In-Store Sub-Navbar matching Brand Store.png */
.subnav-container {
  margin-bottom: 2rem;
}

.store-subnav-bar {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 0.65rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  gap: 1.5rem;
}

.subnav-left-brand {
  flex-shrink: 0;
}

.brand-pill-badge {
  background: #FAF8F5;
  border: 1px solid #EBE4DD;
  border-radius: 9999px;
  padding: 0.35rem 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.subnav-center-tabs {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.store-tab-link {
  background: none;
  border: none;
  font-size: 0.85rem;
  font-weight: 600;
  color: #78716C;
  padding: 0.4rem 0;
  cursor: pointer;
  position: relative;
  transition: color 0.15s ease;
}

.store-tab-link:hover {
  color: #8E4A3E;
}

.store-tab-link.active {
  color: #8E4A3E;
  font-weight: 700;
}

.store-tab-link.active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 2px;
  background: #8E4A3E;
  border-radius: 2px;
}

.subnav-right-search {
  flex-shrink: 0;
}

.in-store-search-box {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  background: #FAF8F5;
  border: 1px solid #E5DED6;
  border-radius: 9999px;
  padding: 0.4rem 0.85rem;
  min-width: 220px;
}

.in-search-icon {
  color: #9C948B;
}

.in-search-input {
  border: none;
  background: transparent;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  width: 100%;
}

/* Category Badges matching Brand Store.png */
.category-badges-container {
  margin-bottom: 2.5rem;
}

.category-badges-scroll {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem 0;
}

.cat-badge-item {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 105px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}

.cat-badge-item:hover {
  border-color: #8E4A3E;
  transform: translateY(-2px);
}

.cat-badge-item.active {
  border-color: #8E4A3E;
  background: #FAF3EE;
}

.cat-circle-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #FAF8F5;
  overflow: hidden;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cat-circle-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.cat-badge-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.cat-badge-count {
  font-size: 0.7rem;
  color: #78716C;
}

/* Bestsellers Section matching Brand Store.png */
.bestsellers-container {
  margin-bottom: 3rem;
}

.bestsellers-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.bestsellers-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.25rem;
}

.bestsellers-sub {
  font-size: 0.88rem;
  color: #78716C;
}

.view-all-products-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.bestsellers-cards-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
}

.bestseller-product-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.2s ease;
}

.bestseller-product-card:hover {
  border-color: #8E4A3E;
  box-shadow: 0 6px 18px rgba(40, 20, 10, 0.06);
  transform: translateY(-2px);
}

.card-wishlist-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #9C948B;
  cursor: pointer;
  z-index: 2;
}

.card-wishlist-btn.active {
  color: #DC2626;
  fill: #DC2626;
}

.card-img-wrap {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  background: #FAF8F5;
  border-radius: 8px;
  padding: 0.5rem;
}

.card-prod-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.card-info-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-brand-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.card-name-link {
  text-decoration: none;
  color: inherit;
  margin-bottom: 0.4rem;
}

.card-product-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.2rem;
}

.card-rating-line {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
}

.star-gold-fill {
  color: #F59E0B;
  fill: #F59E0B;
}

.rating-num {
  font-weight: 700;
  color: #1C1917;
}

.rating-revs {
  color: #78716C;
}

.card-price-box {
  margin-bottom: 0.75rem;
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
}

.card-price {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1C1917;
}

.card-compare-price {
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

/* Bottom Two Editorial Cards matching Brand Store.png */
.editorial-cards-container {
  margin-bottom: 3rem;
}

.editorial-cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.editorial-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.pitera-banner-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  background: linear-gradient(135deg, #FBF4F0 0%, #F5EAE4 100%);
  border-color: rgba(196, 98, 60, 0.15);
}

.pitera-text-area {
  flex: 1;
}

.pitera-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.2;
  margin-bottom: 0.75rem;
}

.pitera-copy {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #78716C;
  margin-bottom: 1.5rem;
}

.pitera-cta-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 9999px;
  padding: 0.55rem 1.25rem;
  font-size: 0.82rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: background 0.15s ease;
}

.pitera-cta-btn:hover {
  background: #7A3B30;
}

.pitera-img-area {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(142, 74, 62, 0.12);
}

.pitera-model-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Right Card: Build Your Routine */
.routine-banner-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.routine-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.45rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.routine-sub {
  font-size: 0.85rem;
  color: #78716C;
  margin-bottom: 1.75rem;
}

.routine-steps-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.routine-step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-prod-circle {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.35rem;
}

.step-prod-circle img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.step-number-tag {
  font-size: 0.72rem;
  font-weight: 600;
  color: #1C1917;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.step-number-tag span {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #8E4A3E;
  color: #FFFFFF;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.65rem;
  font-weight: 700;
}

.step-arrow {
  color: #C4B5AA;
}

/* Responsive */
@media (max-width: 1200px) {
  .bestsellers-cards-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .store-hero-banner {
    flex-direction: column;
    padding: 2rem;
    text-align: center;
  }
  .hero-pillars-row {
    justify-content: center;
  }
  .subnav-center-tabs {
    justify-content: center;
  }
  .editorial-cards-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .bestsellers-cards-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
