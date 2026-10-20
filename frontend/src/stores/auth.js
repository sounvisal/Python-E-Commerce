import { defineStore } from 'pinia'
import { useNotificationStore } from './notification'
import { safeGetJSON, safeSetJSON, safeRemove } from '@/utils/storage'

const DEFAULT_USER = {
  name: 'Sreynich Chan',
  firstName: 'Sreynich',
  lastName: 'Chan',
  email: 'sreynich.chan@example.com',
  phone: '+855 12 345 678',
  avatar: '/images/avatar-sreynich.jpg',
  rewardPoints: 320,
  tier: 'Luméa Radiant Gold',
  joinedDate: 'May 2024',
  totalOrders: 12,
  wishlistCount: 8,
  savedForLaterCount: 3,
  addresses: [
    {
      id: 1,
      name: 'Sreynich Chan',
      tag: 'Home',
      street: '#123, Street 271',
      commune: 'Sangkat Boeung Tumpun',
      district: 'Khan Meanchey',
      city: 'Phnom Penh',
      postalCode: '12000',
      country: 'Cambodia',
      phone: '+855 12 345 678',
      isDefault: true,
    },
    {
      id: 2,
      name: 'Sreynich Chan (Office)',
      tag: 'Work',
      street: '#45, Norodom Boulevard',
      commune: 'Sangkat Phsar Thmei 1',
      district: 'Khan Daun Penh',
      city: 'Phnom Penh',
      postalCode: '12200',
      country: 'Cambodia',
      phone: '+855 12 345 678',
      isDefault: false,
    }
  ],
  paymentMethods: [
    {
      id: 1,
      provider: 'ABA',
      name: 'ABA Pay',
      accountNumber: '**** 3456',
      expiry: '12/28',
      badge: 'Default',
      isDefault: true,
      color: '#005D8E'
    },
    {
      id: 2,
      provider: 'Mastercard',
      name: 'Mastercard',
      accountNumber: '**** 9012',
      expiry: '11/27',
      badge: null,
      isDefault: false,
      color: '#EB001B'
    }
  ]
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    const user = safeGetJSON('lumea_auth_user', null)
    const token = localStorage.getItem('lumea_auth_token') || null
    
    return {
      user,
      token,
      isAuthenticated: !!(token && user),
    }
  },

  getters: {
    userName: (state) => state.user?.name || 'Sreynich Chan',
    userFirstName: (state) => state.user?.firstName || 'Sreynich',
    userEmail: (state) => state.user?.email || 'sreynich.chan@example.com',
    userAvatar: (state) => state.user?.avatar || '/images/avatar-sreynich.jpg',
    defaultAddress: (state) => state.user?.addresses?.find((a) => a.isDefault) || state.user?.addresses?.[0],
    defaultPayment: (state) => state.user?.paymentMethods?.find((p) => p.isDefault) || state.user?.paymentMethods?.[0],
  },

  actions: {
    persist() {
      safeSetJSON('lumea_auth_user', this.user)
      if (this.token) {
        localStorage.setItem('lumea_auth_token', this.token)
      } else {
        safeRemove('lumea_auth_token')
      }
    },

    login({ email, password, remember = true }) {
      const notificationStore = useNotificationStore()
      this.token = 'demo-token-' + Date.now()
      this.isAuthenticated = true
      
      // If logging in with different credentials, update display
      if (email && email !== this.user?.email) {
        if (!this.user) this.user = { ...DEFAULT_USER }
        this.user.email = email
        this.user.name = email.split('@')[0]
      } else if (!this.user) {
        this.user = { ...DEFAULT_USER }
      }
      
      if (remember) {
        this.persist()
      }
      notificationStore.addToast(`Welcome back, ${this.user.firstName}!`, 'success')
      return true
    },

    register({ name, email, phone, password }) {
      const notificationStore = useNotificationStore()
      const parts = name.trim().split(' ')
      const firstName = parts[0] || 'Member'
      const lastName = parts.slice(1).join(' ') || ''

      this.user = {
        ...DEFAULT_USER,
        name,
        firstName,
        lastName,
        email,
        phone: phone || '+855 12 000 000',
        rewardPoints: 100, // welcome bonus points
        totalOrders: 0,
      }
      this.token = 'demo-token-' + Date.now()
      this.isAuthenticated = true
      this.persist()
      notificationStore.addToast(`Welcome to Luméa, ${firstName}! You earned 100 bonus points.`, 'success')
      return true
    },

    logout() {
      const notificationStore = useNotificationStore()
      this.token = null
      this.user = null
      this.isAuthenticated = false
      safeRemove('lumea_auth_token')
      safeRemove('lumea_auth_user')
      notificationStore.addToast('You have been signed out.', 'info')
    },

    updateProfile(updates) {
      const notificationStore = useNotificationStore()
      this.user = { ...this.user, ...updates }
      this.persist()
      notificationStore.addToast('Profile updated successfully.', 'success')
    },

    addAddress(newAddr) {
      const notificationStore = useNotificationStore()
      const id = Date.now()
      if (newAddr.isDefault) {
        this.user.addresses.forEach(a => a.isDefault = false)
      }
      this.user.addresses.push({
        id,
        ...newAddr
      })
      this.persist()
      notificationStore.addToast('New address saved.', 'success')
    },

    addPaymentMethod(payment) {
      const notificationStore = useNotificationStore()
      const id = Date.now()
      if (payment.isDefault) {
        this.user.paymentMethods.forEach(p => p.isDefault = false)
      }
      this.user.paymentMethods.push({
        id,
        ...payment
      })
      this.persist()
      notificationStore.addToast('New payment method added.', 'success')
    }
  }
})
