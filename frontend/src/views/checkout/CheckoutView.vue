<template>
  <div class="checkout-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <router-link to="/cart">Shopping Bag</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Checkout</span>
      </nav>

      <!-- Refined Editorial Header -->
      <header class="checkout-editorial-header">
        <div class="header-titles">
          <span class="atelier-tag">LUMÉA ATELIER · ORDER CHECKOUT</span>
          <h1 class="checkout-title">Review & Dispatch</h1>
          <p class="checkout-subtitle">Authentic dermatological formulations dispatched directly across Cambodia.</p>
        </div>

        <div class="checkout-progress-pills">
          <div class="progress-pill done">
            <span class="pill-dot">✓</span>
            <span>1. Bag</span>
          </div>
          <span class="pill-sep">→</span>
          <div class="progress-pill active">
            <span class="pill-dot">2</span>
            <span>2. Delivery & Payment</span>
          </div>
          <span class="pill-sep">→</span>
          <div class="progress-pill">
            <span class="pill-dot">3</span>
            <span>3. Order Complete</span>
          </div>
        </div>
      </header>

      <div v-if="cartStore.items.length === 0" class="empty-checkout">
        <p>You have no items in your shopping bag.</p>
        <router-link to="/shop" class="btn btn-primary">Return to Catalog</router-link>
      </div>

      <form v-else @submit.prevent="handleSubmitOrder" class="checkout-grid">
        <!-- Customer Details & Shipping Form -->
        <div class="checkout-form-section">
          <!-- 1. Contact Info Card -->
          <div class="form-card atelier-card">
            <div class="card-title-row">
              <div class="step-num-badge">01</div>
              <div class="card-title-meta">
                <h3 class="card-title">Client Information</h3>
                <span class="card-subtitle">Your contact details for order confirmation & courier handover</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="cName">
                  Full Name <span class="req">*</span>
                </label>
                <div class="input-with-icon">
                  <User :size="16" class="input-icon" />
                  <input
                    type="text"
                    id="cName"
                    v-model="form.customer_name"
                    required
                    placeholder="e.g. Sreynich Chan"
                    class="form-input"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="cPhone">
                  Phone Number (Courier Contact) <span class="req">*</span>
                </label>
                <div class="input-with-icon">
                  <Phone :size="16" class="input-icon" />
                  <input
                    type="tel"
                    id="cPhone"
                    v-model="form.customer_phone"
                    required
                    placeholder="012 345 678 / +855 12 345 678"
                    class="form-input"
                  />
                </div>
                <span class="field-hint">Used by VET, J&T, or Grab driver to call before arrival</span>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label" for="cEmail">
                Email Address <span class="req">*</span>
              </label>
              <div class="input-with-icon">
                <Mail :size="16" class="input-icon" />
                <input
                  type="email"
                  id="cEmail"
                  v-model="form.customer_email"
                  required
                  placeholder="sreynich.chan@example.com"
                  class="form-input"
                />
              </div>
              <span class="field-hint">Your itemized digital invoice & tracking link will be sent here</span>
            </div>
          </div>

          <!-- 2. Delivery Address & Cambodia Courier Card (Postal code completely removed!) -->
          <div class="form-card atelier-card">
            <div class="card-title-row">
              <div class="step-num-badge">02</div>
              <div class="card-title-meta">
                <h3 class="card-title">Delivery & Courier Dispatch</h3>
                <span class="card-subtitle">Select your province, address, preferred Cambodian courier, and pin location</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label" for="sCity">
                  Province / City <span class="req">*</span>
                </label>
                <div class="select-wrapper">
                  <select
                    id="sCity"
                    v-model="form.shipping_city"
                    required
                    class="form-select"
                  >
                    <option value="Phnom Penh">Phnom Penh (Capital)</option>
                    <option value="Siem Reap">Siem Reap</option>
                    <option value="Battambang">Battambang</option>
                    <option value="Sihanoukville">Sihanoukville (Preah Sihanouk)</option>
                    <option value="Kampot">Kampot</option>
                    <option value="Kandal">Kandal</option>
                    <option value="Banteay Meanchey">Banteay Meanchey</option>
                    <option value="Kampong Cham">Kampong Cham</option>
                    <option value="Kampong Chhnang">Kampong Chhnang</option>
                    <option value="Kampong Speu">Kampong Speu</option>
                    <option value="Kampong Thom">Kampong Thom</option>
                    <option value="Kep">Kep</option>
                    <option value="Koh Kong">Koh Kong</option>
                    <option value="Kratie">Kratie</option>
                    <option value="Mondulkiri">Mondulkiri</option>
                    <option value="Oddar Meanchey">Oddar Meanchey</option>
                    <option value="Pailin">Pailin</option>
                    <option value="Preah Vihear">Preah Vihear</option>
                    <option value="Prey Veng">Prey Veng</option>
                    <option value="Pursat">Pursat</option>
                    <option value="Ratanakiri">Ratanakiri</option>
                    <option value="Stung Treng">Stung Treng</option>
                    <option value="Svay Rieng">Svay Rieng</option>
                    <option value="Takeo">Takeo</option>
                    <option value="Tboung Khmum">Tboung Khmum</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label" for="sAddress">
                  Street Address, Sangkat & Khan <span class="req">*</span>
                </label>
                <div class="input-with-icon">
                  <MapPin :size="16" class="input-icon" />
                  <input
                    type="text"
                    id="sAddress"
                    v-model="form.shipping_address"
                    required
                    placeholder="e.g. #12A, Street 240, Sangkat Chaktomuk, Khan Daun Penh"
                    class="form-input"
                  />
                </div>
              </div>
            </div>

            <!-- Cambodia Delivery Carrier Selection -->
            <DeliveryCarrierSelector
              v-model="form.shipping_carrier"
              :subtotal="cartStore.subtotal"
              :free-shipping-threshold="cartStore.freeShippingThreshold"
              @change="handleCarrierChange"
            />

            <!-- Interactive GPS Map Location Picker -->
            <LocationMapPicker
              :initial-lat="form.delivery_lat"
              :initial-lng="form.delivery_lng"
              :initial-notes="form.delivery_notes"
              @update:location="handleLocationUpdate"
            />
          </div>

          <!-- 3. Payment Selection -->
          <div class="form-card atelier-card">
            <div class="card-title-row">
              <div class="step-num-badge">03</div>
              <div class="card-title-meta">
                <h3 class="card-title">Payment Selection</h3>
                <span class="card-subtitle">Choose instant bank QR clearance or cash on doorstep delivery</span>
              </div>
            </div>

            <div class="payment-options-grid">
              <!-- 1. Bakong KHQR Option -->
              <label
                class="payment-option-card khqr-card-option"
                :class="{ selected: form.payment_method === 'khqr' }"
              >
                <div class="option-radio-wrap">
                  <input
                    type="radio"
                    v-model="form.payment_method"
                    value="khqr"
                    name="payMethod"
                  />
                </div>
                <div class="option-content">
                  <div class="option-header-row">
                    <div class="khqr-emblem-badge">
                      <span class="emblem-kh">KH</span>
                      <span class="emblem-qr">QR</span>
                    </div>
                    <div class="option-title-group">
                      <strong class="option-title">Bakong KHQR · ABA Mobile</strong>
                      <span class="instant-pill">⚡ Instant Clearance</span>
                    </div>
                  </div>
                  <p class="option-desc">Scan with ABA Mobile, Bakong, Wing, ACLEDA, Sathapana, or any Cambodian banking app.</p>
                  <div class="option-banks-preview">
                    <span class="bank-pill">ABA'Mobile</span>
                    <span class="bank-pill">Bakong</span>
                    <span class="bank-pill">Wing</span>
                    <span class="bank-pill">ACLEDA</span>
                    <span class="bank-pill">+ All Banks</span>
                  </div>
                </div>
              </label>

              <!-- 2. Cash on Delivery -->
              <label
                class="payment-option-card cod-card-option"
                :class="{ selected: form.payment_method === 'cod' }"
              >
                <div class="option-radio-wrap">
                  <input
                    type="radio"
                    v-model="form.payment_method"
                    value="cod"
                    name="payMethod"
                  />
                </div>
                <div class="option-content">
                  <div class="option-header-row">
                    <div class="cod-emblem-badge">
                      <Truck :size="18" />
                    </div>
                    <div class="option-title-group">
                      <strong class="option-title">Cash on Delivery (COD)</strong>
                      <span class="cod-pill">Doorstep Handover</span>
                    </div>
                  </div>
                  <p class="option-desc">Pay in cash (USD $ or KHR ៛) directly to the delivery driver upon receiving your package.</p>
                  <div class="option-banks-preview">
                    <span class="bank-pill">💵 USD Cash</span>
                    <span class="bank-pill">៛ Khmer Riel</span>
                    <span class="bank-pill">Zero Surcharge</span>
                  </div>
                </div>
              </label>
            </div>

            <!-- Dynamic Teaser Note -->
            <div v-if="form.payment_method === 'khqr'" class="payment-teaser-box">
              <div class="teaser-icon">
                <QrCode :size="24" />
              </div>
              <div class="teaser-text">
                <strong>Dynamic NBC-Certified Bakong QR</strong>
                <p>An official KHQR code with your order amount will be generated when you place this order. Includes real-time ABA bank clearance and evaluation demo mode.</p>
              </div>
            </div>

            <div v-else-if="form.payment_method === 'cod'" class="payment-teaser-box cod-teaser">
              <div class="teaser-icon">
                <CheckCircle2 :size="24" />
              </div>
              <div class="teaser-text">
                <strong>No Advance Payment Required</strong>
                <p>Your order will be packaged at our atelier and dispatched immediately via {{ selectedCarrierName }}. Please prepare the exact cash amount ($ or ៛) for the courier.</p>
              </div>
            </div>
          </div>

          <!-- 4. Final Review & Confirm Order Action Card -->
          <div class="form-card checkout-final-action-card">
            <div class="action-card-header">
              <div class="action-total-group">
                <span class="action-total-lbl">Total Payable (with Delivery)</span>
                <div class="action-total-price-row">
                  <span class="action-total-val">${{ cartStore.grandTotal.toFixed(2) }}</span>
                  <span class="action-total-khr">≈ {{ khrEquivalent }} KHR</span>
                </div>
              </div>
              <div class="action-payment-preview">
                <span class="preview-badge" :class="form.payment_method">
                  <span v-if="form.payment_method === 'khqr'">🇰HM Bakong KHQR · ABA Mobile</span>
                  <span v-else-if="form.payment_method === 'cod'">💵 Cash on Delivery</span>
                  <span v-else>💳 Card</span>
                </span>
                <span class="carrier-preview">via {{ selectedCarrierName }}</span>
              </div>
            </div>

            <!-- Error Banner in main form -->
            <div v-if="submitError" class="error-banner">
              {{ submitError }}
            </div>

            <button
              id="btn-confirm-checkout-main"
              type="submit"
              class="btn-finish-checkout"
              :disabled="submitting"
            >
              <span v-if="!submitting" class="finish-btn-content">
                <span class="finish-btn-text">{{ submitButtonText }}</span>
                <ArrowRight :size="18" class="finish-btn-arrow" />
              </span>
              <span v-else class="finish-btn-loading">
                <span class="spinner-inline"></span>
                Processing order with Luméa atelier…
              </span>
            </button>

            <div class="checkout-guarantees">
              <div class="guarantee-pill">
                <ShieldCheck :size="14" />
                <span>100% Genuine Formulations</span>
              </div>
              <div class="guarantee-pill">
                <Truck :size="14" />
                <span>Cambodian Doorstep Courier</span>
              </div>
              <div class="guarantee-pill">
                <Lock :size="14" />
                <span>Bank-Grade Encryption</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary Side Panel (Sticky on Desktop) -->
        <aside class="order-summary-panel">
          <div class="summary-card atelier-summary-card">
            <div class="summary-header">
              <h3 class="summary-title">Order Overview</h3>
              <span class="summary-badge">{{ cartStore.items.length }} {{ cartStore.items.length === 1 ? 'item' : 'items' }}</span>
            </div>

            <!-- Item Mini List -->
            <div class="summary-items">
              <div v-for="item in cartStore.items" :key="item.id" class="summary-item">
                <div class="mini-img-wrap">
                  <img
                    :src="item.image_url"
                    :alt="item.name"
                    class="mini-img"
                    @error="$event.target.src = '/images/prod-essence.jpg'"
                  />
                  <span class="mini-qty-badge">{{ item.quantity }}</span>
                </div>
                <div class="mini-info">
                  <span class="mini-title">{{ item.name }}</span>
                  <span class="mini-subtext">${{ item.price.toFixed(2) }} each</span>
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
                <span>Delivery ({{ selectedCarrierName }})</span>
                <span :class="{ 'free-shipping-tag': cartStore.shippingFee === 0 }">
                  {{ cartStore.shippingFee === 0 ? 'FREE' : `$${cartStore.shippingFee.toFixed(2)}` }}
                </span>
              </div>
              <div class="b-row grand-total">
                <div class="grand-label-col">
                  <span>Grand Total</span>
                  <span class="khr-hint">≈ {{ khrEquivalent }} KHR</span>
                </div>
                <span class="grand-num">${{ cartStore.grandTotal.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Error Banner in sidebar -->
            <div v-if="submitError" class="error-banner">
              {{ submitError }}
            </div>

            <button
              id="btn-authorize-order"
              type="submit"
              class="btn btn-primary btn-lg btn-block btn-summary-submit"
              :disabled="submitting"
            >
              <span v-if="!submitting">{{ submitButtonText }}</span>
              <span v-else>Processing with Atelier...</span>
            </button>

            <p class="terms-note">
              Transactions are protected by 256-bit encryption. Handcrafted delivery by certified Cambodian logistics.
            </p>
          </div>
        </aside>
      </form>
    </div>

    <!-- Authentic Bakong KHQR Modal -->
    <KHQRModal
      v-if="showKHQRModal && pendingKhqrOrder"
      :order-number="pendingKhqrOrder.order_number"
      :amount="pendingKhqrOrder.total"
      :expires-at="pendingKhqrOrder.expires_at"
      merchant-name="LUMÉA ATELIER"
      @approved="handleKHQRApproved"
      @cancelled="handleKHQRCancelled"
    />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useCartStore } from '@/stores/cart'
import { useOrdersStore } from '@/stores/orders'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import { User, Phone, Mail, MapPin, Truck, QrCode, ShieldCheck, Lock, ArrowRight, CheckCircle2, CreditCard } from 'lucide-vue-next'
import { rememberOrderAccess } from '@/utils/orderAccess'
import KHQRModal from '@/components/checkout/KHQRModal.vue'
import DeliveryCarrierSelector from '@/components/checkout/DeliveryCarrierSelector.vue'
import LocationMapPicker from '@/components/checkout/LocationMapPicker.vue'

const router = useRouter()
const cartStore = useCartStore()
const ordersStore = useOrdersStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const hostedCheckout = import.meta.env.VITE_HOSTED_DEPLOYMENT === 'true'

onMounted(() => {
  cartStore.fetchSettings()
  if (authStore.user) {
    if (authStore.user.name) form.customer_name = authStore.user.name
    if (authStore.user.email) form.customer_email = authStore.user.email
    if (authStore.user.phone) form.customer_phone = authStore.user.phone
    const addr = authStore.defaultAddress
    if (addr) {
      if (addr.street) form.shipping_address = addr.street
      if (addr.city) form.shipping_city = addr.city
      if (addr.postalCode) form.shipping_postal_code = addr.postalCode
    }
  }
})

const submitting = ref(false)
const submitError = ref(null)
const showKHQRModal = ref(false)
const pendingKhqrOrder = ref(null)
const checkoutKey = ref(sessionStorage.getItem('lumea_checkout_key') || crypto.randomUUID())
sessionStorage.setItem('lumea_checkout_key', checkoutKey.value)

const form = reactive({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  shipping_address: '',
  shipping_city: 'Phnom Penh',
  shipping_postal_code: '12000',
  shipping_carrier: 'vet_express',
  delivery_lat: 11.5564,
  delivery_lng: 104.9282,
  delivery_notes: '',
  payment_method: 'khqr',
  card_number: '4242 4242 4242 4242',
  card_expiry: '12/28',
  card_cvc: '888',
})

function handleCarrierChange({ carrier, fee }) {
  cartStore.setCarrier(carrier.id)
}

function handleLocationUpdate({ lat, lng, notes, auto_address, auto_city }) {
  form.delivery_lat = lat
  form.delivery_lng = lng
  form.delivery_notes = notes
  if (auto_address) {
    form.shipping_address = auto_address
  }
  if (auto_city) {
    form.shipping_city = auto_city
  }
}

const selectedCarrierName = computed(() => {
  const map = {
    vet_express: 'VET Logistics',
    jt_express: 'J&T Express',
    grab_express: 'GrabExpress',
    lumea_concierge: 'Luméa Concierge'
  }
  return map[form.shipping_carrier] || 'Domestic Courier'
})

const khrEquivalent = computed(() => {
  return Math.round(cartStore.grandTotal * 4100).toLocaleString('en-US')
})

const submitButtonText = computed(() => {
  const total = cartStore.grandTotal.toFixed(2)
  if (form.payment_method === 'khqr') {
    return `Place Order & Pay with KHQR · $${total}`
  }
  if (form.payment_method === 'cod') {
    return `Confirm Order (Cash on Delivery) · $${total}`
  }
  return `Complete Card Order · $${total}`
})

const handleSubmitOrder = async () => {
  if (cartStore.items.length === 0 || submitting.value || showKHQRModal.value) return
  const signature = JSON.stringify({ form, items: cartStore.items, code: cartStore.discountCode })
  if (sessionStorage.getItem('lumea_checkout_signature') !== signature) {
    checkoutKey.value = crypto.randomUUID()
    sessionStorage.setItem('lumea_checkout_key', checkoutKey.value)
    sessionStorage.setItem('lumea_checkout_signature', signature)
  }

  submitting.value = true
  submitError.value = null

  const payload = {
    checkout_key: checkoutKey.value,
    customer_name: form.customer_name,
    customer_email: form.customer_email,
    customer_phone: form.customer_phone,
    shipping_address: form.shipping_address,
    shipping_city: form.shipping_city,
    shipping_postal_code: form.shipping_postal_code,
    shipping_carrier: form.shipping_carrier,
    delivery_lat: form.delivery_lat,
    delivery_lng: form.delivery_lng,
    delivery_notes: form.delivery_notes,
    payment_method: form.payment_method,
    discount_code: cartStore.discountCode || null,
    expected_total: cartStore.grandTotal,
    items: cartStore.items.map((item) => ({
      product_id: item.id,
      quantity: item.quantity,
    })),
  }

  try {
    const { data } = await axios.post('/api/orders/quote', payload)
    const quote = data.data
    if (Math.abs(quote.total - cartStore.grandTotal) > 0.009) {
      cartStore.items = quote.items.map(line => ({ ...cartStore.items.find(i => i.id === line.product_id), price: line.price }))
      cartStore.discountRate = quote.subtotal ? quote.discount / quote.subtotal : 0
      cartStore.saveToStorage()
      await cartStore.fetchSettings()
      submitError.value = 'Your bag prices or delivery fee changed. Please review the updated total and submit again.'
      submitting.value = false
      return
    }
  } catch (err) {
    submitError.value = err.response?.data?.detail || 'Unable to verify your bag. Please try again.'
    submitting.value = false
    return
  }
  // Specialized flow for Bakong KHQR
  if (form.payment_method === 'khqr') {
    try {
      const response = await axios.post('/api/orders', payload)
      if (response.data && response.data.data) {
        rememberOrderAccess(response.data.data)
        pendingKhqrOrder.value = response.data.data
        showKHQRModal.value = true
      }
    } catch (err) {
      console.error('Failed to initiate KHQR order:', err)
      submitError.value =
        err.response?.data?.detail?.message || err.response?.data?.detail || 'Failed to generate order for Bakong KHQR. Please check server status.'
    } finally {
      submitting.value = false
    }
    return
  }

  // Standard flow for other methods
  try {
    const response = await axios.post('/api/orders', payload)
    if (response.data && response.data.data) {
      const order = response.data.data
      rememberOrderAccess(order)
      sessionStorage.removeItem('lumea_checkout_signature')
      ordersStore.addOrder(order)
      cartStore.clearCart()
      notificationStore.addToast('Order successfully confirmed!', 'success')
      router.push(`/order-success/${order.order_number}`)
    }
  } catch (err) {
    console.error('Failed to submit order:', err)
    submitError.value =
      err.response?.data?.detail?.message || err.response?.data?.detail || 'Failed to place order. Please verify that the Luméa atelier backend is running.'
  } finally {
    submitting.value = false
  }
}

const handleKHQRApproved = (data) => {
  if (pendingKhqrOrder.value) {
    sessionStorage.removeItem('lumea_checkout_signature')
    ordersStore.addOrder(pendingKhqrOrder.value)
    cartStore.clearCart()
    notificationStore.addToast('Bakong KHQR payment cleared & verified!', 'success')
    router.push(`/order-success/${pendingKhqrOrder.value.order_number}`)
  }
  showKHQRModal.value = false
}

const handleKHQRCancelled = (result) => {
  sessionStorage.removeItem('lumea_checkout_signature')
  showKHQRModal.value = false
  notificationStore.addToast(result?.requiresReview ? 'Payment needs review. Do not pay again; contact support with your order reference.' : 'KHQR checkout cancelled. You may change payment options.', 'info')
}
</script>

<style scoped>
.checkout-page {
  padding: 1rem 0 5rem;
  background: #FCFAF8;
  min-height: 100vh;
}

/* Breadcrumbs */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #78716C;
  margin-bottom: 1.25rem;
}

