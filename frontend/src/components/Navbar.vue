<template>
  <header class="lumea-beauty-header" ref="headerRef">
    <!-- Format-matching Single-Row Header Bar -->
    <div class="header-main-row">
      <div class="container-fluid header-inner">
        <!-- Left: Mobile Menu Toggle & Brand Logo -->
        <div class="header-left">
          <button
            class="mobile-toggle"
            @click="mobileMenuOpen = !mobileMenuOpen"
            aria-label="Toggle Navigation Menu"
          >
            <Menu v-if="!mobileMenuOpen" :size="22" />
            <X v-else :size="22" />
          </button>

          <router-link to="/" class="brand-logo" aria-label="Luméa - Beauty Lives Here">
            <img src="/images/logo-lumea.png" alt="Luméa - Beauty Lives Here" class="brand-logo-img" />
          </router-link>
        </div>

        <!-- Center: Primary Navigation Links matching Format -->
        <nav class="desktop-nav-links">
          <!-- Shop Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'shop'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/shop"
              class="nav-link"
              :class="{ 'is-active': isShopActive }"
              @click="closeMenu"
            >
              <span>Shop</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'shop'" class="dropdown-menu">
              <router-link to="/shop" class="dropdown-link featured-link" @click="closeMenu">
                All Products (Shop All)
              </router-link>
              <router-link to="/category/cleansers" class="dropdown-link" @click="closeMenu">
                Cleansers &amp; Balms
              </router-link>
              <router-link to="/category/toners" class="dropdown-link" @click="closeMenu">
                Toners &amp; Essences
              </router-link>
              <router-link to="/category/serums" class="dropdown-link" @click="closeMenu">
                Serums &amp; Ampoules
              </router-link>
              <router-link to="/category/moisturizers" class="dropdown-link" @click="closeMenu">
                Moisturizers &amp; Creams
              </router-link>
              <router-link to="/category/sunscreens" class="dropdown-link" @click="closeMenu">
                Sun Protection SPF
              </router-link>
              <router-link to="/category/masks" class="dropdown-link" @click="closeMenu">
                Sheet &amp; Clay Masks
              </router-link>
              <router-link to="/category/treatments" class="dropdown-link" @click="closeMenu">
                Exfoliants &amp; Peels
              </router-link>
              <router-link to="/category/kits" class="dropdown-link" @click="closeMenu">
                Discovery Sets &amp; Bundles
              </router-link>
            </div>
          </div>

          <!-- Brands Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'brands'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/brands"
              class="nav-link"
              :class="{ 'is-active': isBrandsActive }"
              @click="closeMenu"
            >
              <span>Brands</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'brands'" class="dropdown-menu">
              <router-link to="/brands" class="dropdown-link featured-link" @click="closeMenu">
                Browse All Brands Directory &rarr;
              </router-link>
              <router-link to="/brand/sk-ii" class="dropdown-link" @click="closeMenu">SK-II Official Store</router-link>
              <router-link to="/brand/innisfree" class="dropdown-link" @click="closeMenu">Innisfree Official Store</router-link>
              <router-link to="/brand/the-ordinary" class="dropdown-link" @click="closeMenu">The Ordinary</router-link>
              <router-link to="/brand/laneige" class="dropdown-link" @click="closeMenu">LANEIGE</router-link>
              <router-link to="/brand/cerave" class="dropdown-link" @click="closeMenu">CeraVe</router-link>
              <router-link to="/brand/la-roche-posay" class="dropdown-link" @click="closeMenu">La Roche-Posay</router-link>
              <router-link to="/brand/bioderma" class="dropdown-link" @click="closeMenu">Bioderma</router-link>
              <router-link to="/brand/cosrx" class="dropdown-link" @click="closeMenu">COSRX</router-link>
              <router-link to="/brand/beauty-of-joseon" class="dropdown-link" @click="closeMenu">Beauty of Joseon</router-link>
            </div>
          </div>

          <!-- Skin Concerns & Types Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'concerns'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/concerns"
              class="nav-link"
              :class="{ 'is-active': route.path === '/concerns' }"
              @click="closeMenu"
            >
              <span>Concerns &amp; Types</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'concerns'" class="dropdown-menu">
              <router-link to="/concerns" class="dropdown-link featured-link" @click="closeMenu">
                Explore Full Diagnostic Matrix &rarr;
              </router-link>
              <div class="dropdown-section-label">By Skin Concern</div>
              <router-link to="/concerns?concern=dryness" class="dropdown-link" @click="closeMenu">
                Dryness &amp; Dehydration
              </router-link>
              <router-link to="/concerns?concern=dark-spots" class="dropdown-link" @click="closeMenu">
                Dark Spots &amp; Pigmentation
              </router-link>
              <router-link to="/concerns?concern=aging" class="dropdown-link" @click="closeMenu">
                Fine Lines &amp; Elasticity
              </router-link>
              <router-link to="/concerns?concern=acne" class="dropdown-link" @click="closeMenu">
                Blemishes &amp; Pore Care
              </router-link>
              <router-link to="/concerns?concern=sensitivity" class="dropdown-link" @click="closeMenu">
                Redness &amp; Sensitive Barrier
              </router-link>
              <div class="dropdown-section-label">By Skin Type</div>
              <router-link to="/concerns?type=dry" class="dropdown-link" @click="closeMenu">Dry Skin</router-link>
              <router-link to="/concerns?type=oily" class="dropdown-link" @click="closeMenu">Oily Skin</router-link>
              <router-link to="/concerns?type=combination" class="dropdown-link" @click="closeMenu">Combination Skin</router-link>
              <router-link to="/concerns?type=sensitive" class="dropdown-link" @click="closeMenu">Sensitive Skin</router-link>
            </div>
          </div>

          <!-- Direct Links -->
          <router-link
            to="/best-sellers"
            class="nav-link"
            :class="{ 'is-active': route.path === '/best-sellers' }"
            @click="closeMenu"
          >
            Best Sellers
          </router-link>
          <router-link
            to="/new-arrivals"
            class="nav-link"
            :class="{ 'is-active': route.path === '/new-arrivals' }"
            @click="closeMenu"
          >
            New Arrivals
          </router-link>
          <router-link
            to="/deals"
            class="nav-link highlight-deals"
            :class="{ 'is-active': route.path === '/deals' }"
            @click="closeMenu"
          >
            Deals
          </router-link>
          <router-link
            to="/articles"
            class="nav-link"
            :class="{ 'is-active': route.path.startsWith('/articles') }"
            @click="closeMenu"
          >
            Articles
          </router-link>
          <router-link
            to="/quiz"
            class="nav-link nav-quiz-badge"
            :class="{ 'is-active': route.path.startsWith('/quiz') || route.path === '/routine' }"
            @click="closeMenu"
          >
            <Sparkles :size="13" class="quiz-badge-sparkle" />
            <span>Skin Quiz</span>
          </router-link>
        </nav>

        <!-- Center-Right: Compact Pill Search Bar with Icon on the Right -->
        <div class="search-pill-container">
          <form class="search-pill-form" @submit.prevent="handleSearch">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search for products, brands, or concerns..."
              class="search-pill-input"
            />
            <button
              v-if="searchQuery"
              type="button"
              @click="searchQuery = ''"
              class="clear-search-btn"
              aria-label="Clear Search"
            >
              <X :size="13" />
            </button>
            <button type="submit" class="search-submit-btn" aria-label="Submit Search">
              <Search :size="16" class="search-icon" />
            </button>
          </form>
        </div>

        <!-- Far Right: Format Minimal Icons (Wishlist, Cart with Badge, Account) -->
        <div class="header-action-icons">
          <!-- Wishlist Heart Icon with Count Badge -->
          <router-link
            to="/wishlist"
            class="header-icon-btn"
            :class="{ 'is-active': route.path === '/wishlist' }"
            title="Wishlist"
            aria-label="Wishlist"
          >
            <Heart :size="20" :stroke-width="1.8" />
            <span v-if="wishlistStore.totalItems > 0" class="wishlist-circle-badge">
              {{ wishlistStore.totalItems }}
            </span>
          </router-link>

          <!-- Shopping Bag Cart Icon with Terracotta Badge -->
          <button
            class="header-icon-btn cart-btn-pos"
            @click="cartStore.openDrawer"
            title="Shopping Cart"
            aria-label="Shopping Cart"
          >
            <ShoppingBag :size="20" :stroke-width="1.8" />
            <span class="cart-circle-badge">
              {{ cartStore.totalItems }}
            </span>
          </button>

          <!-- Account User Icon -->
          <router-link
            to="/account"
            class="header-icon-btn"
            :class="{ 'is-active': route.path.startsWith('/account') || route.path === '/login' }"
            title="My Account"
            aria-label="My Account"
          >
            <User :size="20" :stroke-width="1.8" />
          </router-link>
        </div>
      </div>
    </div>

    <!-- Mobile Slide-Down Drawer for Responsive Screens -->
    <div v-if="mobileMenuOpen" class="mobile-drawer-backdrop" @click.self="mobileMenuOpen = false">
      <div class="mobile-drawer-panel">
        <div class="mobile-drawer-header">
          <img src="/images/logo-lumea.png" alt="Luméa" class="mobile-logo-img" />
          <button class="mobile-close-btn" @click="mobileMenuOpen = false" aria-label="Close Menu">
            <X :size="20" />
          </button>
        </div>

        <div class="mobile-search-box">
          <form class="search-pill-form" @submit.prevent="handleSearch">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search products, brands..."
              class="search-pill-input"
            />
            <button type="submit" class="search-submit-btn" aria-label="Search">
              <Search :size="16" />
            </button>
          </form>
        </div>

        <nav class="mobile-nav-list">
          <router-link to="/shop" class="mobile-nav-item" @click="closeMenu">
            <span>Shop All Products</span>
          </router-link>
          <router-link to="/category/cleansers" class="mobile-nav-subitem" @click="closeMenu">Cleansers</router-link>
          <router-link to="/category/toners" class="mobile-nav-subitem" @click="closeMenu">Toners</router-link>
          <router-link to="/category/serums" class="mobile-nav-subitem" @click="closeMenu">Serums</router-link>
          <router-link to="/category/moisturizers" class="mobile-nav-subitem" @click="closeMenu">Moisturizers</router-link>

          <div class="mobile-divider"></div>

          <router-link to="/brands" class="mobile-nav-item" @click="closeMenu">
            <span>All Brands Directory</span>
          </router-link>
          <router-link to="/brand/sk-ii" class="mobile-nav-subitem" @click="closeMenu">SK-II</router-link>
          <router-link to="/brand/innisfree" class="mobile-nav-subitem" @click="closeMenu">Innisfree</router-link>
          <router-link to="/brand/the-ordinary" class="mobile-nav-subitem" @click="closeMenu">The Ordinary</router-link>
          <router-link to="/brand/laneige" class="mobile-nav-subitem" @click="closeMenu">LANEIGE</router-link>
          <router-link to="/brand/cerave" class="mobile-nav-subitem" @click="closeMenu">CeraVe</router-link>

          <div class="mobile-divider"></div>

          <router-link to="/best-sellers" class="mobile-nav-item" @click="closeMenu">Best Sellers</router-link>
          <router-link to="/new-arrivals" class="mobile-nav-item" @click="closeMenu">New Arrivals</router-link>
          <router-link to="/deals" class="mobile-nav-item highlight-deals" @click="closeMenu">Special Offers &amp; Deals</router-link>
          <router-link to="/articles" class="mobile-nav-item" @click="closeMenu">Skincare Journal &amp; Articles</router-link>
          <router-link to="/quiz" class="mobile-nav-item highlight-quiz" @click="closeMenu">
            <Sparkles :size="16" class="mobile-quiz-sparkle" />
            <span>Skin Diagnostic Quiz</span>
          </router-link>
          <router-link to="/returns/request" class="mobile-nav-item" @click="closeMenu">Returns &amp; Refunds</router-link>
          <router-link to="/concerns" class="mobile-nav-item" @click="closeMenu">Skin Concerns &amp; Types</router-link>
          <router-link to="/wishlist" class="mobile-nav-item" @click="closeMenu">My Saved Wishlist</router-link>
        </nav>

        <div class="mobile-actions-footer">
          <button class="mobile-account-btn" @click="openAccountModal">
            <User :size="18" />
            <span>Sign In / My Account</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Account Modal -->
    <div v-if="showAccountModal" class="account-modal-backdrop" @click.self="showAccountModal = false">
      <div class="account-modal-card">
        <div class="modal-header">
          <h3>Welcome to Luméa</h3>
          <button class="modal-close" @click="showAccountModal = false" aria-label="Close">
            <X :size="18" />
          </button>
        </div>
        <p class="modal-sub">Sign in to track orders, save your skin routine, and collect beauty points.</p>

        <form @submit.prevent="handleAccountSubmit" class="account-form">
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" v-model="accountEmail" placeholder="you@example.com" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" v-model="accountPassword" placeholder="••••••••" required />
          </div>
          <button type="submit" class="btn btn-dark btn-block">Sign In</button>
        </form>
        <div class="modal-footer-note">
          <router-link to="/account/profile" class="admin-link" @click="showAccountModal = false" style="font-weight: 600; color: #9E3332; display: block; margin-bottom: 8px;">
            Go to My Skin Profile &rarr;
          </router-link>
          <div>
            <span>Admin console user?</span>
            <a href="http://localhost:5174" target="_blank" class="admin-link">Open Atelier Admin &rarr;</a>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { useWishlistStore } from '@/stores/wishlist'
