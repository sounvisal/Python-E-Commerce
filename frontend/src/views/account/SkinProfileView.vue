<template>
  <div class="lumea-skin-profile-view">
    <div class="container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumb-nav">
        <router-link to="/">Home</router-link>
        <span class="sep">›</span>
        <router-link to="/account/profile">My Account</router-link>
        <span class="sep">›</span>
        <span class="current">Beauty Profile</span>
      </nav>

      <!-- Top Header Banner matching Skin Profile.png -->
      <div class="profile-hero-banner">
        <div class="hero-left-content">
          <h1 class="profile-main-title">My Skin Profile</h1>
          <p class="profile-main-desc">
            Your personalized skin profile helps us recommend the best products and advice just for you.
          </p>
        </div>

        <div class="hero-right-stage">
            <img
              src="/images/banners/banner-skin-concerns-clean.jpg"
              alt="Luméa Radiant Skin Profile"
              class="hero-banner-image"
            />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Know Your Skin <Heart :size="16" class="script-heart-icon" /><br>Love Your Skin <Heart :size="16" class="script-heart-icon" /><br>Be Your Best You.</span>
          </div>

          <div class="banner-cta-group">
            <div class="banner-badge-text">
              <span>Real Care.<br>Real Results.</span>
            </div>
            <router-link to="/quiz/questions" class="btn-banner-retake">
              <RotateCcw :size="15" />
              <span>Retake Skin Quiz</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Main Layout: Sidebar + Profile Cards -->
      <div class="account-body-grid">
        <!-- ========================================================= -->
        <!-- LEFT: ACCOUNT NAVIGATION SIDEBAR                          -->
        <!-- ========================================================= -->
        <aside class="account-sidebar">
          <div class="user-profile-badge">
            <img src="/images/avatar-sreynich.jpg" alt="Sreynich Chan" class="user-avatar-img" />
            <h3 class="user-name">Sreynich Chan</h3>
            <span class="user-email">sreynich.chan@example.com</span>
          </div>

          <nav class="account-nav-list">
            <router-link to="/account/profile" class="nav-item">
              <Home :size="18" />
              <span>Overview</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item">
              <Package :size="18" />
              <span>Orders</span>
            </router-link>
            <router-link to="/wishlist" class="nav-item">
              <Heart :size="18" />
              <span>Wishlist</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item">
              <MapPin :size="18" />
              <span>Addresses</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item">
              <CreditCard :size="18" />
              <span>Payment Methods</span>
            </router-link>
            <router-link to="/wishlist" class="nav-item">
              <Bookmark :size="18" />
              <span>Saved Items</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item is-active">
              <Sprout :size="18" />
              <span>Beauty Profile</span>
            </router-link>
            <router-link to="/account/journal" class="nav-item">
              <BookOpen :size="18" />
              <span>Skincare Journal</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item">
              <Bell :size="18" />
              <span>Notifications</span>
            </router-link>
            <router-link to="/account/profile" class="nav-item">
              <Settings :size="18" />
              <span>Account Settings</span>
            </router-link>
          </nav>

          <!-- Support Card -->
          <div class="sidebar-help-card">
            <div class="help-header">
              <Headphones :size="20" class="help-icon" />
              <div>
                <h4 class="help-title">Need Help?</h4>
                <p class="help-desc">Our customer support team is here for you.</p>
              </div>
            </div>
            <router-link to="/contact" class="btn-help-contact">
              Contact Us
            </router-link>
          </div>
        </aside>

        <!-- ========================================================= -->
        <!-- CENTER & RIGHT: PROFILE DETAILS & ROUTINE                 -->
        <!-- ========================================================= -->
        <main class="account-content-main">
          <!-- 6 Grid Characteristics Cards -->
          <div class="characteristics-grid">
            <!-- 1. Skin Type Card -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Skin Type</span>
                <button class="btn-edit-pill" @click="openEditModal('skinType')">Edit</button>
              </div>
              <div class="last-updated-text">Last updated: {{ quizStore.lastUpdated }}</div>
              <div class="skin-type-highlight-row">
                <div class="char-icon-circle">
                  <Droplets :size="22" />
                </div>
                <div>
                  <h4 class="char-large-name">{{ quizStore.currentSkinType }}</h4>
                  <p class="char-desc">{{ quizStore.currentSkinDesc }}</p>
                </div>
              </div>
            </div>

            <!-- 2. Skin Characteristics -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Skin Characteristics</span>
                <button class="btn-edit-pill" @click="openEditModal('characteristics')">Edit</button>
              </div>
              <div class="char-badges-quad">
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Sparkles :size="16" /></div>
                  <span class="quad-title">Pores</span>
                  <span class="quad-sub">Visible in T-zone</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Smile :size="16" /></div>
                  <span class="quad-title">Uneven Tone</span>
                  <span class="quad-sub">Occasional</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Droplets :size="16" /></div>
                  <span class="quad-title">Sensitivity</span>
                  <span class="quad-sub">Slightly sensitive</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Flame :size="16" /></div>
                  <span class="quad-title">Breakouts</span>
                  <span class="quad-sub">Occasional</span>
                </div>
              </div>
            </div>

            <!-- 3. Skin Goals -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Skin Goals</span>
                <button class="btn-edit-pill" @click="openEditModal('goals')">Edit</button>
              </div>
              <div class="char-badges-quad">
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Sparkles :size="16" /></div>
                  <span class="quad-title">Clearer Skin</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Sun :size="16" /></div>
                  <span class="quad-title">Brighter Tone</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Droplets :size="16" /></div>
                  <span class="quad-title">Hydration</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Waves :size="16" /></div>
                  <span class="quad-title">Smoother Texture</span>
                </div>
              </div>
            </div>

            <!-- 4. Your Concerns -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Concerns</span>
                <button class="btn-edit-pill" @click="openEditModal('concerns')">Edit</button>
              </div>
              <div class="concerns-tags-cloud">
                <span class="concern-pill-tag">Oiliness</span>
                <span class="concern-pill-tag">Enlarged Pores</span>
                <span class="concern-pill-tag">Uneven Skin Tone</span>
                <span class="concern-pill-tag">Occasional Breakouts</span>
              </div>
            </div>

            <!-- 5. Your Lifestyle -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Lifestyle</span>
                <button class="btn-edit-pill" @click="openEditModal('lifestyle')">Edit</button>
              </div>
              <div class="char-badges-quad">
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Building :size="16" /></div>
                  <span class="quad-title">Mostly Indoors</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Sun :size="16" /></div>
                  <span class="quad-title">Moderate Sun Exposure</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Clock :size="16" /></div>
                  <span class="quad-title">Busy Schedule</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Sparkles :size="16" /></div>
                  <span class="quad-title">Occasional Makeup</span>
                </div>
              </div>
            </div>

            <!-- 6. Your Environment -->
            <div class="char-card">
              <div class="char-card-header">
                <span class="char-card-title">Your Environment</span>
                <button class="btn-edit-pill" @click="openEditModal('environment')">Edit</button>
              </div>
              <div class="char-badges-quad env-quad">
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Building :size="16" /></div>
                  <span class="quad-title">Urban Area</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Thermometer :size="16" /></div>
                  <span class="quad-title">Warm & Humid Climate</span>
                </div>
                <div class="char-quad-item">
                  <div class="quad-icon-box"><Wind :size="16" /></div>
                  <span class="quad-title">Some Pollution Exposure</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom: Recommended Routine Embed + Sidebar Tips -->
          <div class="routine-and-tips-row">
            <!-- Left 2/3: Routine Embed -->
            <div class="profile-routine-embed">
              <div class="routine-embed-header">
                <div>
                  <h3 class="embed-title">Your Recommended Routine</h3>
                  <p class="embed-desc">A personalized routine based on your skin profile.</p>
                </div>
                <router-link to="/routine" class="link-full-routine">
                  <span>View Full Routine</span>
                  <ArrowRight :size="15" />
                </router-link>
              </div>

              <!-- Time Toggle -->
              <div class="embed-time-toggle">
                <button
                  class="embed-btn"
                  :class="{ 'is-active': activeRoutineTime === 'morning' }"
                  @click="activeRoutineTime = 'morning'"
                >
                  <Sun :size="16" />
                  <span>Morning</span>
                </button>
                <button
                  class="embed-btn"
                  :class="{ 'is-active': activeRoutineTime === 'evening' }"
                  @click="activeRoutineTime = 'evening'"
                >
                  <Moon :size="16" />
                  <span>Evening</span>
                </button>
                <div class="embed-est-time">
                  <Clock :size="14" />
                  <span>Est. 5 minutes</span>
                </div>
              </div>

              <!-- Step Miniatures Flow -->
              <div class="embed-steps-track">
                <template v-for="(prod, idx) in routineProducts" :key="prod.id">
                  <div class="embed-step-pill">
                    <div class="embed-step-number">{{ prod.step }}</div>
                    <span class="embed-step-tag">{{ prod.stepName }}</span>
                    <div class="embed-img-wrap">
                      <img :src="prod.image_url" :alt="prod.name" class="embed-img" />
                    </div>
                    <span class="embed-prod-name">{{ prod.name }}</span>
                  </div>
                  <div class="embed-arrow" v-if="idx < routineProducts.length - 1">
                    <ArrowRight :size="16" />
                  </div>
                </template>
              </div>

              <div class="embed-cta-footer">
                <router-link to="/routine" class="btn-shop-my-routine">
                  Shop My Routine
                </router-link>
              </div>
            </div>

            <!-- Right 1/3: Tips + Promo -->
            <div class="profile-side-tips-column">
              <div class="side-tips-card">
                <div class="tips-card-head">
                  <Lightbulb :size="18" class="tips-bulb" />
                  <h4 class="tips-head-text">Personalized Tips</h4>
                </div>
                <ul class="tips-bullet-list">
                  <li>
                    <Check :size="14" class="tip-check-mark" />
                    <span>Use a gentle cleanser twice daily.</span>
                  </li>
                  <li>
                    <Check :size="14" class="tip-check-mark" />
                    <span>Keep your skin hydrated.</span>
                  </li>
                  <li>
                    <Check :size="14" class="tip-check-mark" />
                    <span>Don't skip sunscreen, even on cloudy days.</span>
                  </li>
                  <li>
                    <Check :size="14" class="tip-check-mark" />
                    <span>Be consistent — results take time.</span>
                  </li>
                  <li>
                    <Check :size="14" class="tip-check-mark" />
                    <span>Adjust products based on how your skin feels.</span>
                  </li>
                </ul>
              </div>

              <div class="side-promo-card">
                <h4 class="side-promo-title">Better Skin<br>Brighter Days</h4>
                <p class="side-promo-sub">Curated just for your unique skin.</p>
                <router-link to="/routine" class="btn-side-promo">
                  Shop Recommended Products
                </router-link>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useQuizStore } from '@/stores/quiz'
