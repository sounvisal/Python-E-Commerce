<template>
  <div class="deals-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">Deals</span>
      </nav>
    </div>

    <!-- Hero Banner matching Deals.png -->
    <section class="container banner-container">
      <div class="deals-hero-card">
        <div class="hero-left-content">
          <h1 class="hero-title">Deals</h1>
          <h2 class="hero-tagline">Beauty You Love. Better Prices.</h2>
          <p class="hero-desc">
            Discover limited-time offers, brand promotions, and exclusive bundles from your favorite skincare brands. Authentic products. Real results. Greater value.
          </p>

          <!-- 4 Trust items in a horizontal row matching Deals.png -->
          <div class="hero-trust-row">
            <div class="trust-item">
              <ShieldCheck :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Authentic Products</span>
                <span class="trust-sub">Guaranteed</span>
              </div>
            </div>
            <div class="trust-item">
              <Clock :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Limited-Time Offers</span>
                <span class="trust-sub">Don't miss out</span>
              </div>
            </div>
            <div class="trust-item">
              <ShoppingBag :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Top Skincare Brands</span>
                <span class="trust-sub">In one place</span>
              </div>
            </div>
            <div class="trust-item">
              <Sparkles :size="18" class="trust-icon" />
              <div class="trust-text">
                <span class="trust-label">Better Beauty</span>
                <span class="trust-sub">For Everyone</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero-right-visual">
          <div class="hero-stage-wrap">
            <img
              src="/images/banners/banner-deals-clean.jpg"
              alt="Luméa Deals Collection"
              class="hero-packshot-img"
            />
            <div class="hero-callout-oval">
              <span class="callout-text">Good<br />Skincare<br />Brighter<br />Days.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Flash Deals Pills & Live Countdown Bar matching Deals.png -->
    <section class="container flash-bar-container">
      <div class="flash-deals-bar">
        <!-- Left Filter Pills -->
        <div class="flash-pills-left">
          <button
            class="deal-tab-pill"
            :class="{ active: selectedFilter === 'all' }"
            @click="selectedFilter = 'all'"
          >
            All Deals
          </button>
          <button
            class="deal-tab-pill"
            :class="{ active: selectedFilter === 'flash' }"
            @click="selectedFilter = 'flash'"
          >
            <Flame :size="14" class="pill-icon" />
            <span>Flash Deals</span>
          </button>
          <button
            class="deal-tab-pill"
            :class="{ active: selectedFilter === 'brand' }"
            @click="selectedFilter = 'brand'"
          >
            <ShoppingBag :size="14" class="pill-icon" />
            <span>Brand Promotions</span>
          </button>
          <button
            class="deal-tab-pill"
            :class="{ active: selectedFilter === 'bundles' }"
            @click="selectedFilter = 'bundles'"
          >
            <Gift :size="14" class="pill-icon" />
            <span>Bundle Offers</span>
          </button>
          <button
            class="deal-tab-pill"
            :class="{ active: selectedFilter === 'clearance' }"
            @click="selectedFilter = 'clearance'"
          >
            <Tag :size="14" class="pill-icon" />
            <span>Clearance</span>
          </button>
        </div>

        <!-- Right Countdown Timer -->
        <div class="flash-countdown-right">
          <span class="flash-countdown-label">Flash Deals End In</span>
          <div class="countdown-digits-group">
            <div class="digit-unit">
              <span class="digit-val">{{ padZero(countdown.hours) }}</span>
              <span class="digit-sub">Hours</span>
            </div>
            <span class="digit-colon">:</span>
            <div class="digit-unit">
              <span class="digit-val">{{ padZero(countdown.minutes) }}</span>
              <span class="digit-sub">Minutes</span>
            </div>
            <span class="digit-colon">:</span>
            <div class="digit-unit">
              <span class="digit-val">{{ padZero(countdown.seconds) }}</span>
              <span class="digit-sub">Seconds</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Top Promo Showcase: 2/3 Wide Banner + 1/3 Stacked Banners matching Deals.png -->
    <section class="container promo-showcase-section">
      <div class="promo-showcase-grid">
        <!-- 2/3 Left Wide Banner: Up to 50% Off -->
        <div class="promo-banner-wide" @click="selectedFilter = 'all'">
          <div class="promo-wide-content">
            <span class="promo-tag-pill">LIMITED TIME</span>
            <h2 class="promo-wide-title">Up to<br /><span class="highlight-discount">50% Off</span></h2>
            <p class="promo-wide-sub">Your Favorite Skincare Brands</p>
            <router-link to="/deals/all" class="promo-wide-btn">
              Shop All Deals &rarr;
            </router-link>
          </div>

          <div class="promo-wide-center-visual">
            <img
              src="/images/deals-showcase-bottles.jpg"
              alt="Luxury Skincare Deals Showcase"
              class="wide-promo-bottles-img"
            />
          </div>

          <div class="promo-wide-right-editorial">
            <div class="wide-callout-script">
              <span class="script-line">Glow</span>
              <span class="script-line">More.</span>
              <span class="script-line">Spend Less.</span>
              <div class="script-divider"></div>
            </div>
          </div>
        </div>

        <!-- 1/3 Right Stacked Cards -->
        <div class="promo-stacked-col">
          <!-- Stack 1: Bundle & Save -->
          <div class="promo-stack-card stack-bundle">
            <div class="stack-content">
              <h3 class="stack-title">Bundle &amp; Save</h3>
              <p class="stack-desc">Skincare Sets for Every Routine</p>
              <router-link to="/deals/all?filter=bundles" class="stack-btn">Shop Bundle Offers &rarr;</router-link>
            </div>
            <div class="stack-visual">
              <img src="/images/deals-bundle-duo.jpg" alt="Skincare Bundles" class="stack-showcase-img" />
            </div>
          </div>

          <!-- Stack 2: Clearance Sale -->
          <div class="promo-stack-card stack-clearance">
            <div class="stack-content">
              <div class="clearance-badge-pill">Up to 70% Off</div>
              <h3 class="stack-title">Clearance Sale</h3>
              <p class="stack-desc">Last Chance Favorites</p>
              <router-link to="/deals/all?filter=clearance" class="stack-btn">Shop Clearance &rarr;</router-link>
            </div>
            <div class="stack-visual">
              <img src="/images/deals-clearance-duo.jpg" alt="Clearance Skincare" class="stack-showcase-img" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Deals Section matching Deals.png -->
    <section class="container featured-deals-section">
      <div class="section-header-row">
        <div>
          <h2 class="section-title">Featured Deals</h2>
          <p class="section-sub">Handpicked offers from top skincare brands.</p>
        </div>
        <router-link to="/deals/all" class="view-all-deals-link">
          View All Deals &rarr;
        </router-link>
      </div>

      <!-- 6 Featured Deals Cards Grid using standardized ProductCard matching HomeView -->
      <div class="featured-deals-grid">
        <div
          v-for="(deal, idx) in featuredDealsList"
          :key="deal.id"
          class="deal-card-stagger-item"
          :style="{ animationDelay: `${idx * 60}ms` }"
        >
          <ProductCard :product="deal" />
        </div>
      </div>
    </section>

    <!-- Bottom 3 Value Cards matching Deals.png -->
    <section class="container bottom-perks-section">
      <div class="bottom-perks-grid">
        <!-- 1. Student Beauty Special -->
        <div class="bottom-perk-card">
          <div class="perk-card-content">
            <div class="perk-icon-square">
              <GraduationCap :size="24" />
            </div>
            <h3 class="perk-card-title">Student Beauty Special</h3>
            <p class="perk-card-highlight">Extra 10% Off</p>
            <p class="perk-card-desc">with Student Verification</p>
            <button class="perk-card-btn" @click="notifyStudent">
              Learn More &rarr;
            </button>
          </div>
          <div class="perk-card-visual">
            <img src="/images/article-daynight.jpg" alt="Student Beauty" class="perk-img" />
          </div>
        </div>

        <!-- 2. New to Luméa -->
        <div class="bottom-perk-card">
          <div class="perk-card-content">
            <div class="perk-icon-square">
              <Gift :size="24" />
            </div>
            <h3 class="perk-card-title">New to Luméa?</h3>
            <p class="perk-card-highlight">Get 15% Off</p>
            <p class="perk-card-desc">Your First Order</p>
            <button class="perk-card-btn" @click="copyCode('LUMEA15')">
              Sign Up Now &rarr;
            </button>
          </div>
          <div class="perk-card-visual">
            <img src="/images/banner-newsletter.jpg" alt="New to Lumea" class="perk-img" />
          </div>
        </div>

        <!-- 3. Free Shipping -->
        <div class="bottom-perk-card">
          <div class="perk-card-content">
            <div class="perk-icon-square">
              <Truck :size="24" />
            </div>
            <h3 class="perk-card-title">Free Shipping</h3>
            <p class="perk-card-highlight">On Orders $50+</p>
            <p class="perk-card-desc">Shop more. Save more.</p>
            <router-link to="/shop" class="perk-card-btn">
              Shop Now &rarr;
            </router-link>
          </div>
          <div class="perk-card-visual">
            <img src="/images/cat-kits.jpg" alt="Free Shipping" class="perk-img" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import ProductCard from '@/components/ProductCard.vue'
