<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
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
  ExternalLink,
  Upload,
  CheckCircle2,
  X,
  Sparkles,
  Save,
  ArrowLeft,
  Star,
  Package,
  ShoppingBag,
  TrendingUp,
  Instagram,
  Facebook,
  Youtube
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View Modes: 'list' | 'detail' | 'editor'
const currentView = ref('list')
const editorMode = ref('add') // 'add' | 'edit'

// Filtering & Search
const searchQuery = ref('')
const selectedCountry = ref('All Countries')
const selectedStatus = ref('All Status')
const selectedFeatured = ref('All')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Selection
const selectedBrandIds = ref([])
const selectAll = ref(false)

// Active brand for detail drawer/view
const activeBrand = ref(null)
const activeDetailTab = ref('overview')

// Brand Form State
const brandForm = reactive({
  id: null,
  name: '',
  slug: '',
  tagline: '',
  country: 'South Korea',
  country_code: 'KR',
  website: 'https://',
  description: '',
  story: '',
  logo_url: '/images/brand-ordinary.png',
  banner_url: '/images/admin-hero-bottles.jpg',
  is_featured: false,
  is_active: true
})

onMounted(async () => {
  await adminStore.fetchBrands()
  if (adminStore.products?.length === 0) {
    await adminStore.fetchProducts()
  }
})

// Countries list
const countriesList = [
  { name: 'Canada', code: 'CA', flag: '🇨🇦' },
  { name: 'South Korea', code: 'KR', flag: '🇰🇷' },
  { name: 'United States', code: 'US', flag: '🇺🇸' },
  { name: 'France', code: 'FR', flag: '🇫🇷' },
  { name: 'Japan', code: 'JP', flag: '🇯🇵' },
  { name: 'United Kingdom', code: 'GB', flag: '🇬🇧' }
]

const getCountryFlag = (countryName) => {
  const match = countriesList.find(c => c.name.toLowerCase() === (countryName || '').toLowerCase())
  return match ? match.flag : '🌐'
}

// Compute filtered brands
const filteredBrands = computed(() => {
  let list = [...(adminStore.brands || [])]

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(b =>
      b.name?.toLowerCase().includes(q) ||
      b.tagline?.toLowerCase().includes(q) ||
      b.country?.toLowerCase().includes(q)
    )
  }

  if (selectedCountry.value !== 'All Countries') {
    list = list.filter(b => b.country === selectedCountry.value)
  }

  if (selectedStatus.value === 'Active') {
    list = list.filter(b => b.is_active)
  } else if (selectedStatus.value === 'Inactive') {
    list = list.filter(b => !b.is_active)
  }

  if (selectedFeatured.value === 'Featured Only') {
    list = list.filter(b => b.is_featured)
  } else if (selectedFeatured.value === 'Standard') {
    list = list.filter(b => !b.is_featured)
  }

  return list
})

// Paginated view
const paginatedBrands = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredBrands.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredBrands.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedCountry.value = 'All Countries'
  selectedStatus.value = 'All Status'
  selectedFeatured.value = 'All'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedBrandIds.value = paginatedBrands.value.map(b => b.id)
  } else {
    selectedBrandIds.value = []
  }
}

// Actions
const toggleFeatured = async (brand) => {
  await adminStore.toggleBrandFeatured(brand.id)
}

const viewBrandDetails = (brand) => {
  activeBrand.value = brand
  activeDetailTab.value = 'overview'
  currentView.value = 'detail'
}

const openAddBrand = () => {
  editorMode.value = 'add'
  brandForm.id = null
  brandForm.name = ''
  brandForm.slug = ''
  brandForm.tagline = ''
  brandForm.country = 'South Korea'
  brandForm.country_code = 'KR'
  brandForm.website = 'https://'
  brandForm.description = ''
  brandForm.story = ''
  brandForm.logo_url = '/images/brand-ordinary.png'
  brandForm.banner_url = '/images/admin-hero-bottles.jpg'
  brandForm.is_featured = false
  brandForm.is_active = true
  currentView.value = 'editor'
}

