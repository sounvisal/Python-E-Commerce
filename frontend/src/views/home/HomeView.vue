<template>
  <div class="lumea-home-page">
    <!-- ================================================================= -->
    <!-- 1. HERO SECTION                                                  -->
    <!-- ================================================================= -->
    <section class="hero-section reveal-on-scroll is-visible">
      <div class="container hero-container">
        <!-- Hero Left Column: Editorial Copy -->
        <div class="hero-text-col">
          <div class="hero-eyebrow animate-fade-in">
            <span>DISCOVER A BRIGHTER YOU</span>
          </div>

          <h1 class="hero-headline animate-fade-in-up">
            Your Skincare<br>
            Destination.
          </h1>

          <p class="hero-description animate-fade-in-up delay-1">
            Explore 100+ trusted skincare brands in one place. Real products. Real results. A healthier, happier you.
          </p>

          <div class="hero-cta-group animate-fade-in-up delay-2">
            <router-link to="/shop" class="btn btn-pill-dark">
              <span>Shop Now</span>
              <ArrowRight :size="16" />
            </router-link>

            <button class="btn btn-pill-outline" @click="showStoryModal = true">
              <Play :size="14" class="play-icon" />
              <span>Watch Our Story</span>
            </button>
          </div>

          <!-- Hero Slider Controls -->
          <div class="hero-slider-bar animate-fade-in-up delay-3">
            <div class="slider-progress-track">
              <div class="slider-progress-fill" :style="{ width: `${(activeSlide / 3) * 100}%` }"></div>
            </div>

            <div class="slider-counter">
              <span class="slide-num" :class="{ 'is-active': activeSlide === 1 }" @click="activeSlide = 1">01</span>
              <span class="slide-num" :class="{ 'is-active': activeSlide === 2 }" @click="activeSlide = 2">02</span>
              <span class="slide-num" :class="{ 'is-active': activeSlide === 3 }" @click="activeSlide = 3">03</span>
            </div>

            <div class="slider-arrows">
              <button class="slider-arrow-btn" @click="prevSlide" aria-label="Previous Slide">
                <ChevronLeft :size="15" />
              </button>
              <button class="slider-arrow-btn" @click="nextSlide" aria-label="Next Slide">
                <ChevronRight :size="15" />
              </button>
            </div>
          </div>
        </div>

        <!-- Hero Right Column: Skincare Bottles Composition -->
        <div class="hero-visual-col animate-fade-in delay-2">
          <div class="hero-image-stage">
            <!-- Floating Editorial Callout -->
            <div class="floating-script-callout">
              <span class="script-phrase">More Brands.<br>Healthier Skin.</span>
            </div>

            <!-- Main Beauty Bottles Visual matching exact composition -->
            <div class="bottles-scene">
              <img
                :src="homeBanner.image_url || '/images/ai-banner-atelier.jpg'"
                alt="Luméa Skincare Essentials - SK-II, The Ordinary, Laneige"
                class="main-scene-img"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 2. BRAND HORIZON ANIMATION (MARQUEE SECTION)                     -->
    <!-- ================================================================= -->
    <section class="horizon-brands-section reveal-on-scroll" id="brands">
      <div class="horizon-track-wrapper">
        <!-- Infinite horizon scrolling marquee with real vector brand logos -->
        <div class="horizon-marquee">
          <div class="marquee-group">
            <div
              v-for="brand in marqueeBrands"
              :key="brand"
              class="marquee-brand-item"
              @click="filterByBrand(brand)"
            >
              <BrandLogo :brand="brand" size="marquee" />
            </div>
          </div>
          <!-- Duplicate group for seamless infinite horizon animation loop -->
          <div class="marquee-group" aria-hidden="true">
            <div
              v-for="brand in marqueeBrands"
              :key="'dup-' + brand"
              class="marquee-brand-item"
              @click="filterByBrand(brand)"
            >
              <BrandLogo :brand="brand" size="marquee" />
            </div>
          </div>
        </div>

        <button class="horizon-nav-btn" @click="scrollBrands" aria-label="Browse Brands">
          <ChevronRight :size="16" />
        </button>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 3. SHOP BY CATEGORY                                              -->
    <!-- ================================================================= -->
    <section class="categories-section reveal-on-scroll" id="categories">
      <div class="container">
        <div class="section-headline-row">
          <h2 class="section-title-tag">SHOP BY CATEGORY</h2>
          <router-link to="/shop" class="view-all-link">
            <span>View All Categories</span>
            <ArrowRight :size="14" />
          </router-link>
        </div>

        <div class="categories-pill-grid">
          <div
            v-for="(cat, idx) in categoriesList"
            :key="cat.name"
            class="cat-pill-card stagger-item"
            :style="{ transitionDelay: `${idx * 60}ms` }"
            @click="filterByCategory(cat.slug)"
          >
            <div class="cat-pill-pedestal">
              <img :src="cat.image" :alt="cat.name" class="cat-bottle-icon" />
            </div>
            <span class="cat-pill-title">{{ cat.name }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 4. SPECIAL OFFER BANNER ("Glow More Spend Less.")                 -->
    <!-- ================================================================= -->
    <section class="special-offer-section reveal-on-scroll" id="special-offer">
      <div class="container">
        <div class="special-offer-card">
          <!-- Left Text Content -->
          <div class="offer-text-block">
            <span class="offer-eyebrow">SPECIAL OFFER</span>
            <h2 class="offer-title">Glow More<br>Spend Less.</h2>
            <p class="offer-desc">Up to 30% off on selected brands.</p>
            <router-link to="/shop?deals=true" class="btn btn-pill-dark offer-btn">
              <span>Shop Deals</span>
              <ArrowRight :size="16" />
            </router-link>
          </div>

          <!-- Right Visual with Caudalie bottles on stone & 30% badge -->
          <div class="offer-visual-block">
            <div class="offer-badge-circle">
              <span class="badge-sub">UP TO</span>
              <span class="badge-percent">30%</span>
              <span class="badge-off">OFF</span>
            </div>

            <div class="offer-script-tag">
              <span>Good Skin<br>Good Days</span>
            </div>

            <img
              src="/images/special-offer.jpg"
              alt="Caudalie Skincare Offer on Stone Pedestal"
              class="offer-hero-bottles"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 5. BEST SELLERS                                                  -->
    <!-- ================================================================= -->
    <section class="best-sellers-section reveal-on-scroll" id="best-sellers">
      <div class="container">
        <div class="section-headline-row">
          <h2 class="section-title-tag">BEST SELLERS</h2>
          <router-link to="/shop?sort=popular" class="view-all-link">
            <span>See All</span>
            <ArrowRight :size="14" />
          </router-link>
        </div>

        <div class="products-carousel-grid">
          <ProductCard
            v-for="product in bestSellersList"
            :key="product.id"
            :product="product"
          />
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 6. BROWSE BY BRAND                                               -->
    <!-- ================================================================= -->
    <section class="browse-brands-section reveal-on-scroll">
      <div class="container">
        <div class="section-headline-row">
          <h2 class="section-title-tag">BROWSE BY BRAND</h2>
          <router-link to="/shop" class="view-all-link">
            <span>View All Brands</span>
            <ArrowRight :size="14" />
          </router-link>
        </div>

        <div class="brand-circles-row">
          <div
            v-for="(brand, idx) in brandCircles"
            :key="brand.name"
            class="brand-circle-item stagger-item"
            :style="{ transitionDelay: `${idx * 40}ms` }"
            @click="filterByBrand(brand.name)"
          >
            <div class="brand-circle-badge">
              <BrandLogo :brand="brand.name" size="circle" />
            </div>
            <span class="brand-circle-label">{{ brand.name }}</span>
          </div>

          <button class="brand-circle-arrow" @click="scrollBrands" aria-label="More Brands">
            <ChevronRight :size="18" />
          </button>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 7. ROUTINE QUIZ BANNER ("Find Your Routine.")                     -->
    <!-- ================================================================= -->
    <section class="quiz-banner-section reveal-on-scroll" id="quiz">
      <div class="container">
        <div class="quiz-banner-card">
          <!-- Left Quiz Text & Badges -->
          <div class="quiz-content-col">
            <span class="quiz-eyebrow">NOT SURE WHAT YOU NEED?</span>
            <h2 class="quiz-title">Find Your Routine.</h2>
            <p class="quiz-desc">
              Take a quick quiz and get personalized recommendations from top skincare brands.
            </p>

            <router-link to="/quiz" class="btn btn-pill-dark quiz-start-btn">
              <span>Start Skin Quiz</span>
              <ArrowRight :size="16" />
            </router-link>

            <!-- 3 Highlights -->
            <div class="quiz-highlights-strip">
              <div class="highlight-item">
                <Clock :size="14" />
                <span>Just 3 Minutes</span>
              </div>
              <div class="highlight-item">
                <Sparkles :size="14" />
                <span>Personalized Results</span>
              </div>
              <div class="highlight-item">
                <CheckCircle2 :size="14" />
                <span>100% Free</span>
              </div>
            </div>
          </div>

          <!-- Right Model Photo with Circular Editorial Stamp -->
          <div class="quiz-visual-col">
            <div class="model-visual-stage">
              <img
                src="/images/quiz-model.jpg"
                alt="Dewy Glowing Skin Model"
                class="quiz-model-img"
              />
              <div class="editorial-stamp-badge">
                <span class="stamp-line">SKIN</span>
                <span class="stamp-line">KNOWS</span>
                <span class="stamp-line">NO ONE</span>
                <span class="stamp-line">DAYS</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 8. WHY SHOP WITH LUMÉA?                                          -->
    <!-- ================================================================= -->
    <section class="value-props-section reveal-on-scroll">
      <div class="container">
        <h2 class="props-heading">WHY SHOP WITH LUMÉA?</h2>

        <div class="props-grid">
          <div
            v-for="(prop, idx) in valueProps"
            :key="prop.title"
            class="prop-item stagger-item"
            :style="{ transitionDelay: `${idx * 70}ms` }"
          >
            <div class="prop-icon-circle">
              <component :is="prop.icon" :size="20" />
            </div>
            <h4 class="prop-title">{{ prop.title }}</h4>
            <p class="prop-desc">{{ prop.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 9. THE LUMÉA EDIT / JOURNAL STORIES                              -->
    <!-- ================================================================= -->
    <section class="lumea-edit-section reveal-on-scroll" id="journal">
      <div class="container">
        <div class="edit-layout">
          <!-- Left Editorial Sidebar -->
          <div class="edit-intro-col">
            <span class="edit-eyebrow">THE LUMÉA EDIT</span>
            <h2 class="edit-title">Skincare Stories<br>& Expert Tips.</h2>
            <p class="edit-desc">
              Learn, explore, and make informed choices for your skin.
            </p>
            <button class="btn btn-pill-dark edit-journal-btn" @click="activeArticle = articlesList[0]">
              <span>Read Our Journal</span>
              <ArrowRight :size="16" />
            </button>
          </div>

          <!-- 3 Editorial Article Cards -->
          <div class="edit-articles-col">
            <div
              v-for="(article, idx) in articlesList"
              :key="article.title"
              class="article-card stagger-item"
              :style="{ transitionDelay: `${idx * 100}ms` }"
              @click="activeArticle = article"
            >
              <div class="article-image-box">
                <img :src="article.image" :alt="article.title" class="article-img" />
              </div>
              <div class="article-text-body">
                <span class="article-tag">{{ article.tag }}</span>
                <h4 class="article-title">{{ article.title }}</h4>
                <span class="article-read-more">
                  <span>Read More</span>
                  <ArrowRight :size="13" />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 10. NEWSLETTER ("Be the First to Know.")                         -->
    <!-- ================================================================= -->
    <section class="newsletter-banner-section reveal-on-scroll">
      <div class="container">
        <div class="newsletter-banner-card">
          <div class="newsletter-content">
            <h2 class="newsletter-title">Be the First to Know.</h2>
            <p class="newsletter-sub">Get exclusive offers, new arrivals, and skincare tips.</p>

            <form @submit.prevent="handleSubscribe" class="newsletter-form">
              <div class="newsletter-input-box">
                <input
                  type="email"
                  v-model="newsletterEmail"
                  placeholder="Your email address"
                  required
                />
                <button type="submit" class="newsletter-submit-btn" aria-label="Subscribe">
                  <ArrowRight :size="17" />
                </button>
              </div>
              <div v-if="newsletterSubscribed" class="newsletter-success">
                ✨ Thank you for subscribing! Check your inbox for your 10% welcome gift.
              </div>
            </form>
          </div>

          <div class="newsletter-script-overlay">
            <span>Good<br>Skin<br>Brighter<br>Days</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- MODALS: Skin Quiz, Brand Story, Article Reader                     -->
    <!-- ================================================================= -->
    <!-- Skin Quiz Modal -->
    <div v-if="showQuizModal" class="modal-backdrop" @click.self="showQuizModal = false">
      <div class="quiz-modal-card">
        <div class="modal-top">
          <span class="modal-badge">SKIN ROUTINE CONSULTANT</span>
          <button class="modal-close-x" @click="showQuizModal = false"><X :size="20" /></button>
        </div>

        <div v-if="quizStep < 3">
          <div class="quiz-progress-indicator">Step {{ quizStep }} of 2</div>
          <h3 class="quiz-step-title" v-if="quizStep === 1">What is your primary skin type?</h3>
          <h3 class="quiz-step-title" v-else>What is your top skincare goal?</h3>

          <div class="quiz-options-list" v-if="quizStep === 1">
            <button class="quiz-option-btn" @click="quizAnswers.skinType = 'dry'; quizStep = 2">
              <strong>Dry / Dehydrated</strong> — Flaky, tight, seeks rich moisture
            </button>
            <button class="quiz-option-btn" @click="quizAnswers.skinType = 'oily'; quizStep = 2">
              <strong>Oily / Combination</strong> — Shine in T-zone, enlarged pores
            </button>
            <button class="quiz-option-btn" @click="quizAnswers.skinType = 'sensitive'; quizStep = 2">
              <strong>Sensitive</strong> — Prone to redness, seeks barrier calm
            </button>
          </div>

          <div class="quiz-options-list" v-else>
            <button class="quiz-option-btn" @click="finishQuiz('Luminous Glass Glow')">
              <strong>Luminous Glass Skin</strong> — Radiance, tone clarity & hydration
            </button>
            <button class="quiz-option-btn" @click="finishQuiz('Barrier Repair & Calm')">
              <strong>Barrier Repair</strong> — Soothing ceramides, moisture sealing
            </button>
            <button class="quiz-option-btn" @click="finishQuiz('Pore & Texture Refinement')">
              <strong>Pore & Texture Care</strong> — Gentle smoothing, zinc & niacinamide
            </button>
          </div>
        </div>

        <!-- Quiz Result -->
        <div v-else class="quiz-result-view">
          <div class="result-check">✨</div>
          <h3>Your Personalized Routine: {{ quizResultRoutine }}</h3>
          <p>Based on your profile, we recommend pairing <strong>SK-II Facial Treatment Essence</strong> with <strong>The Ordinary Niacinamide</strong> and <strong>LANEIGE Lip Mask</strong> for optimal barrier glow.</p>

          <div class="result-actions">
            <button class="btn btn-pill-dark btn-block" @click="addQuizBundleToCart">
              Add Routine Bundle to Cart ($131.90)
            </button>
            <button class="btn btn-pill-outline btn-block" @click="showQuizModal = false">
              Explore Store
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Brand Story Modal -->
    <div v-if="showStoryModal" class="modal-backdrop" @click.self="showStoryModal = false">
      <div class="story-modal-card">
        <div class="modal-top">
          <span class="modal-badge">LUMÉA ATELIER PHILOSOPHY</span>
          <button class="modal-close-x" @click="showStoryModal = false"><X :size="20" /></button>
        </div>
        <div class="story-body">
          <img
            src="/images/hero-skincare.jpg"
            alt="Luméa Story"
            class="story-img"
          />
          <h3>Beauty Born from Intention.</h3>
          <p>
            At Luméa, we believe skincare is not a chore—it is an intimate, restorative ritual. We curate the world's most scientifically rigorous and botanically reverent formulations from Milan, Tokyo, Seoul, and Paris.
          </p>
          <p>
            Every product in our collection is 100% authentic, verified by dermatological standards, and packaged with mindful sustainability.
          </p>
          <button class="btn btn-pill-dark" @click="showStoryModal = false">
            Explore Curations
          </button>
        </div>
      </div>
    </div>

    <!-- Article Reader Modal -->
    <div v-if="activeArticle" class="modal-backdrop" @click.self="activeArticle = null">
      <div class="article-modal-card">
        <div class="modal-top">
          <span class="modal-badge">{{ activeArticle.tag }}</span>
          <button class="modal-close-x" @click="activeArticle = null"><X :size="20" /></button>
        </div>
        <img :src="activeArticle.image" :alt="activeArticle.title" class="article-modal-hero" />
        <h2 class="article-modal-title">{{ activeArticle.title }}</h2>
        <div class="article-modal-content">
          <p>{{ activeArticle.summary }}</p>
          <p>
            Key takeaway: Consistent hydration and sun defense (SPF 50+) constitute 80% of long-term skin health. Always patch test new actives like vitamin C or AHA/BHA exfoliants, and allow your lipid barrier 4 to 6 weeks to acclimate.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BrandLogo from '@/components/BrandLogo.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useCartStore } from '@/stores/cart'
import { useBannerStore } from '@/stores/banners'
import {
  ArrowRight,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Clock,
  FlaskConical,
  Heart,
  Play,
  RotateCcw,
  ShieldCheck,
  ShoppingBag,
  ShoppingCart,
  Sparkles,
  Truck,
  X
} from 'lucide-vue-next'
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const cartStore = useCartStore()
const bannerStore = useBannerStore()

const homeBanner = computed(() =>
  bannerStore.getBanner('home', {
    image_url: '/images/ai-banner-atelier.jpg',
    title: 'Your Skincare Destination',
  })
)

// State
const activeSlide = ref(1)
const wishlist = ref([101, 103])
const addedProductId = ref(null)
const newsletterEmail = ref('')
const newsletterSubscribed = ref(false)

// Modals
const showQuizModal = ref(false)
const quizStep = ref(1)
const quizAnswers = ref({ skinType: '', goal: '' })
const quizResultRoutine = ref('')
const showStoryModal = ref(false)
const activeArticle = ref(null)

// Brand Horizon Partners
const marqueeBrands = [
  'SK-II',
  'LANEIGE',
  'The Ordinary',
  'CeraVe',
  'BIODERMA',
  'LA ROCHE-POSAY',
  'innisfree',
  'COSRX',
  'anua',
  'CAUDALIE',
  'Beauty of Joseon',
]

// 1. Categories List (All local, zero broken links)
const categoriesList = [
  {
    name: 'Cleansers',
    slug: 'cleansers',
    image: '/images/hero-skincare.jpg',
  },
  {
    name: 'Toners',
    slug: 'toners',
    image: '/images/cat-toners.jpg',
  },
  {
    name: 'Serums',
    slug: 'serums',
    image: '/images/prod-ordinary.jpg',
  },
  {
    name: 'Moisturizers',
    slug: 'moisturizers',
    image: '/images/prod-cerave.jpg',
  },
  {
    name: 'Sunscreens',
    slug: 'sunscreens',
    image: '/images/prod-boj.jpg',
  },
  {
    name: 'Masks',
    slug: 'masks',
    image: '/images/cat-masks.jpg',
  },
  {
    name: 'Treatments',
    slug: 'treatments',
    image: '/images/prod-sk2.jpg',
  },
  {
    name: 'Kits & Sets',
    slug: 'kits',
    image: '/images/cat-kits.jpg',
  },
]

// 2. Best Sellers List (Authentic high-res studio photos matching reference design)
const bestSellersList = [
  {
    id: 101,
    brand: 'SK-II',
    name: 'Facial Treatment Essence',
    slug: 'sk-ii-facial-treatment-essence',
    price: 99.00,
    rating: 4.8,
    reviews: '1.2k',
    image_url: '/images/prod-sk2.jpg',
  },
  {
    id: 102,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1%',
    slug: 'the-ordinary-niacinamide-10-zinc-1',
    price: 8.90,
    rating: 4.7,
    reviews: '950',
    image_url: '/images/prod-ordinary.jpg',
  },
  {
    id: 103,
    brand: 'LANEIGE',
    name: 'Lip Sleeping Mask',
    slug: 'laneige-lip-sleeping-mask',
    price: 24.00,
    rating: 4.9,
    reviews: '2.1k',
    image_url: '/images/prod-laneige.jpg',
  },
  {
    id: 104,
    brand: 'CeraVe',
    name: 'Moisturizing Cream',
    slug: 'cerave-moisturizing-cream',
    price: 24.00,
    rating: 4.7,
    reviews: '3.5k',
    image_url: '/images/prod-cerave.jpg',
  },
  {
    id: 105,
    brand: 'Beauty of Joseon',
    name: 'Relief Sun SPF 50+',
    slug: 'beauty-of-joseon-relief-sun-spf50',
    price: 22.00,
    rating: 4.9,
    reviews: '1.9k',
    image_url: '/images/prod-boj.jpg',
  },
]

// 3. Brand Circles
const brandCircles = [
  { name: 'SK-II' },
  { name: 'The Ordinary.' },
  { name: 'CeraVe' },
  { name: 'LA ROCHE-POSAY' },
  { name: 'BIODERMA' },
  { name: 'innisfree' },
  { name: 'COSRX' },
  { name: 'anua' },
]

// 4. Value Props
const valueProps = [
  { icon: Sparkles, title: '100+ Trusted Brands', desc: 'All in one place' },
  { icon: ShieldCheck, title: '100% Authentic', desc: 'Guaranteed' },
  { icon: Truck, title: 'Fast & Reliable Shipping', desc: 'Nationwide' },
  { icon: RotateCcw, title: 'Easy Returns', desc: 'Hassle-free' },
  { icon: FlaskConical, title: 'Skincare Guidance', desc: 'Expert tips & quizzes' },
]

// 5. Articles List (The Luméa Edit - High-Res Editorial Photography)
const articlesList = [
  {
    tag: 'SKINCARE 101',
    title: "How to Build a Skincare Routine (Beginner's Guide)",
    image: '/images/article-routine.jpg',
    summary: 'A step-by-step foundation covering gentle cleansing, hydration layering, active antioxidants, and daily SPF defense.',
  },
  {
    tag: 'INGREDIENTS',
    title: '5 Ingredients Your Skin Will Love',
    image: '/images/article-ingredients.jpg',
    summary: 'From hyaluronic acid to ceramides, niacinamide, and centella asiatica—discover the powerhouse molecules transforming everyday complexions.',
  },
  {
    tag: 'TIPS',
    title: "Morning vs Night Skincare: What's the Difference?",
    image: '/images/article-daynight.jpg',
    summary: 'Daytime is for antioxidant defense and UV shielding; nighttime is reserved for cellular repair, gentle peeling, and barrier replenishment.',
  },
]

// Apple-Inspired Fluid Scroll Animation Observer
let scrollObserver = null

onMounted(() => {
  bannerStore.fetchBanners()

  // Positive rootMargin (120px) triggers before elements enter the screen,
  // completely eliminating blank white spaces or stuck/laggy scroll pauses!
  const options = {
    threshold: 0.02,
    rootMargin: '120px 0px -20px 0px',
  }

  scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
        // Unobserve immediately so browser doesn't re-calculate intersections on scroll
        scrollObserver.unobserve(entry.target)
      }
    })
  }, options)

  const elements = document.querySelectorAll('.reveal-on-scroll')
  elements.forEach((el) => scrollObserver.observe(el))
})

