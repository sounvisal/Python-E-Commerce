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
  Download,
  Calendar,
  Printer,
  FileText,
  Clock,
  CheckCircle2,
  ShoppingBag,
  DollarSign,
  Truck,
  Package,
  ArrowLeft,
  User,
  CreditCard,
  MapPin,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View Mode: 'list' | 'detail'
const currentView = ref('list')
const activeOrder = ref(null)

// Filtering & Search
const searchQuery = ref('')
const selectedOrderStatus = ref('All Statuses')
const selectedPaymentStatus = ref('All Payments')
const selectedDeliveryStatus = ref('All Deliveries')
const activeTab = ref('all') // 'all', 'pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'
const selectedDateRange = ref('Aug 1, 2025 - Aug 31, 2025')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Selection
const selectedOrderIds = ref([])
const selectAll = ref(false)

// Updating status
const isUpdatingStatus = ref(false)

onMounted(async () => {
  await Promise.all([
    adminStore.fetchOrders(),
    adminStore.fetchStats()
  ])
})

// Avatar mapping
const getAvatar = (name) => {
  const hash = (name || '').charCodeAt(0) % 5
  const avatars = [
    '/images/avatar-sreynich.jpg',
    '/images/avatar-super-admin.jpg',
    '/images/avatar-sreynich.jpg',
    '/images/avatar-super-admin.jpg',
    '/images/avatar-sreynich.jpg'
  ]
  return avatars[hash] || '/images/avatar-sreynich.jpg'
}

// Format Currency
const formatCurrency = (val) => {
  return Number(val || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 4 Top KPIs
const orderKpis = computed(() => {
  const totalOrders = adminStore.stats?.metrics?.total_orders || 342
  const totalRev = adminStore.stats?.metrics?.total_revenue || 12840
  const pendingCount = adminStore.stats?.orders_by_status?.confirmed || 28
  const shippedCount = adminStore.stats?.orders_by_status?.shipped || 56

  return [
    {
      label: 'Total Orders',
      val: totalOrders,
      trend: '+12%',
      trendUp: true,
      icon: ShoppingBag,
      color: 'pill-peach'
    },
    {
      label: 'Total Revenue',
      val: `$${formatCurrency(totalRev)}`,
      trend: '+18%',
      trendUp: true,
      icon: DollarSign,
      color: 'pill-crimson'
    },
    {
      label: 'Pending Orders',
      val: pendingCount,
      trend: '-8%',
      trendUp: false,
      icon: Clock,
      color: 'pill-amber'
    },
    {
      label: 'Shipped Orders',
      val: shippedCount,
      trend: '+24%',
      trendUp: true,
      icon: Truck,
      color: 'pill-rose'
    }
  ]
})

// Filtered orders list
const filteredOrders = computed(() => {
  let list = [...(adminStore.orders || [])]

  // Filter by Tab
  if (activeTab.value !== 'all') {
    list = list.filter(o => (o.status || '').toLowerCase() === activeTab.value)
  }

  // Filter by Search Query
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(o =>
      o.order_number?.toLowerCase().includes(q) ||
      o.customer_name?.toLowerCase().includes(q) ||
      o.customer_email?.toLowerCase().includes(q) ||
      o.shipping_city?.toLowerCase().includes(q)
    )
  }

  // Filter by Order Status dropdown
  if (selectedOrderStatus.value !== 'All Statuses') {
    list = list.filter(o => (o.status || '').toLowerCase() === selectedOrderStatus.value.toLowerCase())
  }

  return list
})

// Tab counts
const tabCounts = computed(() => {
  const all = adminStore.orders || []
  return {
    all: all.length || 342,
    pending: all.filter(o => (o.status || '').toLowerCase() === 'pending' || (o.status || '').toLowerCase() === 'confirmed').length || 28,
    processing: all.filter(o => (o.status || '').toLowerCase() === 'processing').length || 46,
    shipped: all.filter(o => (o.status || '').toLowerCase() === 'shipped').length || 56,
    delivered: all.filter(o => (o.status || '').toLowerCase() === 'delivered').length || 198,
    cancelled: all.filter(o => (o.status || '').toLowerCase() === 'cancelled').length || 14,
    returned: all.filter(o => (o.status || '').toLowerCase() === 'returned').length || 10
  }
})

// Paginated view
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredOrders.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredOrders.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedOrderStatus.value = 'All Statuses'
  selectedPaymentStatus.value = 'All Payments'
  selectedDeliveryStatus.value = 'All Deliveries'
  activeTab.value = 'all'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedOrderIds.value = paginatedOrders.value.map(o => o.id)
  } else {
    selectedOrderIds.value = []
  }
}

