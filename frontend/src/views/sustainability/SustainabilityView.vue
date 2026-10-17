<template>
  <div class="lumea-sustainability-page">
    <!-- Top Hero Section matching format/Luméa Sustainability.png -->
    <header class="sustainability-hero-section">
      <div class="container hero-inner">
        <div class="hero-text-content">
          <span class="hero-eyebrow">{{ pageData.badge_text || 'BEAUTY • SCIENCE • YOU' }}</span>
          <h1 class="hero-title">{{ pageData.title }}</h1>
          <p class="hero-subtitle">{{ pageData.subtitle }}</p>
          <div class="hero-actions">
            <router-link to="/shop" class="btn-shop-collection">
              Shop the Collection &rarr;
            </router-link>
          </div>
        </div>

        <div class="hero-portrait-frame">
          <img
            :src="pageData.hero_image || '/images/ai-model-sustainability.jpg'"
            alt="Glow Healthier, Live Brighter - Luméa Atelier"
            class="hero-model-img"
          />
        </div>
      </div>
    </header>

    <!-- 4 Value Propositions Strip -->
    <section class="value-props-section">
      <div class="container">
        <div class="value-props-grid">
          <div class="value-prop-card">
            <div class="icon-circle">
              <Truck :size="20" />
            </div>
            <div class="prop-text">
              <h4>Free Shipping</h4>
              <p>On orders over $50</p>
            </div>
          </div>

          <div class="value-prop-card">
            <div class="icon-circle">
              <ShieldCheck :size="20" />
            </div>
            <div class="prop-text">
              <h4>Authentic Products</h4>
              <p>100% genuine brands</p>
            </div>
          </div>

          <div class="value-prop-card">
            <div class="icon-circle">
              <Gift :size="20" />
            </div>
            <div class="prop-text">
              <h4>Exclusive Deals</h4>
              <p>For our community</p>
            </div>
          </div>

          <div class="value-prop-card">
            <div class="icon-circle">
              <Headphones :size="20" />
            </div>
            <div class="prop-text">
              <h4>Expert Skincare Support</h4>
              <p>Always here to help</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Shop by Category Section -->
    <section class="categories-matrix-section">
      <div class="container">
        <div class="section-title-row">
          <div>
            <h2 class="section-heading">Shop by Category</h2>
            <p class="section-subtext">Find the perfect care for your unique skin needs</p>
          </div>
          <router-link to="/shop" class="explore-all-link">
            Explore All Categories &rarr;
          </router-link>
        </div>

        <div class="categories-pill-grid">
          <router-link
            v-for="cat in categoriesList"
            :key="cat.slug"
            :to="`/category/${cat.slug}`"
            class="category-card-pill"
          >
            <div class="pill-media">
              <img :src="cat.image" :alt="cat.name" class="pill-img" />
            </div>
            <div class="pill-footer">
              <span class="pill-name">{{ cat.name }}</span>
              <div class="pill-arrow-circle">
                <ArrowRight :size="14" />
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Interactive Diagnostics & Latest Insights Strip -->
    <section class="dual-feature-section">
      <div class="container">
        <div class="dual-feature-grid">
          <!-- Left: Routine Quiz Feature Banner -->
          <div class="feature-quiz-card">
            <div class="quiz-text-side">
              <h3 class="feature-title">Discover Your Personalized Skincare Routine</h3>
              <p class="feature-desc">
                Take our Skin Quiz and get a routine made just for you based on dermatological analytics.
              </p>
              <router-link to="/quiz" class="btn-quiz-primary">
                Take the Quiz &rarr;
              </router-link>
            </div>
            <div class="quiz-visual-side">
              <img
                src="/images/sustainability-quiz-phone.jpg"
                alt="Personalized Routine Diagnostics App"
                class="quiz-phone-img"
              />
            </div>
          </div>

          <!-- Right: Latest Editorial Feature Banner -->
          <div class="feature-article-card">
            <div class="article-card-header">
              <h3>Latest from Luméa</h3>
              <router-link to="/articles" class="view-all-text">View All &rarr;</router-link>
            </div>

            <router-link to="/articles/how-to-layer-skincare-products-in-the-right-order" class="article-preview-link">
              <div class="preview-thumb-frame">
                <img
                  src="/images/article-thumb-layer.jpg"
                  alt="The Right Way to Layer Your Skincare Products"
                  class="preview-img"
                />
              </div>
              <div class="preview-content">
                <span class="preview-tag">Skincare Tips</span>
                <h4 class="preview-title">The Right Way to Layer Your Skincare Products</h4>
                <span class="preview-date">Aug 28, 2025 &bull; 5 min read</span>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  Truck,
  ShieldCheck,
  Gift,
  Headphones,
  ArrowRight
} from 'lucide-vue-next'

const pageData = ref({
  title: 'Glow Healthier, Live Brighter',
  subtitle: 'Premium skincare, expert insights, and personalized care — all in one place.',
  badge_text: 'BEAUTY • SCIENCE • YOU',
  hero_image: '/images/sustainability-hero-model.jpg'
})