onUnmounted(() => {
  if (scrollObserver) {
    scrollObserver.disconnect()
  }
})

// Slider Controls
function nextSlide() {
  activeSlide.value = activeSlide.value === 3 ? 1 : activeSlide.value + 1
}

function prevSlide() {
  activeSlide.value = activeSlide.value === 1 ? 3 : activeSlide.value - 1
}

// Navigation & Actions
function filterByCategory(slug) {
  router.push({ path: '/shop', query: { category: slug } })
}

function filterByBrand(name) {
  router.push({ path: '/shop', query: { brand: name } })
}

function goToProduct(slug) {
  router.push(`/product/${slug}`)
}

function toggleWishlist(id) {
  if (wishlist.value.includes(id)) {
    wishlist.value = wishlist.value.filter((item) => item !== id)
  } else {
    wishlist.value.push(id)
  }
}

function addToBag(product) {
  cartStore.addItem({
    id: product.id,
    name: product.name,
    slug: product.slug,
    price: product.price,
    image_url: product.image_url,
    category_name: product.brand,
  })
  addedProductId.value = product.id
  setTimeout(() => {
    addedProductId.value = null
  }, 1800)
  cartStore.openDrawer()
}

function scrollBrands() {
  router.push('/shop')
}

// Quiz
function finishQuiz(routineName) {
  quizAnswers.value.goal = routineName
  quizResultRoutine.value = routineName
  quizStep.value = 3
}

