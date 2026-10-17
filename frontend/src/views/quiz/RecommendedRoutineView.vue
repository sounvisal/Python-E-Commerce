<template>
  <div class="lumea-routine-view">
    <!-- ============================================================= -->
    <!-- 1. BREADCRUMBS & HERO BANNER                                  -->
    <!-- ============================================================= -->
    <section class="routine-hero-section">
      <div class="container">
        <nav class="breadcrumb-nav">
          <router-link to="/">Home</router-link>
          <span class="sep">›</span>
          <router-link to="/quiz">Skin Quiz</router-link>
          <span class="sep">›</span>
          <router-link to="/quiz/results">Results</router-link>
          <span class="sep">›</span>
          <span class="current">Your Routine</span>
        </nav>

        <div class="hero-banner-card">
          <div class="hero-text-content">
            <h1 class="hero-headline">Your Personalized Routine</h1>
            <p class="hero-subline">A simple, effective routine designed for your unique skin.</p>
          </div>

          <div class="hero-stage-container">
            <img
              src="/images/banners/banner-skin-concerns-clean.jpg"
              alt="Glowing Radiant Skin"
              class="hero-banner-image"
            />
            <div class="hero-fade-overlay"></div>
            <div class="banner-script-overlay">
              <span>Consistency Today,<br>Healthier Skin<br>Tomorrow.</span>
            </div>
            <div class="hero-quote-box">
              <h3 class="quote-title">Real Care.<br>Real Results.</h3>
              <div class="quote-line"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================= -->
    <!-- 2. MAIN LAYOUT (PROFILE ASIDE + STEP-BY-STEP ROUTINE)         -->
    <!-- ============================================================= -->
    <section class="routine-main-section">
      <div class="container routine-layout-grid">
        <!-- ----------------------------------------------------------- -->
        <!-- LEFT ASIDE: SKIN PROFILE & EXPERT CHAT                      -->
        <!-- ----------------------------------------------------------- -->
        <aside class="routine-profile-sidebar">
          <div class="profile-card">
            <div class="profile-eyebrow">YOUR SKIN PROFILE</div>

            <!-- Skin Type -->
            <div class="type-box">
              <div class="type-icon-circle">
                <Droplets :size="22" />
              </div>
              <div>
                <span class="type-caption">Skin Type</span>
                <h3 class="type-name">{{ quizStore.currentSkinType }}</h3>
                <p class="type-desc">{{ quizStore.currentSkinDesc }}</p>
              </div>
            </div>

            <!-- Key Concerns -->
            <div class="profile-block">
              <h4 class="block-title">Key Concerns</h4>
              <div class="badges-row">
                <div class="circle-badge" v-for="c in activeConcerns" :key="c.name">
                  <div class="badge-icon-wrap">
                    <component :is="c.icon" :size="16" />
                  </div>
                  <span class="badge-label">{{ c.name }}</span>
                </div>
              </div>
            </div>

            <!-- Your Goals -->
            <div class="profile-block">
              <h4 class="block-title">Your Goals</h4>
              <div class="badges-row">
                <div class="circle-badge" v-for="g in activeGoals" :key="g.name">
                  <div class="badge-icon-wrap">
                    <component :is="g.icon" :size="16" />
                  </div>
                  <span class="badge-label">{{ g.name }}</span>
                </div>
              </div>
            </div>

            <div class="profile-actions">
              <router-link to="/quiz/questions" class="btn-retake">
                <RotateCcw :size="15" />
                <span>Retake Quiz</span>
              </router-link>
            </div>
          </div>

          <!-- Need Expert Advice Card -->
          <div class="expert-advice-card">
            <div class="advisor-row">
              <img src="/images/avatar-sreynich.jpg" alt="Skincare Expert" class="advisor-avatar" />
              <div class="advisor-info">
                <h4 class="advisor-heading">Need expert advice?</h4>
                <p class="advisor-desc">Chat with our skincare specialists for personalized guidance.</p>
              </div>
            </div>
            <router-link to="/contact" class="btn-chat-expert">
              <MessageSquare :size="15" />
              <span>Chat with Us</span>
            </router-link>
          </div>
        </aside>

        <!-- ----------------------------------------------------------- -->
        <!-- MAIN ROUTINE SECTION (MORNING / EVENING TABS & STEP CARDS) -->
        <!-- ----------------------------------------------------------- -->
        <main class="routine-flow-main">
          <!-- Big Day / Night Mode Tabs -->
          <div class="time-tabs-row">
            <button
              class="time-tab-card"
              :class="{ 'is-selected': activeTime === 'morning' }"
              @click="activeTime = 'morning'"
            >
              <div class="tab-icon-box">
                <Sun :size="24" />
              </div>
              <div class="tab-info">
                <h3 class="tab-title">Morning Routine</h3>
                <p class="tab-subtitle">Protect and prepare your skin for the day</p>
              </div>
            </button>

            <button
              class="time-tab-card"
              :class="{ 'is-selected': activeTime === 'evening' }"
              @click="activeTime = 'evening'"
            >
              <div class="tab-icon-box">
                <Moon :size="24" />
              </div>
              <div class="tab-info">
                <h3 class="tab-title">Evening Routine</h3>
                <p class="tab-subtitle">Cleanse and repair your skin overnight</p>
              </div>
            </button>
          </div>

          <!-- Section Subheader with Est. time & "Add All to Cart" -->
          <div class="routine-action-header">
            <div>
              <h2 class="routine-section-title">
                Your {{ activeTime === 'morning' ? 'Morning' : 'Evening' }} Routine
              </h2>
              <p class="routine-section-desc">
                Start your day with these {{ currentProducts.length }} essential steps. Click on each product to learn more.
              </p>
            </div>

            <div class="routine-top-actions">
              <div class="time-estimate-pill">
                <Clock :size="15" />
                <span>Est. 5 minutes</span>
              </div>

              <button class="btn-add-all-cart" @click="addAllToCart">
                <Check v-if="addedAll" :size="16" class="check-inline" />
                <ShoppingBag v-else :size="16" />
                <span>{{ addedAll ? 'Added to Cart' : 'Add All to Cart' }}</span>
              </button>
            </div>
          </div>

          <!-- Step-by-Step Flow with Interconnecting Arrows -->
          <div class="routine-steps-flow">
            <template v-for="(prod, idx) in currentProducts" :key="prod.id">
              <!-- Step Product Card -->
              <div class="routine-step-card">
                <div class="step-card-header">
                  <div class="step-badge-number">{{ prod.step }}</div>
                  <span class="step-action-tag">{{ prod.stepName }}</span>
                  <button
                    class="step-wishlist-btn"
                    :class="{ 'is-active': wishlistStore.isInWishlist(prod.id) }"
                    @click="wishlistStore.toggleWishlist(prod)"
                    aria-label="Add to wishlist"
                  >
                    <Heart :size="16" />
                  </button>
                </div>

                <div class="step-img-box">
                  <img :src="prod.image_url" :alt="prod.name" class="step-prod-img" />
                </div>

                <div class="step-card-body">
                  <span class="step-brand">{{ prod.brand }}</span>
                  <router-link :to="`/product/${prod.slug}`" class="step-title-link">
                    {{ prod.name }}
                  </router-link>
                  <span class="step-tagline">{{ prod.tagline }}</span>

                  <div class="step-price-row">
                    <span class="step-price">${{ prod.price.toFixed(2) }}</span>
                    <div class="step-stars">
                      <Star :size="12" class="fill-star" v-for="i in 5" :key="i" />
                      <span class="review-count">({{ prod.reviews }})</span>
                    </div>
                  </div>

                  <button
                    class="btn-step-add"
                    :class="{ 'is-added': isProductAdded(prod.id) }"
                    @click="addToCart(prod)"
                  >
                    <Check v-if="isProductAdded(prod.id)" :size="13" class="check-inline" />
                    <span>{{ isProductAdded(prod.id) ? 'Added' : 'Add to Cart' }}</span>
                  </button>
                </div>
              </div>

              <!-- Connecting Arrow between cards -->
              <div class="flow-arrow-separator" v-if="idx < currentProducts.length - 1">
                <ArrowRight :size="20" />
              </div>
            </template>
          </div>

          <!-- Bottom: Quick Tips for Better Results -->
          <div class="tips-and-swatch-banner">
            <div class="tips-left-box">
              <div class="tips-headline-row">
                <Lightbulb :size="22" class="bulb-icon" />
                <h3 class="tips-heading">Quick Tips for Better Results</h3>
              </div>

              <div class="tips-two-col-grid">
                <div class="tip-point">
                  <Check :size="16" class="tip-icon" />
                  <span>Use products in the correct order (from lightest to heaviest).</span>
                </div>
                <div class="tip-point">
                  <Check :size="16" class="tip-icon" />
                  <span>Don't skip sunscreen, even on cloudy or overcast days.</span>
                </div>
                <div class="tip-point">
                  <Check :size="16" class="tip-icon" />
                  <span>Be consistent — barrier restoration takes 4 to 6 weeks.</span>
                </div>
                <div class="tip-point">
                  <Check :size="16" class="tip-icon" />
                  <span>Adjust your routine hydration based on seasonal humidity.</span>
                </div>
              </div>
            </div>

            <div class="swatch-right-box">
              <img src="/images/search-gel-swatch.jpg" alt="Pure Formula Swatch" class="swatch-img" />
              <div class="swatch-caption">
                <span class="swatch-title">Small Steps.<br>Big Changes.</span>
                <div class="swatch-line"></div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useQuizStore } from '@/stores/quiz'
