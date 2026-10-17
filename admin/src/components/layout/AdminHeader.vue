<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAdminStore } from '@/stores/admin'
import {
  Search,
  Bell,
  ChevronDown,
  User,
  Settings,
  LogOut,
  Sparkles,
  ExternalLink
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const adminStore = useAdminStore()

const searchQuery = ref('')
const showUserDropdown = ref(false)
const showNotifications = ref(false)

const notifications = ref([
  { id: 1, title: 'New order #LUM-00124', time: '2m ago', type: 'order' },
  { id: 2, title: 'Low stock: Hydrating Toner (5 left)', time: '15m ago', type: 'stock' },
  { id: 3, title: 'Return request #RT-0012 received', time: '1h ago', type: 'return' },
])

function handleSearch() {
  if (!searchQuery.value.trim()) return
  const q = searchQuery.value.trim().toLowerCase()
  // Navigate based on query prefix or default to products
  if (q.startsWith('#lum-') || q.startsWith('lum-')) {
    router.push({ path: '/orders', query: { q: searchQuery.value } })
  } else {
    router.push({ path: '/products', query: { q: searchQuery.value } })
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="atelier-header">
    <!-- Left: Global Search Bar matching mockup -->
    <div class="header-search-area">
      <div class="header-search-box">
        <Search :size="16" class="search-icon" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search products, orders, customers..."
          @keyup.enter="handleSearch"
        />
      </div>
    </div>

    <!-- Right: Notifications & Super Admin Profile Chip -->
    <div class="header-right-area">
      <!-- Notification Bell -->
      <div class="dropdown-anchor">
        <button
          type="button"
          class="btn-header-icon"
          title="Notifications"
          @click="showNotifications = !showNotifications; showUserDropdown = false"
        >
          <Bell :size="18" />
          <span class="notification-badge-dot"></span>
        </button>

        <div v-if="showNotifications" class="dropdown-popover notifications-popover">
          <div class="popover-head">
            <strong>Atelier Notifications</strong>
            <span class="badge-count">{{ notifications.length }}</span>
          </div>
          <div class="notifications-list">
            <div
              v-for="n in notifications"
              :key="n.id"
              class="notif-row"
            >
              <div class="notif-bullet"></div>
              <div class="notif-content">
                <span class="notif-title">{{ n.title }}</span>
                <span class="notif-time">{{ n.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Super Admin Profile Chip matching mockup -->
      <div class="dropdown-anchor">
        <button
          type="button"
          class="admin-profile-chip"
          @click="showUserDropdown = !showUserDropdown; showNotifications = false"
        >
          <img
            src="/images/avatar-super-admin.jpg"
            alt="Super Admin"
            class="admin-avatar-img"
            @error="$event.target.src = '/images/avatar-sreynich.jpg'"
          />
          <div class="admin-meta-text">
            <span class="admin-name">Admin</span>
            <span class="admin-role">Super Admin</span>
          </div>
          <ChevronDown :size="14" class="chevron-arrow" />
        </button>

        <!-- Profile Popover Menu -->
        <div v-if="showUserDropdown" class="dropdown-popover profile-popover">
          <div class="user-popover-header">
            <strong>Administrator</strong>
            <span>admin@lumea.com</span>
          </div>

          <div class="popover-divider"></div>

          <router-link to="/settings" class="popover-menu-item" @click="showUserDropdown = false">
            <Settings :size="15" />
            <span>Atelier Settings</span>
          </router-link>

          <a href="http://localhost:5173" target="_blank" rel="noopener" class="popover-menu-item">
            <ExternalLink :size="15" />
            <span>Storefront Atelier</span>
          </a>

          <div class="popover-divider"></div>

          <button type="button" class="popover-menu-item text-danger" @click="handleLogout">
            <LogOut :size="15" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.atelier-header {
  height: var(--header-height);
  background-color: #FBF8F5;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  flex-shrink: 0;
  position: relative;
  z-index: 40;
}

/* Global Search */
.header-search-area {
  flex: 1;
  max-width: 480px;
}

.header-search-box {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: #FFFFFF;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.95rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  transition: all var(--transition-fast);
}

.header-search-box:focus-within {
  border-color: var(--crimson);
  box-shadow: 0 0 0 2px var(--crimson-glow);
}

.search-icon {
  color: var(--text-dim);
  flex-shrink: 0;
}

.header-search-box input {
  background: transparent;
  border: none;
  outline: none;
  color: var(--text-main);
  font-size: 0.88rem;
  width: 100%;
}

.header-search-box input::placeholder {
  color: var(--text-dim);
}

/* Right Section */
.header-right-area {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.dropdown-anchor {
  position: relative;
}

.btn-header-icon {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  background: #FFFFFF;
  border: 1px solid var(--border-subtle);
  color: #5C554F;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all var(--transition-fast);
}

.btn-header-icon:hover {
  color: var(--crimson);
  border-color: var(--crimson-border);
}

.notification-badge-dot {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 7px;
  height: 7px;
  background-color: var(--crimson);
  border-radius: 50%;
  border: 1.5px solid #FFFFFF;
}

/* Super Admin Chip matching mockup */
.admin-profile-chip {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: var(--radius-sm);
  transition: background-color var(--transition-fast);
}

.admin-profile-chip:hover {
  background-color: var(--bg-surface-elevated);
}

.admin-avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border-medium);
}

.admin-meta-text {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.admin-name {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.2;
}

.admin-role {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.chevron-arrow {
  color: var(--text-dim);
}

/* Dropdown Popovers */
.dropdown-popover {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: #FFFFFF;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 0.5rem;
  min-width: 220px;
  animation: popoverFadeIn 0.15s ease forwards;
}

@keyframes popoverFadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.popover-head {
  padding: 0.5rem 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 0.84rem;
}

.badge-count {
  background: var(--crimson-subtle);
  color: var(--crimson);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: var(--radius-full);
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.5rem 0;
  max-height: 240px;
  overflow-y: auto;
}

.notif-row {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.45rem 0.75rem;
  border-radius: var(--radius-xs);
  transition: background-color var(--transition-fast);
}

.notif-row:hover {
  background-color: var(--bg-surface-elevated);
}

.notif-bullet {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--crimson);
  margin-top: 6px;
  flex-shrink: 0;
}

.notif-content {
  display: flex;
  flex-direction: column;
}

.notif-title {
  font-size: 0.8rem;
  color: var(--text-main);
  line-height: 1.3;
}

.notif-time {
  font-size: 0.7rem;
  color: var(--text-dim);
}

.user-popover-header {
  padding: 0.5rem 0.75rem;
  display: flex;
  flex-direction: column;
}

.user-popover-header strong {
  font-size: 0.88rem;
  color: var(--text-main);
}

.user-popover-header span {
  font-size: 0.74rem;
  color: var(--text-muted);
}

.popover-divider {
  height: 1px;
  background-color: var(--border-subtle);
  margin: 0.35rem 0;
}

.popover-menu-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-xs);
  font-size: 0.84rem;
  color: var(--text-main);
  width: 100%;
  text-align: left;
  transition: all var(--transition-fast);
}

.popover-menu-item:hover {
  background-color: var(--bg-surface-elevated);
  color: var(--crimson);
}

.popover-menu-item.text-danger {
  color: var(--rose);
}

.popover-menu-item.text-danger:hover {
  background-color: var(--rose-bg);
}
</style>