function addQuizBundleToCart() {
  cartStore.addItem(bestSellersList[0])
  cartStore.addItem(bestSellersList[1])
  cartStore.addItem(bestSellersList[2])
  showQuizModal.value = false
  cartStore.openDrawer()
}

// Newsletter
function handleSubscribe() {
  if (newsletterEmail.value) {
    newsletterSubscribed.value = true
    setTimeout(() => {
      newsletterEmail.value = ''
      newsletterSubscribed.value = false
    }, 4000)
  }
}
</script>

<style scoped>
.lumea-home-page {
  background-color: #FAF8F5; /* Exact warm ivory hue from design */
  color: #1C1917;
  overflow-x: hidden;
}

/* ================================================================= */
/* SCROLL REVEAL & STAGGER ANIMATIONS (Apple & Emil Kowalski Fluid Curve) */
/* ================================================================= */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.38s cubic-bezier(0.23, 1, 0.32, 1), transform 0.38s cubic-bezier(0.23, 1, 0.32, 1);
}

.reveal-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.reveal-on-scroll.is-visible .stagger-item {
  opacity: 1;
  transform: translateY(0);
}

.stagger-item {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.35s cubic-bezier(0.23, 1, 0.32, 1), transform 0.35s cubic-bezier(0.23, 1, 0.32, 1);
}