import { useWishlistStore } from '@/stores/wishlist'
import {
  ArrowRight,
  Check,
  Clock,
  Droplets,
  Flame,
  Heart,
  Lightbulb,
  MessageSquare,
  Moon,
  RotateCcw,
  ShoppingBag,
  Sparkles,
  Star,
  Sun
} from 'lucide-vue-next'
import { computed, ref } from 'vue'

const quizStore = useQuizStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()

const activeTime = ref('morning')
const addedItems = ref(new Set())
const addedAll = ref(false)

const activeConcerns = [
  { name: 'Pores', icon: Sparkles },
  { name: 'Uneven Tone', icon: Sun },
  { name: 'Occasional Breakouts', icon: Flame }
]

const activeGoals = [
  { name: 'Clearer Skin', icon: Sparkles },
  { name: 'Brighter Tone', icon: Sun },
  { name: 'Hydration', icon: Droplets }
]

const currentProducts = computed(() => {
  return activeTime.value === 'morning'
    ? quizStore.recommendedRoutineProducts
    : quizStore.eveningRoutineProducts
})

function isProductAdded(id) {
  return addedItems.value.has(id)
}

function addToCart(prod) {
  cartStore.addItem({
    id: prod.id,
    name: prod.name,
    brand: prod.brand,
    price: prod.price,
    image_url: prod.image_url,
    quantity: 1
  })
  addedItems.value.add(prod.id)
  setTimeout(() => {
    addedItems.value.delete(prod.id)
  }, 2200)
}

