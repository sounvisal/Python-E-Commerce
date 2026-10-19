<script setup>
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
import {
  Package,
  Clock,
  CheckCircle2,
  DollarSign,
  Ban,
  Search,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Calendar,
  Download,
  Plus,
  Eye,
  Edit2,
  MoreHorizontal,
  Lightbulb,
  ExternalLink,
  Settings as SettingsIcon,
  Check,
  XCircle,
  Truck,
  RotateCcw,
  ArrowRight,
  Info,
  ShieldCheck,
  CreditCard
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const returns = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedStatusFilter = ref('all')
const selectedReasonFilter = ref('all')
const selectedDateRange = ref('all')
const activeTab = ref('all') // 'all', 'pending', 'approved', 'refunded', 'rejected'
const selectedReturns = ref([])
const activeDropdown = ref(null)

// Inspection Modal
const inspectingReturn = ref(null)
const isUpdating = ref(false)

// Process Return Modal
const showProcessModal = ref(false)
const processForm = ref({
  order_number: '',
  customer_name: '',
  customer_email: '',
  product_name: 'Brightening Face Serum',
  product_variant: '30ml · 1 item',
  price: 28.00,
  reason: 'Changed Mind',
  resolution: 'Full Refund'
})

onMounted(async () => {
  await fetchReturns()
})

async function fetchReturns() {
  loading.value = true
  try {
    const res = await apiClient.get('/returns')
    if (res.data?.success) {
      returns.value = res.data.data
    }
  } catch (err) {
    console.error('Failed to load return requests:', err)
  } finally {
    loading.value = false
  }
}

// Filtered Returns
const filteredReturns = computed(() => {
  let list = returns.value || []

  // Tab filter
  if (activeTab.value !== 'all') {
    list = list.filter(r => (r.status || '').toLowerCase() === activeTab.value.toLowerCase())
  }

  // Status dropdown filter
  if (selectedStatusFilter.value !== 'all') {
    list = list.filter(r => (r.status || '').toLowerCase() === selectedStatusFilter.value.toLowerCase())
  }

  // Reason dropdown filter
  if (selectedReasonFilter.value !== 'all') {
    list = list.filter(r => (r.reason || '').toLowerCase().includes(selectedReasonFilter.value.toLowerCase()))
  }

  // Search filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(r =>
      (r.request_number || '').toLowerCase().includes(q) ||
      (r.order_number || '').toLowerCase().includes(q) ||
      (r.customer_name || '').toLowerCase().includes(q) ||
      (r.customer_email || '').toLowerCase().includes(q) ||
      (r.product_name || '').toLowerCase().includes(q) ||
      (r.reason || '').toLowerCase().includes(q)
    )
  }

  return list
})

// Counts for Tabs
const countAll = computed(() => returns.value.length || 48)
const countPending = computed(() => returns.value.filter(r => (r.status || '').toLowerCase() === 'pending').length || 12)
const countApproved = computed(() => returns.value.filter(r => (r.status || '').toLowerCase() === 'approved').length || 32)
const countRefunded = computed(() => returns.value.filter(r => (r.status || '').toLowerCase() === 'refunded').length || 3)
const countRejected = computed(() => returns.value.filter(r => (r.status || '').toLowerCase() === 'rejected').length || 1)

// Multi-select
const allSelected = computed(() => {
  return filteredReturns.value.length > 0 && selectedReturns.value.length === filteredReturns.value.length
})

function toggleSelectAll() {
  if (allSelected.value) {
    selectedReturns.value = []
  } else {
    selectedReturns.value = filteredReturns.value.map(r => r.id)
  }
}

function toggleSelectReturn(id) {
  const idx = selectedReturns.value.indexOf(id)
  if (idx > -1) {
    selectedReturns.value.splice(idx, 1)
  } else {
    selectedReturns.value.push(id)
  }
}

// Status Updates
async function updateStatus(returnItem, newStatus) {
  activeDropdown.value = null
  isUpdating.value = true
  try {
    const res = await apiClient.patch(`/returns/${returnItem.id}/status`, {
      status: newStatus,
      note: `Status updated to ${newStatus} from Atelier Console`
    })
    if (res.data?.success) {
      adminStore.addToast(`Return #${returnItem.request_number} updated to ${newStatus}`, 'success')
      returnItem.status = newStatus
      if (inspectingReturn.value?.id === returnItem.id) {
        inspectingReturn.value.status = newStatus
      }
    }
  } catch (err) {
    adminStore.addToast('Failed to update return status', 'error')
  } finally {
    isUpdating.value = false
  }
}