/* Keyframe animations for hero */
.animate-fade-in {
  animation: fadeIn 0.8s ease forwards;
}

.animate-fade-in-up {
  animation: fadeInUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.delay-1 { animation-delay: 0.15s; }
.delay-2 { animation-delay: 0.3s; }
.delay-3 { animation-delay: 0.45s; }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ================================================================= */
/* 1. HERO SECTION                                                  */
/* ================================================================= */
.hero-section {
  padding: 1.75rem 0 2rem;
  background: linear-gradient(180deg, #FAF8F5 0%, #FAF8F5 100%);
  position: relative;
}

.hero-container {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  align-items: center;
  gap: 2.5rem;
}

.hero-eyebrow {
  display: inline-block;
  font-size: 0.74rem;
  letter-spacing: 0.18em;
  font-weight: 600;
  color: #8E4A3E;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.hero-headline {
  font-family: var(--font-serif);
  font-size: clamp(2.3rem, 3.5vw, 3.2rem);
  font-weight: 500;
  line-height: 1.15;
  color: #1C1917;
  letter-spacing: -0.02em;
  margin-bottom: 0.75rem;
}

.hero-description {
  font-size: 0.95rem;
  color: #57534E;
  line-height: 1.5;
  max-width: 440px;
  margin-bottom: 1.25rem;
}

.hero-cta-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.btn-pill-dark {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  background: #242721;
  color: #FFFFFF;
  padding: 0.65rem 1.5rem;
  border-radius: var(--radius-full);
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-fast);
  border: none;
  cursor: pointer;
}

.btn-pill-dark:hover {
  background: #171914;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(36, 39, 33, 0.25);
}

.btn-pill-outline {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  color: #1C1917;
  border: 1px solid rgba(28, 25, 23, 0.25);
  padding: 0.65rem 1.4rem;
  border-radius: var(--radius-full);
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-pill-outline:hover {
  border-color: #1C1917;
  background: rgba(28, 25, 23, 0.04);
  transform: translateY(-1px);
}

.play-icon {
  fill: currentColor;
}

/* Slider Controls */
.hero-slider-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.slider-progress-track {
  width: 120px;
  height: 2px;
  background: rgba(28, 25, 23, 0.12);
  position: relative;
  border-radius: 2px;
}

.slider-progress-fill {
  height: 100%;
  background: #1C1917;
  transition: width 0.35s ease;
}

.slider-counter {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.slide-num {
  font-size: 0.78rem;
  color: #8C877F;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.slide-num.is-active {
  color: #1C1917;
  font-weight: 700;
}

.slider-arrows {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.slider-arrow-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: none;
  border: 1px solid rgba(28, 25, 23, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #57534E;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.slider-arrow-btn:hover {
  border-color: #1C1917;
  color: #1C1917;
}

/* Hero Visual Column */
.hero-visual-col {
  position: relative;
  display: flex;
  justify-content: center;
}

.hero-image-stage {
  position: relative;
  width: 100%;
  max-width: 430px;
}

.bottles-scene {
  position: relative;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 20px 45px rgba(70, 50, 40, 0.08);
  background: #FAF8F5;
  max-height: 340px;
}

.main-scene-img {
  width: 100%;
  max-height: 340px;
  display: block;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.bottles-scene:hover .main-scene-img {
  transform: scale(1.03);
}

.floating-script-callout {
  position: absolute;
  top: -16px;
  right: -12px;
  z-index: 10;
  pointer-events: none;
  animation: floatSlow 4s ease-in-out infinite alternate;
}

@keyframes floatSlow {
  0% { transform: translateY(0); }
  100% { transform: translateY(-8px); }
}

.script-phrase {
  font-family: var(--font-script);
  font-style: italic;
  font-size: 1.45rem;
  line-height: 1.15;
  color: #7A2E22;
  display: block;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.8);
}

/* ================================================================= */
/* 2. HORIZON BRANDS ANIMATION MARQUEE                              */
/* ================================================================= */
.horizon-brands-section {
  padding: 1.75rem 0;
  border-top: 1px solid rgba(28, 25, 23, 0.07);
  border-bottom: 1px solid rgba(28, 25, 23, 0.07);
  background: #FFFFFF;
  position: relative;
  overflow: hidden;
}

.horizon-track-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}

.horizon-track-wrapper::before,
.horizon-track-wrapper::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 90px;
  z-index: 2;
  pointer-events: none;
}

.horizon-track-wrapper::before {
  left: 0;
  background: linear-gradient(90deg, #FFFFFF 0%, transparent 100%);
}

.horizon-track-wrapper::after {
  right: 50px;
  background: linear-gradient(270deg, #FFFFFF 0%, transparent 100%);
}

.horizon-marquee {
  display: flex;
  overflow: hidden;
  user-select: none;
  width: 100%;
}

.marquee-group {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  min-width: 100%;
  gap: 4.5rem;
  padding-right: 4.5rem;
  animation: horizonMarquee 26s linear infinite;
}

.horizon-marquee:hover .marquee-group {
  animation-play-state: paused;
}

@keyframes horizonMarquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}

.marquee-brand-item {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-sm);
  transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1), opacity 0.2s cubic-bezier(0.23, 1, 0.32, 1);
  color: #2D2825;
}

.marquee-brand-item:hover {
  transform: translateY(-2px) scale(1.03);
  color: #732A24;
}

.marquee-brand-item:active {
  transform: scale(0.96);
}

.horizon-nav-btn {
  position: absolute;
  right: 1.5rem;
  z-index: 5;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.15);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #44403C;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.horizon-nav-btn:hover {
  border-color: #1C1917;
  color: #1C1917;
  transform: translateX(2px);
}

