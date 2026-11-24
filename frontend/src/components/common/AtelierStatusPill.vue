<template>
  <transition name="pill-fade">
    <div
      v-if="productStore.isOffline"
      class="atelier-offline-pill"
      role="status"
      aria-live="polite"
    >
      <div class="pill-dot-pulse"></div>
      <span class="pill-text">Atelier Offline Mode · Curated Preview</span>
      <button
        class="pill-retry-btn"
        @click="retryConnection"
        :disabled="isRetrying"
        title="Retry connecting to Python Atelier server"
      >
        <RefreshCw :size="12" :class="{ 'is-spinning': isRetrying }" />
        <span>{{ isRetrying ? 'Connecting…' : 'Reconnect' }}</span>
      </button>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { RefreshCw } from 'lucide-vue-next'
import { useProductStore } from '@/stores/products'
import { useBannerStore } from '@/stores/banners'

const productStore = useProductStore()
const bannerStore = useBannerStore()
const isRetrying = ref(false)

async function retryConnection() {
  if (isRetrying.value) return
  isRetrying.value = true
  try {
    await Promise.allSettled([
      productStore.fetchProducts(),
      productStore.fetchCategories(),
      bannerStore.fetchBanners()
    ])
  } finally {
    setTimeout(() => {
      isRetrying.value = false
    }, 600)
  }
}
</script>

<style scoped>
.atelier-offline-pill {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 999;
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  background: rgba(28, 25, 23, 0.92);
  backdrop-filter: blur(12px);
  color: #FAF8F5;
  padding: 0.5rem 0.95rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 500;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: all 0.25s ease;
}

.pill-dot-pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #E09F3E;
  box-shadow: 0 0 0 0 rgba(224, 159, 62, 0.7);
  animation: dotPulse 2s infinite;
}

@keyframes dotPulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(224, 159, 62, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 6px rgba(224, 159, 62, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(224, 159, 62, 0);
  }
}

.pill-text {
  letter-spacing: 0.02em;
}

.pill-retry-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: #FFFFFF;
  padding: 0.22rem 0.55rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease;
}

.pill-retry-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.28);
  transform: translateY(-1px);
}

.pill-retry-btn:active:not(:disabled) {
  transform: scale(0.96);
}

.is-spinning {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pill-fade-enter-active,
.pill-fade-leave-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.pill-fade-enter-from,
.pill-fade-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.95);
}

@media (max-width: 600px) {
  .atelier-offline-pill {
    bottom: 1rem;
    right: 1rem;
    left: 1rem;
    justify-content: space-between;
  }
}
</style>