.breadcrumb-nav a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-nav a:hover {
  color: #7A2E22;
}

.bc-sep {
  color: #D6D3D1;
}

.bc-current {
  color: #7A2E22;
  font-weight: 600;
}

/* Refined Editorial Header */
.checkout-editorial-header {
  background: linear-gradient(135deg, #FAF7F2 0%, #F5EFEB 100%);
  border-radius: 20px;
  border: 1px solid rgba(122, 46, 34, 0.12);
  box-shadow: 0 4px 20px rgba(122, 46, 34, 0.03);
  padding: 2rem 2.5rem;
  margin-bottom: 2.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.atelier-tag {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #7A2E22;
  margin-bottom: 0.35rem;
}

.checkout-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.25rem;
  font-weight: 700;
  color: #1F2937;
  line-height: 1.15;
  margin: 0 0 0.4rem;
}

.checkout-subtitle {
  font-size: 0.95rem;
  color: #57534E;
  margin: 0;
  max-width: 520px;
  line-height: 1.5;
}

.checkout-progress-pills {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #FFFFFF;
  padding: 0.65rem 1.15rem;
  border-radius: 999px;
  border: 1px solid rgba(122, 46, 34, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.progress-pill {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #A8A29E;
}

.progress-pill.done {
  color: #15803D;
}

.progress-pill.active {
  color: #7A2E22;
}

.pill-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #F5EFEB;
  color: #78716C;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-pill.active .pill-dot {
  background: #7A2E22;
  color: #FFFFFF;
}

.progress-pill.done .pill-dot {
  background: #DCFCE7;
  color: #15803D;
}

.pill-sep {
  color: #D6D3D1;
  font-size: 0.85rem;
}

/* Empty Checkout */
.empty-checkout {
  padding: 4rem 2rem;
  text-align: center;
  background: #FFFFFF;
  border-radius: 20px;
  border: 1px solid #EFEAE3;
}

/* Main Grid */
.checkout-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2.75rem;
  align-items: start;
}

/* Atelier Cards */
.atelier-card {
  background: #FFFFFF;
  border-radius: 20px;
  border: 1.5px solid rgba(234, 229, 223, 0.85);
  padding: 2.25rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(28, 25, 23, 0.025);
  transition: all 0.25s ease;
}

.atelier-card:hover {
  border-color: rgba(122, 46, 34, 0.2);
  box-shadow: 0 8px 24px rgba(122, 46, 34, 0.04);
}

.card-title-row {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  margin-bottom: 1.75rem;
  padding-bottom: 1.15rem;
  border-bottom: 1px solid #F5EFEB;
}

.step-num-badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FAF7F2;
  border: 1.5px solid #7A2E22;
  color: #7A2E22;
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 0.95rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.35rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
  line-height: 1.2;
}

