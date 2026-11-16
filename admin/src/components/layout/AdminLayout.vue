<script setup>
import AdminSidebar from '@/components/layout/AdminSidebar.vue'
import ToastContainer from '@/components/common/ToastContainer.vue'
import AdminHeader from '@/components/layout/AdminHeader.vue'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const contentRef = ref(null)
const isSidebarCollapsed = ref(false)

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Reset content scroll position on route change
watch(() => route.path, () => {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0
  }
})
</script>

<template>
  <div class="admin-shell">
    <AdminSidebar
      :collapsed="isSidebarCollapsed"
      @toggle-collapse="toggleSidebar"
    />

    <div class="admin-main-area">
      <AdminHeader />

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

@media (max-width: 768px) {
  .admin-content {
    padding: 1rem;
  }
}
</style>
