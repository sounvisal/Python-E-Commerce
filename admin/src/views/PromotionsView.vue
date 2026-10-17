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
  Download,
  Calendar,
  Tag,
  Percent,
  Gift,
  Flame,
  Package,
  Truck,
  Sparkles,
  Users,
  CheckCircle2,
  X,
  Save,
  ArrowUpRight
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const searchQuery = ref('')
const selectedType = ref('All Types')
const selectedStatus = ref('All Statuses')
const activeTab = ref('all') // 'all', 'discount', 'flash', 'bundle', 'gift'
const selectedDateRange = ref('Aug 1, 2025 - Aug 31, 2025')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Selection
const selectedPromoIds = ref([])
const selectAll = ref(false)

// Modal state
const showPromoModal = ref(false)
const modalMode = ref('create')

// Promotion Form
const promoForm = reactive({
  id: null,
  name: '',
  code: '',
  type: 'Discount Code',
  discount_value: '15% OFF',
  max_uses: 1000,
  current_uses: 0,
  start_date: '2025-08-01',
  end_date: '2025-12-31',
  status: 'Active',
  is_featured: false,
  badge_color: '#84261B'
})

// 4 Top KPI Cards
const promoKpis = [
  {
    label: 'Total Promotions',
    val: '12',
    trend: '+20%',
    trendUp: true,
    icon: Tag,
    color: 'pill-rose'
  },
  {
    label: 'Active Promotions',
    val: '8',
    trend: '+33%',
    trendUp: true,
    icon: Gift,
    color: 'pill-peach'
  },
  {
    label: 'Total Discount Given',
    val: '$2,480.00',
    trend: '+18%',
    trendUp: true,
    icon: Percent,
    color: 'pill-crimson'
  },
  {
    label: 'Total Redemptions',
    val: '1,256',
    trend: '+27%',
    trendUp: true,
    icon: Users,
    color: 'pill-amber'
  }
]

