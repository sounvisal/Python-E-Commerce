import '@/assets/admin.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Admin error:', err)
  console.error('Error info:', info)
  console.error('Component:', instance)
  // TODO: Send to error tracking service (Sentry, LogRocket, etc.)
}

// Warning handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Admin warning:', msg)
  console.warn('Trace:', trace)
}

app.use(pinia)
app.use(router)

app.mount('#app')
