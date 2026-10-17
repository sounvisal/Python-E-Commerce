<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import {
  Calendar,
  Download,
  TrendingUp,
  DollarSign,
  ShoppingBag,
  Users,
  Percent,
  ChevronDown,
  ArrowUpRight,
  Package,
  Layers,
  Sparkles,
  UserCheck,
  Star,
  RotateCcw,
  CheckCircle2,
  ExternalLink
} from 'lucide-vue-next'

const adminStore = useAdminStore()
const selectedTimeframe = ref('Aug 1, 2025 - Aug 31, 2025')
const revenueMetric = ref('revenue')
const growthInterval = ref('Daily')

onMounted(async () => {
  if (!adminStore.stats) {
    await adminStore.fetchStats()
  }
})

// Format helpers
const formatCurrency = (val) => {
  return Number(val || 0).toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  })
}

// 4 Top KPIs
const kpiStats = computed(() => {
  const rev = adminStore.stats?.metrics?.total_revenue || 24850
  const orders = adminStore.stats?.metrics?.total_orders || 892
  const customers = adminStore.stats?.metrics?.total_customers || 624

  return [
    {
      id: 'revenue',
      label: 'Total Revenue',
      value: `$${formatCurrency(rev)}`,
      trend: '+12%',
      trendText: 'vs last month',
      icon: DollarSign,
      color: 'crimson'
    },
    {
      id: 'orders',
      label: 'Total Orders',
      value: formatCurrency(orders),
      trend: '+18%',
      trendText: 'vs last month',
      icon: ShoppingBag,
      color: 'peach'
    },
    {
      id: 'customers',
      label: 'Total Customers',
      value: formatCurrency(customers),
      trend: '+15%',
      trendText: 'vs last month',
      icon: Users,
      color: 'rose'
    },
    {
      id: 'conversion',
      label: 'Conversion Rate',
      value: '3.6%',
      trend: '+0.8%',
      trendText: 'vs last month',
      icon: Percent,
      color: 'coral'
    }
  ]
})

// Revenue & Orders Chart Points (Aug 1 - Aug 31)
const revenueChartData = ref([
  { label: 'Aug 1', rev: 1100, orders: 38 },
  { label: 'Aug 5', rev: 1450, orders: 46 },
  { label: 'Aug 10', rev: 1980, orders: 62 },
  { label: 'Aug 15', rev: 1720, orders: 55 },
  { label: 'Aug 20', rev: 2340, orders: 74 },
  { label: 'Aug 25', rev: 2150, orders: 69 },
  { label: 'Aug 31', rev: 2980, orders: 94 }
])

// SVG Line Calculation for Revenue
const revenueSvgPath = computed(() => {
  const points = [
    { x: 20, y: 155 },
    { x: 95, y: 135 },
    { x: 170, y: 105 },
    { x: 245, y: 125 },
    { x: 320, y: 80 },
    { x: 395, y: 95 },
    { x: 470, y: 50 }
  ]
  let d = `M ${points[0].x} ${points[0].y}`
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i]
    const p1 = points[i + 1]
    const mx = (p0.x + p1.x) / 2
    d += ` C ${mx} ${p0.y}, ${mx} ${p1.y}, ${p1.x} ${p1.y}`
  }
  return { d, points }
})

// Customer Growth SVG Area
const customerGrowthPath = computed(() => {
  const points = [
    { x: 20, y: 140 },
    { x: 75, y: 135 },
    { x: 130, y: 130 },
    { x: 185, y: 115 },
    { x: 240, y: 110 },
    { x: 295, y: 95 },
    { x: 350, y: 90 }
  ]
  let lineD = `M ${points[0].x} ${points[0].y}`
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i]
    const p1 = points[i + 1]
    const mx = (p0.x + p1.x) / 2
    lineD += ` C ${mx} ${p0.y}, ${mx} ${p1.y}, ${p1.x} ${p1.y}`
  }
  const areaD = `${lineD} L ${points[points.length - 1].x} 175 L ${points[0].x} 175 Z`
  return { lineD, areaD, points }
})

