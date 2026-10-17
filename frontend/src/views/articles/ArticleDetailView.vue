<template>
  <div class="lumea-article-detail-page">
    <div class="container article-page-container">
      <!-- Top Breadcrumbs -->
      <nav class="article-breadcrumb" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/articles">Articles</router-link>
        <span class="sep">&rsaquo;</span>
        <span class="cat-link">{{ article.category }}</span>
        <span class="sep">&rsaquo;</span>
        <span class="cur-title">{{ article.title }}</span>
      </nav>

      <!-- Article Header & Meta Bar -->
      <header class="article-header-block">
        <span class="category-badge">{{ (article.category || 'SKINCARE BASICS').toUpperCase() }}</span>
        <h1 class="article-main-title">{{ article.title }}</h1>
        <p class="article-subtitle">{{ article.subtitle }}</p>

        <!-- Author & Social Share Row -->
        <div class="article-meta-bar">
          <div class="meta-left">
            <img :src="article.author_avatar || '/images/avatar-sreynich.jpg'" :alt="article.author_name" class="meta-author-avatar" />
            <div class="meta-author-info">
              <span class="author-name">By {{ article.author_name }}</span>
              <span class="author-role">{{ article.author_role }}</span>
            </div>
            <div class="meta-stat-pill">
              <Calendar :size="14" />
              <span>{{ article.published_at }}</span>
            </div>
            <div class="meta-stat-pill">
              <Clock :size="14" />
              <span>{{ article.read_time }}</span>
            </div>
            <div class="meta-stat-pill">
              <Eye :size="14" />
              <span>{{ article.views_count }}</span>
            </div>
          </div>

          <!-- Social Share Buttons -->
          <div class="meta-share-group">
            <span class="share-label">Share:</span>
            <button @click="shareOn('facebook')" class="share-btn" aria-label="Share on Facebook">
              <Facebook :size="15" />
            </button>
            <button @click="shareOn('pinterest')" class="share-btn" aria-label="Share on Pinterest">
              <Share2 :size="15" />
            </button>
            <button @click="copyLink" class="share-btn" aria-label="Copy Article Link">
              <Link2 :size="15" />
            </button>
            <span v-if="copied" class="copied-toast">Link Copied!</span>
          </div>
        </div>
      </header>

      <!-- 3-Column Layout: TOC / Article Body / Related -->
      <div class="article-layout-grid">
        <!-- Left: Sticky TOC + Quiz Card -->
        <aside class="article-left-aside">
          <div class="left-sticky-box">
            <!-- Table of Contents -->
            <div class="toc-card">
              <h3 class="toc-title">In This Article</h3>
              <nav class="toc-links-list">
                <button
                  v-for="item in tocItems"
                  :key="item.id"
                  class="toc-link-btn"
                  :class="{ 'is-active': activeHeadingId === item.id }"
                  @click="scrollToHeading(item.id)"
                >
                  {{ item.title }}
                </button>
              </nav>
            </div>

            <!-- Personalized Quiz Promo Card -->
            <div class="quiz-promo-card">
              <Leaf :size="20" class="leaf-icon" />
              <h4>Personalized for You</h4>
              <p>Take our Skin Quiz to get a customized routine based on your unique skin.</p>
              <router-link to="/quiz" class="btn-take-quiz">
                Take the Skin Quiz &rarr;
              </router-link>
              <div class="quiz-cream-visual">
                <img
                  src="/images/article-quiz-promo.jpg"
                  alt="Personalized Diagnostics"
                  class="cream-swatch-img"
                />
              </div>
            </div>
          </div>
        </aside>

        <!-- Center: Editorial Content Body -->
        <article class="article-main-body">
          <!-- Featured Hero Image with Script -->
          <div class="article-hero-visual-frame">
            <img
              :src="article.hero_image || '/images/article-details-hero.jpg'"
              :alt="article.title"
              class="article-hero-img"
            />
          </div>

          <!-- Article Lead Paragraph -->
          <div class="article-intro-lead">
            <p>
              A good skincare routine doesn't have to be complicated. It's about understanding your skin, choosing the right products, and using them consistently. Whether you're dealing with dryness, oiliness, or sensitivity, the right routine can help you achieve healthier, brighter skin over time.
            </p>
          </div>

          <!-- Section: Why a Skincare Routine Matters -->
          <section id="matters" class="content-section-block">
            <h2 class="content-heading">Why a Skincare Routine Matters</h2>
            <p>
              Your skin faces many challenges every day — pollution, UV rays, stress, and more. A consistent skincare routine helps to:
            </p>

            <div class="checklist-grid">
              <div class="check-item">
                <Check :size="16" class="check-icon" />
                <span>Keep your skin clean and healthy</span>
              </div>
              <div class="check-item">
                <Check :size="16" class="check-icon" />
                <span>Prevent common skin concerns like acne, dryness, and premature aging</span>
              </div>
              <div class="check-item">
                <Check :size="16" class="check-icon" />
                <span>Support your skin barrier against environmental stressors</span>
              </div>
              <div class="check-item">
                <Check :size="16" class="check-icon" />
                <span>Help skincare products work effectively and synergistically</span>
              </div>
            </div>
          </section>

          <!-- Section: Step 1: Know Your Skin Type -->
          <section id="step1" class="content-section-block">
            <h2 class="content-heading">Step 1: Know Your Skin Type</h2>
            <p>
              Before investing in formulations, diagnosing your baseline skin type ensures targeted results:
            </p>
            <div class="skin-types-box-grid">
              <div class="skin-type-card">
                <h5>Dry Skin</h5>
                <p>Feels tight, lacks natural sebum, easily dehydrated. Thrives with ceramide creams and hyaluronic acid toners.</p>
              </div>
              <div class="skin-type-card">
                <h5>Oily Skin</h5>
                <p>Excess sebum sheen, visible pores, prone to congestion. Benefits from BHA exfoliants and gel hydrators.</p>
              </div>
              <div class="skin-type-card">
                <h5>Combination</h5>
                <p>Oily T-zone paired with normal to dry cheeks. Requires balancing niacinamide and adaptable hydration.</p>
              </div>
              <div class="skin-type-card">
                <h5>Sensitive Skin</h5>
                <p>Readily irritated, reactive to strong fragrances. Demands soothing Centella Asiatica and madecassoside.</p>
              </div>
            </div>
          </section>

          <!-- Section: Step 2: Choose the Right Products -->
          <section id="step2" class="content-section-block">
            <h2 class="content-heading">Step 2: Choose the Right Products</h2>
            <p>
              Focus on the core trio: a gentle cleanser that respects skin pH (around 5.5), an emollient moisturizer to prevent trans-epidermal water loss, and a broad-spectrum daily SPF 50 sunscreen.
            </p>
          </section>

          <!-- Section: Step 3: Follow the Right Order -->
          <section id="step3" class="content-section-block">
            <h2 class="content-heading">Step 3: Follow the Right Order</h2>
            <p>
              Rule of thumb: layer formulations from thinnest to thickest texture:
            </p>
            <ol class="ordered-step-list">
              <li><strong>Cleanser:</strong> Double cleanse in evening if wearing makeup or sunscreen.</li>
              <li><strong>Toner / Essence:</strong> Preps and softens stratum corneum.</li>
              <li><strong>Serums / Ampoules:</strong> Concentrated actives (Vitamin C, Niacinamide, Retinol).</li>
              <li><strong>Moisturizer:</strong> Seals in moisture and reinforces the lipid barrier.</li>
              <li><strong>Sunscreen:</strong> Non-negotiable morning shield against photoaging.</li>
            </ol>
          </section>

          <!-- Section: Sample Routines by Skin Type -->
          <section id="routines" class="content-section-block">
            <h2 class="content-heading">Sample Routines by Skin Type</h2>
            <p>
              Consistency is key. Allow 4 to 6 weeks for cellular turnover before expecting dramatic clinical transformation.
            </p>
          </section>

          <!-- Section: Common Mistakes to Avoid -->
          <section id="mistakes" class="content-section-block">
            <h2 class="content-heading">Common Mistakes to Avoid</h2>
            <p>
              Avoid over-exfoliating with physical scrubs or combining strong AHA/BHA acids with pure retinol simultaneously. Introduce one active at a time to prevent barrier inflammation.
            </p>
          </section>

          <!-- Section: Expert Tips -->
          <section id="expert-tips" class="content-section-block">
            <h2 class="content-heading">Expert Tips</h2>
            <blockquote class="atelier-quote">
              &ldquo;Healthy skin is a marathon, not a sprint. Prioritize barrier repair and sun protection above high-percentage acids.&rdquo;
              <footer>— Sophea Meas, Luméa Atelier Director</footer>
            </blockquote>
          </section>

          <!-- Section: Final Thoughts -->
          <section id="final-thoughts" class="content-section-block">
            <h2 class="content-heading">Final Thoughts</h2>
            <p>
              Embrace the ritual of daily skincare as a mindful act of self-care. When you listen to your skin's changing needs throughout the seasons, radiance follows naturally.
            </p>
          </section>
        </article>

        <!-- Right: Related Articles & Insights Newsletter -->
        <aside class="article-right-aside">
          <div class="right-sticky-box">
            <!-- Knowledge Banner -->
            <div class="knowledge-callout-card">
              <Leaf :size="20" class="leaf-icon" />
              <h4>Better Knowledge.<br>Brighter Skin.</h4>
              <p>Discover expert tips, product guides, and skincare advice curated by our dermatological atelier.</p>
            </div>

            <!-- Related Articles Widget -->
            <div class="related-articles-card">
              <div class="related-header">
                <h4>Related Articles</h4>
                <router-link to="/articles" class="view-all-link">View All &rarr;</router-link>
              </div>

              <div class="related-list">
                <router-link
                  v-for="rel in relatedArticles"
                  :key="rel.id"
                  :to="`/articles/${rel.slug}`"
                  class="related-item"
                >
                  <img :src="rel.thumbnail || rel.hero_image" :alt="rel.title" class="rel-thumb" />
                  <div class="rel-info">
                    <span class="rel-category">{{ (rel.category || 'SKINCARE TIPS').toUpperCase() }}</span>
                    <h5 class="rel-title">{{ rel.title }}</h5>
                    <span class="rel-date">{{ rel.published_at }}</span>
                  </div>
                </router-link>
              </div>
            </div>

            <!-- Newsletter Signup Card -->
            <div class="newsletter-sidebar-card">
              <div class="news-icon-circle">
                <Mail :size="18" />
              </div>
              <h4>Get Beauty Insights</h4>
              <p>Sign up for our newsletter and receive the latest skincare tips, expert advice, and exclusive offers.</p>
              <form @submit.prevent="handleSubscribe" class="news-form">
                <input
                  type="email"
                  v-model="newsletterEmail"
                  placeholder="Your email address"
                  class="news-input"
                  required
                />
                <button type="submit" class="btn-news-submit" :disabled="isSubscribed">
                  <span v-if="!isSubscribed">Subscribe</span>
                  <span v-else>Subscribed &check;</span>
                </button>
              </form>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  Calendar,
  Clock,
  Eye,
  Facebook,
  Share2,
  Link2,
  Leaf,
  Check,
  Mail
} from 'lucide-vue-next'

