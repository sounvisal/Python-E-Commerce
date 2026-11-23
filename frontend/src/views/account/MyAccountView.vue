<template>
  <div class="my-account-page" v-if="authStore.user">
    <div class="container account-container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/" class="crumb-link">Home</router-link>
        <span class="crumb-sep">›</span>
        <span class="crumb-current">My Account</span>
      </nav>

      <!-- Panoramic Hero Banner matching My Account.png -->
      <section class="account-hero-banner">
        <div class="hero-left-content">
          <h1 class="hero-title">My Account</h1>
          <p class="hero-desc">
            Manage your account, orders, and beauty journey.
          </p>
        </div>

        <div class="hero-right-stage">
          <img
            src="/images/banner-my-account.jpg"
            alt="Luméa Beauty Collection"
            class="hero-banner-image"
          />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Good<br />Skin Days<br />Are Ahead.</span>
          </div>
        </div>
      </section>

      <!-- 3-Column Main Content Layout matching format/My Account.png -->
      <div class="account-3col-grid">
        <!-- ========================================================= -->
        <!-- LEFT COLUMN: Reusable Account Sidebar                     -->
        <!-- ========================================================= -->
        <div class="sidebar-column">
          <AccountSidebar
            currentActive="overview"
            @open-addresses="showAddressModal = true"
            @open-payments="showPaymentModal = true"
            @edit-profile="showProfileModal = true"
            @pick-avatar="openAvatarModal"
            @open-notifications="showNotificationsModal = true"
            @open-settings="showSettingsModal = true"
          />
        </div>

        <!-- ========================================================= -->
        <!-- CENTER COLUMN: Dashboard Main Stage                       -->
        <!-- ========================================================= -->
        <main class="dashboard-main-column">
          <!-- Welcome Greeting Card -->
          <div class="welcome-banner-card">
            <div class="welcome-header-content">
              <div class="welcome-top-line">
                <span class="greeting-pre">Hello,</span>
                <button type="button" class="btn-banner-logout" @click="handleLogout" title="Sign out of account">
                  <LogOut :size="14" />
                  <span>Log Out</span>
                </button>
              </div>
              <h2 class="greeting-name">{{ authStore.userFirstName }}!</h2>
              <p class="greeting-sub">Thanks for being part of the Luméa community.</p>
            </div>

            <!-- Luméa Rewards Badge inside Banner -->
            <div class="rewards-callout-pill" :class="{ 'gold-pill': isGoldMember }">
              <div class="rewards-crown-wrap">
                <Crown v-if="isGoldMember" :size="18" class="crown-svg gold" />
                <Star v-else :size="18" class="crown-svg" />
              </div>
              <div class="rewards-text-col">
                <span class="rewards-badge-title">{{ authStore.user?.tier || 'Atelier Member' }}</span>
                <span class="rewards-badge-desc">
                  {{ isGoldMember ? 'Radiant Gold Member • Enjoy 2x Points' : 'Standard Member • Earn points with purchases' }}
                </span>
                <button class="rewards-link-btn" @click="showRewardsModal = true">
                  View Benefits &rarr;
                </button>
              </div>
            </div>
          </div>

          <!-- 4 Stat Counters Grid matching mockup -->
          <div class="stats-counters-grid">
            <div class="stat-counter-card">
              <div class="stat-icon-wrap">
                <Calendar :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ ordersStore.totalOrders }}</span>
                <span class="stat-label">Total Orders</span>
              </div>
            </div>

            <router-link to="/wishlist" class="stat-counter-card clickable">
              <div class="stat-icon-wrap">
                <Heart :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ wishlistStore.totalItems }}</span>
                <span class="stat-label">Items in Wishlist</span>
              </div>
            </router-link>

            <router-link to="/routine" class="stat-counter-card clickable">
              <div class="stat-icon-wrap">
                <Sparkles :size="18" class="stat-icon" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">Active</span>
                <span class="stat-label">My Routine</span>
              </div>
            </router-link>

            <div class="stat-counter-card">
              <div class="stat-icon-wrap">
                <Star :size="18" class="stat-icon star-active" />
              </div>
              <div class="stat-text-col">
                <span class="stat-number">{{ authStore.user.rewardPoints }}</span>
                <span class="stat-label">Reward Points</span>
              </div>
            </div>
          </div>

          <!-- Recent Orders Section -->
          <section class="dashboard-section recent-orders-section">
            <div class="section-header-row">
              <h3 class="section-title">Recent Orders</h3>
              <router-link to="/account/orders" class="section-view-all">
                View All Orders &rarr;
              </router-link>
            </div>

            <div class="recent-orders-list">
              <div
                v-for="order in ordersStore.recentOrders"
                :key="order.orderNumber"
                class="recent-order-row-card"
              >
                <!-- Mini Items Thumbnail Stack -->
                <div class="order-thumbs-stack">
                  <div
                    v-for="(item, idx) in order.items.slice(0, 2)"
                    :key="idx"
                    class="order-mini-thumb"
                  >
                    <img
                      :src="item.image_url"
                      :alt="item.name"
                      @error="$event.target.src = '/images/prod-essence.jpg'"
                    />
                  </div>
                </div>

                <!-- Order Meta -->
                <div class="order-meta-col">
                  <router-link :to="`/account/orders/${order.orderNumber}`" class="order-id-link">
                    Order #{{ order.orderNumber }}
                  </router-link>
                  <span class="order-placed-date">{{ order.placedAt }}</span>
                </div>

                <!-- Status Dot & Label -->
                <div class="order-status-col">
                  <span
                    class="status-indicator-dot"
                    :class="order.statusType"
                  ></span>
                  <span class="status-name-text">{{ order.status }}</span>
                </div>

                <!-- Order Total -->
                <div class="order-price-col">
                  <span class="order-total-val">${{ order.total.toFixed(2) }}</span>
                </div>

                <!-- View Details CTA -->
                <div class="order-action-col">
                  <router-link
                    :to="`/account/orders/${order.orderNumber}`"
                    class="btn-view-order-details"
                  >
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </section>

          <!-- Recommended for You Carousel using UNIVERSAL ProductCard -->
          <section class="dashboard-section recommendations-section">
            <div class="section-header-row">
              <div>
                <h3 class="section-title">Recommended for You</h3>
                <p class="section-subtitle">Based on your recent purchases</p>
              </div>
              <router-link to="/shop" class="section-view-all">
                See All Recommendations &rarr;
              </router-link>
            </div>

            <!-- Grid of standard ProductCard matching homepage -->
            <div class="recommended-cards-grid">
              <ProductCard
                v-for="product in recommendedProducts"
                :key="product.id"
                :product="product"
              />
            </div>
          </section>
        </main>

        <!-- ========================================================= -->
        <!-- RIGHT COLUMN: Addresses, Payments & Loyalty               -->
        <!-- ========================================================= -->
        <aside class="dashboard-aside-column">
          <!-- Saved Addresses Card -->
          <div class="aside-card saved-addresses-card">
            <div class="aside-card-header">
              <h3 class="aside-card-title">Saved Addresses</h3>
              <button class="aside-manage-btn" @click="showAddressModal = true">
                Manage &rarr;
              </button>
            </div>

            <div class="saved-address-body" v-if="authStore.defaultAddress">
              <span class="default-pill-badge">Default</span>
              <div class="address-details-wrap">
                <MapPin :size="16" class="address-pin-icon" />
                <div class="address-text-content">
                  <strong class="addr-name">{{ authStore.defaultAddress.name }}</strong>
                  <p class="addr-street">{{ authStore.defaultAddress.street }}</p>
                  <p class="addr-commune">{{ authStore.defaultAddress.commune }}, {{ authStore.defaultAddress.district }}</p>
                  <p class="addr-city">{{ authStore.defaultAddress.city }} {{ authStore.defaultAddress.postalCode }}, {{ authStore.defaultAddress.country }}</p>
                  <span class="addr-phone">{{ authStore.defaultAddress.phone }}</span>
                </div>
              </div>

              <button class="btn-add-dashed-action" @click="showAddressModal = true">
                <Plus :size="15" />
                <span>Add New Address</span>
              </button>
            </div>
          </div>

          <!-- Payment Methods Card -->
          <div class="aside-card payment-methods-card">
            <div class="aside-card-header">
              <h3 class="aside-card-title">Payment Methods</h3>
              <button class="aside-manage-btn" @click="showPaymentModal = true">
                Manage &rarr;
              </button>
            </div>

            <div class="payment-methods-list">
              <div
                v-for="payment in authStore.user.paymentMethods"
                :key="payment.id"
                class="payment-row-item"
              >
                <div class="payment-provider-icon" :style="{ backgroundColor: payment.color || '#005D8E' }">
                  <span class="provider-symbol">{{ payment.provider }}</span>
                </div>

                <div class="payment-meta-text">
                  <div class="payment-name-row">
                    <span class="pay-name">{{ payment.name }} {{ payment.accountNumber }}</span>
                    <span v-if="payment.isDefault" class="default-tag-pill">Default</span>
                  </div>
                  <span class="pay-expiry">Expires {{ payment.expiry }}</span>
                </div>

                <button class="pay-options-btn" title="Options">
                  <MoreVertical :size="15" />
                </button>
              </div>

              <button class="btn-add-dashed-action" @click="showPaymentModal = true">
                <Plus :size="15" />
                <span>Manage Payment Methods</span>
              </button>
            </div>
          </div>

          <!-- Luméa Rewards Promo Card matching mockup -->
          <div class="aside-card rewards-promo-card">
            <h4 class="rewards-promo-title">Luméa Rewards</h4>
            <p class="rewards-promo-tagline">Shop More, Glow More.</p>

            <ul class="rewards-perks-bullets">
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Earn points on every purchase</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Exclusive member discounts</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Early access to new arrivals</span>
              </li>
              <li>
                <Check :size="14" class="check-perk-icon" />
                <span>Birthday surprises</span>
              </li>
            </ul>

            <button class="btn-rewards-learn-more" @click="showRewardsModal = true">
              Learn More
            </button>
          </div>
        </aside>
      </div>
    </div>
  </div>
  <!-- 1. Edit Profile & Address Modal -->
  <div v-if="showProfileModal || showAddressModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Edit account details" @click.self="showProfileModal = false; showAddressModal = false">
    <form class="account-edit-form" @submit.prevent="showProfileModal ? saveAccountProfile() : saveAddress()">
      <div class="modal-title-row">
        <h2>{{ showProfileModal ? 'Edit Profile' : 'Add New Address' }}</h2>
        <button type="button" class="btn-close-modal" @click="showProfileModal = false; showAddressModal = false"><X :size="18" /></button>
      </div>
      <template v-if="showProfileModal">
        <label>Name<input v-model="profileForm.name" required minlength="2" maxlength="100" class="modal-input" /></label>
        <label>Phone<input v-model="profileForm.phone" type="tel" class="modal-input" placeholder="+855 12 345 678" /></label>
      </template>
      <template v-else>
        <label>Recipient<input v-model="addressForm.name" required class="modal-input" /></label>
        <label>Street address<input v-model="addressForm.street" required class="modal-input" placeholder="#123, Street 2004" /></label>
        <label>City<input v-model="addressForm.city" required class="modal-input" placeholder="Phnom Penh" /></label>
        <label>Postal code<input v-model="addressForm.postalCode" class="modal-input" placeholder="12000" /></label>
        <label>Phone<input v-model="addressForm.phone" type="tel" class="modal-input" placeholder="+855 12 345 678" /></label>
      </template>
      <div class="modal-actions-row">
        <button type="button" class="btn btn-outline" @click="showProfileModal = false; showAddressModal = false">Cancel</button>
        <button type="submit" class="btn btn-primary" :disabled="savingProfile">{{ savingProfile ? 'Saving...' : 'Save' }}</button>
      </div>
    </form>
  </div>

  <!-- 2. Avatar Picker Modal -->
  <div v-if="showAvatarModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Choose profile picture" @click.self="showAvatarModal = false">
    <div class="account-modal-box avatar-picker-modal">
      <div class="modal-head">
        <div>
          <h3>Choose Your Atelier Avatar</h3>
          <p class="modal-subtext">Pick a profile picture that represents your beauty journey.</p>
        </div>
        <button type="button" class="btn-modal-x" @click="showAvatarModal = false"><X :size="18" /></button>
      </div>

      <div class="avatar-choices-grid">
        <div
          v-for="av in avatarChoices"
          :key="av.id"
          class="avatar-pick-card"
          :class="{ active: selectedAvatarPath === av.src }"
          @click="selectedAvatarPath = av.src"
        >
          <div class="avatar-frame">
            <img :src="av.src" :alt="av.label" />
            <div v-if="selectedAvatarPath === av.src" class="avatar-check-badge">
              <Check :size="13" />
            </div>
          </div>
          <span class="avatar-title">{{ av.label }}</span>
          <span class="avatar-tag">{{ av.category }}</span>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn-modal-cancel" @click="showAvatarModal = false">Cancel</button>
        <button type="button" class="btn-modal-save" :disabled="savingProfile" @click="saveChosenAvatar">
          {{ savingProfile ? 'Saving...' : 'Set Profile Picture' }}
        </button>
      </div>
    </div>
  </div>

  <!-- 3. Notifications Modal -->
  <div v-if="showNotificationsModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Notifications" @click.self="showNotificationsModal = false">
    <div class="account-modal-box notifications-modal">
      <div class="modal-head">
        <div>
          <h3>Atelier Notifications</h3>
          <p class="modal-subtext">Recent updates on your orders, rituals, and exclusive member perks.</p>
        </div>
        <button type="button" class="btn-modal-x" @click="showNotificationsModal = false"><X :size="18" /></button>
      </div>

      <div class="notifications-list">
        <div class="notification-item unread">
          <div class="notif-icon-circle welcome-icon"><Sparkles :size="16" /></div>
          <div class="notif-content">
            <div class="notif-top">
              <strong>Welcome to Luméa Atelier!</strong>
              <span class="notif-time">Just now</span>
            </div>
            <p>Your membership is active. Enjoy tailored skincare routines, authentic dermatological advice, and reward points.</p>
          </div>
        </div>

        <div class="notification-item">
          <div class="notif-icon-circle shipping-icon"><Package :size="16" /></div>
          <div class="notif-content">
            <div class="notif-top">
              <strong>Complimentary Delivery Perk</strong>
              <span class="notif-time">Active</span>
            </div>
            <p>Orders over $50 automatically qualify for complimentary nationwide shipping with VET Logistics and J&amp;T Express.</p>
          </div>
        </div>

        <div class="notification-item">
          <div class="notif-icon-circle security-icon"><ShieldCheck :size="16" /></div>
          <div class="notif-content">
            <div class="notif-top">
              <strong>Account Security Notice</strong>
              <span class="notif-time">Today</span>
            </div>
            <p>Your account is secured with encrypted JWT tokens. Remember to keep your credentials confidential.</p>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn-modal-save" @click="showNotificationsModal = false">Done</button>
      </div>
    </div>
  </div>

  <!-- 4. Account Settings Modal -->
  <div v-if="showSettingsModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Account Settings" @click.self="showSettingsModal = false">
    <div class="account-modal-box settings-modal">
      <div class="modal-head">
        <div>
          <h3>Account &amp; Security Settings</h3>
          <p class="modal-subtext">Manage communication preferences, security, and session options.</p>
        </div>
        <button type="button" class="btn-modal-x" @click="showSettingsModal = false"><X :size="18" /></button>
      </div>

      <div class="settings-body-form">
        <div class="settings-section">
          <h4 class="settings-sec-title">Communication Preferences</h4>
          <label class="settings-toggle-row">
            <input type="checkbox" v-model="settingsForm.orderUpdates" class="custom-checkbox" />
            <div>
              <strong>Order &amp; Delivery Tracking Alerts</strong>
              <p>Receive SMS and email status notifications when orders are dispatched.</p>
            </div>
          </label>
          <label class="settings-toggle-row">
            <input type="checkbox" v-model="settingsForm.marketingNewsletter" class="custom-checkbox" />
            <div>
              <strong>Atelier Skincare Journal &amp; New Launches</strong>
              <p>Curated articles, seasonal ingredient insights, and promotional deals.</p>
            </div>
          </label>
        </div>

        <div class="settings-section">
          <h4 class="settings-sec-title">Sign-in Security</h4>
          <p class="settings-subtext">Authenticated as <strong>{{ authStore.userEmail }}</strong></p>
        </div>

        <div class="settings-section danger-sec">
          <div class="danger-header">
            <div>
              <strong>Sign Out of Current Session</strong>
              <p>Terminate your authenticated session on this browser.</p>
            </div>
            <button type="button" class="btn-danger-logout" @click="handleLogout">Log Out</button>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn-modal-cancel" @click="showSettingsModal = false">Cancel</button>
        <button type="button" class="btn-modal-save" @click="saveAccountSettings">Save Settings</button>
      </div>
    </div>
  </div>

  <!-- 5. Payment Methods Modal -->
  <div v-if="showPaymentModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Payment Methods" @click.self="showPaymentModal = false">
    <div class="account-modal-box payments-modal">
      <div class="modal-head">
        <div>
          <h3>Payment Methods &amp; Checkout Preferences</h3>
          <p class="modal-subtext">Luméa accepts authenticated digital payments and cash on delivery.</p>
        </div>
        <button type="button" class="btn-modal-x" @click="showPaymentModal = false"><X :size="18" /></button>
      </div>

      <div class="payments-options-list">
        <div class="payment-method-card" :class="{ selected: selectedPaymentPref === 'khqr' }" @click="selectedPaymentPref = 'khqr'">
          <div class="pay-card-left">
            <div class="pay-logo-badge khqr-badge">KHQR</div>
            <div>
              <strong>Bakong KHQR (NBC Standard)</strong>
              <p>Dynamic scan-to-pay via ABA Mobile, Bakong, Wing, ACLEDA, and Sathapana.</p>
            </div>
          </div>
          <div class="pay-radio-check">
            <span class="radio-dot" v-if="selectedPaymentPref === 'khqr'"></span>
          </div>
        </div>

        <div class="payment-method-card" :class="{ selected: selectedPaymentPref === 'cod' }" @click="selectedPaymentPref = 'cod'">
          <div class="pay-card-left">
            <div class="pay-logo-badge cod-badge">COD</div>
            <div>
              <strong>Cash on Delivery (COD)</strong>
              <p>Pay cash in USD or KHR directly to the courier upon parcel arrival.</p>
            </div>
          </div>
          <div class="pay-radio-check">
            <span class="radio-dot" v-if="selectedPaymentPref === 'cod'"></span>
          </div>
        </div>

        <div class="payment-method-card" :class="{ selected: selectedPaymentPref === 'card' }" @click="selectedPaymentPref = 'card'">
          <div class="pay-card-left">
            <div class="pay-logo-badge card-badge">PAYWAY</div>
            <div>
              <strong>ABA PayWay / Card Payments</strong>
              <p>Direct debit or credit card payments secured through ABA Bank gateway.</p>
            </div>
          </div>
          <div class="pay-radio-check">
            <span class="radio-dot" v-if="selectedPaymentPref === 'card'"></span>
          </div>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn-modal-cancel" @click="showPaymentModal = false">Cancel</button>
        <button type="button" class="btn-modal-save" @click="savePaymentPreference">Set as Default</button>
      </div>
    </div>
  </div>

  <!-- 6. Luméa Rewards Benefits Modal -->
  <div v-if="showRewardsModal" class="account-edit-overlay" role="dialog" aria-modal="true" aria-label="Luméa Rewards" @click.self="showRewardsModal = false">
    <div class="account-modal-box rewards-modal">
      <div class="modal-head">
        <div>
          <h3>Luméa Rewards Program</h3>
          <p class="modal-subtext">Your Tier: <strong>{{ authStore.user?.tier || 'Member' }}</strong> ({{ authStore.user?.rewardPoints || 0 }} pts)</p>
        </div>
        <button type="button" class="btn-modal-x" @click="showRewardsModal = false"><X :size="18" /></button>
      </div>

      <div class="rewards-tiers-comparison">
        <div class="tier-card" :class="{ current: !isGoldMember }">
          <div class="tier-head">
            <UserCheck :size="18" />
            <h4>Member (Standard)</h4>
            <span class="tier-badge-pill" v-if="!isGoldMember">Current Tier</span>
          </div>
          <ul>
            <li>Earn 1 point per $1 spent on orders</li>
            <li>Member-only promotional deals</li>
            <li>Personalized morning &amp; evening regimens</li>
            <li>Free returns within 30 days</li>
          </ul>
        </div>

        <div class="tier-card gold" :class="{ current: isGoldMember }">
          <div class="tier-head">
            <Crown :size="18" />
            <h4>Radiant Gold / VIP</h4>
            <span class="tier-badge-pill gold" v-if="isGoldMember">Current Tier</span>
          </div>
          <ul>
            <li>Earn 2x reward points per $1 spent</li>
            <li>Complimentary express priority delivery</li>
            <li>Early access to limited atelier batches</li>
            <li>Exclusive annual birthday luxury gift</li>
          </ul>
        </div>
      </div>

      <div class="modal-foot">
        <button type="button" class="btn-modal-save" @click="showRewardsModal = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '@/stores/products'
