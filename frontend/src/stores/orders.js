import axios from 'axios'
import { defineStore } from 'pinia'
import { useCartStore } from './cart'
import { useProductStore } from './products'
import { useNotificationStore } from './notification'
import { orderRequest, rememberOrderAccess } from '@/utils/orderAccess'

function mapOrder(o) {
  const events = o.events?.length ? o.events : [{ status: 'Order Placed', at: o.created_at }]
  const carrierNames = {
    vet_express: 'Vireak Buntham (VET Logistics)',
    jt_express: 'J&T Express Cambodia',
    grab_express: 'GrabExpress On-Demand',
    lumea_concierge: 'Luméa Shop Direct Delivery',
  }
  const carrierName = carrierNames[o.shipping_carrier] || 'Vireak Buntham (VET Logistics)'
  const mapUrl = o.map_url || (o.delivery_lat && o.delivery_lng ? `https://www.google.com/maps?q=${o.delivery_lat},${o.delivery_lng}` : null)
  const calcShipping = (typeof o.shipping_fee === 'number' && o.shipping_fee > 0)
    ? o.shipping_fee
    : Math.max(0, Math.round(((o.total || 0) - (o.subtotal || 0) + (o.discount || 0)) * 100) / 100)
  return {
    userId: o.user_id, orderNumber: o.order_number, placedAt: new Date(o.created_at).toLocaleString(),
    date: o.created_at, status: o.status, statusType: o.status.toLowerCase(), paymentStatus: o.payment_status,
    statusText: `${o.status} · ${o.payment_status}`, total: o.total, subtotal: o.subtotal, discount: o.discount,
    discountCode: o.discount_code,
    shippingFee: calcShipping, tax: 0, rewardPointsEarned: o.payment_status === 'Paid' ? Math.floor(o.total) : 0,
    shippingCarrier: o.shipping_carrier || 'vet_express',
    deliveryMethod: carrierName,
    deliveredAt: o.delivered_at || '',
    deliveryLat: o.delivery_lat,
    deliveryLng: o.delivery_lng,
    deliveryNotes: o.delivery_notes,
    mapUrl: mapUrl,
    shippingAddress: { name: o.customer_name, address: o.shipping_address, city: o.shipping_city, phone: o.customer_phone },
    paymentMethod: { provider: (o.payment_method || 'card').toUpperCase(), details: o.payment_status, amount: o.total },
    timeline: events.map(event => ({ step: event.status, date: event.at ? new Date(event.at).toLocaleDateString() : '', time: event.at ? new Date(event.at).toLocaleTimeString() : '', completed: true })),
    items: (o.items || []).map(item => ({ id: item.product_id, orderItemId: item.id, name: item.product_name,
      volume: 'Standard size', price: item.price, qty: item.quantity, total: item.total, image_url: item.image_url,
      slug: useProductStore().allCatalogProducts.find(p => p.id === item.product_id)?.slug || '' })),
  }
}
export const useOrdersStore = defineStore('orders', {
  state: () => ({ orders: [], loading: false, error: '' }),
  getters: {
    totalOrders: s => s.orders.length,
    processingOrders: s => s.orders.filter(o => ['pending', 'confirmed', 'processing'].includes(o.statusType)),
    shippedOrders: s => s.orders.filter(o => ['shipped', 'out for delivery'].includes(o.statusType)),
    deliveredOrders: s => s.orders.filter(o => o.statusType === 'delivered'),
    cancelledOrders: s => s.orders.filter(o => o.statusType === 'cancelled'),
    recentOrders: s => s.orders.slice(0, 3),
    getOrderById: s => number => s.orders.find(o => o.orderNumber === String(number).replace('#', '').trim()) || null,
  },
  actions: {
    saveToStorage() {}, // private purchases stay in memory and are reloaded from the API
    async fetchOrders() {
      this.loading = true; this.error = ''; this.orders = []
      try { this.orders = (await axios.get('/api/orders')).data.map(mapOrder); return true }
      catch (e) { this.error = e.response?.data?.detail || 'Could not load orders.'; return false }
      finally { this.loading = false }
    },
    async fetchOrderByNumber(number) {
      this.loading = true; this.error = ''
      this.orders = this.orders.filter(o => o.orderNumber !== number)
      try {
        const { data } = await axios.get(`/api/orders/${number}`, orderRequest(number))
        return this.addOrder(data.data)
      } catch (e) { this.error = e.response?.data?.detail || 'Could not load this order.'; return null }
      finally { this.loading = false }
    },
    addOrder(order) {
      rememberOrderAccess(order)
      const mapped = mapOrder(order)
      this.orders = [mapped, ...this.orders.filter(o => o.orderNumber !== mapped.orderNumber)]
      return mapped
    },
    async cancelOrder(number) {
      try {
        const { data } = await axios.post(`/api/orders/${number}/cancel`, {}, orderRequest(number))
        this.addOrder(data.data)
        useNotificationStore().addToast('Order cancelled.', 'success'); return true
      } catch (e) {
        useNotificationStore().addToast(e.response?.data?.detail || 'Cancellation failed. Your order has not changed.', 'error'); return false
      }
    },
    async reorder(number) {
      const order = this.getOrderById(number)
      if (!order) return
      const products = useProductStore()
      await products.fetchProducts()
      if (products.error) return useNotificationStore().addToast(products.error, 'error')
      let added = 0
      for (const line of order.items) {
        const product = products.allCatalogProducts.find(p => p.id === line.id)
        const already = useCartStore().items.find(p => p.id === line.id)?.quantity || 0
        if (product && product.stock >= line.qty + already) { useCartStore().addItem(product, line.qty); added++ }
      }
      useNotificationStore().addToast(`Added ${added} of ${order.items.length} product lines at current prices. Unavailable quantities were skipped.`, added ? 'success' : 'info')
    },
  },
})