import { useCartStore } from '@/stores/cart'
import { useNotificationStore } from '@/stores/notification'
import { useWishlistStore } from '@/stores/wishlist'
import {
  ChevronRight,
  Clock,
  Flame,
  Gift,
  GraduationCap,
  Heart,
  ShieldCheck,
  ShoppingBag,
  ShoppingCart,
  Sparkles,
  Tag,
  Truck
} from 'lucide-vue-next'
import { onMounted, onUnmounted, ref } from 'vue'

const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const notificationStore = useNotificationStore()

const selectedFilter = ref('all')

// Real-time countdown timer matching format: 12 : 34 : 56
const countdown = ref({
  hours: 12,
  minutes: 34,
  seconds: 56
})

let timer = null

onMounted(() => {
  timer = setInterval(() => {
    if (countdown.value.seconds > 0) {
      countdown.value.seconds--
    } else {
      countdown.value.seconds = 59
      if (countdown.value.minutes > 0) {
        countdown.value.minutes--
      } else {
        countdown.value.minutes = 59
        if (countdown.value.hours > 0) {
          countdown.value.hours--
        } else {
          countdown.value.hours = 24
        }
      }
    }
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function padZero(num) {
  return String(num).padStart(2, '0')
}

// 6 Featured Deals from format/Deals.png:
// SK-II ($99.00 / $142.00) 30% OFF
// Estee Lauder ($78.00 / $104.00) 25% OFF
// Laneige ($18.00 / $30.00) 40% OFF
// The Ordinary ($7.20 / $9.00) 20% OFF
// CeraVe ($16.00 / $24.50) 35% OFF
// Innisfree ($28.00 / $56.00) 50% OFF
const featuredDealsList = [
  {
    id: 201,
    brand: 'SK-II',
    name: 'Facial Treatment Essence',
    price: 99.00,
    compare_at_price: 142.00,
    discount: '30% OFF',
    rating: 4.8,
    reviews: '1.2K',
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence'
  },
  {
    id: 207,
    brand: 'Estée Lauder',
    name: 'Advanced Night Repair Synchronized Complex',
    price: 78.00,
    compare_at_price: 104.00,
    discount: '25% OFF',
    rating: 4.7,
    reviews: '892',
    image_url: '/images/prod-dermalogica.jpg',
    slug: 'estee-lauder-advanced-night-repair'
  },
  {
    id: 203,
    brand: 'Laneige',
    name: 'Lip Sleeping Mask Intense Moisture',
    price: 18.00,
    compare_at_price: 30.00,
    discount: '40% OFF',
    rating: 4.8,
    reviews: '1.5K',
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask'
  },
  {
    id: 202,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1%',
    price: 7.20,
    compare_at_price: 9.00,
    discount: '20% OFF',
    rating: 4.7,
    reviews: '9.8K',
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1'
  },
  {
    id: 204,
    brand: 'CeraVe',
    name: 'Moisturizing Cream Barrier Defense',
    price: 16.00,
    compare_at_price: 24.50,
    discount: '35% OFF',
    rating: 4.8,
    reviews: '6.2K',
    image_url: '/images/prod-cerave.jpg',
    slug: 'cerave-moisturizing-cream'
  },
  {
    id: 208,
    brand: 'Innisfree',
    name: 'Green Tea Seed Serum Intensive Hydration',
    price: 28.00,
    compare_at_price: 56.00,
    discount: '50% OFF',
    rating: 4.6,
    reviews: '2.1K',
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum'
  }
]

function addToCart(item) {
  cartStore.addItem({
    id: item.id,
    name: item.name,
    brand: item.brand,
    price: item.price,
    compare_at_price: item.compare_at_price,
    image_url: item.image_url,
    slug: item.slug
  })
}

function notifyStudent() {
  alert('Student Verification via StudentBeans opened. Enjoy your extra 10% off!')
}

function copyCode(code) {
  navigator.clipboard?.writeText(code)
  notificationStore.addToast(`Promo code ${code} copied! Apply at checkout.`, 'success')
}
</script>

<style scoped>
/* ==========================================================================
   DEALS PAGE (Strictly matches format/Deals.png)
   ========================================================================== */

.deals-page {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 5rem;
}

/* Breadcrumbs */
.breadcrumb-container {
  padding-top: 1.25rem;
  padding-bottom: 0.75rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.84rem;
  color: #57534E;
}

.breadcrumb-link {
  color: #57534E;
  text-decoration: none;
}

.breadcrumb-link:hover {
  color: #8E4A3E;
}

.breadcrumb-sep {
  color: #8C877F;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Hero Banner */
.banner-container {
  margin-bottom: 1.25rem;
}

.deals-hero-card {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border-radius: 16px;
  border: 1px solid rgba(196, 98, 60, 0.12);
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  overflow: hidden;
  min-height: 275px;
  padding: 1.75rem 2.5rem;
}

.hero-left-content {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
  padding: 0;
}

.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.75rem;
  font-weight: 700;
  color: #111C38;
  line-height: 1.12;
  margin-bottom: 0.35rem;
  letter-spacing: -0.015em;
}

.hero-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.45rem;
  line-height: 1.25;
}

.hero-desc {
  font-size: 0.92rem;
  line-height: 1.45;
  color: #57534E;
  margin-bottom: 1.15rem;
  max-width: 530px;
}

.hero-trust-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(196, 98, 60, 0.12);
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.trust-icon {
  color: #8E2B2B;
  flex-shrink: 0;
}

.trust-text {
  display: flex;
  flex-direction: column;
}

.trust-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
}

.trust-sub {
  font-size: 0.72rem;
  color: #78716C;
  line-height: 1.2;
}

/* Hero Right Stage */
.hero-right-visual {
  width: 480px;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 1;
}

.hero-stage-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.hero-packshot-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  mask-image: linear-gradient(to right, transparent 0%, black 18%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 18%);
  box-shadow: 0 8px 24px rgba(40, 20, 10, 0.06);
}

.hero-callout-oval {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 105px;
  height: 105px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.96) 40%, rgba(253, 242, 238, 0.9) 100%);
  border: 1px solid rgba(196, 98, 60, 0.35);
  box-shadow: 0 4px 16px rgba(142, 43, 43, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  z-index: 3;
}