import { useAuthStore } from '@/stores/auth'
import { useOrdersStore } from '@/stores/orders'
import { useWishlistStore } from '@/stores/wishlist'
import { useNotificationStore } from '@/stores/notification'
import AccountSidebar from '@/components/account/AccountSidebar.vue'
import ProductCard from '@/components/ProductCard.vue'
import {
  Calendar,
  Heart,
  Bookmark,
  Star,
  Crown,
  MapPin,
  Plus,
  MoreVertical,
  Check,
  Sparkles,
  X,
  LogOut,
  Package,
  ShieldCheck,
  UserCheck
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const ordersStore = useOrdersStore()
const wishlistStore = useWishlistStore()
const notificationStore = useNotificationStore()

const showAddressModal = ref(false)
const showPaymentModal = ref(false)
const showProfileModal = ref(false)
const showRewardsModal = ref(false)
const showAvatarModal = ref(false)
const showNotificationsModal = ref(false)
const showSettingsModal = ref(false)

const isGoldMember = computed(() => {
  const t = (authStore.user?.tier || '').toLowerCase()
  return t.includes('gold') || t.includes('vip') || t.includes('radiant')
})

const selectedAvatarPath = ref(authStore.userAvatar || '/images/avatars/avatar-female-1.jpg')

const avatarChoices = [
  { id: 'fem-1', label: 'Radiant Glow', category: 'Female', src: '/images/avatars/avatar-female-1.jpg' },
  { id: 'fem-2', label: 'Dewy Serene', category: 'Female', src: '/images/avatars/avatar-female-2.jpg' },
  { id: 'male-1', label: 'Refined Modern', category: 'Male', src: '/images/avatars/avatar-male-1.jpg' },
  { id: 'male-2', label: 'Warm Botanical', category: 'Male', src: '/images/avatars/avatar-male-2.jpg' },
  { id: 'neut-1', label: 'Luminous Pure', category: 'Neutral / All', src: '/images/avatars/avatar-neutral-1.jpg' },
  { id: 'found-1', label: 'Atelier Founder', category: 'Signature', src: '/images/avatar-sreynich.jpg' },
]

function openAvatarModal() {
  selectedAvatarPath.value = authStore.userAvatar || '/images/avatars/avatar-female-1.jpg'
  showAvatarModal.value = true
}

async function saveChosenAvatar() {
  if (!selectedAvatarPath.value) return
  savingProfile.value = true
  try {
    const ok = await authStore.updateProfile({ avatar: selectedAvatarPath.value })
    if (ok) {
      showAvatarModal.value = false
      notificationStore.addToast('Profile avatar updated successfully.', 'success')
    }
  } finally {
    savingProfile.value = false
  }
}

const settingsForm = reactive({
  orderUpdates: true,
  marketingNewsletter: false,
  currentPassword: '',
  newPassword: ''
})

function saveAccountSettings() {
  showSettingsModal.value = false
  notificationStore.addToast('Account settings and notification preferences saved.', 'success')
}

const selectedPaymentPref = ref(localStorage.getItem('lumea_pref_payment') || 'khqr')

function savePaymentPreference() {
  localStorage.setItem('lumea_pref_payment', selectedPaymentPref.value)
  showPaymentModal.value = false
  notificationStore.addToast(`Default checkout method set to ${selectedPaymentPref.value.toUpperCase()}.`, 'success')
}

function handleLogout() {
  authStore.logout(true)
  router.push('/login')
}

// 4 Exact Recommendations matching format/My Account.png:
const recommendedProducts = computed(() => useProductStore().allCatalogProducts.filter(p => p.stock > 0).slice(0, 4))
onMounted(() => ordersStore.fetchOrders())
const profileForm = reactive({ name: authStore.user?.name || '', phone: authStore.user?.phone || '' })
const addressForm = reactive({ name: authStore.user?.name || '', street: '', city: '', postalCode: '', country: 'Cambodia', phone: '', isDefault: true })
const savingProfile = ref(false)

async function saveAccountProfile() {
  savingProfile.value = true
  if (await authStore.updateProfile(profileForm)) showProfileModal.value = false
  savingProfile.value = false
}

async function saveAddress() {
  savingProfile.value = true
  if (await authStore.addAddress(addressForm)) showAddressModal.value = false
  savingProfile.value = false
}
</script>

<style scoped>
.account-edit-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(28, 25, 23, 0.55);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: grid;
  place-items: center;
  padding: 1.25rem;
}

