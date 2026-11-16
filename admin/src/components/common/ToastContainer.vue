<script setup>
import { useAdminStore } from '@/stores/admin'
import { AlertCircle, CheckCircle, Info, X } from 'lucide-vue-next'

const adminStore = useAdminStore()
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="toast in adminStore.toasts"
        :key="toast.id"
        class="toast-item"
        :class="`toast-${toast.type}`"
      >
        <div class="toast-icon">
          <CheckCircle v-if="toast.type === 'success'" :size="18" />
          <AlertCircle v-else-if="toast.type === 'error'" :size="18" />
          <Info v-else :size="18" />
        </div>
        <div class="toast-content">{{ toast.message }}</div>
        <button class="toast-close" type="button" aria-label="Dismiss notification" @click="adminStore.removeToast(toast.id)">
          <X :size="14" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: min(400px, calc(100% - 48px));
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-elevated);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-medium);
  font-size: 0.88rem;
  color: var(--text-main);
  backdrop-filter: blur(12px);
}

.toast-success {
  border-left: 4px solid var(--emerald);
}
.toast-success .toast-icon {
  color: var(--emerald);
}

.toast-error {
  border-left: 4px solid var(--rose);
}
.toast-error .toast-icon {
  color: var(--rose);
}

.toast-info {
  border-left: 4px solid var(--gold);
}
.toast-info .toast-icon {
  color: var(--gold);
}

.toast-content {
  flex: 1;
  overflow-wrap: anywhere;
}

.toast-close {
  color: var(--text-dim);
  padding: 2px;
  border-radius: 4px;
  transition: color var(--transition-fast);
}

.toast-close:hover {
  color: var(--text-main);
}

.toast-enter-active {
  transition: opacity 200ms cubic-bezier(0.23, 1, 0.32, 1), transform 200ms cubic-bezier(0.23, 1, 0.32, 1);
}

.toast-leave-active {
  transition: opacity 150ms cubic-bezier(0.23, 1, 0.32, 1), transform 150ms cubic-bezier(0.23, 1, 0.32, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

@media (prefers-reduced-motion: reduce) {
  .toast-enter-from,
  .toast-leave-to {
    transform: none;
  }
}
</style>