/* ================================================================= */
/* 3. SHOP BY CATEGORY                                              */
/* ================================================================= */
.categories-section {
  padding: 4.5rem 0 3.5rem;
}

.section-headline-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.section-title-tag {
  font-family: var(--font-sans);
  font-size: 0.92rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #1C1917;
  text-transform: uppercase;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.view-all-link:hover {
  color: #8E4A3E;
}

.categories-pill-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 1.25rem;
}

.cat-pill-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  text-align: center;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.cat-pill-card:hover {
  transform: translateY(-5px);
}

.cat-pill-pedestal {
  width: 100%;
  aspect-ratio: 1 / 1.1;
  background: #F4EFEB;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 1rem;
  border: 1px solid rgba(28, 25, 23, 0.05);
  transition: background 0.3s ease, box-shadow 0.3s ease;
}

.cat-pill-card:hover .cat-pill-pedestal {
  background: #EFE8E0;
  box-shadow: 0 10px 24px rgba(70, 50, 40, 0.08);
}

.cat-bottle-icon {
  width: 82%;
  height: 82%;
  object-fit: contain;
  mix-blend-mode: multiply;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.cat-pill-card:hover .cat-bottle-icon {
  transform: scale(1.1);
}

.cat-pill-title {
  margin-top: 0.75rem;
  font-size: 0.84rem;
  font-weight: 500;
  color: #44403C;
}

/* ================================================================= */
/* 4. SPECIAL OFFER BANNER ("Glow More Spend Less.")                 */
/* ================================================================= */
.special-offer-section {
  padding: 2rem 0 4rem;
}

.special-offer-card {
  background: #DFD8CF; /* Exact warm earthen beige tone from design */
  border-radius: var(--radius-xl);
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  align-items: center;
  overflow: hidden;
  position: relative;
  box-shadow: 0 14px 40px rgba(50, 40, 30, 0.06);
}

.offer-text-block {
  padding: 3.5rem 4rem;
}

.offer-eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  letter-spacing: 0.16em;
  font-weight: 700;
  color: #8E4A3E;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
}