import {
  ChevronDown,
  Heart,
  Menu,
  Search,
  ShoppingBag,
  Sparkles,
  User,
  X
} from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()
const productStore = useProductStore()
const wishlistStore = useWishlistStore()

const headerRef = ref(null)
const mobileMenuOpen = ref(false)
const searchQuery = ref('')
const activeDropdown = ref(null)
const showAccountModal = ref(false)
const accountEmail = ref('customer@lumea.com')
const accountPassword = ref('password123')

const isShopActive = computed(() => {
  return route.path.startsWith('/shop') || route.path.startsWith('/category')
})

const isBrandsActive = computed(() => {
  return route.path.startsWith('/brand')
})

function updateHeaderHeight() {
  if (headerRef.value) {
    const h = headerRef.value.offsetHeight
    document.documentElement.style.setProperty('--navbar-height', `${h}px`)
  }
}

onMounted(() => {
  updateHeaderHeight()
  window.addEventListener('resize', updateHeaderHeight)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateHeaderHeight)
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim()
    productStore.filters.search = q
    router.push({ path: '/search', query: { q } })
    mobileMenuOpen.value = false
  }
}

function closeMenu() {
  mobileMenuOpen.value = false
  activeDropdown.value = null
}

function scrollToSection(sectionId) {
  closeMenu()
  const el = document.getElementById(sectionId)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  } else {
    router.push(`/#${sectionId}`)
  }
}

