<template>
  <div class="lumea-journal-view">
    <div class="container">
      <!-- Breadcrumbs -->
      <nav class="breadcrumb-nav">
        <router-link to="/">Home</router-link>
        <span class="sep">›</span>
        <router-link to="/account/profile">My Account</router-link>
        <span class="sep">›</span>
        <span class="current">Skincare Journal</span>
      </nav>

      <!-- Top Header Banner matching Skincare Journal.png -->
      <div class="journal-hero-banner">
        <div class="hero-left-content">
          <h1 class="journal-main-title">Skincare Journal</h1>
          <p class="journal-main-desc">
            Track your skincare journey. See your progress. Build healthier, happier skin.
          </p>
        </div>

        <div class="hero-right-stage">
            <img
              src="/images/banners/banner-about-clean.jpg"
              alt="Luméa Skincare Journey Progress"
              class="hero-banner-image"
            />
          <div class="hero-fade-overlay"></div>
          <div class="banner-script-overlay">
            <span>Small Steps<br>Real Changes. ♡</span>
          </div>

          <div class="banner-cta-group">
            <div class="banner-badge-text">
              <span>A Healthier<br>You, Day by Day.</span>
            </div>
            <button class="btn-banner-add-entry" @click="showEntryModal = true">
              <Plus :size="16" />
              <span>Add New Entry</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Layout: Sidebar + Journal Feed + Right Widgets -->
      <div class="journal-body-grid">
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
            <router-link to="/account/profile" class="nav-item">
              <Sprout :size="18" />
              <span>Beauty Profile</span>
            </router-link>
            <router-link to="/account/journal" class="nav-item is-active">
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
        <!-- CENTER: JOURNAL FEED & TIMELINE                           -->
        <!-- ========================================================= -->
        <main class="journal-feed-main">
          <!-- Top Sub-Tabs Navigation -->
          <div class="journal-sub-tabs">
            <button
              v-for="tab in subTabs"
              :key="tab.id"
              class="sub-tab-btn"
              :class="{ 'is-active': activeSubTab === tab.id }"
              @click="activeSubTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Entries Header & Filter Dropdown -->
          <div class="entries-section-header">
            <h2 class="entries-title">Recent Entries</h2>
            <div class="entries-filter-dropdown">
              <select v-model="filterSelection" class="custom-select-filter">
                <option value="all">All Entries</option>
                <option value="breakouts">Breakouts</option>
                <option value="hydration">Hydration</option>
                <option value="glowing">Glowing</option>
              </select>
            </div>
          </div>

          <!-- Entries Timeline List -->
          <div class="entries-timeline-list">
            <div
              v-for="entry in displayedEntries"
              :key="entry.id"
              class="journal-entry-card"
            >
              <!-- Left Date Column -->
              <div class="entry-date-column">
                <div class="date-large-number">{{ entry.dayNum }}</div>
                <div class="date-month-year">{{ entry.monthStr }}</div>
                <div class="date-weekday">{{ entry.dayOfWeek }}</div>
              </div>

              <!-- Main Entry Body -->
              <div class="entry-body-content">
                <div class="entry-header-row">
                  <h3 class="entry-headline">{{ entry.title }}</h3>
                </div>

                <p class="entry-notes-text">{{ entry.notes }}</p>

                <div class="entry-tags-row">
                  <span
                    v-for="tag in entry.tags"
                    :key="tag"
                    class="entry-pill-tag"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>

              <!-- Right: Products Used -->
              <div class="entry-products-column">
                <div class="products-header">
                  <span class="products-label">Products Used</span>
                  <button class="options-icon-btn" aria-label="Entry options">
                    <MoreHorizontal :size="16" />
                  </button>
                </div>

                <div class="products-mini-thumbs">
                  <div
                    v-for="(imgSrc, idx) in entry.productImages"
                    :key="idx"
                    class="mini-thumb-wrap"
                  >
                    <img :src="imgSrc" alt="Product used" class="mini-thumb-img" />
                  </div>
                  <div class="extra-count-badge" v-if="entry.extraCount > 0">
                    +{{ entry.extraCount }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>

        <!-- ========================================================= -->
        <!-- RIGHT: STREAK, MONTHLY CALENDAR, SKIN INSIGHTS            -->
        <!-- ========================================================= -->
        <aside class="journal-right-widgets">
          <!-- 1. Streak Card -->
          <div class="widget-streak-card">
            <div class="streak-icon-box">
              <Flame :size="24" class="streak-flame" />
            </div>
            <div class="streak-info">
              <div class="streak-days-count">{{ journalStore.streak }} Days</div>
              <p class="streak-tagline">Keep it going! Consistency leads to real results.</p>
            </div>
          </div>

          <!-- 2. Monthly Calendar Card -->
          <div class="widget-calendar-card">
            <div class="calendar-header-nav">
              <span class="calendar-month-title">Monthly Overview</span>
              <div class="cal-nav-buttons">
                <button class="cal-arrow-btn" aria-label="Previous month"><ChevronLeft :size="16" /></button>
                <span class="cal-current-month">June 2025</span>
                <button class="cal-arrow-btn" aria-label="Next month"><ChevronRight :size="16" /></button>
              </div>
            </div>

            <!-- Calendar Days Grid -->
            <div class="calendar-grid">
              <div class="cal-day-name" v-for="d in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="d">
                {{ d }}
              </div>
              <div
                v-for="day in 30"
                :key="day"
                class="cal-day-cell"
                :class="{ 'is-logged': isDayLogged(day) }"
              >
                <span>{{ day }}</span>
              </div>
            </div>
          </div>

          <!-- 3. Skin Insights Card -->
          <div class="widget-insights-card">
            <div class="insights-card-head">
              <h4 class="insights-title">Skin Insights</h4>
              <router-link to="/account/profile" class="link-insights-view-all">
                <span>View All</span>
                <ArrowRight :size="13" />
              </router-link>
            </div>

            <div class="insights-items-list">
              <div class="insight-row">
                <div class="insight-icon-circle">
                  <BarChart3 :size="16" />
                </div>
                <div>
                  <h5 class="insight-heading">Your skin looks brighter</h5>
                  <p class="insight-subtext">You've reported brighter skin 5 times this month.</p>
                </div>
              </div>

              <div class="insight-row">
                <div class="insight-icon-circle">
                  <Droplets :size="16" />
                </div>
                <div>
                  <h5 class="insight-heading">Hydration is improving</h5>
                  <p class="insight-subtext">Your skin feels more hydrated compared to last month.</p>
                </div>
              </div>

              <div class="insight-row">
                <div class="insight-icon-circle">
                  <Sprout :size="16" />
                </div>
                <div>
                  <h5 class="insight-heading">Fewer breakouts</h5>
                  <p class="insight-subtext">You've had 60% fewer breakouts than last month.</p>
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- ============================================================= -->
    <!-- ADD ENTRY MODAL                                               -->
    <!-- ============================================================= -->
    <div class="modal-backdrop" v-if="showEntryModal" @click.self="showEntryModal = false">
      <div class="entry-modal-surface animate-fade-in-up">
        <div class="modal-header">
          <h3 class="modal-title">Add Journal Entry</h3>
          <button class="modal-close-btn" @click="showEntryModal = false">
            <X :size="20" />
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Entry Title</label>
            <input
              type="text"
              v-model="newEntryTitle"
              placeholder="e.g. Glowing skin, feeling hydrated"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label">How does your skin feel today?</label>
            <textarea
              v-model="newEntryNotes"
              rows="3"
              placeholder="Note down any improvements, dryness, redness, or reactions..."
              class="form-textarea"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">Select Tags</label>
            <div class="tags-picker-row">
              <button
                v-for="t in availableTags"
                :key="t"
                type="button"
                class="tag-pick-btn"
                :class="{ 'is-active': selectedTags.includes(t) }"
                @click="toggleTag(t)"
              >
                {{ t }}
              </button>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-modal-cancel" @click="showEntryModal = false">Cancel</button>
          <button class="btn-modal-save" @click="submitNewEntry">Save Entry</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useJournalStore } from '@/stores/journal'
