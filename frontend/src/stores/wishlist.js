import { privateStorageKey } from '@/utils/orderAccess'
import { defineStore } from 'pinia'
import { useNotificationStore } from './notification'

export const useWishlistStore = defineStore('wishlist', {
  state: () => {
    const stored = localStorage.getItem(privateStorageKey('wishlist'))
    return {
      items: (() => { try { return stored ? JSON.parse(stored) : [] } catch { return [] } })(),
    }
  },

  getters: {
    totalItems: (state) => state.items.length,
    isInWishlist: (state) => (productId) => state.items.some((item) => item.id === productId),
    recentlyViewed: (state) => state.items.filter((item) => item.isRecent),
    priceDrops: (state) => state.items.filter((item) => item.isPriceDrop || (item.compare_at_price && item.compare_at_price > item.price)),
    backInStock: (state) => state.items.filter((item) => item.stockStatus === 'Back in Stock' || item.stockStatus === 'Low Stock'),
  },

  actions: {
    loadProfile() {
      try { this.items = JSON.parse(localStorage.getItem(privateStorageKey('wishlist')) || '[]') } catch { this.items = [] }
    },
    saveToStorage() {
      localStorage.setItem(privateStorageKey('wishlist'), JSON.stringify(this.items))
    },

    toggleItem(product) {
      const notificationStore = useNotificationStore()
      const index = this.items.findIndex((item) => item.id === product.id)
      if (index > -1) {
        this.items.splice(index, 1)
        this.saveToStorage()
        notificationStore.addToast(`Removed "${product.name}" from wishlist`, 'info')
        return false
      } else {
        this.items.unshift({
          id: product.id,
          name: product.name,
          brand: product.brand,
          volume: product.volume || '50 ml',
          price: Number(product.price),
          compare_at_price: product.compare_at_price ? Number(product.compare_at_price) : null,
          rating: product.rating || 4.8,
          reviews: product.reviews || '500',
          stockStatus: product.stockStatus || 'In Stock',
          isPriceDrop: Boolean(product.compare_at_price && product.compare_at_price > product.price),
          isRecent: true,
          image_url: product.image_url,
          slug: product.slug,
          addedAt: new Date().toISOString(),
        })
        this.saveToStorage()
        notificationStore.addToast(`Saved "${product.name}" to wishlist`, 'success')
        return true
      }
    },

    addItem(product) {
      if (!this.isInWishlist(product.id)) {
        this.toggleItem(product)
      }
    },

    removeItem(productId) {
      const item = this.items.find((i) => i.id === productId)
      this.items = this.items.filter((i) => i.id !== productId)
      this.saveToStorage()
      if (item) {
        const notificationStore = useNotificationStore()
        notificationStore.addToast(`Removed "${item.name}" from wishlist`, 'info')
      }
    },

    removeMultiple(ids) {
      this.items = this.items.filter((i) => !ids.includes(i.id))
      this.saveToStorage()
      const notificationStore = useNotificationStore()
      notificationStore.addToast(`Removed ${ids.length} items from wishlist`, 'info')
    },

    resetToDefault() {
      this.items = [...initialMockItems]
      this.saveToStorage()
    },

    clearAll() {
      this.items = []
      this.saveToStorage()
    },
  },
})