const openEditBrand = (brand) => {
  editorMode.value = 'edit'
  brandForm.id = brand.id
  brandForm.name = brand.name
  brandForm.slug = brand.slug
  brandForm.tagline = brand.tagline || ''
  brandForm.country = brand.country || 'South Korea'
  brandForm.country_code = brand.country_code || 'KR'
  brandForm.website = brand.website || 'https://'
  brandForm.description = brand.description || ''
  brandForm.story = brand.story || ''
  brandForm.logo_url = brand.logo_url || '/images/brand-ordinary.png'
  brandForm.banner_url = brand.banner_url || '/images/admin-hero-bottles.jpg'
  brandForm.is_featured = brand.is_featured
  brandForm.is_active = brand.is_active
  currentView.value = 'editor'
}

const isSaving = ref(false)
const saveBrand = async () => {
  if (!brandForm.name) {
    alert('Please provide a brand name.')
    return
  }
  isSaving.value = true

  const payload = {
    name: brandForm.name,
    tagline: brandForm.tagline,
    country: brandForm.country,
    country_code: brandForm.country_code,
    website: brandForm.website,
    description: brandForm.description,
    story: brandForm.story,
    logo_url: brandForm.logo_url,
    banner_url: brandForm.banner_url,
    is_featured: brandForm.is_featured,
    is_active: brandForm.is_active
  }

  try {
    if (editorMode.value === 'add') {
      await adminStore.createBrand(payload)
    } else {
      await adminStore.updateBrand(brandForm.id, payload)
    }
    currentView.value = 'list'
  } catch (err) {
    console.error('Failed to save brand:', err)
  } finally {
    isSaving.value = false
  }
}

const deleteBrand = async (brand) => {
  if (confirm(`Are you sure you want to delete "${brand.name}"?`)) {
    await adminStore.deleteBrand(brand.id)
    if (activeBrand.value?.id === brand.id) {
      currentView.value = 'list'
    }
  }
}

// Top products belonging to active brand
const brandProducts = computed(() => {
  if (!activeBrand.value) return []
  return (adminStore.products || []).filter(
    p => p.brand?.toLowerCase() === activeBrand.value.name.toLowerCase()
  )
})
</script>