// Mock Promotions Data matching Luméa Promotions Management Dashboard.png
const promotionsList = ref([
  {
    id: 1,
    name: 'New Customer Discount',
    code: 'WELCOME15',
    type: 'Discount Code',
    type_badge: 'badge-discount',
    value: '15% OFF',
    used: 428,
    limit: 1000,
    start_date: 'Aug 1, 2025',
    end_date: 'Dec 31, 2025',
    status: 'Active',
    is_featured: true,
    thumb: '15% OFF',
    thumb_type: 'badge-text'
  },
  {
    id: 2,
    name: 'Summer Glow Sale',
    code: 'SUMMER25',
    type: 'Flash Sale',
    type_badge: 'badge-flash',
    value: '25% OFF',
    used: 312,
    limit: 500,
    start_date: 'Aug 10, 2025',
    end_date: 'Aug 25, 2025',
    status: 'Active',
    is_featured: false,
    thumb: '/images/prod-sk2.jpg',
    thumb_type: 'image'
  },
  {
    id: 3,
    name: 'Free Gift with $50+',
    code: 'GIFT50',
    type: 'Free Gift',
    type_badge: 'badge-gift',
    value: 'Free Gift',
    used: 186,
    limit: 300,
    start_date: 'Aug 1, 2025',
    end_date: 'Aug 31, 2025',
    status: 'Active',
    is_featured: true,
    thumb: 'gift',
    thumb_type: 'icon'
  },
  {
    id: 4,
    name: 'Skincare Set Bundle',
    code: 'BUNDLE20',
    type: 'Bundle Deal',
    type_badge: 'badge-bundle',
    value: '20% OFF',
    used: 98,
    limit: 200,
    start_date: 'Aug 5, 2025',
    end_date: 'Sep 5, 2025',
    status: 'Active',
    is_featured: false,
    thumb: '/images/prod-sulwhasoo.jpg',
    thumb_type: 'image'
  },
  {
    id: 5,
    name: 'Clearance Sale',
    code: 'CLEAR50',
    type: 'Discount Code',
    type_badge: 'badge-discount',
    value: '50% OFF',
    used: 256,
    limit: 1000,
    start_date: 'Aug 15, 2025',
    end_date: 'Sep 15, 2025',
    status: 'Active',
    is_featured: false,
    thumb: '50% SALE',
    thumb_type: 'badge-text-red'
  },
  {
    id: 6,
    name: 'Brand Week - Anua',
    code: 'ANUA20',
    type: 'Brand Promotion',
    type_badge: 'badge-brand',
    value: '20% OFF',
    used: 143,
    limit: 500,
    start_date: 'Aug 12, 2025',
    end_date: 'Aug 26, 2025',
    status: 'Active',
    is_featured: true,
    thumb: '/images/prod-lamer.jpg',
    thumb_type: 'image'
  },
  {
    id: 7,
    name: 'Free Shipping',
    code: 'FREESHIP',
    type: 'Shipping Discount',
    type_badge: 'badge-shipping',
    value: 'Free Shipping',
    used: 621,
    limit: 1000,
    start_date: 'Aug 1, 2025',
    end_date: 'Dec 31, 2025',
    status: 'Active',
    is_featured: false,
    thumb: 'truck',
    thumb_type: 'icon'
  },
  {
    id: 8,
    name: '11.11 Mega Sale',
    code: 'MEGA1111',
    type: 'Flash Sale',
    type_badge: 'badge-flash',
    value: '30% OFF',
    used: 0,
    limit: 1000,
    start_date: 'Nov 1, 2025',
    end_date: 'Nov 11, 2025',
    status: 'Scheduled',
    is_featured: false,
    thumb: '11.11',
    thumb_type: 'badge-text-crimson'
  },
  {
    id: 9,
    name: 'VIP Exclusive',
    code: 'VIP30',
    type: 'Member Only',
    type_badge: 'badge-member',
    value: '30% OFF',
    used: 78,
    limit: 300,
    start_date: 'Aug 1, 2025',
    end_date: 'Dec 31, 2025',
    status: 'Active',
    is_featured: false,
    thumb: 'VIP',
    thumb_type: 'badge-text-gold'
  },
  {
    id: 10,
    name: 'Birthday Special',
    code: 'BDAY20',
    type: 'Special Event',
    type_badge: 'badge-event',
    value: '20% OFF',
    used: 54,
    limit: 200,
    start_date: 'Jan 1, 2025',
    end_date: 'Dec 31, 2025',
    status: 'Active',
    is_featured: false,
    thumb: 'sparkles',
    thumb_type: 'icon'
  }
])

// Filtered Promotions
const filteredPromotions = computed(() => {
  let list = [...promotionsList.value]

  if (activeTab.value === 'discount') {
    list = list.filter(p => p.type === 'Discount Code')
  } else if (activeTab.value === 'flash') {
    list = list.filter(p => p.type === 'Flash Sale')
  } else if (activeTab.value === 'bundle') {
    list = list.filter(p => p.type === 'Bundle Deal')
  } else if (activeTab.value === 'gift') {
    list = list.filter(p => p.type === 'Free Gift')
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.code.toLowerCase().includes(q)
    )
  }

  if (selectedType.value !== 'All Types') {
    list = list.filter(p => p.type === selectedType.value)
  }

  if (selectedStatus.value !== 'All Statuses') {
    list = list.filter(p => p.status === selectedStatus.value)
  }

  return list
})

const paginatedPromotions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredPromotions.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredPromotions.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedType.value = 'All Types'
  selectedStatus.value = 'All Statuses'
  activeTab.value = 'all'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedPromoIds.value = paginatedPromotions.value.map(p => p.id)
  } else {
    selectedPromoIds.value = []
  }
}

const toggleFeatured = (promo) => {
  promo.is_featured = !promo.is_featured
  adminStore.addToast(`Promotion "${promo.name}" featured state updated`, 'success')
}

