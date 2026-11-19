<template>
  <div class="cart-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Cart</span>
      </nav>

      <!-- Panoramic Hero Banner matching format/Cart.png -->
      <section class="cart-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">Your Cart</h1>
          <p class="hero-desc">One step closer to healthier, happier skin.</p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banner-my-orders.jpg"
            alt="Luméa Self Care"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span class="script-row">Self care</span>
            <span class="script-row">looks good</span>
            <span class="script-row">on you.</span>
            <div class="script-underline"></div>
          </div>
        </div>
      </section>

      <div v-if="cartStore.items.length === 0" class="empty-cart-view">
        <ShoppingBag :size="48" class="empty-icon" />
        <h2>Your bag is currently empty</h2>
        <p>Explore our atelier collections to discover dermatologically proven formulations for your skin.</p>
        <router-link to="/shop" class="btn btn-primary btn-lg">
          Explore Atelier Catalog
        </router-link>
      </div>

      <div v-else class="cart-layout">
        <!-- Cart Items Table -->
        <div class="cart-items-section">
          <div class="cart-table-header">
            <span class="col-product">{{ localeStore.t('cart.formulation') || 'Formulation' }}</span>
            <span class="col-price">{{ localeStore.t('common.price') || 'Price' }}</span>
            <span class="col-qty">{{ localeStore.t('common.quantity') || 'Quantity' }}</span>
            <span class="col-total">{{ localeStore.t('common.total') || 'Total' }}</span>
          </div>

          <div v-for="item in cartStore.items" :key="item.id" class="cart-row">
            <div class="product-cell">
              <img
                :src="item.image_url"
                :alt="item.name"
                class="table-img"
                @error="$event.target.src = '/images/prod-essence.jpg'"
              />
              <div class="cell-info">
                <span class="cell-cat">{{ item.category_name }}</span>
                <router-link :to="`/product/${item.slug}`" class="cell-title">
                  {{ item.name }}
                </router-link>
                <div class="mobile-price-line">
                  {{ localeStore.formatPrice(item.price) }}
                </div>
                <button class="cell-remove" @click="cartStore.removeItem(item.id)">
                  <Trash2 :size="14" /> {{ localeStore.t('common.delete') || 'Remove' }}
                </button>
              </div>
            </div>

            <div class="price-cell desktop-only">
              {{ localeStore.formatPrice(item.price) }}
            </div>

            <div class="cart-row-controls">
              <div class="qty-cell">
                <div class="qty-control">
                  <button @click="cartStore.updateQuantity(item.id, item.quantity - 1)" class="qty-btn" aria-label="Decrease quantity">
                    <Minus :size="12" />
                  </button>
                  <span class="qty-val">{{ item.quantity }}</span>
                  <button @click="cartStore.updateQuantity(item.id, item.quantity + 1)" class="qty-btn" aria-label="Increase quantity">
                    <Plus :size="12" />
                  </button>
                </div>
              </div>

              <div class="total-cell">
                {{ localeStore.formatPrice(item.price * item.quantity) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary Side Card -->
        <aside class="cart-summary-card">
          <h3>{{ localeStore.t('checkout.order_summary') || 'Summary' }}</h3>

          <!-- Promo Input -->
          <div class="promo-box">
            <div v-if="!cartStore.discountCode" class="promo-form">
              <input
                type="text"
                v-model="promoInput"
                placeholder="Code (Try LUMEA10)"
                class="promo-input"
                @keyup.enter="applyPromo"
              />
              <button class="btn btn-outline btn-sm" @click="applyPromo">{{ localeStore.t('common.apply') || 'Apply' }}</button>
            </div>
            <div v-else class="promo-badge">
              <span>Code <strong>{{ cartStore.discountCode }}</strong> (−{{ localeStore.formatPrice(cartStore.discountAmount) }})</span>
              <button @click="cartStore.removePromoCode" class="remove-btn">Remove</button>
            </div>
          </div>

          <!-- Totals Breakdown -->
          <div class="summary-lines">
            <div class="summary-line">
              <span>{{ localeStore.t('common.subtotal') || 'Subtotal' }}</span>
              <span>{{ localeStore.formatPrice(cartStore.subtotal) }}</span>
            </div>
            <div v-if="cartStore.discountAmount > 0" class="summary-line discount-line">
              <span>{{ localeStore.t('common.discount') || 'Promo Discount' }}</span>
              <span>-{{ localeStore.formatPrice(cartStore.discountAmount) }}</span>
            </div>
            <div class="summary-line">
              <span>{{ localeStore.t('common.shipping') || 'Complimentary Shipping' }}</span>
              <span>{{ cartStore.shippingFee === 0 ? localeStore.t('common.free') : localeStore.formatPrice(cartStore.shippingFee) }}</span>
            </div>
            <div class="summary-line total-line">
              <span>{{ localeStore.t('common.total') || 'Total' }}</span>
              <div class="cart-total-wrap">
                <span class="total-num">{{ localeStore.formatPrice(cartStore.grandTotal) }}</span>
                <span v-if="localeStore.currentCurrency !== 'USD'" class="total-usd-hint">({{ localeStore.formatPrice(cartStore.grandTotal, 'USD') }} USD)</span>
              </div>
            </div>
          </div>

          <router-link to="/checkout" class="btn btn-primary btn-lg btn-block">
            {{ localeStore.t('cart.checkout_btn') || 'Proceed to Checkout' }}
          </router-link>

          <router-link to="/shop" class="btn btn-ghost btn-block continue-link">
            &larr; {{ localeStore.t('cart.return_to_catalog') || 'Continue Exploring' }}
          </router-link>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notification'
import { useLocaleStore } from '@/stores/locale'
import { ShoppingBag, Trash2, Plus, Minus } from 'lucide-vue-next'

const cartStore = useCartStore()
const notificationStore = useNotificationStore()
const localeStore = useLocaleStore()
const promoInput = ref('')

const applyPromo = async () => {
  if (!promoInput.value) return
  const result = await cartStore.applyPromoCode(promoInput.value)
  if (result.success) {
    notificationStore.addToast(result.message, 'success')
    promoInput.value = ''
  } else {
    notificationStore.addToast(result.message, 'error')
  }
}
</script>

<style scoped>
.cart-page {
  padding: 1.25rem 0 4rem;
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

/* Panoramic Hero Banner matching format/Cart.png */
.cart-hero-banner {
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

.empty-cart-view {
  padding: 6rem 2rem;
  text-align: center;
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px dashed var(--border-strong);
  max-width: 600px;
  margin: 0 auto;
}

.empty-icon {
  color: var(--accent-gold);
  margin-bottom: 1.5rem;
}

.empty-cart-view h2 {
  margin-bottom: 0.75rem;
}

.empty-cart-view p {
  margin-bottom: 2rem;
}

.cart-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 3.5rem;
  align-items: start;
}

.cart-items-section {
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  padding: 2rem;
}

.cart-table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}

.cart-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--border-subtle);
}

