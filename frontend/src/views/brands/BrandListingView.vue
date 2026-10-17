<template>
  <div class="brand-listing-page">
    <!-- Breadcrumbs -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">Brands</span>
      </nav>
    </div>

    <!-- Boxed Hero Banner matching Brand Listing.png -->
    <section class="container banner-container">
      <div class="brand-hero-card">
        <div class="brand-hero-left">
          <h1 class="hero-title">Explore Our<br />Skincare Brands.</h1>
          <p class="hero-subtitle">
            100+ trusted global and local brands. Authentic products.<br />Real results. A healthier, happier you.
          </p>

          <div class="hero-search-box">
            <Search :size="18" class="search-box-icon" />
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search brands (e.g. SK-II, CeraVe, Innisfree...)"
              class="hero-search-input"
            />
            <button v-if="searchQuery" @click="searchQuery = ''" class="clear-btn" aria-label="Clear search">
              <X :size="15" />
            </button>
          </div>
        </div>

        <div class="brand-hero-right">
          <div class="hero-visual-wrap">
            <img
              src="/images/banner-brands.jpg"
              alt="Explore Our Skincare Brands"
              class="hero-stage-img"
            />
            <div class="hero-callout-circle">
              <span>More Brands.<br />Healthier Skin.</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 5 Value Guarantees Strip matching Brand Listing.png -->
    <section class="container guarantees-container">
      <div class="guarantees-grid">
        <div class="guarantee-item">
          <div class="guarantee-icon-wrap">
            <ShieldCheck :size="20" />
          </div>
          <div class="guarantee-text">
            <span class="guarantee-title">100+ Trusted Brands</span>
            <span class="guarantee-sub">All in one place</span>
          </div>
        </div>

        <div class="guarantee-item">
          <div class="guarantee-icon-wrap">
            <CheckCircle :size="20" />
          </div>
          <div class="guarantee-text">
            <span class="guarantee-title">100% Authentic</span>
            <span class="guarantee-sub">Guaranteed</span>
          </div>
        </div>

        <div class="guarantee-item">
          <div class="guarantee-icon-wrap">
            <Truck :size="20" />
          </div>
          <div class="guarantee-text">
            <span class="guarantee-title">Global &amp; Local Brands</span>
            <span class="guarantee-sub">From around the world</span>
          </div>
        </div>

        <div class="guarantee-item">
          <div class="guarantee-icon-wrap">
            <Award :size="20" />
          </div>
          <div class="guarantee-text">
            <span class="guarantee-title">Curated by Experts</span>
            <span class="guarantee-sub">Only the best for your skin</span>
          </div>
        </div>

        <div class="guarantee-item">
          <div class="guarantee-icon-wrap">
            <Sparkles :size="20" />
          </div>
          <div class="guarantee-text">
            <span class="guarantee-title">Skincare for a</span>
            <span class="guarantee-sub">Brighter Tomorrow.</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content: All Brands 6-Col Grid + Featured Brands Sidebar -->
    <section class="container directory-section">
      <div class="directory-layout">
        <!-- Left: 6-Column Brand Logo Grid -->
        <div class="directory-main">
          <!-- Heading & Alphabet Bar -->
          <div class="brands-section-header">
            <h2 class="section-title">All Brands</h2>
            <span class="brands-count-badge">100+ Brands</span>
          </div>

          <!-- Alphabet Filter Bar -->
          <div class="alphabet-filter-bar">
            <button
              class="alpha-pill"
              :class="{ active: selectedLetter === 'ALL' }"
              @click="selectedLetter = 'ALL'"
            >
              All
            </button>
            <button
              v-for="letter in alphabet"
              :key="letter"
              class="alpha-letter-btn"
              :class="{ active: selectedLetter === letter }"
              @click="selectedLetter = letter"
            >
              {{ letter }}
            </button>
            <button
              class="alpha-letter-btn"
              :class="{ active: selectedLetter === '#' }"
              @click="selectedLetter = '#'"
            >
              #
            </button>
          </div>

          <!-- 6-Column Rectangular Logo Grid matching Brand Listing.png -->
          <div v-if="filteredBrands.length > 0" class="brands-six-grid">
            <router-link
              v-for="brand in visibleBrands"
              :key="brand.id"
              :to="`/brand/${brand.slug}`"
              class="brand-logo-card"
            >
              <div class="card-logo-container">
                <BrandLogo :slug="brand.slug" :size="38" />
              </div>
              <span class="card-products-count">{{ brand.count }} products</span>
            </router-link>
          </div>

          <!-- Load More Brands Button -->
          <div v-if="hasMoreBrands" class="load-more-wrap">
            <button @click="loadMore" class="load-more-btn">
              <span>Load More Brands</span>
              <ChevronDown :size="16" />
            </button>
          </div>

          <!-- Empty State -->
          <div v-if="filteredBrands.length === 0" class="empty-brands-box">
            <p>No brands found matching "{{ searchQuery }}".</p>
            <button @click="resetFilters" class="reset-link-btn">Reset Search</button>
          </div>
        </div>

        <!-- Right: 4 Featured Brands Cards matching Brand Listing.png -->
        <aside class="featured-brands-sidebar">
          <div class="featured-sidebar-header">
            <h3 class="featured-heading">Featured Brands</h3>
            <router-link to="/brands" class="view-all-link">
              <span>View All</span>
              <ArrowRight :size="14" />
            </router-link>
          </div>

          <div class="featured-cards-stack">
            <!-- Card 1: SK-II -->
            <div class="feat-brand-banner banner-sk2">
              <div class="banner-text-col">
                <div class="banner-brand-logo">
                  <BrandLogo slug="sk-ii" :size="30" />
                </div>
                <p class="banner-tagline">Timeless Beauty<br />Through Science.</p>
                <router-link to="/brand/sk-ii" class="banner-cta-btn cta-sk2">
                  <span>Shop SK-II</span>
                  <ArrowRight :size="13" />
                </router-link>
              </div>
              <div class="banner-img-col">
                <img src="/images/feat-sk2-card.jpg" alt="SK-II Featured" class="feat-img" />
              </div>
            </div>

            <!-- Card 2: innisfree -->
            <div class="feat-brand-banner banner-innisfree">
              <div class="banner-text-col">
                <div class="banner-brand-logo">
                  <BrandLogo slug="innisfree" :size="28" />
                </div>
                <p class="banner-tagline">Pure Ingredients<br />from Nature.</p>
                <router-link to="/brand/innisfree" class="banner-cta-btn cta-innisfree">
                  <span>Shop Innisfree</span>
                  <ArrowRight :size="13" />
                </router-link>
              </div>
              <div class="banner-img-col">
                <img src="/images/feat-innisfree-card.jpg" alt="Innisfree Featured" class="feat-img" />
              </div>
            </div>

            <!-- Card 3: The Ordinary -->
            <div class="feat-brand-banner banner-ordinary">
              <div class="banner-text-col">
                <div class="banner-brand-logo">
                  <BrandLogo slug="the-ordinary" :size="26" />
                </div>
                <p class="banner-tagline">Clinical Formulations.<br />Real Results.</p>
                <router-link to="/brand/the-ordinary" class="banner-cta-btn cta-ordinary">
                  <span>Shop The Ordinary</span>
                  <ArrowRight :size="13" />
                </router-link>
              </div>
              <div class="banner-img-col">
                <img src="/images/feat-ordinary-card.jpg" alt="The Ordinary Featured" class="feat-img" />
              </div>
            </div>

            <!-- Card 4: Can't Find Your Favorite Brand? -->
            <div class="feat-brand-banner banner-request">
              <div class="banner-text-col">
                <h4 class="request-banner-title">Can't Find Your<br />Favorite Brand?</h4>
                <p class="request-banner-sub">
                  Let us know! We're always looking to bring in more brands for you.
                </p>
                <button @click="openRequestModal" class="banner-cta-btn cta-request">
                  <span>Request a Brand</span>
                  <ArrowRight :size="13" />
                </button>
              </div>
              <div class="banner-img-col">
                <img src="/images/feat-request-card.jpg" alt="Request a Brand" class="feat-img" />
              </div>
            </div>
          </div>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  ChevronRight,
  ChevronDown,
  Search,
  X,
  ShieldCheck,
  CheckCircle,
  Truck,
  Award,
  Sparkles,
  ArrowRight,
} from 'lucide-vue-next'
import BrandLogo from '@/components/BrandLogo.vue'
import { BRANDS_DIRECTORY } from '@/stores/products'

