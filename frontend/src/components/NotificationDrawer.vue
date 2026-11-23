<template>
  <div
    class="notif-drawer-container"
    :class="{ 'is-active': notifStore.isDrawerOpen }"
    :inert="!notifStore.isDrawerOpen"
  >
    <!-- Backdrop Overlay -->
    <div class="notif-drawer-backdrop" @click="notifStore.closeDrawer"></div>

    <!-- Drawer Panel -->
    <aside
      ref="panelRef"
      class="notif-drawer-panel"
      role="dialog"
      aria-modal="true"
      aria-labelledby="notif-drawer-title"
      tabindex="-1"
    >
      <!-- Header -->
      <div class="notif-drawer-header">
        <div class="header-left-title">
          <div class="title-row">
            <Bell :size="18" class="title-bell-icon" />
            <h3 id="notif-drawer-title">Atelier Live Feed</h3>
          </div>
          <span v-if="notifStore.unreadCount > 0" class="badge-unread-pill">
            {{ notifStore.unreadCount }} new
          </span>
          <span v-else class="badge-all-read-pill">
            All caught up
          </span>
        </div>

        <div class="header-right-actions">
          <button
            v-if="notifStore.unreadCount > 0"
            class="btn-mark-all-read"
            @click="notifStore.markAllAsRead"
            title="Mark all as read"
          >
            <CheckCheck :size="15" />
            <span>Mark read</span>
          </button>
          <button
            class="close-btn"
            @click="notifStore.closeDrawer"
            aria-label="Close Notifications"
          >
            <X :size="20" />
          </button>
        </div>
      </div>

      <!-- Filter Pills Bar -->
      <div class="notif-filter-bar">
        <button
          type="button"
          class="filter-pill-btn"
          :class="{ active: notifStore.activeFilter === 'all' }"
          @click="notifStore.setFilter('all')"
        >
          All ({{ notifStore.notifications.length }})
        </button>
        <button
          type="button"
          class="filter-pill-btn"
          :class="{ active: notifStore.activeFilter === 'events' }"
          @click="notifStore.setFilter('events')"
        >
          <Sparkles :size="13" />
          <span>Events</span>
        </button>
        <button
          type="button"
          class="filter-pill-btn"
          :class="{ active: notifStore.activeFilter === 'purchases' }"
          @click="notifStore.setFilter('purchases')"
        >
          <ShoppingBag :size="13" />
          <span>Live Buys</span>
        </button>
      </div>

      <!-- Notifications List Body -->
      <div class="notif-drawer-body">
        <div v-if="notifStore.filteredNotifications.length === 0" class="notif-empty-state">
          <div class="empty-icon-wrap">
            <Bell :size="32" />
          </div>
          <h4>No notifications in this filter</h4>
          <p>You are all caught up with current atelier events and orders.</p>
          <button class="btn-reset-filter" @click="notifStore.setFilter('all')">
            View All Feed
          </button>
        </div>

        <div v-else class="notif-list">
          <article
            v-for="item in notifStore.filteredNotifications"
            :key="item.id"
            class="notif-card"
            :class="{ 'is-unread': !isRead(item.id) }"
            @click="handleCardClick(item)"
          >
            <div class="card-status-indicator" v-if="!isRead(item.id)"></div>

            <div class="card-header-row">
              <span class="tag-badge" :class="item.badgeColor || 'terracotta'">
                {{ item.tag }}
              </span>
              <span class="time-chip">{{ item.time }}</span>
            </div>

            <h4 class="card-title">{{ item.title }}</h4>
            <p class="card-message">{{ item.message }}</p>

            <!-- Optional Product Thumbnail Preview -->
            <div v-if="item.productImage" class="card-product-preview">
              <img :src="item.productImage" :alt="item.title" class="preview-img" />
              <div class="preview-details">
                <span class="preview-caption">Verified Purchase</span>
                <span class="preview-cta">View Product Details &rarr;</span>
              </div>
            </div>

            <!-- Action Button -->
            <div class="card-action-row" v-if="item.link">
              <router-link
                :to="item.link"
                class="btn-action-link"
                @click.stop="navigateAndClose(item)"
              >
                <span>{{ item.linkText || 'Learn More' }}</span>
                <ArrowRight :size="13" />
              </router-link>
            </div>
          </article>
        </div>
      </div>

      <!-- Footer Info -->
      <div class="notif-drawer-footer">
        <div class="footer-footnote">
          <Sparkles :size="13" class="footer-sparkle" />
          <span>Curated live by Luméa Atelier Concierge</span>
        </div>
        <router-link to="/shop" class="footer-shop-btn" @click="notifStore.closeDrawer">
          Browse Full Catalog &rarr;
        </router-link>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAtelierNotificationStore } from '@/stores/atelierNotifications'
import {
  Bell,
  X,
  CheckCheck,
  Sparkles,
  ShoppingBag,
  ArrowRight
} from 'lucide-vue-next'

const router = useRouter()
const notifStore = useAtelierNotificationStore()
const panelRef = ref(null)

const isRead = (id) => notifStore.readIds.includes(id)

const handleCardClick = (item) => {
  notifStore.markAsRead(item.id)
  if (item.link) {
    navigateAndClose(item)
  }
}