import {
  ArrowRight,
  Bell,
  Bookmark,
  BookOpen,
  Building,
  Check,
  Clock,
  CreditCard,
  Droplets,
  Flame,
  Headphones,
  Heart,
  Home,
  Lightbulb,
  MapPin,
  Moon,
  Package,
  RotateCcw,
  Settings,
  Smile,
  Sparkles,
  Sprout,
  Sun,
  Thermometer,
  Waves,
  Wind
} from 'lucide-vue-next'
import { computed, ref } from 'vue'

const quizStore = useQuizStore()
const activeRoutineTime = ref('morning')

const routineProducts = computed(() => {
  return activeRoutineTime.value === 'morning'
    ? quizStore.recommendedRoutineProducts
    : quizStore.eveningRoutineProducts
})

function openEditModal(section) {
  // Direct to questions for updating or modal
  window.location.href = '/quiz/questions'
}
</script>

<style scoped>
.lumea-skin-profile-view {
  background-color: #FAF8F5;
  min-height: 100vh;
  color: #242721;
  padding-bottom: 90px;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ================= BREADCRUMBS ================= */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #7A7269;
  padding: 20px 0 16px;
}

.breadcrumb-nav a {
  color: #5C5852;
  text-decoration: none;
}

.breadcrumb-nav a:hover {
  color: #9E3332;
}