.card-subtitle {
  font-size: 0.82rem;
  color: #78716C;
  margin-top: 0.25rem;
  display: block;
}

/* Form Groups & Inputs */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}

.form-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.45rem;
}

.req {
  color: #B91C1C;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #9CA3AF;
  pointer-events: none;
  transition: color 0.2s ease;
}

.form-input {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  border: 1.5px solid #E5DFD7;
  background: #FFFFFF;
  padding: 0 1rem 0 2.75rem;
  font-size: 0.92rem;
  color: #1F2937;
  transition: all 0.2s ease;
}

.form-input:focus {
  border-color: #7A2E22;
  box-shadow: 0 0 0 3px rgba(122, 46, 34, 0.12);
  outline: none;
}

.input-with-icon:focus-within .input-icon {
  color: #7A2E22;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  border: 1.5px solid #E5DFD7;
  background: #FFFFFF;
  padding: 0 1rem;
  font-size: 0.92rem;
  color: #1F2937;
  cursor: pointer;
  transition: all 0.2s ease;
}

.form-select:focus {
  border-color: #7A2E22;
  box-shadow: 0 0 0 3px rgba(122, 46, 34, 0.12);
  outline: none;
}

.field-hint {
  font-size: 0.74rem;
  color: #78716C;
  margin-top: 0.35rem;
}