function openAccountModal() {
  mobileMenuOpen.value = false
  showAccountModal.value = true
}

function handleAccountSubmit() {
  showAccountModal.value = false
  router.push('/account/profile')
}
</script>

<style scoped>
/* ==========================================================================
   FORMAT-MATCHING SINGLE-ROW HEADER
   ========================================================================== */
.lumea-beauty-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #FAF8F5;
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
  box-shadow: 0 1px 6px rgba(28, 25, 23, 0.03);
}

.header-main-row {
  height: 68px;
  display: flex;
  align-items: center;
}

.container-fluid.header-inner {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* 1. Left: Brand Logo */
.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.brand-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.brand-logo-img {
  height: 38px;
  width: auto;
  object-fit: contain;
  display: block;
  transition: transform 0.2s ease;
}

.brand-logo:hover .brand-logo-img {
  transform: scale(1.02);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  padding: 4px;
}

/* 2. Center: Desktop Nav Links */
.desktop-nav-links {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex-shrink: 0;
}

.nav-dropdown-item {
  position: relative;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.22rem;
  font-family: var(--font-sans);
  font-size: 0.86rem;
  font-weight: 500;
  color: #2B2625;
  text-decoration: none;
  padding: 0.5rem 0.15rem;
  transition: color 0.15s ease;
  cursor: pointer;
  white-space: nowrap;
}

.nav-link:hover {
  color: #8E4A3E;
}

.nav-link.is-active {
  color: #8E4A3E;
  font-weight: 600;
}

.nav-link.highlight-deals {
  color: #8E4A3E;
  font-weight: 600;
}

.nav-link.nav-quiz-badge {
  color: #8E4A3E;
  font-weight: 600;
  background: rgba(142, 74, 62, 0.08);
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  border: 1px solid rgba(142, 74, 62, 0.2);
  transition: all 0.2s ease;
}

.nav-link.nav-quiz-badge:hover,
.nav-link.nav-quiz-badge.is-active {
  background: #8E4A3E;
  color: #FFFFFF;
}

.nav-link.nav-quiz-badge:hover .quiz-badge-sparkle,
.nav-link.nav-quiz-badge.is-active .quiz-badge-sparkle {
  color: #FFFFFF;
}

.quiz-badge-sparkle {
  color: #8E4A3E;
}

.highlight-quiz {
  display: flex !important;
  align-items: center;
  gap: 8px;
  color: #8E4A3E !important;
  font-weight: 600;
}

.mobile-quiz-sparkle {
  color: #8E4A3E;
}

.caret-icon {
  color: #8C877F;
  transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1), color 0.15s ease;
}