function addAllToCart() {
  currentProducts.value.forEach(prod => {
    cartStore.addItem({
      id: prod.id,
      name: prod.name,
      brand: prod.brand,
      price: prod.price,
      image_url: prod.image_url,
      quantity: 1
    })
  })
  addedAll.value = true
  setTimeout(() => {
    addedAll.value = false
  }, 3000)
}
</script>

<style scoped>
.lumea-routine-view {
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

/* ================= BREADCRUMBS & HERO ================= */
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

.hero-banner-card {
  background: linear-gradient(135deg, #F8EFE9 0%, #F5E8DF 100%);
  border: 1px solid #EADBCE;
  border-radius: 20px;
  display: grid;
  grid-template-columns: 1.1fr 1.45fr;
  min-height: 275px;
  margin-bottom: 36px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.hero-text-content {
  padding: 36px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
}

.hero-headline {
  font-family: 'Playfair Display', serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  margin-bottom: 12px;
  line-height: 1.15;
}

.hero-subline {
  font-size: 1.15rem;
  color: #5C5852;
  line-height: 1.55;
}

.hero-stage-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 275px;
  overflow: hidden;
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
  width: 140px;
  background: linear-gradient(to right, #F8EFE9, rgba(248, 239, 233, 0));
  pointer-events: none;
  z-index: 1;
}

.banner-script-overlay {
  position: absolute;
  top: 26px;
  left: 36%;
  font-family: 'Cormorant Garamond', cursive, serif;
  font-style: italic;
  font-size: 1.65rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.15;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.95);
  z-index: 2;
  pointer-events: none;
}

.hero-quote-box {
  position: absolute;
  top: 50%;
  right: 32px;
  transform: translateY(-50%);
  max-width: 210px;
  text-align: right;
  z-index: 2;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(8px);
  padding: 14px 18px;
  border-radius: 14px;
  border: 1px solid rgba(234, 219, 206, 0.75);
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.06);
}

.quote-title {
  font-family: 'Playfair Display', serif;
  font-size: 19px;
  line-height: 1.3;
  color: #1A1D1A;
  margin-bottom: 8px;
}

.quote-line {
  width: 32px;
  height: 2px;
  background-color: #9E3332;
  margin-left: auto;
}

/* ================= MAIN LAYOUT GRID ================= */
.routine-layout-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
  align-items: start;
}

