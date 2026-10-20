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

app.use(pinia)
app.use(router)
app.mount('#app')
