<template>
  <div class="my-orders-page">
    <div class="container account-container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/" class="crumb-link">Home</router-link>
        <span class="crumb-sep">›</span>
        <router-link to="/account" class="crumb-link">My Account</router-link>
        <span class="crumb-sep">›</span>
        <span class="crumb-current">My Orders</span>
      </nav>

      <!-- Panoramic Hero Banner matching My Orders.png -->
      <section class="orders-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">My Orders</h1>
          <p class="hero-desc">
            Track, manage, and view all your orders in one place.
          </p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banner-my-orders.jpg"
            alt="Luméa Orders and Gift Sets"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Good<br />Choices<br />Brighter<br />Tomorrows.</span>
          </div>
        </div>
      </section>

      <!-- 2-Column Layout: Sidebar + Orders Management -->
      <div class="orders-body-grid">
        <!-- ========================================================= -->
        <!-- LEFT: ACCOUNT SIDEBAR                                     -->
        <!-- ========================================================= -->
        <aside class="sidebar-column">
          <AccountSidebar currentActive="orders" />
        </aside>

        <!-- ========================================================= -->
        <!-- RIGHT: ORDERS LISTING & FILTERING                         -->
        <!-- ========================================================= -->
        <main class="orders-main-column">
          <!-- Filter Tabs matching format/My Orders.png -->
          <div class="orders-nav-toolbar">
            <div class="order-status-tabs" role="tablist">
              <button
                type="button"
                class="order-tab-btn"
                :class="{ active: currentTab === 'all' }"
                @click="currentTab = 'all'"
              >
                <span>All Orders ({{ ordersStore.totalOrders }})</span>
              </button>
              <button
                type="button"
                class="order-tab-btn"
                :class="{ active: currentTab === 'processing' }"
                @click="currentTab = 'processing'"
              >
                <span>Processing ({{ ordersStore.processingOrders.length }})</span>
              </button>
              <button
                type="button"
                class="order-tab-btn"
                :class="{ active: currentTab === 'shipped' }"
                @click="currentTab = 'shipped'"
              >
                <span>Shipped ({{ ordersStore.shippedOrders.length }})</span>
              </button>
              <button
                type="button"
                class="order-tab-btn"
                :class="{ active: currentTab === 'delivered' }"
                @click="currentTab = 'delivered'"
              >
                <span>Delivered ({{ ordersStore.deliveredOrders.length }})</span>
              </button>
              <button
                type="button"
                class="order-tab-btn"
                :class="{ active: currentTab === 'cancelled' }"
                @click="currentTab = 'cancelled'"
              >
                <span>Cancelled ({{ ordersStore.cancelledOrders.length }})</span>
              </button>
            </div>

            <!-- Search & Filter Controls -->
            <div class="orders-search-filter-row">
              <div class="search-input-wrap">
                <Search :size="16" class="search-icon" />
                <input
                  type="text"
                  v-model="searchQuery"
                  placeholder="Search by order number, product, or date..."
                  class="order-search-field"
                />
              </div>

              <div class="filter-dropdown-wrap">
                <button
                  type="button"
                  class="btn-filter-toggle"
                  @click="showFilterDropdown = !showFilterDropdown"
                >
                  <Filter :size="15" />
                  <span>Filter</span>
                  <ChevronDown :size="14" />
                </button>

                <div v-if="showFilterDropdown" class="filter-menu-popover">
                  <button @click="timeFilter = 'all'; showFilterDropdown = false">All Time</button>
                  <button @click="timeFilter = '2025'; showFilterDropdown = false">2025 Orders</button>
                  <button @click="timeFilter = '30days'; showFilterDropdown = false">Last 30 Days</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredOrders.length === 0" class="empty-orders-box">
            <div class="empty-icon-circle">
              <Package :size="32" class="empty-svg" />
            </div>
            <h3 class="empty-title">No orders found</h3>
            <p class="empty-desc">
              We couldn't find any orders matching your criteria. Try switching tabs or clearing your search.
            </p>
            <button class="btn-empty-reset" @click="currentTab = 'all'; searchQuery = ''">
              View All Orders
            </button>
          </div>

          <!-- Orders Cards List matching format/My Orders.png -->
          <div v-else class="orders-cards-stack">
            <article
              v-for="order in filteredOrders"
              :key="order.orderNumber"
              class="order-record-card"
            >
              <!-- Order Header Meta -->
              <div class="card-meta-col">
                <h3 class="card-order-id">Order #{{ order.orderNumber }}</h3>
                <span class="card-placed-date">Placed on {{ order.placedAt }}</span>
              </div>

              <!-- Thumbnail Preview Stack with +N more -->
              <div class="card-thumbs-stack">
                <div
                  v-for="(item, idx) in order.items.slice(0, 3)"
                  :key="idx"
                  class="item-thumb-box"
                  :title="item.name"
                >
                  <img :src="item.image_url" :alt="item.name" />
                </div>
                <div v-if="order.items.length > 3" class="thumb-extra-badge">
                  <span>+{{ order.items.length - 3 }}<br />more</span>
                </div>
              </div>

              <!-- Status with Colored Dot -->
              <div class="card-status-col">
                <div class="status-badge-inline">
                  <span class="status-dot" :class="order.statusType"></span>
                  <strong class="status-label-name">{{ order.status }}</strong>
                </div>
                <span class="status-detail-desc">{{ order.statusText }}</span>
                <div class="status-items-price-row">
                  <span>{{ order.items.length }} items</span>
                  <span class="price-sep">|</span>
                  <strong class="total-bold-price">${{ order.total.toFixed(2) }}</strong>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="card-actions-col">
                <div class="button-row">
                  <!-- If shipped, show Track Order + View Details -->
                  <template v-if="order.statusType === 'shipped'">
                    <router-link
                      :to="`/account/orders/${order.orderNumber}`"
                      class="btn-order-outline"
                    >
                      Track Order
                    </router-link>
                    <router-link
                      :to="`/account/orders/${order.orderNumber}`"
                      class="btn-order-outline"
                    >
                      View Details
                    </router-link>
                  </template>

                  <!-- If processing, show View Details + Cancel Order -->
                  <template v-else-if="order.statusType === 'processing'">
                    <router-link
                      :to="`/account/orders/${order.orderNumber}`"
                      class="btn-order-outline"
                    >
                      View Details
                    </router-link>
                    <button
                      type="button"
                      class="btn-order-outline danger"
                      @click="handleCancelOrder(order.orderNumber)"
                    >
                      Cancel Order
                    </button>
                  </template>

                  <!-- If delivered or cancelled, show View Details + Buy Again -->
                  <template v-else>
                    <router-link
                      :to="`/account/orders/${order.orderNumber}`"
                      class="btn-order-outline"
                    >
                      View Details
                    </router-link>
                    <button
                      type="button"
                      class="btn-order-solid"
                      @click="ordersStore.reorder(order.orderNumber)"
                    >
                      Buy Again
                    </button>
                  </template>
                </div>

                <!-- Secondary Helper Sub-Links -->
                <div class="sub-links-row">
                  <template v-if="order.statusType === 'delivered'">
                    <a
                      href="#"
                      class="order-sub-link"
                      @click.prevent="openReviewModal(order)"
                    >
                      Write a Review
                    </a>
                    <span class="sub-link-dot">•</span>
                    <router-link
                      :to="`/returns/request?order=${order.orderNumber}`"
                      class="order-sub-link"
                    >
                      Request Return
                    </router-link>
                  </template>
                  <router-link
                    v-else
                    to="/contact"
                    class="order-sub-link"
                  >
                    Need Help?
                  </router-link>
                </div>
              </div>
            </article>
          </div>

          <!-- Pagination Bar matching format/My Orders.png -->
          <div v-if="filteredOrders.length > 0" class="orders-pagination-bar">
            <button class="page-arrow-btn" :disabled="currentPage === 1" @click="currentPage--">
              <ChevronLeft :size="16" />
            </button>
            <button class="page-num-btn active">1</button>
            <button class="page-num-btn">2</button>
            <button class="page-num-btn">3</button>
            <span class="page-ellipsis">...</span>
            <button class="page-num-btn">5</button>
            <button class="page-arrow-btn" @click="currentPage++">
              <ChevronRight :size="16" />
            </button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrdersStore } from '@/stores/orders'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import AccountSidebar from '@/components/account/AccountSidebar.vue'
