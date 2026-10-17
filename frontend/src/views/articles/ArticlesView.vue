<template>
  <div class="lumea-journal-page">
    <!-- Top Hero Banner matching Format -->
    <header class="journal-hero-banner">
      <div class="container hero-banner-inner">
        <div class="hero-text-col">
          <span class="hero-eyebrow">LUMÉA JOURNAL</span>
          <h1 class="hero-title">Skincare Journal</h1>
          <p class="hero-subtitle">
            Expert advice, skincare guides, and real stories to help you build healthier skin and a more confident you.
          </p>
        </div>

        <div class="hero-visual-col">
          <div class="hero-frame">
            <img
              src="/images/journal-header-books.jpg"
              alt="Knowledge for Healthier Skin"
              class="hero-books-img"
            />
            <div class="hero-script-overlay">
              <span class="script-cursive">Knowledge</span>
              <span class="script-cursive">for Healthier</span>
              <span class="script-cursive">Skin</span>
              <div class="script-underline"></div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="container journal-main-container">
      <!-- Search, Categories & Sorting Bar -->
      <div class="journal-filter-bar">
        <!-- Search Input -->
        <div class="journal-search-wrap">
          <Search :size="16" class="search-icon" />
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search articles..."
            class="journal-search-input"
            @input="handleSearchInput"
          />
          <button
            v-if="searchQuery"
            @click="clearSearch"
            class="clear-search-btn"
            aria-label="Clear Search"
          >
            <X :size="13" />
          </button>
        </div>

        <!-- Category Pills -->
        <div class="category-pills-row">
          <button
            v-for="cat in categories"
            :key="cat"
            class="category-pill-btn"
            :class="{ 'is-active': selectedCategory === cat }"
            @click="selectCategory(cat)"
          >
            {{ cat }}
          </button>
        </div>

        <!-- Sort Dropdown -->
        <div class="journal-sort-wrap">
          <SlidersHorizontal :size="14" class="sort-icon" />
          <select v-model="selectedSort" @change="fetchArticles" class="sort-select">
            <option value="latest">Latest First</option>
            <option value="popular">Most Popular</option>
            <option value="title">Title (A-Z)</option>
          </select>
        </div>
      </div>

      <!-- Main Layout: 3x2 Grid + Sidebar -->
      <div class="journal-layout-grid">
        <!-- Left: Articles Grid & Pagination -->
        <div class="articles-content-col">
          <div v-if="loading" class="journal-loading-state">
            <div class="spinner"></div>
            <p>Loading curated skincare stories...</p>
          </div>

          <div v-else-if="articles.length === 0" class="journal-empty-state">
            <BookOpen :size="48" class="empty-icon" />
            <h3>No articles found</h3>
            <p>Try refining your search keyword or selecting a different category.</p>
            <button @click="resetFilters" class="btn-reset-filters">View All Articles</button>
          </div>

          <div v-else class="articles-cards-grid">
            <article
              v-for="art in articles"
              :key="art.id"
              class="journal-article-card"
            >
              <!-- Thumbnail with Duration Badge -->
              <router-link :to="`/articles/${art.slug}`" class="card-thumb-link">
                <img :src="art.thumbnail || art.hero_image" :alt="art.title" class="card-thumb-img" />
                <span class="read-time-badge">{{ art.read_time }}</span>
              </router-link>

              <!-- Card Body -->
              <div class="card-body-content">
                <span class="card-category-eyebrow">{{ art.category.toUpperCase() }}</span>
                <h3 class="card-title">
                  <router-link :to="`/articles/${art.slug}`">{{ art.title }}</router-link>
                </h3>
                <p class="card-excerpt">{{ art.subtitle || art.excerpt }}</p>

                <!-- Author & CTA Row -->
                <div class="card-author-footer">
                  <div class="author-meta">
                    <img :src="art.author_avatar" :alt="art.author_name" class="author-avatar" />
                    <div class="author-info">
                      <span class="author-name">{{ art.author_name }}</span>
                      <span class="author-date">{{ art.published_at }}</span>
                    </div>
                  </div>
                  <router-link :to="`/articles/${art.slug}`" class="read-more-link">
                    <span>Read More</span>
                    <span class="arrow">&rarr;</span>
                  </router-link>
                </div>
              </div>
            </article>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="journal-pagination-bar">
            <button
              :disabled="currentPage <= 1"
              @click="goToPage(currentPage - 1)"
              class="page-btn page-nav-arrow"
              aria-label="Previous Page"
            >
              &lsaquo;
            </button>
            <button
              v-for="p in totalPages"
              :key="p"
              class="page-btn page-num"
              :class="{ 'is-active': p === currentPage }"
              @click="goToPage(p)"
            >
              {{ p }}
            </button>
            <button
              :disabled="currentPage >= totalPages"
              @click="goToPage(currentPage + 1)"
              class="page-btn page-nav-arrow"
              aria-label="Next Page"
            >
              &rsaquo;
            </button>
          </div>
        </div>

        <!-- Right: Atelier Journal Sidebar -->
        <aside class="journal-sidebar-col">
          <!-- Skin Quiz Promo Banner Card -->
          <div class="sidebar-quiz-card">
            <span class="quiz-eyebrow">TAKE OUR SKIN QUIZ</span>
            <h3 class="quiz-title">Find Your Perfect Routine</h3>
            <p class="quiz-desc">
              Get personalized product recommendations based on your skin type and concerns.
            </p>
            <router-link to="/quiz" class="btn-start-quiz">
              Start Skin Quiz &rarr;
            </router-link>
            <div class="quiz-card-visual">
              <img
                src="/images/journal-quiz-sidebar.jpg"
                alt="Personalized Skincare Diagnostic"
                class="quiz-bottles-img"
              />
            </div>
          </div>

          <!-- Popular Articles Widget (1-4) -->
          <div class="sidebar-popular-card">
            <div class="popular-header-row">
              <h4>Popular Articles</h4>
              <button @click="sortByPopular" class="view-all-link">View All &rarr;</button>
            </div>

            <div class="popular-list">
              <router-link
                v-for="(pop, idx) in popularArticles"
                :key="pop.id"
                :to="`/articles/${pop.slug}`"
                class="popular-item"
              >
                <span class="pop-rank">{{ idx + 1 }}</span>
                <img :src="pop.thumbnail || pop.hero_image" :alt="pop.title" class="pop-thumb" />
                <div class="pop-info">
                  <h5 class="pop-title">{{ pop.title }}</h5>
                  <span class="pop-time">{{ pop.read_time }}</span>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Stay in the Glow Newsletter Card -->
          <div class="sidebar-newsletter-card">
            <div class="newsletter-header">
              <h4 class="news-title">Stay in the Glow</h4>
              <p class="news-desc">
                Subscribe to get the latest skincare tips, new articles, and exclusive offers.
              </p>
            </div>
            <form @submit.prevent="handleSubscribe" class="newsletter-form">
              <div class="news-input-wrap">
                <Mail :size="16" class="news-icon" />
                <input
                  type="email"
                  v-model="newsletterEmail"
                  placeholder="Enter your email address"
                  class="news-input"
                  required
                />
              </div>
              <button type="submit" class="btn-news-submit" :disabled="isSubscribed">
                <span v-if="!isSubscribed">Subscribe</span>
                <span v-else>Subscribed &check;</span>
              </button>
            </form>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, X, SlidersHorizontal, BookOpen, Mail } from 'lucide-vue-next'