const route = useRoute()

const article = ref({
  title: 'How to Build a Skincare Routine for Your Skin Type',
  subtitle: 'A simple guide to finding the right products, in the right order, for healthier, happier skin.',
  category: 'Skincare Basics',
  read_time: '8 min read',
  views_count: '12.4K views',
  author_name: 'Sophea Meas',
  author_role: 'Skincare Expert',
  author_avatar: '/images/avatar-sreynich.jpg',
  published_at: 'Jun 15, 2025',
  hero_image: '/images/article-details-hero.jpg'
})

const tocItems = ref([
  { id: 'matters', title: 'Why a Skincare Routine Matters' },
  { id: 'step1', title: 'Step 1: Know Your Skin Type' },
  { id: 'step2', title: 'Step 2: Choose the Right Products' },
  { id: 'step3', title: 'Step 3: Follow the Right Order' },
  { id: 'routines', title: 'Sample Routines by Skin Type' },
  { id: 'mistakes', title: 'Common Mistakes to Avoid' },
  { id: 'expert-tips', title: 'Expert Tips' },
  { id: 'final-thoughts', title: 'Final Thoughts' }
])

const relatedArticles = ref([])
const activeHeadingId = ref('matters')
const copied = ref(false)
const newsletterEmail = ref('')
const isSubscribed = ref(false)

