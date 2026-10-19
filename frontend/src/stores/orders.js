import axios from 'axios'
import { defineStore } from 'pinia'
import { useCartStore } from './cart'
import { useNotificationStore } from './notification'

const MOCK_ORDERS = [
  {
    orderNumber: 'LM250616789',
    placedAt: 'Jun 16, 2025 at 10:24 AM',
    date: '2025-06-16',
    status: 'Delivered',
    statusText: 'Delivered on Jun 19, 2025',
    statusType: 'delivered', // delivered, shipped, processing, cancelled
    total: 156.80,
    subtotal: 156.80,
    shippingFee: 0.00,
    tax: 0.00,
    rewardPointsEarned: 156,
    deliveryMethod: 'Standard Delivery (3 – 5 business days)',
    deliveredAt: 'Jun 19, 2025',
    shippingAddress: {
      name: 'Sreynich Chan',
      address: '#123, Street 271, Sangkat Boeung Tumpun, Khan Meanchey',
      city: 'Phnom Penh 12000, Cambodia',
      phone: '+855 12 345 678',
    },
    paymentMethod: {
      provider: 'ABA Pay',
      details: 'Paid on Jun 16, 2025 at 10:24 AM',
      amount: 156.80,
    },
    timeline: [
      { step: 'Order Placed', date: 'Jun 16, 2025', time: '10:24 AM', completed: true },
      { step: 'Processing', date: 'Jun 16, 2025', time: '02:15 PM', completed: true },
      { step: 'Shipped', date: 'Jun 17, 2025', time: '09:20 AM', completed: true },
      { step: 'Out for Delivery', date: 'Jun 19, 2025', time: '08:12 AM', completed: true },
      { step: 'Delivered', date: 'Jun 19, 2025', time: '02:46 PM', completed: true },
    ],
    items: [
      {
        id: 101,
        name: 'SK-II Facial Treatment Essence',
        volume: '230 ml',
        price: 99.00,
        qty: 1,
        total: 99.00,
        image_url: '/images/prod-sk2.jpg',
        slug: 'sk-ii-facial-treatment-essence',
      },
      {
        id: 103,
        name: 'Laneige Lip Sleeping Mask',
        volume: '20 g',
        price: 24.00,
        qty: 1,
        total: 24.00,
        image_url: '/images/prod-laneige.jpg',
        slug: 'laneige-lip-sleeping-mask',
      },
      {
        id: 102,
        name: 'The Ordinary Niacinamide 10% + Zinc 1%',
        volume: '30 ml',
        price: 17.80,
        qty: 1,
        total: 17.80,
        image_url: '/images/prod-ordinary.jpg',
        slug: 'the-ordinary-niacinamide-10-zinc-1',
      },
      {
        id: 104,
        name: 'CeraVe Hydrating Facial Cleanser',
        volume: '236 ml',
        price: 16.00,
        qty: 1,
        total: 16.00,
        image_url: '/images/prod-cerave-cleanser.jpg',
        slug: 'cerave-hydrating-cleanser',
      },
    ],
  },
  {
    orderNumber: 'LM250528443',
    placedAt: 'May 28, 2025 at 02:15 PM',
    date: '2025-05-28',
    status: 'Out for Delivery',
    statusText: 'Estimated delivery May 30, 2025',
    statusType: 'shipped',
    total: 89.50,
    subtotal: 89.50,
    shippingFee: 0.00,
    tax: 0.00,
    rewardPointsEarned: 89,
    deliveryMethod: 'Standard Delivery (3 – 5 business days)',
    deliveredAt: 'Estimated May 30, 2025',
    shippingAddress: {
      name: 'Sreynich Chan',
      address: '#123, Street 271, Sangkat Boeung Tumpun, Khan Meanchey',
      city: 'Phnom Penh 12000, Cambodia',
      phone: '+855 12 345 678',
    },
    paymentMethod: {
      provider: 'Mastercard **** 9012',
      details: 'Paid on May 28, 2025 at 02:15 PM',
      amount: 89.50,
    },
    timeline: [
      { step: 'Order Placed', date: 'May 28, 2025', time: '02:15 PM', completed: true },
      { step: 'Processing', date: 'May 28, 2025', time: '04:30 PM', completed: true },
      { step: 'Shipped', date: 'May 29, 2025', time: '08:45 AM', completed: true },
      { step: 'Out for Delivery', date: 'May 30, 2025', time: '09:00 AM', completed: true },
      { step: 'Delivered', date: 'Pending', time: '', completed: false },
    ],
    items: [
      {
        id: 103,
        name: 'Laneige Lip Sleeping Mask',
        volume: '20 g',
        price: 24.00,
        qty: 1,
        total: 24.00,
        image_url: '/images/prod-laneige.jpg',
        slug: 'laneige-lip-sleeping-mask',
      },
      {
        id: 102,
        name: 'The Ordinary Niacinamide 10% + Zinc 1%',
        volume: '30 ml',
        price: 17.80,
        qty: 1,
        total: 17.80,
        image_url: '/images/prod-ordinary.jpg',
        slug: 'the-ordinary-niacinamide-10-zinc-1',
      },
      {
        id: 502,
        name: 'innisfree Green Tea Seed Serum',
        volume: '80 ml',
        price: 47.70,
        qty: 1,
        total: 47.70,
        image_url: '/images/prod-innisfree-cleanser.jpg',
        slug: 'innisfree-green-tea-seed-serum',
      },
    ],
  },
  {
    orderNumber: 'LM250512301',
    placedAt: 'May 12, 2025 at 11:07 AM',
    date: '2025-05-12',
    status: 'Preparing',
    statusText: "We're getting your order ready.",
    statusType: 'processing',
    total: 42.00,
    subtotal: 42.00,
    shippingFee: 0.00,
    tax: 0.00,
    rewardPointsEarned: 42,
    deliveryMethod: 'Express Courier Delivery',
    deliveredAt: 'Pending dispatch',
    shippingAddress: {
      name: 'Sreynich Chan',
      address: '#123, Street 271, Sangkat Boeung Tumpun, Khan Meanchey',
      city: 'Phnom Penh 12000, Cambodia',
      phone: '+855 12 345 678',
    },
    paymentMethod: {
      provider: 'ABA Pay',
      details: 'Paid on May 12, 2025 at 11:07 AM',
      amount: 42.00,
    },
    timeline: [
      { step: 'Order Placed', date: 'May 12, 2025', time: '11:07 AM', completed: true },
      { step: 'Processing', date: 'May 12, 2025', time: '11:30 AM', completed: true },
      { step: 'Shipped', date: 'Pending', time: '', completed: false },
      { step: 'Out for Delivery', date: 'Pending', time: '', completed: false },
      { step: 'Delivered', date: 'Pending', time: '', completed: false },
    ],
    items: [
      {
        id: 505,
        name: 'Medicube Collagen Jelly Cream',
        volume: '50 ml',
        price: 28.00,
        qty: 1,
        total: 28.00,
        image_url: '/images/prod-laneige.jpg',
        slug: 'medicube-collagen-jelly-cream',
      },
      {
        id: 506,
        name: 'Anua Heartleaf 77% Soothing Toner',
        volume: '150 ml',
        price: 14.00,
        qty: 1,
        total: 14.00,
        image_url: '/images/prod-anua-cleanser.jpg',
        slug: 'anua-heartleaf-77-toner',
      },
    ],
  },
  {
    orderNumber: 'LM250428776',
    placedAt: 'Apr 28, 2025 at 09:30 AM',
    date: '2025-04-28',
    status: 'Cancelled',
    statusText: 'Cancelled on Apr 29, 2025',
    statusType: 'cancelled',
    total: 68.00,
    subtotal: 68.00,
    shippingFee: 0.00,
    tax: 0.00,
    rewardPointsEarned: 0,
    deliveryMethod: 'Standard Delivery',
    deliveredAt: 'Cancelled',
    shippingAddress: {
      name: 'Sreynich Chan',
      address: '#123, Street 271, Sangkat Boeung Tumpun, Khan Meanchey',
      city: 'Phnom Penh 12000, Cambodia',
      phone: '+855 12 345 678',
    },
    paymentMethod: {
      provider: 'ABA Pay',
      details: 'Refunded on Apr 29, 2025',
      amount: 68.00,
    },
    timeline: [
      { step: 'Order Placed', date: 'Apr 28, 2025', time: '09:30 AM', completed: true },
      { step: 'Cancelled', date: 'Apr 29, 2025', time: '10:15 AM', completed: true },
    ],
    items: [
      {
        id: 104,
        name: 'CeraVe Hydrating Facial Cleanser',
        volume: '236 ml',
        price: 16.00,
        qty: 1,
        total: 16.00,
        image_url: '/images/prod-cerave-cleanser.jpg',
        slug: 'cerave-hydrating-cleanser',
      },
      {
        id: 501,
        name: 'COSRX Advanced Snail 96 Mucin Power Essence',
        volume: '100 ml',
        price: 25.00,
        qty: 1,
        total: 25.00,
        image_url: '/images/prod-cosrx-snail.jpg',
        slug: 'cosrx-snail-96-essence',
      },
      {
        id: 504,
        name: 'TIRTIR Milk Skin Toner',
        volume: '150 ml',
        price: 27.00,
        qty: 1,
        total: 27.00,
        image_url: '/images/prod-anua-toner.jpg',
        slug: 'tirtir-milk-skin-toner',
      },
    ],
  },
  {
    orderNumber: 'LM250410992',
    placedAt: 'Apr 10, 2025 at 04:18 PM',
    date: '2025-04-10',
    status: 'Delivered',
    statusText: 'Delivered on Apr 14, 2025',
    statusType: 'delivered',
    total: 75.20,
    subtotal: 75.20,
    shippingFee: 0.00,
    tax: 0.00,
    rewardPointsEarned: 75,
    deliveryMethod: 'Standard Delivery',
    deliveredAt: 'Apr 14, 2025',
    shippingAddress: {
      name: 'Sreynich Chan',
      address: '#123, Street 271, Sangkat Boeung Tumpun, Khan Meanchey',
      city: 'Phnom Penh 12000, Cambodia',
      phone: '+855 12 345 678',
    },
    paymentMethod: {
      provider: 'ABA Pay',
      details: 'Paid on Apr 10, 2025 at 04:18 PM',
      amount: 75.20,
    },
    timeline: [
      { step: 'Order Placed', date: 'Apr 10, 2025', time: '04:18 PM', completed: true },
      { step: 'Processing', date: 'Apr 11, 2025', time: '09:00 AM', completed: true },
      { step: 'Shipped', date: 'Apr 12, 2025', time: '11:30 AM', completed: true },
      { step: 'Out for Delivery', date: 'Apr 14, 2025', time: '08:00 AM', completed: true },
      { step: 'Delivered', date: 'Apr 14, 2025', time: '03:15 PM', completed: true },
    ],
    items: [
      {
        id: 102,
        name: 'The Ordinary Niacinamide 10% + Zinc 1%',
        volume: '30 ml',
        price: 17.80,
        qty: 1,
        total: 17.80,
        image_url: '/images/prod-ordinary.jpg',
        slug: 'the-ordinary-niacinamide-10-zinc-1',
      },
      {
        id: 103,
        name: 'Laneige Lip Sleeping Mask',
        volume: '20 g',
        price: 24.00,
        qty: 1,
        total: 24.00,
        image_url: '/images/prod-laneige.jpg',
        slug: 'laneige-lip-sleeping-mask',
      },
      {
        id: 106,
        name: 'Beauty of Joseon Relief Sun SPF50+',
        volume: '50 ml',
        price: 17.00,
        qty: 1,
        total: 17.00,
        image_url: '/images/prod-boj.jpg',
        slug: 'beauty-of-joseon-relief-sun',
      },
      {
        id: 104,
        name: 'CeraVe Hydrating Cleanser',
        volume: '236 ml',
        price: 16.40,
        qty: 1,
        total: 16.40,
        image_url: '/images/prod-cerave-cleanser.jpg',
        slug: 'cerave-hydrating-cleanser',
      },
    ],
  },
]