/* Payment Options Grid */
.payment-options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.payment-option-card {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  padding: 1.35rem;
  border: 1.5px solid #E5DFD7;
  border-radius: 16px;
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.25s ease;
}

.payment-option-card:hover {
  border-color: #7A2E22;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(122, 46, 34, 0.06);
}

.payment-option-card.selected {
  border-color: #7A2E22;
  background: #FAF7F2;
  box-shadow: 0 0 0 1px #7A2E22, 0 6px 20px rgba(122, 46, 34, 0.08);
}

.khqr-card-option.selected {
  border-color: #E1251B;
  background: #FFF9F9;
  box-shadow: 0 0 0 1px #E1251B, 0 6px 20px rgba(225, 37, 27, 0.08);
}

.option-radio-wrap {
  padding-top: 2px;
}

.option-radio-wrap input[type="radio"] {
  accent-color: #7A2E22;
  width: 17px;
  height: 17px;
  cursor: pointer;
}

.khqr-card-option input[type="radio"] {
  accent-color: #E1251B;
}

.option-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.option-header-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.khqr-emblem-badge {
  display: flex;
  align-items: center;
  background: #E1251B;
  color: #FFFFFF;
  padding: 3px 6px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 0.75rem;
  line-height: 1;
}

.emblem-qr {
  background: #FFFFFF;
  color: #E1251B;
  padding: 1px 3px;
  border-radius: 3px;
  margin-left: 2px;
}

