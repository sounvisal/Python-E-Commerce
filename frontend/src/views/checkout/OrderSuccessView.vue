<template>
  <div class="success-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <router-link to="/cart">Cart</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Order Success</span>
      </nav>

      <!-- Panoramic Hero Banner matching format/Order_Success.png -->
      <section class="success-hero-banner">
        <div class="hero-left-content">
          <div class="success-check-circle">
            <Check :size="28" />
          </div>
          <div class="hero-titles-wrap">
            <h1 class="hero-title">Thank You!</h1>
            <h2 class="hero-subtitle">Your order has been placed successfully.</h2>
            <p class="hero-desc">We’ve received your order and will prepare it soon.</p>
          </div>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banner-my-orders.jpg"
            alt="Luméa Care Package"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span class="script-row">Good</span>
            <span class="script-row">Skin Days</span>
            <span class="script-row">Are Ahead.</span>
            <div class="script-underline"></div>
          </div>
        </div>
      </section>

      <div v-if="loading" class="loading-box">
        <div class="skeleton" style="height: 350px; border-radius: 18px;"></div>
      </div>

      <div v-else-if="order" class="success-card">
        <div class="icon-wrap">
          <CheckCircle2 :size="48" class="check-icon" />
        </div>

        <span class="confirmed-badge">Order Confirmed</span>
        <h1>Thank you, {{ order.customer_name }}</h1>
        <p class="order-sub">
          Your order has been received by our atelier. A confirmation receipt and courier tracking details have been dispatched to <strong>{{ order.customer_email }}</strong>.
        </p>

        <div class="order-meta-box">
          <div class="meta-item">
            <span class="meta-title">Order Reference</span>
            <span class="meta-value highlight">{{ order.order_number }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-title">Payment Method</span>
            <span class="meta-value">{{ formatPaymentMethod(order.payment_method) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-title">Status</span>
            <span class="meta-value status-tag">{{ order.status }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-title">Estimated Delivery</span>
            <span class="meta-value">3 &ndash; 5 Business Days</span>
          </div>
        </div>

        <!-- Destination -->
        <div class="address-box">
          <h4>Delivery Destination</h4>
          <p>
            {{ order.shipping_address }}<br>
            {{ order.shipping_city }} {{ order.shipping_postal_code }}
          </p>
        </div>

        <!-- Items Recap -->
        <div class="items-recap" v-if="order.items && order.items.length > 0">
          <h4>Selected Works</h4>
          <div v-for="item in order.items" :key="item.id" class="recap-row">
            <div class="recap-left">
              <span class="recap-name">{{ item.product_name }}</span>
              <span class="recap-qty">Qty: {{ item.quantity }}</span>
            </div>
            <span class="recap-price">${{ Number(item.total).toFixed(2) }}</span>
          </div>
        </div>

        <div class="order-total-bar">
          <span>Total Authorized Amount</span>
          <span class="final-amount">${{ Number(order.total).toFixed(2) }}</span>
        </div>

        <div class="action-row">
          <router-link to="/shop" class="btn btn-primary btn-lg">
            Continue Exploring Collections
          </router-link>
          <router-link to="/" class="btn btn-outline btn-lg">
            Return to Atelier Home
          </router-link>
        </div>
      </div>

      <div v-else class="not-found-card">
        <h2>Order Not Found</h2>
        <p>We could not locate this order reference in our records.</p>
        <router-link to="/shop" class="btn btn-primary">Return to Shop</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { CheckCircle2, Check } from 'lucide-vue-next'

const route = useRoute()
const order = ref(null)
const loading = ref(true)

const formatPaymentMethod = (method) => {
  switch (method) {
    case 'apple_pay':
      return 'Apple Pay Express'
    case 'cod':
      return 'Pay on White-Glove Delivery'
    case 'card':
    default:
      return 'Credit Card'
  }
}

onMounted(async () => {
  const orderNumber = route.params.orderNumber
  if (orderNumber) {
    try {
      const res = await axios.get(`/api/orders/${orderNumber}`)
      if (res.data?.data) {
        order.value = res.data.data
      }
    } catch (err) {
      console.error('Failed to load order:', err)
    } finally {
      loading.value = false
    }
  }
})
</script>

<style scoped>
.success-page {
  padding: 1.5rem 0 4rem;
}

/* Breadcrumbs */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #78716C;
  margin-bottom: 0.85rem;
}

.breadcrumb-nav a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-nav a:hover {
  color: #8E4A3E;
}

.bc-sep {
  color: #A8A29E;
}

.bc-current {
  color: #8E4A3E;
  font-weight: 500;
}

/* Panoramic Hero Banner matching format/Order_Success.png */
.success-hero-banner {
  background: linear-gradient(135deg, #FAF7F2 0%, #F5EFE7 50%, #ECE4DB 100%);
  border-radius: 18px;
  border: 1px solid rgba(234, 229, 223, 0.7);
  box-shadow: 0 4px 20px rgba(28, 25, 23, 0.03);
  display: grid;
  grid-template-columns: 1.2fr 1.1fr;
  min-height: 275px;
  margin-bottom: 2.25rem;
  overflow: hidden;
  align-items: stretch;
  position: relative;
  animation: heroEntrance 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes heroEntrance {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-left-content {
  padding: 2rem 2.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.success-check-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #F8E6E2;
  color: #8E4A3E;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid #EADBCE;
}

.hero-titles-wrap {
  display: flex;
  flex-direction: column;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.12;
  letter-spacing: -0.01em;
  margin-bottom: 0.35rem;
}

.hero-subtitle {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.45rem;
  font-weight: 600;
  color: #111C38;
  line-height: 1.25;
  margin-bottom: 0.4rem;
}

.hero-desc {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.05rem;
  line-height: 1.5;
  color: #44403C;
}

.hero-right-stage {
  position: relative;
  width: 100%;
  min-height: 275px;
  overflow: hidden;
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
  width: 100px;
  background: linear-gradient(to right, #FAF7F2, transparent);
  pointer-events: none;
}

.banner-script-overlay {
  position: absolute;
  top: 2rem;
  right: 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  pointer-events: none;
}

.script-row {
  font-family: var(--font-script, 'Cormorant Garamond', Georgia, serif);
  font-style: italic;
  font-weight: 700;
  font-size: 1.7rem;
  line-height: 1.15;
  color: #8E4A3E;
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.85);
}

.script-underline {
  width: 42px;
  height: 2px;
  background: #8E4A3E;
  margin-top: 0.5rem;
}

.success-card {
  max-width: 720px;
  margin: 0 auto;
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  padding: 2rem 2.5rem;
  text-align: center;
  box-shadow: var(--shadow-md);
}

.icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.75rem;
}

.check-icon {
  color: #10B981;
}

.confirmed-badge {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent-gold);
  margin-bottom: 0.5rem;
}

.order-sub {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 1rem 0 2.5rem;
}

.order-meta-box {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  background: var(--bg-muted);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  text-align: left;
  margin-bottom: 2rem;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.meta-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.meta-value.highlight {
  color: var(--accent-gold);
}

.status-tag {
  text-transform: capitalize;
  color: #10B981;
}

.address-box {
  text-align: left;
  padding: 1.25rem 1.5rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: 2rem;
}

.address-box h4 {
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.address-box p {
  font-size: 0.9rem;
  line-height: 1.5;
}

.items-recap {
  text-align: left;
  margin-bottom: 2rem;
  border-top: 1px solid var(--border-subtle);
  padding-top: 1.5rem;
}

.items-recap h4 {
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.recap-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px dashed var(--border-subtle);
}

.recap-left {
  display: flex;
  flex-direction: column;
}

.recap-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.recap-qty {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.recap-price {
  font-weight: 600;
  font-size: 0.95rem;
}

.order-total-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 0;
  border-top: 2px solid var(--text-primary);
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 2.5rem;
}

.final-amount {
  font-size: 1.45rem;
  color: var(--accent-gold);
}

.action-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

@media (max-width: 650px) {
  .order-meta-box {
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
  }
  .success-card {
    padding: 2rem 1.5rem;
  }
}
</style>