.account-modal-box,
.account-edit-form {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  box-shadow: 0 12px 40px rgba(28, 25, 23, 0.15);
  border-radius: 20px;
  padding: 2rem;
  width: min(100%, 540px);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-head,
.modal-title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #F5EFEB;
}

.modal-head h3,
.modal-title-row h2 {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.modal-subtext {
  font-size: 0.85rem;
  color: #78716C;
  margin-top: 0.25rem;
}

.btn-close-modal,
.btn-modal-x {
  background: #F5EFEB;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #78716C;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-close-modal:hover,
.btn-modal-x:hover {
  background: #EFE6DD;
  color: #1C1917;
}

.modal-input {
  display: block;
  width: 100%;
  padding: 0.75rem 0.9rem;
  border: 1px solid #E5DCD3;
  border-radius: 10px;
  font-size: 0.9rem;
  color: #1C1917;
  background: #FAF8F5;
  margin-top: 0.4rem;
}

.modal-input:focus {
  outline: none;
  border-color: #8E4A3E;
  background: #FFFFFF;
}

.modal-actions-row,
.modal-foot {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #F5EFEB;
}

.btn-modal-cancel {
  padding: 0.65rem 1.25rem;
  background: #FFFFFF;
  border: 1px solid #D6C7BF;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #57534E;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-modal-cancel:hover {
  background: #FAF8F5;
}

.btn-modal-save {
  padding: 0.65rem 1.5rem;
  background: #8E4A3E;
  border: 1px solid #8E4A3E;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #FFFFFF;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-modal-save:hover:not(:disabled) {
  background: #763C32;
  border-color: #763C32;
}

/* Avatar Selection Grid */
.avatar-choices-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 1.25rem 0;
}

.avatar-pick-card {
  border: 2px solid #EFE6DD;
  border-radius: 14px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #FFFFFF;
}

.avatar-pick-card:hover {
  border-color: #D6C7BF;
  transform: translateY(-2px);
}

.avatar-pick-card.active {
  border-color: #8E4A3E;
  background: #FDF9F7;
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.15);
}