.offer-title {
  font-family: var(--font-serif);
  font-size: clamp(2.4rem, 3.5vw, 3.2rem);
  font-weight: 500;
  line-height: 1.18;
  color: #1C1917;
  letter-spacing: -0.01em;
  margin-bottom: 0.85rem;
}

.offer-desc {
  font-size: 0.95rem;
  color: #57534E;
  margin-bottom: 2rem;
}

.offer-btn {
  padding: 0.85rem 2rem;
}

.offer-visual-block {
  position: relative;
  height: 100%;
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.offer-hero-bottles {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.special-offer-card:hover .offer-hero-bottles {
  transform: scale(1.03);
}

.offer-badge-circle {
  position: absolute;
  top: 2rem;
  right: 2.5rem;
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: rgba(250, 248, 245, 0.92);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(28, 25, 23, 0.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.1;
  z-index: 5;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.badge-sub { font-size: 0.62rem; font-weight: 600; color: #78716C; }
.badge-percent { font-family: var(--font-serif); font-size: 1.65rem; font-weight: 600; color: #7A2E22; }
.badge-off { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em; color: #78716C; }

.offer-script-tag {
  position: absolute;
  bottom: 2rem;
  right: 2.5rem;
  z-index: 5;
  text-align: right;
}

.offer-script-tag span {
  font-family: var(--font-script);
  font-style: italic;
  font-size: 2rem;
  line-height: 1.1;
  color: #7A2E22;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.85);
}

/* ================================================================= */
/* 5. BEST SELLERS                                                  */
/* ================================================================= */
.best-sellers-section {
  padding: 3rem 0 4rem;
}

.products-carousel-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.15rem;
}

.beauty-product-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.07);
  border-radius: 14px;
  padding: 0.95rem 0.95rem 1.05rem;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1), box-shadow 0.25s ease, border-color 0.25s ease;
}

.beauty-product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(70, 50, 40, 0.06);
  border-color: rgba(28, 25, 23, 0.12);
}

.beauty-product-card:active {
  transform: scale(0.98);
}

.card-wishlist-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #8C877F;
  z-index: 5;
  transition: color var(--transition-fast), transform var(--transition-fast);
}

.card-wishlist-btn:hover {
  color: #8E4A3E;
  transform: scale(1.15);
}

.card-wishlist-btn.is-active {
  color: #8E4A3E;
}

.product-stage {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-bottom: 0.75rem;
  background: #F4EFEB;
  position: relative;
}

.product-bottle-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.35s cubic-bezier(0.23, 1, 0.32, 1);
}