function scrollToHeading(id) {
  activeHeadingId.value = id
  const el = document.getElementById(id)
  if (el) {
    const yOffset = -90
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

function copyLink() {
  navigator.clipboard.writeText(window.location.href)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2500)
}

function shareOn(platform) {
  const url = encodeURIComponent(window.location.href)
  const text = encodeURIComponent(article.value.title)
  if (platform === 'facebook') {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank')
  } else if (platform === 'pinterest') {
    window.open(`https://pinterest.com/pin/create/button/?url=${url}&description=${text}`, '_blank')
  }
}

function handleSubscribe() {
  if (newsletterEmail.value) {
    isSubscribed.value = true
    setTimeout(() => {
      newsletterEmail.value = ''
      isSubscribed.value = false
    }, 4000)
  }
}

async function loadArticle() {
  const slug = route.params.slug || 'how-to-build-a-skincare-routine-for-your-skin-type'
  try {
    const res = await fetch(`/api/articles/${slug}`)
    if (res.ok) {
      const data = await res.json()
      article.value = data.data
      if (data.data.toc && data.data.toc.length) {
        tocItems.value = data.data.toc
      }
      relatedArticles.value = data.related || []
    }
  } catch (err) {
    console.warn('[ArticleDetailView] Using fallback:', err)
  }
}

watch(() => route.params.slug, () => {
  loadArticle()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

onMounted(() => {
  loadArticle()
})
</script>

<style scoped>
.lumea-article-detail-page {
  background: #FCFAF7;
  min-height: 100vh;
  padding: 2rem 0 6rem;
  color: #1C1917;
}

.article-page-container {
  max-width: 1360px;
}

/* Breadcrumbs */
.article-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.article-breadcrumb a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s;
}

.article-breadcrumb a:hover {
  color: #7A2E22;
}

.sep {
  color: #A8A29E;
}

.cat-link {
  color: #57534E;
}

.cur-title {
  color: #1C1917;
  font-weight: 500;
}

/* Header Block */
.article-header-block {
  margin-bottom: 3rem;
  max-width: 900px;
}

.category-badge {
  display: inline-block;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #7A2E22;
  margin-bottom: 0.75rem;
}

.article-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.4rem, 4vw, 3.4rem);
  font-weight: 600;
  color: #7A2E22;
  line-height: 1.18;
  margin: 0 0 1rem;
}

