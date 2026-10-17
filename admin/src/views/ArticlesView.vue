<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
import {
  Search,
  Plus,
  RotateCcw,
  Filter as FilterIcon,
  Edit2,
  Eye,
  Trash2,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Download,
  Calendar,
  BookOpen,
  FileText,
  ThumbsUp,
  MessageSquare,
  CheckCircle2,
  Upload,
  Sparkles,
  Save,
  ArrowLeft,
  ArrowUpRight,
  Send,
  Link as LinkIcon,
  Image as ImageIcon,
  Quote,
  X
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View Mode: 'list' | 'editor'
const currentView = ref('list')
const editorMode = ref('create') // 'create' | 'edit'

// Filtering & Search
const searchQuery = ref('')
const selectedCategory = ref('All Categories')
const selectedAuthor = ref('All Authors')
const selectedStatus = ref('All Statuses')
const activeTab = ref('all') // 'all', 'published', 'drafts', 'scheduled', 'archived'

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(8)

// Selection
const selectedArticleIds = ref([])
const selectAll = ref(false)

// Active Editor Tab
const activeEditorTab = ref('content')

// Article Editor State
const articleForm = reactive({
  id: null,
  title: '10 Skincare Tips for Glowing Skin',
  slug: '10-skincare-tips-for-glowing-skin',
  excerpt: 'Simple daily habits to achieve healthier, brighter skin. Learn expert-backed skincare tips that really work.',
  content: `Glowing skin isn't just about using the right products — it's about building healthy habits. In this article, we'll share 10 simple yet effective skincare tips that can help you achieve brighter, healthier skin, no matter your skin type.

### 1. Cleanse Gently
Cleansing removes dirt, oil, and impurities from your skin. Choose a gentle cleanser that suits your skin type and avoid over-washing, which can strip your skin's natural moisture barrier.

### 2. Hydrate Inside and Out
Hydration is key to radiant skin. Drink plenty of water throughout the day and incorporate hyaluronic acid and ceramides into your daily routine to lock in essential moisture.`,
  featured_image: '/images/article-thumb-sleep.jpg',
  category: 'Skincare Tips',
  tags: ['skincare', 'glowing skin', 'skin care routine'],
  author: 'Sophea Chhun',
  author_avatar: '/images/avatar-sreynich.jpg',
  status: 'Published',
  publish_date: '2025-08-28 10:24',
  is_scheduled: false
})

const tagInput = ref('')
const articleFileInput = ref(null)
const isUploadingImage = ref(false)

function triggerArticleImageUpload() {
  if (articleFileInput.value) {
    articleFileInput.value.click()
  }
}

async function handleArticleImageUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  isUploadingImage.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.data?.status === 'success' && res.data.url) {
      articleForm.featured_image = res.data.url
      adminStore.addToast('Featured image uploaded successfully!', 'success')
    }
  } catch (err) {
    adminStore.addToast('Failed to upload image. Please ensure valid JPG/PNG/WebP.', 'error')
  } finally {
    isUploadingImage.value = false
    if (e.target) e.target.value = ''
  }
}

// 4 Top KPI Cards
const articleKpis = [
  {
    label: 'Total Articles',
    val: '24',
    trend: '+33%',
    trendUp: true,
    icon: BookOpen,
    color: 'pill-peach'
  },
  {
    label: 'Total Views',
    val: '12,480',
    trend: '+18%',
    trendUp: true,
    icon: Eye,
    color: 'pill-rose'
  },
  {
    label: 'Total Likes',
    val: '892',
    trend: '+27%',
    trendUp: true,
    icon: ThumbsUp,
    color: 'pill-crimson'
  },
  {
    label: 'Total Comments',
    val: '126',
    trend: '+15%',
    trendUp: true,
    icon: MessageSquare,
    color: 'pill-amber'
  }
]