.callout-text {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.2;
}

/* ==========================================================================
   FLASH DEALS BAR & COUNTDOWN (Matches Deals.png)
   ========================================================================== */
.flash-bar-container {
  margin-bottom: 2rem;
}

.flash-deals-bar {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 9999px;
  padding: 0.5rem 1.25rem 0.5rem 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.flash-pills-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  overflow-x: auto;
}

.deal-tab-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.55rem 1.15rem;
  background: transparent;
  border: none;
  border-radius: 9999px;
  font-family: var(--font-sans);
  font-size: 0.86rem;
  font-weight: 500;
  color: #44403C;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.deal-tab-pill:hover {
  color: #8E4A3E;
  background: #FAF8F5;
}

.deal-tab-pill.active {
  background: #8E4A3E;
  color: #FFFFFF;
}

.deal-tab-pill.active .pill-icon {
  color: #FFFFFF;
}

.pill-icon {
  color: #8E4A3E;
}

.flash-countdown-right {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-shrink: 0;
}

.flash-countdown-label {
  font-size: 0.86rem;
  font-weight: 600;
  color: #1C1917;
}

.countdown-digits-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.digit-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.digit-val {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1;
}

.digit-sub {
  font-size: 0.6rem;
  color: #8C877F;
  margin-top: 2px;
}

