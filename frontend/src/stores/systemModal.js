import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSystemModalStore = defineStore('systemModal', () => {
  // Session Expired State
  const isSessionExpired = ref(false)

  // Global Error State
  const isErrorOpen = ref(false)
  const errorMessage = ref("We couldn't process your request. Please try again in a moment.")
  const retryCallback = ref(null)

  // Added To Cart Success State
  const isAddToCartSuccessOpen = ref(false)
  const addedProduct = ref({
    name: 'SK-II Facial Treatment Essence',
    volume: '230ml',
    price: 125.0,
    image_url: '/images/prod-sk2.jpg'
  })

  function showSessionExpired() {
    isSessionExpired.value = true
  }

  function hideSessionExpired() {
    isSessionExpired.value = false
  }

  function showError(message, onRetry = null) {
    errorMessage.value = message || "We couldn't process your request. Please try again in a moment."
    retryCallback.value = onRetry
    isErrorOpen.value = true
  }

  function hideError() {
    isErrorOpen.value = false
    retryCallback.value = null
  }

  function retryErrorAction() {
    if (typeof retryCallback.value === 'function') {
      retryCallback.value()
    }
    hideError()
  }

  function showAddToCartSuccess(product) {
    if (product) {
      addedProduct.value = {
        name: product.name || 'Skincare Formulation',
        volume: product.volume || 'Standard Size',
        price: product.price || 0.0,
        image_url: product.image_url || '/images/prod-sk2.jpg'
      }
    }
    isAddToCartSuccessOpen.value = true
  }

  function hideAddToCartSuccess() {
    isAddToCartSuccessOpen.value = false
  }

  return {
    isSessionExpired,
    showSessionExpired,
    hideSessionExpired,

    isErrorOpen,
    errorMessage,
    showError,
    hideError,
    retryErrorAction,

    isAddToCartSuccessOpen,
    addedProduct,
    showAddToCartSuccess,
    hideAddToCartSuccess
  }
})