// Mock & Seed Articles Data matching Skincare Articles Management Dashboard.png
const articlesList = ref([
  {
    id: 1,
    title: '10 Skincare Tips for Glowing Skin',
    subtitle: 'Simple daily habits for healthier, brighter skin.',
    slug: '10-skincare-tips-for-glowing-skin',
    category: 'Skincare Tips',
    category_badge: 'badge-tips',
    author: 'Sophea Chhun',
    author_avatar: '/images/avatar-sreynich.jpg',
    views: '2,845',
    likes: 210,
    comments: 28,
    status: 'Published',
    date: 'Aug 28, 2025',
    time: '10:24 AM',
    thumb: '/images/article-thumb-sleep.jpg'
  },
  {
    id: 2,
    title: 'The Right Sunscreen for Your Skin Type',
    subtitle: 'Find the perfect SPF for your unique needs.',
    slug: 'the-right-sunscreen-for-your-skin-type',
    category: 'Sun Care',
    category_badge: 'badge-sun',
    author: 'Dara Kim',
    author_avatar: '/images/avatar-super-admin.jpg',
    views: '1,982',
    likes: 145,
    comments: 17,
    status: 'Published',
    date: 'Aug 25, 2025',
    time: '02:15 PM',
    thumb: '/images/article-thumb-centella.jpg'
  },
  {
    id: 3,
    title: 'How to Build a Skincare Routine',
    subtitle: 'A step-by-step guide for beginners.',
    slug: 'how-to-build-a-skincare-routine-for-your-skin-type',
    category: 'Skincare Routine',
    category_badge: 'badge-routine',
    author: 'Sophea Chhun',
    author_avatar: '/images/avatar-sreynich.jpg',
    views: '3,421',
    likes: 302,
    comments: 36,
    status: 'Published',
    date: 'Aug 20, 2025',
    time: '09:30 AM',
    thumb: '/images/article-thumb-sleep.jpg'
  },
  {
    id: 4,
    title: 'Top 5 Ingredients for Healthy Skin',
    subtitle: 'Science-backed ingredients that work.',
    slug: 'top-5-ingredients-for-healthy-skin',
    category: 'Ingredients',
    category_badge: 'badge-ingredients',
    author: 'Mony Roth',
    author_avatar: '/images/avatar-sreynich.jpg',
    views: '1,567',
    likes: 98,
    comments: 12,
    status: 'Draft',
    date: 'Aug 18, 2025',
    time: '—',
    thumb: '/images/article-thumb-centella.jpg'
  },
  {
    id: 5,
    title: 'How to Treat Acne Naturally',
    subtitle: 'Gentle and effective solutions for clearer skin.',
    slug: 'how-to-treat-acne-naturally',
    category: 'Acne Care',
    category_badge: 'badge-acne',
    author: 'Dara Kim',
    author_avatar: '/images/avatar-super-admin.jpg',
    views: '2,104',
    likes: 176,
    comments: 24,
    status: 'Published',
    date: 'Aug 15, 2025',
    time: '11:20 AM',
    thumb: '/images/article-thumb-sleep.jpg'
  },
  {
    id: 6,
    title: 'Morning vs. Night Skincare Routine',
    subtitle: "What's the difference and why it matters.",
    slug: 'morning-vs-night-skincare-routine',
    category: 'Skincare Routine',
    category_badge: 'badge-routine',
    author: 'Mony Roth',
    author_avatar: '/images/avatar-sreynich.jpg',
    views: '1,298',
    likes: 88,
    comments: 9,
    status: 'Scheduled',
    date: 'Sep 1, 2025',
    time: '08:00 AM',
    thumb: '/images/article-thumb-centella.jpg'
  },
  {
    id: 7,
    title: 'Natural Ingredients That Actually Work',
    subtitle: 'Discover the power of nature in skincare.',
    slug: 'natural-ingredients-that-actually-work',
    category: 'Natural Care',
    category_badge: 'badge-natural',
    author: 'Sophea Chhun',
    author_avatar: '/images/avatar-sreynich.jpg',
    views: '976',
    likes: 64,
    comments: 8,
    status: 'Published',
    date: 'Aug 10, 2025',
    time: '04:10 PM',
    thumb: '/images/article-thumb-sleep.jpg'
  },
  {
    id: 8,
    title: 'How to Choose Products for Sensitive Skin',
    subtitle: 'Expert advice for calm, healthy skin.',
    slug: 'how-to-choose-products-for-sensitive-skin',
    category: 'Sensitive Skin',
    category_badge: 'badge-sensitive',
    author: 'Dara Kim',
    author_avatar: '/images/avatar-super-admin.jpg',
    views: '1,732',
    likes: 120,
    comments: 12,
    status: 'Archived',
    date: 'Aug 5, 2025',
    time: '01:45 PM',
    thumb: '/images/article-thumb-centella.jpg'
  }
])

onMounted(async () => {
  try {
    const res = await apiClient.get('/articles?limit=100')
    if (res.data?.success && res.data.data?.length > 0) {
      // Merge with real database articles
      const dbArts = res.data.data
      dbArts.forEach((da, idx) => {
        if (!articlesList.value.some(a => a.slug === da.slug)) {
          articlesList.value.push({
            id: da.id || 10 + idx,
            title: da.title,
            subtitle: da.subtitle || da.excerpt?.slice(0, 50),
            slug: da.slug,
            category: da.category || 'Skincare Science',
            category_badge: 'badge-tips',
            author: da.author_name || 'Dr. Celine Laurent',
            author_avatar: da.author_avatar || '/images/avatar-sreynich.jpg',
            views: da.views_count || '1,200',
            likes: 85,
            comments: 10,
            status: 'Published',
            date: da.published_at || 'Aug 28, 2025',
            time: '10:00 AM',
            thumb: da.thumbnail || '/images/article-thumb-sleep.jpg'
          })
        }
      })
    }
  } catch (err) {
    console.warn('Using initial articles list:', err)
  }
})