.breadcrumb-nav .sep {
  color: #B5ABA0;
}

.breadcrumb-nav .current {
  color: #9E3332;
  font-weight: 600;
}

/* ================= TOP HERO BANNER ================= */
.profile-hero-banner {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  display: grid;
  grid-template-columns: 1.1fr 1.35fr;
  margin-bottom: 32px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
  min-height: 275px;
}

.hero-left-content {
  padding: 36px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #FFFFFF;
  z-index: 2;
}

.profile-main-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  margin-bottom: 12px;
  line-height: 1.15;
}

.profile-main-desc {
  font-size: 1.15rem;
  line-height: 1.55;
  color: #5C5852;
}

.hero-right-stage {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 275px;
  overflow: hidden;
  background: #F8EFE9;
}

.hero-banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
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
}

.banner-script-overlay {
  position: absolute;
  top: 24px;
  left: 40px;
  font-family: 'Cormorant Garamond', cursive, serif;
  font-style: italic;
  font-size: 1.65rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.15;
  text-shadow: 0 2px 12px rgba(255, 255, 255, 0.95);
  pointer-events: none;
}

.script-heart-icon {
  display: inline-block;
  vertical-align: -2px;
  margin-left: 3px;
  margin-right: 3px;
  color: #8E4A3E;
  fill: #8E4A3E;
}