// Sales by Channel
const channelData = ref([
  { name: 'Online Store', pct: 68, color: '#84261B' },
  { name: 'Skin Quiz', pct: 16, color: '#D97768' },
  { name: 'Social Commerce', pct: 9, color: '#E89D91' },
  { name: 'Retail Partner', pct: 5, color: '#F3C7C0' },
  { name: 'Others', pct: 2, color: '#EFE7E0' }
])

// Order Status Breakdowns
const orderStatusData = ref([
  { name: 'Completed', pct: 68, color: '#84261B' },
  { name: 'Processing', pct: 18, color: '#D97768' },
  { name: 'Pending', pct: 8, color: '#D4A373' },
  { name: 'Cancelled', pct: 4, color: '#EAA49B' },
  { name: 'Returned', pct: 2, color: '#EAD9CF' }
])

// Top Products Ranking
const topProducts = ref([
  { id: 1, name: 'Brightening Face Serum', sold: 432, revenue: 8640, image: '/images/prod-sk2.jpg' },
  { id: 2, name: 'Hydrating Moisturizer', sold: 318, revenue: 6360, image: '/images/prod-lamer.jpg' },
  { id: 3, name: 'Gentle Cleanser', sold: 275, revenue: 4950, image: '/images/prod-sulwhasoo.jpg' },
  { id: 4, name: 'Vitamin C Serum', sold: 198, revenue: 3960, image: '/images/prod-anr.jpg' },
  { id: 5, name: 'Soothing Sheet Mask', sold: 176, revenue: 2640, image: '/images/prod-sheetmask.jpg' }
])

// Traffic Sources
const trafficSources = ref([
  { source: 'Direct', pct: 32, color: '#84261B' },
  { source: 'Organic Search', pct: 24, color: '#9E3529' },
  { source: 'Social Media', pct: 18, color: '#C86252' },
  { source: 'Paid Ads', pct: 14, color: '#E08C80' },
  { source: 'Email', pct: 8, color: '#EEB7AD' },
  { source: 'Referral', pct: 4, color: '#F4D4CE' }
])

// Sales by Category
const salesByCategory = ref([
  { category: 'Skincare', revenue: 14280, orders: 512, growth: '+18%' },
  { category: 'Sun Care', revenue: 4960, orders: 186, growth: '+12%' },
  { category: 'Body Care', revenue: 3420, orders: 124, growth: '+8%' },
  { category: 'Beauty Tools', revenue: 1860, orders: 70, growth: '+25%' },
  { category: 'Others', revenue: 330, orders: 20, growth: '+5%' }
])

// Customer Segments
const customerSegments = ref([
  { segment: 'New Customers', icon: Users, customers: 312, revenue: 6420, growth: '+28%' },
  { segment: 'Returning Customers', icon: UserCheck, customers: 228, revenue: 12650, growth: '+16%' },
  { segment: 'VIP Customers', icon: Sparkles, customers: 84, revenue: 5780, growth: '+22%' },
  { segment: 'Skin Quiz Users', icon: Star, customers: 410, revenue: 15320, growth: '+36%' }
])

// Recent Activities Feed
const recentActivities = ref([
  { id: 1, title: 'New order #10028', meta: '2 minutes ago', value: '$68.00', icon: ShoppingBag, color: 'text-crimson' },
  { id: 2, title: 'New customer registered', meta: '12 minutes ago', value: 'Srey Pov', icon: Users, color: 'text-blue' },
  { id: 3, title: 'New review submitted', meta: '25 minutes ago', value: '5 stars', icon: Star, color: 'text-amber' },
  { id: 4, title: 'Return request #R1004', meta: '1 hour ago', value: 'Pending', icon: RotateCcw, color: 'text-orange' },
  { id: 5, title: 'Order #10027 completed', meta: '2 hours ago', value: '$42.00', icon: CheckCircle2, color: 'text-green' }
])

const exportReport = () => {
  alert('Exporting executive analytics report (PDF/CSV)...')
}
</script>

