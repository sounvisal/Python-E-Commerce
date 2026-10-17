<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import { useAuthStore } from '@/stores/auth'
import {
  LayoutDashboard,
  Package,
  Store,
  Layers,
  ShoppingBag,
  Users,
  Tag,
  Image as ImageIcon,
  Sparkles,
  BookOpen,
  MessageSquare,
  RotateCcw,
  BarChart2,
  Settings,
  LogOut,
  ExternalLink,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggleCollapse'])

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const adminStore = useAdminStore()

const menuGroups = [
  {
    title: null,
    items: [
      { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    ]
  },
  {
    title: 'COMMERCE',
    items: [
      { name: 'Products', path: '/products', icon: Package },
      { name: 'Brands', path: '/brands', icon: Store },
      { name: 'Categories', path: '/categories', icon: Layers },
      { name: 'Orders', path: '/orders', icon: ShoppingBag, badgeKey: 'orders' },
      { name: 'Customers', path: '/customers', icon: Users },
    ]
  },
  {
    title: 'MARKETING',
    items: [
      { name: 'Promotions', path: '/promotions', icon: Tag },
      { name: 'Homepage', path: '/homepage', icon: ImageIcon },
    ]
  },
  {
    title: 'PERSONALIZATION',
    items: [
      { name: 'Skin Quiz', path: '/quiz', icon: Sparkles },
    ]
  },
  {
    title: 'CONTENT',
    items: [
      { name: 'Articles', path: '/articles', icon: BookOpen },
      { name: 'Reviews', path: '/reviews', icon: MessageSquare },
    ]
  },
  {
    title: 'SERVICE',
    items: [
      { name: 'Returns', path: '/returns', icon: RotateCcw },
    ]
  },
  {
    title: 'ANALYTICS',
    items: [
      { name: 'Analytics', path: '/analytics', icon: BarChart2 },
    ]
  },
  {
    title: 'SYSTEM',
    items: [
      { name: 'Settings', path: '/settings', icon: Settings },
    ]
  }
]

const pendingOrdersCount = computed(() => {
  const confirmed = adminStore.stats?.orders_by_status?.confirmed || 0
  const processing = adminStore.stats?.orders_by_status?.processing || 0
  return confirmed + processing
})

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <aside class="atelier-sidebar" :class="{ 'sidebar-collapsed': collapsed }">
    <!-- Brand Header -->
    <div class="sidebar-brand">
      <router-link to="/dashboard" class="brand-link">
        <h2 class="brand-wordmark">Luméa</h2>
        <span class="brand-sub">ADMIN</span>
      </router-link>

      <button
        type="button"
        class="collapse-toggle-btn"
        :title="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        @click="emit('toggleCollapse')"
      >
        <ChevronRight v-if="collapsed" :size="16" />
        <ChevronLeft v-else :size="16" />
      </button>
    </div>

    <!-- Navigation Scroll Area -->
    <div class="sidebar-nav-scroll">
      <div v-for="(group, gIdx) in menuGroups" :key="gIdx" class="nav-group">
        <span v-if="group.title && !collapsed" class="group-title">{{ group.title }}</span>

        <nav class="group-items">
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            class="nav-link"
            :class="{ active: route.path === item.path || (item.path !== '/dashboard' && route.path.startsWith(item.path)) }"
            :title="collapsed ? item.name : ''"
          >
            <component :is="item.icon" :size="18" class="nav-icon" />
            <span v-if="!collapsed" class="nav-text">{{ item.name }}</span>

            <span
              v-if="!collapsed && item.badgeKey === 'orders' && pendingOrdersCount > 0"
              class="nav-badge-pill"
            >
              {{ pendingOrdersCount }}
            </span>
          </router-link>
        </nav>
      </div>
    </div>

    <!-- Bottom Brand Badge matching mockup -->
    <div class="sidebar-footer">
      <div v-if="!collapsed" class="beauty-lives-card">
        <div class="leaf-icon-wrap">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="#84261B">
            <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1-2.3A4.49 4.49 0 0 0 8 20C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75C7 8 17 8 17 8z"/>
          </svg>
        </div>
        <div class="beauty-text">
          <span class="brand-phrase">Beauty<br/>Lives Here.</span>
        </div>
      </div>

      <!-- Quick Storefront Link -->
      <a
        href="http://localhost:5173"
        target="_blank"
        rel="noopener"
        class="store-link-row"
        :title="collapsed ? 'Open Storefront' : ''"
      >
        <ExternalLink :size="15" />
        <span v-if="!collapsed">Storefront Preview</span>
      </a>
    </div>
  </aside>
</template>

<style scoped>
.atelier-sidebar {
  width: var(--sidebar-width);
  height: 100vh;
  background-color: var(--bg-sidebar);
  border-right: 1px solid #EADFD7;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width var(--transition-normal);
  position: relative;
  z-index: 50;
}

.sidebar-collapsed {
  width: var(--sidebar-collapsed-width);
}

/* Brand Header */
.sidebar-brand {
  padding: 1.25rem 1.4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #EADFD7;
  height: var(--header-height);
}

.brand-link {
  display: flex;
  flex-direction: column;
}

.brand-wordmark {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--crimson);
  letter-spacing: -0.02em;
  line-height: 1;
}

.brand-sub {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.14em;
  margin-top: 2px;
}

.collapse-toggle-btn {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: #FFFFFF;
  border: 1px solid #EADFD7;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.collapse-toggle-btn:hover {
  color: var(--crimson);
  border-color: var(--crimson-border);
}

/* Navigation Scroll */
.sidebar-nav-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.nav-group {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.group-title {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #A3978E;
  padding: 0 0.75rem 0.35rem;
  text-transform: uppercase;
}

.group-items {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-sm);
  color: #5C554F;
  font-size: 0.86rem;
  font-weight: 500;
  transition: all var(--transition-fast);
}

.nav-link:hover {
  background-color: #F8F1EB;
  color: var(--text-main);
}

.nav-link.active {
  background-color: var(--crimson-subtle);
  color: var(--crimson);
  font-weight: 600;
}

.nav-link.active .nav-icon {
  color: var(--crimson);
}

.nav-icon {
  color: #8C827A;
  flex-shrink: 0;
  transition: color var(--transition-fast);
}

.nav-text {
  flex: 1;
  white-space: nowrap;
}

.nav-badge-pill {
  background-color: var(--crimson);
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: var(--radius-full);
}

/* Footer Card matching mockup */
.sidebar-footer {
  padding: 0.85rem 0.75rem;
  border-top: 1px solid #EADFD7;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.beauty-lives-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #F9EBE6;
  border: 1px solid #F1DCD3;
  border-radius: var(--radius-md);
  padding: 0.75rem 0.85rem;
}

.leaf-icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-phrase {
  font-family: var(--font-serif);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--crimson);
  line-height: 1.25;
}

.store-link-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.45rem 0.75rem;
  color: var(--text-muted);
  font-size: 0.8rem;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.store-link-row:hover {
  background-color: #F8F1EB;
  color: var(--crimson);
}
</style>