.banner-cta-group {
  position: absolute;
  top: 50%;
  right: 28px;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(8px);
  padding: 16px 20px;
  border-radius: 16px;
  border: 1px solid rgba(234, 219, 206, 0.8);
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.08);
}

.banner-badge-text {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1A1D1A;
  text-align: right;
  line-height: 1.25;
}

.btn-banner-retake {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: #9E3332;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(158, 51, 50, 0.2);
  transition: all 0.2s ease;
}

.btn-banner-retake:hover {
  background-color: #832726;
  border-color: #832726;
}


/* ================= ACCOUNT BODY GRID ================= */
.account-body-grid {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 32px;
  align-items: start;
}

/* ---------------- LEFT SIDEBAR ---------------- */
.account-sidebar {
  position: sticky;
  top: 90px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-profile-badge {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 24px 20px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.user-avatar-img {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
  border: 2px solid #EADBCE;
}

.user-name {
  font-family: 'Playfair Display', serif;
  font-size: 17px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 3px;
}

.user-email {
  font-size: 11.5px;
  color: #7A7269;
}

.account-nav-list {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  color: #4A453F;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: #FAF4F0;
  color: #9E3332;
}

.nav-item.is-active {
  background-color: #F8EFE9;
  color: #9E3332;
  font-weight: 700;
}

.sidebar-help-card {
  background: #FFFDF9;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 20px;
}

.help-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 14px;
}

.help-icon {
  color: #9E3332;
  flex-shrink: 0;
  margin-top: 2px;
}

.help-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #242721;
  margin-bottom: 2px;
}

.help-desc {
  font-size: 11.5px;
  line-height: 1.4;
  color: #7A7269;
}

.btn-help-contact {
  display: block;
  text-align: center;
  padding: 9px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 12.5px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-help-contact:hover {
  background-color: #FAF4F0;
}

/* ---------------- MAIN CONTENT ---------------- */
.account-content-main {
  min-width: 0;
}

.characteristics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.char-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 20px 18px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.char-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.char-card-title {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1A1D1A;
}

.btn-edit-pill {
  padding: 3px 12px;
  border-radius: 999px;
  border: 1px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit-pill:hover {
  background: #9E3332;
  color: #FFFFFF;
}

.last-updated-text {
  font-size: 11px;
  color: #8C7B70;
  margin-bottom: 12px;
}

.skin-type-highlight-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.char-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #F4E8DF;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.char-large-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #9E3332;
  margin-bottom: 2px;
}

.char-desc {
  font-size: 11px;
  color: #6C665D;
  line-height: 1.35;
}

.char-badges-quad {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.char-badges-quad.env-quad {
  grid-template-columns: repeat(3, 1fr);
}

.char-quad-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
}

.quad-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #FAF3EE;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #F0DFD3;
}

