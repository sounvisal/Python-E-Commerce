<template>
  <div class="checkout-page-wrapper">
    <div class="checkout-container">
      <!-- 1. Hero Header Banner matching mockup -->
      <section class="checkout-hero-banner">
        <div class="hero-left-content">
          <nav class="breadcrumb-trail" aria-label="Breadcrumb">
            <router-link to="/">Home</router-link>
            <span class="bc-arrow">›</span>
            <router-link to="/cart">Shopping Bag</router-link>
            <span class="bc-arrow">›</span>
            <span class="bc-active">Checkout</span>
          </nav>
          <h1 class="hero-heading">Checkout</h1>
          <p class="hero-subheading">Review your details, choose delivery & payment, and place your order.</p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/checkout-hero.png"
            alt="Your Atelier Checkout"
            class="hero-graphic"
          />
        </div>
      </section>

      <!-- 2. Stepper Progress Bar in pill container -->
      <div class="checkout-stepper-bar">
        <div class="stepper-item step-completed">
          <span class="stepper-bubble check">✓</span>
          <span class="stepper-name">Bag</span>
        </div>
        <div class="stepper-line line-active"></div>
        <div class="stepper-item step-active">
          <span class="stepper-bubble num">2</span>
          <span class="stepper-name">Delivery & Payment</span>
        </div>
        <div class="stepper-line"></div>
        <div class="stepper-item step-upcoming">
          <span class="stepper-bubble num">3</span>
          <span class="stepper-name">Review Order</span>
        </div>
      </div>

      <!-- Empty Cart State -->
      <div v-if="cartStore.items.length === 0" class="empty-bag-card">
        <p>Your shopping bag is currently empty.</p>
        <router-link to="/shop" class="btn-return-catalog">Return to Catalog</router-link>
      </div>

      <!-- Main Checkout Form Grid -->
      <form v-else @submit.prevent="handleSubmitOrder" class="checkout-main-grid">
        <!-- LEFT COLUMN: The 3 numbered cards -->
        <div class="checkout-cards-column">
          <!-- CARD 01: Contact Information -->
          <section class="atelier-card card-contact">
            <div class="card-header-row">
              <div class="sec-badge">01</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">Contact Information</h2>
                <p class="sec-subtitle">We'll use this to keep you updated about your order.</p>
              </div>
              <div v-if="!authStore.isAuthenticated" class="sec-login-hint">
                Already have an account? <router-link to="/login" class="link-login">Log in</router-link>
              </div>
            </div>

            <div class="form-grid-2">
              <div class="input-field-group">
                <label class="field-label" for="cName">
                  Full Name <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <User :size="16" class="field-icon" />
                  <input
                    type="text"
                    id="cName"
                    v-model="form.customer_name"
                    required
                    placeholder="e.g. Sreynich Chan"
                    class="form-text-input"
                  />
                </div>
              </div>

              <div class="input-field-group">
                <label class="field-label" for="cPhone">
                  Phone Number (Courier Contact) <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <Phone :size="16" class="field-icon" />
                  <input
                    type="tel"
                    id="cPhone"
                    v-model="form.customer_phone"
                    required
                    placeholder="+855 12 345 678"
                    class="form-text-input"
                  />
                </div>
              </div>
            </div>

            <div class="form-grid-2 form-grid-bottom">
              <div class="input-field-group">
                <label class="field-label" for="cEmail">
                  Email Address <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <Mail :size="16" class="field-icon" />
                  <input
                    type="email"
                    id="cEmail"
                    v-model="form.customer_email"
                    required
                    placeholder="sreynich.chan@example.com"
                    class="form-text-input"
                  />
                </div>
              </div>

              <div class="checkbox-field-group">
                <label class="marketing-checkbox-label">
                  <input
                    type="checkbox"
                    v-model="form.marketing_opt_in"
                    class="custom-check-input"
                  />
                  <span class="custom-check-box">
                    <Check v-if="form.marketing_opt_in" :size="12" class="check-icon-svg" />
                  </span>
                  <span class="checkbox-text">
                    Keep me updated on exclusive offers, new arrivals, and skincare tips.
                  </span>
                </label>
              </div>
            </div>
          </section>

          <!-- CARD 02: Delivery & Courier Dispatch -->
          <section class="atelier-card card-delivery">
            <div class="card-header-row">
              <div class="sec-badge">02</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">Delivery & Courier Dispatch</h2>
                <p class="sec-subtitle">Select your address, courier, and delivery option in Cambodia.</p>
              </div>
            </div>

            <!-- Subsection A: Shipping Address -->
            <div class="sub-section">
              <h3 class="sub-section-title">
                <MapPin :size="16" class="sub-icon" />
                Shipping Address
              </h3>

              <!-- Address Option 1: Default Address Card -->
              <div
                class="address-option-card"
                :class="{ selected: addressSelectionMode === 'default' }"
                @click="selectAddressMode('default')"
              >
                <div class="option-radio-dot" :class="{ active: addressSelectionMode === 'default' }"></div>
                <div class="address-content-wrap">
                  <div class="address-title-line">
                    <strong class="addr-name">Home</strong>
                    <span class="default-pill">(Default)</span>
                  </div>
                  <p class="address-body-text">
                    {{ defaultAddressText }}
                  </p>
                </div>
                <div class="address-actions-btns">
                  <button type="button" class="btn-action-sm" @click.stop="toggleEditDefaultAddress">
                    <Edit2 :size="13" />
                    <span>Edit</span>
                  </button>
                  <button type="button" class="btn-action-sm btn-delete-sm" @click.stop="clearAddressToNew">
                    <Trash2 :size="13" />
                    <span>Delete</span>
                  </button>
                </div>
              </div>

              <!-- Address Option 2: Add New Address Card -->
              <div
                class="address-option-card add-new-card"
                :class="{ selected: addressSelectionMode === 'new' }"
                @click="selectAddressMode('new')"
              >
                <div class="option-radio-dot" :class="{ active: addressSelectionMode === 'new' }"></div>
                <div class="address-content-wrap">
                  <strong class="addr-name">Add New Address</strong>
                  <p class="address-sub-text">Add a new delivery address</p>
                </div>
                <span class="addr-chevron">›</span>
              </div>

              <!-- Editable Address Fields (shown when editing or in 'new' mode) -->
              <div v-if="addressSelectionMode === 'new' || isEditingAddress" class="custom-address-fields">
                <div class="form-grid-2">
                  <div class="input-field-group">
                    <label class="field-label" for="sCity">
                      Province / City <span class="req-star">*</span>
                    </label>
                    <select id="sCity" v-model="form.shipping_city" required class="form-select-input">
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

                  <div class="input-field-group">
                    <label class="field-label" for="sAddress">
                      Street Address, Sangkat & Khan <span class="req-star">*</span>
                    </label>
                    <div class="input-icon-box">
                      <MapPin :size="16" class="field-icon" />
                      <input
                        type="text"
                        id="sAddress"
                        v-model="form.shipping_address"
                        required
                        placeholder="e.g. Phum Ta Nguon, Sangkat Kakab 1, Khan Pou Senchey"
                        class="form-text-input"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Subsection B: Delivery Location (Fine-tune) -->
            <div class="sub-section">
              <h3 class="sub-section-title">
                <MapPin :size="16" class="sub-icon" />
                Delivery Location (Fine-tune)
              </h3>
              <p class="sub-section-hint">Help our courier find you faster. Pin your exact location on the map.</p>

              <!-- Integrated GPS & Leaflet Map Picker -->
              <LocationMapPicker
                :initial-lat="form.delivery_lat"
                :initial-lng="form.delivery_lng"
                :initial-notes="form.delivery_notes"
                :compact="true"
                @update:location="handleLocationUpdate"
              />
            </div>

            <!-- Subsection C: Select Cambodia Courier -->
            <div class="sub-section courier-sub-section">
              <h3 class="sub-section-title">
                <Truck :size="16" class="sub-icon" />
                Select Cambodia Courier
              </h3>
              <p class="sub-section-hint">Direct delivery to all 25 provinces and Phnom Penh.</p>

              <div class="couriers-four-grid">
                <!-- 1. VET Logistics -->
                <div
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'vet_express' }"
                  @click="setCarrier('vet_express')"
                >
                  <div class="courier-top-row">
                    <span class="courier-tag tag-vet">NATIONWIDE #1</span>
                    <span class="courier-price">$1.50</span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'vet_express' }"></span>
                    <strong class="courier-name">Vireak Buntham (VET Logistics)</strong>
                  </div>
                  <p class="courier-desc">Cambodia's #1 nationwide courier service. Direct door-to-door delivery across all 25 provinces.</p>
                  <div class="courier-eta">⏱️ 1-2 Business Days</div>
                </div>

                <!-- 2. J&T Express Cambodia -->
                <div
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'jt_express' }"
                  @click="setCarrier('jt_express')"
                >
                  <div class="courier-top-row">
                    <span class="courier-tag tag-jt">FAST DOMESTIC</span>
                    <span class="courier-price">$1.75</span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'jt_express' }"></span>
                    <strong class="courier-name">J&T Express Cambodia</strong>
                  </div>
                  <p class="courier-desc">High-speed express courier with live automated GPS van dispatch and phone coordination.</p>
                  <div class="courier-eta">⏱️ Next-Day Delivery</div>
                </div>

                <!-- 3. GrabExpress On-Demand -->
                <div
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'grab_express' }"
                  @click="setCarrier('grab_express')"
                >
                  <div class="courier-top-row">
                    <span class="courier-tag tag-grab">INSTANT EXPRESS</span>
                    <span class="courier-price">$3.50</span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'grab_express' }"></span>
                    <strong class="courier-name">GrabExpress On-Demand</strong>
                  </div>
                  <p class="courier-desc">Direct instant motorbike dispatch for urgent beauty rituals within Phnom Penh city limits.</p>
                  <div class="courier-eta">⏱️ 60–90 Mins (Phnom Penh)</div>
                </div>

                <!-- 4. Luméa Atelier Concierge -->
                <div
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'lumea_concierge' }"
                  @click="setCarrier('lumea_concierge')"
                >
                  <div class="courier-top-row">
                    <span class="courier-tag tag-concierge">ATELIER SIGNATURE</span>
                    <span class="courier-price">$3.00</span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'lumea_concierge' }"></span>
                    <strong class="courier-name">Luméa Atelier Concierge</strong>
                  </div>
                  <p class="courier-desc">White-glove luxury delivery in signature silk-ribbon boxes with complimentary deluxe samples.</p>
                  <div class="courier-eta">⏱️ White-Glove Scheduled</div>
                </div>
              </div>
            </div>
          </section>

          <!-- CARD 03: Payment Selection -->
          <section class="atelier-card card-payment">
            <div class="card-header-row">
              <div class="sec-badge">03</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">Payment Selection</h2>
                <p class="sec-subtitle">Choose a secure and convenient payment method.</p>
              </div>
            </div>

            <div class="payment-two-grid">
              <!-- Method 1: Bakong KHQR - ABA Mobile -->
              <div
                class="payment-option-card"
                :class="{ selected: form.payment_method === 'khqr' }"
                @click="form.payment_method = 'khqr'"
              >
                <div class="payment-card-header">
                  <div class="payment-radio-wrap">
                    <span class="payment-radio-circle" :class="{ active: form.payment_method === 'khqr' }"></span>
                    <QrCode :size="18" class="khqr-symbol-icon" />
                    <strong class="payment-title">Bakong KHQR – ABA Mobile</strong>
                  </div>
                  <span class="payment-badge-tag tag-instant">⚡ INSTANT CLEARANCE</span>
                </div>

                <p class="payment-card-desc">
                  Scan with ABA Mobile, Bakong, Wing, ACLEDA, or any Cambodian banking app.
                </p>

                <div class="bank-pill-row">
                  <span class="bank-chip">ABA Mobile</span>
                  <span class="bank-chip">Bakong</span>
                  <span class="bank-chip">Wing</span>
                  <span class="bank-chip">ACLEDA</span>
                  <span class="bank-chip chip-more">+ All Banks</span>
                </div>
              </div>

              <!-- Method 2: Cash on Delivery (COD) -->
              <div
                class="payment-option-card"
                :class="{ selected: form.payment_method === 'cod' }"
                @click="form.payment_method = 'cod'"
              >
                <div class="payment-card-header">
                  <div class="payment-radio-wrap">
                    <span class="payment-radio-circle" :class="{ active: form.payment_method === 'cod' }"></span>
                    <span class="cod-box-icon">📦</span>
                    <strong class="payment-title">Cash on Delivery (COD)</strong>
                  </div>
                  <span class="payment-badge-tag tag-cod">DOORSTEP HANDOVER</span>
                </div>

                <p class="payment-card-desc">
                  Pay in cash (USD $ or KHR ៛) directly to the delivery driver upon receiving your package.
                </p>

                <div class="bank-pill-row">
                  <span class="bank-chip">💵 USD Cash</span>
                  <span class="bank-chip">💵 KHR Cash</span>
                  <span class="bank-chip">🛡️ Zero Surcharge</span>
                </div>
              </div>
            </div>
          </section>

          <!-- BOTTOM ACTION ROW: Back to Shopping Bag & Review Your Order Button -->
          <div class="checkout-footer-row">
            <router-link to="/cart" class="btn-back-to-bag">
              ← Back to Shopping Bag
            </router-link>

            <button
              type="submit"
              id="btn-authorize-order"
              class="btn-review-order-main"
              :disabled="submitting || cartStore.items.length === 0"
            >
              <span v-if="!submitting">Review Your Order →</span>
              <span v-else>Processing with Atelier…</span>
            </button>
          </div>

          <!-- Error Alert Banner -->
          <div v-if="submitError" class="checkout-error-alert" role="alert">
            {{ submitError }}
          </div>
        </div>

        <!-- RIGHT COLUMN: Order Summary, Promo Code, Shop with Confidence & Help -->
        <aside class="checkout-sidebar-column">
          <!-- 1. Order Summary Card -->
          <div class="sidebar-card summary-card">
            <div class="summary-header">
              <h3 class="summary-title">Order Summary ({{ cartStore.totalItems }} items)</h3>
              <router-link to="/cart" class="link-edit-cart">Edit Cart</router-link>
            </div>

            <!-- Itemized List -->
            <ul class="summary-items-list">
              <li v-for="item in cartStore.items" :key="item.id" class="summary-item-row">
                <img :src="item.image" :alt="item.name || item.title" class="item-thumb-img" />
                <div class="item-info-col">
                  <h4 class="item-title">{{ item.name || item.title }}</h4>
                  <div class="item-meta-line">
                    <span class="item-vol">{{ item.selectedVolume || 'Full Size' }}</span>
                    <span class="item-qty">Qty: {{ item.quantity }}</span>
                  </div>
                </div>
                <div class="item-price-col">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                </div>
              </li>
            </ul>

            <!-- Calculation Lines -->
            <div class="summary-breakdown">
              <div class="breakdown-row">
                <span class="bd-label">Subtotal</span>
                <span class="bd-val">${{ cartStore.subtotal.toFixed(2) }}</span>
              </div>
              <div class="breakdown-row">
                <span class="bd-label">
                  Shipping ({{ selectedCarrierName }})
                  <span class="info-circle" title="Calculated based on your selected courier service">ⓘ</span>
                </span>
                <span class="bd-val" :class="{ 'free-shipping-text': cartStore.shippingFee === 0 }">
                  {{ cartStore.shippingFee === 0 ? 'FREE' : `$${cartStore.shippingFee.toFixed(2)}` }}
                </span>
              </div>
              <div v-if="cartStore.discountAmount > 0" class="breakdown-row discount-row">
                <span class="bd-label">Promotion Discount</span>
                <span class="bd-val">-{{ Number(cartStore.discountRate * 100).toFixed(0) }}% (-${{ cartStore.discountAmount.toFixed(2) }})</span>
              </div>
              <div class="breakdown-row">
                <span class="bd-label">Estimated Tax</span>
                <span class="bd-val">$0.00</span>
              </div>

              <div class="breakdown-divider"></div>

              <div class="breakdown-row total-row">
                <span class="total-label">Total <span class="currency-tag">(USD)</span></span>
                <span class="total-price">${{ cartStore.grandTotal.toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- 2. Have a Promo Code? Card -->
          <div class="sidebar-card promo-card">
            <h4 class="promo-heading">🏷️ Have a Promo Code?</h4>
            <div class="promo-input-row">
              <input
                type="text"
                v-model="promoInput"
                placeholder="Enter promo code"
                class="promo-text-input"
                :disabled="isApplyingPromo"
                @keydown.enter.prevent="applyPromo"
              />
              <button
                type="button"
                class="btn-apply-promo"
                :disabled="isApplyingPromo || !promoInput.trim()"
                @click="applyPromo"
              >
                {{ isApplyingPromo ? '…' : 'Apply' }}
              </button>
            </div>
            <p v-if="promoFeedback" class="promo-feedback" :class="{ success: promoSuccess, error: !promoSuccess }">
              {{ promoFeedback }}
            </p>
          </div>

          <!-- 3. Shop with Confidence Card -->
          <div class="sidebar-card confidence-card">
            <h4 class="confidence-title">Shop with Confidence</h4>
            <div class="confidence-four-grid">
              <div class="confidence-col">
                <ShieldCheck :size="24" class="conf-icon" />
                <span class="conf-text">100% Authentic Products</span>
              </div>
              <div class="confidence-col">
                <Truck :size="24" class="conf-icon" />
                <span class="conf-text">Reliable Shipping</span>
              </div>
              <div class="confidence-col">
                <RotateCcw :size="24" class="conf-icon" />
                <span class="conf-text">Easy Returns & Exchanges</span>
              </div>
              <div class="confidence-col">
                <Leaf :size="24" class="conf-icon" />
                <span class="conf-text">Better Skin for Everyone</span>
              </div>
            </div>
          </div>

          <!-- 4. Need Help? Card -->
          <div class="sidebar-card help-card">
            <div class="help-content-row">
              <div class="help-headset-wrap">
                <Headphones :size="26" class="help-headset-icon" />
              </div>
              <div class="help-text-wrap">
                <strong class="help-title">Need Help?</strong>
                <p class="help-desc">Our customer support team is here for you.</p>
              </div>
            </div>
            <router-link to="/contact" class="btn-contact-support">
              💬 Contact Us
            </router-link>
          </div>
        </aside>
      </form>
    </div>

    <!-- Official KHQR Modal from checkout.html -->
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { rememberOrderAccess, orderRequest } from '@/utils/orderAccess'
import LocationMapPicker from '@/components/checkout/LocationMapPicker.vue'
import KHQRModal from '@/components/checkout/KHQRModal.vue'
import {
  User,
  Phone,
  Mail,
  MapPin,
  Truck,
  QrCode,
  ShieldCheck,
  Check,
  Edit2,
  Trash2,
  RotateCcw,
  Leaf,
  Headphones
} from 'lucide-vue-next'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

// Address Selection Mode
const addressSelectionMode = ref('default')
const defaultAddressText = ref('Phum Ta Nguon, Sangkat Kakab 1, Khan Pou Senchey, Phnom Penh, Cambodia')
const isEditingAddress = ref(false)

const form = reactive({
  customer_name: '',
  customer_phone: '',
  customer_email: '',
  shipping_address: 'Phum Ta Nguon, Sangkat Kakab 1, Khan Pou Senchey',
  shipping_city: 'Phnom Penh',
  shipping_carrier: 'vet_express',
  payment_method: 'khqr',
  delivery_lat: 11.5564,
  delivery_lng: 104.9282,
  delivery_notes: '',
  marketing_opt_in: true
})

const submitting = ref(false)
const submitError = ref('')
const showKHQRModal = ref(false)
const pendingKhqrOrder = ref(null)

// Promo code states
const promoInput = ref('')
const isApplyingPromo = ref(false)
const promoFeedback = ref('')
const promoSuccess = ref(false)

onMounted(async () => {
  await cartStore.fetchSettings()

  // Pre-fill from logged-in user profile
  if (authStore.user) {
    form.customer_name = authStore.user.name || authStore.user.full_name || ''
    form.customer_email = authStore.user.email || ''
    if (authStore.user.phone) form.customer_phone = authStore.user.phone
  } else {
    // Default demo placeholders matching mockup
    form.customer_name = 'Sreynich Chan'
    form.customer_email = 'sreynich.chan@example.com'
    form.customer_phone = '+855 12 345 678'
  }
})

function selectAddressMode(mode) {
  addressSelectionMode.value = mode
  if (mode === 'default') {
    form.shipping_address = 'Phum Ta Nguon, Sangkat Kakab 1, Khan Pou Senchey'
    form.shipping_city = 'Phnom Penh'
    isEditingAddress.value = false
  } else {
    isEditingAddress.value = true
  }
}

function toggleEditDefaultAddress() {
  isEditingAddress.value = !isEditingAddress.value
  addressSelectionMode.value = 'default'
}

function clearAddressToNew() {
  addressSelectionMode.value = 'new'
  form.shipping_address = ''
  isEditingAddress.value = true
}

function setCarrier(carrierId) {
  form.shipping_carrier = carrierId
  cartStore.setCarrier(carrierId)
}

function handleLocationUpdate({ lat, lng, notes, auto_address, auto_city }) {
  form.delivery_lat = lat
  form.delivery_lng = lng
  form.delivery_notes = notes
  if (auto_address) {
    form.shipping_address = auto_address
    defaultAddressText.value = `${auto_address}, ${auto_city || form.shipping_city}, Cambodia`
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

async function applyPromo() {
  const code = promoInput.value.trim()
  if (!code) return
  isApplyingPromo.value = true
  promoFeedback.value = ''
  try {
    const res = await cartStore.applyPromoCode(code)
    promoSuccess.value = res.success
    promoFeedback.value = res.message
    if (res.success) {
      promoInput.value = ''
    }
  } catch (err) {
    promoSuccess.value = false
    promoFeedback.value = 'Invalid promo code'
  } finally {
    isApplyingPromo.value = false
  }
}

async function handleSubmitOrder() {
  submitting.value = true
  submitError.value = ''

  if (!form.customer_name || !form.customer_email || !form.customer_phone || !form.shipping_address) {
    submitError.value = 'Please complete all required fields.'
    submitting.value = false
    return
  }

  // Verify server-side quote to ensure no discrepancy
  try {
    const quotePayload = {
      items: cartStore.items.map(item => ({
        product_id: item.id,
        quantity: item.quantity
      })),
      discount_code: cartStore.discountCode || undefined,
      carrier: form.shipping_carrier
    }
    const { data: quote } = await axios.post('/api/orders/quote', quotePayload)
    if (Math.abs(quote.total - cartStore.grandTotal) > 0.009) {
      cartStore.items = quote.items.map(line => ({
        ...cartStore.items.find(i => i.id === line.product_id),
        price: line.price
      }))
      cartStore.discountRate = quote.subtotal ? quote.discount / quote.subtotal : 0
      cartStore.saveToStorage()
      await cartStore.fetchSettings()
      submitError.value = 'Your bag prices or delivery fee changed. Please review the updated total and click Review Your Order again.'
      submitting.value = false
      return
    }
  } catch (err) {
    console.warn('Quote verification skipped or failed:', err)
  }

  // Flow for Bakong KHQR
  if (form.payment_method === 'khqr') {
    pendingKhqrOrder.value = {
      order_number: `LUM-${Date.now().toString(36).toUpperCase()}`,
      total: cartStore.grandTotal,
      expires_at: new Date(Date.now() + 5 * 60 * 1000).toISOString()
    }
    showKHQRModal.value = true
    submitting.value = false
    return
  }

  // Flow for Cash on Delivery (COD)
  await placeOrderFinal({ paymentMethod: 'cod', paymentStatus: 'Pending', reference: 'COD-DOORSTEP' })
}

async function handleKHQRApproved({ orderNumber }) {
  showKHQRModal.value = false
  await placeOrderFinal({
    paymentMethod: 'khqr',
    paymentStatus: 'Paid',
    reference: `BAKONG-${orderNumber}`,
    preassignedOrderNumber: orderNumber
  })
}

function handleKHQRCancelled() {
  showKHQRModal.value = false
  pendingKhqrOrder.value = null
  submitting.value = false
}

async function placeOrderFinal({ paymentMethod, paymentStatus, reference, preassignedOrderNumber }) {
  try {
    const payload = {
      customer_name: form.customer_name,
      customer_email: form.customer_email,
      customer_phone: form.customer_phone,
      shipping_address: form.shipping_address,
      shipping_city: form.shipping_city,
      shipping_postal_code: '',
      shipping_carrier: form.shipping_carrier,
      delivery_lat: form.delivery_lat,
      delivery_lng: form.delivery_lng,
      delivery_notes: form.delivery_notes,
      items: cartStore.items.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      discount_code: cartStore.discountCode || undefined,
      payment_method: paymentMethod,
      payment_status: paymentStatus,
      payment_reference: reference
    }

    if (preassignedOrderNumber) {
      payload.order_number = preassignedOrderNumber
    }

    const res = await axios.post('/api/orders', payload, orderRequest())
    const createdOrder = res.data.data

    if (createdOrder && createdOrder.order_number) {
      rememberOrderAccess(createdOrder)
    }

    cartStore.clearCart()
    router.push({
      name: 'order-success',
      params: { orderNumber: createdOrder.order_number }
    })
  } catch (err) {
    console.error('Order placement error:', err)
    submitError.value = err.response?.data?.detail || 'Failed to dispatch your order. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
/* Page Layout */
.checkout-page-wrapper {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 80px;
}

.checkout-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 24px 20px 0;
  box-sizing: border-box;
}

/* 1. Hero Header Banner matching mockup */
.checkout-hero-banner {
  background: #FAF7F2;
  border: 1px solid #EFEAE4;
  border-radius: 16px;
  padding: 28px 36px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
  position: relative;
  margin-bottom: 20px;
}

.hero-left-content {
  flex: 1;
}

.breadcrumb-trail {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #78716C;
  margin-bottom: 10px;
}

.breadcrumb-trail a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.15s;
}

.breadcrumb-trail a:hover {
  color: #7A2E22;
}

.bc-arrow {
  color: #A8A29E;
  font-size: 14px;
}

.bc-active {
  color: #7A2E22;
  font-weight: 700;
}

.hero-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 34px;
  font-weight: 700;
  color: #2A1B16;
  margin: 0 0 8px;
  line-height: 1.15;
}

.hero-subheading {
  font-size: 14px;
  color: #6B5E57;
  margin: 0;
}

.hero-right-stage {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.hero-graphic {
  height: 130px;
  max-width: 360px;
  object-fit: contain;
  display: block;
}

@media (max-width: 860px) {
  .checkout-hero-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
  }
  .hero-graphic {
    height: 100px;
    align-self: center;
  }
}

/* 2. Stepper Progress Bar */
.checkout-stepper-bar {
  background: #FFFFFF;
  border: 1px solid #EFEAE4;
  border-radius: 40px;
  padding: 12px 36px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

.stepper-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stepper-bubble {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.step-completed .stepper-bubble.check {
  background: #FDF4F2;
  border: 1.5px solid #F3D5CF;
  color: #7A2E22;
}

.step-completed .stepper-name {
  color: #292524;
  font-weight: 600;
  font-size: 14px;
}

.step-active .stepper-bubble.num {
  background: #7A2E22;
  color: #FFFFFF;
}

.step-active .stepper-name {
  color: #7A2E22;
  font-weight: 700;
  font-size: 14px;
}

.step-upcoming .stepper-bubble.num {
  background: #F3F4F6;
  color: #9CA3AF;
}

.step-upcoming .stepper-name {
  color: #9CA3AF;
  font-weight: 500;
  font-size: 14px;
}

.stepper-line {
  flex: 1;
  height: 1.5px;
  background: #E5E7EB;
  margin: 0 16px;
}

.stepper-line.line-active {
  background: #7A2E22;
}

@media (max-width: 640px) {
  .checkout-stepper-bar {
    padding: 10px 16px;
  }
  .stepper-name {
    display: none;
  }
}

/* Empty Bag */
.empty-bag-card {
  background: #fff;
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  border: 1px solid #E5E7EB;
}

.btn-return-catalog {
  display: inline-block;
  margin-top: 16px;
  background: #7A2E22;
  color: #fff;
  padding: 10px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}

/* Main Two-Column Grid */
.checkout-main-grid {
  display: grid;
  grid-template-columns: 1fr 390px;
  gap: 28px;
  align-items: start;
}

@media (max-width: 1024px) {
  .checkout-main-grid {
    grid-template-columns: 1fr;
  }
}

/* Left Column Cards */
.checkout-cards-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.atelier-card {
  background: #FFFFFF;
  border: 1px solid #EBE5DF;
  border-radius: 16px;
  padding: 24px 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* Card Header with 01, 02, 03 Badge */
.card-header-row {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
  position: relative;
}

.sec-badge {
  width: 32px;
  height: 32px;
  border: 1.5px solid #7A2E22;
  color: #7A2E22;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 2px;
}

.sec-title-wrap {
  flex: 1;
}

.sec-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 3px;
}

.sec-subtitle {
  font-size: 13px;
  color: #78716C;
  margin: 0;
}

.sec-login-hint {
  font-size: 13px;
  color: #57534E;
  white-space: nowrap;
}

.link-login {
  color: #7A2E22;
  text-decoration: underline;
  font-weight: 700;
}

/* Form Fields */
.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 640px) {
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}

.form-grid-bottom {
  margin-top: 14px;
  align-items: center;
}

.input-field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: #292524;
}

.req-star {
  color: #DC2626;
}

.input-icon-box {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 12px;
  color: #9CA3AF;
  pointer-events: none;
}

.form-text-input, .form-select-input {
  width: 100%;
  padding: 10px 14px 10px 36px;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 13.5px;
  color: #1C1917;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.form-text-input:focus, .form-select-input:focus {
  outline: none;
  border-color: #7A2E22;
  box-shadow: 0 0 0 3px rgba(122, 46, 34, 0.08);
}

.form-select-input {
  padding-left: 12px;
}

/* Marketing Checkbox */
.checkbox-field-group {
  margin-top: 18px;
}

.marketing-checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.custom-check-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.custom-check-box {
  width: 18px;
  height: 18px;
  border: 1.5px solid #7A2E22;
  border-radius: 4px;
  background: #7A2E22;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.15s;
}

.check-icon-svg {
  color: #FFFFFF;
}

.checkbox-text {
  font-size: 12.5px;
  line-height: 1.4;
  color: #44403C;
}

/* Card 02: Subsections */
.sub-section {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px solid #F3F0EC;
}

.sub-section-title {
  font-size: 14.5px;
  font-weight: 700;
  color: #1C1917;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 6px;
}

.sub-icon {
  color: #7A2E22;
}

.sub-section-hint {
  font-size: 12.5px;
  color: #78716C;
  margin: 0 0 12px;
}

/* Address Cards */
.address-option-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  border-radius: 10px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.address-option-card.selected {
  background: #FFF8F6;
  border-color: #F3D5CF;
}

.option-radio-dot {
  width: 18px;
  height: 18px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.option-radio-dot.active {
  border-color: #7A2E22;
}

.option-radio-dot.active::after {
  content: '';
  width: 10px;
  height: 10px;
  background: #7A2E22;
  border-radius: 50%;
}

.address-content-wrap {
  flex: 1;
}

.address-title-line {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}

.addr-name {
  font-size: 13.5px;
  color: #1C1917;
}

.default-pill {
  font-size: 11px;
  font-weight: 600;
  color: #78716C;
}

.address-body-text {
  font-size: 12.5px;
  color: #57534E;
  margin: 0;
  line-height: 1.4;
}

.address-sub-text {
  font-size: 12px;
  color: #78716C;
  margin: 0;
}

.address-actions-btns {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-action-sm {
  background: none;
  border: none;
  color: #78716C;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.15s, color 0.15s;
}

.btn-action-sm:hover {
  background: #F3F4F6;
  color: #1C1917;
}

.btn-delete-sm:hover {
  color: #DC2626;
}

.addr-chevron {
  font-size: 18px;
  color: #9CA3AF;
  font-weight: 700;
}

.custom-address-fields {
  margin-top: 12px;
  padding: 14px;
  background: #FAF8F5;
  border-radius: 8px;
  border: 1px solid #EAE5DF;
}

/* Couriers 4-Grid */
.couriers-four-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

@media (max-width: 900px) {
  .couriers-four-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .couriers-four-grid {
    grid-template-columns: 1fr;
  }
}

.courier-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
}

.courier-card.selected {
  border-color: #7A2E22;
  background: #FFF8F6;
  box-shadow: 0 0 0 1px #7A2E22;
}

.courier-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.courier-tag {
  font-size: 9.5px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.3px;
}

.tag-vet { background: #FEF3C7; color: #92400E; }
.tag-jt { background: #FFEDD5; color: #C2410C; }
.tag-grab { background: #DCFCE7; color: #15803D; }
.tag-concierge { background: #FEF9C3; color: #854D0E; }

.courier-price {
  font-size: 13.5px;
  font-weight: 800;
  color: #1C1917;
}

.courier-title-line {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.courier-radio-circle {
  width: 14px;
  height: 14px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.courier-radio-circle.active {
  border-color: #7A2E22;
}

.courier-radio-circle.active::after {
  content: '';
  width: 8px;
  height: 8px;
  background: #7A2E22;
  border-radius: 50%;
}

.courier-name {
  font-size: 12px;
  color: #1C1917;
  line-height: 1.25;
}

.courier-desc {
  font-size: 11px;
  color: #6B7280;
  line-height: 1.35;
  margin: 0 0 8px;
  flex: 1;
}

.courier-eta {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
  padding-top: 6px;
  border-top: 1px dashed #E5E7EB;
}

/* Card 03: Payment Methods 2-Grid */
.payment-two-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

@media (max-width: 700px) {
  .payment-two-grid {
    grid-template-columns: 1fr;
  }
}

.payment-option-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
}

.payment-option-card.selected {
  border-color: #7A2E22;
  background: #FFF8F6;
  box-shadow: 0 0 0 1px #7A2E22;
}

.payment-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.payment-radio-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.payment-radio-circle {
  width: 16px;
  height: 16px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.payment-radio-circle.active {
  border-color: #7A2E22;
}

.payment-radio-circle.active::after {
  content: '';
  width: 8px;
  height: 8px;
  background: #7A2E22;
  border-radius: 50%;
}

.khqr-symbol-icon {
  color: #DC2626;
}

.cod-box-icon {
  font-size: 16px;
}

.payment-title {
  font-size: 13.5px;
  color: #1C1917;
}

.payment-badge-tag {
  font-size: 9.5px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 10px;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.tag-instant {
  background: #DC2626;
  color: #FFFFFF;
}

.tag-cod {
  background: #F5EFEB;
  color: #7A2E22;
}

.payment-card-desc {
  font-size: 11.5px;
  color: #6B7280;
  margin: 0 0 12px;
  line-height: 1.4;
  flex: 1;
}

.bank-pill-row {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.bank-chip {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  font-size: 10px;
  font-weight: 600;
  color: #374151;
  padding: 3px 8px;
  border-radius: 4px;
}

.chip-more {
  background: #F3F4F6;
  color: #4B5563;
}

/* Bottom Action Row */
.checkout-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  gap: 16px;
}

.btn-back-to-bag {
  color: #1C1917;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.15s;
}

.btn-back-to-bag:hover {
  color: #7A2E22;
}

.btn-review-order-main {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 14px 38px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(122, 46, 34, 0.2);
}

.btn-review-order-main:hover:not(:disabled) {
  background: #632218;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(122, 46, 34, 0.3);
}

.btn-review-order-main:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.checkout-error-alert {
  padding: 12px 16px;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 8px;
  color: #B91C1C;
  font-size: 13px;
  margin-top: 10px;
}

/* RIGHT COLUMN: Sidebar Cards */
.checkout-sidebar-column {
  display: flex;
  flex-direction: column;
  gap: 18px;
  position: sticky;
  top: 90px;
}

.sidebar-card {
  background: #FFFFFF;
  border: 1px solid #EBE5DF;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* 1. Summary Card */
.summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F3F0EC;
}

.summary-title {
  font-size: 15px;
  font-weight: 700;
  color: #1C1917;
  margin: 0;
}

.link-edit-cart {
  font-size: 12.5px;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: underline;
}

.summary-items-list {
  list-style: none;
  padding: 0;
  margin: 0 0 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 240px;
  overflow-y: auto;
}

.summary-item-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-thumb-img {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  border: 1px solid #E5E7EB;
  object-fit: cover;
  flex-shrink: 0;
}

.item-info-col {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 12.5px;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta-line {
  display: flex;
  gap: 8px;
  font-size: 11px;
  color: #6B7280;
}

.item-price-col {
  font-size: 13.5px;
  font-weight: 700;
  color: #1C1917;
  white-space: nowrap;
}

.summary-breakdown {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #F3F0EC;
}

.breakdown-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #44403C;
}

.info-circle {
  font-size: 11px;
  color: #9CA3AF;
  cursor: help;
  margin-left: 2px;
}

.free-shipping-text {
  color: #16A34A;
  font-weight: 700;
}

.discount-row {
  color: #16A34A;
  font-weight: 600;
}

.breakdown-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 8px 0;
}

.total-row {
  font-size: 14px;
  font-weight: 700;
  color: #1C1917;
}

.currency-tag {
  font-size: 11px;
  font-weight: 500;
  color: #78716C;
}

.total-price {
  font-size: 24px;
  font-weight: 800;
  color: #B91C1C;
}

/* 2. Promo Card */
.promo-heading {
  font-size: 13.5px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 10px;
}

.promo-input-row {
  display: flex;
  gap: 8px;
}

.promo-text-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #D6D3D1;
  border-radius: 6px;
  font-size: 12.5px;
  color: #1C1917;
}

.promo-text-input:focus {
  outline: none;
  border-color: #7A2E22;
}

.btn-apply-promo {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
}

.btn-apply-promo:hover:not(:disabled) {
  opacity: 0.9;
}

.promo-feedback {
  margin: 8px 0 0;
  font-size: 11.5px;
}

.promo-feedback.success { color: #16A34A; font-weight: 600; }
.promo-feedback.error { color: #DC2626; }

/* 3. Shop with Confidence Card */
.confidence-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 17px;
  font-weight: 700;
  color: #7A2E22;
  text-align: center;
  margin: 0 0 16px;
}

.confidence-four-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  text-align: center;
}

.confidence-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.conf-icon {
  color: #7A2E22;
}

.conf-text {
  font-size: 10.5px;
  line-height: 1.25;
  color: #44403C;
  font-weight: 500;
}

/* 4. Need Help? Card */
.help-content-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.help-headset-wrap {
  width: 40px;
  height: 40px;
  border: 1.5px solid #F3D5CF;
  background: #FFF8F6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.help-headset-icon {
  color: #7A2E22;
}

.help-title {
  display: block;
  font-size: 13.5px;
  color: #1C1917;
}

.help-desc {
  font-size: 11.5px;
  color: #78716C;
  margin: 2px 0 0;
}

.btn-contact-support {
  display: block;
  width: 100%;
  text-align: center;
  padding: 8px 16px;
  border: 1.5px solid #7A2E22;
  border-radius: 8px;
  color: #7A2E22;
  background: #FFFFFF;
  text-decoration: none;
  font-size: 13px;
  font-weight: 700;
  box-sizing: border-box;
  transition: all 0.15s ease;
}

.btn-contact-support:hover {
  background: #FFF8F6;
}
</style>