.article-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.1rem;
  color: #57534E;
  line-height: 1.6;
  margin: 0 0 2rem;
}

/* Meta Bar */
.article-meta-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(122, 46, 34, 0.1);
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.meta-author-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.meta-author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
}

.author-role {
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  color: #78716C;
}

.meta-stat-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #78716C;
}

.meta-share-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  position: relative;
}

.share-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
  margin-right: 0.2rem;
}

.share-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F5EFEB;
  border: none;
  color: #57534E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.share-btn:hover {
  background: #7A2E22;
  color: #FFFFFF;
}

.copied-toast {
  position: absolute;
  top: -28px;
  right: 0;
  background: #1C1917;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

/* 3-Column Layout */
.article-layout-grid {
  display: grid;
  grid-template-columns: 240px 1fr 310px;
  gap: 3.5rem;
  align-items: start;
}

/* Left Aside: TOC & Quiz Card */
.left-sticky-box {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.toc-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem 1.25rem;
}

.toc-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 1.25rem;
}

.toc-links-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.toc-link-btn {
  background: transparent;
  border: none;
  border-left: 2px solid transparent;
  padding: 0.4rem 0 0.4rem 0.75rem;
  text-align: left;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  cursor: pointer;
  line-height: 1.35;
  transition: all 0.2s;
}

.toc-link-btn:hover {
  color: #7A2E22;
}

.toc-link-btn.is-active {
  border-left-color: #7A2E22;
  color: #7A2E22;
  font-weight: 600;
}

/* Quiz Promo Card */
.quiz-promo-card {
  background: #FAF2EE;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.5rem;
}

.quiz-promo-card .leaf-icon {
  color: #7A2E22;
  margin-bottom: 0.5rem;
}

.quiz-promo-card h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
}

.quiz-promo-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1rem;
}