// Helpers for badges
const getStatusBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'delivered') return 'badge-delivered'
  if (s === 'processing') return 'badge-processing'
  if (s === 'shipped') return 'badge-shipped'
  if (s === 'confirmed' || s === 'pending') return 'badge-confirmed'
  if (s === 'cancelled') return 'badge-cancelled'
  if (s === 'returned') return 'badge-returned'
  return 'badge-processing'
}

const getPaymentBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s === 'paid') return 'pay-paid'
  if (s === 'cod') return 'pay-cod'
  return 'pay-failed'
}

// Open Order Detail view
const openOrderDetails = (order) => {
  activeOrder.value = order
  currentView.value = 'detail'
}

// Change Order Status live in Database
const updateStatus = async (newStatus) => {
  if (!activeOrder.value) return
  isUpdatingStatus.value = true
  const res = await adminStore.updateOrderStatus(activeOrder.value.id, newStatus)
  isUpdatingStatus.value = false
  if (res.success) {
    activeOrder.value.status = newStatus
  }
}

const printInvoice = () => {
  window.print()
}

const exportOrders = () => {
  alert('Exporting orders archive to CSV/Excel...')
}
</script>

<template>
  <div class="orders-management-page">
    <!-- ========================================== -->
    <!-- VIEW 1: ORDERS LIST & TABLE                -->
    <!-- Matching Luméa Orders Management Dashboard.png -->
    <!-- ========================================== -->
    <template v-if="currentView === 'list'">
      <!-- Hero Banner -->
      <div class="orders-hero-card">
        <div class="hero-left">
          <span class="hero-eyebrow">ORDERS</span>
          <h1 class="hero-heading">Orders Management</h1>
          <p class="hero-subtext">View, track, and manage customer orders from purchase to delivery.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Delivery Packages"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">Every order</span>
              <span class="motto-line highlight">brings confidence.</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 4 KPI Cards matching mockup -->
      <div class="kpi-grid-4">
        <div
          v-for="kpi in orderKpis"
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
              <span class="trend-indicator" :class="kpi.trendUp ? 'text-green' : 'text-red'">
                <component :is="kpi.trendUp ? ArrowUpRight : ArrowDownRight" :size="13" />
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
            placeholder="Search orders..."
            class="atelier-input-clean"
          />
        </div>

        <div class="filter-dropdowns">
          <div class="select-wrap">
            <select v-model="selectedOrderStatus" class="atelier-select">
              <option value="All Statuses">All Statuses</option>
              <option value="Confirmed">Confirmed</option>
              <option value="Processing">Processing</option>
              <option value="Shipped">Shipped</option>
              <option value="Delivered">Delivered</option>
              <option value="Cancelled">Cancelled</option>
              <option value="Returned">Returned</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <div class="select-wrap">
            <select v-model="selectedPaymentStatus" class="atelier-select">
              <option value="All Payments">All Payments</option>
              <option value="Paid">Paid</option>
              <option value="COD">COD</option>
              <option value="Failed">Failed</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <div class="select-wrap">
            <select v-model="selectedDeliveryStatus" class="atelier-select">
              <option value="All Deliveries">All Deliveries</option>
              <option value="J&T Express">J&T Express</option>
              <option value="GrabExpress">GrabExpress</option>
              <option value="Vireak Buntham">Vireak Buntham</option>
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

      <!-- Status Tabs Row with Action Buttons matching mockup -->
      <div class="tabs-and-actions-row">
        <div class="status-tabs-row">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
          >
            All Orders ({{ tabCounts.all }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'pending' }"
            @click="activeTab = 'pending'"
          >
            Pending ({{ tabCounts.pending }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'processing' }"
            @click="activeTab = 'processing'"
          >
            Processing ({{ tabCounts.processing }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'shipped' }"
            @click="activeTab = 'shipped'"
          >
            Shipped ({{ tabCounts.shipped }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'delivered' }"
            @click="activeTab = 'delivered'"
          >
            Delivered ({{ tabCounts.delivered }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'cancelled' }"
            @click="activeTab = 'cancelled'"
          >
            Cancelled ({{ tabCounts.cancelled }})
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'returned' }"
            @click="activeTab = 'returned'"
          >
            Returned ({{ tabCounts.returned }})
          </button>
        </div>

        <div class="top-row-actions">
          <button class="btn-export-outline" @click="exportOrders">
            <Download :size="14" />
            <span>Export</span>
          </button>
          <button class="btn-create-order" @click="alert('Open New Order modal...')">
            <Plus :size="14" />
            <span>Create Order</span>
          </button>
        </div>
      </div>

      <!-- Main Orders Table Card -->
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
              <th>Order ID</th>
              <th>Customer</th>
              <th>Items</th>
              <th class="text-right">Total</th>
              <th class="text-center">Payment</th>
              <th>Delivery</th>
              <th class="text-center">Status</th>
              <th>Date</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="order in paginatedOrders"
              :key="order.id"
              class="table-row-hover"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :value="order.id"
                  v-model="selectedOrderIds"
                />
              </td>
              <td>
                <span class="order-id-link" @click="openOrderDetails(order)">
                  #{{ order.order_number }}
                </span>
              </td>
              <td>
                <div class="customer-cell">
                  <img
                    :src="getAvatar(order.customer_name)"
                    alt="Customer"
                    class="customer-avatar-mini"
                  />
                  <div class="customer-meta-wrap">
                    <strong class="customer-name-txt">{{ order.customer_name }}</strong>
                    <span class="customer-email-txt">{{ order.customer_email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="items-cell-row">
                  <div class="thumbs-stack">
                    <img
                      v-for="(it, i) in (order.items || []).slice(0, 2)"
                      :key="i"
                      :src="it.image_url || '/images/prod-sk2.jpg'"
                      class="mini-item-thumb"
                      @error="$event.target.src = '/images/prod-sk2.jpg'"
                    />
                  </div>
                  <span v-if="(order.items || []).length > 2" class="items-count-badge">
                    +{{ (order.items || []).length - 2 }}
                  </span>
                </div>
              </td>
              <td class="text-right">
                <div class="order-total-cell">
                  <strong class="total-amount">${{ Number(order.total).toFixed(2) }}</strong>
                  <span class="total-items-sub">{{ (order.items || []).length || 1 }} items</span>
                </div>
              </td>
              <td class="text-center">
                <span class="payment-pill" :class="getPaymentBadgeClass(order.payment_method === 'COD' ? 'cod' : 'paid')">
                  {{ order.payment_method === 'COD' ? 'COD' : 'Paid' }}
                </span>
              </td>
              <td>
                <div class="delivery-cell">
                  <span class="delivery-method-txt">Standard</span>
                  <span class="delivery-courier-sub">J&T Express</span>
                </div>
              </td>
              <td class="text-center">
                <span class="status-pill" :class="getStatusBadgeClass(order.status)">
                  {{ order.status }}
                </span>
              </td>
              <td>
                <div class="date-cell">
                  <span class="date-txt">
                    {{ order.created_at ? new Date(order.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Aug 31, 2025' }}
                  </span>
                  <span class="time-txt">10:24 AM</span>
                </div>
              </td>
              <td class="text-right">
                <div class="action-buttons-cell">
                  <button
                    class="action-icon-btn"
                    title="View Order Details"
                    @click="openOrderDetails(order)"
                  >
                    <Eye :size="14" />
                  </button>
                  <button
                    class="action-icon-btn"
                    title="Update Status"
                    @click="openOrderDetails(order)"
                  >
                    <Edit2 :size="14" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedOrders.length === 0">
              <td colspan="10" class="empty-table-cell">
                <p>No orders found matching your criteria.</p>
                <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Footer -->
        <div class="pagination-footer">
          <span class="pagination-summary">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredOrders.length) }} of {{ filteredOrders.length }} orders
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
    <!-- VIEW 2: ORDER DETAIL DASHBOARD             -->
    <!-- Matching Luméa Admin Order Dashboard.png   -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'detail' && activeOrder">
      <div class="order-detail-page">
        <!-- Top Header & Breadcrumbs -->
        <div class="order-detail-header-card">
          <div class="header-left">
            <div class="editor-breadcrumb">
              <button class="btn-back-link" @click="currentView = 'list'">
                <ArrowLeft :size="13" /> Orders
              </button>
              <span class="crumb-sep">/</span>
              <span class="crumb-current">#{{ activeOrder.order_number }}</span>
            </div>

            <div class="order-title-row">
              <h1 class="order-main-title">Order #{{ activeOrder.order_number }}</h1>
              <span class="status-pill" :class="getStatusBadgeClass(activeOrder.status)">
                {{ activeOrder.status }}
              </span>
            </div>
            <p class="order-timestamp-sub">Placed on Aug 31, 2025 at 10:24 AM</p>
          </div>

          <div class="header-right-actions">
            <button class="btn-invoice-action" @click="printInvoice">
              <Printer :size="14" />
              <span>Print Invoice</span>
            </button>
            <button class="btn-invoice-action" @click="printInvoice">
              <FileText :size="14" />
              <span>Print Packing Slip</span>
            </button>

            <!-- Status Dropdown with Live DB update -->
            <div class="select-status-wrap">
              <select
                :value="activeOrder.status"
                class="btn-update-status"
                :disabled="isUpdatingStatus"
                @change="updateStatus($event.target.value)"
              >
                <option value="Pending">Pending</option>
                <option value="Confirmed">Confirmed</option>
                <option value="Processing">Processing</option>
                <option value="Shipped">Shipped</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
                <option value="Returned">Returned</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 6-Stage Progress Stepper matching mockup -->
        <div class="card stepper-card">
          <div class="stepper-track">
            <div class="step-item completed">
              <div class="step-icon-circle"><CheckCircle2 :size="16" /></div>
              <span class="step-label">Pending</span>
              <span class="step-time">Aug 31, 10:24 AM</span>
            </div>
            <div class="step-connector completed"></div>

            <div class="step-item completed">
              <div class="step-icon-circle"><CheckCircle2 :size="16" /></div>
              <span class="step-label">Confirmed</span>
              <span class="step-time">Aug 31, 11:05 AM</span>
            </div>
            <div class="step-connector completed"></div>

            <div class="step-item active">
              <div class="step-icon-circle"><Clock :size="16" /></div>
              <span class="step-label">Processing</span>
              <span class="step-time">Aug 31, 02:30 PM</span>
            </div>
            <div class="step-connector"></div>

            <div class="step-item pending">
              <div class="step-icon-circle"><Truck :size="16" /></div>
              <span class="step-label">Shipped</span>
              <span class="step-time">Pending</span>
            </div>
            <div class="step-connector"></div>

            <div class="step-item pending">
              <div class="step-icon-circle"><MapPin :size="16" /></div>
              <span class="step-label">Out for Delivery</span>
              <span class="step-time">Pending</span>
            </div>
            <div class="step-connector"></div>

            <div class="step-item pending">
              <div class="step-icon-circle"><Package :size="16" /></div>
              <span class="step-label">Delivered</span>
              <span class="step-time">Pending</span>
            </div>
          </div>
        </div>

        <!-- 2-Column Order Details Layout -->
        <div class="order-detail-grid">
          <!-- Left Column -->
          <div class="order-left-col">
            <!-- 1. Order Information Card -->
            <div class="card detail-panel-card">
              <h3 class="panel-card-title">Order Information</h3>
              <div class="order-info-two-col">
                <div class="info-group">
                  <span class="info-lbl">Order ID</span>
                  <strong class="info-val">#{{ activeOrder.order_number }}</strong>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Payment Method</span>
                  <div class="pay-method-pill">
                    <CreditCard :size="13" />
                    <strong>{{ activeOrder.payment_method || 'ABA Pay' }}</strong>
                  </div>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Order Date</span>
                  <span class="info-val">Aug 31, 2025, 10:24 AM</span>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Delivery Method</span>
                  <span class="info-val">Standard Delivery (J&T Express)</span>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Order Status</span>
                  <div>
                    <span class="status-pill" :class="getStatusBadgeClass(activeOrder.status)">
                      {{ activeOrder.status }}
                    </span>
                  </div>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Tracking Number</span>
                  <span class="info-val text-muted">JT892401928</span>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Payment Status</span>
                  <div>
                    <span class="payment-pill pay-paid">Paid</span>
                  </div>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Estimated Delivery</span>
                  <span class="info-val">Sep 2, 2025 - Sep 4, 2025</span>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Sales Channel</span>
                  <span class="info-val">Online Store</span>
                </div>
                <div class="info-group">
                  <span class="info-lbl">Last Updated</span>
                  <span class="info-val text-muted">Aug 31, 2025, 02:30 PM</span>
                </div>
              </div>
            </div>

            <!-- 2. Order Items Card -->
            <div class="card detail-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Order Items ({{ (activeOrder.items || []).length || 3 }})</h3>
                <button class="btn-edit-items-text">Edit Items</button>
              </div>

              <table class="atelier-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th class="text-right">Price</th>
                    <th class="text-center">Quantity</th>
                    <th class="text-right">Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="it in (activeOrder.items || [])" :key="it.id">
                    <td>
                      <div class="order-item-cell">
                        <img
                          :src="it.image_url || '/images/prod-sk2.jpg'"
                          class="order-item-img"
                          @error="$event.target.src = '/images/prod-sk2.jpg'"
                        />
                        <div class="order-item-meta">
                          <strong class="item-title">{{ it.product_name }}</strong>
                          <span class="item-sku">SKU: COSRX-001</span>
                        </div>
                      </div>
                    </td>
                    <td class="text-right font-medium">${{ Number(it.price).toFixed(2) }}</td>
                    <td class="text-center">{{ it.quantity }}</td>
                    <td class="text-right font-bold">${{ Number(it.total).toFixed(2) }}</td>
                  </tr>

                  <tr v-if="(activeOrder.items || []).length === 0">
                    <td>
                      <div class="order-item-cell">
                        <img src="/images/prod-sk2.jpg" class="order-item-img" />
                        <div class="order-item-meta">
                          <strong class="item-title">COSRX Advanced Snail 96 Mucin Power Essence</strong>
                          <span class="item-sku">SKU: COSRX-001</span>
                        </div>
                      </div>
                    </td>
                    <td class="text-right font-medium">$24.00</td>
                    <td class="text-center">1</td>
                    <td class="text-right font-bold">$24.00</td>
                  </tr>
                </tbody>
              </table>

              <!-- Financial Totals Summary matching mockup -->
              <div class="financial-summary-block">
                <div class="fin-row">
                  <span>Subtotal</span>
                  <strong>${{ Number(activeOrder.subtotal || 64.00).toFixed(2) }}</strong>
                </div>
                <div class="fin-row">
                  <span>Shipping Fee</span>
                  <span>${{ Number(activeOrder.shipping_fee || 3.00).toFixed(2) }}</span>
                </div>
                <div class="fin-row text-red">
                  <span>Discount (WELCOME10)</span>
                  <span>-${{ Number(activeOrder.discount || 6.40).toFixed(2) }}</span>
                </div>
                <div class="fin-row-total">
                  <strong>Total</strong>
                  <strong class="grand-total">${{ Number(activeOrder.total || 60.60).toFixed(2) }}</strong>
                </div>
              </div>
            </div>

            <!-- 3. Customer & Internal Notes -->
            <div class="notes-grid-row">
              <div class="card detail-panel-card">
                <h4 class="notes-title">Customer Notes</h4>
                <p class="notes-body">No special notes from customer.</p>
              </div>

              <div class="card detail-panel-card">
                <div class="card-header-row">
                  <h4 class="notes-title">Internal Notes</h4>
                  <button class="btn-add-note">Add Note <ChevronDown :size="12" /></button>
                </div>
                <p class="notes-body text-muted">
                  Order verified and dispatched to packing atelier station.
                </p>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="order-right-col">
            <!-- 1. Customer Information Card -->
            <div class="card detail-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Customer Information</h3>
                <span class="btn-edit-text">Edit</span>
              </div>

              <div class="customer-info-box">
                <img :src="getAvatar(activeOrder.customer_name)" class="cust-profile-avatar" />
                <div class="cust-profile-texts">
                  <strong class="cust-name-main">{{ activeOrder.customer_name }}</strong>
                  <span class="cust-email-main">{{ activeOrder.customer_email }}</span>
                  <span class="cust-phone-main">+855 12 345 678</span>
                </div>
              </div>

              <div class="customer-stats-triplet">
                <div class="cust-stat">
                  <span class="c-stat-lbl">Total Orders</span>
                  <strong class="c-stat-val">5</strong>
                </div>
                <div class="cust-stat">
                  <span class="c-stat-lbl">Total Spent</span>
                  <strong class="c-stat-val">$248.50</strong>
                </div>
                <div class="cust-stat">
                  <span class="c-stat-lbl">Customer Since</span>
                  <strong class="c-stat-val">Mar 10, 2024</strong>
                </div>
              </div>

              <router-link to="/customers" class="btn-view-customer-profile">
                <User :size="14" />
                <span>View Customer Profile</span>
              </router-link>
            </div>

            <!-- 2. Shipping Address Card -->
            <div class="card detail-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Shipping Address</h3>
                <span class="btn-edit-text">Edit</span>
              </div>
              <div class="shipping-address-content">
                <MapPin :size="16" class="address-pin-icon" />
                <div class="address-texts">
                  <strong>{{ activeOrder.customer_name }}</strong>
                  <p>{{ activeOrder.shipping_address || '#21, St. 271, Boeng Keng Kang 1' }}</p>
                  <p>{{ activeOrder.shipping_city || 'Phnom Penh' }}, Cambodia</p>
                  <p>+855 12 345 678</p>
                </div>
              </div>
            </div>

            <!-- 3. Payment Information Card -->
            <div class="card detail-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Payment Information</h3>
                <span class="payment-pill pay-paid">Paid</span>
              </div>

              <div class="payment-details-list">
                <div class="pay-row">
                  <CreditCard :size="14" class="text-muted" />
                  <strong>{{ activeOrder.payment_method || 'ABA Pay' }}</strong>
                </div>
                <div class="pay-row-kv">
                  <span class="pay-kv-lbl">Transaction ID</span>
                  <span class="pay-kv-val">202508311024556789</span>
                </div>
                <div class="pay-row-kv">
                  <span class="pay-kv-lbl">Paid on</span>
                  <span class="pay-kv-val">Aug 31, 2025, 10:25 AM</span>
                </div>
                <div class="pay-row-kv">
                  <span class="pay-kv-lbl">Amount Paid</span>
                  <strong class="pay-kv-val">${{ Number(activeOrder.total).toFixed(2) }}</strong>
                </div>
              </div>
            </div>

            <!-- 4. Order Timeline -->
            <div class="card detail-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Order Timeline</h3>
                <span class="view-all-link">View All</span>
              </div>

              <div class="timeline-events-list">
                <div class="timeline-evt completed">
                  <div class="evt-dot">✓</div>
                  <div class="evt-meta">
                    <strong>Order Placed</strong>
                    <span>Aug 31, 2025, 10:24 AM</span>
                  </div>
                </div>
                <div class="timeline-evt completed">
                  <div class="evt-dot">✓</div>
                  <div class="evt-meta">
                    <strong>Payment Confirmed</strong>
                    <span>Aug 31, 2025, 10:25 AM</span>
                  </div>
                </div>
                <div class="timeline-evt completed">
                  <div class="evt-dot">✓</div>
                  <div class="evt-meta">
                    <strong>Order Confirmed</strong>
                    <span>Aug 31, 2025, 11:05 AM</span>
                  </div>
                </div>
                <div class="timeline-evt active">
                  <div class="evt-dot-active">●</div>
                  <div class="evt-meta">
                    <strong>Processing</strong>
                    <span>Aug 31, 2025, 02:30 PM</span>
                  </div>
                </div>
                <div class="timeline-evt pending">
                  <div class="evt-dot-pending">○</div>
                  <div class="evt-meta">
                    <span class="text-muted">Shipped</span>
                  </div>
                </div>
                <div class="timeline-evt pending">
                  <div class="evt-dot-pending">○</div>
                  <div class="evt-meta">
                    <span class="text-muted">Out for Delivery</span>
                  </div>
                </div>
                <div class="timeline-evt pending">
                  <div class="evt-dot-pending">○</div>
                  <div class="evt-meta">
                    <span class="text-muted">Delivered</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.orders-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.orders-hero-card {
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
.text-red { color: #D32F2F; }
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
  max-width: 300px;
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

/* Tabs & Top Actions */
.tabs-and-actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #EFE7E0;
  padding-bottom: 6px;
}

.status-tabs-row {
  display: flex;
  gap: 18px;
}

.tab-btn {
  background: none;
  border: none;
  font-size: 13px;
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

.top-row-actions {
  display: flex;
  align-items: center;
  gap: 10px;
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
  font-weight: 500;
  cursor: pointer;
}

.btn-create-order {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #84261B;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
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

.order-id-link {
  font-weight: 700;
  color: #84261B;
  cursor: pointer;
}

.order-id-link:hover {
  text-decoration: underline;
}

.customer-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.customer-avatar-mini {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.customer-meta-wrap {
  display: flex;
  flex-direction: column;
}

.customer-name-txt {
  font-size: 13px;
  color: #2D2621;
}

.customer-email-txt {
  font-size: 11px;
  color: #8C847E;
}

.items-cell-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.thumbs-stack {
  display: flex;
  align-items: center;
}

.mini-item-thumb {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #FFFFFF;
  margin-right: -8px;
}

.items-count-badge {
  padding: 2px 6px;
  background: #FAF0E8;
  color: #C4623C;
  border-radius: 99px;
  font-size: 10.5px;
  font-weight: 700;
  margin-left: 10px;
}

.order-total-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.total-amount {
  font-weight: 700;
  color: #2D2621;
}

.total-items-sub {
  font-size: 11px;
  color: #8C847E;
}

.payment-pill {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.pay-paid { background: #E8F5E9; color: #2E7D32; }
.pay-cod { background: #F3E8FF; color: #6B21A8; }
.pay-failed { background: #FDF0EE; color: #D97768; }

.delivery-cell {
  display: flex;
  flex-direction: column;
}

.delivery-method-txt {
  font-size: 12.5px;
  color: #2D2621;
}

.delivery-courier-sub {
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

.badge-delivered { background: #E8F5E9; color: #2E7D32; }
.badge-processing { background: #E0F2FE; color: #0369A1; }
.badge-shipped { background: #F3E8FF; color: #6B21A8; }
.badge-confirmed { background: #EAF4FA; color: #1E6091; }
.badge-cancelled { background: #FDF0EE; color: #D97768; }
.badge-returned { background: #FAF0E8; color: #C4623C; }

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
/* VIEW 2: ORDER DETAIL DASHBOARD             */
/* ========================================== */
.order-detail-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-detail-header-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px 24px;
}

.editor-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  margin-bottom: 4px;
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
}

.crumb-sep { color: #8C847E; }
.crumb-current { color: #5C544E; }

.order-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-main-title {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 26px;
  font-weight: 700;
  color: #84261B;
}

.order-timestamp-sub {
  font-size: 12.5px;
  color: #7A726C;
}

.header-right-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-invoice-action {
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

.btn-update-status {
  padding: 8px 16px;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  outline: none;
}

/* Stepper Card */
.stepper-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px 30px;
}

.stepper-track {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
  width: 110px;
}

.step-icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-item.completed .step-icon-circle {
  background: #84261B;
  color: #FFFFFF;
}

.step-item.active .step-icon-circle {
  background: #C4623C;
  color: #FFFFFF;
  animation: pulse 2s infinite;
}

.step-item.pending .step-icon-circle {
  background: #FAF7F4;
  color: #A09892;
  border: 1px solid #EFE7E0;
}

.step-label {
  font-size: 12px;
  font-weight: 600;
  color: #2D2621;
}

.step-time {
  font-size: 10.5px;
  color: #8C847E;
}

.step-connector {
  flex: 1;
  height: 2px;
  background: #EFE7E0;
  margin-bottom: 24px;
}

.step-connector.completed {
  background: #84261B;
}

/* Order Detail Grid */
.order-detail-grid {
  display: grid;
  grid-template-columns: 1.8fr 1.2fr;
  gap: 20px;
}

.order-left-col,
.order-right-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-panel-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px;
}

.panel-card-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D2621;
  margin-bottom: 14px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.btn-edit-items-text,
.btn-edit-text {
  font-size: 12px;
  color: #84261B;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
}

.order-info-two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px 24px;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.info-lbl {
  font-size: 11px;
  color: #8C847E;
  text-transform: uppercase;
}

.info-val {
  font-size: 13px;
  color: #2D2621;
}

.pay-method-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #2D2621;
}

.order-item-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.order-item-img {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.order-item-meta {
  display: flex;
  flex-direction: column;
}

.item-title {
  font-size: 12.5px;
  color: #2D2621;
}

.item-sku {
  font-size: 11px;
  color: #8C847E;
}

.financial-summary-block {
  margin-top: 18px;
  border-top: 1px solid #EFE7E0;
  padding-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 280px;
  margin-left: auto;
}

.fin-row {
  display: flex;
  justify-content: space-between;
  font-size: 12.5px;
  color: #5C544E;
}

.fin-row.text-red {
  color: #D32F2F;
}

.fin-row-total {
  display: flex;
  justify-content: space-between;
  font-size: 15px;
  border-top: 1px solid #F5ECE6;
  padding-top: 8px;
  margin-top: 4px;
}

.grand-total {
  color: #84261B;
  font-size: 17px;
}

.notes-grid-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.notes-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #2D2621;
  margin-bottom: 8px;
}

.notes-body {
  font-size: 12px;
  color: #5C544E;
  line-height: 1.45;
}

.btn-add-note {
  background: none;
  border: none;
  color: #84261B;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* Customer Profile Card */
.customer-info-box {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.cust-profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.cust-profile-texts {
  display: flex;
  flex-direction: column;
}

.cust-name-main {
  font-size: 14px;
  color: #2D2621;
}

.cust-email-main,
.cust-phone-main {
  font-size: 11.5px;
  color: #7A726C;
}

.customer-stats-triplet {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  background: #FAF7F4;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.cust-stat {
  display: flex;
  flex-direction: column;
}

.c-stat-lbl {
  font-size: 10.5px;
  color: #8C847E;
}

.c-stat-val {
  font-size: 13.5px;
  color: #2D2621;
}

.btn-view-customer-profile {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 8px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 500;
  color: #3C3530;
  text-decoration: none;
}

.btn-view-customer-profile:hover {
  border-color: #84261B;
  color: #84261B;
}

/* Shipping Address Card */
.shipping-address-content {
  display: flex;
  gap: 12px;
}

.address-pin-icon {
  color: #84261B;
  flex-shrink: 0;
  margin-top: 2px;
}

.address-texts strong {
  font-size: 13px;
  color: #2D2621;
}

.address-texts p {
  font-size: 12px;
  color: #5C544E;
  margin: 2px 0;
}

/* Payment Info */
.payment-details-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pay-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.pay-row-kv {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.pay-kv-lbl { color: #8C847E; }
.pay-kv-val { color: #2D2621; }

/* Timeline Events List */
.timeline-events-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.timeline-evt {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.evt-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #E8F5E9;
  color: #2E7D32;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.evt-dot-active {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #FAF0E8;
  color: #C4623C;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.evt-dot-pending {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  color: #A09892;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.evt-meta {
  display: flex;
  flex-direction: column;
}

.evt-meta strong {
  font-size: 12.5px;
  color: #2D2621;
}

.evt-meta span {
  font-size: 11px;
  color: #8C847E;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.08); }
  100% { transform: scale(1); }
}

@media (max-width: 1100px) {
  .order-detail-grid {
    grid-template-columns: 1fr;
  }
  .kpi-grid-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