.cod-emblem-badge {
  background: #FAF7F2;
  color: #7A2E22;
  padding: 6px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-title-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.option-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1F2937;
}

.instant-pill {
  font-size: 0.65rem;
  font-weight: 700;
  background: #E1251B;
  color: #FFFFFF;
  padding: 2px 7px;
  border-radius: 12px;
  text-transform: uppercase;
}

.cod-pill {
  font-size: 0.65rem;
  font-weight: 700;
  background: #F5EFEB;
  color: #7A2E22;
  padding: 2px 7px;
  border-radius: 12px;
  text-transform: uppercase;
}

.option-desc {
  font-size: 0.8rem;
  color: #57534E;
  line-height: 1.4;
  margin: 0;
}

.option-banks-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.35rem;
}

.bank-pill {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 6px;
  background: #F3F4F6;
  color: #4B5563;
}

/* Payment Teaser Box */
.payment-teaser-box {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: #FFF8F8;
  border: 1px solid rgba(225, 37, 27, 0.2);
  border-left: 4px solid #E1251B;
  padding: 1.15rem 1.35rem;
  border-radius: 14px;
}

.payment-teaser-box.cod-teaser {
  background: #FDFBF8;
  border: 1px solid rgba(122, 46, 34, 0.18);
  border-left: 4px solid #7A2E22;
}