.digit-colon {
  font-size: 1.1rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1;
}

/* ==========================================================================
   PROMO SHOWCASE: 2/3 WIDE + 1/3 STACKED (Matches Deals.png)
   ========================================================================== */
.promo-showcase-section {
  margin-bottom: 3.5rem;
}

.promo-showcase-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

/* 2/3 Left Wide Banner */
.promo-banner-wide {
  background: linear-gradient(135deg, #FBF2EE 0%, #F7EAE5 50%, #F0DFD8 100%);
  border-radius: 16px;
  border: 1px solid rgba(142, 74, 62, 0.15);
  padding: 2.2rem 2.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  cursor: pointer;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.28s ease;
  position: relative;
  overflow: hidden;
}

.promo-banner-wide:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 32px rgba(142, 74, 62, 0.12);
}

.promo-wide-content {
  flex: 0 0 230px;
  max-width: 240px;
  z-index: 2;
}

.promo-tag-pill {
  display: inline-block;
  background: #FFFFFF;
  border: 1px solid rgba(142, 74, 62, 0.25);
  color: #8E4A3E;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  margin-bottom: 0.85rem;
}

.promo-wide-title {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.1;
  margin-bottom: 0.25rem;
}

.highlight-discount {
  color: #8E4A3E;
  font-size: 2.85rem;
  font-weight: 700;
  display: block;
}