.nav-dropdown-item:hover .caret-icon {
  transform: rotate(180deg);
  color: #8E4A3E;
}

/* Dropdown Menus */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.09);
  border-radius: 10px;
  box-shadow: 0 10px 28px rgba(35, 25, 20, 0.08);
  min-width: 220px;
  padding: 0.5rem 0;
  z-index: 200;
  animation: dropdownFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-link {
  display: block;
  padding: 0.55rem 1.25rem;
  font-size: 0.84rem;
  color: #44403C;
  text-decoration: none;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.dropdown-link:hover {
  background-color: #F8F4F0;
  color: #8E4A3E;
}

.dropdown-link.featured-link {
  font-weight: 600;
  color: #8E4A3E;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
  margin-bottom: 0.25rem;
}

.dropdown-section-label {
  padding: 0.4rem 1.25rem 0.15rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #8C877F;
  border-top: 1px solid rgba(28, 25, 23, 0.05);
  margin-top: 0.25rem;
}

/* 3. Center-Right: Search Pill Form (Icon on Right matching format) */
.search-pill-container {
  flex: 0 1 310px;
  min-width: 180px;
}

.search-pill-form {
  position: relative;
  display: flex;
  align-items: center;
  background: #F4EFEB;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 9999px;
  padding: 0.42rem 0.75rem 0.42rem 1.1rem;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.search-pill-form:focus-within {
  background: #FFFFFF;
  border-color: #8E4A3E;
  box-shadow: 0 0 0 2px rgba(142, 74, 62, 0.12);
}

.search-pill-input {
  flex: 1;
  width: 100%;
  border: none;
  background: transparent;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  font-family: var(--font-sans);
}

.search-pill-input::placeholder {
  color: #8C877F;
  font-size: 0.8rem;
}

.clear-search-btn {
  color: #8C877F;
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 4px;
  display: flex;
  align-items: center;
}

.search-submit-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #2B2625;
  display: flex;
  align-items: center;
  padding: 2px 4px;
  transition: color 0.15s ease, transform 0.15s ease;
}

.search-submit-btn:hover {
  color: #8E4A3E;
  transform: scale(1.08);
}

/* 4. Far Right: Clean Minimal Icons (No Text Labels) */
.header-action-icons {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex-shrink: 0;
}

.header-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  position: relative;
  padding: 4px;
  text-decoration: none;
  transition: color 0.15s ease, transform 0.15s ease;
}