.teaser-icon {
  color: #E1251B;
  flex-shrink: 0;
  padding-top: 2px;
}

.payment-teaser-box.cod-teaser .teaser-icon {
  color: #7A2E22;
}

.teaser-text strong {
  display: block;
  font-size: 0.88rem;
  color: #1F2937;
  margin-bottom: 0.25rem;
}

.teaser-text p {
  font-size: 0.8rem;
  color: #57534E;
  line-height: 1.45;
  margin: 0;
}

/* Final Action Card */
.checkout-final-action-card {
  background: linear-gradient(180deg, #FDFBF9 0%, #F5EFEB 100%);
  border: 1.5px solid rgba(122, 46, 34, 0.22);
  border-radius: 22px;
  padding: 2.25rem;
  box-shadow: 0 10px 32px rgba(122, 46, 34, 0.08);
  margin-top: 2rem;
}

.action-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding-bottom: 1.35rem;
  border-bottom: 1px solid rgba(122, 46, 34, 0.12);
  margin-bottom: 1.35rem;
}

.action-total-group {
  display: flex;
  flex-direction: column;
}

.action-total-lbl {
  font-size: 0.8rem;
  font-weight: 600;
  color: #78716C;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.action-total-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.action-total-val {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.3rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1;
}

.action-total-khr {
  font-size: 0.95rem;
  font-weight: 600;
  color: #78716C;
}