const searchQuery = ref('')
const selectedLetter = ref('ALL')
const displayLimit = ref(24)

const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')

const filteredBrands = computed(() => {
  let list = [...BRANDS_DIRECTORY]

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim()
    list = list.filter(
      (b) =>
        b.name.toLowerCase().includes(q) ||
        b.origin.toLowerCase().includes(q) ||
        b.desc.toLowerCase().includes(q)
    )
  }

  if (selectedLetter.value !== 'ALL') {
    if (selectedLetter.value === '#') {
      list = list.filter((b) => !/^[A-Z]/i.test(b.name))
    } else {
      list = list.filter((b) => b.name.toUpperCase().startsWith(selectedLetter.value))
    }
  }

  return list
})

const visibleBrands = computed(() => {
  return filteredBrands.value.slice(0, displayLimit.value)
})

const hasMoreBrands = computed(() => {
  return displayLimit.value < filteredBrands.value.length
})

function loadMore() {
  displayLimit.value += 12
}

function resetFilters() {
  searchQuery.value = ''
  selectedLetter.value = 'ALL'
  displayLimit.value = 24
}

function openRequestModal() {
  const brand = prompt('Which skincare brand would you love Luméa to carry?')
  if (brand) {
    alert(`Thank you! We have submitted your request for "${brand}" to our beauty curation team.`)
  }
}
</script>

