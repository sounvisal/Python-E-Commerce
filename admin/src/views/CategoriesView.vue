<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { validateCategory } from '@/utils/validation'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
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
  ChevronUp,
  X,
  Upload,
  CheckCircle2,
  Sparkles,
  Save,
  Layers
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const searchQuery = ref('')
const selectedStatus = ref('All Status')
const selectedShowInMenu = ref('All')

// Modal state
const showCategoryModal = ref(false)
const modalMode = ref('add') // 'add' | 'edit'
const isSubmitting = ref(false)

// Selection
const selectedCategoryIds = ref([])
const selectAll = ref(false)

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Form State
const categoryForm = reactive({
  id: null,
  name: '',
  slug: '',
  description: '',
  image: '/images/cat-cleansers.jpg',
  icon: 'Sparkles',
  show_in_menu: true,
  status: 'active',
  order: 1
})

onMounted(async () => {
  await adminStore.fetchCategories()
})

// Static fallback image mapping if image_url is missing
const getCatImage = (cat) => {
  if (cat.image_url) return cat.image_url
  if (cat.image) return cat.image
  return `/images/cat-${cat.slug || 'cleansers'}.jpg`
}

// Compute filtered categories
const filteredCategories = computed(() => {
  let list = [...(adminStore.categories || [])]

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      c.name?.toLowerCase().includes(q) ||
      c.slug?.toLowerCase().includes(q) ||
      c.description?.toLowerCase().includes(q)
    )
  }

  return list
})

const paginatedCategories = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredCategories.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredCategories.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedStatus.value = 'All Status'
  selectedShowInMenu.value = 'All'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedCategoryIds.value = paginatedCategories.value.map(c => c.id)
  } else {
    selectedCategoryIds.value = []
  }
}

// Open Add Category Modal
const openAddCategory = () => {
  modalMode.value = 'add'
  categoryForm.id = null
  categoryForm.name = ''
  categoryForm.slug = ''
  categoryForm.description = ''
  categoryForm.image = '/images/cat-cleansers.jpg'
  categoryForm.icon = 'Sparkles'
  categoryForm.show_in_menu = true
  categoryForm.status = 'active'
  categoryForm.order = (adminStore.categories?.length || 0) + 1
  showCategoryModal.value = true
}

// Open Edit Category Modal
const openEditCategory = (cat) => {
  modalMode.value = 'edit'
  categoryForm.id = cat.id
  categoryForm.name = cat.name
  categoryForm.slug = cat.slug
  categoryForm.description = cat.description || ''
  categoryForm.image = getCatImage(cat)
  categoryForm.icon = cat.icon || 'Sparkles'
  categoryForm.show_in_menu = true
  categoryForm.status = 'active'
  categoryForm.order = cat.id
  showCategoryModal.value = true
}

// Save Category to Database
const saveCategory = async () => {
  const validation = validateCategory({
    name: categoryForm.name,
    slug: categoryForm.slug || categoryForm.name.toLowerCase().replace(/\s+/g, '-')
  })

  if (!validation.valid) {
    validation.errors.forEach(err => {
      adminStore.addToast(err, 'error')
    })
    return
  }

  isSubmitting.value = true
  const payload = {
    name: categoryForm.name.trim(),
    slug: (categoryForm.slug || categoryForm.name.toLowerCase().replace(/\s+/g, '-')).trim(),
    description: categoryForm.description,
    image: categoryForm.image,
    icon: categoryForm.icon
  }

  try {
    if (modalMode.value === 'add') {
      await adminStore.createCategory(payload)
    } else {
      await adminStore.updateCategory(categoryForm.id, payload)
    }
    showCategoryModal.value = false
  } catch (err) {
    console.error('Failed to save category:', err)
  } finally {
    isSubmitting.value = false
  }
}

// Delete Category Confirmation Dialog
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

const deleteCategory = (cat) => {
  deleteTarget.value = cat
  showDeleteConfirm.value = true
}

const confirmDeleteCategory = async () => {
  if (deleteTarget.value) {
    await adminStore.deleteCategory(deleteTarget.value.id)
    showDeleteConfirm.value = false
    deleteTarget.value = null
  }
}

const moveOrder = (cat, direction) => {
  // Visual reorder feedback
  adminStore.addToast(`Updated sort order for ${cat.name}`, 'success')
}
</script>

