<template>
  <div class="drawer-container" :class="{ 'is-active': cartStore.isDrawerOpen }">
    <!-- Backdrop Overlay -->
    <div class="drawer-backdrop" @click="cartStore.closeDrawer"></div>

    <!-- Drawer Panel -->
    <aside class="drawer-panel">
      <!-- Header -->
      <div class="drawer-header">
        <div class="header-title">
          <h3>Shopping Bag</h3>
          <span class="badge badge-subtle">{{ cartStore.totalItems }} items</span>
        </div>
        <button class="close-btn" @click="cartStore.closeDrawer" aria-label="Close Bag">
          <X :size="20" />
        </button>
      </div>

      <!-- Free Shipping Bar -->
      <div class="shipping-tracker">
        <div class="tracker-text">
          <span v-if="cartStore.subtotal >= cartStore.freeShippingThreshold" class="shipping-unlocked">
            <Sparkles :size="15" class="shipping-sparkle" /> You have unlocked <strong>Free Complimentary Shipping!</strong>
          </span>
          <span v-else>
            Add <strong>${{ Math.max(0, cartStore.freeShippingThreshold - cartStore.subtotal).toFixed(2) }}</strong> more for Free Shipping
          </span>
        </div>
        <div class="progress-bar-bg">
          <div
            class="progress-bar-fill"
            :style="{ width: Math.min(100, (cartStore.subtotal / cartStore.freeShippingThreshold) * 100) + '%' }"
          ></div>
        </div>
      </div>

      <!-- Items List -->
      <div class="drawer-body">
        <div v-if="cartStore.items.length === 0" class="empty-state">
          <div class="empty-icon-wrap">
            <ShoppingBag :size="36" />
          </div>
          <h4>Your bag is empty</h4>
          <p>Explore our curated selection of transformative skincare essentials.</p>
          <button class="btn btn-outline btn-sm" @click="exploreShop">
            Start Exploring
          </button>
        </div>

        <div v-else class="items-list">
          <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
            <img
              :src="item.image_url"
              :alt="item.name"
              class="item-img"
              @error="$event.target.src = '/images/prod-essence.jpg'"
            />
            <div class="item-details">
              <div class="item-top">
                <router-link
                  :to="`/product/${item.slug}`"
                  class="item-name"
                  @click="cartStore.closeDrawer"
                >
                  {{ item.name }}
                </router-link>
                <button class="remove-btn" @click="cartStore.removeItem(item.id)" title="Remove">
                  <Trash2 :size="15" />
                </button>
              </div>

              <span class="item-category">{{ item.category_name }}</span>

              <div class="item-bottom">
                <!-- Quantity Controls -->
                <div class="qty-control">
                  <button @click="cartStore.updateQuantity(item.id, item.quantity - 1)" class="qty-btn">
                    <Minus :size="13" />
                  </button>
                  <span class="qty-val">{{ item.quantity }}</span>
                  <button @click="cartStore.updateQuantity(item.id, item.quantity + 1)" class="qty-btn">
                    <Plus :size="13" />
                  </button>
                </div>

                <span class="item-total">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer & Totals -->
      <div v-if="cartStore.items.length > 0" class="drawer-footer">
        <!-- Promo Code Input -->
        <div class="promo-section">
          <div class="promo-input-group" v-if="!cartStore.discountCode">
            <input
              type="text"
              v-model="promoInput"
              placeholder="Promo code (Try LUMEA10)"
              class="promo-input"
              @keyup.enter="applyPromo"
            />
            <button class="btn btn-sm btn-outline" @click="applyPromo">Apply</button>
          </div>
          <div v-else class="promo-applied">
            <span class="applied-tag">
              <Check :size="14" /> {{ cartStore.discountCode }} Applied (-10%)
            </span>
            <button class="remove-promo" @click="cartStore.removePromoCode">Remove</button>
          </div>
        </div>

        <!-- Price Breakdown -->
        <div class="totals-breakdown">
          <div class="total-row">
            <span>Subtotal</span>
            <span>${{ cartStore.subtotal.toFixed(2) }}</span>
          </div>
          <div v-if="cartStore.discountAmount > 0" class="total-row discount-row">
            <span>Promo Discount</span>
            <span>-${{ cartStore.discountAmount.toFixed(2) }}</span>
          </div>
          <div class="total-row">
            <span>Estimated Shipping</span>
            <span>{{ cartStore.shippingFee === 0 ? 'Free' : `$${cartStore.shippingFee.toFixed(2)}` }}</span>
          </div>
          <div class="total-row grand-total-row">
            <span>Total</span>
            <span class="grand-total-amount">${{ cartStore.grandTotal.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Checkout Buttons -->
        <div class="action-buttons">
          <button class="btn btn-primary btn-block btn-lg" @click="goToCheckout">
            Proceed to Checkout
          </button>
          <router-link to="/cart" class="btn btn-outline btn-block" @click="cartStore.closeDrawer">
            View Full Bag
          </router-link>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notification'
import { X, Trash2, Plus, Minus, ShoppingBag, Check, Sparkles } from 'lucide-vue-next'

const router = useRouter()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

onMounted(() => {
  cartStore.fetchSettings()
})

const promoInput = ref('')

const applyPromo = () => {
  if (!promoInput.value) return
  const result = cartStore.applyPromoCode(promoInput.value)
  if (result.success) {
    notificationStore.addToast(result.message, 'success')
    promoInput.value = ''
  } else {
    notificationStore.addToast(result.message, 'error')
  }
}

const exploreShop = () => {
  cartStore.closeDrawer()
  router.push('/shop')
}

const goToCheckout = () => {
  cartStore.closeDrawer()
  router.push('/checkout')
}
</script>

<style scoped>
.drawer-container {
  position: fixed;
  inset: 0;
  z-index: 999;
  visibility: hidden;
  transition: visibility var(--transition-normal);
}

.drawer-container.is-active {
  visibility: visible;
}

.drawer-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(18, 19, 22, 0.5);
  backdrop-filter: blur(4px);
  opacity: 0;
  transition: opacity var(--transition-normal);
}

.drawer-container.is-active .drawer-backdrop {
  opacity: 1;
}

.drawer-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  max-width: 440px;
  height: 100%;
  background: var(--bg-surface);
  box-shadow: var(--shadow-floating);
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform var(--transition-smooth);
}

