<template>
  <div class="lumea-quiz-results-view">
    <!-- ============================================================= -->
    <!-- 1. BREADCRUMBS & EDITORIAL HERO BANNER                        -->
    <!-- ============================================================= -->
    <section class="results-hero-section">
      <div class="container">
        <nav class="breadcrumb-nav">
          <router-link to="/">Home</router-link>
          <span class="sep">›</span>
          <router-link to="/quiz">Skin Quiz</router-link>
          <span class="sep">›</span>
          <span class="current">Results</span>
        </nav>

        <div class="hero-banner-card">
          <div class="hero-text-content">
            <h1 class="hero-headline">Your Skin, Our Care.</h1>
            <p class="hero-subline">Here are your personalized results and product recommendations.</p>
          </div>

          <div class="hero-stage-container">
            <img
              src="/images/banners/banner-skin-concerns-clean.jpg"
              alt="Radiant Healthy Skin"
              class="hero-banner-image"
            />
            <div class="hero-fade-overlay"></div>
            <div class="banner-script-overlay">
              <span>Healthy Skin<br>Happier You. <Heart :size="16" class="script-heart-icon" /></span>
            </div>
            <div class="hero-quote-box">
              <p class="quote-text">“Skincare that fits you, not the crowd.”</p>
              <div class="quote-line"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================= -->
    <!-- 2. MAIN 3-COLUMN CONTENT GRID                                 -->
    <!-- ============================================================= -->
    <section class="results-main-section">
      <div class="container main-grid-layout">
        <!-- ----------------------------------------------------------- -->
        <!-- LEFT: YOUR RESULTS PROFILE SUMMARY                          -->
        <!-- ----------------------------------------------------------- -->
        <aside class="left-profile-column">
          <div class="profile-card">
            <div class="profile-eyebrow">LUMÉA SKIN QUIZ</div>
            <h2 class="profile-title">Your Results</h2>
            <p class="profile-desc">Based on your answers, here's your personalized skin profile.</p>

            <!-- Skin Type Highlight Box -->
            <div class="skin-type-badge-box">
              <div class="skin-type-icon-circle">
                <Droplets :size="24" />
              </div>
              <div class="skin-type-details">
                <span class="type-caption">Your Skin Type</span>
                <span class="type-name">{{ quizStore.currentSkinType }}</span>
                <span class="type-snippet">{{ quizStore.currentSkinDesc }}</span>
              </div>
            </div>

            <!-- Key Concerns -->
            <div class="profile-group-block">
              <h4 class="group-heading">Your Key Concerns</h4>
              <div class="badges-row">
                <div class="profile-circle-badge" v-for="c in activeConcerns" :key="c.name">
                  <div class="badge-icon-wrap">
                    <component :is="c.icon" :size="18" />
                  </div>
                  <span class="badge-name">{{ c.name }}</span>
                </div>
              </div>
            </div>

            <!-- Skin Goals -->
            <div class="profile-group-block">
              <h4 class="group-heading">Your Skin Goals</h4>
              <div class="badges-row">
                <div class="profile-circle-badge" v-for="g in activeGoals" :key="g.name">
                  <div class="badge-icon-wrap">
                    <component :is="g.icon" :size="18" />
                  </div>
                  <span class="badge-name">{{ g.name }}</span>
                </div>
              </div>
            </div>

            <div class="profile-actions">
              <router-link to="/quiz/questions" class="btn-retake-quiz">
                <RotateCcw :size="15" />
                <span>Retake Quiz</span>
              </router-link>
            </div>
          </div>
        </aside>

        <!-- ----------------------------------------------------------- -->
        <!-- CENTER: CURATED RECOMMENDATIONS (Using ProductCard)         -->
        <!-- ----------------------------------------------------------- -->
        <main class="center-content-column">
          <!-- Curated Banner -->
          <div class="curated-banner-card">
            <div class="curated-icon-box">
              <ShoppingBag :size="26" />
            </div>
            <div class="curated-text">
              <h3 class="curated-title">Curated Just for You</h3>
              <p class="curated-desc">We've handpicked these products based on your skin profile, concerns, and goals.</p>
            </div>
            <div class="curated-script-badge">
              <span>Good Choices<br>Ahead.</span>
            </div>
          </div>

          <!-- Section Header & Filter Pills -->
          <div class="recommendations-header-row">
            <div>
              <h2 class="section-title">Recommended for You</h2>
            </div>
            <router-link to="/routine" class="link-view-all">
              <span>View All Recommendations</span>
              <ArrowRight :size="15" />
            </router-link>
          </div>

          <!-- Filter Pills -->
          <div class="filter-pills-bar">
            <button
              v-for="cat in categoryTabs"
              :key="cat.id"
              class="filter-pill-btn"
              :class="{ 'is-active': activeTab === cat.id }"
              @click="activeTab = cat.id"
            >
              {{ cat.label }}
            </button>
          </div>

          <!-- Product Recommendations (Universal ProductCard) -->
          <div class="recommended-cards-grid">
            <ProductCard
              v-for="product in filteredProducts"
              :key="product.id"
              :product="product"
            />
          </div>

          <!-- "You Might Also Like" Slider -->
          <div class="you-might-like-section">
            <div class="section-sub-header">
              <h3 class="sub-section-title">You Might Also Like</h3>
              <div class="slider-arrows">
                <button class="arrow-btn" @click="scrollSlider(-1)" aria-label="Previous products">
                  <ChevronLeft :size="18" />
                </button>
                <button class="arrow-btn" @click="scrollSlider(1)" aria-label="Next products">
                  <ChevronRight :size="18" />
                </button>
              </div>
            </div>

            <div class="cards-carousel-row" ref="carouselRef">
              <div
                v-for="altProd in alsoLikeProducts"
                :key="altProd.id"
                class="carousel-card-wrapper"
              >
                <ProductCard :product="altProd" />
              </div>
            </div>
          </div>
        </main>

        <!-- ----------------------------------------------------------- -->
        <!-- RIGHT: PERSONALIZED ROUTINE OUTLINE & EXPERT TIPS           -->
        <!-- ----------------------------------------------------------- -->
        <aside class="right-routine-column">
          <!-- Routine Summary Card -->
          <div class="routine-summary-card">
            <h3 class="routine-card-title">Your Personalized Routine</h3>

            <!-- Morning / Evening Toggle -->
            <div class="routine-time-toggle">
              <button
                class="toggle-btn"
                :class="{ 'is-active': routineTime === 'morning' }"
                @click="routineTime = 'morning'"
              >
                <Sun :size="16" />
                <span>Morning</span>
              </button>
              <button
                class="toggle-btn"
                :class="{ 'is-active': routineTime === 'evening' }"
                @click="routineTime = 'evening'"
              >
                <Moon :size="16" />
                <span>Evening</span>
              </button>
            </div>

            <!-- Steps List -->
            <div class="routine-steps-list">
              <router-link
                to="/routine"
                v-for="step in currentRoutineSteps"
                :key="step.number"
                class="routine-step-row"
              >
                <div class="step-num-badge">{{ step.number }}</div>
                <div class="step-info">
                  <div class="step-title">{{ step.title }}</div>
                  <div class="step-desc">{{ step.desc }}</div>
                </div>
                <ChevronRight :size="16" class="step-arrow" />
              </router-link>
            </div>
          </div>

          <!-- Expert Tips Card -->
          <div class="expert-tips-card">
            <div class="tips-header">
              <Lightbulb :size="20" class="tips-icon" />
              <h4 class="tips-title">Expert Tips for Your Skin</h4>
            </div>
            <ul class="tips-list">
              <li>
                <Check :size="15" class="tip-check" />
                <span>Use a gentle cleanser twice daily</span>
              </li>
              <li>
                <Check :size="15" class="tip-check" />
                <span>Keep your skin hydrated with lightweight layers</span>
              </li>
              <li>
                <Check :size="15" class="tip-check" />
                <span>Don't skip sunscreen even on cloudy days</span>
              </li>
              <li>
                <Check :size="15" class="tip-check" />
                <span>Be consistent — barrier turnover takes 28 days</span>
              </li>
            </ul>
          </div>

          <!-- Real Care Real Results Promo Card -->
          <div class="real-care-promo-card">
            <div class="promo-text">
              <h4 class="promo-headline">Real Care.<br>Real Results.</h4>
            </div>
            <router-link to="/routine" class="btn-shop-routine">
              <span>Shop All Recommended</span>
              <ArrowRight :size="15" />
            </router-link>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import ProductCard from '@/components/ProductCard.vue'
