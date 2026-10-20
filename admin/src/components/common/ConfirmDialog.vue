<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="handleCancel">
        <div class="confirm-dialog" @click.stop>
          <div class="dialog-icon" :class="`icon-${type}`">
            <AlertTriangle v-if="type === 'warning'" :size="24" />
            <Trash2 v-else-if="type === 'danger'" :size="24" />
            <Info v-else :size="24" />
          </div>

          <h3 class="dialog-title">{{ title }}</h3>
          <p class="dialog-message">{{ message }}</p>

          <div class="dialog-actions">
            <button type="button" class="btn-cancel" @click="handleCancel">
              {{ cancelText }}
            </button>
            <button
              type="button"
              class="btn-confirm"
              :class="`btn-${type}`"
              @click="handleConfirm"
            >
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { AlertTriangle, Trash2, Info } from 'lucide-vue-next'

defineProps({
  isOpen: { type: Boolean, default: false },
  title: { type: String, default: 'Confirm Action' },
  message: { type: String, required: true },
  type: { type: String, default: 'warning' }, // 'warning' | 'danger' | 'info'
  confirmText: { type: String, default: 'Confirm' },
  cancelText: { type: String, default: 'Cancel' }
})

const emit = defineEmits(['confirm', 'cancel'])

function handleConfirm() {
  emit('confirm')
}

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26, 23, 21, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.confirm-dialog {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 2rem;
  max-width: 420px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  text-align: center;
  border: 1px solid #EFE7E0;
}

.dialog-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.icon-warning {
  background: #FFF7ED;
  color: #D97706;
}

.icon-danger {
  background: #FDF0EE;
  color: #84261B;
}

.icon-info {
  background: #EFF6FF;
  color: #2563EB;
}

.dialog-title {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 1.25rem;
  color: #2D2422;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.dialog-message {
  font-size: 0.875rem;
  color: #6E635E;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.dialog-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-cancel {
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  color: #3C3530;
}

.btn-cancel:hover {
  background: #EFE7E0;
}

.btn-confirm {
  border: none;
  color: #FFFFFF;
}

.btn-warning {
  background: #D97706;
}

.btn-warning:hover {
  background: #B45309;
}

.btn-danger {
  background: #84261B;
}

.btn-danger:hover {
  background: #6C1E14;
}

.btn-info {
  background: #2563EB;
}

.btn-info:hover {
  background: #1D4ED8;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
