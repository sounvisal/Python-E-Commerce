import { defineStore } from 'pinia'

// Module-level map to track timeouts and prevent memory leaks
const toastTimeouts = new Map()

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    toasts: [],
  }),

  actions: {
    addToast(message, type = 'success', duration = 3000) {
      const id = Date.now() + Math.random().toString(36).substring(2, 5)
      this.toasts.push({ id, message, type })

      if (duration > 0) {
        const timeoutId = setTimeout(() => {
          this.removeToast(id)
        }, duration)
        toastTimeouts.set(id, timeoutId)
      }
      return id
    },

    removeToast(id) {
      if (toastTimeouts.has(id)) {
        clearTimeout(toastTimeouts.get(id))
        toastTimeouts.delete(id)
      }
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },

    clearAllToasts() {
      toastTimeouts.forEach((timeoutId) => clearTimeout(timeoutId))
      toastTimeouts.clear()
      this.toasts = []
    },
  },
})