import { useProductStore } from '@/stores/products'
import { useQuizStore } from '@/stores/quiz'
import {
  ArrowRight,
  Check,
  ChevronLeft,
  ChevronRight,
  Droplets,
  Flame,
  Heart,
  Lightbulb,
  Moon,
  RotateCcw,
  ShoppingBag,
  Sparkles,
  Sun,
  Zap
} from 'lucide-vue-next'
import { computed, ref } from 'vue'

const quizStore = useQuizStore()
const productStore = useProductStore()

const activeTab = ref('all')
const routineTime = ref('morning')
const carouselRef = ref(null)

const categoryTabs = [
  { id: 'all', label: 'Complete Routine' },
  { id: 'cleansers', label: 'Cleansers' },
  { id: 'treatments', label: 'Treatments' },
  { id: 'moisturizers', label: 'Moisturizers' },
  { id: 'sunscreens', label: 'Sunscreens' }
]

// Active concerns display
const activeConcerns = [
  { name: 'Pores', icon: Sparkles },
  { name: 'Uneven Tone', icon: Sun },
  { name: 'Occasional Breakouts', icon: Flame }
]

// Active goals display
const activeGoals = [
  { name: 'Clearer Skin', icon: Sparkles },
  { name: 'Brighter Tone', icon: Sun },
  { name: 'Hydration', icon: Droplets }
]