.avatar-frame {
  position: relative;
  width: 68px;
  height: 68px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 8px;
  border: 2px solid #EFE6DD;
}

.avatar-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-check-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #FFFFFF;
}

.avatar-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.2;
}

.avatar-tag {
  font-size: 0.7rem;
  color: #A8A29E;
  margin-top: 2px;
}

/* Notifications List */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 1rem 0;
}

.notification-item {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  border-radius: 12px;
}

.notification-item.unread {
  background: #FDF8F6;
  border-color: #F3DDD7;
}

.notif-icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.welcome-icon { background: #FAF0ED; color: #8E4A3E; }
.shipping-icon { background: #EDF7F6; color: #0D9488; }
.security-icon { background: #EEF2F6; color: #3B82F6; }

.notif-content {
  flex: 1;
}

.notif-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3px;
}

.notif-top strong {
  font-size: 0.86rem;
  color: #1C1917;
}

.notif-time {
  font-size: 0.72rem;
  color: #A8A29E;
}

.notif-content p {
  font-size: 0.8rem;
  color: #78716C;
  line-height: 1.4;
  margin: 0;
}

/* Settings Form */
.settings-body-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin: 1rem 0;
}

.settings-section {
  padding-bottom: 14px;
  border-bottom: 1px solid #F5EFEB;
}

.settings-sec-title {
  font-size: 0.92rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 10px;
}

.settings-toggle-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 0;
  cursor: pointer;
}