.cart-row:last-child {
  border-bottom: none;
}

.product-cell {
  display: flex;
  gap: 1.25rem;
  align-items: center;
}

.table-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-md);
  background: var(--bg-muted);
}

.cell-info {
  display: flex;
  flex-direction: column;
}

.cell-cat {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.cell-title {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary);
  margin: 0.15rem 0 0.4rem;
}

.cell-remove {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.78rem;
  color: var(--text-muted);
  width: fit-content;
}

.cell-remove:hover {
  color: #DC2626;
}

.price-cell, .total-cell {
  font-weight: 600;
  color: var(--text-primary);
}

.total-cell {
  font-size: 1.05rem;
}

.qty-control {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
}

.qty-btn {
  padding: 0.35rem 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.qty-val {
  font-size: 0.85rem;
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

.cart-summary-card {
  background: var(--bg-surface);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-subtle);
  padding: 2rem;
}

.cart-summary-card h3 {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.promo-box {
  margin-bottom: 1.5rem;
}

.promo-form {
  display: flex;
  gap: 0.5rem;
}

.promo-input {
  flex: 1;
  padding: 0.6rem 0.85rem;
  font-size: 0.85rem;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-md);
}

.promo-badge {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.85rem;
  background: rgba(194, 155, 56, 0.12);
  border-radius: var(--radius-md);
  font-size: 0.82rem;
  color: var(--accent-gold);
}

.promo-badge .remove-btn {
  font-size: 0.75rem;
  text-decoration: underline;
  color: var(--text-secondary);
}

.summary-lines {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.75rem;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.discount-line {
  color: #10B981;
}

.total-line {
  padding-top: 1rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
}

.cart-total-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.total-num {
  font-size: 1.35rem;
}

.total-usd-hint {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 500;
  margin-top: 2px;
}

.btn-block {
  width: 100%;
}

.continue-link {
  margin-top: 0.75rem;
  font-size: 0.85rem;
}

.cart-row-controls {
  display: contents;
}

.mobile-price-line {
  display: none;
  font-size: 0.85rem;
  color: #78716C;
  margin: 3px 0 6px;
}

@media (max-width: 960px) {
  .cart-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .cart-hero-banner {
    grid-template-columns: 1fr;
  }
  .hero-right-stage {
    min-height: 160px;
  }
  .hero-left-content {
    padding: 1.5rem;
  }
}

@media (max-width: 640px) {
  .cart-items-section {
    padding: 1rem;
  }
  .cart-table-header {
    display: none;
  }
  .cart-row {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    padding: 1.15rem 0;
  }
  .product-cell {
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
  }
  .table-img {
    width: 64px;
    height: 64px;
    flex-shrink: 0;
  }
  .mobile-price-line {
    display: block;
  }
  .desktop-only {
    display: none !important;
  }
  .cart-row-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding-top: 0.65rem;
    border-top: 1px dashed var(--border-subtle);
  }
  .total-cell {
    font-size: 1.05rem;
    font-weight: 700;
  }
  .script-row {
    font-size: 1.15rem;
  }
  .banner-script-overlay {
    top: 1rem;
    right: 1rem;
  }
  .hero-title {
    font-size: 2rem;
  }
  .hero-desc {
    font-size: 0.95rem;
  }
}

@media (max-width: 360px) {
  .cart-items-section,
  .cart-summary-card {
    padding: 0.85rem;
  }
  .hero-left-content {
    padding: 1.25rem 0.85rem;
  }
  .hero-title {
    font-size: 1.7rem;
  }
}
</style>