const articles = ref([])
const popularArticles = ref([])
const categories = ref([
  'All',
  'Skincare Basics',
  'Ingredients',
  'Skincare Tips',
  'Sun Care',
  'Acne Care',
  'Anti-Aging',
  'Sensitive Skin'
])

const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref('All')
const selectedSort = ref('latest')
const currentPage = ref(1)
const pageSize = ref(6)
const totalArticles = ref(0)
const totalPages = ref(1)

const newsletterEmail = ref('')
const isSubscribed = ref(false)

let searchTimeout = null

function handleSearchInput() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchArticles()
  }, 350)
}

function clearSearch() {
  searchQuery.value = ''
  currentPage.value = 1
  fetchArticles()
}

function selectCategory(cat) {
  selectedCategory.value = cat
  currentPage.value = 1
  fetchArticles()
}

function sortByPopular() {
  selectedSort.value = 'popular'
  selectedCategory.value = 'All'
  currentPage.value = 1
  fetchArticles()
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'All'
  selectedSort.value = 'latest'
  currentPage.value = 1
  fetchArticles()
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchArticles()
    window.scrollTo({ top: 400, behavior: 'smooth' })
  }
}

async function fetchArticles() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (searchQuery.value) params.append('search', searchQuery.value)
    if (selectedCategory.value && selectedCategory.value !== 'All') {
      params.append('category', selectedCategory.value)
    }
    if (selectedSort.value) params.append('sort', selectedSort.value)
    params.append('page', currentPage.value.toString())
    params.append('limit', pageSize.value.toString())

    const res = await fetch(`/api/articles?${params.toString()}`)
    if (res.ok) {
      const data = await res.json()
      articles.value = data.data || []
      totalArticles.value = data.total || 0
      totalPages.value = Math.ceil(totalArticles.value / pageSize.value) || 1
      if (data.categories && data.categories.length) {
        categories.value = data.categories
      }
      if (data.popular && data.popular.length) {
        popularArticles.value = data.popular
      }
    }
  } catch (err) {
    console.error('[ArticlesView] Failed to fetch articles:', err)
  } finally {
    loading.value = false
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

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.lumea-journal-page {
  background: #FCFAF7;
  min-height: 100vh;
  padding-bottom: 6rem;
  color: #1C1917;
}

/* Hero Banner */
.journal-hero-banner {
  background: #F5EFEB;
  border-bottom: 1px solid rgba(122, 46, 34, 0.08);
  padding: 3rem 0;
  margin-bottom: 3rem;
}

.hero-banner-inner {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  align-items: center;
  gap: 3rem;
}

.hero-eyebrow {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #7A2E22;
  margin-bottom: 0.75rem;
}

.hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.4rem, 4.2vw, 3.6rem);
  font-weight: 600;
  color: #7A2E22;
  line-height: 1.15;
  margin: 0 0 1rem;
}

