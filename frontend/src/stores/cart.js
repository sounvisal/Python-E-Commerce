import axios from 'axios'
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('lumea_cart') || '[]'),
    isDrawerOpen: false,
    discountCode: localStorage.getItem('lumea_discount_code') || '',
    discountRate: parseFloat(localStorage.getItem('lumea_discount_rate') || '0'),
    freeShippingThreshold: 50.0,
    taxRate: 10.0,
    standardShippingFee: 15.0,
    settingsLoaded: false,
  }),

  getters: {
    totalItems: (state) => state.items.reduce((sum, item) => sum + item.quantity, 0),

    subtotal: (state) => {
      const sum = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      return Math.round(sum * 100) / 100
    },

    discountAmount: (state) => {
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      return Math.round(sub * state.discountRate * 100) / 100
    },

    shippingFee: (state) => {
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      if (sub === 0) return 0
      return sub >= state.freeShippingThreshold ? 0 : state.standardShippingFee
    },

    taxAmount: (state) => {
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      const discount = Math.round(sub * state.discountRate * 100) / 100
      const taxable = Math.max(0, sub - discount)
      return Math.round(taxable * (state.taxRate / 100) * 100) / 100
    },

    grandTotal: (state) => {
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      const discount = Math.round(sub * state.discountRate * 100) / 100
      const shipping = sub === 0 ? 0 : sub >= state.freeShippingThreshold ? 0 : state.standardShippingFee
      return Math.max(0, Math.round((sub - discount + shipping) * 100) / 100)
    },
  },

  actions: {
    saveToStorage() {
      localStorage.setItem('lumea_cart', JSON.stringify(this.items))
      localStorage.setItem('lumea_discount_code', this.discountCode)
      localStorage.setItem('lumea_discount_rate', this.discountRate.toString())
    },

    addItem(product, quantity = 1) {
      const existing = this.items.find((item) => item.id === product.id)
      if (existing) {
        existing.quantity += quantity
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          slug: product.slug,
          price: product.price,
          compare_at_price: product.compare_at_price,
          image_url: product.image_url,
          category_name: product.category?.name || 'Curated',
          quantity: quantity,
        })
      }
      this.saveToStorage()
      this.openDrawer()
    },

    updateQuantity(productId, quantity) {
      if (quantity <= 0) {
        this.removeItem(productId)
        return
      }
      const item = this.items.find((i) => i.id === productId)
      if (item) {
        item.quantity = quantity
        this.saveToStorage()
      }
    },

    removeItem(productId) {
      this.items = this.items.filter((i) => i.id !== productId)
      this.saveToStorage()
    },

    clearCart() {
      this.items = []
      this.discountCode = ''
      this.discountRate = 0
      this.saveToStorage()
    },

    applyPromoCode(code) {
      const cleanCode = code.trim().toUpperCase()
      if (cleanCode === 'LUMEA10') {
        this.discountCode = cleanCode
        this.discountRate = 0.10 // 10% off
        this.saveToStorage()
        return { success: true, message: 'Promo code applied: 10% off your atelier order!' }
      } else if (cleanCode === 'LUMEA20') {
        this.discountCode = cleanCode
        this.discountRate = 0.20 // 20% off
        this.saveToStorage()
        return { success: true, message: 'VIP Privilege code applied: 20% off your entire order!' }
      } else if (cleanCode === 'ATELIER15') {
        this.discountCode = cleanCode
        this.discountRate = 0.15 // 15% off
        this.saveToStorage()
        return { success: true, message: 'Curator code applied: 15% off!' }
      }
      return { success: false, message: 'Invalid promo code. Try LUMEA10, LUMEA20, or ATELIER15' }
    },

    removePromoCode() {
      this.discountCode = ''
      this.discountRate = 0
      this.saveToStorage()
    },

    openDrawer() {
      this.isDrawerOpen = true
    },

    closeDrawer() {
      this.isDrawerOpen = false
    },

    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen
    },

    async fetchSettings() {
      try {
        const res = await axios.get('/api/settings')
        if (res.data?.status === 'success' && res.data.data) {
          const d = res.data.data
          if (d.free_shipping_threshold !== undefined) {
            this.freeShippingThreshold = Number(d.free_shipping_threshold)
          }
          if (d.tax_rate !== undefined) {
            this.taxRate = Number(d.tax_rate)
          }
          this.settingsLoaded = true
        }
      } catch (err) {
        // Fallback silently to defaults
      }
    },
  },
})
