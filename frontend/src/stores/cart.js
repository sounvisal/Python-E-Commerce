import axios from 'axios'
import { defineStore } from 'pinia'
import { safeGetJSON, safeSetJSON } from '@/utils/storage'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: safeGetJSON('lumea_cart', []),
    isDrawerOpen: false,
    discountCode: localStorage.getItem('lumea_discount_code') || '',
    discountRate: parseFloat(localStorage.getItem('lumea_discount_rate') || '0'),
    freeShippingThreshold: 50.0,
    taxRate: 10.0,
    standardShippingFee: 1.50,
    carrierFeeMap: {
      vet_express: 1.50,
      jt_express: 1.75,
      grab_express: 3.50,
      lumea_concierge: 3.00,
    },
    selectedCarrier: 'vet_express',
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
      const carrierFee = state.carrierFeeMap[state.selectedCarrier] ?? 1.50
      if (sub >= state.freeShippingThreshold && state.selectedCarrier !== 'grab_express') {
        return 0
      }
      return carrierFee
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
      const carrierFee = state.carrierFeeMap[state.selectedCarrier] ?? 1.50
      const shipping = sub === 0 ? 0 : (sub >= state.freeShippingThreshold && state.selectedCarrier !== 'grab_express') ? 0 : carrierFee
      return Math.max(0, Math.round((sub - discount + shipping) * 100) / 100)
    },
  },

  actions: {
    saveToStorage() {
      safeSetJSON('lumea_cart', this.items)
      localStorage.setItem('lumea_discount_code', this.discountCode)
      localStorage.setItem('lumea_discount_rate', this.discountRate.toString())
    },

    setCarrier(carrierId) {
      if (this.carrierFeeMap[carrierId] !== undefined) {
        this.selectedCarrier = carrierId
      }
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

    async applyPromoCode(code) {
      const cleanCode = (code || '').trim().toUpperCase()
      if (!cleanCode) return { success: false, message: 'Enter a promotion code.' }
      try {
        const { data } = await axios.get(`/api/promotions/validate/${encodeURIComponent(cleanCode)}`)
        this.discountCode = data.code
        this.discountRate = data.rate
        this.saveToStorage()
        return { success: true, message: `Promotion ${data.code} applied.` }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail || 'Unable to validate the promotion. Please retry.' }
      }
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
