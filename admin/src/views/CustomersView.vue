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
  Mail,
  UserPlus,
  ShoppingBag,
  DollarSign,
  Users,
  UserCheck,
  TrendingUp,
  TrendingDown,
  ArrowLeft,
  MapPin,
  CreditCard,
  Lock,
  FileText,
  Star,
  CheckCircle2,
  Sparkles,
  ExternalLink,
  X,
  Save,
  Crown
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View Modes: 'list' | 'vip'
const currentView = ref('list')
const activeCustomer = ref(null)

// Filtering & Search
const searchQuery = ref('')
const selectedGroup = ref('All Groups')
const selectedStatus = ref('All')
const activeTab = ref('all') // 'all', 'new', 'vip', 'inactive'

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Selection
const selectedCustomerIds = ref([])
const selectAll = ref(false)

// Active tab in VIP detail view
const activeVipTab = ref('overview')

// Add Customer modal
const showAddModal = ref(false)
const newCustomerForm = reactive({
  name: '',
  email: '',
  phone: '+855 12 345 678',
  tier: 'VIP',
  location: 'Cambodia',
  city: 'Phnom Penh'
})

onMounted(async () => {
  await adminStore.fetchCustomers()
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

// 4 Top KPIs
const customerKpis = computed(() => {
  const count = adminStore.customers?.length || 1248
  return [
    {
      label: 'Total Customers',
      val: count > 10 ? count : 1248,
      trend: '+12%',
      trendUp: true,
      icon: Users,
      color: 'pill-rose'
    },
    {
      label: 'New Customers',
      val: 96,
      trend: '+18%',
      trendUp: true,
      icon: UserPlus,
      color: 'pill-peach'
    },
    {
      label: 'Avg. Orders per Customer',
      val: '4.8',
      trend: '-6%',
      trendUp: false,
      icon: ShoppingBag,
      color: 'pill-amber'
    },
    {
      label: 'Avg. Spend per Customer',
      val: '$78.30',
      trend: '+14%',
      trendUp: true,
      icon: DollarSign,
      color: 'pill-crimson'
    }
  ]
})

// Customer directory mock fallback data to match Luméa Customer Management Dashboard.png
const directoryData = ref([
  {
    id: 1,
    name: 'Sokha Meas',
    email: 'sokha.meas@gmail.com',
    phone: '+855 12 345 678',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 12,
    total_spent: 248.50,
    group: 'VIP',
    status: 'Active',
    created_at: 'Mar 10, 2024'
  },
  {
    id: 2,
    name: 'Dara Kim',
    email: 'dara.kim@gmail.com',
    phone: '+855 98 765 432',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 5,
    total_spent: 98.00,
    group: 'Regular',
    status: 'Active',
    created_at: 'Apr 22, 2024'
  },
  {
    id: 3,
    name: 'Chanthy Norn',
    email: 'chanthy.norn@gmail.com',
    phone: '+855 16 234 567',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 18,
    total_spent: 412.00,
    group: 'VIP',
    status: 'Active',
    created_at: 'Jan 5, 2024'
  },
  {
    id: 4,
    name: 'Visal Chhum',
    email: 'visal.chhum@gmail.com',
    phone: '+855 70 123 456',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 3,
    total_spent: 56.00,
    group: 'Regular',
    status: 'Active',
    created_at: 'Jun 18, 2024'
  },
  {
    id: 5,
    name: 'Sreypov Tep',
    email: 'sreypov.tep@gmail.com',
    phone: '+855 11 987 654',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 8,
    total_spent: 189.00,
    group: 'Gold',
    status: 'Active',
    created_at: 'Feb 14, 2024'
  },
  {
    id: 6,
    name: 'Leap Meng',
    email: 'leap.meng@gmail.com',
    phone: '+855 93 456 789',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 2,
    total_spent: 32.00,
    group: 'Regular',
    status: 'Inactive',
    created_at: 'Aug 1, 2024'
  },
  {
    id: 7,
    name: 'Takakvitya Tey',
    email: 'takakvitya.tey@gmail.com',
    phone: '+855 81 222 333',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 10,
    total_spent: 276.00,
    group: 'Gold',
    status: 'Active',
    created_at: 'Mar 28, 2024'
  },
  {
    id: 8,
    name: 'Put Sokchan',
    email: 'put.sokchan@gmail.com',
    phone: '+855 17 444 555',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 1,
    total_spent: 24.00,
    group: 'Regular',
    status: 'Active',
    created_at: 'Aug 15, 2024'
  },
  {
    id: 9,
    name: 'Keat Pichudom',
    email: 'keat.pichudom@gmail.com',
    phone: '+855 69 888 999',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 7,
    total_spent: 156.00,
    group: 'Regular',
    status: 'Active',
    created_at: 'May 3, 2024'
  },
  {
    id: 10,
    name: 'Rathana Sor',
    email: 'rathana.sor@gmail.com',
    phone: '+855 77 111 222',
    country: 'Cambodia',
    country_flag: '🇰🇭',
    orders_count: 4,
    total_spent: 89.00,
    group: 'Regular',
    status: 'Inactive',
    created_at: 'Jul 19, 2024'
  }
])

// Merge DB users with directory data if available
const combinedCustomers = computed(() => {
  const dbUsers = adminStore.customers || []
  if (dbUsers.length > 0) {
    return directoryData.value.map(c => {
      const match = dbUsers.find(u => u.email === c.email)
      if (match) {
        return {
          ...c,
          orders_count: match.orders_count || c.orders_count,
          total_spent: match.total_spent || c.total_spent,
          name: match.name || c.name
        }
      }
      return c
    })
  }
  return directoryData.value
})

// Filtered customers
const filteredCustomers = computed(() => {
  let list = [...combinedCustomers.value]

  if (activeTab.value === 'new') {
    list = list.filter(c => c.orders_count <= 2)
  } else if (activeTab.value === 'vip') {
    list = list.filter(c => c.group === 'VIP' || c.group === 'Gold')
  } else if (activeTab.value === 'inactive') {
    list = list.filter(c => c.status === 'Inactive')
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      c.name.toLowerCase().includes(q) ||
      c.email.toLowerCase().includes(q) ||
      c.phone.includes(q)
    )
  }

  if (selectedGroup.value !== 'All Groups') {
    list = list.filter(c => c.group === selectedGroup.value)
  }

  if (selectedStatus.value !== 'All') {
    list = list.filter(c => c.status === selectedStatus.value)
  }

  return list
})

const paginatedCustomers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredCustomers.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredCustomers.value.length / itemsPerPage.value) || 1
})

