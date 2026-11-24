<template>
  <div id="lumea-app">
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
import { useProductStore } from '@/stores/products'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import CartDrawer from '@/components/CartDrawer.vue'
import NotificationDrawer from '@/components/NotificationDrawer.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import SystemModalContainer from '@/components/SystemModalContainer.vue'
import AtelierStatusPill from '@/components/common/AtelierStatusPill.vue'

onMounted(() => useProductStore().fetchProducts())
</script>

<style scoped>
#lumea-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}
</style>
