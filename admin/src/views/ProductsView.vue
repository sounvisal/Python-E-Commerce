<script setup>
import apiClient from '@/api/client'
import { ref, computed, reactive, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { validateProduct } from '@/utils/validation'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import LoadingSkeleton from '@/components/common/LoadingSkeleton.vue'
import {
  Search,
  Plus,
  RotateCcw,
  Filter as FilterIcon,
  Edit2,
  Eye,
  MoreHorizontal,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Star,
  Trash2,
  Upload,
  CheckCircle2,
  X,
  ExternalLink,
  Sparkles,
  Save,
  ArrowLeft,
  Video,
  Film
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View Mode: 'list' | 'editor'
const currentView = ref('list')
const editorMode = ref('add') // 'add' | 'edit'

// Filtering & Search
const searchQuery = ref('')
const selectedCategory = ref('All Categories')
const selectedBrand = ref('All Brands')
const selectedStockStatus = ref('All Stock')
const selectedProductStatus = ref('All Status')
const currentTab = ref('all') // 'all', 'active', 'inactive', 'low_stock', 'out_of_stock'

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Selection
const selectedProductIds = ref([])
const selectAll = ref(false)

// Active tab for the editor form
const activeEditorTab = ref('basic')

// Product form state
const productForm = reactive({
  id: null,
  name: '',
  sku: '',
  brand: 'The Ordinary',
  category_id: 1,
  category_name: 'Face Serums',
  subcategory: 'Hydrating',
  short_description: '',
  description: '',
  price: 24.00,
  compare_at_price: null,
  stock: 20,
  low_stock_threshold: 10,
  status: 'active', // 'active', 'draft', 'inactive'
  rating: 4.8,
  reviews: 124,
  skin_types: ['Normal', 'Dry'],
  skin_concerns: ['Dryness', 'Brightening'],
  ingredients: 'Hyaluronic Acid, Niacinamide, Camellia Sinensis Leaf Extract',
  how_to_use: 'Apply a few drops to cleansed face morning and night before heavier creams.',
  video_url: '',
  video_title: '',
  video_thumbnail: '',
  images: [
    '/images/prod-sk2.jpg',
    '/images/prod-lamer.jpg',
    '/images/prod-sulwhasoo.jpg'
  ]
})

// Quick Preview Modal state
const previewProduct = ref(null)
const showPreviewModal = ref(false)

onMounted(async () => {
  await Promise.all([
    adminStore.fetchProducts(),
    adminStore.fetchCategories()
  ])
})

// Brand options
const brandOptions = [
  'All Brands',
  'The Ordinary',
  'SKIN1004',
  'CeraVe',
  'La Roche-Posay',
  'Cetaphil',
  'innisfree',
  "Paula's Choice",
  "L'Oréal",
  'Anua',
  'COSRX',
  'Luméa Atelier'
]

// Skin options
const skinTypesList = ['Normal', 'Oily', 'Dry', 'Combination', 'Sensitive']
const skinConcernsList = ['Acne', 'Aging', 'Dark Spots', 'Dryness', 'Oil Control', 'Pores', 'Redness', 'Brightening']

// Compute filtered products
const filteredProducts = computed(() => {
  let list = [...(adminStore.products || [])]

  // Filter by Tab
  if (currentTab.value === 'active') {
    list = list.filter(p => (p.stock || 0) > 0 && p.status !== 'inactive')
  } else if (currentTab.value === 'inactive') {
    list = list.filter(p => p.status === 'inactive')
  } else if (currentTab.value === 'low_stock') {
    list = list.filter(p => (p.stock || 0) <= 10 && (p.stock || 0) > 0)
  } else if (currentTab.value === 'out_of_stock') {
    list = list.filter(p => (p.stock || 0) === 0)
  }

  // Filter by Search Query
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.name?.toLowerCase().includes(q) ||
      p.brand?.toLowerCase().includes(q) ||
      p.slug?.toLowerCase().includes(q) ||
      p.category_name?.toLowerCase().includes(q)
    )
  }

  // Filter by Category
  if (selectedCategory.value !== 'All Categories') {
    list = list.filter(p =>
      p.category_name === selectedCategory.value ||
      p.category === selectedCategory.value.toLowerCase().replace(/\s+/g, '-')
    )
  }

  // Filter by Brand
  if (selectedBrand.value !== 'All Brands') {
    list = list.filter(p => p.brand === selectedBrand.value)
  }

  // Filter by Stock Status
  if (selectedStockStatus.value === 'In Stock') {
    list = list.filter(p => (p.stock || 0) > 10)
  } else if (selectedStockStatus.value === 'Low Stock') {
    list = list.filter(p => (p.stock || 0) <= 10 && (p.stock || 0) > 0)
  } else if (selectedStockStatus.value === 'Out of Stock') {
    list = list.filter(p => (p.stock || 0) === 0)
  }

  return list
})

// Tab counts
const counts = computed(() => {
  const all = adminStore.products || []
  return {
    all: all.length,
    active: all.filter(p => (p.stock || 0) > 0 && p.status !== 'inactive').length,
    inactive: all.filter(p => p.status === 'inactive').length,
    low_stock: all.filter(p => (p.stock || 0) <= 10 && (p.stock || 0) > 0).length,
    out_of_stock: all.filter(p => (p.stock || 0) === 0).length
  }
})

// Paginated view
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredProducts.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'All Categories'
  selectedBrand.value = 'All Brands'
  selectedStockStatus.value = 'All Stock'
  selectedProductStatus.value = 'All Status'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedProductIds.value = paginatedProducts.value.map(p => p.id)
  } else {
    selectedProductIds.value = []
  }
}