// Filtered Articles
const filteredArticles = computed(() => {
  let list = [...articlesList.value]

  if (activeTab.value === 'published') {
    list = list.filter(a => a.status === 'Published')
  } else if (activeTab.value === 'drafts') {
    list = list.filter(a => a.status === 'Draft')
  } else if (activeTab.value === 'scheduled') {
    list = list.filter(a => a.status === 'Scheduled')
  } else if (activeTab.value === 'archived') {
    list = list.filter(a => a.status === 'Archived')
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(a =>
      a.title.toLowerCase().includes(q) ||
      a.subtitle?.toLowerCase().includes(q) ||
      a.author.toLowerCase().includes(q)
    )
  }

  if (selectedCategory.value !== 'All Categories') {
    list = list.filter(a => a.category === selectedCategory.value)
  }

  return list
})

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredArticles.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredArticles.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'All Categories'
  selectedAuthor.value = 'All Authors'
  selectedStatus.value = 'All Statuses'
  activeTab.value = 'all'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedArticleIds.value = paginatedArticles.value.map(a => a.id)
  } else {
    selectedArticleIds.value = []
  }
}

// Editor Navigation
const openCreateArticle = () => {
  editorMode.value = 'create'
  articleForm.id = null
  articleForm.title = ''
  articleForm.slug = ''
  articleForm.excerpt = ''
  articleForm.content = ''
  articleForm.category = 'Skincare Tips'
  articleForm.tags = ['skincare', 'botanical']
  articleForm.status = 'Draft'
  currentView.value = 'editor'
}

const openEditArticle = (art) => {
  editorMode.value = 'edit'
  articleForm.id = art.id
  articleForm.title = art.title
  articleForm.slug = art.slug
  articleForm.excerpt = art.subtitle || ''
  articleForm.category = art.category
  articleForm.author = art.author
  articleForm.status = art.status
  articleForm.featured_image = art.thumb
  currentView.value = 'editor'
}

const addTag = () => {
  if (tagInput.value.trim() && !articleForm.tags.includes(tagInput.value.trim())) {
    articleForm.tags.push(tagInput.value.trim())
    tagInput.value = ''
  }
}

const removeTag = (index) => {
  articleForm.tags.splice(index, 1)
}

const saveDraft = () => {
  articleForm.status = 'Draft'
  adminStore.addToast(`Article "${articleForm.title}" saved as draft`, 'success')
  currentView.value = 'list'
}

const publishArticle = () => {
  if (!articleForm.title) {
    alert('Please enter an article title.')
    return
  }

  if (editorMode.value === 'create') {
    articlesList.value.unshift({
      id: Date.now(),
      title: articleForm.title,
      subtitle: articleForm.excerpt,
      slug: articleForm.slug || articleForm.title.toLowerCase().replace(/\s+/g, '-'),
      category: articleForm.category,
      category_badge: 'badge-tips',
      author: articleForm.author,
      author_avatar: '/images/avatar-sreynich.jpg',
      views: '1',
      likes: 0,
      comments: 0,
      status: 'Published',
      date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      time: 'Just now',
      thumb: articleForm.featured_image
    })
    adminStore.addToast('Article published to Skincare Journal!', 'success')
  } else {
    const item = articlesList.value.find(a => a.id === articleForm.id)
    if (item) {
      item.title = articleForm.title
      item.subtitle = articleForm.excerpt
      item.category = articleForm.category
      item.status = 'Published'
    }
    adminStore.addToast('Article updated and published!', 'success')
  }
  currentView.value = 'list'
}
</script>