.beauty-product-card:hover .product-bottle-img {
  transform: scale(1.05);
}

.product-meta {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.product-brand-tag {
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: #1C1917;
  margin-bottom: 2px;
}

.product-title {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 400;
  color: #78716C;
  line-height: 1.25;
  cursor: pointer;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-title:hover {
  color: #1C1917;
}

.product-rating-row {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.68rem;
  margin-bottom: 4px;
}

.rating-stars {
  color: #F59E0B;
  letter-spacing: 0.5px;
  font-size: 0.68rem;
}

.rating-score {
  font-weight: 600;
  color: #1C1917;
}

.reviews-count {
  color: #78716C;
}

.product-pricing {
  margin-bottom: 8px;
  margin-top: 2px;
}

.product-price {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.btn-add-cart {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.52rem 0.65rem;
  border-radius: 6px;
  background: #F4EFEB;
  border: 1px solid rgba(28, 25, 23, 0.06);
  font-size: 0.78rem;
  font-weight: 600;
  color: #1C1917;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.btn-add-cart:hover {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
  transform: translateY(-1px);
}

.btn-add-cart:active {
  transform: scale(0.97);
}

.btn-add-cart.btn-added {
  background: #242721;
  color: #FFFFFF;
}

/* ================================================================= */
/* 6. BROWSE BY BRAND                                               */
/* ================================================================= */
.browse-brands-section {
  padding: 2.5rem 0 4rem;
}

.brand-circles-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.25rem;
  overflow-x: auto;
  padding: 0.5rem 0;
}

.brand-circle-item {
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.65rem;
  transition: transform 0.25s cubic-bezier(0.23, 1, 0.32, 1);
}

.brand-circle-item:hover {
  transform: translateY(-4px);
}

.brand-circle-item:active {
  transform: scale(0.94);
}

.brand-circle-badge {
  width: 104px;
  height: 104px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.85rem;
  text-align: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast), background var(--transition-fast);
}

.brand-circle-item:hover .brand-circle-badge {
  border-color: #8E4A3E;
  box-shadow: 0 8px 24px rgba(168, 90, 60, 0.12);
  background: #FFFDFB;
}

.brand-circle-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #57534E;
  letter-spacing: 0.02em;
  text-align: center;
  transition: color var(--transition-fast);
}

.brand-circle-item:hover .brand-circle-label {
  color: #1C1917;
}

.brand-circle-arrow {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1C1917;
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.brand-circle-arrow:hover {
  background: #242721;
  color: #FFFFFF;
}

/* ================================================================= */
/* 7. ROUTINE QUIZ BANNER ("Find Your Routine.")                     */
/* ================================================================= */
.quiz-banner-section {
  padding: 2rem 0 4.5rem;
}

.quiz-banner-card {
  background: #EBE5DD; /* Exact warm soft stone from design */
  border-radius: var(--radius-xl);
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  align-items: center;
  overflow: hidden;
  position: relative;
  box-shadow: 0 12px 35px rgba(50, 40, 30, 0.05);
}

.quiz-content-col {
  padding: 4rem 4.5rem;
}

.quiz-eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  letter-spacing: 0.16em;
  font-weight: 700;
  color: #8E4A3E;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
}

.quiz-title {
  font-family: var(--font-serif);
  font-size: clamp(2.4rem, 3.8vw, 3.2rem);
  font-weight: 500;
  line-height: 1.15;
  color: #1C1917;
  letter-spacing: -0.01em;
  margin-bottom: 0.85rem;
}

.quiz-desc {
  font-size: 0.95rem;
  color: #57534E;
  margin-bottom: 2rem;
  max-width: 440px;
}

.quiz-start-btn {
  padding: 0.85rem 2rem;
  margin-bottom: 2.5rem;
}

.quiz-highlights-strip {
  display: flex;
  align-items: center;
  gap: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(28, 25, 23, 0.1);
}

.highlight-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #44403C;
}

.quiz-visual-col {
  position: relative;
  height: 100%;
  min-height: 420px;
  overflow: hidden;
}

.model-visual-stage {
  position: relative;
  width: 100%;
  height: 100%;
}

.quiz-model-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.quiz-banner-card:hover .quiz-model-img {
  transform: scale(1.03);
}

.editorial-stamp-badge {
  position: absolute;
  top: 3rem;
  right: 3rem;
  width: 105px;
  height: 105px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.65);
  background: rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(8px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  line-height: 1.25;
}

.stamp-line {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #FFFFFF;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.35);
}

/* ================================================================= */
/* 8. WHY SHOP WITH LUMÉA?                                          */
/* ================================================================= */
.value-props-section {
  padding: 4.5rem 0;
  background: #FFFFFF;
  border-top: 1px solid rgba(28, 25, 23, 0.06);
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
}

.props-heading {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #1C1917;
  text-align: center;
  margin-bottom: 3rem;
}

.props-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2rem;
  text-align: center;
}

.prop-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.3s ease;
}

.prop-item:hover {
  transform: translateY(-4px);
}