// Helpers
const getStockBadge = (stock) => {
  if (stock === 0) return { label: 'Out of Stock', class: 'badge-out' }
  if (stock <= 10) return { label: 'Low Stock', class: 'badge-low' }
  return { label: 'Active', class: 'badge-active' }
}

const getSku = (prod) => {
  if (prod.sku) return prod.sku
  const idStr = String(prod.id || 1).padStart(3, '0')
  return `LUM-P${idStr}`
}

// Open Editor in 'add' mode
const openAddProduct = () => {
  editorMode.value = 'add'
  productForm.id = null
  productForm.name = ''
  productForm.sku = `LUM-P${String((adminStore.products?.length || 0) + 1).padStart(3, '0')}`
  productForm.brand = 'The Ordinary'
  productForm.category_id = adminStore.categories[0]?.id || 1
  productForm.category_name = adminStore.categories[0]?.name || 'Face Serums'
  productForm.subcategory = 'Hydrating'
  productForm.short_description = ''
  productForm.description = ''
  productForm.price = 24.00
  productForm.compare_at_price = null
  productForm.stock = 25
  productForm.low_stock_threshold = 10
  productForm.status = 'active'
  productForm.rating = 5.0
  productForm.reviews = 0
  productForm.skin_types = ['Normal', 'Dry']
  productForm.skin_concerns = ['Dryness', 'Brightening']
  productForm.ingredients = 'Hyaluronic Acid, Vitamin C, Niacinamide'
  productForm.how_to_use = 'Gently smooth onto face and neck after cleansing.'
  productForm.images = ['/images/prod-sk2.jpg']
  productForm.video_url = ''
  productForm.video_title = ''
  productForm.video_thumbnail = ''

  currentView.value = 'editor'
}

// Open Editor in 'edit' mode
const openEditProduct = (prod) => {
  editorMode.value = 'edit'
  productForm.id = prod.id
  productForm.name = prod.name
  productForm.sku = getSku(prod)
  productForm.brand = prod.brand || 'Luméa Atelier'
  productForm.category_id = prod.category_id || 1
  productForm.category_name = prod.category_name || prod.category || 'Face Serums'
  productForm.subcategory = 'Essence'
  productForm.short_description = prod.short_description || prod.description?.slice(0, 140) || ''
  productForm.description = prod.description || ''
  productForm.price = prod.price || 24.00
  productForm.compare_at_price = prod.compare_at_price || null
  productForm.stock = prod.stock ?? 20
  productForm.low_stock_threshold = 10
  productForm.status = (prod.stock === 0) ? 'draft' : 'active'
  productForm.rating = prod.rating || 4.8
  productForm.reviews = prod.reviews || 42
  productForm.skin_types = prod.skin_types || ['Normal', 'Combination']
  productForm.skin_concerns = prod.skin_concerns || ['Brightening', 'Pores']
  productForm.ingredients = prod.ingredients || 'Pitera, Niacinamide, Botanical Extracts'
  productForm.how_to_use = prod.how_to_use || 'Dispense 2-3 drops into palm and press into clean skin.'
  productForm.images = prod.image_url ? [prod.image_url] : ['/images/prod-sk2.jpg']
  productForm.video_url = prod.video_url || ''
  productForm.video_title = prod.video_title || ''
  productForm.video_thumbnail = prod.video_thumbnail || ''

  currentView.value = 'editor'
}

// Save Product directly to SQLite Database
const isSaving = ref(false)
const saveProduct = async () => {
  const validation = validateProduct(productForm)
  if (!validation.valid) {
    validation.errors.forEach(err => {
      adminStore.addToast(err, 'error')
    })
    return
  }

  isSaving.value = true

  const payload = {
    name: productForm.name.trim(),
    brand: productForm.brand,
    category_id: productForm.category_id,
    category_name: productForm.category_name,
    price: Number(productForm.price),
    compare_at_price: productForm.compare_at_price ? Number(productForm.compare_at_price) : null,
    stock: Number(productForm.stock),
    image_url: productForm.images[0] || '/images/prod-sk2.jpg',
    description: productForm.description || productForm.short_description,
    short_description: productForm.short_description,
    is_featured: false,
    rating: productForm.rating,
    reviews: productForm.reviews,
    video_url: productForm.video_url || null,
    video_title: productForm.video_title || null,
    video_thumbnail: productForm.video_thumbnail || null,
  }

  try {
    if (editorMode.value === 'add') {
      await adminStore.createProduct(payload)
    } else {
      await adminStore.updateProduct(productForm.id, payload)
    }
    currentView.value = 'list'
  } catch (err) {
    console.error('Failed to save product:', err)
    adminStore.addToast('Failed to save product. Please try again.', 'error')
  } finally {
    isSaving.value = false
  }
}

// Quick View Product Modal
const openQuickView = (prod) => {
  previewProduct.value = prod
  showPreviewModal.value = true
}

// Delete Product Confirmation Dialog
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

const deleteProduct = (id, name) => {
  deleteTarget.value = { id, name }
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  if (deleteTarget.value) {
    await adminStore.deleteProduct(deleteTarget.value.id)
    showDeleteConfirm.value = false
    deleteTarget.value = null
  }
}

// Real Image upload to backend /api/upload
const fileInputRef = ref(null)
const isUploading = ref(false)

const triggerImageUpload = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click()
  }
}

const handleProductFileUpload = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.data?.status === 'success' && res.data.data?.url) {
      productForm.images.unshift(res.data.data.url)
      adminStore.addToast('Image uploaded and synced to atelier storage', 'success')
    }
  } catch (err) {
    console.error('Failed to upload product image:', err)
    adminStore.addToast('Failed to upload image', 'error')
  } finally {
    isUploading.value = false
    if (e.target) e.target.value = ''
  }
}

