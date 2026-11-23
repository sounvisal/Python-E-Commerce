import { defineStore } from 'pinia'

const STORAGE_KEY = 'lumea_read_notifications'

function getInitialReadIds() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export const useAtelierNotificationStore = defineStore('atelierNotifications', {
  state: () => ({
    isDrawerOpen: false,
    activeFilter: 'all', // 'all' | 'events' | 'purchases'
    readIds: getInitialReadIds(),
    notifications: [
      {
        id: 'notif-event-summer',
        type: 'event',
        tag: 'Atelier Event',
        badgeColor: 'terracotta',
        title: 'Luméa Grand Summer Solstice Event',
        message: 'Curated 20% privilege across all antioxidant serums, soothing essences, and broad-spectrum sunscreens. Complimentary botanical samples with all orders.',
        time: 'Just now',
        link: '/deals',
        linkText: 'Explore Event Deals',
      },
      {
        id: 'notif-buy-phnom-penh',
        type: 'purchase',
        tag: 'Just Purchased',
        badgeColor: 'emerald',
        title: 'Recent Purchase · Phnom Penh',
        message: 'Sreynich C. just purchased SK-II Facial Treatment Essence (230ml).',
        time: '4 minutes ago',
        link: '/product/sk-ii-facial-treatment-essence',
        linkText: 'View Formulation',
        productImage: '/images/prod-essence.jpg',
      },
      {
        id: 'notif-story-masterclass',
        type: 'event',
        tag: 'Atelier Journal',
        badgeColor: 'gold',
        title: 'New Dermatological Masterclass',
        message: '"Mineral vs. Chemical Sunscreens" & "Skin Barrier Repair" clinical deep dives are now published with complete ingredient breakdowns.',
        time: '2 hours ago',
        link: '/articles/mineral-vs-chemical-sunscreen-the-ultimate-dermatology-guide',
        linkText: 'Read Masterclass',
      },
      {
        id: 'notif-buy-siem-reap',
        type: 'purchase',
        tag: 'Just Purchased',
        badgeColor: 'emerald',
        title: 'Recent Purchase · Siem Reap',
        message: 'Sophea M. just ordered La Roche-Posay Anthelios UVmune 400 SPF 50+ Invisible Fluid.',
        time: '18 minutes ago',
        link: '/product/la-roche-posay-anthelios-uvmune-400',
        linkText: 'View Formulation',
        productImage: '/images/prod-anthelios.jpg',
      },
      {
        id: 'notif-buy-battambang',
        type: 'purchase',
        tag: 'Just Purchased',
        badgeColor: 'emerald',
        title: 'Recent Purchase · Battambang',
        message: 'Dara K. added Innisfree Green Tea Seed Hyaluronic Serum & Balancing Toner.',
        time: '35 minutes ago',
        link: '/product/innisfree-green-tea-seed-serum',
        linkText: 'View Formulation',
        productImage: '/images/prod-greentea-serum.jpg',
      },
      {
        id: 'notif-event-quiz',
        type: 'event',
        tag: 'Diagnostic Routine',
        badgeColor: 'terracotta',
        title: 'Personalized Skin Regimen Matching',
        message: 'Updated 5-step diagnostic quiz now matches formulations to specific skin barrier concerns and daily UV exposure levels.',
        time: '1 day ago',
        link: '/quiz',
        linkText: 'Start Skin Quiz',
      },
      {
        id: 'notif-buy-kampot',
        type: 'purchase',
        tag: 'Just Purchased',
        badgeColor: 'emerald',
        title: 'Recent Purchase · Kampot',
        message: 'Chenda V. just claimed The Ordinary Niacinamide 10% + Zinc 1% (60ml).',
        time: '2 hours ago',
        link: '/product/the-ordinary-niacinamide-10-zinc-1',
        linkText: 'View Formulation',
        productImage: '/images/prod-ordinary-niacinamide.jpg',
      },
    ],
  }),

  getters: {
    unreadCount(state) {
      return state.notifications.filter((n) => !state.readIds.includes(n.id)).length
    },

    filteredNotifications(state) {
      if (state.activeFilter === 'events') {
        return state.notifications.filter((n) => n.type === 'event' || n.type === 'story')
      }
      if (state.activeFilter === 'purchases') {
        return state.notifications.filter((n) => n.type === 'purchase')
      }
      return state.notifications
    },
  },

  actions: {
    openDrawer() {
      this.isDrawerOpen = true
    },

    closeDrawer() {
      this.isDrawerOpen = false
    },

    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen
    },

    setFilter(filter) {
      this.activeFilter = filter
    },

    markAsRead(id) {
      if (!this.readIds.includes(id)) {
        this.readIds.push(id)
        this.persistReadIds()
      }
    },

    markAllAsRead() {
      this.readIds = this.notifications.map((n) => n.id)
      this.persistReadIds()
    },

    addLivePurchase(customerName, city, productName, productSlug, productImage) {
      const id = `notif-live-${Date.now()}`
      this.notifications.unshift({
        id,
        type: 'purchase',
        tag: 'Just Purchased',
        badgeColor: 'emerald',
        title: `Recent Purchase · ${city}`,
        message: `${customerName} just placed an order for ${productName}.`,
        time: 'Just now',
        link: `/product/${productSlug}`,
        linkText: 'View Formulation',
        productImage: productImage || '/images/prod-essence.jpg',
      })
    },

    persistReadIds() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.readIds))
      } catch (e) {
        console.warn('Could not persist read notification IDs', e)
      }
    },
  },
})
