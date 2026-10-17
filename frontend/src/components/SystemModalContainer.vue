<template>
  <div class="system-modals-root">
    <!-- ======================================================== -->
    <!-- 1. SESSION EXPIRED MODAL (format/System States.png #8)   -->
    <!-- ======================================================== -->
    <Teleport to="body">
      <div
        v-if="systemModalStore.isSessionExpired"
        class="sys-modal-backdrop"
        role="dialog"
        aria-modal="true"
        aria-labelledby="session-expired-title"
      >
        <div class="sys-modal-card">
          <!-- Dark red circular clock icon -->
          <div class="sys-icon-circle icon-clock">
            <Clock :size="30" stroke-width="2" />
          </div>

          <h2 id="session-expired-title" class="sys-modal-title">Your session has expired</h2>
          <p class="sys-modal-subtitle">
            For your security, you've been logged out due to inactivity. Please sign in again to continue.
          </p>

          <div class="sys-btn-group">
            <button type="button" class="btn-sys-primary" @click="handleSignIn">
              Sign In
            </button>
            <button type="button" class="btn-sys-outline" @click="handleGoHome">
              Go to Homepage
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ======================================================== -->
    <!-- 2. GLOBAL ERROR MODAL (format/System States.png #5)      -->
    <!-- ======================================================== -->
    <Teleport to="body">
      <div
        v-if="systemModalStore.isErrorOpen"
        class="sys-modal-backdrop"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="error-modal-title"
      >
        <div class="sys-modal-card">
          <button
            type="button"
            class="sys-close-btn"
            aria-label="Close Error Modal"
            @click="systemModalStore.hideError"
          >
            <X :size="18" />
          </button>

          <!-- Soft pink badge with dark red exclamation point -->
          <div class="sys-icon-circle icon-error">
            <span class="exclamation-mark">!</span>
          </div>

          <h2 id="error-modal-title" class="sys-modal-title">Something went wrong</h2>
          <p class="sys-modal-subtitle">
            {{ systemModalStore.errorMessage }}
          </p>

          <div class="sys-btn-group">
            <button type="button" class="btn-sys-primary" @click="systemModalStore.retryErrorAction">
              Try Again
            </button>
            <button type="button" class="btn-sys-outline" @click="systemModalStore.hideError">
              Dismiss
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ======================================================== -->
    <!-- 3. ADDED TO CART MODAL (format/System States.png #4)     -->
    <!-- ======================================================== -->
    <Teleport to="body">
      <div
        v-if="systemModalStore.isAddToCartSuccessOpen"
        class="sys-modal-backdrop"
        role="dialog"
        aria-modal="true"
        aria-labelledby="cart-success-title"
      >
        <div class="sys-modal-card cart-success-card">
          <button
            type="button"
            class="sys-close-btn"
            aria-label="Close Dialog"
            @click="systemModalStore.hideAddToCartSuccess"
          >
            <X :size="18" />
          </button>

          <!-- Soft mint badge with green checkmark -->
          <div class="sys-icon-circle icon-success">
            <Check :size="24" stroke-width="2.5" />
          </div>

          <h2 id="cart-success-title" class="sys-modal-title">Added to Cart</h2>

          <!-- Mini Product Card Row -->
          <div class="mini-prod-row">
            <img
              :src="systemModalStore.addedProduct.image_url"
              :alt="systemModalStore.addedProduct.name"
              class="mini-prod-thumb"
            />
            <div class="mini-prod-meta">
              <strong class="mini-prod-name">{{ systemModalStore.addedProduct.name }}</strong>
              <span class="mini-prod-volume">{{ systemModalStore.addedProduct.volume }}</span>
              <span class="mini-prod-price">${{ Number(systemModalStore.addedProduct.price).toFixed(2) }}</span>
            </div>
          </div>

          <div class="sys-btn-group">
            <button type="button" class="btn-sys-outline" @click="handleViewCart">
              View Cart
            </button>
            <button type="button" class="btn-sys-primary" @click="systemModalStore.hideAddToCartSuccess">
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useSystemModalStore } from '@/stores/systemModal'
import { useCartStore } from '@/stores/cart'
import { Clock, X, Check } from 'lucide-vue-next'

const router = useRouter()
const systemModalStore = useSystemModalStore()
const cartStore = useCartStore()

function handleSignIn() {
  systemModalStore.hideSessionExpired()
  router.push('/login')
}

function handleGoHome() {
  systemModalStore.hideSessionExpired()
  router.push('/')
}

function handleViewCart() {
  systemModalStore.hideAddToCartSuccess()
  // Open cart drawer or route to cart
  if (cartStore && typeof cartStore.openDrawer === 'function') {
    cartStore.openDrawer()
  } else {
    router.push('/cart')
  }
}
</script>

<style scoped>
.sys-modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 12, 10, 0.55);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 1rem;
}