.settings-toggle-row strong {
  font-size: 0.85rem;
  color: #1C1917;
  display: block;
}

.settings-toggle-row p {
  font-size: 0.78rem;
  color: #78716C;
  margin: 2px 0 0;
}

.settings-subtext {
  font-size: 0.84rem;
  color: #78716C;
}

.danger-sec {
  border-bottom: none;
  padding-bottom: 0;
}

.danger-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #FEF2F2;
  border: 1px solid #FEE2E2;
  border-radius: 12px;
  padding: 12px 16px;
}

.danger-header strong {
  color: #991B1B;
  font-size: 0.86rem;
}

.danger-header p {
  color: #B91C1C;
  font-size: 0.76rem;
  margin: 2px 0 0;
}

.btn-danger-logout {
  padding: 6px 14px;
  background: #DC2626;
  border: none;
  border-radius: 999px;
  color: #FFFFFF;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-danger-logout:hover {
  background: #B91C1C;
}

/* Payment Methods List */
.payments-options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 1rem 0;
}

.payment-method-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border: 1.5px solid #EFE6DD;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.payment-method-card:hover {
  border-color: #D6C7BF;
}

.payment-method-card.selected {
  border-color: #8E4A3E;
  background: #FDF9F7;
}

.pay-card-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.pay-logo-badge {
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.khqr-badge { background: #E1251B; color: #FFFFFF; }
.cod-badge { background: #1C1917; color: #FFFFFF; }
.card-badge { background: #005D8E; color: #FFFFFF; }

.pay-card-left strong {
  font-size: 0.88rem;
  color: #1C1917;
  display: block;
}

.pay-card-left p {
  font-size: 0.78rem;
  color: #78716C;
  margin: 2px 0 0;
}

.pay-radio-check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #D6C7BF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.payment-method-card.selected .pay-radio-check {
  border-color: #8E4A3E;
}

.radio-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #8E4A3E;
}

/* Rewards Comparison */
.rewards-tiers-comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin: 1rem 0;
}

.tier-card {
  border: 1.5px solid #EFE6DD;
  border-radius: 14px;
  padding: 16px;
  background: #FFFFFF;
}

.tier-card.current {
  border-color: #8E4A3E;
  background: #FDF9F7;
}

.tier-card.gold.current {
  border-color: #F59E0B;
  background: #FFFDF7;
}

.tier-head {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.tier-head h4 {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1rem;
  margin: 0;
}

.tier-badge-pill {
  display: inline-block;
  padding: 2px 8px;
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 600;
  width: fit-content;
}

.tier-badge-pill.gold {
  background: #F59E0B;
}

.tier-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.tier-card li {
  font-size: 0.78rem;
  color: #57534E;
  line-height: 1.35;
  position: relative;
  padding-left: 14px;
}

.tier-card li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #8E4A3E;
  font-weight: bold;
}

/* Welcome Card Log Out Button */
.welcome-top-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.btn-banner-logout {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-banner-logout:hover {
  background: #FEF2F2;
  border-color: #FEE2E2;
  color: #DC2626;
}

/* ==========================================================================
   MY ACCOUNT PAGE (Strictly matches format/My Account.png)
   ========================================================================== */

.my-account-page {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 5rem;
}

.account-container {
  max-width: 1340px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Breadcrumbs */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.84rem;
  color: #78716C;
  padding: 0.6rem 0 0.5rem;
}

.crumb-link {
  color: #57534E;
  text-decoration: none;
}

.crumb-link:hover {
  color: #8E4A3E;
}

.crumb-sep {
  color: #A8A29E;
}

.crumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Panoramic Hero Banner matching My Account.png */
.account-hero-banner {
  background: #FFFFFF;
  border-radius: 18px;
  border: 1px solid #EFE6DD;
  box-shadow: 0 4px 18px rgba(28, 25, 23, 0.03);
  display: grid;
  grid-template-columns: 1.1fr 1.35fr;
  overflow: hidden;
  align-items: stretch;
  min-height: 250px;
  margin-bottom: 1.75rem;
}

.hero-left-content {
  padding: 1.75rem 2.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #FFFFFF;
  z-index: 2;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.15;
  letter-spacing: -0.01em;
  margin-bottom: 0.5rem;
}

.hero-desc {
  font-size: 1.15rem;
  line-height: 1.55;
  color: #57534E;
  max-width: 520px;
}

.hero-right-stage {
  position: relative;
  width: 100%;
  min-height: 250px;
  overflow: hidden;
  background: #FAF6F1;
}

.hero-banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;
  display: block;
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 15%);
  mask-image: linear-gradient(to right, transparent 0%, black 15%);
}

