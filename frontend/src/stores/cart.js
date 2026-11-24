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

const ATELIER_LAT = 10.6106068
const ATELIER_LNG = 104.1815019

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
    freeShippingCarriers: ['lumea_concierge', 'vet_express', 'jt_express'],
    grabSubsidyEnabled: true,
    taxRate: 10.0,
    standardShippingFee: 1.00,
    shippingCity: 'Kampot',
    deliveryLat: null,
    deliveryLng: null,
    selectedCarrier: 'lumea_concierge',
    settingsLoaded: false,
    announcementEnabled: true,
    announcementText: 'Complimentary nationwide shipping on orders over $50 | 100% Authentic Guaranteed',
    storeName: 'Luméa',
    storeEmail: 'support@lumea.com',
    storePhone: '+855 12 345 678',
    maintenanceMode: false,
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

    isSameCity: (state) => {
      const c = (state.shippingCity || 'Kampot').trim().toLowerCase()
      return c.includes('kampot') || c.includes('krong kampot') || c.includes('teuk chhou') || c.includes('chhouk')
    },

    grabDistanceKm: (state) => {
      if (!state.deliveryLat || !state.deliveryLng) return 4.5
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
      const c = (state.shippingCity || 'Kampot').trim().toLowerCase()
      const isLocal = c.includes('kampot') || c.includes('krong kampot') || c.includes('teuk chhou') || c.includes('chhouk')

      const isEligible = (carrierId) => {
        if (!state.isFreeDeliveryActive) return false
        return (state.freeShippingCarriers || []).includes(carrierId)
      }

      // 1. Luméa Shop Direct Delivery (Atelier Messenger) - Flat $1.00 (Cheapest, Most Realistic Shop Delivery!)
      const conciergeBase = 1.00
      const conciergeIsFree = isEligible('lumea_concierge')
      const conciergeFee = conciergeIsFree ? 0.0 : conciergeBase

      // 2. Vireak Buntham (VET Logistics) - Flat $1.50 Nationwide
      const vetBase = 1.50
      const vetIsFree = isEligible('vet_express')
      const vetFee = vetIsFree ? 0.0 : vetBase

      // 3. J&T Express Cambodia - Flat $1.75 Nationwide
      const jtBase = 1.75
      const jtIsFree = isEligible('jt_express')
      const jtFee = jtIsFree ? 0.0 : jtBase

      // 4. GrabExpress (Grab) - Same Province / City Only (Kampot) & GPS Distance-Based
      let grabAvailable = isLocal
      let grabDistance = 4.5
      let grabBase = 2.50
      let grabFee = 2.50
      let grabTransit = '30–60 Mins (Kampot On-Demand)'

      if (isLocal) {
        grabDistance = calculateHaversineKm(ATELIER_LAT, ATELIER_LNG, state.deliveryLat, state.deliveryLng)
        // Base $1.50 for first 3km, then $0.35 per additional km
        grabBase = Math.round((1.50 + Math.max(0, grabDistance - 3.0) * 0.35) * 100) / 100
        const hasSubsidy = state.isFreeDeliveryActive && state.grabSubsidyEnabled
        grabFee = hasSubsidy ? Math.max(1.00, Math.round((grabBase - 1.00) * 100) / 100) : grabBase
        grabTransit = `30–60 Mins (${grabDistance} km)`
      } else {
        grabAvailable = false
        grabBase = 0.0
        grabFee = 0.0
        grabTransit = 'Same City/Province Only (Kampot)'
      }

      return {
        lumea_concierge: {
          fee: conciergeFee,
          baseFee: conciergeBase,
          transit: isLocal ? 'Same-Day Direct Delivery' : '1–2 Business Days Direct',
          available: true,
          isFree: conciergeIsFree,
          badge: 'Shop Best Value',
          logo: null
        },
        vet_express: {
          fee: vetFee,
          baseFee: vetBase,
          transit: isLocal ? '1 Business Day' : '1–2 Business Days',
          available: true,
          isFree: vetIsFree,
          badge: 'Nationwide #1',
          logo: '/images/couriers/vet_express.png'
        },
        jt_express: {
          fee: jtFee,
          baseFee: jtBase,
          transit: 'Next-Day Delivery',
          available: true,
          isFree: jtIsFree,
          badge: 'Fast Domestic',
          logo: '/images/couriers/jt_express.png'
        },
        grab_express: {
          fee: grabFee,
          baseFee: grabBase,
          transit: grabTransit,
          available: grabAvailable,
          isFree: false,
          badge: 'Instant Express',
          distanceKm: grabDistance,
          logo: '/images/couriers/grab_express.png'
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
      return state.carrierQuoteMap['lumea_concierge'].fee
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
      const shipping = sub === 0 ? 0 : state.carrierQuoteMap[state.selectedCarrier]?.fee ?? 1.00
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
      // If GrabExpress was selected but destination is not in same city/province, switch to Luméa Shop Direct ($1.00)
      const isLocal = (this.shippingCity || '').toLowerCase().includes('kampot')
      if (this.selectedCarrier === 'grab_express' && !isLocal) {
        this.selectedCarrier = 'lumea_concierge'
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
          if (d.announcement_enabled !== undefined) {
            this.announcementEnabled = Boolean(d.announcement_enabled)
          }
          if (d.announcement_text !== undefined) {
            this.announcementText = d.announcement_text
          }
          if (d.store_name) {
            this.storeName = d.store_name
          }
          if (d.store_email) {
            this.storeEmail = d.store_email
          }
          if (d.store_phone) {
            this.storePhone = d.store_phone
          }
          if (d.maintenance_mode !== undefined) {
            this.maintenanceMode = Boolean(d.maintenance_mode)
          }
          this.settingsLoaded = true
        }
      } catch (err) {
        // Fallback silently to defaults
      }
    },
  },
})
