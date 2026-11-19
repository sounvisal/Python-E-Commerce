import axios from 'axios'
import { defineStore } from 'pinia'
import { safeGetJSON, safeSetJSON } from '@/utils/storage'

function calculateHaversineKm(lat1, lon1, lat2, lon2) {
  if (!lat1 || !lon1 || !lat2 || !lon2) return 6.5
  const R = 6371.0
  const dLat = ((lat2 - lat1) * Math.PI) / 180.0
  const dLon = ((lon2 - lon1) * Math.PI) / 180.0
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180.0) *
      Math.cos((lat2 * Math.PI) / 180.0) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return Math.round(R * c * 10) / 10
}

const ATELIER_LAT = 11.5564
const ATELIER_LNG = 104.9282

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: safeGetJSON('lumea_cart', []),
    isDrawerOpen: false,
    discountCode: localStorage.getItem('lumea_discount_code') || '',
    discountRate: parseFloat(localStorage.getItem('lumea_discount_rate') || '0'),
    freeShippingEnabled: true,
    freeShippingMode: 'threshold', // 'threshold' | 'all_orders' | 'disabled'
    freeShippingThreshold: 50.0,
    freeShippingPromoText: 'Complimentary nationwide shipping on orders over $50',
    freeShippingCarriers: ['vet_express', 'jt_express', 'lumea_concierge'],
    grabSubsidyEnabled: true,
    taxRate: 10.0,
    standardShippingFee: 1.50,
    shippingCity: 'Phnom Penh',
    deliveryLat: null,
    deliveryLng: null,
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

    isPhnomPenh: (state) => {
      const c = (state.shippingCity || 'Phnom Penh').trim().toLowerCase()
      return c.includes('phnom penh') || c.includes('khan') || c.includes('bkk') || c.includes('chamkarmon') || c.includes('daun penh') || c.includes('toul kork') || c.includes('sen sok') || c.includes('pou senchey')
    },

    grabDistanceKm: (state) => {
      if (!state.deliveryLat || !state.deliveryLng) return 6.5
      return calculateHaversineKm(ATELIER_LAT, ATELIER_LNG, state.deliveryLat, state.deliveryLng)
    },

    // Whether free delivery condition is fulfilled based on active admin settings
    isFreeDeliveryActive: (state) => {
      if (!state.freeShippingEnabled || state.freeShippingMode === 'disabled') return false
      if (state.freeShippingMode === 'all_orders') return true
      if (state.freeShippingMode === 'threshold') {
        const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
        return sub >= state.freeShippingThreshold
      }
      return false
    },

    // Amount remaining to qualify for free shipping in threshold mode
    freeDeliveryRemaining: (state) => {
      if (!state.freeShippingEnabled || state.freeShippingMode !== 'threshold') return 0
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      return Math.max(0, Math.round((state.freeShippingThreshold - sub) * 100) / 100)
    },

    // Authentic dynamic tariffs for all 4 couriers
    carrierQuoteMap: (state) => {
      const c = (state.shippingCity || 'Phnom Penh').trim().toLowerCase()
      const isPP = c.includes('phnom penh') || c.includes('khan') || c.includes('bkk') || c.includes('chamkarmon') || c.includes('daun penh') || c.includes('toul kork') || c.includes('sen sok') || c.includes('pou senchey')

      const isEligible = (carrierId) => {
        if (!state.isFreeDeliveryActive) return false
        return (state.freeShippingCarriers || []).includes(carrierId)
      }

      // 1. Vireak Buntham (VET Logistics) - Flat $1.50 Nationwide
      const vetBase = 1.50
      const vetIsFree = isEligible('vet_express')
      const vetFee = vetIsFree ? 0.0 : vetBase

      // 2. J&T Express Cambodia - Flat $1.75 Nationwide
      const jtBase = 1.75
      const jtIsFree = isEligible('jt_express')
      const jtFee = jtIsFree ? 0.0 : jtBase

      // 3. GrabExpress (Grab) - Phnom Penh Only & Distance-Based
      let grabAvailable = isPP
      let grabDistance = 6.5
      let grabBase = 3.50
      let grabFee = 3.50
      let grabTransit = '60–90 Mins (Phnom Penh)'

      if (isPP) {
        grabDistance = calculateHaversineKm(ATELIER_LAT, ATELIER_LNG, state.deliveryLat, state.deliveryLng)
        grabBase = Math.round((2.00 + Math.max(0, grabDistance - 3.0) * 0.40) * 100) / 100
        const hasSubsidy = state.isFreeDeliveryActive && state.grabSubsidyEnabled
        grabFee = hasSubsidy ? Math.max(1.50, Math.round((grabBase - 1.50) * 100) / 100) : grabBase
        grabTransit = `60–90 Mins (${grabDistance} km)`
      } else {
        grabAvailable = false
        grabBase = 0.0
        grabFee = 0.0
        grabTransit = 'Phnom Penh Only'
      }

      // 4. Luméa Atelier Concierge - Flat $3.00
      const conciergeBase = 3.00
      const conciergeIsFree = isEligible('lumea_concierge')
      const conciergeFee = conciergeIsFree ? 0.0 : conciergeBase

      return {
        vet_express: {
          fee: vetFee,
          baseFee: vetBase,
          transit: isPP ? '1 Business Day' : '1–2 Business Days',
          available: true,
          isFree: vetIsFree,
          logo: '/images/couriers/vet_express.png'
        },
        jt_express: {
          fee: jtFee,
          baseFee: jtBase,
          transit: 'Next-Day Delivery',
          available: true,
          isFree: jtIsFree,
          logo: '/images/couriers/jt_express.png'
        },
        grab_express: {
          fee: grabFee,
          baseFee: grabBase,
          transit: grabTransit,
          available: grabAvailable,
          isFree: false,
          distanceKm: grabDistance,
          logo: '/images/couriers/grab_express.png'
        },
        lumea_concierge: {
          fee: conciergeFee,
          baseFee: conciergeBase,
          transit: 'White-Glove Scheduled',
          available: true,
          isFree: conciergeIsFree,
          logo: null
        }
      }
    },

    shippingFee: (state) => {
      const sub = state.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      if (sub === 0) return 0
      const quote = state.carrierQuoteMap[state.selectedCarrier]
      if (quote && quote.available) {
        return quote.fee
      }
      return state.carrierQuoteMap['vet_express'].fee
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
      const shipping = sub === 0 ? 0 : state.carrierQuoteMap[state.selectedCarrier]?.fee ?? 1.50
      return Math.max(0, Math.round((sub - discount + shipping) * 100) / 100)
    },
  },

  actions: {
    saveToStorage() {
      safeSetJSON('lumea_cart', this.items)
      localStorage.setItem('lumea_discount_code', this.discountCode)
      localStorage.setItem('lumea_discount_rate', this.discountRate.toString())
    },

    setDeliveryDestination({ city, lat, lng }) {
      if (city) this.shippingCity = city
      if (lat !== undefined) this.deliveryLat = lat
      if (lng !== undefined) this.deliveryLng = lng
      // If GrabExpress was selected but destination is provincial, switch to VET Logistics
      if (this.selectedCarrier === 'grab_express' && (this.shippingCity || '').toLowerCase() !== 'phnom penh') {
        this.selectedCarrier = 'vet_express'
      }
    },

    setCarrier(carrierId) {
      this.selectedCarrier = carrierId
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
          if (d.free_shipping_enabled !== undefined) {
            this.freeShippingEnabled = Boolean(d.free_shipping_enabled)
          }
          if (d.free_shipping_mode !== undefined) {
            this.freeShippingMode = d.free_shipping_mode
          }
          if (d.free_shipping_threshold !== undefined) {
            this.freeShippingThreshold = Number(d.free_shipping_threshold)
          }
          if (d.free_shipping_promo_text !== undefined) {
            this.freeShippingPromoText = d.free_shipping_promo_text
          }
          if (d.free_shipping_carriers !== undefined) {
            this.freeShippingCarriers = d.free_shipping_carriers
          }
          if (d.grab_subsidy_enabled !== undefined) {
            this.grabSubsidyEnabled = Boolean(d.grab_subsidy_enabled)
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
