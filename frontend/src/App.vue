<template>
  <div id="lumea-app">
    <div v-if="cartStore.maintenanceMode" class="maintenance-alert-banner">
      <div class="maintenance-inner">
        <AlertTriangle :size="15" />
        <span>Atelier Notice: Storefront is currently undergoing scheduled catalog calibration. New orders and inquiries will be processed shortly.</span>
      </div>
    </div>
    <Navbar />
    <main>
      <router-view />
    </main>
    <Footer />
    <CartDrawer />
    <NotificationDrawer />
    <ToastContainer />
    <SystemModalContainer />
    <AtelierStatusPill />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { AlertTriangle } from 'lucide-vue-next'
import { useProductStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import CartDrawer from '@/components/CartDrawer.vue'
import NotificationDrawer from '@/components/NotificationDrawer.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import SystemModalContainer from '@/components/SystemModalContainer.vue'
import AtelierStatusPill from '@/components/common/AtelierStatusPill.vue'

const cartStore = useCartStore()

onMounted(() => {
  useProductStore().fetchProducts()
  cartStore.fetchSettings()
})
</script>

<style scoped>
#lumea-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.maintenance-alert-banner {
  background: #B45309;
  color: #FFFDF5;
  font-size: 12px;
  font-weight: 600;
  padding: 8px 16px;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 101;
}

.maintenance-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  max-width: 1400px;
  margin: 0 auto;
}

main {
  flex: 1;
}
</style>
