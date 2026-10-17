<script setup>
import AdminLayout from '@/components/layout/AdminLayout.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isLoginPage = computed(() => route.name === 'login')
</script>

<template>
  <div id="app-root">
    <router-view v-if="isLoginPage" />
    <AdminLayout v-else />
  </div>
</template>

<style>
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
