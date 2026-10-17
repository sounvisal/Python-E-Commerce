<template>
  <div id="lumea-app">
    <Navbar />
    <main>
      <router-view />
    </main>
    <Footer />
    <CartDrawer />
    <ToastContainer />
    <SystemModalContainer />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import CartDrawer from '@/components/CartDrawer.vue'
import ToastContainer from '@/components/ToastContainer.vue'
import SystemModalContainer from '@/components/SystemModalContainer.vue'
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
