import apiClient from '@/api/client'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('lumea_admin_token') || 'demo_super_admin_session_active')
  const user = ref(
    JSON.parse(localStorage.getItem('lumea_admin_user') || 'null') || {
      name: 'Sreynich Chan',
      email: 'admin@lumea.com',
      role: 'Super Admin',
    }
  )
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email, password) {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.post('/auth/login', { email, password })
      const tokenVal = response.data?.data?.access_token || response.data?.data?.token
      if (tokenVal) {
        token.value = tokenVal
        user.value = {
          ...response.data.data.user,
          role: 'Master Curator / Admin',
        }
        localStorage.setItem('lumea_admin_token', token.value)
        localStorage.setItem('lumea_admin_user', JSON.stringify(user.value))
        return { success: true }
      }
      return { success: false, message: 'Invalid server response' }
    } catch (err) {
      error.value = err.response?.data?.message || 'Login failed. Please verify credentials.'
      return { success: false, message: error.value }
    } finally {
      isLoading.value = false
    }
  }

  function demoLogin() {
    token.value = 'demo_admin_bearer_token_' + Date.now()
    user.value = {
      id: 1,
      name: 'Alexander Vance',
      email: 'admin@lumea.com',
      role: 'Master Curator / Admin',
    }
    localStorage.setItem('lumea_admin_token', token.value)
    localStorage.setItem('lumea_admin_user', JSON.stringify(user.value))
    return true
  }

  async function logout() {
    try {
      if (token.value && !token.value.startsWith('demo_admin_')) {
        await apiClient.post('/auth/logout')
      }
    } catch (e) {
      console.warn('Logout request ignored error:', e)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('lumea_admin_token')
      localStorage.removeItem('lumea_admin_user')
    }
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    demoLogin,
    logout,
  }
})