<template>
  <div class="articles-management-page">
    <!-- ========================================== -->
    <!-- VIEW 1: ARTICLES DIRECTORY                -->
    <!-- Matching Skincare Articles Management Dashboard.png -->
    <!-- ========================================== -->
    <template v-if="currentView === 'list'">
      <!-- Hero Banner -->
      <div class="articles-hero-card">
        <div class="hero-left">
          <div class="editor-breadcrumb">
            <span>Content</span>
            <span class="crumb-sep">></span>
            <span class="crumb-current">Articles</span>
          </div>
          <h1 class="hero-heading">Articles Management</h1>
          <p class="hero-subtext">Create and manage skincare articles, tips, and expert advice to engage your audience.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Botanical Articles"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">Knowledge</span>
              <span class="motto-line highlight">today. Healthier</span>
              <span class="motto-line highlight">skin tomorrow.</span>
            </div>
          </div>

          <button class="btn-create-article" @click="openCreateArticle">
            <Plus :size="16" />
            <span>Create Article</span>
          </button>
        </div>
      </div>

      <!-- 4 KPI Cards -->
      <div class="kpi-grid-4">
        <div
          v-for="kpi in articleKpis"
          :key="kpi.label"
          class="card kpi-card"
        >
          <div class="kpi-icon-pill" :class="kpi.color">
            <component :is="kpi.icon" :size="18" />
          </div>
          <div class="kpi-meta">
            <span class="kpi-label">{{ kpi.label }}</span>
            <strong class="kpi-val">{{ kpi.val }}</strong>
            <div class="kpi-trend-row">
              <span class="trend-indicator text-green">
                <ArrowUpRight :size="13" />
                {{ kpi.trend }}
              </span>
              <span class="trend-sub">vs last month</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Toolbar -->
      <div class="filter-toolbar card">
        <div class="search-input-wrap">
          <Search :size="16" class="search-icon" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search articles, topics, or keywords..."
            class="atelier-input-clean"
          />
        </div>

        <div class="filter-dropdowns">
          <div class="select-wrap">
            <select v-model="selectedCategory" class="atelier-select">
              <option value="All Categories">All Categories</option>
              <option value="Skincare Tips">Skincare Tips</option>
              <option value="Sun Care">Sun Care</option>
              <option value="Skincare Routine">Skincare Routine</option>
              <option value="Ingredients">Ingredients</option>
              <option value="Acne Care">Acne Care</option>
              <option value="Natural Care">Natural Care</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <div class="select-wrap">
            <select v-model="selectedAuthor" class="atelier-select">
              <option value="All Authors">All Authors</option>
              <option value="Sophea Chhun">Sophea Chhun</option>
              <option value="Dara Kim">Dara Kim</option>
              <option value="Mony Roth">Mony Roth</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <button class="btn-reset-filter" @click="resetFilters">
            <RotateCcw :size="14" />
            <span>Reset</span>
          </button>

          <button class="btn-apply-filter">
            <FilterIcon :size="14" />
            <span>Filter</span>
          </button>
        </div>
      </div>

      <!-- Tabs and Export Row -->
      <div class="tabs-and-actions-row">
        <div class="status-tabs-row">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
          >
            All Articles (24)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'published' }"
            @click="activeTab = 'published'"
          >
            Published (18)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'drafts' }"
            @click="activeTab = 'drafts'"
          >
            Drafts (4)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'scheduled' }"
            @click="activeTab = 'scheduled'"
          >
            Scheduled (1)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'archived' }"
            @click="activeTab = 'archived'"
          >
            Archived (1)
          </button>
        </div>

        <button class="btn-export-outline" @click="alert('Exporting articles library...')">
          <Download :size="14" />
          <span>Export</span>
        </button>
      </div>

      <!-- Articles Table Card -->
      <div class="card table-card">
        <table class="atelier-table">
          <thead>
            <tr>
              <th class="col-checkbox">
                <input
                  type="checkbox"
                  v-model="selectAll"
                  @change="toggleSelectAll"
                />
              </th>
              <th class="col-order">#</th>
              <th>Article</th>
              <th>Category</th>
              <th>Author</th>
              <th class="text-center">Views</th>
              <th class="text-center">Likes</th>
              <th class="text-center">Comments</th>
              <th class="text-center">Status</th>
              <th>Published Date</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(art, index) in paginatedArticles"
              :key="art.id"
              class="table-row-hover"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :value="art.id"
                  v-model="selectedArticleIds"
                />
              </td>
              <td class="col-order text-muted font-medium">
                {{ index + 1 }}
              </td>
              <td>
                <div class="article-cell" @click="openEditArticle(art)">
                  <img
                    :src="art.thumb"
                    alt="Article Cover"
                    class="article-table-thumb"
                    @error="$event.target.src = '/images/article-thumb-sleep.jpg'"
                  />
                  <div class="article-names-wrap">
                    <strong class="article-title-txt">{{ art.title }}</strong>
                    <span class="article-sub-txt">{{ art.subtitle }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="cat-badge-pill" :class="art.category_badge">
                  {{ art.category }}
                </span>
              </td>
              <td>
                <div class="author-cell">
                  <img :src="art.author_avatar" class="author-avatar" />
                  <span class="author-name-txt">{{ art.author }}</span>
                </div>
              </td>
              <td class="text-center font-medium">{{ art.views }}</td>
              <td class="text-center text-muted">{{ art.likes }}</td>
              <td class="text-center text-muted">{{ art.comments }}</td>
              <td class="text-center">
                <span
                  class="status-pill"
                  :class="{
                    'badge-active': art.status === 'Published',
                    'badge-inactive': art.status === 'Draft',
                    'badge-scheduled': art.status === 'Scheduled',
                    'badge-archived': art.status === 'Archived'
                  }"
                >
                  {{ art.status }}
                </span>
              </td>
              <td>
                <div class="date-cell">
                  <span class="date-txt">{{ art.date }}</span>
                  <span class="time-txt">{{ art.time }}</span>
                </div>
              </td>
              <td class="text-right">
                <div class="action-buttons-cell">
                  <button
                    class="action-icon-btn"
                    title="Edit Article"
                    @click="openEditArticle(art)"
                  >
                    <Edit2 :size="14" />
                  </button>
                  <button
                    class="action-icon-btn"
                    title="View Online"
                    @click="alert(`Opening /articles/${art.slug}`)"
                  >
                    <Eye :size="14" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedArticles.length === 0">
              <td colspan="11" class="empty-table-cell">
                <p>No articles found matching your filter criteria.</p>
                <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Footer -->
        <div class="pagination-footer">
          <span class="pagination-summary">
            Showing 1 to {{ paginatedArticles.length }} of {{ filteredArticles.length }} articles
          </span>

          <div class="pagination-controls">
            <button class="page-nav-btn" disabled>
              <ChevronLeft :size="15" />
            </button>
            <button class="page-num-btn active">1</button>
            <button class="page-num-btn">2</button>
            <button class="page-num-btn">3</button>
            <button class="page-nav-btn">
              <ChevronRight :size="15" />
            </button>
          </div>

          <div class="items-per-page-select">
            <select class="page-size-select">
              <option>10 / page</option>
              <option>20 / page</option>
            </select>
          </div>
        </div>
      </div>
    </template>

    <!-- ========================================== -->
    <!-- VIEW 2: ARTICLE EDITOR                     -->
    <!-- Matching Luméa Skincare Article Editor Dashboard.png -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'editor'">
      <!-- Editor Hero Banner -->
      <div class="articles-hero-card">
        <div class="hero-left">
          <div class="editor-breadcrumb">
            <button class="btn-back-link" @click="currentView = 'list'">
              <ArrowLeft :size="13" /> Articles
            </button>
            <span class="crumb-sep">/</span>
            <span class="crumb-current">{{ editorMode === 'create' ? 'Add Article' : 'Edit Article' }}</span>
          </div>
          <h1 class="hero-heading">
            {{ editorMode === 'create' ? 'Add New Article' : `Edit: ${articleForm.title}` }}
          </h1>
          <p class="hero-subtext">Share expert knowledge, tips, and stories to inspire healthier skin.</p>
        </div>

        <div class="hero-right">
          <div class="editor-top-actions">
            <button class="btn-save-draft" @click="saveDraft">
              <FileText :size="14" />
              <span>Save Draft</span>
            </button>
            <button class="btn-preview-art" @click="alert('Previewing reader view...')">
              <Eye :size="14" />
              <span>Preview</span>
            </button>
            <button class="btn-publish-art" @click="publishArticle">
              <Send :size="14" />
              <span>Publish</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs inside Editor -->
      <div class="editor-nav-tabs">
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'content' }"
          @click="activeEditorTab = 'content'"
        >
          Content
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'seo' }"
          @click="activeEditorTab = 'seo'"
        >
          SEO
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'social' }"
          @click="activeEditorTab = 'social'"
        >
          Social Sharing
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'settings' }"
          @click="activeEditorTab = 'settings'"
        >
          Settings
        </button>
      </div>

      <!-- 2-Column Editor Grid matching mockup -->
      <div class="article-editor-grid">
        <!-- Left Column: Writing Arena -->
        <div class="editor-arena-col">
          <div class="card editor-content-card">
            <!-- Title -->
            <div class="form-group-clean">
              <div class="label-with-counter">
                <label class="form-lbl">Title <span class="req">*</span></label>
                <span class="char-counter">{{ (articleForm.title || '').length }}/100</span>
              </div>
              <input
                v-model="articleForm.title"
                type="text"
                placeholder="e.g. 10 Skincare Tips for Glowing Skin"
                class="atelier-input-lg"
                required
              />
            </div>

            <!-- Slug -->
            <div class="form-group-clean">
              <div class="label-with-counter">
                <label class="form-lbl">Slug <span class="req">*</span></label>
                <span class="char-counter">{{ (articleForm.slug || '').length }}/100</span>
              </div>
              <input
                v-model="articleForm.slug"
                type="text"
                placeholder="10-skincare-tips-for-glowing-skin"
                class="atelier-input"
              />
            </div>

            <!-- Excerpt -->
            <div class="form-group-clean">
              <div class="label-with-counter">
                <label class="form-lbl">Excerpt</label>
                <span class="char-counter">{{ (articleForm.excerpt || '').length }}/200</span>
              </div>
              <textarea
                v-model="articleForm.excerpt"
                maxlength="200"
                rows="2"
                placeholder="Simple daily habits to achieve healthier, brighter skin. Learn expert-backed skincare tips that really work."
                class="atelier-textarea"
              ></textarea>
            </div>

            <!-- Rich Text Editor -->
            <div class="form-group-clean">
              <label class="form-lbl">Content <span class="req">*</span></label>

              <!-- Editorial Toolbar matching mockup -->
              <div class="editor-rte-toolbar">
                <select class="rte-select">
                  <option>Paragraph</option>
                  <option>Heading 1</option>
                  <option>Heading 2</option>
                  <option>Heading 3</option>
                </select>
                <div class="rte-divider"></div>
                <button type="button" class="rte-btn"><b>B</b></button>
                <button type="button" class="rte-btn"><i>I</i></button>
                <button type="button" class="rte-btn"><u>U</u></button>
                <div class="rte-divider"></div>
                <button type="button" class="rte-btn">• List</button>
                <button type="button" class="rte-btn">1. List</button>
                <div class="rte-divider"></div>
                <button type="button" class="rte-btn" title="Insert Link"><LinkIcon :size="13" /></button>
                <button type="button" class="rte-btn" title="Insert Image"><ImageIcon :size="13" /></button>
                <button type="button" class="rte-btn" title="Blockquote"><Quote :size="12" /> Quote</button>
              </div>

              <!-- In-Article Graphic Banner matching mockup -->
              <div class="in-article-banner-frame">
                <div class="article-graphic-banner">
                  <img src="/images/ai-banner-atelier.jpg" class="banner-photo" />
                  <div class="banner-callout-text">
                    <h2>Healthy Skin<br/>Happier You</h2>
                    <span>SIMPLE TIPS. REAL RESULTS.</span>
                  </div>
                </div>
              </div>

              <!-- Main Body Textarea -->
              <textarea
                v-model="articleForm.content"
                rows="12"
                class="atelier-textarea-body"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Right Column: Metadata & Settings -->
        <div class="editor-sidebar-col">
          <!-- 1. Featured Image -->
          <div class="card editor-side-card">
            <h4 class="side-card-title">Featured Image</h4>
            <div class="featured-img-preview-box">
              <img :src="articleForm.featured_image" class="featured-img" />
            </div>
            <div class="featured-img-actions">
              <input
                type="file"
                ref="articleFileInput"
                @change="handleArticleImageUpload"
                accept="image/*"
                style="display: none"
              />
              <button class="btn-img-action" @click="triggerArticleImageUpload" :disabled="isUploadingImage">
                <Upload :size="13" />
                <span>{{ isUploadingImage ? 'Uploading...' : 'Change Image' }}</span>
              </button>
              <button class="btn-img-action text-danger" @click="articleForm.featured_image = '/images/article-thumb-sleep.jpg'">
                <Trash2 :size="13" />
                <span>Remove</span>
              </button>
            </div>
            <span class="field-hint">Recommended size: 1200 × 630 px (JPG, PNG)</span>
          </div>

          <!-- 2. Category -->
          <div class="card editor-side-card">
            <h4 class="side-card-title">Category <span class="req">*</span></h4>
            <select v-model="articleForm.category" class="atelier-input">
              <option value="Skincare Tips">Skincare Tips</option>
              <option value="Sun Care">Sun Care</option>
              <option value="Skincare Routine">Skincare Routine</option>
              <option value="Ingredients">Ingredients</option>
              <option value="Acne Care">Acne Care</option>
              <option value="Natural Care">Natural Care</option>
            </select>
            <span class="link-add-cat">+ Add New Category</span>
          </div>

          <!-- 3. Tags -->
          <div class="card editor-side-card">
            <h4 class="side-card-title">Tags</h4>
            <div class="tags-container">
              <span
                v-for="(tag, idx) in articleForm.tags"
                :key="tag"
                class="tag-badge-pill"
              >
                {{ tag }}
                <button type="button" class="btn-tag-x" @click="removeTag(idx)">×</button>
              </span>
            </div>
            <input
              v-model="tagInput"
              type="text"
              placeholder="Add a tag and press Enter..."
              class="atelier-input"
              @keydown.enter.prevent="addTag"
            />
          </div>

          <!-- 4. Author -->
          <div class="card editor-side-card">
            <h4 class="side-card-title">Author</h4>
            <select v-model="articleForm.author" class="atelier-input">
              <option value="Sophea Chhun">Sophea Chhun</option>
              <option value="Dara Kim">Dara Kim</option>
              <option value="Mony Roth">Mony Roth</option>
              <option value="Dr. Celine Laurent">Dr. Celine Laurent</option>
            </select>
          </div>

          <!-- 5. Status & Publish Date -->
          <div class="card editor-side-card">
            <h4 class="side-card-title">Status</h4>
            <select v-model="articleForm.status" class="atelier-input">
              <option value="Draft">Draft</option>
              <option value="Published">Published</option>
              <option value="Scheduled">Scheduled</option>
            </select>

            <div class="publish-date-group">
              <label class="form-lbl">Publish Date</label>
              <input
                v-model="articleForm.publish_date"
                type="text"
                class="atelier-input"
              />
              <label class="checkbox-schedule">
                <input type="checkbox" v-model="articleForm.is_scheduled" />
                <span>Schedule for later</span>
              </label>
            </div>
          </div>

          <!-- 6. Tips Card -->
          <div class="card tips-card">
            <div class="tips-top">
              <Sparkles :size="15" class="tip-ico" />
              <strong>Editorial Tips</strong>
            </div>
            <ul class="tips-list">
              <li>Use a clear and engaging title.</li>
              <li>Add a relevant featured image.</li>
              <li>Include categories and tags for better discoverability.</li>
              <li>Optimize for SEO to reach more readers.</li>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.articles-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.articles-hero-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FFFFFF 0%, #FAF5F2 100%);
  border: 1px solid #EFE7E0;
  border-radius: 16px;
  padding: 24px 32px;
  box-shadow: 0 4px 18px rgba(132, 38, 27, 0.04);
}