.quad-title {
  font-size: 10.5px;
  font-weight: 600;
  color: #38342F;
  line-height: 1.25;
}

.quad-sub {
  font-size: 9.5px;
  color: #8C7B70;
  line-height: 1.2;
}

.concerns-tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.concern-pill-tag {
  background: #F8EFE9;
  color: #4A453F;
  font-size: 11.5px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid #EFE0D5;
}

/* Routine & Tips Row */
.routine-and-tips-row {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 20px;
  align-items: start;
}

.profile-routine-embed {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.routine-embed-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.embed-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 2px;
}

.embed-desc {
  font-size: 12.5px;
  color: #7A7269;
}

.link-full-routine {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 600;
  color: #9E3332;
  text-decoration: none;
}

.link-full-routine:hover {
  text-decoration: underline;
}

.embed-time-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.embed-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 16px;
  border-radius: 999px;
  border: 1.5px solid #E5DBD1;
  background: #FFFFFF;
  font-size: 12px;
  font-weight: 600;
  color: #5C5852;
  cursor: pointer;
}

.embed-btn.is-active {
  background-color: #9E3332;
  border-color: #9E3332;
  color: #FFFFFF;
}

.embed-est-time {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11.5px;
  font-weight: 600;
  color: #7A7269;
  margin-left: auto;
}

.embed-steps-track {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 14px;
  margin-bottom: 20px;
}

.embed-step-pill {
  flex: 0 0 110px;
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  padding: 10px 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.embed-step-number {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #F4EBE3;
  color: #9E3332;
  font-size: 10.5px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2px;
}

.embed-step-tag {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  color: #7A7269;
  margin-bottom: 6px;
}

.embed-img-wrap {
  width: 60px;
  height: 60px;
  margin-bottom: 6px;
}

.embed-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.embed-prod-name {
  font-size: 10px;
  font-weight: 600;
  color: #242721;
  line-height: 1.25;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.embed-arrow {
  color: #C2B7AC;
  flex-shrink: 0;
}

.embed-cta-footer {
  text-align: center;
}

.btn-shop-my-routine {
  display: inline-block;
  padding: 12px 36px;
  border-radius: 999px;
  background-color: #9E3332;
  color: #FFFFFF;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-shop-my-routine:hover {
  background-color: #832726;
}

/* Side Tips */
.profile-side-tips-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.side-tips-card {
  background: #FFFDF9;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 18px;
}

.tips-card-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tips-bulb {
  color: #9E3332;
}

.tips-head-text {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  font-weight: 600;
  color: #1A1D1A;
}

.tips-bullet-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.tips-bullet-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 11.5px;
  line-height: 1.4;
  color: #5C5852;
}

.tip-check-mark {
  color: #9E3332;
  flex-shrink: 0;
  margin-top: 1px;
}

.side-promo-card {
  background: linear-gradient(135deg, #F9EDE4 0%, #F5E4D7 100%);
  border: 1px solid #EADBCE;
  border-radius: 18px;
  padding: 20px;
  text-align: center;
}

.side-promo-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #1A1D1A;
  line-height: 1.25;
  margin-bottom: 4px;
}

.side-promo-sub {
  font-size: 11.5px;
  color: #6C665D;
  margin-bottom: 14px;
}

.btn-side-promo {
  display: block;
  padding: 10px;
  border-radius: 999px;
  background-color: #9E3332;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-side-promo:hover {
  background-color: #832726;
}

/* Responsive */
@media (max-width: 1080px) {
  .account-body-grid {
    grid-template-columns: 1fr;
  }
  .account-sidebar {
    position: static;
  }
  .characteristics-grid {
    grid-template-columns: 1fr 1fr;
  }
  .routine-and-tips-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .profile-hero-banner {
    flex-direction: column;
    gap: 20px;
  }
  .characteristics-grid {
    grid-template-columns: 1fr;
  }
}
</style>