// Open modal
const openCreatePromo = () => {
  modalMode.value = 'create'
  promoForm.id = null
  promoForm.name = ''
  promoForm.code = ''
  promoForm.type = 'Discount Code'
  promoForm.discount_value = '15% OFF'
  promoForm.max_uses = 1000
  promoForm.current_uses = 0
  promoForm.start_date = '2025-09-01'
  promoForm.end_date = '2025-12-31'
  promoForm.status = 'Active'
  promoForm.is_featured = false
  showPromoModal.value = true
}

const openEditPromo = (promo) => {
  modalMode.value = 'edit'
  promoForm.id = promo.id
  promoForm.name = promo.name
  promoForm.code = promo.code
  promoForm.type = promo.type
  promoForm.discount_value = promo.value
  promoForm.max_uses = promo.limit
  promoForm.current_uses = promo.used
  promoForm.start_date = '2025-08-01'
  promoForm.end_date = '2025-12-31'
  promoForm.status = promo.status
  promoForm.is_featured = promo.is_featured
  showPromoModal.value = true
}

const savePromotion = () => {
  if (!promoForm.name || !promoForm.code) {
    alert('Please enter promotion title and coupon code.')
    return
  }

  if (modalMode.value === 'create') {
    promotionsList.value.unshift({
      id: Date.now(),
      name: promoForm.name,
      code: promoForm.code.toUpperCase(),
      type: promoForm.type,
      type_badge: 'badge-discount',
      value: promoForm.discount_value,
      used: 0,
      limit: promoForm.max_uses,
      start_date: promoForm.start_date,
      end_date: promoForm.end_date,
      status: promoForm.status,
      is_featured: promoForm.is_featured,
      thumb: promoForm.discount_value,
      thumb_type: 'badge-text'
    })
    adminStore.addToast(`Campaign "${promoForm.name}" created`, 'success')
  } else {
    const idx = promotionsList.value.findIndex(p => p.id === promoForm.id)
    if (idx !== -1) {
      promotionsList.value[idx].name = promoForm.name
      promotionsList.value[idx].code = promoForm.code.toUpperCase()
      promotionsList.value[idx].value = promoForm.discount_value
      promotionsList.value[idx].type = promoForm.type
      promotionsList.value[idx].status = promoForm.status
    }
    adminStore.addToast('Promotion updated successfully', 'success')
  }
  showPromoModal.value = false
}

const deletePromo = (promo) => {
  if (confirm(`Delete promotion "${promo.name}"?`)) {
    promotionsList.value = promotionsList.value.filter(p => p.id !== promo.id)
    adminStore.addToast('Promotion removed', 'success')
  }
}
</script>