.prop-icon-circle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #FAF8F5;
  border: 1px solid rgba(28, 25, 23, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1C1917;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.prop-item:hover .prop-icon-circle {
  background: #242721;
  color: #FFFFFF;
}

.prop-title {
  font-family: var(--font-sans);
  font-size: 0.9rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.25rem;
}

.prop-desc {
  font-size: 0.78rem;
  color: #8C877F;
}

/* ================================================================= */
/* 9. THE LUMÉA EDIT / JOURNAL STORIES                              */
/* ================================================================= */
.lumea-edit-section {
  padding: 5rem 0;
}

.edit-layout {
  display: grid;
  grid-template-columns: 1fr 2.5fr;
  gap: 3.5rem;
}

.edit-eyebrow {
  font-size: 0.75rem;
  letter-spacing: 0.16em;
  font-weight: 700;
  color: #8E4A3E;
  text-transform: uppercase;
  display: inline-block;
  margin-bottom: 0.85rem;
}

.edit-title {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  font-weight: 500;
  line-height: 1.25;
  color: #1C1917;
  margin-bottom: 1rem;
}

.edit-desc {
  font-size: 0.92rem;
  color: #57534E;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.edit-journal-btn {
  padding: 0.85rem 1.85rem;
}

.edit-articles-col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.article-card {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-image-box {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: 1rem;
}

.article-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.article-card:hover .article-img {
  transform: scale(1.06);
}

.article-tag {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #8E4A3E;
  text-transform: uppercase;
  margin-bottom: 0.4rem;
  display: inline-block;
}

.article-title {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.35;
  color: #1C1917;
  margin-bottom: 0.75rem;
}

.article-read-more {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #1C1917;
  transition: color var(--transition-fast);
}

.article-card:hover .article-read-more {
  color: #8E4A3E;
}

/* ================================================================= */
/* 10. NEWSLETTER ("Be the First to Know.")                         */
/* ================================================================= */
.newsletter-banner-section {
  padding: 2rem 0 4.5rem;
}

.newsletter-banner-card {
  background: #E5DED5; /* Exact warm sand/linen from design */
  border-radius: var(--radius-xl);
  padding: 4.5rem 5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
}

.newsletter-content {
  max-width: 520px;
  position: relative;
  z-index: 5;
}

.newsletter-title {
  font-family: var(--font-serif);
  font-size: clamp(2.2rem, 3.5vw, 2.8rem);
  font-weight: 500;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.newsletter-sub {
  font-size: 0.95rem;
  color: #57534E;
  margin-bottom: 1.75rem;
}

.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.newsletter-input-box {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border-radius: var(--radius-full);
  padding: 0.4rem 0.5rem 0.4rem 1.5rem;
  border: 1px solid rgba(28, 25, 23, 0.1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.newsletter-input-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.9rem;
  color: #1C1917;
}

.newsletter-submit-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #242721;
  color: #FFFFFF;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background var(--transition-fast), transform var(--transition-fast);
}

.newsletter-submit-btn:hover {
  background: #171914;
  transform: scale(1.05);
}

.newsletter-success {
  font-size: 0.85rem;
  color: #15803D;
  font-weight: 600;
}

.newsletter-script-overlay {
  position: absolute;
  right: 5rem;
  top: 50%;
  transform: translateY(-50%);
  text-align: right;
  pointer-events: none;
}

.newsletter-script-overlay span {
  font-family: var(--font-script);
  font-style: italic;
  font-size: 2.8rem;
  line-height: 1.1;
  color: #8E4A3E;
  opacity: 0.85;
}

/* ================================================================= */
/* MODALS STYLING                                                   */
/* ================================================================= */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.65);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 1.5rem;
}

.quiz-modal-card,
.story-modal-card,
.article-modal-card {
  width: 100%;
  max-width: 580px;
  background: #FFFFFF;
  border-radius: var(--radius-xl);
  padding: 2.5rem;
  box-shadow: var(--shadow-lg);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.modal-badge {
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  font-weight: 700;
  color: #8E4A3E;
}

.modal-close-x {
  background: none;
  border: none;
  cursor: pointer;
  color: #8C877F;
  transition: color var(--transition-fast);
}

.modal-close-x:hover {
  color: #1C1917;
}

.quiz-progress-indicator {
  font-size: 0.8rem;
  color: #8C877F;
  margin-bottom: 0.5rem;
}

.quiz-step-title {
  font-family: var(--font-serif);
  font-size: 1.45rem;
  color: #1C1917;
  margin-bottom: 1.5rem;
}

.quiz-options-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.quiz-option-btn {
  text-align: left;
  padding: 1.15rem 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(28, 25, 23, 0.12);
  background: #FAF8F5;
  font-size: 0.9rem;
  color: #44403C;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.quiz-option-btn:hover {
  border-color: #8E4A3E;
  background: #FFFFFF;
  box-shadow: 0 4px 14px rgba(196, 98, 60, 0.1);
}

.quiz-result-view {
  text-align: center;
}

.result-check {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.quiz-result-view h3 {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  color: #1C1917;
  margin-bottom: 0.75rem;
}

.quiz-result-view p {
  font-size: 0.92rem;
  color: #57534E;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.result-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-block {
  width: 100%;
  justify-content: center;
}

.story-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.story-body h3 {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}

.story-body p {
  font-size: 0.92rem;
  color: #57534E;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}

.article-modal-hero {
  width: 100%;
  height: 240px;
  object-fit: cover;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.article-modal-title {
  font-family: var(--font-serif);
  font-size: 1.65rem;
  color: #1C1917;
  margin-bottom: 1rem;
}

.article-modal-content p {
  font-size: 0.95rem;
  color: #44403C;
  line-height: 1.7;
  margin-bottom: 1rem;
}

/* ================================================================= */
/* RESPONSIVE DESIGN                                                */
/* ================================================================= */
@media (max-width: 1100px) {
  .categories-pill-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .products-carousel-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .props-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .special-offer-card,
  .quiz-banner-card {
    grid-template-columns: 1fr;
  }

  .offer-text-block,
  .quiz-content-col {
    padding: 3rem 2.5rem;
  }

  .edit-layout {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .products-carousel-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .categories-pill-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .edit-articles-col {
    grid-template-columns: 1fr;
  }

  .props-grid {
    grid-template-columns: 1fr 1fr;
  }

  .newsletter-banner-card {
    padding: 3rem 2rem;
  }

  .newsletter-script-overlay {
    display: none;
  }
}
</style>