import {
  ArrowRight,
  BarChart3,
  Bell,
  Bookmark,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  CreditCard,
  Droplets,
  Flame,
  Headphones,
  Heart,
  Home,
  MapPin,
  MoreHorizontal,
  Package,
  Plus,
  Settings,
  Sprout,
  X
} from 'lucide-vue-next'
import { computed, ref } from 'vue'

const journalStore = useJournalStore()

const activeSubTab = ref('all')
const filterSelection = ref('all')
const showEntryModal = ref(false)

const newEntryTitle = ref('')
const newEntryNotes = ref('')
const selectedTags = ref(['Hydrated', 'Glowing'])

const availableTags = [
  'Hydrated',
  'Glowing',
  'Less Oil',
  'Brighter',
  'No Breakouts',
  'Dryness',
  'Used Mask',
  'Calm'
]

const subTabs = [
  { id: 'all', label: 'All Entries' },
  { id: 'progress', label: 'Progress' },
  { id: 'photos', label: 'Photos' },
  { id: 'products', label: 'Products Used' },
  { id: 'insights', label: 'Skin Insights' }
]

function isDayLogged(day) {
  return journalStore.loggedDays.includes(day)
}

const displayedEntries = computed(() => {
  return journalStore.entries
})

function toggleTag(t) {
  if (selectedTags.value.includes(t)) {
    selectedTags.value = selectedTags.value.filter(item => item !== t)
  } else {
    selectedTags.value.push(t)
  }
}

