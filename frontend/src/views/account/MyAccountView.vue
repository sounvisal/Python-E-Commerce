<template>
  <div class="my-account-page">
    <div class="container account-container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/" class="crumb-link">Home</router-link>
        <span class="crumb-sep">›</span>
        <span class="crumb-current">My Account</span>
      </nav>

      <!-- Panoramic Hero Banner matching My Account.png -->
      <section class="account-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">My Account</h1>
          <p class="hero-desc">
            Manage your account, orders, and beauty journey.
          </p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banner-my-account.jpg"
            alt="Luméa Beauty Collection"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Good<br />Skin Days<br />Are Ahead.</span>
          </div>
        </div>
      </section>

      <!-- 3-Column Main Content Layout matching format/My Account.png -->
      <div class="account-3col-grid">
        <!-- ========================================================= -->
        <!-- LEFT COLUMN: Reusable Account Sidebar                     -->
        <!-- ========================================================= -->
        <div class="sidebar-column">
          <AccountSidebar
            currentActive="overview"
            @open-addresses="showAddressModal = true"
            @open-payments="showPaymentModal = true"
            @edit-profile="showProfileModal = true"
          />
        </div>

        <!-- ========================================================= -->
        <!-- CENTER COLUMN: Dashboard Main Stage                       -->
        <!-- ========================================================= -->
        <main class="dashboard-main-column">
          <!-- Welcome Greeting Card -->
          <div class="welcome-banner-card">
            <div class="welcome-header-content">
              <span class="greeting-pre">Hello,</span>
              <h2 class="greeting-name">{{ authStore.userFirstName }}!</h2>
              <p class="greeting-sub">Thanks for being part of the Luméa community.</p>
            </div>

            <!-- Luméa Rewards Badge inside Banner -->
            <div class="rewards-callout-pill">
              <div class="rewards-crown-wrap">
                <Crown :size="18" class="crown-svg" />
              </div>
              <div class="rewards-text-col">
                <span class="rewards-badge-title">Luméa Rewards</span>
                <span class="rewards-badge-desc">Beauty Rewards for a Brighter You.</span>
                <button class="rewards-link-btn" @click="showRewardsModal = true">
                  View Benefits &rarr;
                </button>
              </div>
            </div>
          </div>

          <!-- 4 Stat Counters Grid matching mockup -->
          <div class="stats-counters-grid">
            <div class="stat-counter-card">
              <div class="stat-icon-wrap">
                <Calendar :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ ordersStore.totalOrders }}</span>
                <span class="stat-label">Total Orders</span>
              </div>
            </div>

            <router-link to="/wishlist" class="stat-counter-card clickable">
              <div class="stat-icon-wrap">
                <Heart :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ wishlistStore.totalItems }}</span>
                <span class="stat-label">Items in Wishlist</span>
              </div>
            </router-link>

            <router-link to="/wishlist" class="stat-counter-card clickable">
              <div class="stat-icon-wrap">
                <Bookmark :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ authStore.user.savedForLaterCount || 3 }}</span>
                <span class="stat-label">Saved for Later</span>
              </div>
            </router-link>

            <div class="stat-counter-card">
              <div class="stat-icon-wrap">
                <Star :size="18" class="stat-icon star-active" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ authStore.user.rewardPoints }}</span>
                <span class="stat-label">Reward Points</span>
              </div>
            </div>
          </div>

          <!-- Recent Orders Section -->
          <section class="dashboard-section recent-orders-section">
            <div class="section-header-row">
              <h3 class="section-title">Recent Orders</h3>
              <router-link to="/account/orders" class="section-view-all">
                View All Orders &rarr;
              </router-link>
            </div>

            <div class="recent-orders-list">
              <div
                v-for="order in ordersStore.recentOrders"
                :key="order.orderNumber"
                class="recent-order-row-card"
              >
                <!-- Mini Items Thumbnail Stack -->
                <div class="order-thumbs-stack">
                  <div
                    v-for="(item, idx) in order.items.slice(0, 2)"
                    :key="idx"
                    class="order-mini-thumb"
                  >
                    <img :src="item.image_url" :alt="item.name" />
                  </div>
                </div>

                <!-- Order Meta -->
                <div class="order-meta-col">
                  <router-link :to="`/account/orders/${order.orderNumber}`" class="order-id-link">
                    Order #{{ order.orderNumber }}
                  </router-link>
                  <span class="order-placed-date">{{ order.placedAt }}</span>
                </div>

                <!-- Status Dot & Label -->
                <div class="order-status-col">
                  <span
                    class="status-indicator-dot"
                    :class="order.statusType"
                  ></span>
                  <span class="status-name-text">{{ order.status }}</span>
                </div>

                <!-- Order Total -->
                <div class="order-price-col">
                  <span class="order-total-val">${{ order.total.toFixed(2) }}</span>
                </div>

                <!-- View Details CTA -->
                <div class="order-action-col">
                  <router-link
                    :to="`/account/orders/${order.orderNumber}`"
                    class="btn-view-order-details"
                  >
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </section>

          <!-- Recommended for You Carousel using UNIVERSAL ProductCard -->
          <section class="dashboard-section recommendations-section">
            <div class="section-header-row">
              <div>
                <h3 class="section-title">Recommended for You</h3>
                <p class="section-subtitle">Based on your recent purchases</p>
              </div>
              <router-link to="/shop" class="section-view-all">
                See All Recommendations &rarr;
              </router-link>
            </div>

            <!-- Grid of standard ProductCard matching homepage -->
            <div class="recommended-cards-grid">
              <ProductCard
                v-for="product in recommendedProducts"
                :key="product.id"
                :product="product"
              />
            </div>
          </section>
        </main>

        <!-- ========================================================= -->
        <!-- RIGHT COLUMN: Addresses, Payments & Loyalty               -->
        <!-- ========================================================= -->
        <aside class="dashboard-aside-column">
          <!-- Saved Addresses Card -->
          <div class="aside-card saved-addresses-card">
            <div class="aside-card-header">
              <h3 class="aside-card-title">Saved Addresses</h3>
              <button class="aside-manage-btn" @click="showAddressModal = true">
                Manage &rarr;
              </button>
            </div>

            <div class="saved-address-body" v-if="authStore.defaultAddress">
              <span class="default-pill-badge">Default</span>
              <div class="address-details-wrap">
                <MapPin :size="16" class="address-pin-icon" />
                <div class="address-text-content">
                  <strong class="addr-name">{{ authStore.defaultAddress.name }}</strong>
                  <p class="addr-street">{{ authStore.defaultAddress.street }}</p>
                  <p class="addr-commune">{{ authStore.defaultAddress.commune }}, {{ authStore.defaultAddress.district }}</p>
                  <p class="addr-city">{{ authStore.defaultAddress.city }} {{ authStore.defaultAddress.postalCode }}, {{ authStore.defaultAddress.country }}</p>
                  <span class="addr-phone">{{ authStore.defaultAddress.phone }}</span>
                </div>
              </div>

              <button class="btn-add-dashed-action" @click="showAddressModal = true">
                <Plus :size="15" />
                <span>Add New Address</span>
              </button>
            </div>
          </div>

          <!-- Payment Methods Card -->
          <div class="aside-card payment-methods-card">
            <div class="aside-card-header">
              <h3 class="aside-card-title">Payment Methods</h3>
              <button class="aside-manage-btn" @click="showPaymentModal = true">
                Manage &rarr;
              </button>
            </div>

            <div class="payment-methods-list">
              <div
                v-for="payment in authStore.user.paymentMethods"
                :key="payment.id"
                class="payment-row-item"
              >
                <div class="payment-provider-icon" :style="{ backgroundColor: payment.color || '#005D8E' }">
                  <span class="provider-symbol">{{ payment.provider }}</span>
                </div>

                <div class="payment-meta-text">
                  <div class="payment-name-row">
                    <span class="pay-name">{{ payment.name }} {{ payment.accountNumber }}</span>
                    <span v-if="payment.isDefault" class="default-tag-pill">Default</span>
                  </div>
                  <span class="pay-expiry">Expires {{ payment.expiry }}</span>
                </div>

                <button class="pay-options-btn" title="Options">
                  <MoreVertical :size="15" />
                </button>
              </div>

              <button class="btn-add-dashed-action" @click="showPaymentModal = true">
                <Plus :size="15" />
                <span>Add Payment Method</span>
              </button>
            </div>
          </div>

          <!-- Luméa Rewards Promo Card matching mockup -->
          <div class="aside-card rewards-promo-card">
            <h4 class="rewards-promo-title">Luméa Rewards</h4>
            <p class="rewards-promo-tagline">Shop More, Glow More.</p>

            <ul class="rewards-perks-bullets">
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Earn points on every purchase</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Exclusive member discounts</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Early access to new arrivals</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Birthday surprises</span>
              </li>
            </ul>

            <button class="btn-rewards-learn-more" @click="showRewardsModal = true">
              Learn More
            </button>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useOrdersStore } from '@/stores/orders'
