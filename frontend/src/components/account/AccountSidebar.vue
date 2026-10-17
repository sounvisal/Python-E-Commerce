<template>
  <aside class="account-sidebar-component">
    <!-- User Profile Header Card -->
    <div class="user-profile-badge">
      <div class="user-avatar-wrap">
        <img :src="authStore.userAvatar" :alt="authStore.userName" class="user-avatar-img" />
        <span class="user-tier-dot" title="Gold Member"></span>
      </div>
      <h3 class="user-name">{{ authStore.userName }}</h3>
      <span class="user-email">{{ authStore.userEmail }}</span>
      <button class="btn-edit-profile" @click="emit('edit-profile')">
        Edit Profile
      </button>
    </div>

    <!-- Account Navigation Menu -->
    <nav class="account-nav-list" aria-label="Account Navigation">
      <router-link
        to="/account"
        class="nav-item"
        :class="{ active: currentActive === 'overview' || route.path === '/account' }"
      >
        <Home :size="18" class="nav-icon" />
        <span>Overview</span>
      </router-link>

      <router-link
        to="/account/orders"
        class="nav-item"
        :class="{ active: currentActive === 'orders' || route.path.startsWith('/account/orders') }"
      >
        <Package :size="18" class="nav-icon" />
        <span>Orders</span>
        <span v-if="ordersStore.totalOrders" class="nav-badge">{{ ordersStore.totalOrders }}</span>
      </router-link>

      <router-link
        to="/wishlist"
        class="nav-item"
        :class="{ active: currentActive === 'wishlist' || route.path === '/wishlist' }"
      >
        <Heart :size="18" class="nav-icon" />
        <span>Wishlist</span>
        <span v-if="wishlistStore.totalItems" class="nav-badge">{{ wishlistStore.totalItems }}</span>
      </router-link>

      <button
        type="button"
        class="nav-item btn-nav-trigger"
        :class="{ active: currentActive === 'addresses' }"
        @click="emit('open-addresses')"
      >
        <MapPin :size="18" class="nav-icon" />
        <span>Addresses</span>
      </button>

      <button
        type="button"
        class="nav-item btn-nav-trigger"
        :class="{ active: currentActive === 'payments' }"
        @click="emit('open-payments')"
      >
        <CreditCard :size="18" class="nav-icon" />
        <span>Payment Methods</span>
      </button>

      <router-link
        to="/wishlist"
        class="nav-item"
        :class="{ active: currentActive === 'saved' }"
      >
        <Bookmark :size="18" class="nav-icon" />
        <span>Saved Items</span>
      </router-link>

      <router-link
        to="/account/profile"
        class="nav-item"
        :class="{ active: currentActive === 'profile' || route.path === '/account/profile' }"
      >
        <Sparkles :size="18" class="nav-icon" />
        <span>Beauty Profile</span>
      </router-link>

      <router-link
        to="/account/journal"
        class="nav-item"
        :class="{ active: currentActive === 'journal' || route.path === '/account/journal' }"
      >
        <BookOpen :size="18" class="nav-icon" />
        <span>Skincare Journal</span>
      </router-link>

      <button
        type="button"
        class="nav-item btn-nav-trigger"
        :class="{ active: currentActive === 'notifications' }"
        @click="emit('open-notifications')"
      >
        <Bell :size="18" class="nav-icon" />
        <span>Notifications</span>
      </button>

      <button
        type="button"
        class="nav-item btn-nav-trigger"
        :class="{ active: currentActive === 'settings' }"
        @click="emit('open-settings')"
      >
        <Settings :size="18" class="nav-icon" />
        <span>Account Settings</span>
      </button>
    </nav>

    <!-- Support / Need Help Card -->
    <div class="sidebar-help-card">
      <div class="help-icon-wrap">
        <Headphones :size="22" class="help-icon" />
      </div>
      <div class="help-info">
        <h4 class="help-title">Need Help?</h4>
        <p class="help-desc">Our customer support team is here for you.</p>
      </div>
      <router-link to="/contact" class="btn-sidebar-contact">
        Contact Us
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useOrdersStore } from '@/stores/orders'
import { useWishlistStore } from '@/stores/wishlist'
import {
  Home,
  Package,
  Heart,
  MapPin,
  CreditCard,
  Bookmark,
  Sparkles,
  BookOpen,
  Bell,
  Settings,
  Headphones
} from 'lucide-vue-next'

const props = defineProps({
  currentActive: {
    type: String,
    default: ''
  }
})

const emit = defineEmits([
  'edit-profile',
  'open-addresses',
  'open-payments',
  'open-notifications',
  'open-settings'
])

const route = useRoute()
const authStore = useAuthStore()
const ordersStore = useOrdersStore()
const wishlistStore = useWishlistStore()
</script>

<style scoped>
.account-sidebar-component {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* User Profile Badge */
.user-profile-badge {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.user-avatar-wrap {
  position: relative;
  width: 76px;
  height: 76px;
  margin-bottom: 12px;
}

.user-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #EFE6DD;
  box-shadow: 0 4px 12px rgba(28, 25, 23, 0.08);
}

.user-tier-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #D4AF37;
  border: 2px solid #FFFFFF;
}

.user-name {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 18px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 3px;
}

.user-email {
  font-size: 12.5px;
  color: #78716C;
  margin-bottom: 16px;
  word-break: break-all;
}

.btn-edit-profile {
  display: inline-block;
  width: 100%;
  padding: 8px 16px;
  background: #F8F3ED;
  border: 1px solid #EADBCF;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit-profile:hover {
  background: #8E4A3E;
  color: #FFFFFF;
  border-color: #8E4A3E;
}

/* Nav Menu */
.account-nav-list {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  color: #57534E;
  font-size: 13.5px;
  font-weight: 500;
  text-decoration: none;
  background: transparent;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: all 0.18s ease;
}

.btn-nav-trigger {
  font-family: inherit;
}

.nav-icon {
  color: #78716C;
  transition: color 0.18s ease;
  flex-shrink: 0;
}

.nav-item:hover {
  background: #FAF7F2;
  color: #1A1D1A;
}

.nav-item:hover .nav-icon {
  color: #8E4A3E;
}

.nav-item.active {
  background: #FDF2EE;
  color: #8E4A3E;
  font-weight: 600;
}

.nav-item.active .nav-icon {
  color: #8E4A3E;
}

.nav-badge {
  margin-left: auto;
  padding: 1px 7px;
  background: #F5EAE7;
  color: #8E4A3E;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
}

/* Help Card */
.sidebar-help-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.help-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #FAF3EE;
  display: flex;
  align-items: center;
  justify-content: center;
}

.help-icon {
  color: #8E4A3E;
}

.help-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 15px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 2px;
}

.help-desc {
  font-size: 12px;
  color: #78716C;
  line-height: 1.45;
}

.btn-sidebar-contact {
  display: inline-block;
  width: 100%;
  padding: 8px 16px;
  text-align: center;
  background: #FFFFFF;
  border: 1px solid #8E4A3E;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-sidebar-contact:hover {
  background: #8E4A3E;
  color: #FFFFFF;
}
</style>