<style scoped>
.brand-listing-page {
  padding-bottom: 5rem;
  background-color: #FAF8F5;
  min-height: 100vh;
}

/* Breadcrumbs */
.breadcrumb-container {
  padding-top: 0.6rem;
  padding-bottom: 0.5rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
}

.breadcrumb-link {
  color: #8E4A3E;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: #73382E;
  text-decoration: underline;
}

.breadcrumb-sep {
  color: #8E4A3E;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* Hero Banner matching Brand Listing.png */
.banner-container {
  margin-bottom: 1.25rem;
}

.brand-hero-card {
  background: linear-gradient(135deg, #FAF4EF 0%, #F6EBE2 50%, #ECE0D5 100%);
  border: 1px solid rgba(196, 98, 60, 0.12);
  border-radius: 16px;
  padding: 1.75rem 2.5rem;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  box-shadow: 0 4px 20px rgba(78, 59, 45, 0.04);
  position: relative;
  overflow: hidden;
  min-height: 275px;
}

.brand-hero-left {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
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

.hero-subtitle {
  font-size: 1.05rem;
  line-height: 1.45;
  color: #57534E;
  margin-bottom: 1.15rem;
}

.hero-search-box {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background-color: #FFFFFF;
  border: 1px solid #E5DED6;
  border-radius: 9999px;
  padding: 0.55rem 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  max-width: 440px;
}

.search-box-icon {
  color: #8E2B2B;
  flex-shrink: 0;
}

.hero-search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.88rem;
  color: #1C1917;
  outline: none;
}

.hero-search-input::placeholder {
  color: #9C948B;
}

.clear-btn {
  background: none;
  border: none;
  color: #78716C;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-hero-right {
  width: 480px;
  flex-shrink: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 1;
}

.hero-visual-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.hero-stage-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 14px;
  mask-image: linear-gradient(to right, transparent 0%, black 18%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 18%);
  box-shadow: 0 8px 24px rgba(40, 20, 10, 0.06);
}

.hero-callout-circle {
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
  animation: ambientFloat 4.5s ease-in-out infinite;
  z-index: 3;
}

@keyframes ambientFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

.hero-callout-circle span {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8E2B2B;
  line-height: 1.2;
}

/* 5 Value Guarantees Strip */
.guarantees-container {
  margin-bottom: 2.5rem;
}

.guarantees-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.guarantee-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.guarantee-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FDF4F0;
  color: #8E4A3E;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.guarantee-text {
  display: flex;
  flex-direction: column;
}

.guarantee-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
}

.guarantee-sub {
  font-size: 0.72rem;
  color: #78716C;
}

/* Main Directory Layout */
.directory-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2.5rem;
  align-items: start;
}

/* Directory Left */
.brands-section-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #7A2E22;
}

.brands-count-badge {
  font-size: 0.85rem;
  color: #78716C;
  font-weight: 500;
}

/* Alphabet Filter Bar */
.alphabet-filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: nowrap;
  gap: 0.15rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid #EAE5DF;
  overflow-x: auto;
}

.alpha-pill {
  background: #6D3B2E;
  color: #FFFFFF;
  border: none;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  cursor: pointer;
  flex-shrink: 0;
}

.alpha-letter-btn {
  background: none;
  border: none;
  font-size: 0.76rem;
  font-weight: 600;
  color: #78716C;
  padding: 0.2rem 0.25rem;
  cursor: pointer;
  transition: color 0.15s ease;
  flex-shrink: 0;
}

.alpha-letter-btn:hover {
  color: #8E4A3E;
}

.alpha-letter-btn.active {
  color: #8E4A3E;
  font-weight: 800;
}

/* 6-Column Rectangular Card Grid matching Brand Listing.png */
.brands-six-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.85rem;
  margin-bottom: 2rem;
}