.action-payment-preview {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.35rem;
}

.preview-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.4rem 0.95rem;
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.15);
  font-size: 0.82rem;
  font-weight: 600;
  color: #1F2937;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.preview-badge.khqr {
  border-color: #E1251B;
  color: #B91C1C;
  background: #FFF5F5;
}

.carrier-preview {
  font-size: 0.78rem;
  color: #78716C;
  font-weight: 500;
}

.btn-finish-checkout {
  width: 100%;
  min-height: 58px;
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  border-radius: 14px;
  padding: 1.1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(122, 46, 34, 0.3);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-finish-checkout:hover:not(:disabled) {
  background: #622217;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(122, 46, 34, 0.38);
}

.btn-finish-checkout:active:not(:disabled) {
  transform: translateY(0);
}

.btn-finish-checkout:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.finish-btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.85rem;
  width: 100%;
}

.finish-btn-text {
  font-size: 1.08rem;
  font-weight: 600;
}

.finish-btn-arrow {
  transition: transform 0.2s ease;
}

.btn-finish-checkout:hover .finish-btn-arrow {
  transform: translateX(4px);
}

.finish-btn-loading {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.95rem;
}

.spinner-inline {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.checkout-guarantees {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1.35rem;
  margin-top: 1.35rem;
  padding-top: 1.15rem;
  border-top: 1px dashed rgba(122, 46, 34, 0.15);
}

.guarantee-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.78rem;
  color: #6B7280;
  font-weight: 500;
}