.hero-fade-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 120px;
  background: linear-gradient(to right, #FFFFFF, transparent);
  pointer-events: none;
  z-index: 2;
}

.banner-script-overlay {
  position: absolute;
  top: 24px;
  right: 32px;
  font-family: 'Cormorant Garamond', cursive, serif;
  font-style: italic;
  font-size: 1.65rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.15;
  text-align: right;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.95);
  pointer-events: none;
  z-index: 3;
}

/* ================= 3-COLUMN LAYOUT ================= */
.account-3col-grid {
  display: grid;
  grid-template-columns: 260px 1fr 340px;
  gap: 1.75rem;
  align-items: start;
}

/* ================= CENTER MAIN COLUMN ================= */
.dashboard-main-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Welcome Greeting Banner */
.welcome-banner-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.welcome-header-content {
  display: flex;
  flex-direction: column;
}

.greeting-pre {
  font-size: 0.9rem;
  font-weight: 500;
  color: #8E4A3E;
}

.greeting-name {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2rem;
  font-weight: 700;
  color: #1C1917;
  letter-spacing: -0.01em;
  line-height: 1.15;
  margin-bottom: 0.25rem;
}

.greeting-sub {
  font-size: 0.88rem;
  color: #57534E;
}

/* Rewards Pill inside Welcome */
.rewards-callout-pill {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  background: #FFF8F6;
  border: 1px solid #F6D7D0;
  padding: 1rem 1.25rem;
  border-radius: 12px;
}