/* ---------------- LEFT SIDEBAR ---------------- */
.routine-profile-sidebar {
  position: sticky;
  top: 90px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 24px 20px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.profile-eyebrow {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #8C7B70;
  margin-bottom: 16px;
  text-transform: uppercase;
}

.type-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FDF9F7;
  border: 1.5px solid #F0DFD3;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 20px;
}

.type-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #F4E4D7;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.type-caption {
  font-size: 11px;
  font-weight: 600;
  color: #8C7B70;
}

.type-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #9E3332;
  margin: 2px 0;
}

.type-desc {
  font-size: 11.5px;
  color: #6C665D;
  line-height: 1.35;
}

.profile-block {
  border-top: 1px solid #F2EBE3;
  padding-top: 16px;
  margin-bottom: 16px;
}

.block-title {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #38342F;
  margin-bottom: 12px;
}

.badges-row {
  display: flex;
  justify-content: space-between;
  gap: 6px;
}

.circle-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
}

.badge-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FAF3EE;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
  border: 1px solid #F0DFD3;
}

.badge-label {
  font-size: 10.5px;
  font-weight: 600;
  color: #5C5852;
  line-height: 1.2;
}

.profile-actions {
  border-top: 1px solid #F2EBE3;
  padding-top: 16px;
}

.btn-retake {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 11px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-retake:hover {
  background-color: #9E3332;
  color: #FFFFFF;
}

/* Expert Advice Card */
.expert-advice-card {
  background: #FFFDF9;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 18px 20px;
}

.advisor-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.advisor-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 1px solid #EFE6DD;
}

.advisor-heading {
  font-size: 13.5px;
  font-weight: 700;
  color: #242721;
  margin-bottom: 2px;
}

.advisor-desc {
  font-size: 11.5px;
  line-height: 1.4;
  color: #7A7269;
}

.btn-chat-expert {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-chat-expert:hover {
  background-color: #FAF4F0;
}

/* ---------------- MAIN ROUTINE COLUMN ---------------- */
.routine-flow-main {
  min-width: 0;
}

.time-tabs-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}

.time-tab-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  border-radius: 18px;
  border: 1.5px solid #EFE6DD;
  background: #FFFFFF;
  text-align: left;
  cursor: pointer;
  transition: all 0.22s ease;
}

.time-tab-card:hover {
  border-color: #D3C4B6;
  background: #FAF6F2;
}

.time-tab-card.is-selected {
  border-color: #9E3332;
  background: #FDF8F5;
  box-shadow: 0 4px 16px rgba(158, 51, 50, 0.08);
}

.tab-icon-box {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #F4EBE3;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.time-tab-card.is-selected .tab-icon-box {
  background: #9E3332;
  color: #FFFFFF;
}

.tab-title {
  font-family: 'Playfair Display', serif;
  font-size: 17.5px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 2px;
}

.tab-subtitle {
  font-size: 12px;
  color: #7A7269;
}