import { useWishlistStore } from '@/stores/wishlist'
import AccountSidebar from '@/components/account/AccountSidebar.vue'
import ProductCard from '@/components/ProductCard.vue'
import {
  Calendar,
  Heart,
  Bookmark,
  Star,
  Crown,
  MapPin,
  Plus,
  MoreVertical,
  Check
} from 'lucide-vue-next'

const authStore = useAuthStore()
const ordersStore = useOrdersStore()
const wishlistStore = useWishlistStore()

const showAddressModal = ref(false)
const showPaymentModal = ref(false)
const showProfileModal = ref(false)
const showRewardsModal = ref(false)

// 4 Exact Recommendations matching format/My Account.png:
// 1. SK-II Facial Treatment Essence ($99.00)
// 2. Laneige Lip Sleeping Mask ($24.00)
// 3. The Ordinary Niacinamide 10% + Zinc 1% ($17.80)
// 4. CeraVe Hydrating Facial Cleanser ($16.00)
const recommendedProducts = [
  {
    id: 101,
    brand: 'SK-II',
    name: 'Facial Treatment Essence',
    volume: '230 ml',
    price: 99.00,
    rating: 4.8,
    reviews: '1.2K',
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence'
  },
  {
    id: 103,
    brand: 'Laneige',
    name: 'Lip Sleeping Mask',
    volume: '20 g',
    price: 24.00,
    rating: 4.8,
    reviews: '4.1K',
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask'
  },
  {
    id: 102,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1%',
    volume: '30 ml',
    price: 17.80,
    rating: 4.7,
    reviews: '9.8K',
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1'
  },
  {
    id: 104,
    brand: 'CeraVe',
    name: 'Hydrating Facial Cleanser',
    volume: '236 ml',
    price: 16.00,
    rating: 4.7,
    reviews: '6.2K',
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-hydrating-cleanser'
  }
]
</script>