<template>
  <div class="promotions-management-page">
    <!-- Hero Banner matching Luméa Promotions Management Dashboard.png -->
    <div class="promotions-hero-card">
      <div class="hero-left">
        <span class="hero-eyebrow">PROMOTIONS</span>
        <h1 class="hero-heading">Promotions Management</h1>
        <p class="hero-subtext">Create and manage discounts, vouchers, and campaigns to boost your sales.</p>
      </div>

      <div class="hero-right">
        <div class="hero-visual-callout">
          <img
            src="/images/admin-hero-bottles.jpg"
            alt="Luméa Promotional Offerings"
            class="hero-bottles"
            @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
          />
          <div class="hero-motto">
            <span class="motto-line">Great skincare</span>
            <span class="motto-line highlight">deserves great offers.</span>
          </div>
        </div>

        <button class="btn-create-promo" @click="openCreatePromo">
          <Plus :size="16" />
          <span>Create Promotion</span>
        </button>
      </div>
    </div>

    <!-- 4 KPI Cards -->
    <div class="kpi-grid-4">
      <div
        v-for="kpi in promoKpis"
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
          placeholder="Search promotions..."
          class="atelier-input-clean"
        />
      </div>

      <div class="filter-dropdowns">
        <div class="select-wrap">
          <select v-model="selectedType" class="atelier-select">
            <option value="All Types">All Types</option>
            <option value="Discount Code">Discount Code</option>
            <option value="Flash Sale">Flash Sale</option>
            <option value="Free Gift">Free Gift</option>
            <option value="Bundle Deal">Bundle Deal</option>
          </select>
          <ChevronDown :size="14" class="select-arrow" />
        </div>

        <div class="select-wrap">
          <select v-model="selectedStatus" class="atelier-select">
            <option value="All Statuses">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Scheduled">Scheduled</option>
            <option value="Expired">Expired</option>
          </select>
          <ChevronDown :size="14" class="select-arrow" />
        </div>

        <button class="date-range-btn">
          <Calendar :size="14" />
          <span>{{ selectedDateRange }}</span>
        </button>

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
          All Promotions (12)
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'discount' }"
          @click="activeTab = 'discount'"
        >
          Discount Codes (6)
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'flash' }"
          @click="activeTab = 'flash'"
        >
          Flash Sales (3)
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'bundle' }"
          @click="activeTab = 'bundle'"
        >
          Bundle Deals (2)
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'gift' }"
          @click="activeTab = 'gift'"
        >
          Free Gift (1)
        </button>
      </div>

      <button class="btn-export-outline" @click="alert('Exporting promotions list...')">
        <Download :size="14" />
        <span>Export</span>
      </button>
    </div>

    <!-- Promotions Table Card -->
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
            <th>Promotion Name</th>
            <th>Type</th>
            <th>Discount / Value</th>
            <th>Usage</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th class="text-center">Status</th>
            <th class="text-center">Featured</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(promo, index) in paginatedPromotions"
            :key="promo.id"
            class="table-row-hover"
          >
            <td class="col-checkbox">
              <input
                type="checkbox"
                :value="promo.id"
                v-model="selectedPromoIds"
              />
            </td>
            <td class="col-order text-muted font-medium">
              {{ index + 1 }}
            </td>
            <td>
              <div class="promo-thumb-wrap">
                <span v-if="promo.thumb_type.includes('badge-text')" class="badge-text-thumb" :class="promo.thumb_type">
                  {{ promo.thumb }}
                </span>
                <span v-else-if="promo.thumb_type === 'icon'" class="icon-thumb">
                  <Gift v-if="promo.thumb === 'gift'" :size="18" />
                  <Truck v-else-if="promo.thumb === 'truck'" :size="18" />
                  <Sparkles v-else-if="promo.thumb === 'sparkles'" :size="18" />
                  <Tag v-else :size="18" />
                </span>
                <img
                  v-else
                  :src="promo.thumb"
                  alt="Promo Thumb"
                  class="promo-img-thumb"
                  @error="$event.target.src = '/images/prod-sk2.jpg'"
                />
              </div>
            </td>
            <td>
              <div class="promo-title-cell">
                <strong class="promo-name-txt">{{ promo.name }}</strong>
                <span class="promo-code-txt">{{ promo.code }}</span>
              </div>
            </td>
            <td>
              <span class="promo-type-pill" :class="promo.type_badge">
                {{ promo.type }}
              </span>
            </td>
            <td>
              <strong class="promo-val-txt">{{ promo.value }}</strong>
            </td>
            <td>
              <div class="usage-progress-cell">
                <span class="usage-counts-txt">{{ promo.used }} / {{ promo.limit }}</span>
                <div class="usage-bar-track">
                  <div
                    class="usage-bar-fill"
                    :style="{ width: `${Math.min(100, (promo.used / promo.limit) * 100)}%` }"
                  ></div>
                </div>
              </div>
            </td>
            <td>
              <span class="date-txt">{{ promo.start_date }}</span>
            </td>
            <td>
              <span class="date-txt">{{ promo.end_date }}</span>
            </td>
            <td class="text-center">
              <span
                class="status-pill"
                :class="promo.status === 'Active' ? 'badge-active' : 'badge-scheduled'"
              >
                {{ promo.status }}
              </span>
            </td>
            <td class="text-center">
              <button
                type="button"
                class="atelier-toggle-switch"
                :class="{ active: promo.is_featured }"
                @click="toggleFeatured(promo)"
              >
                <span class="toggle-slider"></span>
              </button>
            </td>
            <td class="text-right">
              <div class="action-buttons-cell">
                <button
                  class="action-icon-btn"
                  title="Edit Promotion"
                  @click="openEditPromo(promo)"
                >
                  <Edit2 :size="14" />
                </button>
                <button
                  class="action-icon-btn text-danger"
                  title="Delete Promotion"
                  @click="deletePromo(promo)"
                >
                  <Trash2 :size="14" />
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="paginatedPromotions.length === 0">
            <td colspan="12" class="empty-table-cell">
              <p>No promotions found matching your active filter.</p>
              <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination Footer -->
      <div class="pagination-footer">
        <span class="pagination-summary">
          Showing 1 to {{ paginatedPromotions.length }} of {{ filteredPromotions.length }} promotions
        </span>

        <div class="pagination-controls">
          <button class="page-nav-btn" disabled>
            <ChevronLeft :size="15" />
          </button>
          <button class="page-num-btn active">1</button>
          <button class="page-num-btn">2</button>
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

    <!-- Create / Edit Promotion Modal -->
    <div v-if="showPromoModal" class="modal-backdrop" @click="showPromoModal = false">
      <div class="promo-modal-dialog" @click.stop>
        <div class="modal-header-clean">
          <div>
            <h3 class="modal-title">{{ modalMode === 'create' ? 'Create New Promotion' : 'Edit Promotion' }}</h3>
            <p class="modal-sub">Set up promotional campaign details, discount value, and usage limits.</p>
          </div>
          <button class="btn-close-modal" @click="showPromoModal = false">
            <X :size="18" />
          </button>
        </div>

        <div class="modal-form-body">
          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Promotion Name <span class="req">*</span></label>
              <input
                v-model="promoForm.name"
                type="text"
                placeholder="e.g. Summer Glow Sale"
                class="atelier-input"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label">Coupon Code <span class="req">*</span></label>
              <input
                v-model="promoForm.code"
                type="text"
                placeholder="e.g. SUMMER25"
                class="atelier-input uppercase"
                required
              />
            </div>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Promotion Type</label>
              <select v-model="promoForm.type" class="atelier-input">
                <option value="Discount Code">Discount Code</option>
                <option value="Flash Sale">Flash Sale</option>
                <option value="Free Gift">Free Gift</option>
                <option value="Bundle Deal">Bundle Deal</option>
                <option value="Brand Promotion">Brand Promotion</option>
                <option value="Shipping Discount">Shipping Discount</option>
                <option value="Member Only">Member Only</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Discount / Benefit Value</label>
              <input
                v-model="promoForm.discount_value"
                type="text"
                placeholder="e.g. 20% OFF or Free Gift"
                class="atelier-input"
              />
            </div>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Maximum Redemptions</label>
              <input
                v-model.number="promoForm.max_uses"
                type="number"
                placeholder="1000"
                class="atelier-input"
              />
            </div>
            <div class="form-group">
              <label class="form-label">Status</label>
              <select v-model="promoForm.status" class="atelier-input">
                <option value="Active">Active</option>
                <option value="Scheduled">Scheduled</option>
                <option value="Expired">Expired</option>
              </select>
            </div>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label">Start Date</label>
              <input
                v-model="promoForm.start_date"
                type="date"
                class="atelier-input"
              />
            </div>
            <div class="form-group">
              <label class="form-label">End Date</label>
              <input
                v-model="promoForm.end_date"
                type="date"
                class="atelier-input"
              />
            </div>
          </div>

          <div class="featured-toggle-row">
            <button
              type="button"
              class="atelier-toggle-switch"
              :class="{ active: promoForm.is_featured }"
              @click="promoForm.is_featured = !promoForm.is_featured"
            >
              <span class="toggle-slider"></span>
            </button>
            <div class="toggle-texts">
              <strong>Feature on Homepage Banner</strong>
              <span>Display promotional banner on storefront entrance.</span>
            </div>
          </div>
        </div>

        <div class="modal-footer-clean">
          <button class="btn-cancel" @click="showPromoModal = false">Cancel</button>
          <button class="btn-save-modal" @click="savePromotion">
            <Save :size="15" />
            <span>{{ modalMode === 'create' ? 'Create Promotion' : 'Save Changes' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.promotions-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.promotions-hero-card {
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

.btn-create-promo {
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

.btn-create-promo:hover {
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

.date-range-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12.5px;
  color: #3C3530;
  cursor: pointer;
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

.promo-thumb-wrap {
  width: 52px;
  height: 38px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.promo-img-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #EFE7E0;
}

.badge-text-thumb {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #FAF0E8;
  color: #C4623C;
  font-size: 10.5px;
  font-weight: 800;
  border-radius: 6px;
  border: 1px solid #F1E2D8;
}

.badge-text-red {
  background: #FDF0EE;
  color: #D97768;
}

.badge-text-crimson {
  background: #84261B;
  color: #FFFFFF;
}

.badge-text-gold {
  background: #FEF7ED;
  color: #B25E00;
}

.icon-thumb {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #FAF0E8;
  color: #C4623C;
  border-radius: 6px;
  border: 1px solid #F1E2D8;
}

.promo-title-cell {
  display: flex;
  flex-direction: column;
}

.promo-name-txt {
  font-size: 13px;
  color: #2D2621;
}

.promo-code-txt {
  font-size: 11px;
  color: #84261B;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.promo-type-pill {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.badge-discount { background: #FEF7ED; color: #B25E00; }
.badge-flash { background: #FDF0EE; color: #D97768; }
.badge-gift { background: #F3E8FF; color: #6B21A8; }
.badge-bundle { background: #E0F2FE; color: #0369A1; }
.badge-brand { background: #E8F5E9; color: #2E7D32; }
.badge-shipping { background: #FAF0E8; color: #C4623C; }
.badge-member { background: #F8E9E4; color: #84261B; }
.badge-event { background: #F5ECE6; color: #5C544E; }

.promo-val-txt {
  font-size: 13px;
  color: #2D2621;
}

.usage-progress-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100px;
}

.usage-counts-txt {
  font-size: 11px;
  color: #5C544E;
}

.usage-bar-track {
  height: 6px;
  background: #FAF0E8;
  border-radius: 99px;
  overflow: hidden;
}

.usage-bar-fill {
  height: 100%;
  background: #84261B;
  border-radius: 99px;
}

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-active { background: #E8F5E9; color: #2E7D32; }
.badge-scheduled { background: #E0F2FE; color: #0369A1; }

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

.atelier-toggle-switch.active { background: #84261B; }
.toggle-slider {
  display: block;
  width: 16px;
  height: 16px;
  background: #FFFFFF;
  border-radius: 50%;
  transition: transform 0.2s;
}
.atelier-toggle-switch.active .toggle-slider { transform: translateX(18px); }

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
.action-icon-btn.text-danger:hover { border-color: #D32F2F; color: #D32F2F; }

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

/* Modal */
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

.promo-modal-dialog {
  background: #FFFFFF;
  border-radius: 16px;
  width: 90%;
  max-width: 560px;
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

.modal-title { font-size: 17px; font-weight: 700; color: #2D2621; }
.modal-sub { font-size: 12px; color: #8C847E; margin-top: 2px; }
.btn-close-modal { background: none; border: none; color: #8C847E; cursor: pointer; }

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

.form-label { font-size: 12px; font-weight: 600; color: #3C3530; }
.req { color: #84261B; }

.atelier-input {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 12.5px;
  color: #2D2621;
  outline: none;
}

.atelier-input.uppercase { text-transform: uppercase; }
.atelier-input:focus { border-color: #84261B; }

.featured-toggle-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-texts { display: flex; flex-direction: column; }
.toggle-texts strong { font-size: 12.5px; color: #2D2621; }
.toggle-texts span { font-size: 11px; color: #8C847E; }

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