/* Header with Est time & Add All */
.routine-action-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 24px;
}

.routine-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 6px;
}

.routine-section-desc {
  font-size: 14px;
  color: #6C665D;
}

.routine-top-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.time-estimate-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 600;
  color: #7A7269;
  background: #EFE8E1;
  padding: 8px 14px;
  border-radius: 999px;
}

.btn-add-all-cart {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add-all-cart:hover {
  background-color: #9E3332;
  color: #FFFFFF;
}

/* Step Cards Horizontal Flow */
.routine-steps-flow {
  display: flex;
  align-items: stretch;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 20px;
  margin-bottom: 40px;
}

.routine-step-card {
  flex: 0 0 210px;
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 16px 14px 18px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(36, 39, 33, 0.04);
  transition: transform 0.2s ease;
}

.routine-step-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(36, 39, 33, 0.08);
}

.step-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.step-badge-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #F4EBE3;
  color: #9E3332;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-action-tag {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #7A7269;
}

.step-wishlist-btn {
  background: transparent;
  border: none;
  color: #B5ABA0;
  cursor: pointer;
  padding: 2px;
  transition: color 0.2s ease;
}

.step-wishlist-btn.is-active {
  color: #9E3332;
}

.step-img-box {
  width: 100%;
  height: 140px;
  border-radius: 12px;
  overflow: hidden;
  background-color: #FAF8F5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.step-prod-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.step-card-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.step-brand {
  font-size: 11px;
  font-weight: 600;
  color: #8C7B70;
  margin-bottom: 2px;
}

.step-title-link {
  font-family: 'Playfair Display', serif;
  font-size: 14.5px;
  font-weight: 600;
  color: #1A1D1A;
  text-decoration: none;
  line-height: 1.3;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.step-title-link:hover {
  color: #9E3332;
}

.step-tagline {
  font-size: 11.5px;
  color: #7A7269;
  line-height: 1.35;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.step-price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  margin-bottom: 12px;
}

.step-price {
  font-size: 15px;
  font-weight: 700;
  color: #242721;
}

.step-stars {
  display: flex;
  align-items: center;
  gap: 2px;
}

.fill-star {
  color: #D4A373;
  fill: #D4A373;
}

.review-count {
  font-size: 10.5px;
  color: #8C7B70;
  margin-left: 2px;
}

.btn-step-add {
  width: 100%;
  padding: 10px;
  border-radius: 999px;
  background-color: #9E3332;
  border: none;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.check-inline {
  flex-shrink: 0;
}

.btn-step-add:hover {
  background-color: #832726;
}

.btn-step-add.is-added {
  background-color: #242721;
}

.flow-arrow-separator {
  color: #C2B7AC;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ================= BOTTOM TIPS & SWATCH ================= */
.tips-and-swatch-banner {
  background: #FFFDF9;
  border: 1px solid #EADBCE;
  border-radius: 20px;
  padding: 28px;
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  gap: 28px;
  align-items: center;
}

.tips-headline-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.bulb-icon {
  color: #9E3332;
}

.tips-heading {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #1A1D1A;
}

.tips-two-col-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.tip-point {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12.5px;
  line-height: 1.45;
  color: #5C5852;
}

.tip-icon {
  color: #9E3332;
  flex-shrink: 0;
  margin-top: 2px;
}

.swatch-right-box {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  height: 150px;
  border: 1px solid #EFE6DD;
}

.swatch-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.swatch-caption {
  position: absolute;
  top: 16px;
  left: 18px;
}

.swatch-title {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 19px;
  font-weight: 600;
  color: #242721;
  line-height: 1.2;
}

.swatch-line {
  width: 28px;
  height: 2px;
  background-color: #9E3332;
  margin-top: 8px;
}

/* Responsive */
@media (max-width: 992px) {
  .routine-layout-grid {
    grid-template-columns: 1fr;
  }
  .routine-profile-sidebar {
    position: static;
  }
  .time-tabs-row {
    grid-template-columns: 1fr;
  }
  .tips-and-swatch-banner {
    grid-template-columns: 1fr;
  }
  .tips-two-col-grid {
    grid-template-columns: 1fr;
  }
}
</style>
