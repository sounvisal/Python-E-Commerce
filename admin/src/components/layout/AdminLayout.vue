<script setup>
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import ToastContainer from '@/components/common/ToastContainer.vue'
import AdminHeader from '@/components/layout/AdminHeader.vue'
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/admin'

const route = useRoute()
const adminStore = useAdminStore()
const contentRef = ref(null)
const isSidebarCollapsed = ref(false)
const isMobileSidebarOpen = ref(false)

onMounted(() => {
  adminStore.fetchUploadStatus()
})

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Reset content scroll position & close mobile sidebar on route change
watch(() => route.path, () => {
  isMobileSidebarOpen.value = false
  if (contentRef.value) {
    contentRef.value.scrollTop = 0
  }
})
</script>

<template>
  <div class="admin-shell">
    <div
      v-if="isMobileSidebarOpen"
      class="sidebar-mobile-backdrop"
      @click="isMobileSidebarOpen = false"
    ></div>

    <AdminSidebar
      :collapsed="isSidebarCollapsed"
      :mobile-open="isMobileSidebarOpen"
      @toggle-collapse="toggleSidebar"
      @close-mobile="isMobileSidebarOpen = false"
    />

    <div class="admin-main-area">
      <AdminHeader @toggle-mobile-sidebar="isMobileSidebarOpen = !isMobileSidebarOpen" />

      <main ref="contentRef" class="admin-content">
        <router-view />
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
  width: 100%;
  max-width: 100vw;
  background-color: var(--bg-app);
  overflow-x: hidden;
}

.admin-main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  max-width: 100%;
  height: 100vh;
  overflow: hidden;
}

.admin-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  max-width: 100%;
  min-width: 0;
  width: 100%;
  padding: 2rem;
  background-color: var(--bg-app);
}

.sidebar-mobile-backdrop {
  display: none;
}

@media (max-width: 768px) {
  .admin-main-area {
    width: 100vw;
    max-width: 100vw;
  }

  .sidebar-mobile-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 1050;
    backdrop-filter: blur(2px);
  }

  .admin-content {
    padding: 1rem 0.75rem;
  }
}
</style>