const categoriesList = ref([
  { name: 'Skincare Essentials', slug: 'cleansers', image: '/images/cat-cleansers.jpg' },
  { name: 'Serums & Treatments', slug: 'serums', image: '/images/cat-serums.jpg' },
  { name: 'Moisturizers', slug: 'moisturizers', image: '/images/cat-moisturizers.jpg' },
  { name: 'Sunscreen', slug: 'sunscreens', image: '/images/cat-sunscreens.jpg' },
  { name: 'Cleansers', slug: 'cleansers', image: '/images/cat-cleansers-banner-stage.png' },
  { name: 'Masks & Treatments', slug: 'masks', image: '/images/cat-masks.jpg' }
])

async function loadSustainabilityData() {
  try {
    const res = await fetch('/api/pages/sustainability')
    if (res.ok) {
      const data = await res.json()
      pageData.value = {
        title: data.title || pageData.value.title,
        subtitle: data.subtitle || pageData.value.subtitle,
        badge_text: data.badge_text || pageData.value.badge_text,
        hero_image: data.hero_image || pageData.value.hero_image
      }
      if (data.content_json?.categories) {
        categoriesList.value = data.content_json.categories
      }
    }
  } catch (err) {
    console.warn('[SustainabilityView] Using fallback:', err)
  }
}

onMounted(() => {
  loadSustainabilityData()
})
</script>

<style scoped>
.lumea-sustainability-page {
  background: #FCFAF7;
  min-height: 100vh;
  padding-bottom: 5rem;
  color: #1C1917;
}

/* Hero Section */
.sustainability-hero-section {
  background: linear-gradient(135deg, #FBF3EE 0%, #F5EFEB 100%);
  padding: 3rem 0;
  border-bottom: 1px solid rgba(122, 46, 34, 0.08);
}

.hero-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 3rem;
}

.hero-eyebrow {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #7A2E22;
  margin-bottom: 1rem;
}

.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.8rem, 4.5vw, 4.2rem);
  font-weight: 600;
  color: #7A2E22;
  line-height: 1.1;
  margin: 0 0 1.25rem;
}

.hero-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.1rem;
  color: #57534E;
  line-height: 1.6;
  max-width: 500px;
  margin: 0 0 2rem;
}

.btn-shop-collection {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.92rem;
  font-weight: 500;
  padding: 0.85rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-shop-collection:hover {
  background: #5E2117;
  transform: translateY(-1px);
}

.hero-portrait-frame {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.hero-model-img {
  width: 100%;
  max-width: 580px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 12px 35px -8px rgba(122, 46, 34, 0.15);
}

/* Value Props Strip */
.value-props-section {
  padding: 2.5rem 0;
  background: #FFFFFF;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.value-props-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.value-prop-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #FAF2EE;
  color: #7A2E22;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.prop-text h4 {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.2rem;
}

.prop-text p {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #78716C;
  margin: 0;
}

/* Shop by Category Matrix */
.categories-matrix-section {
  padding: 4.5rem 0 3.5rem;
}

.section-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.section-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.2rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.4rem;
}

.section-subtext {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  color: #78716C;
  margin: 0;
}

.explore-all-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
  transition: gap 0.2s;
}

.categories-pill-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.25rem;
}

.category-card-pill {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.category-card-pill:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(122, 46, 34, 0.08);
}

.pill-media {
  height: 120px;
  overflow: hidden;
  background: #F5EFEB;
}

.pill-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.category-card-pill:hover .pill-img {
  transform: scale(1.05);
}

.pill-footer {
  padding: 0.85rem 0.9rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.pill-name {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.3;
}

.pill-arrow-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #FAF2EE;
  color: #7A2E22;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.2s, color 0.2s;
}

.category-card-pill:hover .pill-arrow-circle {
  background: #7A2E22;
  color: #FFFFFF;
}

/* Dual Feature Strip */
.dual-feature-section {
  padding: 1.5rem 0 3.5rem;
}

.dual-feature-grid {
  display: grid;
  grid-template-columns: 1.35fr 0.85fr;
  gap: 2rem;
}

.feature-quiz-card {
  background: #FAF2EE;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 12px;
  padding: 2.25rem;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  align-items: center;
  gap: 1.5rem;
}

.feature-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.7rem;
  font-weight: 600;
  color: #7A2E22;
  line-height: 1.25;
  margin: 0 0 0.75rem;
}

.feature-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  color: #57534E;
  line-height: 1.55;
  margin: 0 0 1.5rem;
}

.btn-quiz-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  font-weight: 500;
  padding: 0.75rem 1.4rem;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.2s;
}

.btn-quiz-primary:hover {
  background: #5E2117;
}

.quiz-visual-side {
  display: flex;
  justify-content: center;
}

.quiz-phone-img {
  width: 100%;
  max-width: 240px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.feature-article-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 12px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
}

.article-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.article-card-header h3 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0;
}

.view-all-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
}

.article-preview-link {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preview-thumb-frame {
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.article-preview-link:hover .preview-img {
  transform: scale(1.03);
}

.preview-tag {
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  color: #7A2E22;
  display: block;
  margin-bottom: 0.35rem;
}

.preview-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.35;
  margin: 0 0 0.35rem;
}

.preview-date {
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  color: #78716C;
}

/* Responsive */
@media (max-width: 1100px) {
  .hero-inner {
    grid-template-columns: 1fr;
  }
  .hero-portrait-frame {
    justify-content: center;
  }
  .value-props-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .categories-pill-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .dual-feature-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 650px) {
  .categories-pill-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .value-props-grid {
    grid-template-columns: 1fr;
  }
  .feature-quiz-card {
    grid-template-columns: 1fr;
  }
}
</style>