<template>
  <div class="analytics-page">
    <!-- Top Hero Banner matching format mockup -->
    <div class="analytics-hero-card">
      <div class="hero-left">
        <span class="hero-eyebrow">Analytics</span>
        <h1 class="hero-heading">Analytics Dashboard</h1>
        <p class="hero-subtext">Insights that help you grow a healthier, brighter tomorrow.</p>
      </div>

      <div class="hero-right">
        <div class="hero-visual-callout">
          <img
            src="/images/admin-hero-bottles.jpg"
            alt="Luméa Botanical Formulation"
            class="hero-bottles"
            @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
          />
          <div class="hero-motto">
            <span class="motto-line">Data today.</span>
            <span class="motto-line highlight">A more beautiful</span>
            <span class="motto-line highlight">tomorrow.</span>
          </div>
        </div>

        <div class="hero-actions">
          <button class="date-range-picker-btn">
            <Calendar :size="15" />
            <span>{{ selectedTimeframe }}</span>
            <ChevronDown :size="14" />
          </button>
          <button class="btn-export-report" @click="exportReport">
            <Download :size="15" />
            <span>Export Report</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 4 Pastel KPI Metric Cards -->
    <div class="kpi-grid">
      <div
        v-for="kpi in kpiStats"
        :key="kpi.id"
        class="card kpi-card"
      >
        <div class="kpi-icon-pill" :class="`pill-${kpi.color}`">
          <component :is="kpi.icon" :size="18" />
        </div>
        <div class="kpi-meta">
          <span class="kpi-label">{{ kpi.label }}</span>
          <div class="kpi-value-row">
            <strong class="kpi-val">{{ kpi.value }}</strong>
          </div>
          <div class="kpi-trend-row">
            <span class="trend-indicator">
              <ArrowUpRight :size="13" />
              {{ kpi.trend }}
            </span>
            <span class="trend-sub">{{ kpi.trendText }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Row 1: Revenue Overview + Sales by Channel + Top Products -->
    <div class="analytics-row-3">
      <!-- 1. Revenue Overview (Dual Line & Bars) -->
      <div class="card chart-card revenue-card">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">Revenue Overview</h3>
            <div class="revenue-big-stat">
              <span class="big-val">$24,850</span>
              <span class="trend-badge-pill">
                <ArrowUpRight :size="13" /> +12%
                <span class="trend-light">vs last month</span>
              </span>
            </div>
          </div>
          <div class="chart-controls">
            <span class="chart-legend-bullet">
              <span class="dot-crimson"></span> Revenue
            </span>
            <div class="pill-dropdown">
              <span>Orders</span>
              <ChevronDown :size="13" />
            </div>
          </div>
        </div>

        <div class="chart-viewport">
          <svg viewBox="0 0 500 200" class="revenue-svg">
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#EAA49B" stop-opacity="0.6"/>
                <stop offset="100%" stop-color="#F7E6E2" stop-opacity="0.1"/>
              </linearGradient>
            </defs>

            <!-- Horizontal Grid lines -->
            <line x1="20" y1="30" x2="480" y2="30" stroke="#F1E8E2" stroke-dasharray="3,3" />
            <line x1="20" y1="70" x2="480" y2="70" stroke="#F1E8E2" stroke-dasharray="3,3" />
            <line x1="20" y1="110" x2="480" y2="110" stroke="#F1E8E2" stroke-dasharray="3,3" />
            <line x1="20" y1="150" x2="480" y2="150" stroke="#F1E8E2" stroke-dasharray="3,3" />

            <!-- Orders Bars -->
            <rect x="85" y="85" width="20" height="75" rx="3" fill="url(#barGradient)" />
            <rect x="160" y="60" width="20" height="100" rx="3" fill="url(#barGradient)" />
            <rect x="235" y="75" width="20" height="85" rx="3" fill="url(#barGradient)" />
            <rect x="310" y="45" width="20" height="115" rx="3" fill="url(#barGradient)" />
            <rect x="385" y="55" width="20" height="105" rx="3" fill="url(#barGradient)" />
            <rect x="460" y="35" width="20" height="125" rx="3" fill="url(#barGradient)" />

            <!-- Revenue Line Curve -->
            <path
              :d="revenueSvgPath.d"
              fill="none"
              stroke="#84261B"
              stroke-width="2.5"
              stroke-linecap="round"
            />

            <!-- Points on curve -->
            <circle
              v-for="(p, idx) in revenueSvgPath.points"
              :key="idx"
              :cx="p.x"
              :cy="p.y"
              r="3.5"
              fill="#FFFFFF"
              stroke="#84261B"
              stroke-width="2"
            />

            <!-- Labels X Axis -->
            <text x="20" y="185" class="svg-axis-label">Aug 1</text>
            <text x="95" y="185" class="svg-axis-label">Aug 5</text>
            <text x="170" y="185" class="svg-axis-label">Aug 10</text>
            <text x="245" y="185" class="svg-axis-label">Aug 15</text>
            <text x="320" y="185" class="svg-axis-label">Aug 20</text>
            <text x="395" y="185" class="svg-axis-label">Aug 25</text>
            <text x="465" y="185" class="svg-axis-label">Aug 31</text>
          </svg>
        </div>
      </div>

      <!-- 2. Sales by Channel Donut -->
      <div class="card chart-card channel-card">
        <h3 class="chart-title">Sales by Channel</h3>

        <div class="donut-container">
          <div class="donut-graphic-wrap">
            <svg viewBox="0 0 160 160" class="donut-svg">
              <!-- Background ring -->
              <circle cx="80" cy="80" r="54" fill="transparent" stroke="#F5ECE6" stroke-width="20" />
              <!-- Segments using stroke-dasharray (circumference = ~339.29) -->
              <!-- Online Store 68% = 230.7 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#84261B"
                stroke-width="20"
                stroke-dasharray="230.7 339.29"
                stroke-dashoffset="0"
                transform="rotate(-90 80 80)"
              />
              <!-- Skin Quiz 16% = 54.3 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#D97768"
                stroke-width="20"
                stroke-dasharray="54.3 339.29"
                stroke-dashoffset="-230.7"
                transform="rotate(-90 80 80)"
              />
              <!-- Social Commerce 9% = 30.5 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#E89D91"
                stroke-width="20"
                stroke-dasharray="30.5 339.29"
                stroke-dashoffset="-285"
                transform="rotate(-90 80 80)"
              />
              <!-- Retail Partner 5% = 17 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#F3C7C0"
                stroke-width="20"
                stroke-dasharray="17 339.29"
                stroke-dashoffset="-315.5"
                transform="rotate(-90 80 80)"
              />
            </svg>
            <div class="donut-center-label">
              <strong class="donut-val">$24,850</strong>
              <span class="donut-sub">Total Revenue</span>
            </div>
          </div>

          <div class="channel-legend-list">
            <div
              v-for="ch in channelData"
              :key="ch.name"
              class="channel-legend-item"
            >
              <div class="legend-color-dot" :style="{ backgroundColor: ch.color }"></div>
              <span class="legend-ch-name">{{ ch.name }}</span>
              <span class="legend-ch-pct">{{ ch.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Top Products Ranking -->
      <div class="card chart-card top-products-card">
        <div class="card-header-row">
          <h3 class="chart-title">Top Products</h3>
          <router-link to="/products" class="view-all-link">
            View All <ArrowUpRight :size="13" />
          </router-link>
        </div>

        <div class="top-products-list">
          <div
            v-for="item in topProducts"
            :key="item.id"
            class="top-product-item"
          >
            <span class="rank-num">{{ item.id }}</span>
            <img
              :src="item.image"
              :alt="item.name"
              class="prod-thumb"
              @error="$event.target.src = '/images/prod-sk2.jpg'"
            />
            <div class="prod-info">
              <h4 class="prod-name">{{ item.name }}</h4>
              <span class="prod-sold">{{ item.sold }} sold</span>
            </div>
            <strong class="prod-rev">${{ formatCurrency(item.revenue) }}</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- Row 2: Customer Growth + Order Status + Traffic Sources -->
    <div class="analytics-row-3">
      <!-- 1. Customer Growth Area -->
      <div class="card chart-card">
        <div class="chart-header">
          <div>
            <h3 class="chart-title">Customer Growth</h3>
            <div class="growth-stat-row">
              <span class="big-val">624</span>
              <span class="trend-badge-pill">
                <ArrowUpRight :size="13" /> +15%
                <span class="trend-light">vs last month</span>
              </span>
            </div>
          </div>
          <div class="pill-dropdown">
            <span>{{ growthInterval }}</span>
            <ChevronDown :size="13" />
          </div>
        </div>

        <div class="chart-viewport">
          <svg viewBox="0 0 380 190" class="growth-svg">
            <defs>
              <linearGradient id="growthAreaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#EAA49B" stop-opacity="0.35"/>
                <stop offset="100%" stop-color="#FDF7F5" stop-opacity="0.0"/>
              </linearGradient>
            </defs>

            <!-- Grid Lines -->
            <line x1="20" y1="40" x2="360" y2="40" stroke="#F1E8E2" stroke-dasharray="2,2" />
            <line x1="20" y1="80" x2="360" y2="80" stroke="#F1E8E2" stroke-dasharray="2,2" />
            <line x1="20" y1="120" x2="360" y2="120" stroke="#F1E8E2" stroke-dasharray="2,2" />
            <line x1="20" y1="160" x2="360" y2="160" stroke="#F1E8E2" />

            <!-- Area & Line -->
            <path :d="customerGrowthPath.areaD" fill="url(#growthAreaGradient)" />
            <path
              :d="customerGrowthPath.lineD"
              fill="none"
              stroke="#D97768"
              stroke-width="2"
              stroke-linecap="round"
            />

            <!-- Points -->
            <circle
              v-for="(p, idx) in customerGrowthPath.points"
              :key="idx"
              :cx="p.x"
              :cy="p.y"
              r="3"
              fill="#FFFFFF"
              stroke="#D97768"
              stroke-width="2"
            />

            <!-- X Labels -->
            <text x="20" y="178" class="svg-axis-label">Aug 1</text>
            <text x="75" y="178" class="svg-axis-label">Aug 5</text>
            <text x="130" y="178" class="svg-axis-label">Aug 10</text>
            <text x="185" y="178" class="svg-axis-label">Aug 15</text>
            <text x="240" y="178" class="svg-axis-label">Aug 20</text>
            <text x="295" y="178" class="svg-axis-label">Aug 25</text>
            <text x="345" y="178" class="svg-axis-label">Aug 31</text>
          </svg>
        </div>
      </div>

      <!-- 2. Order Status Donut -->
      <div class="card chart-card">
        <h3 class="chart-title">Order Status</h3>

        <div class="donut-container">
          <div class="donut-graphic-wrap">
            <svg viewBox="0 0 160 160" class="donut-svg">
              <circle cx="80" cy="80" r="54" fill="transparent" stroke="#F5ECE6" stroke-width="20" />
              <!-- Completed 68% = 230.7 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#84261B"
                stroke-width="20"
                stroke-dasharray="230.7 339.29"
                transform="rotate(-90 80 80)"
              />
              <!-- Processing 18% = 61 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#D97768"
                stroke-width="20"
                stroke-dasharray="61 339.29"
                stroke-dashoffset="-230.7"
                transform="rotate(-90 80 80)"
              />
              <!-- Pending 8% = 27 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#D4A373"
                stroke-width="20"
                stroke-dasharray="27 339.29"
                stroke-dashoffset="-291.7"
                transform="rotate(-90 80 80)"
              />
              <!-- Cancelled 4% = 13.5 -->
              <circle
                cx="80" cy="80" r="54"
                fill="transparent"
                stroke="#EAA49B"
                stroke-width="20"
                stroke-dasharray="13.5 339.29"
                stroke-dashoffset="-318.7"
                transform="rotate(-90 80 80)"
              />
            </svg>
            <div class="donut-center-label">
              <strong class="donut-val">892</strong>
              <span class="donut-sub">Total Orders</span>
            </div>
          </div>

          <div class="channel-legend-list">
            <div
              v-for="st in orderStatusData"
              :key="st.name"
              class="channel-legend-item"
            >
              <div class="legend-color-dot" :style="{ backgroundColor: st.color }"></div>
              <span class="legend-ch-name">{{ st.name }}</span>
              <span class="legend-ch-pct">{{ st.pct }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Traffic Sources -->
      <div class="card chart-card">
        <div class="card-header-row">
          <h3 class="chart-title">Traffic Sources</h3>
          <span class="view-all-link">View All <ArrowUpRight :size="13" /></span>
        </div>

        <div class="traffic-sources-list">
          <div
            v-for="t in trafficSources"
            :key="t.source"
            class="traffic-source-row"
          >
            <span class="traffic-source-name">{{ t.source }}</span>
            <div class="traffic-bar-track">
              <div
                class="traffic-bar-fill"
                :style="{ width: `${t.pct * 2.8}px`, backgroundColor: t.color }"
              ></div>
            </div>
            <span class="traffic-source-pct">{{ t.pct }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Row 3: Sales by Category + Top Customer Segments + Recent Activities -->
    <div class="analytics-row-3">
      <!-- 1. Sales by Category Table -->
      <div class="card table-panel-card">
        <div class="card-header-row">
          <h3 class="chart-title">Sales by Category</h3>
          <router-link to="/categories" class="view-all-link">
            View All <ArrowUpRight :size="13" />
          </router-link>
        </div>

        <table class="atelier-table">
          <thead>
            <tr>
              <th>Category</th>
              <th class="text-right">Revenue</th>
              <th class="text-center">Orders</th>
              <th class="text-right">Growth</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in salesByCategory" :key="cat.category">
              <td>
                <div class="cat-cell">
                  <div class="cat-icon-badge">
                    <Package :size="13" />
                  </div>
                  <span class="table-text-strong">{{ cat.category }}</span>
                </div>
              </td>
              <td class="text-right font-medium">${{ formatCurrency(cat.revenue) }}</td>
              <td class="text-center text-muted">{{ cat.orders }}</td>
              <td class="text-right">
                <span class="growth-green">{{ cat.growth }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 2. Top Customer Segments Table -->
      <div class="card table-panel-card">
        <div class="card-header-row">
          <h3 class="chart-title">Top Customer Segments</h3>
          <router-link to="/customers" class="view-all-link">
            View All <ArrowUpRight :size="13" />
          </router-link>
        </div>

        <table class="atelier-table">
          <thead>
            <tr>
              <th>Segment</th>
              <th class="text-center">Customers</th>
              <th class="text-right">Revenue</th>
              <th class="text-right">Growth</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="seg in customerSegments" :key="seg.segment">
              <td>
                <div class="cat-cell">
                  <div class="seg-icon-badge">
                    <component :is="seg.icon" :size="13" />
                  </div>
                  <span class="table-text-strong">{{ seg.segment }}</span>
                </div>
              </td>
              <td class="text-center text-muted">{{ seg.customers }}</td>
              <td class="text-right font-medium">${{ formatCurrency(seg.revenue) }}</td>
              <td class="text-right">
                <span class="growth-green">{{ seg.growth }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 3. Recent Activities Feed -->
      <div class="card table-panel-card">
        <div class="card-header-row">
          <h3 class="chart-title">Recent Activities</h3>
          <router-link to="/orders" class="view-all-link">
            View All <ArrowUpRight :size="13" />
          </router-link>
        </div>

        <div class="activities-list">
          <div
            v-for="act in recentActivities"
            :key="act.id"
            class="activity-row"
          >
            <div class="activity-icon-pill" :class="act.color">
              <component :is="act.icon" :size="14" />
            </div>
            <div class="activity-content">
              <span class="act-title">{{ act.title }}</span>
              <span class="act-meta">{{ act.meta }}</span>
            </div>
            <strong class="act-val">{{ act.value }}</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analytics-page {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* Hero Banner matching Luméa Skincare Analytics Dashboard.png */
.analytics-hero-card {
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
  max-width: 440px;
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
  position: relative;
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

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.date-range-picker-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #3C3530;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.date-range-picker-btn:hover {
  border-color: #84261B;
}

.btn-export-report {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #84261B;
  border-radius: 8px;
  color: #84261B;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-export-report:hover {
  background: #84261B;
  color: #FFFFFF;
}

/* 4 KPI Grid */
.kpi-grid {
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

.pill-crimson {
  background: #F8E9E4;
  color: #84261B;
}

.pill-peach {
  background: #FAF0E8;
  color: #C4623C;
}

.pill-rose {
  background: #FDF0EE;
  color: #D97768;
}

.pill-coral {
  background: #FBF1ED;
  color: #A03B2E;
}

.kpi-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
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
  letter-spacing: -0.01em;
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
  color: #2E7D32;
  font-weight: 600;
}

.trend-sub {
  color: #8C847E;
}

/* 3-Column Rows */
.analytics-row-3 {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 18px;
}

.chart-card,
.table-panel-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.chart-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D2621;
}

.view-all-link {
  font-size: 12px;
  color: #84261B;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  cursor: pointer;
}

.view-all-link:hover {
  text-decoration: underline;
}

.revenue-big-stat,
.growth-stat-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-top: 4px;
}

.big-val {
  font-size: 24px;
  font-weight: 800;
  color: #2D2621;
  letter-spacing: -0.02em;
}

.trend-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11.5px;
  font-weight: 600;
  color: #2E7D32;
}

.trend-light {
  color: #8C847E;
  font-weight: 400;
  margin-left: 2px;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}

.chart-legend-bullet {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #5C544E;
}

.dot-crimson {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #84261B;
}

.pill-dropdown {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  font-size: 12px;
  color: #3C3530;
  background: #FAF7F4;
  cursor: pointer;
}

.chart-viewport {
  margin-top: auto;
  width: 100%;
}

.revenue-svg,
.growth-svg {
  width: 100%;
  height: auto;
  overflow: visible;
}

.svg-axis-label {
  font-size: 10px;
  fill: #9C948E;
  text-anchor: middle;
}

/* Donut Styles */
.donut-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  margin-top: 6px;
}

.donut-graphic-wrap {
  position: relative;
  width: 160px;
  height: 160px;
}

.donut-svg {
  width: 100%;
  height: 100%;
}

.donut-center-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  display: flex;
  flex-direction: column;
}

.donut-val {
  font-size: 18px;
  font-weight: 800;
  color: #2D2621;
}

.donut-sub {
  font-size: 10px;
  color: #8C847E;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.channel-legend-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  width: 100%;
}

.channel-legend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.legend-color-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-right: 8px;
}

.legend-ch-name {
  color: #5C544E;
  flex: 1;
}

.legend-ch-pct {
  font-weight: 600;
  color: #2D2621;
}

/* Top Products List */
.top-products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.top-product-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rank-num {
  font-size: 12px;
  font-weight: 700;
  color: #8C847E;
  width: 14px;
}

.prod-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  object-fit: cover;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
}

.prod-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.prod-name {
  font-size: 12.5px;
  font-weight: 600;
  color: #2D2621;
  line-height: 1.3;
}

.prod-sold {
  font-size: 11px;
  color: #8C847E;
}

.prod-rev {
  font-size: 12.5px;
  font-weight: 700;
  color: #2D2621;
}

/* Traffic Sources */
.traffic-sources-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.traffic-source-row {
  display: grid;
  grid-template-columns: 100px 1fr 35px;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.traffic-source-name {
  color: #5C544E;
}

.traffic-bar-track {
  height: 8px;
  background: #FAF5F2;
  border-radius: 99px;
  overflow: hidden;
}

.traffic-bar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.3s ease;
}

.traffic-source-pct {
  font-weight: 600;
  color: #2D2621;
  text-align: right;
}

/* Atelier Tables */
.atelier-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.atelier-table th {
  padding: 8px 10px;
  color: #8C847E;
  font-weight: 500;
  border-bottom: 1px solid #EFE7E0;
  background: #FAF7F4;
  font-size: 11px;
}

.atelier-table td {
  padding: 10px;
  border-bottom: 1px solid #F5ECE6;
  color: #3C3530;
}

.cat-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cat-icon-badge,
.seg-icon-badge {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #F8E9E4;
  color: #84261B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-text-strong {
  font-weight: 600;
  color: #2D2621;
}

.growth-green {
  color: #2E7D32;
  font-weight: 600;
}

/* Recent Activities */
.activities-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-icon-pill {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #FAF5F2;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.text-crimson { color: #84261B; background: #F8E9E4; }
.text-blue { color: #1E6091; background: #EAF4FA; }
.text-amber { color: #B25E00; background: #FEF7ED; }
.text-orange { color: #C4623C; background: #FAF0E8; }
.text-green { color: #2E7D32; background: #E8F5E9; }

.activity-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.act-title {
  font-size: 12px;
  font-weight: 600;
  color: #2D2621;
}

.act-meta {
  font-size: 10.5px;
  color: #8C847E;
}

.act-val {
  font-size: 12px;
  font-weight: 700;
  color: #2D2621;
}

@media (max-width: 1200px) {
  .analytics-row-3 {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