// Routine Steps lookup
const morningSteps = [
  { number: 1, title: 'Cleanser', desc: 'Gently removes oil and impurities' },
  { number: 2, title: 'Treatment', desc: 'Targets pores and uneven tone' },
  { number: 3, title: 'Moisturizer', desc: 'Keeps skin balanced and hydrated' },
  { number: 4, title: 'Sunscreen', desc: 'Protects from UV and environment damage' }
]

const eveningSteps = [
  { number: 1, title: 'Cleanser', desc: 'Dissolves pollutants and SPF residue' },
  { number: 2, title: 'Toner & Essence', desc: 'Preps cellular barrier for active treatments' },
  { number: 3, title: 'Active Serum', desc: 'Cellular repair and brightening treatment' },
  { number: 4, title: 'Night Cream', desc: 'Intensive overnight lipid replenishment' }
]

const currentRoutineSteps = computed(() => {
  return routineTime.value === 'morning' ? morningSteps : eveningSteps
})

// Products mapped from product catalog
const allCatalogProducts = computed(() => productStore.products)

const recommendedProducts = computed(() => {
  // Recommend 4 core hero products matching format mockup
  return [
    allCatalogProducts.value.find(p => p.id === 204) || {
      id: 204,
      name: 'CeraVe Foaming Facial Cleanser',
      brand: 'CeraVe',
      category: 'cleansers',
      price: 16.00,
      rating: 4.8,
      reviews: 1200,
      image_url: '/images/prod-cerave-cleanser.jpg',
      slug: 'cerave-foaming-facial-cleanser',
      badge: 'Step 1'
    },
    allCatalogProducts.value.find(p => p.id === 202) || {
      id: 202,
      name: 'The Ordinary Niacinamide 10% + Zinc 1%',
      brand: 'The Ordinary',
      category: 'treatments',
      price: 17.80,
      rating: 4.7,
      reviews: 2400,
      image_url: '/images/prod-ordinary.jpg',
      slug: 'the-ordinary-niacinamide-10-zinc-1',
      badge: 'Step 2'
    },
    allCatalogProducts.value.find(p => p.id === 203) || {
      id: 203,
      name: 'Laneige Water Bank Moisture Cream',
      brand: 'Laneige',
      category: 'moisturizers',
      price: 32.00,
      rating: 4.8,
      reviews: 987,
      image_url: '/images/prod-laneige.jpg',
      slug: 'laneige-water-bank-moisture-cream',
      badge: 'Step 3'
    },
    allCatalogProducts.value.find(p => p.id === 208) || {
      id: 208,
      name: 'La Roche-Posay Anthelios SPF 50+',
      brand: 'La Roche-Posay',
      category: 'sunscreens',
      price: 29.50,
      rating: 4.9,
      reviews: 1800,
      image_url: '/images/prod-laroche-effaclar.jpg',
      slug: 'la-roche-posay-anthelios-spf-50',
      badge: 'Step 4'
    }
  ]
})

const filteredProducts = computed(() => {
  if (activeTab.value === 'all') return recommendedProducts.value
  return recommendedProducts.value.filter(p => p.category === activeTab.value)
})

