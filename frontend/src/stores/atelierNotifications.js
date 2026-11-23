import axios from 'axios'
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
    notifications: [],
    isLoading: false,
    hasLoaded: false,
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
    async fetchNotifications() {
      this.isLoading = true
      try {
        const { data } = await axios.get('/api/notifications')
        if (data?.status === 'success' && Array.isArray(data?.data)) {
          this.notifications = data.data
          this.hasLoaded = true
        }
      } catch (err) {
        console.warn('Could not load live notifications from backend', err)
      } finally {
        this.isLoading = false
      }
    },

    openDrawer() {
      this.isDrawerOpen = true
      this.fetchNotifications()
    },

    closeDrawer() {
      this.isDrawerOpen = false
    },

    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen
      if (this.isDrawerOpen) {
        this.fetchNotifications()
      }
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