.guarantee-pill svg {
  color: #7A2E22;
}

/* Order Summary Panel (Sticky) */
.order-summary-panel {
  position: sticky;
  top: 90px;
}

.atelier-summary-card {
  background: #FFFFFF;
  border-radius: 20px;
  border: 1.5px solid rgba(234, 229, 223, 0.9);
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(28, 25, 23, 0.04);
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.35rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid #F5EFEB;
}

.summary-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.25rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

.summary-badge {
  font-size: 0.75rem;
  font-weight: 600;
  background: #FAF7F2;
  color: #7A2E22;
  padding: 3px 9px;
  border-radius: 12px;
  border: 1px solid rgba(122, 46, 34, 0.15);
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 260px;
  overflow-y: auto;
  padding-right: 0.25rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.mini-img-wrap {
  position: relative;
  width: 52px;
  height: 52px;
  flex-shrink: 0;
}

.mini-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  background: #F9F7F5;
  border: 1px solid #EFEAE3;
}

.mini-qty-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #7A2E22;
  color: #FFFFFF;
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.mini-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.mini-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.3;
}

.mini-subtext {
  font-size: 0.74rem;
  color: #78716C;
  margin-top: 2px;
}

.mini-price {
  font-weight: 700;
  font-size: 0.92rem;
  color: #1F2937;
}

.summary-divider {
  border: none;
  border-top: 1px solid #F5EFEB;
  margin: 1.35rem 0;
}

.breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.b-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  color: #57534E;
}

.discount-text {
  color: #15803D;
  font-weight: 600;
}

.free-shipping-tag {
  color: #15803D;
  font-weight: 700;
}

.grand-total {
  padding-top: 0.95rem;
  border-top: 1px solid #E8E2D9;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1F2937;
  align-items: baseline;
}

.grand-label-col {
  display: flex;
  flex-direction: column;
}

.khr-hint {
  font-size: 0.78rem;
  font-weight: 500;
  color: #78716C;
  margin-top: 2px;
}

.grand-num {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.45rem;
  font-weight: 700;
  color: #7A2E22;
}

.error-banner {
  background: #FEE2E2;
  color: #B91C1C;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  border-left: 3px solid #DC2626;
}

.btn-summary-submit {
  width: 100%;
  min-height: 50px;
  background: #7A2E22 !important;
  color: #FFFFFF !important;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.98rem;
  transition: all 0.25s ease;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(122, 46, 34, 0.22);
}

.btn-summary-submit:hover:not(:disabled) {
  background: #622217 !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(122, 46, 34, 0.3);
}

.terms-note {
  font-size: 0.74rem;
  color: #78716C;
  line-height: 1.45;
  margin-top: 1rem;
  text-align: center;
}

/* Responsive Media Queries */
@media (max-width: 960px) {
  .checkout-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .order-summary-panel {
    position: static;
  }
  .payment-options-grid {
    grid-template-columns: 1fr;
  }
  .checkout-editorial-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.5rem;
  }
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .atelier-card {
    padding: 1.5rem;
  }
  .action-card-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .action-payment-preview {
    align-items: flex-start;
  }
}
</style>