function submitNewEntry() {
  if (!newEntryTitle.value.trim()) return

  journalStore.addEntry({
    title: newEntryTitle.value,
    notes: newEntryNotes.value,
    tags: selectedTags.value.length ? selectedTags.value : ['Glowing'],
    productImages: [
      '/images/prod-anua-toner.jpg',
      '/images/prod-ordinary.jpg',
      '/images/prod-laneige.jpg'
    ],
    extraCount: 1
  })

  newEntryTitle.value = ''
  newEntryNotes.value = ''
  showEntryModal.value = false
}
</script>

<style scoped>
.lumea-journal-view {
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
.journal-hero-banner {
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

.journal-main-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  margin-bottom: 12px;
  line-height: 1.15;
}

.journal-main-desc {
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

.btn-banner-add-entry {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  border-radius: 999px;
  background-color: #9E3332;
  border: none;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(158, 51, 50, 0.25);
  transition: all 0.2s ease;
}

.btn-banner-add-entry:hover {
  background-color: #832726;
  transform: translateY(-1px);
}


/* ================= BODY 3-COLUMN GRID ================= */
.journal-body-grid {
  display: grid;
  grid-template-columns: 260px 1fr 280px;
  gap: 28px;
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

/* ---------------- CENTER JOURNAL FEED ---------------- */
.journal-feed-main {
  min-width: 0;
}

.journal-sub-tabs {
  display: flex;
  gap: 28px;
  border-bottom: 1.5px solid #EFE6DD;
  margin-bottom: 24px;
}

.sub-tab-btn {
  background: transparent;
  border: none;
  font-size: 14px;
  font-weight: 600;
  color: #7A7269;
  padding-bottom: 12px;
  cursor: pointer;
  position: relative;
  transition: color 0.2s ease;
}

.sub-tab-btn:hover {
  color: #1A1D1A;
}

.sub-tab-btn.is-active {
  color: #9E3332;
}

.sub-tab-btn.is-active::after {
  content: '';
  position: absolute;
  bottom: -1.5px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #9E3332;
}

.entries-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.entries-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #1A1D1A;
}

.custom-select-filter {
  padding: 8px 16px;
  border-radius: 999px;
  border: 1.5px solid #E5DBD1;
  background-color: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  color: #4A453F;
  outline: none;
  cursor: pointer;
}

/* Timeline Cards */
.entries-timeline-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.journal-entry-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 24px 20px;
  display: grid;
  grid-template-columns: 80px 1fr 180px;
  gap: 20px;
  align-items: center;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.journal-entry-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(36, 39, 33, 0.08);
}

/* Date col */
.entry-date-column {
  text-align: center;
  border-right: 1px solid #F0E8DF;
  padding-right: 16px;
}

.date-large-number {
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 600;
  color: #1A1D1A;
  line-height: 1;
  margin-bottom: 4px;
}

.date-month-year {
  font-size: 11px;
  font-weight: 600;
  color: #7A7269;
  line-height: 1.2;
}

.date-weekday {
  font-size: 11px;
  color: #9E3332;
  font-weight: 600;
}

/* Content */
.entry-body-content {
  min-width: 0;
}

.entry-headline {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 6px;
}

.entry-notes-text {
  font-size: 13px;
  color: #5C5852;
  line-height: 1.5;
  margin-bottom: 12px;
}

.entry-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.entry-pill-tag {
  background: #FAF0E8;
  color: #7A423B;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid #F0DFD3;
}

/* Products Column */
.entry-products-column {
  border-left: 1px solid #F0E8DF;
  padding-left: 18px;
}

.products-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.products-label {
  font-size: 11px;
  font-weight: 600;
  color: #8C7B70;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.options-icon-btn {
  background: transparent;
  border: none;
  color: #B5ABA0;
  cursor: pointer;
  padding: 2px;
}

.products-mini-thumbs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-thumb-wrap {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mini-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.extra-count-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F8EFE9;
  color: #9E3332;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ---------------- RIGHT WIDGETS ---------------- */
.journal-right-widgets {
  position: sticky;
  top: 90px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Streak Card */
.widget-streak-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.streak-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #FBEFE8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.streak-flame {
  color: #E25822;
}

.streak-days-count {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  color: #1A1D1A;
  line-height: 1.1;
  margin-bottom: 2px;
}

.streak-tagline {
  font-size: 11.5px;
  color: #7A7269;
  line-height: 1.35;
}

/* Calendar Card */
.widget-calendar-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 22px 18px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.calendar-header-nav {
  margin-bottom: 14px;
}

.calendar-month-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #242721;
  display: block;
  margin-bottom: 10px;
}

.cal-nav-buttons {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cal-current-month {
  font-size: 13px;
  font-weight: 600;
  color: #38342F;
}

.cal-arrow-btn {
  background: transparent;
  border: none;
  color: #8C7B70;
  cursor: pointer;
  padding: 4px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  text-align: center;
}

.cal-day-name {
  font-size: 10px;
  font-weight: 600;
  color: #A3978C;
  padding: 4px 0;
}

.cal-day-cell {
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #5C5852;
  border-radius: 50%;
}

.cal-day-cell.is-logged {
  background-color: #F8E4D8;
  color: #9E3332;
  font-weight: 700;
}

/* Insights Card */
.widget-insights-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 22px 18px;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
}

.insights-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.insights-title {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1A1D1A;
}

.link-insights-view-all {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  font-weight: 600;
  color: #9E3332;
  text-decoration: none;
}

.insights-items-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.insight-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.insight-icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #FAF3EE;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.insight-heading {
  font-size: 12.5px;
  font-weight: 600;
  color: #242721;
  margin-bottom: 2px;
}

