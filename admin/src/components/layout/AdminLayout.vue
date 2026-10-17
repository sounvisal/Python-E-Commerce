<script setup>
import ToastContainer from '@/components/common/ToastContainer.vue'
import AdminHeader from '@/components/layout/AdminHeader.vue'
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import { ref } from 'vue'

const isSidebarCollapsed = ref(false)

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<template>
  <div class="admin-shell">
    <AdminSidebar
      :collapsed="isSidebarCollapsed"
      @toggle-collapse="toggleSidebar"
    />

    <div class="admin-main-area">
      <AdminHeader />

      <main class="admin-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-view" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- Global Toasts -->
    <ToastContainer />
  </div>
</template>

<style scoped>
.admin-shell {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  background-color: var(--bg-app);
  overflow-x: hidden;
}

.admin-main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100vh;
  overflow: hidden;
}

.admin-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background-color: var(--bg-app);
}

.fade-view-enter-active,
.fade-view-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-view-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.fade-view-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 768px) {
  .admin-content {
    padding: 1rem;
  }
}
</style>
