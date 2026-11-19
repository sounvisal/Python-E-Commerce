import axios from 'axios'
import { defineStore, getActivePinia } from 'pinia'
import { useNotificationStore } from './notification'

function stored(key) {
  try { return sessionStorage.getItem(key) || localStorage.getItem(key) } catch { return null }
}
function mapUser(user) {
  return { ...user, firstName: user.first_name || user.name?.split(' ')[0] || '',
    lastName: user.last_name || '', rewardPoints: user.reward_points ?? 0,
    addresses: user.profile_data?.addresses || [], paymentMethods: [],
    totalOrders: 0, wishlistCount: 0, savedForLaterCount: 0,
    joinedDate: user.created_at ? new Date(user.created_at).toLocaleDateString() : '' }
}
function errorMessage(error, fallback) {
  const detail = error.response?.data?.detail
  return typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map(d => d.msg).join('. ') : fallback
}
function clearPrivateState() {
  for (const key of ['lumea_orders', 'lumea_skin_profile', 'lumea_journal_entries', 'lumea_wishlist']) localStorage.removeItem(key)
  const stores = getActivePinia()?._s
  if (!stores) return
  if (stores.has('orders')) stores.get('orders').orders = []
  if (stores.has('wishlist')) stores.get('wishlist').loadProfile?.()
  if (stores.has('quiz')) stores.get('quiz').loadProfile?.()
  if (stores.has('journal')) stores.get('journal').loadProfile?.()
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    let user = null
    try { user = JSON.parse(stored('lumea_auth_user') || 'null') } catch {}
    const token = stored('lumea_auth_token')
    if (token) axios.defaults.headers.common.Authorization = `Bearer ${token}`
    return { user, token, isAuthenticated: !!(token && user), remember: !!localStorage.getItem('lumea_auth_token'), validated: false }
  },
  getters: {
    userName: s => s.user?.name || 'Guest', userFirstName: s => s.user?.firstName || 'Guest',
    userEmail: s => s.user?.email || '', userAvatar: s => s.user?.avatar || '',
    defaultAddress: s => s.user?.addresses?.find(a => a.isDefault) || s.user?.addresses?.[0],
    defaultPayment: s => s.user?.paymentMethods?.[0],
  },
  actions: {
    persist() {
      for (const storage of [localStorage, sessionStorage]) {
        storage.removeItem('lumea_auth_user'); storage.removeItem('lumea_auth_token')
      }
      if (this.token) {
        const storage = this.remember ? localStorage : sessionStorage
        storage.setItem('lumea_auth_token', this.token)
        storage.setItem('lumea_auth_user', JSON.stringify(this.user))
        axios.defaults.headers.common.Authorization = `Bearer ${this.token}`
      } else delete axios.defaults.headers.common.Authorization
    },
    setSession(data, remember = true) {
      this.user = mapUser(data.user); this.token = data.access_token; this.remember = remember
      this.isAuthenticated = true; this.validated = true; this.persist(); clearPrivateState()
    },
    async ensureSession() {
      if (!this.token) return false
      if (this.validated) return this.isAuthenticated
      try {
        this.user = mapUser((await axios.get('/api/auth/me')).data)
        this.isAuthenticated = true; this.validated = true; this.persist(); return true
      } catch (error) {
        if (error.response?.status === 401 || error.response?.status === 404) this.logout(false)
        return false
      }
    },
    async login({ email, password, remember = true }) {
      try {
        const { data } = await axios.post('/api/auth/login', { email, password })
        if (!data.data?.access_token) throw new Error('Missing session')
        this.setSession(data.data, remember)
        useNotificationStore().addToast(`Welcome back, ${this.user.firstName}!`, 'success')
        return true
      } catch (error) {
        useNotificationStore().addToast(errorMessage(error, 'Sign-in is unavailable. Please try again.'), 'error')
        return false
      }
    },
    async register({ name, email, phone, password }) {
      try {
        const { data } = await axios.post('/api/auth/register', { name, email, phone, password })
        if (!data.data?.access_token) throw new Error('Missing session')
        this.setSession(data.data)
        useNotificationStore().addToast(`Welcome to Luméa, ${this.user.firstName}!`, 'success')
        return true
      } catch (error) {
        useNotificationStore().addToast(errorMessage(error, 'Registration is unavailable. Your account has not been created.'), 'error')
        return false
      }
    },
    logout(notify = true) {
      this.token = null; this.user = null; this.isAuthenticated = false; this.validated = false; this.persist(); clearPrivateState()
      for (const key of Object.keys(sessionStorage)) if (key.startsWith('lumea_order_access_')) sessionStorage.removeItem(key)
      sessionStorage.removeItem('lumea_pending_khqr')
      sessionStorage.removeItem('lumea_checkout_attempt')
      if (notify) useNotificationStore().addToast('You have been signed out.', 'info')
    },
    async updateProfile(updates) {
      try {
        const { data } = await axios.patch('/api/auth/me', updates)
        this.user = mapUser(data); this.persist()
        useNotificationStore().addToast('Profile saved.', 'success')
        return true
      } catch (error) {
        useNotificationStore().addToast(errorMessage(error, 'Could not save your profile.'), 'error'); return false
      }
    },
    async addAddress(address) {
      const addresses = JSON.parse(JSON.stringify(this.user?.addresses || []))
      if (address.isDefault) addresses.forEach(a => { a.isDefault = false })
      addresses.push({ ...address, id: Date.now() })
      return this.updateProfile({ addresses })
    },
    addPaymentMethod() {
      useNotificationStore().addToast('Saved card payments are not available yet.', 'info')
      return false
    },
  },
})