.drawer-container.is-active .drawer-panel {
  transform: translateX(0);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-subtle);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-title h3 {
  font-size: 1.25rem;
}

.close-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.close-btn:hover {
  background: var(--bg-muted);
  color: var(--text-primary);
}

.shipping-tracker {
  background: var(--bg-muted);
  padding: 0.85rem 1.5rem;
  border-bottom: 1px solid var(--border-subtle);
}

.tracker-text {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.shipping-unlocked {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.shipping-sparkle {
  color: var(--color-primary);
  flex-shrink: 0;
}

.progress-bar-bg {
  height: 5px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: var(--accent-gold);
  border-radius: var(--radius-full);
  transition: width 0.4s ease;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 1rem;
}

.empty-icon-wrap {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--bg-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
}

.empty-state h4 {
  font-size: 1.15rem;
}

.empty-state p {
  font-size: 0.88rem;
  max-width: 260px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border-subtle);
}

.item-img {
  width: 76px;
  height: 76px;
  object-fit: cover;
  border-radius: var(--radius-md);
  background: var(--bg-muted);
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-top {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.item-name {
  font-size: 0.925rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
}

.item-category {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0.2rem 0 0.5rem;
}

.remove-btn {
  color: var(--text-muted);
  padding: 2px;
  transition: color var(--transition-fast);
}

.remove-btn:hover {
  color: #DC2626;
}

.item-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}

.qty-control {
  display: flex;
  align-items: center;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
}

.qty-btn {
  padding: 0.25rem 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.qty-btn:hover {
  color: var(--text-primary);
}

.qty-val {
  font-size: 0.825rem;
  font-weight: 600;
  min-width: 22px;
  text-align: center;
}

.item-total {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.drawer-footer {
  padding: 1.25rem 1.5rem 1.5rem;
  border-top: 1px solid var(--border-subtle);
  background: #FCFBFA;
}

.promo-section {
  margin-bottom: 1rem;
}

.promo-input-group {
  display: flex;
  gap: 0.5rem;
}

.promo-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  font-size: 0.825rem;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-md);
  background: #FFFFFF;
}

.promo-applied {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.4rem 0.75rem;
  background: rgba(194, 155, 56, 0.12);
  border-radius: var(--radius-md);
  font-size: 0.8rem;
  color: var(--accent-gold);
  font-weight: 600;
}

.applied-tag {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.remove-promo {
  color: var(--text-secondary);
  font-size: 0.75rem;
  text-decoration: underline;
}

.totals-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  margin-bottom: 1.25rem;
}

.total-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.discount-row {
  color: #10B981;
}

.grand-total-row {
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
}

.grand-total-amount {
  font-size: 1.25rem;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.btn-block {
  width: 100%;
}
</style>