const resetFilters = () => {
  searchQuery.value = ''
  selectedGroup.value = 'All Groups'
  selectedStatus.value = 'All'
  activeTab.value = 'all'
  currentPage.value = 1
}

const toggleSelectAll = () => {
  if (selectAll.value) {
    selectedCustomerIds.value = paginatedCustomers.value.map(c => c.id)
  } else {
    selectedCustomerIds.value = []
  }
}

// Helpers
const getGroupBadgeClass = (group) => {
  if (group === 'VIP') return 'badge-vip'
  if (group === 'Gold') return 'badge-gold'
  return 'badge-regular'
}

// Open VIP Details view
const viewCustomerVip = (customer) => {
  activeCustomer.value = customer
  activeVipTab.value = 'overview'
  currentView.value = 'vip'
}

// Marketing preferences state for the VIP customer
const marketingPrefs = reactive({
  email: true,
  sms: true,
  promos: true,
  updates: false
})
</script>

<template>
  <div class="customers-management-page">
    <!-- ========================================== -->
    <!-- VIEW 1: CUSTOMERS DIRECTORY               -->
    <!-- Matching Luméa Customer Management Dashboard.png -->
    <!-- ========================================== -->
    <template v-if="currentView === 'list'">
      <!-- Hero Banner -->
      <div class="customers-hero-card">
        <div class="hero-left">
          <span class="hero-eyebrow">CUSTOMERS</span>
          <h1 class="hero-heading">Customers Management</h1>
          <p class="hero-subtext">View and manage your customers, their orders, and activity.</p>
        </div>

        <div class="hero-right">
          <div class="hero-visual-callout">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Clientele"
              class="hero-bottles"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
            <div class="hero-motto">
              <span class="motto-line">Real people.</span>
              <span class="motto-line highlight">Brighter tomorrows.</span>
            </div>
          </div>

          <button class="btn-add-customer" @click="showAddModal = true">
            <Plus :size="16" />
            <span>Add Customer</span>
          </button>
        </div>
      </div>

      <!-- 4 KPI Cards -->
      <div class="kpi-grid-4">
        <div
          v-for="kpi in customerKpis"
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
                <component :is="kpi.trendUp ? TrendingUp : TrendingDown" :size="13" />
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
            placeholder="Search customers by name, email, or phone..."
            class="atelier-input-clean"
          />
        </div>

        <div class="filter-dropdowns">
          <div class="select-wrap">
            <select v-model="selectedGroup" class="atelier-select">
              <option value="All Groups">All Groups</option>
              <option value="VIP">VIP</option>
              <option value="Gold">Gold</option>
              <option value="Regular">Regular</option>
            </select>
            <ChevronDown :size="14" class="select-arrow" />
          </div>

          <div class="select-wrap">
            <select v-model="selectedStatus" class="atelier-select">
              <option value="All">All Status</option>
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
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
            All Customers (1,248)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'new' }"
            @click="activeTab = 'new'"
          >
            New Customers (96)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'vip' }"
            @click="activeTab = 'vip'"
          >
            VIP Customers (42)
          </button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'inactive' }"
            @click="activeTab = 'inactive'"
          >
            Inactive Customers (18)
          </button>
        </div>

        <button class="btn-export-outline" @click="alert('Exporting customers database (CSV)...')">
          <Download :size="14" />
          <span>Export</span>
        </button>
      </div>

      <!-- Customers Table Card -->
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
              <th>Customer</th>
              <th>Contact</th>
              <th>Location</th>
              <th class="text-center">Orders</th>
              <th class="text-right">Total Spent</th>
              <th class="text-center">Customer Group</th>
              <th class="text-center">Status</th>
              <th>Date Joined</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(cust, index) in paginatedCustomers"
              :key="cust.id"
              class="table-row-hover"
            >
              <td class="col-checkbox">
                <input
                  type="checkbox"
                  :value="cust.id"
                  v-model="selectedCustomerIds"
                />
              </td>
              <td class="col-order text-muted font-medium">
                {{ index + 1 }}
              </td>
              <td>
                <div class="customer-cell" @click="viewCustomerVip(cust)">
                  <img
                    :src="getAvatar(cust.name)"
                    alt="Customer Avatar"
                    class="cust-avatar-img"
                  />
                  <div class="cust-info-wrap">
                    <strong class="cust-name-txt">{{ cust.name }}</strong>
                    <span class="cust-email-txt">{{ cust.email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="phone-txt">{{ cust.phone }}</span>
              </td>
              <td>
                <div class="location-cell">
                  <span class="flag-icon">{{ cust.country_flag || '🇰🇭' }}</span>
                  <span>{{ cust.country || 'Cambodia' }}</span>
                </div>
              </td>
              <td class="text-center">
                <strong class="orders-count-txt">{{ cust.orders_count }}</strong>
              </td>
              <td class="text-right font-bold text-dark">
                ${{ Number(cust.total_spent).toFixed(2) }}
              </td>
              <td class="text-center">
                <span class="group-pill" :class="getGroupBadgeClass(cust.group)">
                  {{ cust.group }}
                </span>
              </td>
              <td class="text-center">
                <span
                  class="status-pill"
                  :class="cust.status === 'Active' ? 'badge-active' : 'badge-inactive'"
                >
                  {{ cust.status }}
                </span>
              </td>
              <td>
                <span class="date-cell-text">{{ cust.created_at }}</span>
              </td>
              <td class="text-right">
                <div class="action-buttons-cell">
                  <button
                    class="action-icon-btn"
                    title="View VIP Customer Profile"
                    @click="viewCustomerVip(cust)"
                  >
                    <Eye :size="14" />
                  </button>
                  <button
                    class="action-icon-btn"
                    title="Send Email"
                    @click="alert(`Send concierge email to ${cust.email}`)"
                  >
                    <Mail :size="14" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedCustomers.length === 0">
              <td colspan="11" class="empty-table-cell">
                <p>No customers found matching your filter criteria.</p>
                <button class="btn-reset-small" @click="resetFilters">Reset Filters</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Footer -->
        <div class="pagination-footer">
          <span class="pagination-summary">
            Showing 1 to {{ paginatedCustomers.length }} of {{ filteredCustomers.length }} customers
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
    <!-- VIEW 2: VIP CUSTOMER DASHBOARD            -->
    <!-- Matching Luméa VIP Customer Dashboard.png  -->
    <!-- ========================================== -->
    <template v-else-if="currentView === 'vip' && activeCustomer">
      <div class="vip-customer-page">
        <!-- Top Breadcrumbs & Actions -->
        <div class="vip-top-nav-card">
          <div class="nav-left">
            <div class="editor-breadcrumb">
              <button class="btn-back-link" @click="currentView = 'list'">
                <ArrowLeft :size="13" /> Customers
              </button>
              <span class="crumb-sep">/</span>
              <span class="crumb-current">{{ activeCustomer.name }}</span>
            </div>
            <div class="vip-title-row">
              <h1 class="vip-name-heading">{{ activeCustomer.name }}</h1>
              <span class="group-pill badge-vip">VIP</span>
            </div>
            <p class="vip-sub-date">Customer since {{ activeCustomer.created_at || 'Mar 10, 2024' }}</p>
          </div>

          <div class="nav-right-actions">
            <button class="btn-vip-action" @click="alert(`Send email to ${activeCustomer.email}`)">
              <Mail :size="14" />
              <span>Send Email</span>
            </button>
            <button class="btn-vip-action" @click="alert('Edit Customer Details...')">
              <Edit2 :size="14" />
              <span>Edit Customer</span>
            </button>
          </div>
        </div>

        <!-- VIP Showcase Hero Banner matching mockup -->
        <div class="vip-hero-banner">
          <div class="vip-profile-summary">
            <img
              :src="getAvatar(activeCustomer.name)"
              alt="VIP Customer"
              class="vip-large-avatar"
            />
            <div class="vip-meta-texts">
              <div class="name-status-flex">
                <strong class="vip-person-name">{{ activeCustomer.name }}</strong>
                <span class="status-pill badge-active">Active</span>
              </div>
              <div class="crown-badge-row">
                <Crown :size="13" class="crown-icon" />
                <span class="crown-txt">VIP Customer</span>
              </div>
              <div class="vip-contact-lines">
                <span>{{ activeCustomer.email }}</span>
                <span>{{ activeCustomer.phone }}</span>
                <span>Phnom Penh, Cambodia</span>
                <span>Joined on {{ activeCustomer.created_at || 'Mar 10, 2024' }}</span>
              </div>
            </div>
          </div>

          <div class="vip-motto-callout">
            <span class="quote-text">"Skincare is not a luxury,</span>
            <span class="quote-text italic">it's self-care."</span>
          </div>

          <!-- 3 Stat Cards on the Right -->
          <div class="vip-stats-triplet">
            <div class="vip-stat-box">
              <ShoppingBag :size="18" class="stat-ico text-rose" />
              <div class="stat-nums">
                <strong>{{ activeCustomer.orders_count || 12 }}</strong>
                <span>Total Orders</span>
              </div>
            </div>

            <div class="vip-stat-box">
              <DollarSign :size="18" class="stat-ico text-crimson" />
              <div class="stat-nums">
                <strong>${{ Number(activeCustomer.total_spent || 248.50).toFixed(2) }}</strong>
                <span>Total Spent</span>
              </div>
            </div>

            <div class="vip-stat-box">
              <Star :size="18" class="stat-ico text-amber" />
              <div class="stat-nums">
                <strong>4.8</strong>
                <span>Avg. Rating</span>
              </div>
            </div>
          </div>
        </div>

        <!-- VIP Navigation Tabs -->
        <div class="editor-nav-tabs">
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'overview' }"
            @click="activeVipTab = 'overview'"
          >
            Overview
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'orders' }"
            @click="activeVipTab = 'orders'"
          >
            Orders ({{ activeCustomer.orders_count || 12 }})
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'addresses' }"
            @click="activeVipTab = 'addresses'"
          >
            Addresses (3)
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'payments' }"
            @click="activeVipTab = 'payments'"
          >
            Payment Methods (2)
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'wishlist' }"
            @click="activeVipTab = 'wishlist'"
          >
            Wishlist (8)
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'reviews' }"
            @click="activeVipTab = 'reviews'"
          >
            Reviews (4)
          </button>
          <button
            class="editor-tab"
            :class="{ active: activeVipTab === 'activity' }"
            @click="activeVipTab = 'activity'"
          >
            Activity Log
          </button>
        </div>

        <!-- 2-Column VIP Dashboard Content -->
        <div class="vip-dashboard-grid">
          <!-- Left Column -->
          <div class="vip-left-col">
            <!-- 1. Personal Information -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Personal Information</h3>
                <span class="btn-edit-text">Edit</span>
              </div>
              <div class="info-kv-grid">
                <div class="kv-item">
                  <span class="kv-lbl">Full Name</span>
                  <strong class="kv-val">{{ activeCustomer.name }}</strong>
                </div>
                <div class="kv-item">
                  <span class="kv-lbl">Email</span>
                  <span class="kv-val">{{ activeCustomer.email }}</span>
                </div>
                <div class="kv-item">
                  <span class="kv-lbl">Phone</span>
                  <span class="kv-val">{{ activeCustomer.phone }}</span>
                </div>
                <div class="kv-item">
                  <span class="kv-lbl">Date of Birth</span>
                  <span class="kv-val">Apr 15, 1995</span>
                </div>
                <div class="kv-item">
                  <span class="kv-lbl">Gender</span>
                  <span class="kv-val">Female</span>
                </div>
                <div class="kv-item">
                  <span class="kv-lbl">Language</span>
                  <span class="kv-val">English</span>
                </div>
                <div class="kv-item full-width">
                  <span class="kv-lbl">Notes</span>
                  <p class="kv-desc">Loves Korean skincare products. Prefers gentle formulas for sensitive skin.</p>
                </div>
              </div>
            </div>

            <!-- 2. Customer Group -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Customer Group</h3>
                <span class="btn-edit-text">Edit</span>
              </div>
              <div class="group-info-row">
                <div class="crown-badge-row">
                  <Crown :size="15" class="crown-icon" />
                  <strong>VIP</strong>
                </div>
                <p class="group-subtext">High-value customer with frequent purchases and strong atelier engagement.</p>
              </div>
              <div class="group-stats-row">
                <div class="g-stat">
                  <span>Member Since</span>
                  <strong>Mar 10, 2024</strong>
                </div>
                <div class="g-stat">
                  <span>Total Spent</span>
                  <strong>${{ Number(activeCustomer.total_spent || 248.50).toFixed(2) }}</strong>
                </div>
                <div class="g-stat">
                  <span>Total Orders</span>
                  <strong>{{ activeCustomer.orders_count || 12 }}</strong>
                </div>
                <div class="g-stat">
                  <span>Avg. Order Value</span>
                  <strong>$20.71</strong>
                </div>
              </div>
            </div>

            <!-- 3. Addresses -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Addresses</h3>
                <span class="btn-edit-text">Add Address</span>
              </div>
              <div class="address-cards-stack">
                <div class="addr-box">
                  <span class="addr-tag default">Default</span>
                  <p class="addr-body">#21, St. 271, Boeng Keng Kang 1, Chamkarmon, Phnom Penh 12301, Cambodia</p>
                  <span class="addr-phone">+855 12 345 678</span>
                </div>
                <div class="addr-box">
                  <span class="addr-tag office">Office</span>
                  <p class="addr-body">#15, Norodom Blvd, Sangkat Tonle Bassac, Phnom Penh 120101, Cambodia</p>
                  <span class="addr-phone">+855 12 345 678</span>
                </div>
              </div>
            </div>

            <!-- 4. Customer Tags -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Customer Tags</h3>
                <span class="btn-edit-text">Edit</span>
              </div>
              <div class="tags-pill-wrap">
                <span class="tag-pill rose">VIP</span>
                <span class="tag-pill peach">Repeat Customer</span>
                <span class="tag-pill neutral">Sensitive Skin</span>
                <span class="tag-pill neutral">Loves Korean Brands</span>
                <button class="btn-add-tag">+ Add Tag</button>
              </div>
            </div>

            <!-- 5. Marketing Preferences -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Marketing Preferences</h3>
                <span class="btn-edit-text">Edit</span>
              </div>
              <div class="prefs-grid">
                <div class="pref-item">
                  <button
                    type="button"
                    class="atelier-toggle-switch"
                    :class="{ active: marketingPrefs.email }"
                    @click="marketingPrefs.email = !marketingPrefs.email"
                  >
                    <span class="toggle-slider"></span>
                  </button>
                  <span>Email Notifications</span>
                </div>

                <div class="pref-item">
                  <button
                    type="button"
                    class="atelier-toggle-switch"
                    :class="{ active: marketingPrefs.sms }"
                    @click="marketingPrefs.sms = !marketingPrefs.sms"
                  >
                    <span class="toggle-slider"></span>
                  </button>
                  <span>SMS Notifications</span>
                </div>

                <div class="pref-item">
                  <button
                    type="button"
                    class="atelier-toggle-switch"
                    :class="{ active: marketingPrefs.promos }"
                    @click="marketingPrefs.promos = !marketingPrefs.promos"
                  >
                    <span class="toggle-slider"></span>
                  </button>
                  <span>Promotional Emails</span>
                </div>

                <div class="pref-item">
                  <button
                    type="button"
                    class="atelier-toggle-switch"
                    :class="{ active: marketingPrefs.updates }"
                    @click="marketingPrefs.updates = !marketingPrefs.updates"
                  >
                    <span class="toggle-slider"></span>
                  </button>
                  <span>New Product Updates</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="vip-right-col">
            <!-- 1. Quick Actions -->
            <div class="card vip-panel-card">
              <h3 class="panel-card-title">Quick Actions</h3>
              <div class="quick-actions-2x2">
                <button class="qa-btn" @click="alert('Send Concierge Email...')">
                  <Mail :size="15" />
                  <span>Send Email</span>
                </button>
                <button class="qa-btn" @click="alert('Add Patron Note...')">
                  <FileText :size="15" />
                  <span>Add Note</span>
                </button>
                <button class="qa-btn" @click="alert('Create Order for Customer...')">
                  <ShoppingBag :size="15" />
                  <span>Create Order</span>
                </button>
                <button class="qa-btn" @click="alert('Send Password Reset Link...')">
                  <Lock :size="15" />
                  <span>Reset Password</span>
                </button>
              </div>
            </div>

            <!-- 2. Recent Orders -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Recent Orders</h3>
                <router-link to="/orders" class="view-all-link">View All</router-link>
              </div>
              <div class="recent-orders-list">
                <div class="cust-order-row">
                  <div class="c-order-id">
                    <strong>#LUM-001</strong>
                    <span class="text-muted">Aug 31, 2025</span>
                  </div>
                  <span class="c-order-items">3 items</span>
                  <strong class="c-order-total">$64.00</strong>
                  <span class="status-pill badge-processing">Processing</span>
                </div>
                <div class="cust-order-row">
                  <div class="c-order-id">
                    <strong>#LUM-002</strong>
                    <span class="text-muted">Aug 18, 2025</span>
                  </div>
                  <span class="c-order-items">1 item</span>
                  <strong class="c-order-total">$28.00</strong>
                  <span class="status-pill badge-delivered">Delivered</span>
                </div>
                <div class="cust-order-row">
                  <div class="c-order-id">
                    <strong>#LUM-003</strong>
                    <span class="text-muted">Jul 22, 2025</span>
                  </div>
                  <span class="c-order-items">4 items</span>
                  <strong class="c-order-total">$89.00</strong>
                  <span class="status-pill badge-delivered">Delivered</span>
                </div>
              </div>
            </div>

            <!-- 3. Customer Activity Timeline -->
            <div class="card vip-panel-card">
              <div class="card-header-row">
                <h3 class="panel-card-title">Customer Activity</h3>
                <span class="view-all-link">View All</span>
              </div>
              <div class="activity-timeline-feed">
                <div class="feed-item">
                  <div class="feed-icon-pill rose"><ShoppingBag :size="13" /></div>
                  <div class="feed-content">
                    <span class="feed-title">Placed an order #LUM-001</span>
                    <span class="feed-time">Aug 31, 2025, 10:24 AM</span>
                  </div>
                </div>
                <div class="feed-item">
                  <div class="feed-icon-pill neutral"><Eye :size="13" /></div>
                  <div class="feed-content">
                    <span class="feed-title">Viewed Anua Heartleaf 77% Soothing Toner</span>
                    <span class="feed-time">Aug 30, 2025, 08:15 PM</span>
                  </div>
                </div>
                <div class="feed-item">
                  <div class="feed-icon-pill peach"><Star :size="13" /></div>
                  <div class="feed-content">
                    <span class="feed-title">Left a 5-star review on Centella Ampoule</span>
                    <span class="feed-time">Aug 18, 2025, 11:12 AM</span>
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
.customers-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.customers-hero-card {
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

.btn-add-customer {
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

.btn-add-customer:hover {
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

.customer-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.cust-avatar-img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}

.cust-info-wrap {
  display: flex;
  flex-direction: column;
}

.cust-name-txt {
  font-size: 13px;
  color: #2D2621;
}

.cust-email-txt {
  font-size: 11px;
  color: #8C847E;
}

.phone-txt {
  font-size: 12px;
  color: #5C544E;
}

.location-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.flag-icon {
  font-size: 15px;
}

.orders-count-txt {
  font-size: 13px;
  color: #2D2621;
}

.group-pill {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-vip { background: #F8E9E4; color: #84261B; }
.badge-gold { background: #FEF7ED; color: #B25E00; }
.badge-regular { background: #F5ECE6; color: #5C544E; }

.status-pill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-active { background: #E8F5E9; color: #2E7D32; }
.badge-inactive { background: #F5ECE6; color: #8C847E; }

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
/* VIEW 2: VIP CUSTOMER DASHBOARD            */
/* ========================================== */
.vip-customer-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.vip-top-nav-card {
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

.vip-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.vip-name-heading {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 28px;
  font-weight: 700;
  color: #84261B;
}

.vip-sub-date {
  font-size: 12.5px;
  color: #7A726C;
}

.nav-right-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-vip-action {
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

/* VIP Hero Banner */
.vip-hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FAF5F2 0%, #FFFFFF 100%);
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px 30px;
}

.vip-profile-summary {
  display: flex;
  align-items: center;
  gap: 20px;
}

.vip-large-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #EFE7E0;
}

.vip-meta-texts {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name-status-flex {
  display: flex;
  align-items: center;
  gap: 8px;
}

.vip-person-name {
  font-size: 18px;
  color: #2D2621;
}

.crown-badge-row {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #B25E00;
  font-size: 12px;
  font-weight: 700;
}

.vip-contact-lines {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #7A726C;
  flex-wrap: wrap;
}

.vip-motto-callout {
  display: flex;
  flex-direction: column;
  text-align: center;
}

.quote-text {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 15px;
  color: #84261B;
  font-weight: 600;
}

.quote-text.italic {
  font-style: italic;
}

.vip-stats-triplet {
  display: flex;
  gap: 16px;
}

.vip-stat-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 10px;
  padding: 12px 18px;
}

.stat-nums {
  display: flex;
  flex-direction: column;
}

.stat-nums strong {
  font-size: 18px;
  color: #2D2621;
}

.stat-nums span {
  font-size: 11px;
  color: #8C847E;
}

.text-rose { color: #84261B; }
.text-crimson { color: #A03B2E; }
.text-amber { color: #B25E00; }

/* Tabs */
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

/* Grid Layout */
.vip-dashboard-grid {
  display: grid;
  grid-template-columns: 1.6fr 1.4fr;
  gap: 20px;
}

.vip-left-col,
.vip-right-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.vip-panel-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px;
}

.panel-card-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D2621;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.btn-edit-text {
  font-size: 12px;
  color: #84261B;
  font-weight: 600;
  cursor: pointer;
}

.info-kv-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.kv-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.kv-item.full-width {
  grid-column: span 2;
}

.kv-lbl {
  font-size: 11px;
  color: #8C847E;
  text-transform: uppercase;
}

.kv-val {
  font-size: 13px;
  color: #2D2621;
}

.kv-desc {
  font-size: 12.5px;
  color: #5C544E;
  line-height: 1.45;
}

/* Group Stats */
.group-subtext {
  font-size: 12px;
  color: #7A726C;
  margin: 4px 0 12px 0;
}

.group-stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  background: #FAF7F4;
  border-radius: 8px;
  padding: 12px;
}

.g-stat {
  display: flex;
  flex-direction: column;
}

.g-stat span {
  font-size: 10.5px;
  color: #8C847E;
}

.g-stat strong {
  font-size: 13.5px;
  color: #2D2621;
}

/* Addresses */
.address-cards-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.addr-box {
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.addr-tag {
  align-self: flex-start;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 700;
}

.addr-tag.default { background: #E8F5E9; color: #2E7D32; }
.addr-tag.office { background: #EAF4FA; color: #1E6091; }

.addr-body { font-size: 12.5px; color: #3C3530; }
.addr-phone { font-size: 11px; color: #8C847E; }

/* Tags */
.tags-pill-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag-pill {
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 600;
}

.tag-pill.rose { background: #F8E9E4; color: #84261B; }
.tag-pill.peach { background: #FAF0E8; color: #C4623C; }
.tag-pill.neutral { background: #F5ECE6; color: #5C544E; }

.btn-add-tag {
  background: none;
  border: 1px dashed #C4623C;
  color: #C4623C;
  border-radius: 99px;
  padding: 4px 12px;
  font-size: 11.5px;
  cursor: pointer;
}

/* Preferences */
.prefs-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.pref-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
  color: #3C3530;
}

.atelier-toggle-switch {
  width: 36px;
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
.atelier-toggle-switch.active .toggle-slider { transform: translateX(16px); }

/* Quick Actions */
.quick-actions-2x2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.qa-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: #3C3530;
  cursor: pointer;
  transition: all 0.2s;
}

.qa-btn:hover {
  border-color: #84261B;
  color: #84261B;
  background: #FFFFFF;
}

/* Recent Orders */
.recent-orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cust-order-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #F5ECE6;
}

.c-order-id {
  display: flex;
  flex-direction: column;
}

.c-order-id strong { font-size: 13px; color: #84261B; }
.c-order-id span { font-size: 11px; }

.c-order-items { font-size: 12px; color: #7A726C; }
.c-order-total { font-size: 13px; color: #2D2621; }

.badge-delivered { background: #E8F5E9; color: #2E7D32; }
.badge-processing { background: #E0F2FE; color: #0369A1; }

/* Activity Timeline */
.activity-timeline-feed {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feed-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.feed-icon-pill {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feed-icon-pill.rose { background: #F8E9E4; color: #84261B; }
.feed-icon-pill.peach { background: #FAF0E8; color: #C4623C; }
.feed-icon-pill.neutral { background: #F5ECE6; color: #5C544E; }

.feed-content {
  display: flex;
  flex-direction: column;
}

.feed-title {
  font-size: 12px;
  color: #2D2621;
}

.feed-time {
  font-size: 10.5px;
  color: #8C847E;
}

@media (max-width: 1100px) {
  .vip-dashboard-grid {
    grid-template-columns: 1fr;
  }
  .kpi-grid-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