.header-icon-btn:hover {
  color: #8E4A3E;
  transform: scale(1.08);
}

.cart-btn-pos {
  position: relative;
}

/* Format Red/Terracotta Circular Cart Badge */
.cart-circle-badge {
  position: absolute;
  top: -3px;
  right: -7px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 1.5px solid #FAF8F5;
}

/* Wishlist Badge */
.wishlist-circle-badge {
  position: absolute;
  top: -3px;
  right: -7px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #242721;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 1.5px solid #FAF8F5;
}

/* ==========================================================================
   MOBILE DRAWER & RESPONSIVE BEHAVIOR
   ========================================================================== */
@media (max-width: 1180px) {
  .desktop-nav-links {
    gap: 0.85rem;
  }
  .nav-link {
    font-size: 0.82rem;
  }
  .search-pill-container {
    flex: 0 1 240px;
  }
}

@media (max-width: 1040px) {
  .desktop-nav-links {
    display: none;
  }
  .mobile-toggle {
    display: flex;
  }
  .search-pill-container {
    display: none;
  }
}

.mobile-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.45);
  backdrop-filter: blur(4px);
  z-index: 250;
  display: flex;
  justify-content: flex-start;
}

.mobile-drawer-panel {
  width: 82%;
  max-width: 320px;
  height: 100vh;
  background: #FFFFFF;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 1.5rem;
  animation: slideInLeft 0.25s cubic-bezier(0.23, 1, 0.32, 1);
}