.promo-wide-sub {
  font-size: 0.88rem;
  color: #57534E;
  margin-bottom: 1.35rem;
  line-height: 1.3;
}

.promo-wide-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.35rem;
  border-radius: 6px;
  font-size: 0.84rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.2);
}

.promo-wide-btn:hover {
  background: #73382D;
  transform: translateY(-1px);
}

.promo-wide-center-visual {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
}

.wide-promo-bottles-img {
  width: 100%;
  max-width: 380px;
  height: 205px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(142, 74, 62, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.promo-banner-wide:hover .wide-promo-bottles-img {
  transform: scale(1.03);
}

.promo-wide-right-editorial {
  flex: 0 0 110px;
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
}

.wide-callout-script {
  font-family: var(--font-serif);
  font-style: italic;
  color: #7A3326;
  font-size: 1.35rem;
  line-height: 1.25;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.wide-callout-script .script-line {
  display: block;
}

.script-divider {
  width: 28px;
  height: 2px;
  background: #8E4A3E;
  margin-top: 8px;
  border-radius: 2px;
  opacity: 0.6;
}

/* 1/3 Right Stacked Banners */
.promo-stacked-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.promo-stack-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 14px;
  padding: 1.35rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.22s ease;
  overflow: hidden;
}

.promo-stack-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(70, 40, 30, 0.08);
}

.stack-bundle {
  background: linear-gradient(135deg, #FAF4EF 0%, #F4EAE0 100%);
}

.stack-clearance {
  background: linear-gradient(135deg, #FDF2EE 0%, #F7E5DE 100%);
  border-color: rgba(142, 74, 62, 0.16);
}

.clearance-badge-pill {
  display: inline-block;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.16rem 0.55rem;
  border-radius: 4px;
  margin-bottom: 0.35rem;
}

.stack-title {
  font-family: var(--font-serif);
  font-size: 1.3rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 0.2rem;
  line-height: 1.2;
}

.stack-desc {
  font-size: 0.8rem;
  color: #57534E;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.stack-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.45rem 0.95rem;
  border-radius: 5px;
  font-size: 0.76rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
  transition: background 0.15s ease;
}

.stack-btn:hover {
  background: #73382D;
}

.stack-visual {
  flex: 0 0 120px;
  width: 120px;
  height: 110px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(40, 20, 10, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.stack-showcase-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.35s ease;
}

.promo-stack-card:hover .stack-showcase-img {
  transform: scale(1.06);
}

/* ==========================================================================
   FEATURED DEALS SECTION (Matches Deals.png)
   ========================================================================== */
.featured-deals-section {
  margin-bottom: 4rem;
}

.section-header-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 1.75rem;
}

.section-title {
  font-family: var(--font-serif);
  font-size: 1.65rem;
  color: #7A2E22;
  margin-bottom: 0.2rem;
}

.section-sub {
  font-size: 0.88rem;
  color: #57534E;
}

.view-all-deals-link {
  font-size: 0.86rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
}

.view-all-deals-link:hover {
  text-decoration: underline;
}

.featured-deals-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.15rem;
}

.format-deal-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 8px;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.format-deal-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(28, 25, 23, 0.06);
  border-color: #8E4A3E;
}

.card-top-stage {
  position: relative;
  width: 100%;
  height: 140px;
  background: #FAF8F5;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.discount-tag-pill {
  position: absolute;
  top: 6px;
  left: 6px;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.66rem;
  font-weight: 700;
  padding: 0.15rem 0.45rem;
  border-radius: 3px;
  z-index: 2;
}

.deal-heart-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  z-index: 2;
}