.insight-subtext {
  font-size: 11px;
  line-height: 1.35;
  color: #7A7269;
}

/* ================= MODAL ================= */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(36, 39, 33, 0.45);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 20px;
}

.entry-modal-surface {
  background: #FFFFFF;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #EFE6DD;
}

.modal-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #1A1D1A;
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: #7A7269;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #38342F;
}

.form-input,
.form-textarea {
  padding: 10px 14px;
  border-radius: 10px;
  border: 1.5px solid #E2D7CC;
  font-size: 13.5px;
  color: #242721;
  outline: none;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #9E3332;
}

.tags-picker-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-pick-btn {
  padding: 5px 12px;
  border-radius: 999px;
  border: 1.5px solid #E5DBD1;
  background: #FAF8F5;
  color: #5C5852;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tag-pick-btn.is-active {
  background: #9E3332;
  border-color: #9E3332;
  color: #FFFFFF;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #EFE6DD;
}

.btn-modal-cancel {
  padding: 9px 18px;
  border-radius: 999px;
  border: 1px solid #D6CBC1;
  background: transparent;
  color: #5C5852;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-modal-save {
  padding: 9px 24px;
  border-radius: 999px;
  border: none;
  background-color: #9E3332;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-modal-save:hover {
  background-color: #832726;
}

/* Responsive */
@media (max-width: 1080px) {
  .journal-body-grid {
    grid-template-columns: 1fr;
  }
  .account-sidebar,
  .journal-right-widgets {
    position: static;
  }
}

@media (max-width: 768px) {
  .journal-hero-banner {
    flex-direction: column;
    gap: 20px;
  }
  .journal-entry-card {
    grid-template-columns: 1fr;
  }
  .entry-date-column,
  .entry-products-column {
    border: none;
    padding: 0;
  }
}
</style>