@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

.mobile-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.mobile-logo-img {
  height: 32px;
  width: auto;
}

.mobile-close-btn {
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  padding: 4px;
}

.mobile-search-box {
  margin-bottom: 1.25rem;
}

.mobile-nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.mobile-nav-item {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
}

.mobile-nav-item:hover,
.mobile-nav-item.highlight-deals {
  color: #8E4A3E;
}

.mobile-nav-subitem {
  font-size: 0.85rem;
  color: #57534E;
  text-decoration: none;
  padding: 0.35rem 0.75rem;
  display: block;
}

.mobile-nav-subitem:hover {
  color: #8E4A3E;
}

.mobile-divider {
  height: 1px;
  background: rgba(28, 25, 23, 0.08);
  margin: 0.75rem 0;
}

.mobile-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(28, 25, 23, 0.08);
}

.mobile-account-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #242721;
  color: #FFFFFF;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.88rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

/* ==========================================================================
   ACCOUNT QUICK MODAL
   ========================================================================== */
.account-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.6);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 1.5rem;
}

.account-modal-card {
  width: 100%;
  max-width: 420px;
  background: #FFFFFF;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.modal-header h3 {
  font-family: var(--font-serif);
  font-size: 1.4rem;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #8C877F;
  padding: 4px;
}

.modal-sub {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.account-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.form-group input {
  padding: 0.7rem 1rem;
  border: 1px solid rgba(28, 25, 23, 0.15);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-family: inherit;
}

.btn-dark {
  background: #242721;
  color: #FFFFFF;
  padding: 0.85rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  border: none;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s ease;
}

.btn-dark:hover {
  background: #171914;
}

.btn-block {
  width: 100%;
}

.modal-footer-note {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.78rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.admin-link {
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
}
</style>