// Process new return
async function submitProcessReturn() {
  try {
    const payload = {
      order_number: processForm.value.order_number || '#10029',
      customer_name: processForm.value.customer_name || 'Walk-in Patron',
      customer_email: processForm.value.customer_email || 'patron@example.com',
      product_name: processForm.value.product_name,
      product_variant: processForm.value.product_variant,
      price: processForm.value.price,
      reason: processForm.value.reason,
      resolution: processForm.value.resolution,
      description: 'Handled via Atelier Admin Console quick process action.'
    }
    const res = await apiClient.post('/returns', payload)
    if (res.data?.success) {
      adminStore.addToast('Return request processed and recorded in database', 'success')
      showProcessModal.value = false
      await fetchReturns()
    }
  } catch (err) {
    adminStore.addToast('Failed to process return', 'error')
  }
}

// Export CSV
function exportReturnsCSV() {
  const items = filteredReturns.value
  if (!items || items.length === 0) return
  const headers = ['Request #', 'Order #', 'Customer', 'Product', 'Variant', 'Price', 'Reason', 'Status', 'Date']
  const rows = items.map(r => [
    `"${r.request_number}"`,
    `"${r.order_number}"`,
    `"${r.customer_name}"`,
    `"${r.product_name}"`,
    `"${r.product_variant}"`,
    r.price,
    `"${r.reason}"`,
    r.status,
    `"${r.submitted_date}"`
  ])
  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `lumea_returns_${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  adminStore.addToast('Returns exported (CSV)', 'success')
}

function formatRequestedDate(dateStr) {
  if (!dateStr) return { date: 'Aug 28, 2025', time: '10:24 AM' }
  if (dateStr.includes('T')) {
    const [d, t] = dateStr.split('T')
    return { date: d, time: t.substring(0, 5) }
  }
  if (dateStr.includes('·')) {
    const [d, t] = dateStr.split('·')
    return { date: d.trim(), time: t.trim() }
  }
  const parts = dateStr.trim().split(' ')
  if (parts.length >= 3 && parts[2].includes(',')) {
    const date = `${parts[0]} ${parts[1]} ${parts[2]}`
    const time = parts.slice(3).join(' ') || '10:24 AM'
    return { date, time }
  }
  if (parts.length >= 4) {
    const date = `${parts[0]} ${parts[1]} ${parts[2]}`
    const time = parts.slice(3).join(' ')
    return { date, time }
  }
  return { date: dateStr, time: '' }
}
</script>

<template>
  <div class="returns-page">
      <!-- BREADCRUMB -->
      <div class="breadcrumb-bar">
        <span class="crumb-parent">Service</span>
        <span class="crumb-sep">></span>
        <span class="crumb-current">Returns</span>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">Returns Management</h1>
          <p class="hero-subtitle">Process and manage product returns, refunds, and exchanges with ease.</p>
        </div>

        <div class="hero-art-side">
          <img src="/images/admin-hero-bottles.jpg" alt="Luméa Returns Atelier" class="hero-art-img" />
          <div class="hero-quote">
            <span class="quote-line-1">Hassle-free returns.</span>
            <span class="quote-line-2">Happier customers.</span>
          </div>
          <button class="btn-process-top" @click="showProcessModal = true">
            <Plus class="w-4 h-4 mr-1" />
            <span>Process Return</span>
          </button>
        </div>
      </div>

      <!-- 5 KPI METRICS CARDS -->
      <div class="kpi-grid">
        <!-- 1. Total Return Requests -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Package class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">48</span>
              <span class="kpi-badge positive">↗ +12%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Total Return Requests</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 2. Pending Review -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Clock class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">12</span>
              <span class="kpi-badge positive">↗ +33%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Pending Review</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 3. Approved -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <CheckCircle2 class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">32</span>
              <span class="kpi-badge positive">↗ +8%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Approved</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 4. Refunded -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <DollarSign class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">3</span>
              <span class="kpi-badge positive">↗ +50%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Refunded</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 5. Rejected -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Ban class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">1</span>
              <span class="kpi-badge negative">↘ -50%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Rejected</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN SPLIT: RETURNS TABLE (LEFT) + REASONS & RECENT (RIGHT) -->
      <div class="returns-split-layout">
        <!-- LEFT: FILTERS + TABS + TABLE -->
        <div class="returns-main-pane">
          <!-- Top Filter Bar -->
          <div class="filter-toolbar">
            <div class="search-input-wrap">
              <Search class="search-icon w-4 h-4" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search returns, order numbers, customers..."
                class="search-input"
              />
            </div>

            <div class="filter-field">
              <label class="filter-label">Status</label>
              <select v-model="selectedStatusFilter" class="filter-select">
                <option value="all">All Statuses</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="refunded">Refunded</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>

            <div class="filter-field">
              <label class="filter-label">Return Reason</label>
              <select v-model="selectedReasonFilter" class="filter-select">
                <option value="all">All Reasons</option>
                <option value="Changed Mind">Changed Mind</option>
                <option value="Product Not Suitable">Product Not Suitable</option>
                <option value="Damaged Item">Damaged Item</option>
                <option value="Skin Irritation">Skin Irritation</option>
                <option value="Wrong Item">Wrong Item</option>
                <option value="Expired Product">Expired Product</option>
                <option value="Defective Item">Defective Item</option>
              </select>
            </div>

            <div class="filter-field">
              <label class="filter-label">Date Range</label>
              <div class="date-select-wrap">
                <Calendar class="w-3.5 h-3.5 text-taupe mr-1" />
                <select v-model="selectedDateRange" class="filter-select date-select">
                  <option value="all">All Time</option>
                  <option value="30d">Last 30 Days</option>
                  <option value="90d">Last 90 Days</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Secondary Tabs Bar + Export -->
          <div class="tabs-export-bar">
            <div class="returns-tabs">
              <button
                class="tab-pill"
                :class="{ active: activeTab === 'all' }"
                @click="activeTab = 'all'"
              >
                All Returns ({{ countAll }})
              </button>
              <button
                class="tab-pill"
                :class="{ active: activeTab === 'pending' }"
                @click="activeTab = 'pending'"
              >
                Pending ({{ countPending }})
              </button>
              <button
                class="tab-pill"
                :class="{ active: activeTab === 'approved' }"
                @click="activeTab = 'approved'"
              >
                Approved ({{ countApproved }})
              </button>
              <button
                class="tab-pill"
                :class="{ active: activeTab === 'refunded' }"
                @click="activeTab = 'refunded'"
              >
                Refunded ({{ countRefunded }})
              </button>
              <button
                class="tab-pill"
                :class="{ active: activeTab === 'rejected' }"
                @click="activeTab = 'rejected'"
              >
                Rejected ({{ countRejected }})
              </button>
            </div>

            <button class="btn-export-outline" @click="exportReturnsCSV">
              <Download class="w-3.5 h-3.5 mr-1" />
              <span>Export</span>
            </button>
          </div>

          <!-- Returns Table -->
          <div class="table-card">
            <table class="returns-table">
              <thead>
                <tr>
                  <th class="th-check">
                    <input type="checkbox" :checked="allSelected" @change="toggleSelectAll" class="custom-checkbox" />
                  </th>
                  <th class="th-num">#</th>
                  <th class="th-item">Return Information</th>
                  <th class="th-customer">Customer</th>
                  <th class="th-order">Order #</th>
                  <th class="th-reason">Reason</th>
                  <th class="th-status">Status</th>
                  <th class="th-date">Requested Date</th>
                  <th class="th-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="9" class="td-loading">
                    <div class="spinner"></div>
                    <span>Loading return requests...</span>
                  </td>
                </tr>

                <tr v-else-if="filteredReturns.length === 0">
                  <td colspan="9" class="td-empty">
                    <RotateCcw class="w-10 h-10 text-taupe mx-auto mb-2 opacity-50" />
                    <p class="font-serif text-lg text-charcoal">No return requests found</p>
                    <p class="text-xs text-taupe">Adjust filter criteria to view records.</p>
                  </td>
                </tr>

                <tr
                  v-for="(item, index) in filteredReturns"
                  :key="item.id"
                  :class="{ 'row-selected': selectedReturns.includes(item.id) }"
                >
                  <!-- Checkbox -->
                  <td class="td-check">
                    <input
                      type="checkbox"
                      :checked="selectedReturns.includes(item.id)"
                      @change="toggleSelectReturn(item.id)"
                      class="custom-checkbox"
                    />
                  </td>

                  <!-- Number -->
                  <td class="td-num">{{ index + 1 }}</td>

                  <!-- Product Return Info -->
                  <td class="td-item">
                    <div class="return-prod-block">
                      <img :src="item.product_image || '/images/prod-sk2.jpg'" :alt="item.product_name" class="return-thumb" />
                      <div class="return-prod-details">
                        <span class="prod-title">{{ item.product_name }}</span>
                        <span class="prod-variant">{{ item.product_variant || '30ml · 1 item' }}</span>
                        <span class="prod-price">${{ Number(item.price || 28).toFixed(2) }}</span>
                      </div>
                    </div>
                  </td>

                  <!-- Customer Info -->
                  <td class="td-customer">
                    <div class="customer-cell">
                      <img :src="item.customer_avatar || '/images/avatar-sreynich.jpg'" :alt="item.customer_name" class="cust-avatar" />
                      <div class="cust-details">
                        <span class="cust-name">{{ item.customer_name }}</span>
                        <span class="cust-email">{{ item.customer_email }}</span>
                      </div>
                    </div>
                  </td>

                  <!-- Order Number -->
                  <td class="td-order">
                    <div class="order-cell">
                      <span class="order-num">{{ item.order_number }}</span>
                      <span class="order-date">{{ item.submitted_date?.split(' ')[0] || 'Aug 15, 2025' }}</span>
                    </div>
                  </td>

                  <!-- Reason -->
                  <td class="td-reason">
                    <span class="reason-text">{{ item.reason }}</span>
                  </td>

                  <!-- Status -->
                  <td class="td-status">
                    <span
                      class="badge-status"
                      :class="{
                        'status-pending': (item.status || '').toLowerCase() === 'pending',
                        'status-approved': (item.status || '').toLowerCase() === 'approved',
                        'status-refunded': (item.status || '').toLowerCase() === 'refunded',
                        'status-rejected': (item.status || '').toLowerCase() === 'rejected'
                      }"
                    >
                      {{ item.status }}
                    </span>
                  </td>

                  <!-- Requested Date -->
                  <td class="td-date">
                    <div class="date-cell">
                      <span class="date-main">{{ formatRequestedDate(item.submitted_date).date }}</span>
                      <span class="date-sub">{{ formatRequestedDate(item.submitted_date).time }}</span>
                    </div>
                  </td>

                  <!-- Actions -->
                  <td class="td-actions">
                    <div class="actions-group">
                      <button class="action-btn" title="Inspect Return" @click="inspectingReturn = item">
                        <Eye class="w-3.5 h-3.5" />
                      </button>
                      <button class="action-btn" title="Advance Status" @click="inspectingReturn = item">
                        <Edit2 class="w-3.5 h-3.5" />
                      </button>

                      <div class="dropdown-wrap">
                        <button class="action-btn" title="More" @click="activeDropdown = activeDropdown === item.id ? null : item.id">
                          <MoreHorizontal class="w-3.5 h-3.5" />
                        </button>

                        <div v-if="activeDropdown === item.id" class="dropdown-menu">
                          <button
                            v-if="(item.status || '').toLowerCase() !== 'approved'"
                            class="dropdown-item text-green"
                            @click="updateStatus(item, 'approved')"
                          >
                            <CheckCircle2 class="w-4 h-4 mr-2" />
                            <span>Approve Return</span>
                          </button>
                          <button
                            v-if="(item.status || '').toLowerCase() !== 'refunded'"
                            class="dropdown-item text-blue"
                            @click="updateStatus(item, 'refunded')"
                          >
                            <DollarSign class="w-4 h-4 mr-2" />
                            <span>Disburse Refund</span>
                          </button>
                          <button
                            v-if="(item.status || '').toLowerCase() !== 'rejected'"
                            class="dropdown-item text-red"
                            @click="updateStatus(item, 'rejected')"
                          >
                            <XCircle class="w-4 h-4 mr-2" />
                            <span>Reject Return</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Table Footer -->
            <div class="table-footer">
              <span class="footer-count">Showing 1 to {{ filteredReturns.length }} of 48 returns</span>
              <div class="pagination-bar">
                <button class="btn-page-nav" disabled aria-label="Previous page"><ChevronLeft :size="13" /></button>
                <button class="btn-page-num active">1</button>
                <button class="btn-page-num">2</button>
                <button class="btn-page-num">3</button>
                <button class="btn-page-num">4</button>
                <button class="btn-page-num">5</button>
                <button class="btn-page-nav" aria-label="Next page"><ChevronRight :size="13" /></button>
                <span class="page-size-label">
                  <span>10 / page</span>
                  <ChevronDown :size="12" class="page-size-arrow" />
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT: SIDEBAR (DONUT + RECENT + POLICY) -->
        <div class="returns-sidebar">
          <!-- 1. RETURN REASONS DONUT WIDGET -->
          <div class="widget-card">
            <h3 class="widget-title">Return Reasons</h3>

            <div class="donut-chart-container">
              <svg viewBox="0 0 160 160" class="donut-svg">
                <!-- Changed Mind 31% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#84261B" stroke-width="18"
                  stroke-dasharray="113 251" stroke-dashoffset="0" />
                <!-- Product Not Suitable 27% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#C0392B" stroke-width="18"
                  stroke-dasharray="98 266" stroke-dashoffset="-113" />
                <!-- Damaged Item 19% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#D35400" stroke-width="18"
                  stroke-dasharray="69 295" stroke-dashoffset="-211" />
                <!-- Skin Irritation 10% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#E67E22" stroke-width="18"
                  stroke-dasharray="36 328" stroke-dashoffset="-280" />
                <!-- Wrong Item 8% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#F39C12" stroke-width="18"
                  stroke-dasharray="29 335" stroke-dashoffset="-316" />
                <!-- Expired 4% & Other 1% -->
                <circle cx="80" cy="80" r="58" fill="none" stroke="#D6CBC2" stroke-width="18"
                  stroke-dasharray="18 346" stroke-dashoffset="-345" />
              </svg>

              <div class="donut-center-text">
                <span class="donut-num">48</span>
                <span class="donut-label">Returns</span>
              </div>
            </div>

            <!-- Legend List -->
            <div class="donut-legend-list">
              <div class="legend-row">
                <span class="legend-dot" style="background: #84261B;"></span>
                <span class="legend-name">Changed Mind</span>
                <span class="legend-pct">31%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #C0392B;"></span>
                <span class="legend-name">Product Not Suitable</span>
                <span class="legend-pct">27%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #D35400;"></span>
                <span class="legend-name">Damaged Item</span>
                <span class="legend-pct">19%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #E67E22;"></span>
                <span class="legend-name">Skin Irritation</span>
                <span class="legend-pct">10%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #F39C12;"></span>
                <span class="legend-name">Wrong Item</span>
                <span class="legend-pct">8%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #B5ABA4;"></span>
                <span class="legend-name">Expired Product</span>
                <span class="legend-pct">4%</span>
              </div>
              <div class="legend-row">
                <span class="legend-dot" style="background: #E8DFD8;"></span>
                <span class="legend-name">Other</span>
                <span class="legend-pct">1%</span>
              </div>
            </div>
          </div>

          <!-- 2. RECENT RETURN REQUESTS WIDGET -->
          <div class="widget-card">
            <h3 class="widget-title">Recent Return Requests</h3>

            <div class="recent-list">
              <div class="recent-item">
                <img src="/images/prod-sk2.jpg" alt="Serum" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Brightening Face Serum</span>
                  <div class="recent-meta">
                    <span class="recent-order">#10028 ·</span>
                    <span class="recent-status-pill pending">Pending</span>
                  </div>
                  <span class="recent-date">Aug 28, 2025</span>
                </div>
              </div>

              <div class="recent-item">
                <img src="/images/prod-laneige.jpg" alt="Moisturizer" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Hydrating Moisturizer</span>
                  <div class="recent-meta">
                    <span class="recent-order">#10024 ·</span>
                    <span class="recent-status-pill approved">Approved</span>
                  </div>
                  <span class="recent-date">Aug 27, 2025</span>
                </div>
              </div>

              <div class="recent-item">
                <img src="/images/prod-anua-cleanser.jpg" alt="Cleanser" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Gentle Cleanser</span>
                  <div class="recent-meta">
                    <span class="recent-order">#10021 ·</span>
                    <span class="recent-status-pill pending">Pending</span>
                  </div>
                  <span class="recent-date">Aug 26, 2025</span>
                </div>
              </div>
            </div>

            <div class="widget-footer-action">
              <button class="link-action" @click="activeTab = 'all'">
                <span>View All Returns</span>
                <ArrowRight class="w-3.5 h-3.5 ml-1" />
              </button>
            </div>
          </div>

          <!-- 3. RETURN POLICY REMINDER -->
          <div class="widget-card policy-card">
            <div class="policy-header">
              <Info class="w-5 h-5 text-crimson mr-2" />
              <h4 class="policy-title">Return Policy Reminder</h4>
            </div>
            <p class="policy-body">
              Standard return window is 30 days from the delivery date. Items must be unused and in original packaging.
            </p>
            <a href="javascript:void(0)" class="policy-link">
              <span>View Full Return Policy</span>
              <ArrowRight class="w-3.5 h-3.5 ml-1" />
            </a>
          </div>
        </div>
      </div>

      <!-- BOTTOM BANNER -->
      <div class="bottom-action-banner">
        <div class="bottom-left">
          <Lightbulb class="w-5 h-5 text-crimson mr-3 flex-shrink-0" />
          <div>
            <h4 class="bottom-title">Provide a smooth return experience</h4>
            <p class="bottom-subtitle">Quick and transparent returns build customer trust and encourage repeat purchases.</p>
          </div>
        </div>
        <button class="btn-settings-bottom" @click="alert('Manage Return Settings...')">
          <SettingsIcon class="w-4 h-4 mr-1.5" />
          <span>Manage Return Settings</span>
        </button>
      </div>

      <!-- INSPECT RETURN MODAL -->
      <div v-if="inspectingReturn" class="modal-backdrop" @click.self="inspectingReturn = null">
        <div class="modal-card">
          <div class="modal-header">
            <div>
              <span class="modal-label">Return Request Details</span>
              <h2 class="modal-title">{{ inspectingReturn.request_number }}</h2>
            </div>
            <button class="modal-close" @click="inspectingReturn = null">×</button>
          </div>

          <div class="modal-body">
            <!-- Customer & Order Details Grid -->
            <div class="inspect-details-grid">
              <div class="detail-box">
                <span class="box-lbl">Order Number</span>
                <span class="box-val font-semibold">{{ inspectingReturn.order_number }}</span>
              </div>
              <div class="detail-box">
                <span class="box-lbl">Customer Name</span>
                <span class="box-val">{{ inspectingReturn.customer_name }}</span>
              </div>
              <div class="detail-box">
                <span class="box-lbl">Resolution</span>
                <span class="box-val text-crimson font-medium">{{ inspectingReturn.resolution || 'Full Refund' }}</span>
              </div>
              <div class="detail-box">
                <span class="box-lbl">Current Status</span>
                <span class="badge-status inline-block mt-0.5" :class="`status-${(inspectingReturn.status || 'pending').toLowerCase()}`">
                  {{ inspectingReturn.status }}
                </span>
              </div>
            </div>

            <!-- Product Row -->
            <div class="inspect-prod-row mt-4">
              <img :src="inspectingReturn.product_image || '/images/prod-sk2.jpg'" class="inspect-thumb" />
              <div>
                <span class="font-medium text-sm text-charcoal block">{{ inspectingReturn.product_name }}</span>
                <span class="text-xs text-taupe block">{{ inspectingReturn.product_variant }}</span>
                <span class="text-sm font-semibold text-crimson">${{ Number(inspectingReturn.price || 28).toFixed(2) }}</span>
              </div>
            </div>

            <!-- Customer Reason & Description -->
            <div class="inspect-reason-box mt-4">
              <span class="box-lbl">Return Reason: <strong>{{ inspectingReturn.reason }}</strong></span>
              <p class="text-xs text-charcoal mt-1">{{ inspectingReturn.description || 'No additional comments provided by customer.' }}</p>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="inspectingReturn = null">Close</button>
            <button
              v-if="(inspectingReturn.status || '').toLowerCase() !== 'approved'"
              class="btn-approve"
              @click="updateStatus(inspectingReturn, 'approved')"
            >
              Approve Return
            </button>
            <button
              v-if="(inspectingReturn.status || '').toLowerCase() !== 'refunded'"
              class="btn-refund"
              @click="updateStatus(inspectingReturn, 'refunded')"
            >
              Disburse Refund
            </button>
            <button
              v-if="(inspectingReturn.status || '').toLowerCase() !== 'rejected'"
              class="btn-reject"
              @click="updateStatus(inspectingReturn, 'rejected')"
            >
              Reject
            </button>
          </div>
        </div>
      </div>

      <!-- PROCESS NEW RETURN MODAL -->
      <div v-if="showProcessModal" class="modal-backdrop" @click.self="showProcessModal = false">
        <div class="modal-card">
          <div class="modal-header">
            <div>
              <span class="modal-label">Concierge Workflow</span>
              <h2 class="modal-title">Process In-Store / Direct Return</h2>
            </div>
            <button class="modal-close" @click="showProcessModal = false">×</button>
          </div>

          <div class="modal-body">
            <div class="form-group">
              <label class="form-label">Order Number</label>
              <input v-model="processForm.order_number" type="text" placeholder="#10030" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Customer Name</label>
              <input v-model="processForm.customer_name" type="text" placeholder="Sreypov Chhum" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Customer Email</label>
              <input v-model="processForm.customer_email" type="email" placeholder="customer@example.com" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Reason</label>
              <select v-model="processForm.reason" class="form-select">
                <option value="Changed Mind">Changed Mind</option>
                <option value="Product Not Suitable">Product Not Suitable</option>
                <option value="Damaged Item">Damaged Item</option>
                <option value="Skin Irritation">Skin Irritation</option>
                <option value="Wrong Item">Wrong Item</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Resolution Preference</label>
              <select v-model="processForm.resolution" class="form-select">
                <option value="Full Refund">Full Refund</option>
                <option value="Store Credit">Store Credit</option>
                <option value="Replacement Formulation">Replacement Formulation</option>
              </select>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="showProcessModal = false">Cancel</button>
            <button class="btn-primary" @click="submitProcessReturn">Submit & Record</button>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.returns-page {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Breadcrumb */
.breadcrumb-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #8C827A;
}

.crumb-parent { color: #8C827A; }
.crumb-sep { color: #B5ABA4; }
.crumb-current { color: #2D2422; font-weight: 500; }

/* Hero Banner */
.hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FBF8F5 0%, #F5ECE6 100%);
  border: 1px solid #EBE1D7;
  border-radius: 12px;
  padding: 1.5rem 2rem;
  min-height: 120px;
}

.hero-content {
  max-width: 550px;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2rem;
  font-weight: 600;
  color: #84261B;
  margin: 0 0 0.35rem 0;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 0.875rem;
  color: #6E635E;
  margin: 0;
  line-height: 1.45;
}

.hero-art-side {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.hero-art-img {
  width: 90px;
  height: 65px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(45, 36, 34, 0.08);
}

.hero-quote {
  display: flex;
  flex-direction: column;
}

.quote-line-1 {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.125rem;
  font-weight: 600;
  color: #84261B;
}

.quote-line-2 {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.125rem;
  font-weight: 600;
  color: #84261B;
}

.btn-process-top {
  display: inline-flex;
  align-items: center;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(132, 38, 27, 0.2);
}

/* 5 KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}

.kpi-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.125rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.kpi-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-icon-wrap.rose-soft {
  background: #FCECE9;
}

.text-crimson { color: #84261B; }

.kpi-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.kpi-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.kpi-num {
  font-size: 1.35rem;
  font-weight: 700;
  color: #2D2422;
}

.kpi-badge {
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.15rem 0.4rem;
  border-radius: 12px;
}

.kpi-badge.positive {
  background: #EAF5EE;
  color: #2D8A4E;
}

.kpi-badge.negative {
  background: #FDECEB;
  color: #C0392B;
}

.kpi-sub {
  display: flex;
  flex-direction: column;
  margin-top: 0.15rem;
}

.kpi-label {
  font-size: 0.75rem;
  color: #8C827A;
  font-weight: 500;
}

.kpi-compare {
  font-size: 0.6875rem;
  color: #B5ABA4;
}

/* Split Layout */
.returns-split-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1.25rem;
  align-items: flex-start;
}

.returns-main-pane {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Filter Toolbar */
.filter-toolbar {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 0.875rem 1rem;
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1fr;
  gap: 0.875rem;
  align-items: flex-end;
}

.search-input-wrap {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #8C827A;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 38px;
  padding: 0 0.75rem 0 2.25rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.8125rem;
  background: #FAF6F2;
  color: #2D2422;
  outline: none;
  box-sizing: border-box;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.filter-label {
  font-size: 0.6875rem;
  color: #8C827A;
  text-transform: uppercase;
  font-weight: 600;
}

.filter-select {
  width: 100%;
  height: 38px;
  padding: 0 1.75rem 0 0.75rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.8125rem;
  background: #FFFFFF url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238C827A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 0.75rem center;
  appearance: none;
  color: #2D2422;
  outline: none;
  box-sizing: border-box;
  cursor: pointer;
}

.date-select-wrap {
  display: flex;
  align-items: center;
  height: 38px;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0 0.5rem;
  background: #FFFFFF;
  box-sizing: border-box;
}

.date-select {
  border: none;
  background: transparent;
  height: 100%;
  padding-left: 0.25rem;
}

/* Tabs & Export Bar */
.tabs-export-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.returns-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-pill {
  border: none;
  background: none;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #6E635E;
  padding: 0.45rem 0.85rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-pill.active {
  background: #84261B;
  color: #FFFFFF;
  font-weight: 600;
}

.btn-export-outline {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.45rem 0.85rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  color: #2D2422;
  cursor: pointer;
}

/* Returns Table */
.table-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  overflow: hidden;
}

.returns-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
}

.returns-table th {
  background: #FAF6F2;
  padding: 0.75rem 0.875rem;
  font-weight: 600;
  color: #6E635E;
  text-align: left;
  border-bottom: 1px solid #EBE1D7;
  font-size: 0.75rem;
}

.returns-table td {
  padding: 0.875rem;
  border-bottom: 1px solid #F5ECE6;
  color: #2D2422;
  vertical-align: middle;
}

.custom-checkbox {
  accent-color: #84261B;
  width: 15px;
  height: 15px;
  cursor: pointer;
}

.th-num, .td-num {
  width: 30px;
  color: #8C827A;
  white-space: nowrap;
}

.return-prod-block {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  max-width: 220px;
}

.return-thumb {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EBE1D7;
  flex-shrink: 0;
}

.return-prod-details {
  display: flex;
  flex-direction: column;
}

.prod-title {
  font-weight: 600;
  color: #2D2422;
  font-size: 0.8125rem;
}

.prod-variant {
  font-size: 0.6875rem;
  color: #8C827A;
}

.prod-price {
  font-size: 0.75rem;
  font-weight: 600;
  color: #84261B;
  margin-top: 0.15rem;
}

.customer-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cust-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EBE1D7;
}

.cust-details {
  display: flex;
  flex-direction: column;
}

.cust-name {
  font-weight: 500;
  color: #2D2422;
  font-size: 0.8125rem;
  white-space: nowrap;
}

.cust-email {
  font-size: 0.6875rem;
  color: #8C827A;
  white-space: nowrap;
}

.order-cell {
  display: flex;
  flex-direction: column;
}

.th-order, .td-order {
  white-space: nowrap;
}

.order-num {
  font-weight: 600;
  color: #2D2422;
  white-space: nowrap;
}

.order-date {
  font-size: 0.6875rem;
  color: #8C827A;
  white-space: nowrap;
}

.th-reason, .td-reason {
  min-width: 130px;
}

.reason-text {
  font-weight: 500;
  color: #2D2422;
  white-space: nowrap;
}

/* Status Badges */
.th-status, .td-status {
  white-space: nowrap;
}

.badge-status {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
  white-space: nowrap;
}

.status-pending { background: #FEF6E7; color: #B57914; }
.status-approved { background: #EAF5EE; color: #2D8A4E; }
.status-refunded { background: #EBF4FE; color: #2980B9; }
.status-rejected { background: #FDECEB; color: #C0392B; }

.th-date, .td-date {
  white-space: nowrap;
}

.date-cell {
  display: flex;
  flex-direction: column;
}

.date-main {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #2D2422;
  white-space: nowrap;
}

.date-sub {
  font-size: 0.6875rem;
  color: #8C827A;
  white-space: nowrap;
}

.th-actions, .td-actions {
  white-space: nowrap;
  width: 110px;
}

/* Actions */
.actions-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #EBE1D7;
  background: #FFFFFF;
  border-radius: 6px;
  color: #6E635E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.action-btn:hover {
  background: #FAF6F2;
  color: #84261B;
  border-color: #84261B;
}

.dropdown-wrap {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(45, 36, 34, 0.12);
  z-index: 50;
  min-width: 160px;
  padding: 0.35rem 0;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.85rem;
  background: none;
  border: none;
  font-size: 0.75rem;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover { background: #FAF6F2; }
.text-green { color: #2D8A4E; }
.text-blue { color: #2980B9; }
.text-red { color: #C0392B; }

.table-footer {
  padding: 0.875rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #EBE1D7;
  background: #FAF6F2;
}

.footer-count {
  font-size: 0.75rem;
  color: #6E635E;
}

.pagination-bar {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.btn-page-nav, .btn-page-num {
  min-width: 28px;
  height: 28px;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #6E635E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.btn-page-num.active {
  background: #84261B;
  color: #FFFFFF;
  border-color: #84261B;
}

.page-size-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: #6E635E;
  margin-left: 0.5rem;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
}

.page-size-arrow {
  color: #6E635E;
}

/* SIDEBAR WIDGETS */
.returns-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.widget-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.25rem;
}

.widget-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0 0 1rem 0;
}

/* Donut */
.donut-chart-container {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 0 auto 1.25rem auto;
}

.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-center-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.donut-num {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2D2422;
  line-height: 1;
}

.donut-label {
  font-size: 0.6875rem;
  color: #8C827A;
}

.donut-legend-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.legend-row {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.legend-name {
  color: #6E635E;
  flex: 1;
}

.legend-pct {
  font-weight: 600;
  color: #2D2422;
}

/* Recent */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.recent-item {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.recent-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EBE1D7;
}

.recent-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.recent-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

.recent-meta {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.15rem;
}

.recent-order {
  font-size: 0.6875rem;
  color: #8C827A;
}

.recent-status-pill {
  font-size: 0.625rem;
  padding: 0.1rem 0.4rem;
  border-radius: 8px;
  font-weight: 600;
}

.recent-status-pill.pending { background: #FEF6E7; color: #B57914; }
.recent-status-pill.approved { background: #EAF5EE; color: #2D8A4E; }

.recent-date {
  font-size: 0.625rem;
  color: #B5ABA4;
}

.widget-footer-action {
  margin-top: 1rem;
  border-top: 1px solid #F5ECE6;
  padding-top: 0.75rem;
  text-align: center;
}

.link-action {
  background: none;
  border: none;
  color: #84261B;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

/* Policy Card */
.policy-card {
  background: #FAF6F2;
}

.policy-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.policy-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.policy-body {
  font-size: 0.75rem;
  color: #6E635E;
  line-height: 1.45;
  margin: 0 0 0.75rem 0;
}

.policy-link {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  color: #84261B;
  font-weight: 600;
  text-decoration: none;
}

/* Bottom Action Banner */
.bottom-action-banner {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bottom-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.bottom-subtitle {
  font-size: 0.75rem;
  color: #6E635E;
  margin: 0.15rem 0 0 0;
}

.btn-settings-bottom {
  display: inline-flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  padding: 0.55rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #2D2422;
  cursor: pointer;
}

/* Modals */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(30, 24, 22, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1.5rem;
}

.modal-card {
  background: #FFFFFF;
  border-radius: 12px;
  width: 100%;
  max-width: 520px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid #EBE1D7;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #F5ECE6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF6F2;
}

.modal-label {
  font-size: 0.6875rem;
  color: #84261B;
  text-transform: uppercase;
  font-weight: 600;
}

.modal-title {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.25rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0.15rem 0 0 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #8C827A;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.inspect-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.875rem;
}

.detail-box {
  background: #FAF6F2;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #EBE1D7;
}

.box-lbl {
  font-size: 0.6875rem;
  color: #8C827A;
  display: block;
}

.box-val {
  font-size: 0.8125rem;
  color: #2D2422;
  margin-top: 0.15rem;
  display: block;
}

.inspect-prod-row {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  padding: 0.75rem;
  border-radius: 8px;
}

.inspect-thumb {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  object-fit: cover;
}

.inspect-reason-box {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 6px;
  padding: 0.75rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #F5ECE6;
  background: #FAF6F2;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-secondary {
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  color: #6E635E;
  cursor: pointer;
}

.btn-primary {
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-approve {
  background: #2D8A4E;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-refund {
  background: #2980B9;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-reject {
  background: #C0392B;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

@media (max-width: 1200px) {
  .returns-split-layout {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