.brand-logo-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 10px;
  height: 105px;
  padding: 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}

.brand-logo-card:hover {
  border-color: #8E4A3E;
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.1);
  transform: translateY(-2px);
}

.card-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.card-products-count {
  font-size: 0.74rem;
  color: #78716C;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* Load More Brands Button */
.load-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.load-more-btn {
  background: #FFFFFF;
  border: 1px solid #D6CEC5;
  border-radius: 8px;
  padding: 0.65rem 1.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1C1917;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.load-more-btn:hover {
  background: #FAF8F5;
  border-color: #8E4A3E;
  color: #8E4A3E;
}

/* Featured Brands Right Sidebar */
.featured-brands-sidebar {
  display: flex;
  flex-direction: column;
  position: sticky;
  top: calc(var(--navbar-height, 68px) + 1.25rem);
  max-height: calc(100vh - var(--navbar-height, 68px) - 2rem);
  overflow-y: auto;
  scrollbar-width: thin;
}

.featured-sidebar-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.featured-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #7A2E22;
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.featured-cards-stack {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

/* 4 Featured Brand Banners */
.feat-brand-banner {
  border-radius: 12px;
  padding: 1.1rem 0 1.1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  position: relative;
  min-height: 125px;
}

.banner-text-col {
  flex: 1;
  z-index: 2;
}

.banner-brand-logo {
  margin-bottom: 0.4rem;
  display: flex;
  align-items: center;
}

.banner-tagline {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.88rem;
  line-height: 1.35;
  color: #1C1917;
  margin-bottom: 0.75rem;
}

.banner-cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.85rem;
  border-radius: 6px;
  font-size: 0.74rem;
  font-weight: 700;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.banner-cta-btn:hover {
  opacity: 0.9;
}

.banner-img-col {
  width: 145px;
  height: 125px;
  margin: -1.1rem 0 -1.1rem 0;
  border-radius: 0 12px 12px 0;
  overflow: hidden;
  flex-shrink: 0;
}

.feat-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Colors for the 4 banners matching format */
.banner-sk2 {
  background: #FCECE8;
  border: 1px solid rgba(185, 28, 28, 0.1);
}
.cta-sk2 {
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 9999px;
  padding: 0.45rem 1.15rem;
}
.cta-sk2:hover {
  background: #75392F;
}

.banner-innisfree {
  background: #EAF3EC;
  border: 1px solid rgba(21, 128, 61, 0.1);
}
.cta-innisfree {
  background: #3B543F;
  color: #FFFFFF;
  border-radius: 9999px;
  padding: 0.45rem 1.15rem;
}
.cta-innisfree:hover {
  background: #2D4131;
}

.banner-ordinary {
  background: #F3EFEB;
  border: 1px solid rgba(28, 25, 23, 0.08);
}
.cta-ordinary {
  background: #2E2D2B;
  color: #FFFFFF;
  border-radius: 9999px;
  padding: 0.45rem 1.15rem;
}
.cta-ordinary:hover {
  background: #1C1917;
}

.banner-request {
  background: #FDF0EB;
  border: 1px solid rgba(142, 74, 62, 0.14);
}
.cta-request {
  background: #8E4A3E;
  color: #FFFFFF;
  border-radius: 9999px;
  padding: 0.45rem 1.15rem;
}
.cta-request:hover {
  background: #75392F;
}

.request-banner-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.98rem;
  font-weight: 700;
  color: #7A2E22;
  line-height: 1.25;
  margin-bottom: 0.35rem;
}
.request-banner-sub {
  font-size: 0.74rem;
  line-height: 1.4;
  color: #78716C;
  margin-bottom: 0.85rem;
}
.cta-request {
  background: #8E4A3E;
  color: #FFFFFF;
}

/* Empty State */
.empty-brands-box {
  text-align: center;
  padding: 3rem;
  background: #FFFFFF;
  border-radius: 12px;
  border: 1px solid #EAE5DF;
  color: #78716C;
}

.reset-link-btn {
  background: none;
  border: none;
  color: #8E4A3E;
  font-weight: 700;
  text-decoration: underline;
  cursor: pointer;
  margin-top: 0.5rem;
}

/* Responsive */
@media (max-width: 1200px) {
  .brands-six-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .brand-hero-card {
    flex-direction: column;
    padding: 2rem;
    text-align: center;
  }
  .hero-search-box {
    margin: 0 auto;
  }
  .guarantees-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .directory-layout {
    grid-template-columns: 1fr;
  }
  .brands-six-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 600px) {
  .brands-six-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .guarantees-grid {
    grid-template-columns: 1fr;
  }
}
</style>