<template>
  <div class="brands-management-page">
    <!-- ========================================== -->
    <!-- VIEW 1: BRANDS LIST & TABLE               -->
    <!-- Matching Luméa Brands Management Dashboard.png -->
    <!-- ========================================== -->
    <template v-if="currentView === 'list'">
      <!-- Hero Banner -->
      <div class="brands-hero-card">
        <div class="hero-left">
          <span class="hero-eyebrow">BRANDS</span>
          <h1 class="hero-heading">Brands Management</h1>
          <p class="hero-subtext">Manage brand information, logos, and featured status. Showcase the best skincare brands to your customers.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Botanical Brands"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">More great brands</span>
              <span class="motto-line highlight">for a brighter tomorrow.</span>
            </div>
          </div>

          <button class="btn-add-brand" @click="openAddBrand">
            <Plus :size="16" />
            <span>Add Brand</span>
          </button>
        </div>
      </div>

      <!-- Filter Toolbar -->
      <div class="filter-toolbar card">
        <div class="search-input-wrap">
          <Search :size="16" class="search-icon" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search brands..."
            class="atelier-input-clean"
          />
        </div>

        <div class="filter-dropdowns">
          <!-- Country Filter -->
          <div class="select-wrap">
            <select v-model="selectedCountry" class="atelier-select">
              <option value="All Countries">All Countries</option>
              <option v-for="c in countriesList" :key="c.name" :value="c.name">
                {{ c.flag }} {{ c.name }}
              </option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Status Filter -->
          <div class="select-wrap">
            <select v-model="selectedStatus" class="atelier-select">
              <option value="All Status">All Status</option>
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Featured Filter -->
          <div class="select-wrap">
            <select v-model="selectedFeatured" class="atelier-select">
              <option value="All">All Brands</option>
              <option value="Featured Only">Featured Only</option>
              <option value="Standard">Standard Only</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Reset Button -->
          <button class="btn-reset-filter" @click="resetFilters">
            <RotateCcw :size="14" />
            <span>Reset</span>
          </button>

          <!-- Filter Action -->
          <button class="btn-apply-filter">
            <FilterIcon :size="14" />
            <span>Filter</span>
          </button>
        </div>
      </div>

      <!-- Brands Table Card -->
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
              <th>Brand</th>
              <th>Country</th>
              <th class="text-center">Products</th>
              <th>Description</th>
              <th class="text-center">Status</th>
              <th class="text-center">Featured</th>
              <th>Date Added</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="brand in paginatedBrands"
              :key="brand.id"
              class="table-row-hover"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :value="brand.id"
                  v-model="selectedBrandIds"
                />
              </td>
              <td>
                <div class="brand-cell">
                  <div class="brand-logo-pill">
                    <span class="brand-logo-txt">{{ brand.name.slice(0, 2).toUpperCase() }}</span>
                  </div>
                  <div class="brand-names-wrap">
                    <strong class="brand-primary-name">{{ brand.name }}</strong>
                    <span class="brand-tagline-text">{{ brand.tagline || 'Clinical Formulations' }}</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="country-cell">
                  <span class="flag-icon">{{ getCountryFlag(brand.country) }}</span>
                  <span>{{ brand.country }}</span>
                </div>
              </td>
              <td class="text-center">
                <strong class="prod-count-text">{{ brand.products_count || 24 }}</strong>
              </td>
              <td>
                <span class="desc-cell-text">{{ brand.description || 'Gentle skincare formulation.' }}</span>
              </td>
              <td class="text-center">
                <span
                  class="status-pill"
                  :class="brand.is_active ? 'badge-active' : 'badge-inactive'"
                >
                  {{ brand.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="text-center">
                <!-- Toggle Switch matching mockup -->
                <button
                  type="button"
                  class="atelier-toggle-switch"
                  :class="{ active: brand.is_featured }"
                  @click="toggleFeatured(brand)"
                >
                  <span class="toggle-slider"></span>
                </button>
              </td>
              <td>
                <span class="date-cell-text">
                  {{ brand.created_at ? new Date(brand.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Jan 12, 2024' }}
                </span>
              </td>
              <td class="text-right">
                <div class="action-buttons-cell">
                  <button
                    class="action-icon-btn"
                    title="Edit Brand"
                    @click="openEditBrand(brand)"
                  >
                    <Edit2 :size="14" />
                  </button>
                  <button
                    class="action-icon-btn"
                    title="View Details"
                    @click="viewBrandDetails(brand)"
                  >
                    <Eye :size="14" />
                  </button>
                  <button
                    class="action-icon-btn text-danger"
                    title="Delete Brand"
                    @click="deleteBrand(brand)"
                  >
                    <Trash2 :size="14" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedBrands.length === 0">
              <td colspan="9" class="empty-table-cell">
                <p>No skincare brands found matching your criteria.</p>
                <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Footer -->
        <div class="pagination-footer">
          <span class="pagination-summary">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredBrands.length) }} of {{ filteredBrands.length }} brands
          </span>

          <div class="pagination-controls">
            <button
              class="page-nav-btn"
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              <ChevronLeft :size="15" />
            </button>

            <button
              v-for="page in totalPages"
              :key="page"
              class="page-num-btn"
              :class="{ active: currentPage === page }"
              @click="currentPage = page"
            >
              {{ page }}
            </button>

            <button
              class="page-nav-btn"
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              <ChevronRight :size="15" />
            </button>
          </div>

          <div class="items-per-page-select">
            <select v-model="itemsPerPage" class="page-size-select">
              <option :value="10">10 / page</option>
              <option :value="20">20 / page</option>
            </select>
          </div>
        </div>
      </div>
    </template>

    <!-- ========================================== -->
    <!-- VIEW 2: BRAND DETAIL SHOWCASE             -->
    <!-- Matching Luméa Skincare Brand Management Dashboard.png (Right Mockup) -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'detail' && activeBrand">
      <div class="detail-page-wrapper">
        <!-- Top Breadcrumb & Header -->
        <div class="detail-header-card">
          <div class="header-left">
            <div class="editor-breadcrumb">
              <button class="btn-back-link" @click="currentView = 'list'">
                <ArrowLeft :size="13" /> Brands
              </button>
              <span class="crumb-sep">/</span>
              <span class="crumb-current">{{ activeBrand.name }}</span>
            </div>
            <div class="title-with-badge">
              <h1 class="brand-hero-title">{{ activeBrand.name }}</h1>
              <span class="status-pill badge-active">Active</span>
            </div>
            <p class="brand-hero-sub">View and manage brand information, products, and performance.</p>
          </div>

          <div class="header-right-actions">
            <button class="btn-edit-brand-pill" @click="openEditBrand(activeBrand)">
              <Edit2 :size="14" />
              <span>Edit Brand</span>
            </button>
            <button class="btn-more-options">
              <Trash2 :size="14" @click="deleteBrand(activeBrand)" />
            </button>
          </div>
        </div>

        <!-- Brand Showcase Visual Hero -->
        <div class="brand-showcase-banner">
          <div class="showcase-content">
            <div class="showcase-logo-badge">
              <strong class="logo-display-text">{{ activeBrand.name }}</strong>
              <span class="logo-tagline-sub">{{ activeBrand.tagline || 'Clinical Formulations' }}</span>
            </div>

            <div class="showcase-meta-row">
              <div class="showcase-meta-item">
                <span class="flag-icon">{{ getCountryFlag(activeBrand.country) }}</span>
                <span>{{ activeBrand.country }}</span>
              </div>
              <a :href="activeBrand.website" target="_blank" class="showcase-link">
                <ExternalLink :size="13" />
                <span>{{ activeBrand.website || 'https://theordinary.com' }}</span>
              </a>
              <span class="showcase-joined">Joined {{ new Date(activeBrand.created_at || Date.now()).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}</span>
            </div>
          </div>

          <div class="showcase-right-badges">
            <div class="featured-switch-card">
              <span>Featured Brand</span>
              <button
                type="button"
                class="atelier-toggle-switch"
                :class="{ active: activeBrand.is_featured }"
                @click="toggleFeatured(activeBrand)"
              >
                <span class="toggle-slider"></span>
              </button>
            </div>
            <div class="brand-prods-counter">
              <strong>{{ activeBrand.products_count || 24 }}</strong>
              <span>Products</span>
            </div>
          </div>
        </div>

        <!-- Detail Tabs -->
        <div class="editor-nav-tabs">
          <button
            class="editor-tab"
            :class="{ active: activeDetailTab === 'overview' }"
            @click="activeDetailTab = 'overview'"
          >
            Overview
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeDetailTab === 'products' }"
            @click="activeDetailTab = 'products'"
          >
            Products ({{ activeBrand.products_count || 24 }})
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeDetailTab === 'promotions' }"
            @click="activeDetailTab = 'promotions'"
          >
            Promotions (3)
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeDetailTab === 'performance' }"
            @click="activeDetailTab = 'performance'"
          >
            Performance
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeDetailTab === 'settings' }"
            @click="activeDetailTab = 'settings'"
          >
            Settings
          </button>
        </div>

        <!-- 2-Column Detail Content -->
        <div class="detail-grid-layout">
          <!-- Left Column -->
          <div class="detail-left-col">
            <!-- Brand Information Card -->
            <div class="card detail-card">
              <div class="card-header-row">
                <h3 class="detail-card-title">Brand Information</h3>
                <button class="btn-edit-text" @click="openEditBrand(activeBrand)">Edit</button>
              </div>

              <div class="info-kv-list">
                <div class="kv-row">
                  <span class="kv-label">Brand Name</span>
                  <strong class="kv-val">{{ activeBrand.name }}</strong>
                </div>
                <div class="kv-row">
                  <span class="kv-label">Country</span>
                  <div class="kv-val-flex">
                    <span>{{ getCountryFlag(activeBrand.country) }}</span>
                    <strong>{{ activeBrand.country }}</strong>
                  </div>
                </div>
                <div class="kv-row">
                  <span class="kv-label">Tagline</span>
                  <span class="kv-val">{{ activeBrand.tagline || 'Clinical Formulations with Integrity.' }}</span>
                </div>
                <div class="kv-row">
                  <span class="kv-label">Website</span>
                  <a :href="activeBrand.website" target="_blank" class="kv-link">
                    {{ activeBrand.website || 'https://theordinary.com' }} <ExternalLink :size="12" />
                  </a>
                </div>
                <div class="kv-row">
                  <span class="kv-label">Short Description</span>
                  <span class="kv-val">{{ activeBrand.description || 'Science-backed skincare at an honest price.' }}</span>
                </div>
                <div class="kv-row">
                  <span class="kv-label">Brand Story</span>
                  <p class="kv-story">
                    {{ activeBrand.story || 'The Ordinary is a skincare brand committed to clinical formulations and transparency. Their mission is to make effective skincare more accessible by focusing on proven ingredients, clear information, and affordable prices.' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Social Media Card -->
            <div class="card detail-card">
              <h3 class="detail-card-title">Social Media</h3>
              <div class="social-links-list">
                <div class="social-link-item">
                  <Instagram :size="16" class="social-icon text-pink" />
                  <span>https://instagram.com/{{ activeBrand.slug || 'theordinary' }}</span>
                </div>
                <div class="social-link-item">
                  <Facebook :size="16" class="social-icon text-blue" />
                  <span>https://facebook.com/{{ activeBrand.slug || 'theordinary' }}</span>
                </div>
                <div class="social-link-item">
                  <Youtube :size="16" class="social-icon text-red" />
                  <span>https://youtube.com/{{ activeBrand.slug || 'theordinary' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="detail-right-col">
            <!-- Brand Images -->
            <div class="card detail-card">
              <div class="card-header-row">
                <h3 class="detail-card-title">Brand Images</h3>
                <button class="btn-edit-text" @click="openEditBrand(activeBrand)">Edit</button>
              </div>

              <div class="brand-images-showcase">
                <div class="brand-logo-frame">
                  <span class="frame-label">Brand Logo</span>
                  <div class="logo-box">
                    <strong>{{ activeBrand.name }}</strong>
                  </div>
                </div>
                <div class="brand-banner-frame">
                  <span class="frame-label">Brand Banner</span>
                  <img
                    :src="activeBrand.banner_url || '/images/admin-hero-bottles.jpg'"
                    class="banner-box-img"
                    @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
                  />
                </div>
              </div>
            </div>

            <!-- Quick Stats 4 Grid -->
            <div class="card detail-card">
              <div class="card-header-row">
                <h3 class="detail-card-title">Quick Stats</h3>
                <span class="sub-muted">Last 6 Months</span>
              </div>

              <div class="quick-stats-4-grid">
                <div class="quick-stat-box">
                  <div class="stat-icon-wrap rose-bg">
                    <Package :size="16" />
                  </div>
                  <div class="stat-meta">
                    <strong>{{ activeBrand.products_count || 24 }}</strong>
                    <span>Products</span>
                  </div>
                </div>

                <div class="quick-stat-box">
                  <div class="stat-icon-wrap peach-bg">
                    <ShoppingBag :size="16" />
                  </div>
                  <div class="stat-meta">
                    <strong>12,450</strong>
                    <span>Total Sales</span>
                  </div>
                </div>

                <div class="quick-stat-box">
                  <div class="stat-icon-wrap amber-bg">
                    <TrendingUp :size="16" />
                  </div>
                  <div class="stat-meta">
                    <strong>3,280</strong>
                    <span>Total Orders</span>
                  </div>
                </div>

                <div class="quick-stat-box">
                  <div class="stat-icon-wrap gold-bg">
                    <Star :size="16" />
                  </div>
                  <div class="stat-meta">
                    <strong>4.8</strong>
                    <span>Avg. Rating</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Products for this Brand -->
            <div class="card detail-card">
              <div class="card-header-row">
                <h3 class="detail-card-title">Top Products</h3>
                <router-link to="/products" class="view-all-link">View all</router-link>
              </div>

              <div class="brand-top-prods-list">
                <div
                  v-for="(prod, idx) in brandProducts.slice(0, 5)"
                  :key="prod.id || idx"
                  class="brand-prod-row"
                >
                  <span class="prod-rank">{{ idx + 1 }}</span>
                  <img :src="prod.image_url" class="mini-prod-img" @error="$event.target.src = '/images/prod-sk2.jpg'" />
                  <div class="mini-prod-info">
                    <strong class="mini-title">{{ prod.name }}</strong>
                    <span class="mini-sold">{{ 200 + (idx * 150) }} sold</span>
                  </div>
                  <strong class="mini-rev">${{ Number(prod.price * (200 + (idx * 150))).toLocaleString() }}</strong>
                </div>

                <div v-if="brandProducts.length === 0" class="sub-muted">
                  No products registered for this brand yet.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ========================================== -->
    <!-- VIEW 3: ADD / EDIT BRAND FORM             -->
    <!-- Matching Luméa Skincare Brand Management Dashboard.png (Left Mockup) -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'editor'">
      <div class="brands-hero-card">
        <div class="hero-left">
          <div class="editor-breadcrumb">
            <button class="btn-back-link" @click="currentView = 'list'">
              <ArrowLeft :size="13" /> Brands
            </button>
            <span class="crumb-sep">/</span>
            <span class="crumb-current">{{ editorMode === 'add' ? 'Add Brand' : 'Edit Brand' }}</span>
          </div>
          <h1 class="hero-heading">
            {{ editorMode === 'add' ? 'Add New Brand' : `Edit: ${brandForm.name}` }}
          </h1>
          <p class="hero-subtext">Add brand information and showcase a new skincare brand on your store.</p>
        </div>

        <div class="hero-right">
          <div class="editor-top-actions">
            <button class="btn-cancel" @click="currentView = 'list'">Cancel</button>
            <button class="btn-save-brand" :disabled="isSaving" @click="saveBrand">
              <Save :size="15" />
              <span>{{ isSaving ? 'Saving to Database...' : 'Save Brand' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Editor Form Grid -->
      <div class="brand-editor-container">
        <!-- 1. Basic Information -->
        <div class="card editor-card">
          <h3 class="editor-card-title">Basic Information</h3>
          <p class="editor-card-sub">Enter the main information about the brand.</p>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Brand Name <span class="req">*</span></label>
              <input
                v-model="brandForm.name"
                type="text"
                placeholder="e.g. The Ordinary"
                class="atelier-input"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Country <span class="req">*</span></label>
              <select v-model="brandForm.country" class="atelier-input">
                <option v-for="c in countriesList" :key="c.name" :value="c.name">
                  {{ c.flag }} {{ c.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Tagline</label>
              <input
                v-model="brandForm.tagline"
                type="text"
                placeholder="e.g. Clinical Formulations with Integrity"
                class="atelier-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Website</label>
              <input
                v-model="brandForm.website"
                type="url"
                placeholder="https://example.com"
                class="atelier-input"
              />
            </div>
          </div>

          <div class="form-group">
            <div class="label-with-counter">
              <label class="form-label">Short Description <span class="req">*</span></label>
              <span class="char-counter">{{ (brandForm.description || '').length }}/160</span>
            </div>
            <textarea
              v-model="brandForm.description"
              maxlength="160"
              rows="2"
              placeholder="A short description that will appear in brand listings (max 160 characters)."
              class="atelier-textarea"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">Brand Story</label>
            <textarea
              v-model="brandForm.story"
              rows="4"
              placeholder="Tell the story of this brand, its values, and what makes it special..."
              class="atelier-textarea"
            ></textarea>
          </div>
        </div>

        <!-- 2. Brand Images -->
        <div class="card editor-card">
          <h3 class="editor-card-title">Brand Images</h3>
          <p class="editor-card-sub">Upload brand logo and banner image.</p>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Brand Logo <span class="req">*</span></label>
              <div class="dropzone-box-small">
                <Upload :size="20" class="upload-icon" />
                <span class="drop-text-sm">Drag and drop logo here or browse</span>
                <span class="drop-hint">PNG, JPG, SVG (Max 2MB) • 500x500px</span>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Brand Banner</label>
              <div class="dropzone-box-small">
                <Upload :size="20" class="upload-icon" />
                <span class="drop-text-sm">Drag and drop banner here or browse</span>
                <span class="drop-hint">PNG, JPG (Max 5MB) • 1920x600px</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Settings -->
        <div class="card editor-card">
          <h3 class="editor-card-title">Settings</h3>
          <p class="editor-card-sub">Set the brand status and display options.</p>

          <div class="form-row-2 align-center">
            <div class="form-group">
              <label class="form-label">Status <span class="req">*</span></label>
              <select v-model="brandForm.is_active" class="atelier-input">
                <option :value="true">Active</option>
                <option :value="false">Inactive</option>
              </select>
            </div>

            <div class="featured-toggle-row">
              <button
                type="button"
                class="atelier-toggle-switch"
                :class="{ active: brandForm.is_featured }"
                @click="brandForm.is_featured = !brandForm.is_featured"
              >
                <span class="toggle-slider"></span>
              </button>
              <div class="toggle-texts">
                <strong>Featured Brand</strong>
                <span>Show this brand on homepage and featured sections.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.brands-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.brands-hero-card {
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

.hero-eyebrow {
  display: inline-block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #84261B;
  font-weight: 600;
  margin-bottom: 4px;
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

.btn-add-brand {
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

.btn-add-brand:hover {
  background: #6D1E15;
}

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
  max-width: 320px;
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

.brand-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo-pill {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #F8E9E4;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #EFE7E0;
}

.brand-logo-txt {
  font-size: 13px;
  font-weight: 800;
  color: #84261B;
}

.brand-names-wrap {
  display: flex;
  flex-direction: column;
}

.brand-primary-name {
  font-size: 13.5px;
  color: #2D2621;
}

.brand-tagline-text {
  font-size: 11px;
  color: #8C847E;
}

.country-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.flag-icon {
  font-size: 15px;
}

.prod-count-text {
  font-size: 13px;
  color: #2D2621;
}

.desc-cell-text {
  color: #7A726C;
  font-size: 12px;
  max-width: 240px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-active {
  background: #E8F5E9;
  color: #2E7D32;
}

.badge-inactive {
  background: #F5ECE6;
  color: #8C847E;
}

/* Atelier Toggle Switch */
.atelier-toggle-switch {
  width: 38px;
  height: 20px;
  background: #EFE7E0;
  border-radius: 99px;
  border: none;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s;
  padding: 2px;
}

.atelier-toggle-switch.active {
  background: #84261B;
}

.toggle-slider {
  display: block;
  width: 16px;
  height: 16px;
  background: #FFFFFF;
  border-radius: 50%;
  transition: transform 0.2s;
}

.atelier-toggle-switch.active .toggle-slider {
  transform: translateX(18px);
}

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

.action-icon-btn:hover {
  border-color: #84261B;
  color: #84261B;
}

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
/* DETAIL SHOWCASE STYLES                     */
/* ========================================== */
.detail-page-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-header-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px 24px;
}

.title-with-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 4px 0;
}

.brand-hero-title {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 28px;
  font-weight: 700;
  color: #84261B;
}

.brand-hero-sub {
  font-size: 13px;
  color: #7A726C;
}

.header-right-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-edit-brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1px solid #84261B;
  color: #84261B;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-more-options {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
  color: #8C847E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* Brand Showcase Banner */
.brand-showcase-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FAF5F2 0%, #FFFFFF 100%);
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px 30px;
}

.showcase-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.showcase-logo-badge strong {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 24px;
  color: #2D2621;
}

.showcase-logo-badge .logo-tagline-sub {
  font-size: 12px;
  color: #8C847E;
  display: block;
}

.showcase-meta-row {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12.5px;
  color: #5C544E;
}

.showcase-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #84261B;
  text-decoration: none;
}

.showcase-right-badges {
  display: flex;
  align-items: center;
  gap: 20px;
}

.featured-switch-card {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: #3C3530;
}

.brand-prods-counter {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 10px;
  padding: 8px 16px;
}

.brand-prods-counter strong {
  font-size: 18px;
  color: #84261B;
}

.brand-prods-counter span {
  font-size: 10.5px;
  color: #8C847E;
  text-transform: uppercase;
}

/* Detail Grid Layout */
.detail-grid-layout {
  display: grid;
  grid-template-columns: 1.4fr 1.6fr;
  gap: 20px;
}

.detail-left-col,
.detail-right-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px;
}

.detail-card-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D2621;
}

.btn-edit-text {
  background: none;
  border: none;
  color: #84261B;
  font-weight: 600;
  font-size: 12.5px;
  cursor: pointer;
}

.info-kv-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 14px;
}

.kv-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.kv-label {
  font-size: 11px;
  color: #8C847E;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kv-val {
  font-size: 13px;
  color: #2D2621;
}

.kv-val-flex {
  display: flex;
  align-items: center;
  gap: 6px;
}

.kv-link {
  font-size: 13px;
  color: #84261B;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
}

.kv-story {
  font-size: 12.5px;
  color: #5C544E;
  line-height: 1.5;
}

/* Quick Stats 4 Grid */
.quick-stats-4-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.quick-stat-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
}

.stat-icon-wrap {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rose-bg { background: #F8E9E4; color: #84261B; }
.peach-bg { background: #FAF0E8; color: #C4623C; }
.amber-bg { background: #FEF7ED; color: #B25E00; }
.gold-bg { background: #FDF9E8; color: #9A7B1C; }

.stat-meta {
  display: flex;
  flex-direction: column;
}

.stat-meta strong {
  font-size: 16px;
  color: #2D2621;
}

.stat-meta span {
  font-size: 11px;
  color: #8C847E;
}

/* Brand Images Showcase */
.brand-images-showcase {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 16px;
  margin-top: 12px;
}

.brand-logo-frame,
.brand-banner-frame {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.frame-label {
  font-size: 11px;
  color: #8C847E;
}

.logo-box {
  width: 100%;
  height: 90px;
  border-radius: 8px;
  border: 1px solid #EFE7E0;
  background: #FAF7F4;
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner-box-img {
  width: 100%;
  height: 90px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

/* Social Links */
.social-links-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 12px;
}

.social-link-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
  color: #5C544E;
}

.text-pink { color: #E1306C; }
.text-blue { color: #1877F2; }
.text-red { color: #FF0000; }

/* Top Products list */
.brand-top-prods-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 12px;
}

.brand-prod-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.prod-rank {
  font-size: 12px;
  font-weight: 700;
  color: #8C847E;
  width: 14px;
}

.mini-prod-img {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.mini-prod-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.mini-title {
  font-size: 12px;
  color: #2D2621;
}

.mini-sold {
  font-size: 10.5px;
  color: #8C847E;
}

.mini-rev {
  font-size: 12px;
  font-weight: 700;
  color: #2D2621;
}

/* Editor Form */
.brand-editor-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.btn-save-brand {
  padding: 8px 18px;
  background: #84261B;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.dropzone-box-small {
  border: 1.5px dashed #E5D7CD;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  background: #FAF7F4;
}

.drop-text-sm {
  font-size: 12px;
  color: #3C3530;
  display: block;
}

.featured-toggle-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.toggle-texts {
  display: flex;
  flex-direction: column;
}

.toggle-texts strong {
  font-size: 13px;
  color: #2D2621;
}

.toggle-texts span {
  font-size: 11px;
  color: #8C847E;
}

@media (max-width: 1100px) {
  .detail-grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>