<style scoped>
/* ==========================================================================
   MY ACCOUNT PAGE (Strictly matches format/My Account.png)
   ========================================================================== */

.my-account-page {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 5rem;
}

.account-container {
  max-width: 1340px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Breadcrumbs */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.84rem;
  color: #78716C;
  padding: 0.6rem 0 0.5rem;
}

.crumb-link {
  color: #57534E;
  text-decoration: none;
}

.crumb-link:hover {
  color: #8E4A3E;
}

.crumb-sep {
  color: #A8A29E;
}

.crumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Panoramic Hero Banner matching My Account.png */
.account-hero-banner {
  background: #FFFFFF;
  border-radius: 18px;
  border: 1px solid #EFE6DD;
  box-shadow: 0 4px 18px rgba(28, 25, 23, 0.03);
  display: grid;
  grid-template-columns: 1.1fr 1.35fr;
  overflow: hidden;
  align-items: stretch;
  min-height: 250px;
  margin-bottom: 1.75rem;
}

.hero-left-content {
  padding: 1.75rem 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #FFFFFF;
  z-index: 2;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.15;
  letter-spacing: -0.01em;
  margin-bottom: 0.5rem;
}

.hero-desc {
  font-size: 1.15rem;
  line-height: 1.55;
  color: #57534E;
  max-width: 520px;
}

.hero-right-stage {
  position: relative;
  width: 100%;
  min-height: 250px;
  overflow: hidden;
  background: #FAF6F1;
}

