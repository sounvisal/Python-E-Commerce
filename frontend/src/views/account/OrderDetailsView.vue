<template>
  <div class="order-details-page">
    <div class="container account-container">
      <!-- Breadcrumbs matching format/Order Details.png -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/" class="crumb-link">Home</router-link>
        <span class="crumb-sep">›</span>
        <router-link to="/account" class="crumb-link">My Account</router-link>
        <span class="crumb-sep">›</span>
        <router-link to="/account/orders" class="crumb-link">My Orders</router-link>
        <span class="crumb-sep">›</span>
        <span class="crumb-current">Order Details</span>
      </nav>

      <!-- 3-Column Layout: Account Sidebar + Main Details + Aside Summary -->
      <div class="order-details-grid">
        <!-- ========================================================= -->
        <!-- LEFT: ACCOUNT SIDEBAR                                     -->
        <!-- ========================================================= -->
        <aside class="sidebar-column">
          <AccountSidebar currentActive="orders" />
        </aside>

        <!-- ========================================================= -->
        <!-- CENTER: ORDER DETAILS MAIN STAGE                          -->
        <!-- ========================================================= -->
        <main class="order-main-content">
          <!-- Header Title & Order Number -->
          <div class="order-header-block">
            <h1 class="order-title">Order Details</h1>
            <div class="order-sub-meta">
              <h2 class="order-number-heading">Order #{{ order.orderNumber }}</h2>
              <span class="order-placed-timestamp">Placed on {{ order.placedAt }}</span>
            </div>

            <!-- Status Banner Pill matching format/Order Details.png -->
            <div class="order-status-banner" :class="order.statusType">
              <div class="status-banner-left">
                <div class="status-circle-icon">
                  <Check v-if="order.statusType === 'delivered'" :size="16" />
                  <Truck v-else-if="order.statusType === 'shipped'" :size="16" />
                  <Clock v-else :size="16" />
                </div>
                <div class="status-banner-text">
                  <strong class="status-banner-heading">{{ order.status }}</strong>
                  <span class="status-banner-sub">Your order was {{ order.statusText.toLowerCase() }}.</span>
                </div>
              </div>
              <button class="btn-track-order-action" @click="showTrackingModal = true">
                Track Order
              </button>
            </div>
          </div>

          <!-- Order Timeline Stepper matching format/Order Details.png -->
          <div class="order-card timeline-card">
            <h3 class="card-inner-title">Order Timeline</h3>

            <div class="timeline-stepper">
              <div
                v-for="(step, index) in order.timeline"
                :key="index"
                class="timeline-step"
                :class="{ completed: step.completed, active: !step.completed && index === activeStepIndex }"
              >
                <!-- Line before node -->
                <div v-if="index > 0" class="step-connector-line"></div>

                <!-- Check / Node Circle -->
                <div class="step-node-circle">
                  <Check v-if="step.completed" :size="14" class="node-check-svg" />
                  <span v-else class="node-empty-dot"></span>
                </div>

                <!-- Step Info -->
                <div class="step-info-labels">
                  <strong class="step-title-name">{{ step.step }}</strong>
                  <span class="step-date-str">{{ step.date }}</span>
                  <span v-if="step.time" class="step-time-str">{{ step.time }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Shipping Information & Delivery Method matching mockup -->
          <div class="order-card shipping-delivery-card">
            <div class="info-half-column">
              <h3 class="card-inner-title">Shipping Information</h3>
              <div class="address-display-row">
                <MapPin :size="18" class="info-icon" />
                <div class="address-text-col">
                  <strong class="address-recipient">{{ order.shippingAddress.name }}</strong>
                  <p class="address-line">{{ order.shippingAddress.address }}</p>
                  <p class="address-city-line">{{ order.shippingAddress.city }}</p>
                  <span class="address-contact-phone">{{ order.shippingAddress.phone }}</span>
                </div>
              </div>
            </div>

            <div class="info-half-column divider-left">
              <h3 class="card-inner-title">Delivery Method</h3>
              <div class="delivery-display-row">
                <Truck :size="18" class="info-icon" />
                <div class="delivery-text-col">
                  <strong class="delivery-method-name">{{ order.deliveryMethod }}</strong>
                  <span class="delivery-status-note">{{ order.statusText }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Items in This Order Table matching format/Order Details.png -->
          <div class="order-card items-table-card">
            <h3 class="card-inner-title">Items in This Order ({{ order.items.length }})</h3>

            <div class="order-items-table">
              <div class="table-head-row">
                <span class="th-col col-product">Product</span>
                <span class="th-col col-price">Price</span>
                <span class="th-col col-qty">Qty</span>
                <span class="th-col col-total">Total</span>
                <span class="th-col col-action">Action</span>
              </div>

              <div
                v-for="item in order.items"
                :key="item.id"
                class="table-body-row"
              >
                <!-- Product Thumb + Info -->
                <div class="td-col col-product">
                  <router-link :to="`/product/${item.slug}`" class="item-img-link">
                    <img
                      :src="item.image_url"
                      :alt="item.name"
                      class="item-table-img"
                      @error="$event.target.src = '/images/prod-essence.jpg'"
                    />
                  </router-link>
                  <div class="item-meta-text">
                    <router-link :to="`/product/${item.slug}`" class="item-name-link">
                      {{ item.name }}
                    </router-link>
                    <span class="item-volume-text">{{ item.volume }}</span>
                  </div>
                </div>

                <!-- Price -->
                <div class="td-col col-price">
                  <span class="cell-price">${{ item.price.toFixed(2) }}</span>
                </div>

                <!-- Quantity -->
                <div class="td-col col-qty">
                  <span class="cell-qty">{{ item.qty }}</span>
                </div>

                <!-- Total -->
                <div class="td-col col-total">
                  <strong class="cell-total">${{ item.total.toFixed(2) }}</strong>
                </div>

                <!-- Action Button -->
                <div class="td-col col-action">
                  <button
                    type="button"
                    class="btn-write-review"
                    @click="openReviewFor(item)"
                  >
                    Write a Review
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>

        <!-- ========================================================= -->
        <!-- RIGHT: SUMMARY, PAYMENT & QUICK ACTIONS                   -->
        <!-- ========================================================= -->
        <aside class="order-aside-column">
          <!-- Order Summary Card -->
          <div class="order-aside-card order-summary-card">
            <h3 class="aside-card-title">Order Summary</h3>

            <div class="summary-lines-list">
              <div class="summary-line">
                <span class="summary-label">Subtotal ({{ order.items.length }} items)</span>
                <span class="summary-value">${{ order.subtotal.toFixed(2) }}</span>
              </div>
              <div class="summary-line">
                <span class="summary-label">Shipping (Standard Delivery)</span>
                <span class="summary-value free-text">Free</span>
              </div>
              <div class="summary-line">
                <span class="summary-label">Estimated Tax</span>
                <span class="summary-value">$0.00</span>
              </div>
              <div class="summary-total-divider"></div>
              <div class="summary-line total-line">
                <strong class="total-label">Total <span class="currency-tag">(USD)</span></strong>
                <strong class="total-big-price">${{ order.total.toFixed(2) }}</strong>
              </div>
            </div>

            <!-- Reward Points Callout Badge matching mockup -->
            <div class="rewards-earned-callout">
              <Gift :size="18" class="gift-icon" />
              <div class="reward-points-text">
                <strong>You earned {{ order.rewardPointsEarned }} reward points!</strong>
                <span>Use your points for exclusive rewards.</span>
              </div>
            </div>
          </div>

          <!-- Payment Information Card -->
          <div class="order-aside-card payment-info-card">
            <h3 class="aside-card-title">Payment Information</h3>

            <div class="payment-info-content">
              <div class="aba-badge-square">
                <span>ABA</span>
              </div>
              <div class="payment-method-text">
                <strong class="pay-provider-title">{{ order.paymentMethod.provider }}</strong>
                <span class="pay-details-date">{{ order.paymentMethod.details }}</span>
              </div>
              <span class="pay-amount-val">${{ order.paymentMethod.amount.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Order Actions Quick Links matching format/Order Details.png -->
          <div class="order-aside-card order-actions-card">
            <h3 class="aside-card-title">Order Actions</h3>

            <div class="order-actions-menu">
              <button type="button" class="action-menu-row" @click="showTrackingModal = true">
                <Truck :size="16" class="action-icon" />
                <span>Track Order</span>
                <ArrowRight :size="14" class="arrow-icon" />
              </button>

              <button type="button" class="action-menu-row" @click="ordersStore.reorder(order.orderNumber)">
                <RotateCcw :size="16" class="action-icon" />
                <span>Buy Again</span>
                <ArrowRight :size="14" class="arrow-icon" />
              </button>

              <router-link :to="{ path: '/returns/request', query: { order: order.orderNumber } }" class="action-menu-row">
                <RefreshCw :size="16" class="action-icon" />
                <span>Return or Exchange</span>
                <ArrowRight :size="14" class="arrow-icon" />
              </router-link>

              <router-link to="/contact" class="action-menu-row">
                <Headphones :size="16" class="action-icon" />
                <span>Contact Support</span>
                <ArrowRight :size="14" class="arrow-icon" />
              </router-link>
            </div>
          </div>

          <!-- Thank You Promo Box matching format/Order Details.png -->
          <div class="order-aside-card promo-brand-box">
            <div class="promo-text-wrap">
              <h4 class="promo-heading">Thank you<br />for shopping with Luméa!</h4>
              <p class="promo-tagline">Good Skin Days Are Ahead.</p>
              <router-link to="/best-sellers" class="btn-shop-best-sellers">
                Shop Best Sellers
              </router-link>
            </div>
            <div class="promo-image-wrap">
              <img
                src="/images/banner-order-promo.jpg"
                alt="Luméa Beauty Gift Collection"
                class="promo-img"
              />
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOrdersStore } from '@/stores/orders'
import { useNotificationStore } from '@/stores/notification'
import AccountSidebar from '@/components/account/AccountSidebar.vue'
import {
  Check,
  Truck,
  Clock,
  MapPin,
  Gift,
  ArrowRight,
  RotateCcw,
  RefreshCw,
  Headphones
} from 'lucide-vue-next'

const route = useRoute()
const ordersStore = useOrdersStore()
const notificationStore = useNotificationStore()

const showTrackingModal = ref(false)

onMounted(async () => {
  if (route.params.orderNumber) {
    await ordersStore.fetchOrderByNumber(route.params.orderNumber)
  }
})

const order = computed(() => {
  const param = route.params.orderNumber || 'LM250616789'
  return ordersStore.getOrderById(param)
})

const activeStepIndex = computed(() => {
  const index = order.value.timeline.findIndex((s) => !s.completed)
  return index === -1 ? order.value.timeline.length - 1 : index
})

function openReviewFor(item) {
  notificationStore.addToast(`Review form opened for ${item.name}`, 'info')
}
</script>

<style scoped>
/* ==========================================================================
   ORDER DETAILS PAGE (Strictly matches format/Order Details.png)
   ========================================================================== */

.order-details-page {
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

/* 3-Column Grid Layout */
.order-details-grid {
  display: grid;
  grid-template-columns: 260px 1fr 340px;
  gap: 2rem;
  align-items: start;
}

/* ================= CENTER COLUMN ================= */
.order-main-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header Block */
.order-header-block {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #1C1917;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.order-sub-meta {
  display: flex;
  flex-direction: column;
}

.order-number-heading {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1C1917;
}

.order-placed-timestamp {
  font-size: 0.82rem;
  color: #78716C;
}

/* Status Banner */
.order-status-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
}

.order-status-banner.delivered {
  background-color: #EBF6EE;
  border: 1px solid #C6E7CD;
}

.order-status-banner.shipped {
  background-color: #E8F0FE;
  border: 1px solid #BED4FC;
}

.order-status-banner.processing {
  background-color: #F5F5F4;
  border: 1px solid #E7E5E4;
}

.order-status-banner.cancelled {
  background-color: #FDE8E8;
  border: 1px solid #F8B4B4;
}

.status-banner-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.status-circle-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #2E7D32;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.order-status-banner.shipped .status-circle-icon {
  background: #1565C0;
}

.order-status-banner.processing .status-circle-icon {
  background: #78716C;
}

.status-banner-text {
  display: flex;
  flex-direction: column;
}

.status-banner-heading {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.status-banner-sub {
  font-size: 0.82rem;
  color: #57534E;
}

.btn-track-order-action {
  padding: 8px 18px;
  background: #FFFFFF;
  border: 1px solid #8E4A3E;
  color: #8E4A3E;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-track-order-action:hover {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* Order Cards Common */
.order-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.card-inner-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 1.25rem;
}

/* Timeline Stepper */
.timeline-stepper {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
  padding: 0.5rem 0.5rem 0.25rem;
}

.timeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
  position: relative;
}

.step-node-circle {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #FAF7F2;
  border: 2px solid #D6CECE;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  transition: all 0.2s ease;
}

.timeline-step.completed .step-node-circle {
  background: #8E4A3E;
  border-color: #8E4A3E;
  color: #FFFFFF;
}

.node-check-svg {
  color: #FFFFFF;
}

.node-empty-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #A8A29E;
}

.step-connector-line {
  position: absolute;
  top: 13px;
  left: -50%;
  width: 100%;
  height: 2px;
  background-color: #EFE6DD;
  z-index: 1;
}

.timeline-step.completed .step-connector-line {
  background-color: #8E4A3E;
}

.step-info-labels {
  display: flex;
  flex-direction: column;
  margin-top: 0.75rem;
}

.step-title-name {
  font-size: 0.84rem;
  color: #1C1917;
  font-weight: 700;
}

.step-date-str {
  font-size: 0.74rem;
  color: #78716C;
}

.step-time-str {
  font-size: 0.72rem;
  color: #A8A29E;
}

/* Shipping & Delivery 2-Column Card */
.shipping-delivery-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.info-half-column {
  display: flex;
  flex-direction: column;
}

.divider-left {
  border-left: 1px solid #EFE6DD;
  padding-left: 2rem;
}

.address-display-row,
.delivery-display-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.info-icon {
  color: #8E4A3E;
  margin-top: 2px;
  flex-shrink: 0;
}

.address-text-col,
.delivery-text-col {
  display: flex;
  flex-direction: column;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.45;
}

.address-recipient,
.delivery-method-name {
  color: #1C1917;
  font-size: 0.88rem;
}

.address-contact-phone,
.delivery-status-note {
  margin-top: 4px;
  color: #78716C;
}

/* Items Table */
.order-items-table {
  display: flex;
  flex-direction: column;
}

.table-head-row {
  display: grid;
  grid-template-columns: 2fr 100px 60px 100px 130px;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #EFE6DD;
  font-size: 0.78rem;
  font-weight: 600;
  color: #78716C;
}

.table-body-row {
  display: grid;
  grid-template-columns: 2fr 100px 60px 100px 130px;
  align-items: center;
  padding: 1.15rem 0;
  border-bottom: 1px solid #F5EFEB;
}

.table-body-row:last-child {
  border-bottom: none;
}

.td-col.col-product {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.item-img-link {
  width: 52px;
  height: 52px;
  border-radius: 8px;
  border: 1px solid #EFE6DD;
  background: #FAF7F2;
  overflow: hidden;
  flex-shrink: 0;
}

.item-table-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.item-meta-text {
  display: flex;
  flex-direction: column;
}

.item-name-link {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
}

.item-name-link:hover {
  color: #8E4A3E;
}

.item-volume-text {
  font-size: 0.76rem;
  color: #78716C;
}

.cell-price,
.cell-qty {
  font-size: 0.88rem;
  color: #57534E;
}

.cell-total {
  font-size: 0.92rem;
  font-weight: 700;
  color: #1C1917;
}

.btn-write-review {
  padding: 6px 14px;
  border: 1px solid #8E4A3E;
  background: #FFFFFF;
  color: #8E4A3E;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-write-review:hover {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* ================= RIGHT ASIDE ================= */
.order-aside-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-aside-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.aside-card-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 1.15rem;
}

/* Summary Lines */
.summary-lines-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.84rem;
  color: #57534E;
}

.free-text {
  color: #2E7D32;
  font-weight: 600;
}

.summary-total-divider {
  height: 1px;
  background-color: #EFE6DD;
  margin: 0.5rem 0;
}

.summary-line.total-line {
  font-size: 1.05rem;
  color: #1C1917;
}

.currency-tag {
  font-size: 0.78rem;
  color: #78716C;
  font-weight: normal;
}

.total-big-price {
  font-size: 1.25rem;
  color: #8E4A3E;
}

/* Reward Points Earned Callout */
.rewards-earned-callout {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #FFF5F2;
  border: 1px solid #F6D7D0;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  margin-top: 1.25rem;
}

.gift-icon {
  color: #8E4A3E;
  flex-shrink: 0;
}

.reward-points-text {
  display: flex;
  flex-direction: column;
  font-size: 0.78rem;
  color: #57534E;
}

.reward-points-text strong {
  color: #8E4A3E;
}

/* Payment Info Content */
.payment-info-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.aba-badge-square {
  width: 38px;
  height: 38px;
  border-radius: 6px;
  background: #005D8E;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.payment-method-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.pay-provider-title {
  font-size: 0.86rem;
  color: #1C1917;
}

.pay-details-date {
  font-size: 0.74rem;
  color: #78716C;
}

.pay-amount-val {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

/* Order Actions Menu */
.order-actions-menu {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.action-menu-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.5rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #57534E;
  font-size: 0.84rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.18s ease;
  width: 100%;
  text-align: left;
}

.action-icon {
  color: #8E4A3E;
}

.arrow-icon {
  margin-left: auto;
  color: #A8A29E;
  transition: transform 0.18s ease;
}

.action-menu-row:hover {
  background: #FAF7F2;
  color: #8E4A3E;
}

.action-menu-row:hover .arrow-icon {
  transform: translateX(3px);
  color: #8E4A3E;
}

/* Promo Brand Box */
.promo-brand-box {
  background: #FFF8F6;
  border-color: #F0D5CD;
  overflow: hidden;
  padding: 0;
}

.promo-text-wrap {
  padding: 1.5rem 1.5rem 1rem;
}

.promo-heading {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.25;
  margin-bottom: 0.25rem;
}

.promo-tagline {
  font-size: 0.8rem;
  color: #1C1917;
  font-weight: 500;
  margin-bottom: 1rem;
}

.btn-shop-best-sellers {
  display: inline-block;
  padding: 7px 16px;
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-shop-best-sellers:hover {
  background: #76392F;
}

.promo-image-wrap {
  width: 100%;
  height: 140px;
  overflow: hidden;
}

.promo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Responsive */
@media (max-width: 1200px) {
  .order-details-grid {
    grid-template-columns: 240px 1fr;
  }
  .order-aside-column {
    grid-column: span 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .promo-brand-box {
    grid-column: span 2;
  }
}

@media (max-width: 900px) {
  .order-details-grid {
    grid-template-columns: 1fr;
  }
  .shipping-delivery-card {
    grid-template-columns: 1fr;
  }
  .divider-left {
    border-left: none;
    padding-left: 0;
    border-top: 1px solid #EFE6DD;
    padding-top: 1.5rem;
  }
  .table-head-row,
  .table-body-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>