import {
  Package,
  Search,
  Filter,
  ChevronDown,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'

const ordersStore = useOrdersStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

onMounted(() => {
  ordersStore.fetchOrders(authStore.userEmail)
})

const currentTab = ref('all')
const searchQuery = ref('')
const timeFilter = ref('all')
const showFilterDropdown = ref(false)
const currentPage = ref(1)

const filteredOrders = computed(() => {
  let list = ordersStore.orders

  if (currentTab.value === 'processing') {
    list = ordersStore.processingOrders
  } else if (currentTab.value === 'shipped') {
    list = ordersStore.shippedOrders
  } else if (currentTab.value === 'delivered') {
    list = ordersStore.deliveredOrders
  } else if (currentTab.value === 'cancelled') {
    list = ordersStore.cancelledOrders
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter((o) =>
      o.orderNumber.toLowerCase().includes(q) ||
      o.placedAt.toLowerCase().includes(q) ||
      o.items.some((item) => item.name.toLowerCase().includes(q))
    )
  }

  return list
})

function handleCancelOrder(orderNumber) {
  if (confirm(`Are you sure you want to cancel Order #${orderNumber}?`)) {
    ordersStore.cancelOrder(orderNumber)
  }
}

function openReviewModal(order) {
  notificationStore.addToast(`Reviewing products from Order #${order.orderNumber}`, 'info')
}
</script>

<style scoped>
/* ==========================================================================
   MY ORDERS PAGE (Strictly matches format/My Orders.png)
   ========================================================================== */

.my-orders-page {
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

/* Panoramic Hero Banner */
.orders-hero-banner {
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
  object-position: center 30%;
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

/* ================= 2-COLUMN BODY ================= */
.orders-body-grid {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2rem;
  align-items: start;
}

.orders-main-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Nav Toolbar */
.orders-nav-toolbar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.02);
}

.order-status-tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 1px solid #F0EAE3;
  padding-bottom: 0.5rem;
  overflow-x: auto;
}