.hero-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  color: #57534E;
  line-height: 1.6;
  max-width: 560px;
  margin: 0;
}

.hero-visual-col {
  display: flex;
  justify-content: flex-end;
}

.hero-frame {
  position: relative;
  max-width: 500px;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 30px -8px rgba(122, 46, 34, 0.15);
}

.hero-books-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.hero-script-overlay {
  position: absolute;
  top: 1.5rem;
  right: 1.75rem;
  text-align: right;
  pointer-events: none;
}

.script-cursive {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: 1.45rem;
  color: #8C4334;
  display: block;
  line-height: 1.15;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.9);
}

.script-underline {
  width: 50px;
  height: 2px;
  background: #8C4334;
  margin-left: auto;
  margin-top: 0.35rem;
}

/* Filter & Search Bar */
.journal-filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 0.85rem 1.25rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.02);
}

.journal-search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  min-width: 220px;
}

.search-icon {
  position: absolute;
  left: 0.85rem;
  color: #78716C;
}

.journal-search-input {
  width: 100%;
  padding: 0.55rem 2rem 0.55rem 2.4rem;
  border: 1px solid #E7E5E4;
  border-radius: 20px;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: #1C1917;
  background: #FAF9F6;
  outline: none;
  transition: all 0.2s;
}

.journal-search-input:focus {
  border-color: #7A2E22;
  background: #FFFFFF;
}

.clear-search-btn {
  position: absolute;
  right: 0.65rem;
  background: transparent;
  border: none;
  color: #78716C;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.category-pills-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 0.2rem 0;
  scrollbar-width: none;
}

.category-pills-row::-webkit-scrollbar {
  display: none;
}

.category-pill-btn {
  background: transparent;
  border: 1px solid #E7E5E4;
  border-radius: 20px;
  padding: 0.4rem 1rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.category-pill-btn:hover {
  border-color: #7A2E22;
  color: #7A2E22;
}

.category-pill-btn.is-active {
  background: #7A2E22;
  border-color: #7A2E22;
  color: #FFFFFF;
  font-weight: 500;
}

.journal-sort-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #E7E5E4;
  border-radius: 6px;
  padding: 0.35rem 0.75rem;
  background: #FAF9F6;
}

.sort-icon {
  color: #78716C;
}