const alsoLikeProducts = computed(() => {
  return [
    allCatalogProducts.value.find(p => p.id === 205) || {
      id: 205,
      name: 'Anua Heartleaf 77% Soothing Toner',
      brand: 'Anua',
      price: 24.00,
      rating: 4.9,
      reviews: 892,
      image_url: '/images/prod-anua-toner.jpg',
      slug: 'anua-heartleaf-77-soothing-toner'
    },
    allCatalogProducts.value.find(p => p.id === 206) || {
      id: 206,
      name: 'COSRX Advanced Snail 92 Cream',
      brand: 'COSRX',
      price: 25.00,
      rating: 4.8,
      reviews: 1450,
      image_url: '/images/prod-cosrx-snail.jpg',
      slug: 'cosrx-advanced-snail-92-cream'
    },
    allCatalogProducts.value.find(p => p.id === 201) || {
      id: 201,
      name: 'SK-II Facial Treatment Essence',
      brand: 'SK-II',
      price: 99.00,
      rating: 4.8,
      reviews: 1200,
      image_url: '/images/prod-sk2.jpg',
      slug: 'sk-ii-facial-treatment-essence'
    },
    allCatalogProducts.value.find(p => p.id === 207) || {
      id: 207,
      name: 'Beauty of Joseon Calming Serum',
      brand: 'Beauty of Joseon',
      price: 22.00,
      rating: 4.7,
      reviews: 640,
      image_url: '/images/prod-boj.jpg',
      slug: 'beauty-of-joseon-calming-serum'
    }
  ]
})

function scrollSlider(direction) {
  if (carouselRef.value) {
    carouselRef.value.scrollBy({ left: direction * 280, behavior: 'smooth' })
  }
}
</script>

<style scoped>
.lumea-quiz-results-view {
  background-color: #FAF8F5;
  min-height: 100vh;
  color: #242721;
  padding-bottom: 80px;
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
  font-size: 1.7rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.15;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.95);
  z-index: 2;
  pointer-events: none;
}

.script-heart-icon {
  display: inline-block;
  vertical-align: -2px;
  margin-left: 4px;
  color: #8E4A3E;
  fill: #8E4A3E;
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

.quote-text {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 15px;
  line-height: 1.4;
  color: #1A1D1A;
  margin-bottom: 8px;
}

.quote-line {
  width: 32px;
  height: 2px;
  background-color: #9E3332;
  margin-left: auto;
}

/* ================= MAIN 3-COLUMN LAYOUT ================= */
.main-grid-layout {
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 28px;
  align-items: start;
}

/* ---------------- LEFT PROFILE COLUMN ---------------- */
.left-profile-column {
  position: sticky;
  top: 90px;
}

.profile-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 26px 22px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.profile-eyebrow {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #8C7B70;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.profile-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 8px;
}

.profile-desc {
  font-size: 12.5px;
  color: #7A7269;
  line-height: 1.5;
  margin-bottom: 22px;
}

.skin-type-badge-box {
  background: #FDF9F7;
  border: 1.5px solid #F0DFD3;
  border-radius: 16px;
  padding: 18px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.skin-type-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #F4E4D7;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.skin-type-details {
  display: flex;
  flex-direction: column;
}

.type-caption {
  font-size: 11.5px;
  font-weight: 600;
  color: #8C7B70;
}

.type-name {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #9E3332;
  margin: 2px 0;
}

.type-snippet {
  font-size: 11.5px;
  color: #6C665D;
  line-height: 1.35;
}

.profile-group-block {
  margin-bottom: 22px;
  border-top: 1px solid #F2EBE3;
  padding-top: 18px;
}

.group-heading {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #38342F;
  margin-bottom: 14px;
}

.badges-row {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.profile-circle-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  flex: 1;
}

.badge-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #FAF3EE;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
  border: 1px solid #F0DFD3;
}

.badge-name {
  font-size: 11px;
  font-weight: 600;
  color: #5C5852;
  line-height: 1.25;
}

.profile-actions {
  border-top: 1px solid #F2EBE3;
  padding-top: 20px;
}

.btn-retake-quiz {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  border-radius: 999px;
  border: 1.5px solid #9E3332;
  background: transparent;
  color: #9E3332;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-retake-quiz:hover {
  background-color: #9E3332;
  color: #FFFFFF;
}

/* ---------------- CENTER CONTENT COLUMN ---------------- */
.center-content-column {
  min-width: 0;
}