const navigateAndClose = (item) => {
  notifStore.markAsRead(item.id)
  notifStore.closeDrawer()
  if (item.link) {
    router.push(item.link)
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' && notifStore.isDrawerOpen) {
    notifStore.closeDrawer()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  notifStore.fetchNotifications()
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.notif-drawer-container {
  position: fixed;
  inset: 0;
  z-index: 9999;
  visibility: hidden;
  pointer-events: none;
  transition: visibility 0.3s ease;
}

.notif-drawer-container.is-active {
  visibility: visible;
  pointer-events: auto;
}

.notif-drawer-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(18, 16, 15, 0.45);
  backdrop-filter: blur(4px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.notif-drawer-container.is-active .notif-drawer-backdrop {
  opacity: 1;
}

.notif-drawer-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 100%;
  max-width: 440px;
  height: 100%;
  background: #FCFAF7;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: -8px 0 32px rgba(28, 25, 23, 0.12);
  outline: none;
}

.notif-drawer-container.is-active .notif-drawer-panel {
  transform: translateX(0);
}

/* Header */
.notif-drawer-header {
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #EFEAE4;
  background: #FFFFFF;
}

.header-left-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-bell-icon {
  color: #7A2E22;
}

#notif-drawer-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.2rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.badge-unread-pill {
  background: #7A2E22;
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.15rem 0.55rem;
  border-radius: 9999px;
  letter-spacing: 0.02em;
}

.badge-all-read-pill {
  background: #EFEAE4;
  color: #78716C;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.15rem 0.55rem;
  border-radius: 9999px;
}

.header-right-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-mark-all-read {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: transparent;
  border: none;
  font-size: 0.78rem;
  font-weight: 500;
  color: #78716C;
  cursor: pointer;
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-mark-all-read:hover {
  color: #7A2E22;
  background: #F5EFEB;
}

.close-btn {
  background: transparent;
  border: none;
  color: #78716C;
  cursor: pointer;
  padding: 0.35rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  color: #1C1917;
  background: #F5EFEB;
}

/* Filter bar */
.notif-filter-bar {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.75rem 1.5rem;
  background: #FAF7F2;
  border-bottom: 1px solid #EFEAE4;
}

.filter-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #FFFFFF;
  border: 1px solid #E8DFD8;
  border-radius: 9999px;
  padding: 0.35rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #57534E;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill-btn:hover {
  border-color: #7A2E22;
  color: #7A2E22;
}

.filter-pill-btn.active {
  background: #1C1917;
  border-color: #1C1917;
  color: #FFFFFF;
}

/* Body */
.notif-drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem 1.5rem;
}

.notif-empty-state {
  text-align: center;
  padding: 3.5rem 1rem;
}

.empty-icon-wrap {
  width: 56px;
  height: 56px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  background: #F5EFEB;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #A8A29E;
}

.notif-empty-state h4 {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.1rem;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.notif-empty-state p {
  font-size: 0.85rem;
  color: #78716C;
  margin-bottom: 1.25rem;
}

.btn-reset-filter {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
}

/* List items */
.notif-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.notif-card {
  position: relative;
  background: #FFFFFF;
  border: 1px solid #EFEAE4;
  border-radius: 12px;
  padding: 1.1rem 1.15rem 1.1rem 1.35rem;
  cursor: pointer;
  transition: all 0.22s ease;
}

.notif-card:hover {
  border-color: #D6CBC2;
  box-shadow: 0 4px 14px rgba(28, 25, 23, 0.05);
  transform: translateY(-1px);
}

.notif-card.is-unread {
  background: #FFFAF8;
  border-color: #F0D5CD;
}

.card-status-indicator {
  position: absolute;
  top: 1.25rem;
  left: 0.5rem;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #7A2E22;
}

.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.45rem;
}

.tag-badge {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
}

.tag-badge.terracotta {
  background: #FBF0ED;
  color: #7A2E22;
}

.tag-badge.emerald {
  background: #EEF8F2;
  color: #1B7A43;
}

.tag-badge.gold {
  background: #FCF7E8;
  color: #926A18;
}

.time-chip {
  font-size: 0.72rem;
  color: #A8A29E;
}

.card-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 0.98rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.35rem;
  line-height: 1.35;
}

.card-message {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 0.65rem;
}

/* Product preview */
.card-product-preview {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #FAF7F2;
  border: 1px solid #EFEAE4;
  border-radius: 8px;
  padding: 0.45rem 0.65rem;
  margin-bottom: 0.65rem;
}

.preview-img {
  width: 38px;
  height: 38px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #E8DFD8;
}

.preview-details {
  display: flex;
  flex-direction: column;
}

.preview-caption {
  font-size: 0.68rem;
  color: #1B7A43;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.preview-cta {
  font-size: 0.75rem;
  color: #1C1917;
  font-weight: 500;
}

/* Action button */
.card-action-row {
  display: flex;
  justify-content: flex-end;
}

.btn-action-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
  transition: gap 0.2s ease;
}

.btn-action-link:hover {
  gap: 0.55rem;
  text-decoration: underline;
}

/* Footer */
.notif-drawer-footer {
  padding: 1.15rem 1.5rem;
  background: #FFFFFF;
  border-top: 1px solid #EFEAE4;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.footer-footnote {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  font-size: 0.74rem;
  color: #8C827A;
}

.footer-sparkle {
  color: #D97706;
}

.footer-shop-btn {
  display: block;
  text-align: center;
  background: #1C1917;
  color: #FFFFFF;
  padding: 0.65rem 1rem;
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.2s ease;
}

.footer-shop-btn:hover {
  background: #7A2E22;
}

@media (max-width: 480px) {
  .notif-drawer-panel {
    max-width: 100%;
  }
}
</style>
