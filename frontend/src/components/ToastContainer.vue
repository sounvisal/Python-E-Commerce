<template>
  <div class="toast-container" v-if="notificationStore.toasts.length > 0">
    <div
      v-for="toast in notificationStore.toasts"
      :key="toast.id"
      class="toast"
      :class="`toast-${toast.type}`"
    >
      <CheckCircle2 v-if="toast.type === 'success'" :size="18" class="icon-success" />
      <AlertCircle v-else-if="toast.type === 'error'" :size="18" class="icon-error" />
      <Info v-else :size="18" />
      <span>{{ toast.message }}</span>
    </div>
  </div>
</template>

<script setup>
import { useNotificationStore } from '@/stores/notification'
import { CheckCircle2, AlertCircle, Info } from 'lucide-vue-next'

const notificationStore = useNotificationStore()
</script>

<style scoped>
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