.order-tab-btn {
  background: none;
  border: none;
  padding: 0.5rem 0.85rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  position: relative;
  transition: color 0.2s ease;
  white-space: nowrap;
}

.order-tab-btn.active {
  color: #8E4A3E;
}

.order-tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  right: 0;
  height: 2.5px;
  background-color: #8E4A3E;
  border-radius: 2px 2px 0 0;
}

.orders-search-filter-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-input-wrap {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: #A8A29E;
}

.order-search-field {
  width: 100%;
  padding: 0.65rem 1rem 0.65rem 2.5rem;
  border: 1px solid #D6CECE;
  border-radius: 8px;
  font-size: 0.84rem;
  color: #1C1917;
  outline: none;
}

.order-search-field:focus {
  border-color: #8E4A3E;
}

.filter-dropdown-wrap {
  position: relative;
}

.btn-filter-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1rem;
  border: 1px solid #D6CECE;
  background: #FFFFFF;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
  cursor: pointer;
}

.filter-menu-popover {
  position: absolute;
  right: 0;
  top: calc(100% + 6px);
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(28, 25, 23, 0.1);
  display: flex;
  flex-direction: column;
  min-width: 150px;
  z-index: 20;
}

.filter-menu-popover button {
  padding: 8px 14px;
  text-align: left;
  background: none;
  border: none;
  font-size: 0.82rem;
  color: #57534E;
  cursor: pointer;
}