.hero-banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;
  display: block;
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 15%);
  mask-image: linear-gradient(to right, transparent 0%, black 15%);
}

.hero-fade-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 120px;
  background: linear-gradient(to right, #FFFFFF, transparent);
  pointer-events: none;
  z-index: 2;
}

.banner-script-overlay {
  position: absolute;
  top: 24px;
  right: 32px;
  font-family: 'Cormorant Garamond', cursive, serif;
  font-style: italic;
  font-size: 1.65rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.15;
  text-align: right;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.95);
  pointer-events: none;
  z-index: 3;
}

/* ================= 3-COLUMN LAYOUT ================= */
.account-3col-grid {
  display: grid;
  grid-template-columns: 260px 1fr 340px;
  gap: 1.75rem;
  align-items: start;
}

/* ================= CENTER MAIN COLUMN ================= */
.dashboard-main-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Welcome Greeting Banner */
.welcome-banner-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.welcome-header-content {
  display: flex;
  flex-direction: column;
}

.greeting-pre {
  font-size: 0.9rem;
  font-weight: 500;
  color: #8E4A3E;
}

.greeting-name {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2rem;
  font-weight: 700;
  color: #1C1917;
  letter-spacing: -0.01em;
  line-height: 1.15;
  margin-bottom: 0.25rem;
}

.greeting-sub {
  font-size: 0.88rem;
  color: #57534E;
}

/* Rewards Pill inside Welcome */
.rewards-callout-pill {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  background: #FFF8F6;
  border: 1px solid #F6D7D0;
  padding: 1rem 1.25rem;
  border-radius: 12px;
}

.rewards-crown-wrap {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #8E4A3E;
  display: flex;
  align-items: center;
  justify-content: center;
}

.crown-svg {
  color: #FFFFFF;
}

.rewards-text-col {
  display: flex;
  flex-direction: column;
}

.rewards-badge-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: #8E4A3E;
}

.rewards-badge-desc {
  font-size: 0.78rem;
  color: #57534E;
  margin-bottom: 0.25rem;
}

.rewards-link-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #8E4A3E;
  cursor: pointer;
  text-align: left;
}

.rewards-link-btn:hover {
  text-decoration: underline;
}

/* 4 Counters Grid */
.stats-counters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-counter-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  padding: 1.25rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 2px 8px rgba(28, 25, 23, 0.02);
  text-decoration: none;
  transition: all 0.2s ease;
}

.stat-counter-card.clickable:hover {
  border-color: #D4BAA8;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(28, 25, 23, 0.06);
}

.stat-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #FAF7F2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon {
  color: #8E4A3E;
}

.stat-icon.star-active {
  color: #D4AF37;
  fill: #D4AF37;
}

.stat-text-col {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.1;
}

.stat-label {
  font-size: 0.76rem;
  color: #78716C;
  font-weight: 500;
}

/* Section Common */
.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.section-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: #1C1917;
}

.section-subtitle {
  font-size: 0.82rem;
  color: #78716C;
}

.section-view-all {
  font-size: 0.84rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
}

.section-view-all:hover {
  text-decoration: underline;
}

/* Recent Orders List */
.recent-orders-list {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.02);
}

.recent-order-row-card {
  display: grid;
  grid-template-columns: 80px 1.4fr 1.2fr 1fr 120px;
  align-items: center;
  gap: 1rem;
  padding: 1.15rem 1.5rem;
  border-bottom: 1px solid #F5EFEB;
  transition: background 0.15s ease;
}

.recent-order-row-card:last-child {
  border-bottom: none;
}

.recent-order-row-card:hover {
  background: #FAF7F2;
}

.order-thumbs-stack {
  display: flex;
  align-items: center;
  gap: 4px;
}

.order-mini-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #EFE6DD;
  background: #FAF7F2;
}

.order-mini-thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.order-meta-col {
  display: flex;
  flex-direction: column;
}

.order-id-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
}

.order-id-link:hover {
  color: #8E4A3E;
}

.order-placed-date {
  font-size: 0.78rem;
  color: #78716C;
}