// Real Video Upload to backend /api/upload/video
const videoFileInputRef = ref(null)
const isUploadingVideo = ref(false)

const triggerVideoUpload = () => {
  if (videoFileInputRef.value) {
    videoFileInputRef.value.click()
  }
}

const handleProductVideoUpload = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  isUploadingVideo.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await apiClient.post('/upload/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.data?.status === 'success' && res.data.data?.url) {
      productForm.video_url = res.data.data.url
      if (!productForm.video_title) {
        productForm.video_title = `${productForm.name} Texture Demonstration`
      }
      adminStore.addToast('Texture demonstration video uploaded and synced to storage', 'success')
    }
  } catch (err) {
    console.error('Failed to upload video:', err)
    adminStore.addToast('Failed to upload video', 'error')
  } finally {
    isUploadingVideo.value = false
    if (e.target) e.target.value = ''
  }
}

const removeImage = (index) => {
  productForm.images.splice(index, 1)
}

const toggleSkinType = (type) => {
  const idx = productForm.skin_types.indexOf(type)
  if (idx > -1) {
    productForm.skin_types.splice(idx, 1)
  } else {
    productForm.skin_types.push(type)
  }
}

const toggleSkinConcern = (concern) => {
  const idx = productForm.skin_concerns.indexOf(concern)
  if (idx > -1) {
    productForm.skin_concerns.splice(idx, 1)
  } else {
    productForm.skin_concerns.push(concern)
  }
}
</script>