.btn-take-quiz {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  margin-bottom: 1.25rem;
  transition: background 0.2s;
}

.btn-take-quiz:hover {
  background: #5E2117;
}

.quiz-cream-visual {
  border-radius: 6px;
  overflow: hidden;
}

.cream-swatch-img {
  width: 100%;
  height: 90px;
  object-fit: cover;
  display: block;
}

/* Center Article Body */
.article-hero-visual-frame {
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 2.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
}

.article-hero-img {
  width: 100%;
  height: auto;
  display: block;
}

.article-intro-lead p {
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  line-height: 1.75;
  color: #292524;
  margin: 0 0 2rem;
}

.content-section-block {
  margin-bottom: 3rem;
  scroll-margin-top: 100px;
}

.content-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.85rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 1rem;
}

.content-section-block p {
  font-family: 'Inter', sans-serif;
  font-size: 0.96rem;
  line-height: 1.7;
  color: #44403C;
  margin: 0 0 1.25rem;
}

/* Checklist Grid */
.checklist-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  background: #FAF7F2;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.check-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.check-icon {
  color: #7A2E22;
  margin-top: 0.2rem;
  flex-shrink: 0;
}

.check-item span {
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  color: #292524;
  line-height: 1.45;
}

/* Skin Types Box Grid */
.skin-types-box-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
}

.skin-type-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 6px;
  padding: 1.25rem;
}

.skin-type-card h5 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.35rem;
}

.skin-type-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0;
}

.ordered-step-list {
  padding-left: 1.25rem;
  margin: 1.25rem 0;
}

.ordered-step-list li {
  font-family: 'Inter', sans-serif;
  font-size: 0.94rem;
  line-height: 1.7;
  color: #44403C;
  margin-bottom: 0.65rem;
}

.atelier-quote {
  border-left: 3px solid #7A2E22;
  background: #FAF2EE;
  padding: 1.5rem 1.75rem;
  border-radius: 0 8px 8px 0;
  margin: 1.75rem 0;
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  font-size: 1.15rem;
  line-height: 1.6;
  color: #7A2E22;
}

.atelier-quote footer {
  font-family: 'Inter', sans-serif;
  font-style: normal;
  font-size: 0.82rem;
  font-weight: 600;
  color: #57534E;
  margin-top: 0.75rem;
}

/* Right Aside */
.right-sticky-box {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.knowledge-callout-card {
  background: #FFFBF8;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.5rem;
}

.knowledge-callout-card .leaf-icon {
  color: #7A2E22;
  margin-bottom: 0.5rem;
}

.knowledge-callout-card h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.2rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
  line-height: 1.2;
}

.knowledge-callout-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0;
}

.related-articles-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
}

.related-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.related-header h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.view-all-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.related-item {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  text-decoration: none;
  transition: transform 0.2s;
}

.related-item:hover {
  transform: translateX(3px);
}

.rel-thumb {
  width: 58px;
  height: 58px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.rel-info {
  display: flex;
  flex-direction: column;
}

.rel-category {
  font-family: 'Inter', sans-serif;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #7A2E22;
  margin-bottom: 0.2rem;
}

.rel-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.86rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.35;
  margin: 0 0 0.2rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-item:hover .rel-title {
  color: #7A2E22;
}

.rel-date {
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  color: #78716C;
}

.newsletter-sidebar-card {
  background: #FFFBF8;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.5rem;
}

.news-icon-circle {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #F5E8E5;
  color: #7A2E22;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}

.newsletter-sidebar-card h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.4rem;
}

.newsletter-sidebar-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1rem;
}

.news-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.news-input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #E7E5E4;
  border-radius: 4px;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
}

.news-input:focus {
  border-color: #7A2E22;
}

.btn-news-submit {
  width: 100%;
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.65rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-news-submit:hover:not(:disabled) {
  background: #5E2117;
}

/* Responsive */
@media (max-width: 1200px) {
  .article-layout-grid {
    grid-template-columns: 220px 1fr;
  }
  .article-right-aside {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
}

@media (max-width: 860px) {
  .article-layout-grid {
    grid-template-columns: 1fr;
  }
  .article-left-aside {
    display: none;
  }
  .checklist-grid, .skin-types-box-grid {
    grid-template-columns: 1fr;
  }
}
</style>