.order-status-col {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator-dot.delivered {
  background-color: #2E7D32;
}

.status-indicator-dot.shipped {
  background-color: #1565C0;
}

.status-indicator-dot.processing {
  background-color: #78716C;
}

.status-indicator-dot.cancelled {
  background-color: #C62828;
}

.status-name-text {
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
}

.order-price-col {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.btn-view-order-details {
  display: inline-block;
  padding: 6px 14px;
  border: 1px solid #D4BAA8;
  background: #FFFFFF;
  color: #8E4A3E;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  transition: all 0.2s ease;
}

.btn-view-order-details:hover {
  background: #8E4A3E;
  border-color: #8E4A3E;
  color: #FFFFFF;
}

/* Recommended Cards Grid using standard ProductCard */
.recommended-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

/* ================= RIGHT ASIDE COLUMN ================= */
.dashboard-aside-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.aside-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.aside-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.15rem;
}

.aside-card-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.1rem;
  font-weight: 600;
  color: #1C1917;
}

.aside-manage-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
}

.aside-manage-btn:hover {
  text-decoration: underline;
}

/* Address Card */
.saved-address-body {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.default-pill-badge {
  display: inline-block;
  align-self: flex-start;
  padding: 2px 8px;
  background: #FFF5F2;
  color: #8E4A3E;
  border: 1px solid #F6D7D0;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.address-details-wrap {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.address-pin-icon {
  color: #8E4A3E;
  margin-top: 2px;
  flex-shrink: 0;
}

.address-text-content {
  font-size: 0.82rem;
  line-height: 1.45;
  color: #57534E;
}

.addr-name {
  color: #1C1917;
  font-size: 0.86rem;
}

.addr-phone {
  display: block;
  margin-top: 4px;
  color: #78716C;
}

.btn-add-dashed-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  width: 100%;
  padding: 0.65rem 1rem;
  background: #FFFFFF;
  border: 1px dashed #D4BAA8;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.btn-add-dashed-action:hover {
  background: #FDF2EE;
  border-color: #8E4A3E;
}

/* Payment Methods List */
.payment-methods-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.payment-row-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #F5EFEB;
}

.payment-row-item:last-of-type {
  border-bottom: none;
}

.payment-provider-icon {
  width: 38px;
  height: 26px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 0.68rem;
  font-weight: 700;
  flex-shrink: 0;
}

.payment-meta-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.payment-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pay-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
}

.default-tag-pill {
  font-size: 0.65rem;
  padding: 1px 5px;
  background: #E8F5E9;
  color: #2E7D32;
  border-radius: 3px;
  font-weight: 600;
}

.pay-expiry {
  font-size: 0.74rem;
  color: #78716C;
}

.pay-options-btn {
  background: none;
  border: none;
  color: #A8A29E;
  cursor: pointer;
  padding: 4px;
}

/* Luméa Rewards Promo Card */
.rewards-promo-card {
  background: linear-gradient(135deg, #FFF9F6 0%, #FBF0EB 100%);
  border-color: #F0D5CD;
}

.rewards-promo-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 2px;
}

.rewards-promo-tagline {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 1rem;
}

.rewards-perks-bullets {
  list-style: none;
  padding: 0;
  margin: 0 0 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.rewards-perks-bullets li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #57534E;
}

.check-perk-icon {
  color: #8E4A3E;
  flex-shrink: 0;
}

.btn-rewards-learn-more {
  width: 100%;
  padding: 0.65rem 1rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(142, 74, 62, 0.2);
  transition: all 0.2s ease;
}

.btn-rewards-learn-more:hover {
  background: #76392F;
}

/* Responsive */
@media (max-width: 1200px) {
  .account-3col-grid {
    grid-template-columns: 240px 1fr;
  }
  .dashboard-aside-column {
    grid-column: span 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .rewards-promo-card {
    grid-column: span 2;
  }
}

@media (max-width: 900px) {
  .account-hero-banner {
    grid-template-columns: 1fr;
  }
  .hero-right-stage {
    min-height: 180px;
  }
  .account-3col-grid {
    grid-template-columns: 1fr;
  }
  .stats-counters-grid {
    grid-template-columns: 1fr 1fr;
  }
  .recommended-cards-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