.sys-modal-card {
  position: relative;
  background: #FFFFFF;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  padding: 2.25rem 2rem;
  text-align: center;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.16);
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: modalPopIn 0.22s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes modalPopIn {
  from {
    opacity: 0;
    transform: scale(0.94) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.sys-close-btn {
  position: absolute;
  top: 1.15rem;
  right: 1.15rem;
  background: transparent;
  border: none;
  color: #8C847E;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.15s ease;
}

.sys-close-btn:hover {
  color: #1A1715;
  background-color: #F5EFEB;
}

.sys-icon-circle {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}

/* Clock icon circle (format/System States.png #8) */
.icon-clock {
  border: 2px solid #7A2E22;
  color: #7A2E22;
  background: transparent;
}

/* Error exclamation circle (format/System States.png #5) */
.icon-error {
  background-color: #FCE8E6;
  color: #7A2E22;
}

.exclamation-mark {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}

/* Success check circle (format/System States.png #4) */
.icon-success {
  background-color: #E2F5EA;
  color: #1E8E47;
}

.sys-modal-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.55rem;
  font-weight: 600;
  color: #1A1715;
  margin-bottom: 0.65rem;
  line-height: 1.25;
}

.sys-modal-subtitle {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.92rem;
  color: #554F4A;
  line-height: 1.55;
  margin-bottom: 1.75rem;
  max-width: 360px;
}

/* Mini product row for added-to-cart modal */
.mini-prod-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #FAF7F5;
  border: 1px solid #EFE8E2;
  border-radius: 8px;
  padding: 0.85rem 1rem;
  width: 100%;
  margin-bottom: 1.75rem;
  text-align: left;
}

.mini-prod-thumb {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 6px;
  background: #FFF;
  border: 1px solid #E5DCD5;
}

.mini-prod-meta {
  display: flex;
  flex-direction: column;
}

.mini-prod-name {
  font-size: 0.88rem;
  color: #1A1715;
  line-height: 1.3;
}

.mini-prod-volume {
  font-size: 0.78rem;
  color: #8C847E;
}

.mini-prod-price {
  font-size: 0.86rem;
  font-weight: 600;
  color: #1A1715;
  margin-top: 2px;
}

/* Button Group */
.sys-btn-group {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  justify-content: center;
}

.btn-sys-primary {
  flex: 1;
  background-color: #7A2E22;
  color: #FFFFFF;
  border: 1px solid #7A2E22;
  border-radius: 6px;
  padding: 0.75rem 1.15rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.btn-sys-primary:hover {
  background-color: #63241A;
}

.btn-sys-outline {
  flex: 1;
  background-color: #FFFFFF;
  color: #7A2E22;
  border: 1px solid #D5C7BE;
  border-radius: 6px;
  padding: 0.75rem 1.15rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-sys-outline:hover {
  border-color: #7A2E22;
  background-color: #FAF7F5;
}

@media (max-width: 480px) {
  .sys-btn-group {
    flex-direction: column;
  }
}
</style>