.curated-banner-card {
  background: #FFFBF8;
  border: 1px solid #F2E2D6;
  border-radius: 18px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 28px;
  box-shadow: 0 2px 12px rgba(158, 51, 50, 0.04);
}

.curated-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #F8ECE3;
  color: #9E3332;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.curated-text {
  flex: 1;
}

.curated-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #9E3332;
  margin-bottom: 4px;
}

.curated-desc {
  font-size: 13px;
  color: #6C665D;
  line-height: 1.45;
}

.curated-script-badge {
  font-family: 'Cormorant Garamond', cursive, serif;
  font-style: italic;
  font-size: 19px;
  font-weight: 600;
  color: #9E3332;
  line-height: 1.1;
  text-align: right;
  flex-shrink: 0;
}

/* Header & Filter Pills */
.recommendations-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 600;
  color: #1A1D1A;
}

.link-view-all {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #9E3332;
  text-decoration: none;
}

.link-view-all:hover {
  text-decoration: underline;
}

.filter-pills-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.filter-pill-btn {
  padding: 9px 20px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  border: 1.5px solid #E5DBD1;
  background: #FFFFFF;
  color: #4A453F;
}

.filter-pill-btn:hover {
  border-color: #9E3332;
  color: #9E3332;
}

.filter-pill-btn.is-active {
  background-color: #9E3332;
  border-color: #9E3332;
  color: #FFFFFF;
}

/* Recommended Cards Grid */
.recommended-cards-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

/* You Might Also Like Slider */
.you-might-like-section {
  border-top: 1px solid #ECE4DC;
  padding-top: 32px;
}

.section-sub-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.sub-section-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #1A1D1A;
}

.slider-arrows {
  display: flex;
  gap: 8px;
}

.arrow-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid #D6CBC1;
  background: #FFFFFF;
  color: #4A453F;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.arrow-btn:hover {
  border-color: #9E3332;
  color: #9E3332;
}

.cards-carousel-row {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding-bottom: 12px;
}

.carousel-card-wrapper {
  flex: 0 0 calc(50% - 8px);
  min-width: 220px;
}

/* ---------------- RIGHT ROUTINE COLUMN ---------------- */
.right-routine-column {
  position: sticky;
  top: 90px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.routine-summary-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.routine-card-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 16px;
}

.routine-time-toggle {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  background: #F4EFEB;
  padding: 4px;
  border-radius: 999px;
  margin-bottom: 20px;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px 12px;
  border-radius: 999px;
  border: none;
  background: transparent;
  font-size: 12.5px;
  font-weight: 600;
  color: #5C5852;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn.is-active {
  background-color: #9E3332;
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(158, 51, 50, 0.2);
}

.routine-steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.routine-step-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: background-color 0.2s ease;
}

.routine-step-row:hover {
  background-color: #FAF4F0;
}

.step-num-badge {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #F4ECE6;
  color: #9E3332;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-info {
  flex: 1;
}

.step-title {
  font-size: 13.5px;
  font-weight: 600;
  color: #242721;
}

.step-desc {
  font-size: 11.5px;
  color: #7A7269;
}

.step-arrow {
  color: #B5ABA0;
}

/* Expert Tips Card */
.expert-tips-card {
  background: #FFFDF9;
  border: 1px solid #EFE6DD;
  border-radius: 18px;
  padding: 22px 20px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.tips-icon {
  color: #9E3332;
}

.tips-title {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1A1D1A;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 12px;
  line-height: 1.45;
  color: #5C5852;
}

.tip-check {
  color: #9E3332;
  flex-shrink: 0;
  margin-top: 1px;
}

/* Real Care Promo Card */
.real-care-promo-card {
  background: linear-gradient(135deg, #F9EDE4 0%, #F5E4D7 100%);
  border: 1px solid #EADBCE;
  border-radius: 18px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.promo-headline {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  font-weight: 600;
  color: #1A1D1A;
  line-height: 1.25;
}

.btn-shop-routine {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: #9E3332;
  color: #FFFFFF;
  padding: 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-shop-routine:hover {
  background-color: #832726;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 1080px) {
  .main-grid-layout {
    grid-template-columns: 1fr;
  }
  .left-profile-column,
  .right-routine-column {
    position: static;
  }
}

@media (max-width: 768px) {
  .hero-banner-card {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  .hero-center-stage {
    margin: 0;
  }
  .hero-quote-box {
    text-align: center;
  }
  .quote-line {
    margin: 0 auto;
  }
  .recommended-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