<template>
  <div class="products-management-page">
    <!-- ========================================== -->
    <!-- VIEW 1: PRODUCTS LIST & TABLE              -->
    <!-- ========================================== -->
    <template v-if="currentView === 'list'">
      <!-- Hero Banner matching Luméa Beauty Products Dashboard.png -->
      <div class="products-hero-card">
        <div class="hero-left">
          <span class="hero-eyebrow">PRODUCTS</span>
          <h1 class="hero-heading">Products Management</h1>
          <p class="hero-subtext">Manage your products, update details, track stock, and keep your store fresh.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Botanical Products"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">Great products</span>
              <span class="motto-line highlight">brighter tomorrows.</span>
            </div>
          </div>

          <button class="btn-add-product" @click="openAddProduct">
            <Plus :size="16" />
            <span>Add Product</span>
          </button>
        </div>
      </div>

      <!-- Status Tabs matching mockup -->
      <div class="status-tabs-row">
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'all' }"
          @click="currentTab = 'all'"
        >
          All Products ({{ counts.all }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'active' }"
          @click="currentTab = 'active'"
        >
          Active ({{ counts.active }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'inactive' }"
          @click="currentTab = 'inactive'"
        >
          Inactive ({{ counts.inactive }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'low_stock' }"
          @click="currentTab = 'low_stock'"
        >
          Low Stock ({{ counts.low_stock }})
        </button>
        <button
          class="tab-btn"
          :class="{ active: currentTab === 'out_of_stock' }"
          @click="currentTab = 'out_of_stock'"
        >
          Out of Stock ({{ counts.out_of_stock }})
        </button>
      </div>

      <!-- Filter & Search Toolbar matching mockup -->
      <div class="filter-toolbar card">
        <div class="search-input-wrap">
          <Search :size="16" class="search-icon" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search products..."
            class="atelier-input-clean"
          />
        </div>

        <div class="filter-dropdowns">
          <!-- Category Filter -->
          <div class="select-wrap">
            <select v-model="selectedCategory" class="atelier-select">
              <option value="All Categories">All Categories</option>
              <option
                v-for="cat in adminStore.categories"
                :key="cat.id"
                :value="cat.name"
              >
                {{ cat.name }}
              </option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Brand Filter -->
          <div class="select-wrap">
            <select v-model="selectedBrand" class="atelier-select">
              <option v-for="b in brandOptions" :key="b" :value="b">{{ b }}</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Stock Filter -->
          <div class="select-wrap">
            <select v-model="selectedStockStatus" class="atelier-select">
              <option value="All Stock">All Stock</option>
              <option value="In Stock">In Stock (> 10)</option>
              <option value="Low Stock">Low Stock (≤ 10)</option>
              <option value="Out of Stock">Out of Stock (0)</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <!-- Product Status -->
          <div class="select-wrap">
            <select v-model="selectedProductStatus" class="atelier-select">
              <option value="All Status">All Status</option>
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
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

      <!-- Main Products Table Card -->
      <div class="card table-card">
        <LoadingSkeleton v-if="adminStore.productsLoading" :rows="8" :columns="8" />
        <template v-else>
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
              <th>Product</th>
              <th>Brand</th>
              <th>Category</th>
              <th class="text-right">Price</th>
              <th class="text-center">Stock</th>
              <th class="text-center">Rating</th>
              <th class="text-center">Status</th>
              <th>Date Added</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="prod in paginatedProducts"
              :key="prod.id"
              class="table-row-hover"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :value="prod.id"
                  v-model="selectedProductIds"
                />
              </td>
              <td>
                <div class="product-cell">
                  <img
                    :src="prod.image_url || '/images/prod-sk2.jpg'"
                    :alt="prod.name"
                    class="prod-table-thumb"
                    @error="$event.target.src = '/images/prod-sk2.jpg'"
                  />
                  <div class="prod-names-wrap">
                    <div class="prod-name-video-row">
                      <span class="prod-primary-name">{{ prod.name }}</span>
                      <span v-if="prod.video_url" class="badge-prod-video" title="Texture Demonstration Video">
                        <Video :size="11" class="text-crimson" />
                        <span>Reel</span>
                      </span>
                    </div>
                    <span class="prod-sku-code">SKU: {{ getSku(prod) }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="brand-text-badge">{{ prod.brand || 'Luméa Atelier' }}</span>
              </td>
              <td>
                <span class="cat-pill-badge">{{ prod.category_name || prod.category || 'Serums' }}</span>
              </td>
              <td class="text-right">
                <div class="price-cell">
                  <strong class="curr-price">${{ Number(prod.price).toFixed(2) }}</strong>
                  <span v-if="prod.compare_at_price" class="old-price">
                    ${{ Number(prod.compare_at_price).toFixed(2) }}
                  </span>
                </div>
              </td>
              <td class="text-center">
                <strong
                  class="stock-number"
                  :class="{ 'stock-danger': (prod.stock || 0) <= 10 }"
                >
                  {{ prod.stock ?? 0 }}
                </strong>
              </td>
              <td class="text-center">
                <div class="rating-cell">
                  <Star :size="13" class="star-icon" />
                  <span class="rating-val">{{ Number(prod.rating || 4.8).toFixed(1) }}</span>
                  <span class="rating-count">({{ prod.reviews || 42 }})</span>
                </div>
              </td>
              <td class="text-center">
                <span
                  class="status-pill"
                  :class="getStockBadge(prod.stock ?? 0).class"
                >
                  {{ getStockBadge(prod.stock ?? 0).label }}
                </span>
              </td>
              <td>
                <span class="date-cell-text">
                  {{ prod.created_at ? new Date(prod.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Aug 20, 2025' }}
                </span>
              </td>
              <td class="text-right">
                <div class="action-buttons-cell">
                  <button
                    class="action-icon-btn"
                    title="Edit Product"
                    @click="openEditProduct(prod)"
                  >
                    <Edit2 :size="14" />
                  </button>
                  <button
                    class="action-icon-btn"
                    title="View Preview"
                    @click="openQuickView(prod)"
                  >
                    <Eye :size="14" />
                  </button>
                  <button
                    class="action-icon-btn text-danger"
                    title="Delete Product"
                    @click="deleteProduct(prod.id, prod.name)"
                  >
                    <Trash2 :size="14" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedProducts.length === 0">
              <td colspan="10" class="empty-table-cell">
                <p>No formulations found matching your active filter criteria.</p>
                <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Footer matching mockup -->
        <div class="pagination-footer">
          <span class="pagination-summary">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredProducts.length) }} of {{ filteredProducts.length }} products
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
              <option :value="50">50 / page</option>
            </select>
          </div>
        </div>
        </template>
      </div>
    </template>

    <!-- ========================================== -->
    <!-- VIEW 2: ADD / EDIT PRODUCT FORM           -->
    <!-- Matching Luméa Product Management Dashboard -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'editor'">
      <!-- Editor Top Hero Banner -->
      <div class="products-hero-card">
        <div class="hero-left">
          <div class="editor-breadcrumb">
            <button class="btn-back-link" @click="currentView = 'list'">
              <ArrowLeft :size="13" /> Products
            </button>
            <span class="crumb-sep">/</span>
            <span class="crumb-current">{{ editorMode === 'add' ? 'Add Product' : 'Edit Product' }}</span>
          </div>
          <h1 class="hero-heading">
            {{ editorMode === 'add' ? 'Add New Product' : `Edit: ${productForm.name}` }}
          </h1>
          <p class="hero-subtext">Add product details, images, and other information to your store.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Formulation"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">Great products</span>
              <span class="motto-line highlight">brighter tomorrows.</span>
            </div>
          </div>

          <div class="editor-top-actions">
            <button class="btn-cancel" @click="currentView = 'list'">Cancel</button>
            <button class="btn-save-product" :disabled="isSaving" @click="saveProduct">
              <Save :size="15" />
              <span>{{ isSaving ? 'Saving to Database...' : 'Save Product' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs inside Editor -->
      <div class="editor-nav-tabs">
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'basic' }"
          @click="activeEditorTab = 'basic'"
        >
          Basic Information
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'details' }"
          @click="activeEditorTab = 'details'"
        >
          Product Details
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'media' }"
          @click="activeEditorTab = 'media'"
        >
          Media & Images
        </button>
        <button
          class="editor-tab"
          :class="{ active: activeEditorTab === 'seo' }"
          @click="activeEditorTab = 'seo'"
        >
          SEO & Settings
        </button>
      </div>

      <!-- 2-Column Editor Layout matching Luméa Product Management Dashboard.png -->
      <div class="editor-grid-layout">
        <!-- Left Column: Form Cards -->
        <div class="editor-left-column">
          <!-- 1. Basic Information -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Basic Information</h3>
            <p class="editor-card-sub">Add the essential information about your product.</p>

            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label">Product Name <span class="req">*</span></label>
                <input
                  v-model="productForm.name"
                  type="text"
                  placeholder="e.g. Hydrating Toner"
                  class="atelier-input"
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">SKU <span class="req">*</span></label>
                <input
                  v-model="productForm.sku"
                  type="text"
                  placeholder="e.g. LUM-001"
                  class="atelier-input"
                  required
                />
                <span class="field-hint">A unique identifier for this product.</span>
              </div>
            </div>

            <div class="form-row-3">
              <div class="form-group">
                <label class="form-label">Brand <span class="req">*</span></label>
                <select v-model="productForm.brand" class="atelier-input">
                  <option v-for="b in brandOptions.slice(1)" :key="b" :value="b">{{ b }}</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Category <span class="req">*</span></label>
                <select v-model="productForm.category_id" class="atelier-input">
                  <option
                    v-for="cat in adminStore.categories"
                    :key="cat.id"
                    :value="cat.id"
                  >
                    {{ cat.name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Subcategory</label>
                <select v-model="productForm.subcategory" class="atelier-input">
                  <option value="Hydrating">Hydrating</option>
                  <option value="Exfoliating">Exfoliating</option>
                  <option value="Nourishing">Nourishing</option>
                  <option value="Balancing">Balancing</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <div class="label-with-counter">
                <label class="form-label">Short Description <span class="req">*</span></label>
                <span class="char-counter">{{ (productForm.short_description || '').length }}/160</span>
              </div>
              <textarea
                v-model="productForm.short_description"
                maxlength="160"
                rows="2"
                placeholder="A brief description that will appear in product listings (max 160 characters)."
                class="atelier-textarea"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Full Description <span class="req">*</span></label>
              <!-- Editorial Rich Text Toolbar -->
              <div class="rte-toolbar">
                <select class="rte-select">
                  <option>Normal</option>
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
              </div>
              <textarea
                v-model="productForm.description"
                rows="5"
                placeholder="Write a detailed description about the product, dermatological formulation, and active ingredients..."
                class="atelier-textarea rte-textarea"
              ></textarea>
            </div>
          </div>

          <!-- 2. Pricing & Inventory -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Pricing & Inventory</h3>
            <p class="editor-card-sub">Set the price, stock, and inventory details.</p>

            <div class="form-row-4">
              <div class="form-group">
                <label class="form-label">Regular Price <span class="req">*</span></label>
                <div class="input-with-prefix">
                  <span class="prefix">$</span>
                  <input
                    v-model.number="productForm.price"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    class="atelier-input-prefixed"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Sale Price</label>
                <div class="input-with-prefix">
                  <span class="prefix">$</span>
                  <input
                    v-model.number="productForm.compare_at_price"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    class="atelier-input-prefixed"
                  />
                </div>
                <span class="field-hint">Leave empty if no discount.</span>
              </div>

              <div class="form-group">
                <label class="form-label">Stock Quantity <span class="req">*</span></label>
                <input
                  v-model.number="productForm.stock"
                  type="number"
                  placeholder="0"
                  class="atelier-input"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Low Stock Alert</label>
                <input
                  v-model.number="productForm.low_stock_threshold"
                  type="number"
                  placeholder="10"
                  class="atelier-input"
                />
                <span class="field-hint">Notified when below this number.</span>
              </div>
            </div>
          </div>

          <!-- 3. Product Attributes -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Product Attributes</h3>
            <p class="editor-card-sub">Select product attributes to help customers find your product.</p>

            <!-- Skin Types -->
            <div class="form-group">
              <label class="form-label">Skin Type</label>
              <div class="checkbox-pill-grid">
                <label
                  v-for="st in skinTypesList"
                  :key="st"
                  class="checkbox-chip"
                  :class="{ checked: productForm.skin_types.includes(st) }"
                >
                  <input
                    type="checkbox"
                    :value="st"
                    :checked="productForm.skin_types.includes(st)"
                    @change="toggleSkinType(st)"
                  />
                  <span>{{ st }}</span>
                </label>
              </div>
            </div>

            <!-- Skin Concerns -->
            <div class="form-group">
              <label class="form-label">Skin Concerns</label>
              <div class="checkbox-pill-grid">
                <label
                  v-for="sc in skinConcernsList"
                  :key="sc"
                  class="checkbox-chip"
                  :class="{ checked: productForm.skin_concerns.includes(sc) }"
                >
                  <input
                    type="checkbox"
                    :value="sc"
                    :checked="productForm.skin_concerns.includes(sc)"
                    @change="toggleSkinConcern(sc)"
                  />
                  <span>{{ sc }}</span>
                </label>
              </div>
            </div>

            <div class="form-row-2">
              <div class="form-group">
                <label class="form-label">Ingredients</label>
                <input
                  v-model="productForm.ingredients"
                  type="text"
                  placeholder="e.g. Hyaluronic Acid, Niacinamide"
                  class="atelier-input"
                />
                <span class="field-hint">Separate ingredients with commas.</span>
              </div>

              <div class="form-group">
                <label class="form-label">How to Use</label>
                <input
                  v-model="productForm.how_to_use"
                  type="text"
                  placeholder="e.g. Apply small amount to clean skin morning and night."
                  class="atelier-input"
                />
              </div>
            </div>
          </div>

          <!-- 4. Product Status Radios -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Product Status</h3>
            <div class="status-radios-grid">
              <label class="status-radio-card" :class="{ selected: productForm.status === 'active' }">
                <input type="radio" value="active" v-model="productForm.status" />
                <div class="radio-texts">
                  <strong>Active</strong>
                  <span>Product will be visible on the website.</span>
                </div>
              </label>

              <label class="status-radio-card" :class="{ selected: productForm.status === 'draft' }">
                <input type="radio" value="draft" v-model="productForm.status" />
                <div class="radio-texts">
                  <strong>Draft</strong>
                  <span>Save as draft, not visible to customers.</span>
                </div>
              </label>

              <label class="status-radio-card" :class="{ selected: productForm.status === 'inactive' }">
                <input type="radio" value="inactive" v-model="productForm.status" />
                <div class="radio-texts">
                  <strong>Inactive</strong>
                  <span>Hide product from the website catalog.</span>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Right Column: Images, Live Preview, and Tips -->
        <div class="editor-right-column">
          <!-- 1. Product Images Card -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Product Images</h3>

            <div class="dropzone-box" @click="triggerImageUpload">
              <input
                type="file"
                ref="fileInputRef"
                style="display: none"
                accept="image/*"
                @change="handleProductFileUpload"
              />
              <Upload :size="24" class="upload-icon" />
              <p class="drop-text">{{ isUploading ? 'Uploading to atelier storage...' : 'Drag and drop images here or' }} <span class="browse-link">click to browse</span></p>
              <span class="drop-hint">Supports JPG, PNG, WebP (Saved directly to backend)</span>
            </div>

            <!-- Uploaded Thumbnails with Main tag and remove button -->
            <div class="images-thumb-row">
              <div
                v-for="(img, idx) in productForm.images"
                :key="idx"
                class="thumb-preview-box"
              >
                <img :src="img" alt="Product Image" class="thumb-img" />
                <span v-if="idx === 0" class="main-badge">Main</span>
                <button
                  type="button"
                  class="btn-remove-thumb"
                  @click="removeImage(idx)"
                >
                  <X :size="11" />
                </button>
              </div>
            </div>
          </div>

          <!-- Texture & Demonstration Video Card -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Texture &amp; Demonstration Video</h3>
            <p class="editor-card-sub">Upload sensory texture demonstrations or routine reels.</p>

            <div class="form-group mb-3">
              <label class="form-label">Video Title / Routine Caption</label>
              <input
                v-model="productForm.video_title"
                type="text"
                placeholder="e.g. PITERA™ Water Texture & Absorption Swatch"
                class="atelier-input"
              />
            </div>

            <!-- Video File Upload Box -->
            <div class="video-dropzone-box" @click="triggerVideoUpload">
              <input
                type="file"
                ref="videoFileInputRef"
                style="display: none"
                accept="video/mp4,video/webm,video/quicktime"
                @change="handleProductVideoUpload"
              />
              <Video :size="24" class="upload-icon text-crimson" />
              <p class="drop-text">{{ isUploadingVideo ? 'Streaming video to atelier storage...' : 'Click to Upload Texture Video (.mp4, max 50MB)' }}</p>
              <span class="drop-hint">Synced to both storefront & admin public assets</span>
            </div>

            <div class="form-group mt-3">
              <label class="form-label">Or Direct Video URL</label>
              <input
                v-model="productForm.video_url"
                type="text"
                placeholder="/videos/reel-sk2-texture.mp4"
                class="atelier-input"
              />
            </div>

            <!-- Video Player Preview -->
            <div v-if="productForm.video_url" class="product-video-preview-wrap">
              <div class="video-preview-header">
                <span class="font-medium text-xs text-charcoal">Live Video Preview</span>
                <button type="button" class="btn-clear-video" @click="productForm.video_url = ''">Remove Video</button>
              </div>
              <video
                :src="productForm.video_url"
                controls
                playsinline
                class="prod-editor-video"
              ></video>
            </div>
          </div>

          <!-- 2. Live Preview Card matching mockup -->
          <div class="card editor-card">
            <h3 class="editor-card-title">Preview</h3>
            <p class="editor-card-sub">This is how your product will appear on the website.</p>

            <div class="live-preview-box">
              <div class="preview-img-wrap">
                <img
                  :src="productForm.images[0] || '/images/prod-sk2.jpg'"
                  alt="Preview"
                  class="preview-img"
                  @error="$event.target.src = '/images/prod-sk2.jpg'"
                />
              </div>

              <div class="preview-meta">
                <span class="preview-brand">{{ productForm.brand || 'Luméa Atelier' }}</span>
                <h4 class="preview-title">{{ productForm.name || 'Hydrating Toner' }}</h4>

                <div class="preview-stars">
                  <Star :size="12" fill="#D4A373" stroke="#D4A373" />
                  <Star :size="12" fill="#D4A373" stroke="#D4A373" />
                  <Star :size="12" fill="#D4A373" stroke="#D4A373" />
                  <Star :size="12" fill="#D4A373" stroke="#D4A373" />
                  <Star :size="12" fill="#D4A373" stroke="#D4A373" />
                  <span class="preview-reviews">4.8 (124 reviews)</span>
                </div>

                <div class="preview-price-row">
                  <strong class="preview-price">${{ Number(productForm.price || 24).toFixed(2) }}</strong>
                  <span v-if="productForm.compare_at_price" class="preview-old-price">
                    ${{ Number(productForm.compare_at_price).toFixed(2) }}
                  </span>
                </div>

                <p class="preview-desc">
                  {{ productForm.short_description || 'A gentle, hydrating formulation that balances the skin and prepares it for deeper nutrient absorption.' }}
                </p>
              </div>
            </div>
          </div>

          <!-- 3. Tips Card -->
          <div class="card tips-card">
            <div class="tips-header">
              <Sparkles :size="16" class="tip-sparkle" />
              <h4>Tips for High Conversion</h4>
            </div>
            <ul class="tips-checklist">
              <li>
                <CheckCircle2 :size="14" class="check-icon" />
                <span>Use high-quality product images</span>
              </li>
              <li>
                <CheckCircle2 :size="14" class="check-icon" />
                <span>Write clear and detailed descriptions</span>
              </li>
              <li>
                <CheckCircle2 :size="14" class="check-icon" />
                <span>Set the correct category and brand</span>
              </li>
              <li>
                <CheckCircle2 :size="14" class="check-icon" />
                <span>Add relevant skin types and concerns</span>
              </li>
              <li>
                <CheckCircle2 :size="14" class="check-icon" />
                <span>Keep your product information up to date</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>

    <!-- Quick Preview Modal -->
    <div v-if="showPreviewModal && previewProduct" class="modal-backdrop" @click="showPreviewModal = false">
      <div class="preview-modal-dialog" @click.stop>
        <div class="modal-header-clean">
          <h3>Quick Formulations Inspection</h3>
          <button class="btn-close-modal" @click="showPreviewModal = false">
            <X :size="16" />
          </button>
        </div>
        <div class="modal-body-preview">
          <img :src="previewProduct.image_url" class="quick-view-img" />
          <div class="quick-view-info">
            <span class="preview-brand">{{ previewProduct.brand }}</span>
            <h2>{{ previewProduct.name }}</h2>
            <p class="quick-price">${{ Number(previewProduct.price).toFixed(2) }}</p>
            <p class="quick-desc">{{ previewProduct.description || 'Gentle atelier skincare formulation.' }}</p>
            <div class="quick-stock-stat">
              <span>Stock available: <strong>{{ previewProduct.stock }} units</strong></span>
              <span>Category: <strong>{{ previewProduct.category_name || previewProduct.category }}</strong></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Product Confirmation Dialog -->
    <ConfirmDialog
      :is-open="showDeleteConfirm"
      title="Delete Product?"
      :message="`Are you sure you want to delete '${deleteTarget?.name}' from the atelier catalog? This action cannot be undone.`"
      type="danger"
      confirm-text="Delete Product"
      cancel-text="Cancel"
      @confirm="confirmDelete"
      @cancel="showDeleteConfirm = false"
    />
  </div>
</template>

<style scoped>
.products-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.products-hero-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FFFFFF 0%, #FAF5F2 100%);
  border: 1px solid #EFE7E0;
  border-radius: 16px;
  padding: 24px 32px;
  position: relative;
  overflow: hidden;
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
  filter: drop-shadow(0 6px 12px rgba(132, 38, 27, 0.08));
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

.btn-add-product {
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
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(132, 38, 27, 0.2);
}

.btn-add-product:hover {
  background: #6D1E15;
  transform: translateY(-1px);
}

/* Status Tabs */
.status-tabs-row {
  display: flex;
  gap: 24px;
  border-bottom: 1px solid #EFE7E0;
  padding-bottom: 4px;
}

.tab-btn {
  background: transparent;
  border: none;
  font-size: 13.5px;
  font-weight: 500;
  color: #7A726C;
  padding: 8px 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: #84261B;
}

.tab-btn.active {
  color: #84261B;
  font-weight: 700;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  right: 0;
  height: 2px;
  background: #84261B;
  border-radius: 2px;
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
  flex-wrap: wrap;
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
  outline: none;
  transition: border-color 0.2s;
}

.atelier-select:focus {
  border-color: #84261B;
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
  transition: all 0.2s;
}

.btn-reset-filter:hover {
  border-color: #84261B;
  color: #84261B;
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
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

.product-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.prod-table-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  object-fit: cover;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
}

.prod-names-wrap {
  display: flex;
  flex-direction: column;
}

.prod-primary-name {
  font-weight: 600;
  color: #2D2621;
  font-size: 13px;
}

.prod-sku-code {
  font-size: 11px;
  color: #8C847E;
}

.brand-text-badge {
  font-weight: 600;
  color: #3C3530;
}

.cat-pill-badge {
  display: inline-block;
  padding: 3px 8px;
  background: #FAF5F2;
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  font-size: 11.5px;
  color: #5C544E;
}

.price-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.curr-price {
  font-weight: 700;
  color: #2D2621;
}

.old-price {
  font-size: 11px;
  color: #9C948E;
  text-decoration: line-through;
}

.stock-number {
  font-weight: 600;
  color: #2D2621;
}

.stock-danger {
  color: #C4623C;
}

.rating-cell {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.star-icon {
  color: #D4A373;
  fill: #D4A373;
}

.rating-val {
  font-weight: 700;
  color: #2D2621;
}

.rating-count {
  font-size: 11px;
  color: #8C847E;
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

.badge-low {
  background: #FAF0E8;
  color: #C4623C;
}

.badge-out {
  background: #FDF0EE;
  color: #D97768;
}

.date-cell-text {
  color: #7A726C;
  font-size: 12px;
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
  transition: all 0.2s;
}

.action-icon-btn:hover {
  border-color: #84261B;
  color: #84261B;
}

.action-icon-btn.text-danger:hover {
  border-color: #D32F2F;
  color: #D32F2F;
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

.pagination-summary {
  color: #7A726C;
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
  font-weight: 700;
}

.page-size-select {
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  padding: 6px 10px;
  background: #FFFFFF;
  font-size: 12px;
  color: #3C3530;
}

/* ========================================== */
/* EDITOR STYLES                              */
/* ========================================== */
.editor-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 6px;
}

.btn-back-link {
  background: none;
  border: none;
  color: #84261B;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0;
}

.crumb-sep {
  color: #8C847E;
}

.crumb-current {
  color: #5C544E;
}

.editor-top-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-cancel {
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  color: #5C544E;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.btn-save-product {
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
  box-shadow: 0 3px 8px rgba(132, 38, 27, 0.2);
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

.editor-grid-layout {
  display: grid;
  grid-template-columns: 1.8fr 1.2fr;
  gap: 24px;
}

.editor-left-column,
.editor-right-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.editor-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px;
}

.editor-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #2D2621;
  margin-bottom: 2px;
}

.editor-card-sub {
  font-size: 12.5px;
  color: #8C847E;
  margin-bottom: 18px;
}

.form-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #3C3530;
  margin-bottom: 6px;
}

.req {
  color: #84261B;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 16px;
}

.form-row-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.form-row-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}

.atelier-input,
.atelier-textarea {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 13px;
  color: #2D2621;
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}

.atelier-input:focus,
.atelier-textarea:focus {
  border-color: #84261B;
}

.field-hint {
  font-size: 11px;
  color: #8C847E;
  margin-top: 4px;
}

.label-with-counter {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.char-counter {
  font-size: 11px;
  color: #8C847E;
}

.rte-toolbar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
}

.rte-select {
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 11.5px;
}

.rte-divider {
  width: 1px;
  height: 16px;
  background: #EFE7E0;
}

.rte-btn {
  background: none;
  border: none;
  padding: 2px 6px;
  font-size: 12px;
  color: #5C544E;
  cursor: pointer;
  border-radius: 4px;
}

.rte-textarea {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.input-with-prefix {
  display: flex;
  align-items: center;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  background: #FFFFFF;
}

.prefix {
  padding: 0 10px;
  color: #8C847E;
  font-size: 13px;
}

.atelier-input-prefixed {
  border: none;
  outline: none;
  padding: 10px 10px 10px 0;
  width: 100%;
  font-size: 13px;
  color: #2D2621;
}

/* Checkbox Pills */
.checkbox-pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.checkbox-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  background: #FFFFFF;
  font-size: 12px;
  color: #5C544E;
  cursor: pointer;
  transition: all 0.2s;
}

.checkbox-chip.checked {
  background: #F8E9E4;
  border-color: #84261B;
  color: #84261B;
  font-weight: 600;
}

.status-radios-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.status-radio-card {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.status-radio-card.selected {
  border-color: #84261B;
  background: #FDF9F8;
}

.radio-texts {
  display: flex;
  flex-direction: column;
}

.radio-texts strong {
  font-size: 13px;
  color: #2D2621;
}

.radio-texts span {
  font-size: 11px;
  color: #8C847E;
}

/* Dropzone & Thumbnails */
.dropzone-box {
  border: 2px dashed #E5D7CD;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  background: #FAF7F4;
  cursor: pointer;
  transition: border-color 0.2s;
}

.dropzone-box:hover {
  border-color: #84261B;
}

.upload-icon {
  color: #84261B;
  margin-bottom: 8px;
}

.drop-text {
  font-size: 13px;
  color: #3C3530;
  margin-bottom: 4px;
}

.browse-link {
  color: #84261B;
  font-weight: 600;
}

.drop-hint {
  font-size: 11px;
  color: #8C847E;
}

.images-thumb-row {
  display: flex;
  gap: 10px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.thumb-preview-box {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  position: relative;
  border: 1px solid #EFE7E0;
  overflow: hidden;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-badge {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: #84261B;
  color: #FFFFFF;
  font-size: 9px;
  text-align: center;
  font-weight: 700;
  padding: 1px 0;
}

.btn-remove-thumb {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: #FFFFFF;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Product Table Video Badge */
.prod-name-video-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.badge-prod-video {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: #FFF1F0;
  border: 1px solid #FFCCC7;
  color: #84261B;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 9999px;
}

/* Texture Video Dropzone & Editor Preview */
.video-dropzone-box {
  border: 2px dashed #E5D7CD;
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  background: #FAF7F4;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 6px;
}

.video-dropzone-box:hover {
  border-color: #84261B;
  background: #FDF9F8;
}

.product-video-preview-wrap {
  margin-top: 14px;
  background: #1C1917;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #EBE1D7;
}

.video-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: #FAF6F2;
  border-bottom: 1px solid #EBE1D7;
}

.btn-clear-video {
  background: none;
  border: none;
  color: #DC2626;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}

.prod-editor-video {
  width: 100%;
  max-height: 220px;
  object-fit: contain;
  background: #000;
  display: block;
}

/* Live Preview Card */
.live-preview-box {
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  overflow: hidden;
  background: #FAF7F4;
  padding: 14px;
}

.preview-img-wrap {
  width: 100%;
  height: 180px;
  border-radius: 8px;
  overflow: hidden;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.preview-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.preview-meta {
  display: flex;
  flex-direction: column;
}

.preview-brand {
  font-size: 11px;
  text-transform: uppercase;
  color: #8C847E;
  font-weight: 600;
}

.preview-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D2621;
  margin: 2px 0 4px 0;
}

.preview-stars {
  display: flex;
  align-items: center;
  gap: 3px;
  margin-bottom: 6px;
}

.preview-reviews {
  font-size: 11px;
  color: #8C847E;
  margin-left: 4px;
}

.preview-price-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 6px;
}

.preview-price {
  font-size: 16px;
  font-weight: 800;
  color: #84261B;
}

.preview-old-price {
  font-size: 12px;
  color: #9C948E;
  text-decoration: line-through;
}

.preview-desc {
  font-size: 12px;
  color: #5C544E;
  line-height: 1.4;
}

/* Tips Card */
.tips-card {
  background: #FAF5F2;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 18px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.tip-sparkle {
  color: #C4623C;
}

.tips-header h4 {
  font-size: 13.5px;
  font-weight: 700;
  color: #2D2621;
}

.tips-checklist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tips-checklist li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #5C544E;
}

.check-icon {
  color: #2E7D32;
  flex-shrink: 0;
}

/* Quick Preview Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.preview-modal-dialog {
  background: #FFFFFF;
  border-radius: 16px;
  width: 90%;
  max-width: 560px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.modal-header-clean {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.btn-close-modal {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
}

.modal-body-preview {
  display: flex;
  gap: 20px;
}

.quick-view-img {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid #EFE7E0;
}

.quick-view-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.quick-price {
  font-size: 18px;
  font-weight: 700;
  color: #84261B;
  margin: 6px 0;
}

.quick-desc {
  font-size: 12.5px;
  color: #5C544E;
  line-height: 1.45;
  margin-bottom: 12px;
}

.quick-stock-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 11.5px;
  color: #7A726C;
  border-top: 1px solid #F5ECE6;
  padding-top: 8px;
}

@media (max-width: 1100px) {
  .editor-grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>
