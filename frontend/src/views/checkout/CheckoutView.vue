<template>
  <div class="checkout-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <router-link to="/cart">Cart</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Checkout</span>
      </nav>

      <!-- Panoramic Hero Banner matching format/Checkout_Information.png -->
      <section class="checkout-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">Checkout</h1>
          <p class="hero-desc">Almost there! Complete your order and start your journey to healthier, happier skin.</p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banners/banner-best-sellers-clean.jpg"
            alt="Luméa Checkout Care"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span class="script-row">Good</span>
            <span class="script-row">Skin Today.</span>
            <span class="script-row">Brighter</span>
            <span class="script-row">Tomorrows.</span>
            <div class="script-underline"></div>
          </div>
        </div>
      </section>

      <div v-if="cartStore.items.length === 0" class="empty-checkout">
        <p>You have no items in your shopping bag.</p>
        <router-link to="/shop" class="btn btn-primary">Return to Catalog</router-link>
      </div>

      <form v-else @submit.prevent="handleSubmitOrder" class="checkout-grid">
        <!-- Customer Details & Shipping Form -->
        <div class="checkout-form-section">
          <!-- Contact Info -->
          <div class="form-card">
            <h3>1. Contact Information</h3>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="cName">Full Name *</label>
                <input
                  type="text"
                  id="cName"
                  v-model="form.customer_name"
                  required
                  placeholder="e.g. Elena Rostova"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label class="form-label" for="cEmail">Email Address *</label>
                <input
                  type="email"
                  id="cEmail"
                  v-model="form.customer_email"
                  required
                  placeholder="elena@example.com"
                  class="form-input"
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="cPhone">Phone Number (For delivery updates)</label>
              <input
                type="tel"
                id="cPhone"
                v-model="form.customer_phone"
                placeholder="+1 (555) 019-2834"
                class="form-input"
              />
            </div>
          </div>

          <!-- Shipping Address -->
          <div class="form-card">
            <h3>2. White-Glove Delivery Address</h3>
            <div class="form-group">
              <label class="form-label" for="sAddress">Street Address *</label>
              <input
                type="text"
                id="sAddress"
                v-model="form.shipping_address"
                required
                placeholder="452 Architectural Boulevard, Apt 14B"
                class="form-input"
              />
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="sCity">City *</label>
                <input
                  type="text"
                  id="sCity"
                  v-model="form.shipping_city"
                  required
                  placeholder="Stockholm / New York"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label class="form-label" for="sZip">Postal / ZIP Code</label>
                <input
                  type="text"
                  id="sZip"
                  v-model="form.shipping_postal_code"
                  placeholder="10001"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Payment Simulation -->
          <div class="form-card">
            <h3>3. Payment Method</h3>
            <div class="payment-options">
              <label
                class="payment-option"
                :class="{ selected: form.payment_method === 'card' }"
              >
                <input
                  type="radio"
                  v-model="form.payment_method"
                  value="card"
                  name="payMethod"
                />
                <div class="pay-label">
                  <CreditCard :size="18" />
                  <span>Credit / Debit Card</span>
                </div>
              </label>

              <label
                class="payment-option"
                :class="{ selected: form.payment_method === 'apple_pay' }"
              >
                <input
                  type="radio"
                  v-model="form.payment_method"
                  value="apple_pay"
                  name="payMethod"
                />
                <div class="pay-label">
                  <Smartphone :size="18" />
                  <span>Apple Pay &middot; Instant Express</span>
                </div>
              </label>

              <label
                class="payment-option"
                :class="{ selected: form.payment_method === 'cod' }"
              >
                <input
                  type="radio"
                  v-model="form.payment_method"
                  value="cod"
                  name="payMethod"
                />
                <div class="pay-label">
                  <Truck :size="18" />
                  <span>Pay Upon White-Glove Inspection</span>
                </div>
              </label>
            </div>

            <div v-if="form.payment_method === 'card'" class="card-inputs">
              <div class="form-group">
                <label class="form-label" for="cardNum">Card Number</label>
                <input
                  id="cardNum"
                  type="text"
                  placeholder="4242 •••• •••• 4242"
                  class="form-input"
                  v-model="form.card_number"
                  maxlength="19"
                />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label" for="cardExp">Expiry</label>
                  <input
                    id="cardExp"
                    type="text"
                    placeholder="MM/YY"
                    class="form-input"
                    v-model="form.card_expiry"
                    maxlength="5"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label" for="cardCvc">CVC</label>
                  <input
                    id="cardCvc"
                    type="text"
                    placeholder="CVC"
                    class="form-input"
                    v-model="form.card_cvc"
                    maxlength="4"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary Side Panel -->
        <aside class="order-summary-panel">
          <div class="summary-card">
            <h3>Order Overview</h3>

            <!-- Item Mini List -->
            <div class="summary-items">
              <div v-for="item in cartStore.items" :key="item.id" class="summary-item">
                <img
                  :src="item.image_url"
                  :alt="item.name"
                  class="mini-img"
                  @error="$event.target.src = '/images/prod-essence.jpg'"
                />
                <div class="mini-info">
                  <span class="mini-title">{{ item.name }}</span>
                  <span class="mini-qty">Qty: {{ item.quantity }}</span>
                </div>
                <span class="mini-price">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                </span>
              </div>
            </div>

            <hr class="summary-divider" />

            <!-- Price Breakdown -->
            <div class="breakdown">
              <div class="b-row">
                <span>Subtotal</span>
                <span>${{ cartStore.subtotal.toFixed(2) }}</span>
              </div>
              <div v-if="cartStore.discountAmount > 0" class="b-row discount-text">
                <span>Promotional Discount</span>
                <span>-${{ cartStore.discountAmount.toFixed(2) }}</span>
              </div>
              <div class="b-row">
                <span>Shipping (White-Glove)</span>
                <span>{{ cartStore.shippingFee === 0 ? 'Complimentary' : `$${cartStore.shippingFee.toFixed(2)}` }}</span>
              </div>
              <div class="b-row grand-total">
                <span>Grand Total</span>
                <span class="grand-num">${{ cartStore.grandTotal.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Error Banner -->
            <div v-if="submitError" class="error-banner">
              {{ submitError }}
            </div>

            <button
              type="submit"
              class="btn btn-primary btn-lg btn-block"
              :disabled="submitting"
            >
              <span v-if="!submitting">Authorize Order &middot; ${{ cartStore.grandTotal.toFixed(2) }}</span>
              <span v-else>Processing with Atelier...</span>
            </button>

            <p class="terms-note">
              By authorizing this order, you agree to the LUMEA Terms of Concierge Service. All transactions are 256-bit encrypted.
            </p>
          </div>
        </aside>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useNotificationStore } from '@/stores/notification'
import { CreditCard, Smartphone, Truck } from 'lucide-vue-next'

const router = useRouter()
const cartStore = useCartStore()
const ordersStore = useOrdersStore()
const notificationStore = useNotificationStore()

onMounted(() => {
  cartStore.fetchSettings()
})

const submitting = ref(false)
const submitError = ref(null)

const form = reactive({
  customer_name: 'Elena Rostova',
  customer_email: 'elena.rostova@atelier-lumea.com',
  customer_phone: '+46 8 123 4567',
  shipping_address: 'Strandvägen 18, 4th Floor',
  shipping_city: 'Stockholm',
  shipping_postal_code: '114 56',
  payment_method: 'card',
  card_number: '4242 4242 4242 4242',
  card_expiry: '12/28',
  card_cvc: '888',
})

const handleSubmitOrder = async () => {
  if (cartStore.items.length === 0) return

  submitting.value = true
  submitError.value = null

  const payload = {
    customer_name: form.customer_name,
    customer_email: form.customer_email,
    customer_phone: form.customer_phone,
    shipping_address: form.shipping_address,
    shipping_city: form.shipping_city,
    shipping_postal_code: form.shipping_postal_code,
    payment_method: form.payment_method,
    discount_code: cartStore.discountCode || null,
    items: cartStore.items.map((item) => ({
      product_id: item.id,
      quantity: item.quantity,
    })),
  }

  try {
    const response = await axios.post('/api/orders', payload)
    if (response.data && response.data.data) {
      const order = response.data.data
      ordersStore.addOrder(order)
      cartStore.clearCart()
      notificationStore.addToast('Order successfully confirmed!', 'success')
      router.push(`/order-success/${order.order_number}`)
    }
  } catch (err) {
    console.error('Failed to submit order:', err)
    submitError.value =
      err.response?.data?.message || 'Failed to place order. Please verify that the Luméa atelier backend is running.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.checkout-page {
  padding: 1rem 0 4rem;
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

/* Panoramic Hero Banner matching format/Checkout_Information.png */
.checkout-hero-banner {
  background: linear-gradient(135deg, #FAF7F2 0%, #F5EFE7 50%, #ECE4DB 100%);
  border-radius: 18px;
  border: 1px solid rgba(234, 229, 223, 0.7);
  box-shadow: 0 4px 20px rgba(28, 25, 23, 0.03);
  display: grid;
  grid-template-columns: 1.15fr 1.1fr;
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
  padding: 1.75rem 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
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
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.15rem;
  line-height: 1.55;
  color: #44403C;
  max-width: 520px;
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

.empty-checkout {
  padding: 4rem 2rem;
  text-align: center;
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
}

.checkout-grid {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 3.5rem;
  align-items: start;
}

.form-card {
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  padding: 2rem;
  margin-bottom: 2rem;
}

.form-card h3 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.payment-option.selected {
  border-color: var(--text-primary);
  background: var(--bg-muted);
}

.pay-label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.card-inputs {
  padding: 1.25rem;
  background: var(--bg-muted);
  border-radius: var(--radius-md);
}

.summary-card {
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
}

.summary-card h3 {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 280px;
  overflow-y: auto;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.mini-img {
  width: 52px;
  height: 52px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  background: var(--bg-muted);
}

.mini-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.mini-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
}

.mini-qty {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.mini-price {
  font-weight: 600;
  font-size: 0.9rem;
}

.summary-divider {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: 1.5rem 0;
}

.breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.75rem;
}

.b-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  color: var(--text-secondary);
}

.discount-text {
  color: #10B981;
}

.grand-total {
  padding-top: 0.85rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
}

.grand-num {
  font-size: 1.35rem;
}

.error-banner {
  background: #FEE2E2;
  color: #B91C1C;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

.btn-block {
  width: 100%;
}

.terms-note {
  font-size: 0.75rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin-top: 1rem;
  text-align: center;
}

@media (max-width: 960px) {
  .checkout-grid {
    grid-template-columns: 1fr;
  }
}

.checkout-stepper-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.25rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 18px rgba(28, 25, 23, 0.03);
}

.step-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  cursor: pointer;
  user-select: none;
  transition: opacity 0.2s ease;
}

.step-circle {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #EFE9E2;
  color: #78716C;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}

.step-item.active .step-circle {
  background: #8E4A3E;
  color: #FFFFFF;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.3);
}

.step-item.completed .step-circle {
  background: #8E4A3E;
  color: #FFFFFF;
}

.step-label-group {
  display: flex;
  flex-direction: column;
}

.step-name {
  font-weight: 700;
  font-size: 0.92rem;
  color: #78716C;
  line-height: 1.2;
}

.step-item.active .step-name {
  color: #8E4A3E;
}

.step-item.completed .step-name {
  color: #111C38;
}

.step-sub {
  font-size: 0.74rem;
  color: #A8A29E;
  line-height: 1.2;
}

.step-line {
  flex: 1;
  height: 2px;
  background: #EFE9E2;
  margin: 0 1.25rem;
  border-radius: 2px;
  transition: background 0.3s ease;
}

.step-line.filled {
  background: #8E4A3E;
}

/* ================= STEP CONTENT CARDS ================= */
.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.card-hint {
  font-size: 0.85rem;
  color: #78716C;
}

.login-link, .edit-cart-link, .btn-link-edit {
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  font-size: 0.85rem;
}

.step-nav-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
}

/* Shipping Options */
.shipping-options-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.shipping-choice-card {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border: 1.5px solid #EFE6DD;
  border-radius: 12px;
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.2s ease;
}

.shipping-choice-card:hover {
  border-color: #D4A373;
}

.shipping-choice-card.selected {
  border-color: #8E4A3E;
  background: #FDF9F7;
}

.shipping-choice-card input[type="radio"] {
  margin-top: 0.25rem;
  accent-color: #8E4A3E;
}

.choice-content {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.choice-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.choice-title {
  font-weight: 600;
  font-size: 0.95rem;
  color: #111C38;
}

.choice-desc {
  font-size: 0.82rem;
  color: #78716C;
}

.choice-price {
  font-weight: 700;
  color: #8E4A3E;
  font-size: 0.95rem;
}

.review-brief-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #FAF7F2;
  border: 1px solid #EFE6DD;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-top: 1rem;
}

.brief-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #8E4A3E;
  display: block;
  margin-bottom: 0.2rem;
}

.brief-val {
  font-size: 0.88rem;
  color: #111C38;
}

/* Review details block */
.review-details-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-block {
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #EFE6DD;
}

.review-block:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.review-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.review-block-header h4 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111C38;
}

.review-val-name {
  font-weight: 600;
  font-size: 0.92rem;
  color: #111C38;
  margin-bottom: 0.2rem;
}

.review-val-sub {
  font-size: 0.86rem;
  color: #57534E;
  line-height: 1.4;
}

.reward-points-strip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #FDF9F7;
  border: 1px dashed #EADBCE;
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  font-size: 0.82rem;
  color: #8E4A3E;
  margin-bottom: 1rem;
}

.btn-place-order {
  padding: 0.9rem 2rem;
  font-size: 1.05rem;
}

@media (max-width: 960px) {
  .checkout-grid {
    grid-template-columns: 1fr;
  }
  .checkout-stepper-bar {
    flex-wrap: wrap;
    gap: 1rem;
  }
  .step-line {
    display: none;
  }
}
</style>
