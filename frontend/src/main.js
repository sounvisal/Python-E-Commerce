import axios from 'axios'
import { useAuthStore } from './stores/auth'
import { useSystemModalStore } from './stores/systemModal'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Storefront error:', err)
  console.error('Error info:', info)
  console.error('Component:', instance)
}

// Warning handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Storefront warning:', msg)
  console.warn('Trace:', trace)
}

axios.interceptors.response.use(response => response, error => {
  if (error.response?.status === 401 && !/auth\/(login|register)/.test(error.config?.url || '')) {
    useAuthStore(pinia).logout(false)
    useSystemModalStore(pinia).showSessionExpired()
  }
  return Promise.reject(error)
})
app.use(pinia)
app.use(router)
app.mount('#app')