.rewards-crown-wrap {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #8E4A3E;
  display: flex;
  align-items: center;
  justify-content: center;
}

.crown-svg {
  color: #FFFFFF;
}

.rewards-text-col {
  display: flex;
  flex-direction: column;
}

.rewards-badge-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: #8E4A3E;
}

.rewards-badge-desc {
  font-size: 0.78rem;
  color: #57534E;
  margin-bottom: 0.25rem;
}

.rewards-link-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #8E4A3E;
  cursor: pointer;
  text-align: left;
}

.rewards-link-btn:hover {
  text-decoration: underline;
}

/* 4 Counters Grid */
.stats-counters-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-counter-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  padding: 1.25rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  box-shadow: 0 2px 8px rgba(28, 25, 23, 0.02);
  text-decoration: none;
  transition: all 0.2s ease;
}

.stat-counter-card.clickable:hover {
  border-color: #D4BAA8;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(28, 25, 23, 0.06);
}

.stat-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #FAF7F2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon {
  color: #8E4A3E;
}

.stat-icon.star-active {
  color: #D4AF37;
  fill: #D4AF37;
}

.stat-text-col {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.5rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.1;
}

.stat-label {
  font-size: 0.76rem;
  color: #78716C;
  font-weight: 500;
}

/* Section Common */
.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.section-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: #1C1917;
}

.section-subtitle {
  font-size: 0.82rem;
  color: #78716C;
}

.section-view-all {
  font-size: 0.84rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
}

.section-view-all:hover {
  text-decoration: underline;
}

/* Recent Orders List */
.recent-orders-list {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.02);
}

.recent-order-row-card {
  display: grid;
  grid-template-columns: 80px 1.4fr 1.2fr 1fr 120px;
  align-items: center;
  gap: 1rem;
  padding: 1.15rem 1.5rem;
  border-bottom: 1px solid #F5EFEB;
  transition: background 0.15s ease;
}

.recent-order-row-card:last-child {
  border-bottom: none;
}

.recent-order-row-card:hover {
  background: #FAF7F2;
}

.order-thumbs-stack {
  display: flex;
  align-items: center;
  gap: 4px;
}

.order-mini-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #EFE6DD;
  background: #FAF7F2;
}

.order-mini-thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.order-meta-col {
  display: flex;
  flex-direction: column;
}

.order-id-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
}

.order-id-link:hover {
  color: #8E4A3E;
}