.hero-left {
  max-width: 480px;
}

.editor-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #84261B;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}

.crumb-sep { color: #8C847E; }
.crumb-current { color: #5C544E; }

.btn-back-link {
  background: none;
  border: none;
  color: #84261B;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.hero-heading {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 32px;
  line-height: 1.15;
  color: #84261B;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.hero-subtext {
  font-size: 13.5px;
  color: #7A726C;
  line-height: 1.45;
}

.hero-right {
  display: flex;
  align-items: center;
  gap: 32px;
}

.hero-visual-callout {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-bottles {
  height: 90px;
  width: auto;
  object-fit: contain;
}

.hero-motto {
  display: flex;
  flex-direction: column;
}

.motto-line {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 16px;
  line-height: 1.25;
  color: #84261B;
  font-style: italic;
  font-weight: 600;
}

.btn-create-article {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #84261B;
  color: #FFFFFF;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13.5px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(132, 38, 27, 0.2);
}

.btn-create-article:hover {
  background: #6D1E15;
}

/* 4 KPI Cards */
.kpi-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 20px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
}

.kpi-icon-pill {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pill-peach { background: #FAF0E8; color: #C4623C; }
.pill-crimson { background: #F8E9E4; color: #84261B; }
.pill-amber { background: #FEF7ED; color: #B25E00; }
.pill-rose { background: #FDF0EE; color: #D97768; }

.kpi-meta {
  display: flex;
  flex-direction: column;
}

.kpi-label {
  font-size: 12px;
  color: #7A726C;
  font-weight: 500;
}

.kpi-val {
  font-size: 22px;
  font-weight: 700;
  color: #2D2621;
}

.kpi-trend-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
}

.trend-indicator {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-weight: 600;
}

.text-green { color: #2E7D32; }
.trend-sub { color: #8C847E; }

/* Filter Toolbar */
.filter-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 20px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 8px 14px;
  flex: 1;
  max-width: 380px;
}

.search-icon {
  color: #8C847E;
}

.atelier-input-clean {
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  width: 100%;
  color: #2D2621;
}

.filter-dropdowns {
  display: flex;
  align-items: center;
  gap: 10px;
}

.select-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.atelier-select {
  appearance: none;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 8px 30px 8px 12px;
  font-size: 12.5px;
  color: #3C3530;
  cursor: pointer;
}

.select-arrow {
  position: absolute;
  right: 10px;
  color: #8C847E;
  pointer-events: none;
}

.btn-reset-filter {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-apply-filter {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
}

/* Tabs & Export */
.tabs-and-actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #EFE7E0;
  padding-bottom: 6px;
}

.status-tabs-row {
  display: flex;
  gap: 20px;
}

.tab-btn {
  background: none;
  border: none;
  font-size: 13.5px;
  font-weight: 500;
  color: #7A726C;
  padding: 8px 4px;
  cursor: pointer;
  position: relative;
}

.tab-btn.active {
  color: #84261B;
  font-weight: 700;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -7px;
  left: 0;
  right: 0;
  height: 2px;
  background: #84261B;
}

.btn-export-outline {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #3C3530;
  cursor: pointer;
}

/* Table Card */
.table-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  overflow: hidden;
}

.atelier-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.atelier-table th {
  background: #FAF7F4;
  padding: 12px 14px;
  font-size: 11.5px;
  font-weight: 600;
  color: #8C847E;
  border-bottom: 1px solid #EFE7E0;
  text-align: left;
}

.atelier-table td {
  padding: 14px;
  border-bottom: 1px solid #F5ECE6;
  color: #3C3530;
  vertical-align: middle;
}

.table-row-hover:hover {
  background: #FCF9F7;
}

.col-checkbox {
  width: 40px;
  text-align: center;
}

.col-order {
  width: 40px;
  text-align: center;
}

.article-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.article-table-thumb {
  width: 48px;
  height: 38px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.article-names-wrap {
  display: flex;
  flex-direction: column;
  max-width: 320px;
}

.article-title-txt {
  font-size: 13px;
  color: #2D2621;
  line-height: 1.3;
}

.article-sub-txt {
  font-size: 11px;
  color: #8C847E;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cat-badge-pill {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.badge-tips { background: #FDF0EE; color: #D97768; }
.badge-sun { background: #FEF7ED; color: #B25E00; }
.badge-routine { background: #F3E8FF; color: #6B21A8; }
.badge-ingredients { background: #E8F5E9; color: #2E7D32; }
.badge-acne { background: #FAF0E8; color: #C4623C; }
.badge-natural { background: #E8F5E9; color: #2E7D32; }
.badge-sensitive { background: #FDF0EE; color: #D97768; }

.author-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name-txt {
  font-size: 12px;
  color: #3C3530;
}

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-active { background: #E8F5E9; color: #2E7D32; }
.badge-inactive { background: #F5ECE6; color: #8C847E; }
.badge-scheduled { background: #E0F2FE; color: #0369A1; }
.badge-archived { background: #FAF0E8; color: #C4623C; }

.date-cell {
  display: flex;
  flex-direction: column;
}

.date-txt { font-size: 12px; color: #2D2621; }
.time-txt { font-size: 10.5px; color: #8C847E; }

.action-buttons-cell {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.action-icon-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
  color: #5C544E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.action-icon-btn:hover { border-color: #84261B; color: #84261B; }

/* Pagination Footer */
.pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #FAF7F4;
  border-top: 1px solid #EFE7E0;
  font-size: 12.5px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-nav-btn,
.page-num-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
  color: #3C3530;
  font-size: 12.5px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.page-num-btn.active {
  background: #84261B;
  color: #FFFFFF;
  border-color: #84261B;
}

.page-size-select {
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  padding: 6px 10px;
  background: #FFFFFF;
  font-size: 12px;
}

/* ========================================== */
/* VIEW 2: ARTICLE EDITOR                     */
/* ========================================== */
.editor-top-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-save-draft {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-preview-art {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-publish-art {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  background: #84261B;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
}

.editor-nav-tabs {
  display: flex;
  gap: 20px;
  border-bottom: 1px solid #EFE7E0;
}

.editor-tab {
  background: none;
  border: none;
  font-size: 13.5px;
  font-weight: 500;
  color: #7A726C;
  padding: 8px 4px;
  cursor: pointer;
  position: relative;
}

.editor-tab.active {
  color: #84261B;
  font-weight: 700;
}

.editor-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #84261B;
}

/* 2-Column Grid */
.article-editor-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.editor-arena-col,
.editor-sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.editor-content-card,
.editor-side-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px;
}

.form-group-clean {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-with-counter {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-lbl {
  font-size: 12.5px;
  font-weight: 600;
  color: #3C3530;
}

.char-counter {
  font-size: 11px;
  color: #8C847E;
}

.req { color: #84261B; }

.atelier-input-lg {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 16px;
  font-weight: 600;
  color: #2D2621;
  outline: none;
}

.atelier-input,
.atelier-textarea {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 12.5px;
  color: #2D2621;
  outline: none;
}

.atelier-input:focus,
.atelier-textarea:focus { border-color: #84261B; }

/* Rich Text Toolbar */
.editor-rte-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
}

.rte-select {
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 11.5px;
}

.rte-divider {
  width: 1px;
  height: 18px;
  background: #EFE7E0;
}

.rte-btn {
  background: none;
  border: none;
  padding: 3px 6px;
  font-size: 12px;
  color: #5C544E;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.rte-btn:hover {
  background: #EFE7E0;
  color: #1A1817;
}

.in-article-banner-frame {
  border-left: 1px solid #EFE7E0;
  border-right: 1px solid #EFE7E0;
  background: #FFFFFF;
  padding: 14px;
}

.article-graphic-banner {
  height: 160px;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 24px;
}

.banner-photo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.9);
}

.banner-callout-text {
  position: relative;
  z-index: 1;
  color: #FFFFFF;
}

.banner-callout-text h2 {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 24px;
  line-height: 1.15;
  color: #84261B;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

.banner-callout-text span {
  font-size: 10.5px;
  letter-spacing: 0.1em;
  font-weight: 700;
  color: #3C3530;
}

.atelier-textarea-body {
  border: 1px solid #EFE7E0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  padding: 16px;
  font-size: 13.5px;
  line-height: 1.6;
  color: #2D2621;
  outline: none;
  font-family: inherit;
}

/* Sidebar Cards */
.side-card-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #2D2621;
  margin-bottom: 10px;
}

.featured-img-preview-box {
  width: 100%;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #EFE7E0;
  margin-bottom: 10px;
}

.featured-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-img-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 6px;
}

.btn-img-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  font-size: 11.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-img-action.text-danger:hover {
  border-color: #D32F2F;
  color: #D32F2F;
}

.field-hint {
  font-size: 10.5px;
  color: #8C847E;
}

.link-add-cat {
  font-size: 11.5px;
  color: #84261B;
  font-weight: 600;
  margin-top: 6px;
  display: inline-block;
  cursor: pointer;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.tag-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 99px;
  font-size: 11.5px;
  color: #3C3530;
}

.btn-tag-x {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
}

.publish-date-group {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.checkbox-schedule {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  color: #5C544E;
  margin-top: 4px;
}

.tips-card {
  background: #FAF5F2;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 16px;
}

.tips-top {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #84261B;
  font-size: 13px;
  margin-bottom: 8px;
}

.tips-list {
  padding-left: 18px;
  margin: 0;
  font-size: 11.5px;
  color: #5C544E;
  line-height: 1.5;
}

@media (max-width: 1100px) {
  .article-editor-grid {
    grid-template-columns: 1fr;
  }
}
</style>