export const useOrdersStore = defineStore('orders', {
  state: () => {
    const saved = localStorage.getItem('lumea_orders')
    return {
      orders: saved ? JSON.parse(saved) : [...MOCK_ORDERS],
    }
  },

  getters: {
    totalOrders: (state) => state.orders.length,
    processingOrders: (state) => state.orders.filter((o) => o.statusType === 'processing'),
    shippedOrders: (state) => state.orders.filter((o) => o.statusType === 'shipped'),
    deliveredOrders: (state) => state.orders.filter((o) => o.statusType === 'delivered'),
    cancelledOrders: (state) => state.orders.filter((o) => o.statusType === 'cancelled'),
    recentOrders: (state) => state.orders.slice(0, 3),
    getOrderById: (state) => (orderNumber) => {
      const cleanNum = String(orderNumber).replace('#', '').trim()
      return state.orders.find((o) => o.orderNumber === cleanNum) || state.orders[0]
    },
  },

  actions: {
    saveToStorage() {
      localStorage.setItem('lumea_orders', JSON.stringify(this.orders))
    },

    async fetchOrders(email = 'sreynich.chan@example.com') {
      try {
        const res = await axios.get('/api/orders', { params: { email } })
        if (res.data && Array.isArray(res.data) && res.data.length > 0) {
          const mapped = res.data.map(o => ({
            orderNumber: o.order_number,
            placedAt: o.created_at ? new Date(o.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recent',
            date: o.created_at ? o.created_at.split('T')[0] : new Date().toISOString().split('T')[0],
            status: o.status || 'Confirmed',
            statusText: `${o.status || 'Confirmed'} · Delivery in 3-5 days`,
            statusType: (o.status || 'confirmed').toLowerCase(),
            total: o.total,
            subtotal: o.subtotal,
            shippingFee: o.shipping_fee,
            tax: 0.0,
            rewardPointsEarned: Math.floor(o.total),
            deliveryMethod: 'Standard Atelier Delivery (3 – 5 days)',
            deliveredAt: o.status === 'Delivered' ? 'Delivered' : 'Estimated in 3 days',
            shippingAddress: {
              name: o.customer_name,
              address: o.shipping_address,
              city: `${o.shipping_city || 'Phnom Penh'} ${o.shipping_postal_code || ''}, Cambodia`,
              phone: o.customer_phone
            },
            paymentMethod: {
              provider: (o.payment_method || 'card').toUpperCase(),
              details: `Paid via ${(o.payment_method || 'card').toUpperCase()}`,
              amount: o.total
            },
            timeline: [
              { step: 'Order Placed', date: 'Confirmed', time: '10:00 AM', completed: true },
              { step: 'Processing', date: o.status !== 'Pending' ? 'Active' : 'Pending', time: '11:00 AM', completed: o.status !== 'Pending' },
              { step: 'Shipped', date: ['Shipped', 'Delivered'].includes(o.status) ? 'In Transit' : 'Pending', time: '02:00 PM', completed: ['Shipped', 'Delivered'].includes(o.status) },
              { step: 'Delivered', date: o.status === 'Delivered' ? 'Completed' : 'Pending', time: '04:00 PM', completed: o.status === 'Delivered' }
            ],
            items: (o.items || []).map(item => ({
              id: item.product_id || 201,
              name: item.product_name,
              volume: 'Standard Size',
              price: item.price,
              qty: item.quantity,
              total: item.total,
              image_url: item.image_url || '/images/prod-sk2.jpg',
              slug: item.product_name.toLowerCase().replace(/\s+/g, '-')
            }))
          }))

          const existingIds = new Set(mapped.map(m => m.orderNumber))
          const existingRemaining = this.orders.filter(o => !existingIds.has(o.orderNumber))
          this.orders = [...mapped, ...existingRemaining]
          this.saveToStorage()
        }
      } catch (err) {
        console.warn('Could not fetch backend orders, using stored orders:', err)
      }
    },

    async fetchOrderByNumber(orderNumber) {
      if (!orderNumber) return null
      const cleanNum = String(orderNumber).replace('#', '').trim()
      try {
        const res = await axios.get(`/api/orders/${cleanNum}`)
        if (res.data?.data) {
          const o = res.data.data
          const mapped = {
            orderNumber: o.order_number,
            placedAt: o.created_at ? new Date(o.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Recent',
            date: o.created_at ? o.created_at.split('T')[0] : new Date().toISOString().split('T')[0],
            status: o.status || 'Confirmed',
            statusText: o.status === 'Delivered' ? 'Delivered successfully' : `${o.status || 'Confirmed'} · Delivery in 3-5 days`,
            statusType: (o.status || 'confirmed').toLowerCase(),
            total: o.total,
            subtotal: o.subtotal,
            shippingFee: o.shipping_fee,
            tax: 0.0,
            rewardPointsEarned: Math.floor(o.total),
            deliveryMethod: 'Standard Atelier Delivery (3 – 5 days)',
            deliveredAt: o.status === 'Delivered' ? 'Delivered' : 'Estimated in 3 days',
            shippingAddress: {
              name: o.customer_name,
              address: o.shipping_address,
              city: `${o.shipping_city || 'Phnom Penh'} ${o.shipping_postal_code || ''}, Cambodia`,
              phone: o.customer_phone
            },
            paymentMethod: {
              provider: (o.payment_method || 'card').toUpperCase(),
              details: `Paid via ${(o.payment_method || 'card').toUpperCase()}`,
              amount: o.total
            },
            timeline: [
              { step: 'Order Placed', date: 'Confirmed', time: '10:00 AM', completed: true },
              { step: 'Processing', date: o.status !== 'Pending' ? 'Active' : 'Pending', time: '11:00 AM', completed: o.status !== 'Pending' },
              { step: 'Shipped', date: ['Shipped', 'Out for Delivery', 'Delivered'].includes(o.status) ? 'In Transit' : 'Pending', time: '02:00 PM', completed: ['Shipped', 'Out for Delivery', 'Delivered'].includes(o.status) },
              { step: 'Out for Delivery', date: ['Out for Delivery', 'Delivered'].includes(o.status) ? 'Out for Delivery' : 'Pending', time: '08:30 AM', completed: ['Out for Delivery', 'Delivered'].includes(o.status) },
              { step: 'Delivered', date: o.status === 'Delivered' ? 'Completed' : 'Pending', time: '04:00 PM', completed: o.status === 'Delivered' }
            ],
            items: (o.items || []).map(item => ({
              id: item.product_id || 201,
              name: item.product_name,
              volume: 'Standard Size',
              price: item.price,
              qty: item.quantity,
              total: item.total,
              image_url: item.image_url || '/images/prod-sk2.jpg',
              slug: item.product_name.toLowerCase().replace(/\s+/g, '-')
            }))
          }

          const idx = this.orders.findIndex(x => x.orderNumber === cleanNum)
          if (idx !== -1) {
            this.orders[idx] = mapped
          } else {
            this.orders.unshift(mapped)
          }
          this.saveToStorage()
          return mapped
        }
      } catch (err) {
        console.warn(`Could not fetch backend order ${cleanNum}:`, err)
      }
      return this.getOrderById(cleanNum)
    },

    addOrder(order) {
      if (!order) return
      const mapped = {
        orderNumber: order.order_number,
        placedAt: 'Just now',
        date: new Date().toISOString().split('T')[0],
        status: order.status || 'Confirmed',
        statusText: `${order.status || 'Confirmed'} · Delivery in 3-5 days`,
        statusType: (order.status || 'confirmed').toLowerCase(),
        total: order.total,
        subtotal: order.subtotal,
        shippingFee: order.shipping_fee,
        tax: 0.0,
        rewardPointsEarned: Math.floor(order.total),
        deliveryMethod: 'Standard Atelier Delivery (3 – 5 days)',
        deliveredAt: 'Estimated in 3 days',
        shippingAddress: {
          name: order.customer_name,
          address: order.shipping_address,
          city: `${order.shipping_city} ${order.shipping_postal_code || ''}, Cambodia`,
          phone: order.customer_phone
        },
        paymentMethod: {
          provider: (order.payment_method || 'card').toUpperCase(),
          details: `Paid via ${(order.payment_method || 'card').toUpperCase()}`,
          amount: order.total
        },
        timeline: [
          { step: 'Order Placed', date: 'Just now', time: '10:00 AM', completed: true },
          { step: 'Processing', date: 'Active', time: '11:00 AM', completed: true },
          { step: 'Shipped', date: 'Pending', time: '', completed: false },
          { step: 'Delivered', date: 'Pending', time: '', completed: false }
        ],
        items: (order.items || []).map(item => ({
          id: item.product_id || 201,
          name: item.product_name,
          volume: 'Standard Size',
          price: item.price,
          qty: item.quantity,
          total: item.total,
          image_url: item.image_url || '/images/prod-sk2.jpg',
          slug: item.product_name.toLowerCase().replace(/\s+/g, '-')
        }))
      }
      this.orders.unshift(mapped)
      this.saveToStorage()
    },

    cancelOrder(orderNumber) {
      const notificationStore = useNotificationStore()
      const order = this.orders.find((o) => o.orderNumber === orderNumber)
      if (order && order.statusType === 'processing') {
        order.status = 'Cancelled'
        order.statusText = `Cancelled on ${new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`
        order.statusType = 'cancelled'
        this.saveToStorage()
        notificationStore.addToast(`Order #${orderNumber} has been cancelled.`, 'info')
        return true
      }
      return false
    },

    reorder(orderNumber) {
      const cartStore = useCartStore()
      const notificationStore = useNotificationStore()
      const order = this.orders.find((o) => o.orderNumber === orderNumber)
      if (order) {
        order.items.forEach((item) => {
          cartStore.addItem({
            id: item.id,
            name: item.name,
            brand: item.brand || 'Luméa Curated',
            price: item.price,
            image_url: item.image_url,
            slug: item.slug,
          })
        })
        notificationStore.addToast(`Added ${order.items.length} items from Order #${orderNumber} to cart!`, 'success')
        cartStore.openDrawer()
      }
    },
  },
})