.order-placed-date {
  font-size: 0.78rem;
  color: #78716C;
}

.order-status-col {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator-dot.delivered {
  background-color: #2E7D32;
}

.status-indicator-dot.shipped {
  background-color: #1565C0;
}

.status-indicator-dot.processing {
  background-color: #78716C;
}

.status-indicator-dot.cancelled {
  background-color: #C62828;
}

.status-name-text {
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
}

.order-price-col {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.btn-view-order-details {
  display: inline-block;
  padding: 6px 14px;
  border: 1px solid #D4BAA8;
  background: #FFFFFF;
  color: #8E4A3E;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  transition: all 0.2s ease;
}

.btn-view-order-details:hover {
  background: #8E4A3E;
  border-color: #8E4A3E;
  color: #FFFFFF;
}

/* Recommended Cards Grid using standard ProductCard */
.recommended-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

/* ================= RIGHT ASIDE COLUMN ================= */
.dashboard-aside-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.aside-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.aside-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.15rem;
}

.aside-card-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.1rem;
  font-weight: 600;
  color: #1C1917;
}

.aside-manage-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
}

.aside-manage-btn:hover {
  text-decoration: underline;
}

/* Address Card */
.saved-address-body {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.default-pill-badge {
  display: inline-block;
  align-self: flex-start;
  padding: 2px 8px;
  background: #FFF5F2;
  color: #8E4A3E;
  border: 1px solid #F6D7D0;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}

.address-details-wrap {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.address-pin-icon {
  color: #8E4A3E;
  margin-top: 2px;
  flex-shrink: 0;
}

.address-text-content {
  font-size: 0.82rem;
  line-height: 1.45;
  color: #57534E;
}

.addr-name {
  color: #1C1917;
  font-size: 0.86rem;
}

.addr-phone {
  display: block;
  margin-top: 4px;
  color: #78716C;
}

.btn-add-dashed-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  width: 100%;
  padding: 0.65rem 1rem;
  background: #FFFFFF;
  border: 1px dashed #D4BAA8;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.btn-add-dashed-action:hover {
  background: #FDF2EE;
  border-color: #8E4A3E;
}

/* Payment Methods List */
.payment-methods-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.payment-row-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #F5EFEB;
}

.payment-row-item:last-of-type {
  border-bottom: none;
}

.payment-provider-icon {
  width: 38px;
  height: 26px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-size: 0.68rem;
  font-weight: 700;
  flex-shrink: 0;
}

.payment-meta-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.payment-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pay-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
}

.default-tag-pill {
  font-size: 0.65rem;
  padding: 1px 5px;
  background: #E8F5E9;
  color: #2E7D32;
  border-radius: 3px;
  font-weight: 600;
}

.pay-expiry {
  font-size: 0.74rem;
  color: #78716C;
}

.pay-options-btn {
  background: none;
  border: none;
  color: #A8A29E;
  cursor: pointer;
  padding: 4px;
}

/* Luméa Rewards Promo Card */
.rewards-promo-card {
  background: linear-gradient(135deg, #FFF9F6 0%, #FBF0EB 100%);
  border-color: #F0D5CD;
}

.rewards-promo-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 2px;
}

.rewards-promo-tagline {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 1rem;
}

.rewards-perks-bullets {
  list-style: none;
  padding: 0;
  margin: 0 0 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.rewards-perks-bullets li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #57534E;
}

.check-perk-icon {
  color: #8E4A3E;
  flex-shrink: 0;
}

.btn-rewards-learn-more {
  width: 100%;
  padding: 0.65rem 1rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(142, 74, 62, 0.2);
  transition: all 0.2s ease;
}

.btn-rewards-learn-more:hover {
  background: #76392F;
}

/* Responsive */
.my-account-page {
  max-width: 100%;
  overflow-x: clip;
}

@media (max-width: 1200px) {
  .account-3col-grid {
    grid-template-columns: 240px 1fr;
  }
  .dashboard-aside-column {
    grid-column: span 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .rewards-promo-card {
    grid-column: span 2;
  }
}

@media (max-width: 900px) {
  .account-hero-banner {
    grid-template-columns: 1fr;
  }
  .hero-right-stage {
    min-height: 180px;
  }
  .account-3col-grid {
    grid-template-columns: 1fr;
  }
  .stats-counters-grid {
    grid-template-columns: 1fr 1fr;
  }
  .recommended-cards-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .account-container {
    padding: 0 0.85rem;
  }
  .account-hero-banner {
    padding: 1.5rem 1rem;
    min-height: auto;
  }
  .hero-title {
    font-size: 2rem;
  }
  .hero-right-stage {
    display: none;
  }
  .welcome-banner-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1.25rem;
    padding: 1.25rem;
  }
  .stats-counters-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  .recent-order-row-card {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 1rem;
  }
  .recent-order-row-card .order-action-col {
    width: 100%;
    margin-top: 0.25rem;
  }
  .btn-view-order-details {
    width: 100%;
    text-align: center;
    padding: 0.6rem;
  }
  .recommended-cards-grid {
    grid-template-columns: 1fr;
  }
  .dashboard-aside-column {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 360px) {
  .account-container {
    padding: 0 0.5rem;
  }
  .welcome-banner-card {
    padding: 1rem 0.75rem;
  }
  .greeting-name {
    font-size: 1.5rem;
  }
  .rewards-callout-pill {
    padding: 0.75rem;
  }
  .stat-counter-card {
    padding: 0.85rem 0.75rem;
  }
}
</style>