.card-img-wrap {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.deal-prod-img {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
  transition: transform 0.2s ease;
}

.format-deal-card:hover .deal-prod-img {
  transform: scale(1.06);
}

.card-bottom-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-brand {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.15rem;
}

.card-title {
  font-size: 0.8rem;
  font-weight: 500;
  line-height: 1.35;
  margin-bottom: 0.35rem;
  min-height: 2.2em;
}

.card-title a {
  color: #44403C;
  text-decoration: none;
}

.card-title a:hover {
  color: #8E4A3E;
}

.card-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.68rem;
  margin-bottom: 0.45rem;
}

.card-rating .stars {
  color: #D97706;
}

.rating-val {
  font-weight: 600;
  color: #1C1917;
}

.review-count {
  color: #8C877F;
}

.card-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  margin-bottom: 0.75rem;
  margin-top: auto;
}

.price-current {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.price-compare {
  font-size: 0.76rem;
  color: #8C877F;
  text-decoration: line-through;
}

/* Format Terracotta Button */
.format-add-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.52rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: 1px solid #8E4A3E;
  border-radius: 4px;
  font-size: 0.76rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.format-add-btn:hover {
  background: #73382D;
  border-color: #73382D;
}

/* ==========================================================================
   BOTTOM 3 VALUE CARDS (Matches Deals.png)
   ========================================================================== */
.bottom-perks-section {
  border-top: 1px solid rgba(28, 25, 23, 0.08);
  padding-top: 2rem;
}

.bottom-perks-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.bottom-perk-card {
  background: #FAF4F0;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 12px;
  padding: 1.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.perk-card-content {
  display: flex;
  flex-direction: column;
}

.perk-icon-square {
  color: #8E4A3E;
  margin-bottom: 0.75rem;
}

.perk-card-title {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.perk-card-highlight {
  font-size: 1.1rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 0.1rem;
}

.perk-card-desc {
  font-size: 0.78rem;
  color: #57534E;
  margin-bottom: 1rem;
}

.perk-card-btn {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.45rem 1rem;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  width: fit-content;
  transition: background 0.15s ease;
}

.perk-card-btn:hover {
  background: #73382D;
}

.perk-card-visual {
  width: 90px;
  height: 90px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
}

.perk-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Responsive */
@media (max-width: 1200px) {
  .featured-deals-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .promo-showcase-grid {
    grid-template-columns: 1fr;
  }
  .bottom-perks-grid {
    grid-template-columns: 1fr;
  }
  .deals-hero-card {
    grid-template-columns: 1fr;
  }
  .hero-trust-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .featured-deals-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