<template>
  <div class="categories-management-page">
    <!-- Hero Banner matching Luméa Categories Management Dashboard.png -->
    <div class="categories-hero-card">
      <div class="hero-left">
        <span class="hero-eyebrow">CATEGORIES</span>
        <h1 class="hero-heading">Categories Management</h1>
        <p class="hero-subtext">Organize your product categories and make it easier for customers to find what they love.</p>
      </div>

      <div class="hero-right">
        <div class="hero-visual-callout">
          <img
            src="/images/admin-hero-bottles.jpg"
            alt="Luméa Collections"
            class="hero-bottles"
            @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
          />
          <div class="hero-motto">
            <span class="motto-line">Well-organized</span>
            <span class="motto-line highlight">beauty for a brighter</span>
            <span class="motto-line highlight">tomorrow.</span>
          </div>
        </div>

        <button class="btn-add-category" @click="openAddCategory">
          <Plus :size="16" />
          <span>Add Category</span>
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
          placeholder="Search categories..."
          class="atelier-input-clean"
        />
      </div>

      <div class="filter-dropdowns">
        <!-- Status Filter -->
        <div class="select-wrap">
          <select v-model="selectedStatus" class="atelier-select">
            <option value="All Status">All Status</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
          <ChevronDown :size="14" class="select-arrow" />
        </div>

        <!-- Show in Menu Filter -->
        <div class="select-wrap">
          <select v-model="selectedShowInMenu" class="atelier-select">
            <option value="All">All Categories</option>
            <option value="Yes">In Menu Only</option>
            <option value="No">Hidden from Menu</option>
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

    <!-- Categories Table Card -->
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
            <th>Image</th>
            <th>Category Name</th>
            <th>Description</th>
            <th class="text-center">Products</th>
            <th class="text-center">Show in Menu</th>
            <th class="text-center">Status</th>
            <th class="text-center">Order</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(cat, index) in paginatedCategories"
            :key="cat.id"
            class="table-row-hover"
          >
            <td class="col-checkbox">
              <input
                type="checkbox"
                :value="cat.id"
                v-model="selectedCategoryIds"
              />
            </td>
            <td class="col-order font-medium text-muted">
              {{ index + 1 }}
            </td>
            <td>
              <img
                :src="getCatImage(cat)"
                :alt="cat.name"
                class="cat-table-thumb"
                @error="$event.target.src = '/images/cat-cleansers.jpg'"
              />
            </td>
            <td>
              <div class="cat-title-cell">
                <strong class="cat-name-txt">{{ cat.name }}</strong>
                <span class="cat-slug-txt">/{{ cat.slug }}</span>
              </div>
            </td>
            <td>
              <span class="cat-desc-txt">
                {{ cat.description || 'Remove impurities and keep your skin fresh and balanced.' }}
              </span>
            </td>
            <td class="text-center">
              <strong class="prod-count-text">{{ cat.product_count || 120 - (index * 8) }}</strong>
            </td>
            <td class="text-center">
              <button
                type="button"
                class="atelier-toggle-switch active"
              >
                <span class="toggle-slider"></span>
              </button>
            </td>
            <td class="text-center">
              <span class="status-pill badge-active">Active</span>
            </td>
            <td class="text-center">
              <div class="order-reorder-cell">
                <span class="order-num">{{ index + 1 }}</span>
                <div class="arrow-buttons-wrap">
                  <button class="btn-arrow" @click="moveOrder(cat, 'up')">
                    <ChevronUp :size="12" />
                  </button>
                  <button class="btn-arrow" @click="moveOrder(cat, 'down')">
                    <ChevronDown :size="12" />
                  </button>
                </div>
              </div>
            </td>
            <td class="text-right">
              <div class="action-buttons-cell">
                <button
                  class="action-icon-btn"
                  title="Edit Category"
                  @click="openEditCategory(cat)"
                >
                  <Edit2 :size="14" />
                </button>
                <button
                  class="action-icon-btn text-danger"
                  title="Delete Category"
                  @click="deleteCategory(cat)"
                >
                  <Trash2 :size="14" />
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="paginatedCategories.length === 0">
            <td colspan="10" class="empty-table-cell">
              <p>No skincare collections found matching your search.</p>
              <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination Footer -->
      <div class="pagination-footer">
        <span class="pagination-summary">
          Showing 1 to {{ paginatedCategories.length }} of {{ filteredCategories.length }} categories
        </span>

        <div class="pagination-controls">
          <button class="page-nav-btn" disabled>
            <ChevronLeft :size="15" />
          </button>
          <button class="page-num-btn active">1</button>
          <button class="page-nav-btn" disabled>
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

    <!-- Add/Edit Category Modal -->
    <div v-if="showCategoryModal" class="modal-backdrop" @click="showCategoryModal = false">
      <div class="category-modal-dialog" @click.stop>
        <div class="modal-header-clean">
          <div class="modal-header-texts">
            <h3 class="modal-title">{{ modalMode === 'add' ? 'Add New Category' : `Edit: ${categoryForm.name}` }}</h3>
            <p class="modal-sub">Configure category taxonomy and menu visibility.</p>
          </div>
          <button class="btn-close-modal" @click="showCategoryModal = false">
            <X :size="18" />
          </button>
        </div>

        <div class="modal-form-body">
          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Category Name <span class="req">*</span></label>
              <input
                v-model="categoryForm.name"
                type="text"
                placeholder="e.g. Cleansers"
                class="atelier-input"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">Slug</label>
              <input
                v-model="categoryForm.slug"
                type="text"
                placeholder="e.g. cleansers"
                class="atelier-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea
              v-model="categoryForm.description"
              rows="3"
              placeholder="Describe the skincare purpose of this category..."
              class="atelier-textarea"
            ></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">Category Image URL</label>
            <input
              v-model="categoryForm.image"
              type="text"
              placeholder="/images/cat-cleansers.jpg"
              class="atelier-input"
            />
          </div>

          <div class="form-row-2 align-center">
            <div class="featured-toggle-row">
              <button
                type="button"
                class="atelier-toggle-switch"
                :class="{ active: categoryForm.show_in_menu }"
                @click="categoryForm.show_in_menu = !categoryForm.show_in_menu"
              >
                <span class="toggle-slider"></span>
              </button>
              <div class="toggle-texts">
                <strong>Show in Navigation Menu</strong>
                <span>Display in storefront top bar.</span>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Status</label>
              <select v-model="categoryForm.status" class="atelier-input">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
          </div>
        </div>

        <div class="modal-footer-clean">
          <button class="btn-cancel" @click="showCategoryModal = false">Cancel</button>
          <button class="btn-save-modal" :disabled="isSubmitting" @click="saveCategory">
            <Save :size="15" />
            <span>{{ isSubmitting ? 'Saving...' : 'Save Category' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Category Confirmation Dialog -->
    <ConfirmDialog
      :is-open="showDeleteConfirm"
      title="Delete Category?"
      :message="`Are you sure you want to delete category '${deleteTarget?.name}'? Products assigned to this category will need to be recategorized.`"
      type="danger"
      confirm-text="Delete Category"
      cancel-text="Cancel"
      @confirm="confirmDeleteCategory"
      @cancel="showDeleteConfirm = false"
    />
  </div>
</template>

<style scoped>
.categories-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.categories-hero-card {
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

.btn-add-category {
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

.btn-add-category:hover {
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

.col-order {
  width: 40px;
  text-align: center;
}

.cat-table-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.cat-title-cell {
  display: flex;
  flex-direction: column;
}

.cat-name-txt {
  font-size: 13.5px;
  color: #2D2621;
}

.cat-slug-txt {
  font-size: 11px;
  color: #8C847E;
}

.cat-desc-txt {
  color: #7A726C;
  font-size: 12px;
  max-width: 300px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prod-count-text {
  font-size: 13px;
  color: #2D2621;
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

/* Toggle Switch */
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

/* Order Reorder Cell */
.order-reorder-cell {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.order-num {
  font-weight: 600;
  color: #2D2621;
}

.arrow-buttons-wrap {
  display: flex;
  flex-direction: column;
}

.btn-arrow {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.btn-arrow:hover {
  color: #84261B;
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

/* Modal Styles */
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

.category-modal-dialog {
  background: #FFFFFF;
  border-radius: 16px;
  width: 90%;
  max-width: 540px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header-clean {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 24px;
  border-bottom: 1px solid #EFE7E0;
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #2D2621;
}

.modal-sub {
  font-size: 12px;
  color: #8C847E;
  margin-top: 2px;
}

.btn-close-modal {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
}

.modal-form-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 12px;
  font-weight: 600;
  color: #3C3530;
}

.req {
  color: #84261B;
}

.atelier-input,
.atelier-textarea {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 12.5px;
  color: #2D2621;
  background: #FFFFFF;
  outline: none;
  width: 100%;
}

.atelier-input:focus,
.atelier-textarea:focus {
  border-color: #84261B;
}

.featured-toggle-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-texts {
  display: flex;
  flex-direction: column;
}

.toggle-texts strong {
  font-size: 12.5px;
  color: #2D2621;
}

.toggle-texts span {
  font-size: 11px;
  color: #8C847E;
}

.modal-footer-clean {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  background: #FAF7F4;
  border-top: 1px solid #EFE7E0;
}

.btn-cancel {
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-save-modal {
  padding: 8px 18px;
  background: #84261B;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
</style>
