<template>
  <div class="toast-container" role="status" aria-atomic="false">
    <TransitionGroup name="toast">
      <div
        v-for="toast in notificationStore.toasts"
        :key="toast.id"
        class="toast"
        :class="`toast-${toast.type}`"
      >
        <CheckCircle2 v-if="toast.type === 'success'" :size="18" class="icon-success" aria-hidden="true" />
        <AlertCircle v-else-if="toast.type === 'error'" :size="18" class="icon-error" aria-hidden="true" />
        <Info v-else :size="18" aria-hidden="true" />
        <span>{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notification'
import { CheckCircle2, AlertCircle, Info } from 'lucide-vue-next'

const notificationStore = useNotificationStore()
</script>

<style scoped>
.toast > svg {
  flex-shrink: 0;
}

.toast-enter-active {
  transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out);
}

.toast-leave-active {
  transition: opacity 150ms var(--ease-out), transform 150ms var(--ease-out);
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

.toast-success {
  border-left: 4px solid #10B981;
}

.toast-error {
  border-left: 4px solid #EF4444;
}

.icon-success {
  color: #10B981;
}

.icon-error {
  color: #EF4444;
}
</style>