.filter-menu-popover button:hover {
  background: #FAF7F2;
  color: #8E4A3E;
}

/* Order Cards Stack */
.orders-cards-stack {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.order-record-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  display: grid;
  grid-template-columns: 180px 190px 1.2fr 230px;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
  transition: all 0.2s ease;
}

.order-record-card:hover {
  border-color: #D4BAA8;
  box-shadow: 0 6px 20px rgba(28, 25, 23, 0.06);
}

.card-meta-col {
  display: flex;
  flex-direction: column;
}

.card-order-id {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 4px;
}

.card-placed-date {
  font-size: 0.78rem;
  color: #78716C;
}

/* Thumbs Stack */
.card-thumbs-stack {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-thumb-box {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid #EFE6DD;
  background: #FAF7F2;
  overflow: hidden;
  flex-shrink: 0;
}

.item-thumb-box img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.thumb-extra-badge {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px dashed #D4BAA8;
  background: #FFF8F6;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.1;
}

/* Status Column */
.card-status-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-badge-inline {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}

.status-dot.delivered {
  background-color: #2E7D32;
}

.status-dot.shipped {
  background-color: #1565C0;
}

.status-dot.processing {
  background-color: #78716C;
}

.status-dot.cancelled {
  background-color: #C62828;
}

.status-label-name {
  font-size: 0.92rem;
  font-weight: 700;
  color: #1C1917;
}

.status-detail-desc {
  font-size: 0.8rem;
  color: #78716C;
}

.status-items-price-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.84rem;
  color: #57534E;
  margin-top: 2px;
}

.price-sep {
  color: #D6CECE;
}

.total-bold-price {
  font-size: 0.95rem;
  color: #1C1917;
}

/* Actions Column */
.card-actions-col {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.button-row {
  display: flex;
  gap: 8px;
}

.btn-order-outline {
  padding: 8px 16px;
  border: 1px solid #8E4A3E;
  background: #FFFFFF;
  color: #8E4A3E;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-order-outline:hover {
  background: #FDF2EE;
}

.btn-order-outline.danger {
  border-color: #C62828;
  color: #C62828;
}

.btn-order-outline.danger:hover {
  background: #FFEBEE;
}

.btn-order-solid {
  padding: 8px 18px;
  border: 1px solid #8E4A3E;
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-order-solid:hover {
  background: #76392F;
}

.sub-links-row {
  display: flex;
  gap: 12px;
}

.order-sub-link {
  font-size: 0.76rem;
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}

.order-sub-link:hover {
  color: #6C332A;
}

.sub-link-dot {
  color: #D6CECE;
  font-size: 0.75rem;
}

/* Empty Box */
.empty-orders-box {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 4rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #FAF7F2;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.empty-svg {
  color: #8E4A3E;
}

.empty-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.4rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.empty-desc {
  font-size: 0.88rem;
  color: #78716C;
  max-width: 420px;
  margin-bottom: 1.5rem;
}

.btn-empty-reset {
  padding: 8px 20px;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
}

/* Pagination Bar */
.orders-pagination-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-top: 1rem;
}

.page-arrow-btn,
.page-num-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid #EFE6DD;
  background: #FFFFFF;
  font-size: 0.82rem;
  font-weight: 600;
  color: #57534E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
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

.page-ellipsis {
  padding: 0 4px;
  color: #A8A29E;
}

/* Responsive */
@media (max-width: 1024px) {
  .orders-hero-banner {
    grid-template-columns: 1fr;
  }
  .hero-right-stage {
    min-height: 180px;
  }
  .orders-body-grid {
    grid-template-columns: 1fr;
  }
  .order-record-card {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .card-actions-col {
    align-items: flex-start;
  }
}
</style>