.sort-select {
  border: none;
  background: transparent;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  cursor: pointer;
}

/* Layout Grid */
.journal-layout-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 3rem;
  align-items: start;
}

/* 3x2 Articles Cards Grid */
.articles-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.75rem;
}

.journal-article-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.journal-article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(122, 46, 34, 0.1);
}

.card-thumb-link {
  position: relative;
  display: block;
  overflow: hidden;
  height: 180px;
}

.card-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.journal-article-card:hover .card-thumb-img {
  transform: scale(1.04);
}

.read-time-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: rgba(28, 25, 23, 0.75);
  backdrop-filter: blur(4px);
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
}

.card-body-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-category-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #7A2E22;
  margin-bottom: 0.45rem;
}

.card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.35;
  margin: 0 0 0.6rem;
}

.card-title a {
  color: #1C1917;
  text-decoration: none;
  transition: color 0.2s;
}

.card-title a:hover {
  color: #7A2E22;
}

.card-excerpt {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-author-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.85rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.author-meta {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  color: #1C1917;
}

.author-date {
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  color: #78716C;
}

.read-more-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
  transition: gap 0.2s;
}

.read-more-link:hover {
  gap: 0.55rem;
}

/* Pagination Bar */
.journal-pagination-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 3.5rem;
}

.page-btn {
  min-width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid #E7E5E4;
  background: #FFFFFF;
  color: #57534E;
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #7A2E22;
  color: #7A2E22;
}

.page-btn.is-active {
  background: #7A2E22;
  border-color: #7A2E22;
  color: #FFFFFF;
  font-weight: 600;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Sidebar Columns */
.journal-sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Quiz Card */
.sidebar-quiz-card {
  background: #FAF2EE;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 10px;
  padding: 1.75rem 1.5rem;
  text-align: left;
}

.quiz-eyebrow {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #7A2E22;
  margin-bottom: 0.4rem;
}

.quiz-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.6rem;
  line-height: 1.2;
}

.quiz-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.25rem;
}

.btn-start-quiz {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.7rem 1.25rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s;
  margin-bottom: 1.25rem;
}

.btn-start-quiz:hover {
  background: #5E2117;
}

.quiz-card-visual {
  border-radius: 6px;
  overflow: hidden;
}

.quiz-bottles-img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  display: block;
}

/* Popular Articles */
.sidebar-popular-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  padding: 1.5rem;
}

.popular-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.popular-header-row h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.view-all-link {
  background: transparent;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  color: #7A2E22;
  cursor: pointer;
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  text-decoration: none;
  transition: transform 0.2s;
}

.popular-item:hover {
  transform: translateX(3px);
}

.pop-rank {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #78716C;
  min-width: 16px;
}

.pop-thumb {
  width: 52px;
  height: 52px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.pop-info {
  display: flex;
  flex-direction: column;
}

.pop-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.86rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.35;
  margin: 0 0 0.25rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.popular-item:hover .pop-title {
  color: #7A2E22;
}

.pop-time {
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  color: #78716C;
}

/* Newsletter Card */
.sidebar-newsletter-card {
  background: #FFFBF8;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 10px;
  padding: 1.75rem 1.5rem;
}

.news-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
}

.news-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.25rem;
}

.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.news-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.news-icon {
  position: absolute;
  left: 0.85rem;
  color: #78716C;
}

.news-input {
  width: 100%;
  padding: 0.65rem 0.85rem 0.65rem 2.4rem;
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
  padding: 0.7rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-news-submit:hover:not(:disabled) {
  background: #5E2117;
}

/* States */
.journal-loading-state,
.journal-empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
}

.empty-icon {
  color: #A8A29E;
  margin-bottom: 1rem;
}

.btn-reset-filters {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  border-radius: 4px;
  padding: 0.65rem 1.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  cursor: pointer;
  margin-top: 1rem;
}

/* Responsive */
@media (max-width: 1100px) {
  .journal-layout-grid {
    grid-template-columns: 1fr;
  }
  .articles-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .journal-sidebar-col {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-banner-inner {
    grid-template-columns: 1fr;
  }
  .hero-visual-col {
    justify-content: center;
  }
  .journal-filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .articles-cards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
