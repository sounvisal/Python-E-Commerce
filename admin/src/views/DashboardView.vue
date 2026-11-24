<script setup>
import { computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { getStorefrontUrl } from '@/utils/storefront'
import StatusBadge from '@/components/common/StatusBadge.vue'
import {
  ShoppingBag,
  Users,
  Package,
  Store,
  Tag,
  FileText,
  ChevronRight
} from 'lucide-vue-next'

const adminStore = useAdminStore()

onMounted(() => adminStore.fetchStats())

const metrics = computed(() => adminStore.stats?.metrics)
const recentOrders = computed(() => (adminStore.stats?.recent_orders || []).slice(0, 5))
const topProducts = computed(() => adminStore.stats?.top_products || [])
const lowStockProducts = computed(() => adminStore.stats?.low_stock_products || [])
const recentReturns = computed(() => adminStore.stats?.recent_returns || [])
const salesSeries = computed(() => adminStore.stats?.timeline || [])
const chartMax = computed(() => Math.max(3, Math.ceil(Math.max(0, ...salesSeries.value.map(day => day.revenue)) / 3) * 3))
const salesPoints = computed(() => salesSeries.value.map((day, index, series) => ({
  x: index * 500 / Math.max(series.length - 1, 1),
  y: 150 - 145 * day.revenue / chartMax.value,
})))
const salesLine = computed(() => salesPoints.value.map(point => `${point.x},${point.y}`).join(' '))

const statusColors = {
  'awaiting confirmation': '#D9B36C',
  pending: '#E7C98D',
  confirmed: '#A77C53',
  processing: '#E89E88',
  shipped: '#C4623C',
  'out for delivery': '#A34532',
  delivered: '#84261B',
  cancelled: '#A89D95',
  expired: '#756C65',
  'payment review': '#9B779B',
}
const statusSegments = computed(() => {
  const counts = adminStore.stats?.orders_by_status || {}
  const sum = Object.values(counts).reduce((total, count) => total + count, 0)
  let start = 0
  return Object.entries(counts).filter(([, count]) => count > 0).map(([state, count]) => {
    const end = start + count / sum * 100
    const segment = { state, count, color: statusColors[state] || '#756C65', start, end }
    start = end
    return segment
  })
})
const statusBackground = computed(() => statusSegments.value.length
  ? `conic-gradient(${statusSegments.value.map(segment => `${segment.color} ${segment.start}% ${segment.end}%`).join(', ')})`
  : '#F6EFE9'
)

// Quick Actions
const quickActions = [
  { name: 'Add Product', path: '/products', icon: Package },
  { name: 'Add Brand', path: '/brands', icon: Store },
  { name: 'Create Promotion', path: '/promotions', icon: Tag },
  { name: 'View Orders', path: '/orders', icon: FileText },
]

function formatCurrency(val) {
  return val == null ? '—' : Number(val).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}
</script>

<template>
  <div class="dashboard-page">
    <div v-if="adminStore.statsLoading && !metrics" role="status">Loading dashboard…</div>
    <div v-else-if="!metrics" role="alert" class="dashboard-error">
      Dashboard data is unavailable.
      <button type="button" class="view-all-link" @click="adminStore.fetchStats()">Retry</button>
    </div>
    <div class="dashboard-split-layout">
      <!-- ============================================== -->
      <!-- MAIN COLUMN (LEFT): Hero, KPIs, Charts, Orders -->
      <!-- ============================================== -->
      <div class="dashboard-main-col">
        <!-- Welcome Hero Banner -->
        <div class="hero-welcome-card">
          <div class="hero-content">
            <span class="hero-eyebrow">WELCOME BACK, ADMIN</span>
            <h1 class="hero-heading">
              Manage beauty.<br/>
              Create brighter tomorrows.
            </h1>
            <p class="hero-subtext">From products to people, everything in one place.</p>
          </div>
          <div class="hero-graphic-wrap">
            <img
              src="/images/admin-hero-bottles.jpg"
              alt="Luméa Atelier"
              class="hero-bottles-img"
              @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
            />
          </div>
        </div>

    <!-- 4 Pastel KPI Metric Cards matching mockup -->
    <div class="kpi-metrics-row">
      <!-- 1. Total Sales -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <ShoppingBag :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ metrics ? '$' + formatCurrency(metrics.total_revenue) : '—' }}</strong>
            <span class="kpi-label">Total Sales</span>
          </div>
        </div>
      </div>

      <!-- 2. Orders -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Package :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ formatCurrency(metrics?.total_orders) }}</strong>
            <span class="kpi-label">Orders</span>
          </div>
        </div>
      </div>

      <!-- 3. Customers -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Users :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ formatCurrency(metrics?.total_customers) }}</strong>
            <span class="kpi-label">Customers</span>
          </div>
        </div>
      </div>

      <!-- 4. Products -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Tag :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ formatCurrency(metrics?.total_products) }}</strong>
            <span class="kpi-label">Products</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Mid Section: Sales Overview Chart + Order Status Donut + Low Stock Widget -->
    <div class="dashboard-mid-grid">
      <!-- Sales Overview Chart Box -->
      <div class="card sales-overview-box">
        <div class="card-head-row">
          <h3 class="panel-card-title">Sales Overview</h3>
          <span class="chart-period">Last 7 days</span>
        </div>
        <div v-if="salesSeries.length" class="sales-chart-wrap">
          <div class="chart-y-axis">
            <span v-for="step in [3, 2, 1, 0]" :key="step">{{ formatCurrency(chartMax / 3 * step) }}</span>
          </div>
          <div class="chart-drawing-area">
            <svg class="sales-curve-svg" viewBox="0 0 500 155" preserveAspectRatio="none" role="img"
              :aria-label="salesSeries.map(day => day.date + ' $' + formatCurrency(day.revenue)).join(', ')">
              <polyline :points="salesLine" fill="none" stroke="#84261B" stroke-width="2.5"
                vector-effect="non-scaling-stroke" />
            </svg>
            <div class="chart-x-axis">
              <span v-for="day in salesSeries" :key="day.date">{{ day.date }}</span>
            </div>
          </div>
        </div>
        <p v-else-if="metrics" class="dashboard-empty">No sales data for this period.</p>
      </div>

      <div class="card order-status-box">
        <h3 class="panel-card-title">Order Status</h3>
        <div class="donut-and-legend">
          <div class="donut-wrap" :style="{ background: statusBackground }">
            <div class="donut-center-text">
              <strong class="donut-total">{{ formatCurrency(metrics?.total_orders) }}</strong>
              <span class="donut-label">Total Orders</span>
            </div>
          </div>
          <div v-if="statusSegments.length" class="donut-legend-col">
            <div v-for="segment in statusSegments" :key="segment.state" class="legend-row">
              <span class="dot-color" :style="{ backgroundColor: segment.color }"></span>
              <span class="legend-name">{{ segment.state }}</span>
              <strong class="legend-val">{{ segment.count }}</strong>
            </div>
          </div>
          <p v-else-if="metrics" class="dashboard-empty">No orders yet.</p>
        </div>
      </div>
    </div>

    <!-- Bottom Section: Recent Orders + Top Products (Spacious 2-column layout) -->
    <div class="dashboard-bottom-grid">
      <!-- Recent Orders Table -->
      <div class="card recent-orders-panel">
        <div class="card-head-row">
          <h3 class="panel-card-title">Recent Orders</h3>
          <router-link to="/orders" class="view-all-link">View all</router-link>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Customer</th>
                <th>Products</th>
                <th>Total</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="metrics && !recentOrders.length"><td colspan="6">No orders yet.</td></tr>
              <tr v-for="order in recentOrders" :key="order.order_number || order.id">
                <td>
                  <span class="order-hash-id">#{{ order.order_number }}</span>
                </td>
                <td>
                  <span class="customer-name-bold">{{ order.customer_name }}</span>
                </td>
                <td>
                  <div class="mini-thumbs-stack">
                    <img v-for="item in (order.items || []).filter(item => item.image_url).slice(0, 2)" :key="item.id"
                      :src="item.image_url" :alt="item.product_name" class="table-item-micro" />
                  </div>
                </td>
                <td>
                  <strong>${{ Number(order.total).toFixed(2) }}</strong>
                </td>
                <td>
                  <StatusBadge :status="order.status" />
                </td>
                <td>
                  <span class="date-dim">{{ order.created_at ? order.created_at.substring(0, 10) : 'Aug 30, 2025' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Top Products Table -->
      <div class="card top-products-panel">
        <div class="card-head-row">
          <h3 class="panel-card-title">Top Products</h3>
          <router-link to="/products" class="view-all-link">View all</router-link>
        </div>

        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Product</th>
                <th>Sold</th>
                <th>Item sales</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="metrics && !topProducts.length"><td colspan="4">No paid product sales yet.</td></tr>
              <tr v-for="(prod, index) in topProducts" :key="prod.id">
                <td>{{ index + 1 }}</td>
                <td>
                  <div class="product-cell-flex">
                    <img :src="prod.image_url" :alt="prod.name" class="table-item-micro" />
                    <span class="prod-name-text">{{ prod.name }}</span>
                  </div>
                </td>
                <td>{{ prod.sold }}</td>
                <td>
                  <strong>${{ formatCurrency(prod.sales) }}</strong>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- ============================================== -->
  <!-- SIDEBAR COLUMN (RIGHT): Actions, Stock, Returns -->
  <!-- ============================================== -->
  <div class="dashboard-side-col">
    <!-- 1. Quick Actions Card matching mockup -->
    <div class="card quick-actions-card">
      <h3 class="panel-card-title">Quick Actions</h3>
      <div class="actions-list">
        <router-link
          v-for="action in quickActions"
          :key="action.name"
          :to="action.path"
          class="action-item-row"
        >
          <div class="action-icon-box">
            <component :is="action.icon" :size="16" />
          </div>
          <span class="action-label">{{ action.name }}</span>
          <ChevronRight :size="14" class="action-arrow" />
        </router-link>
      </div>
    </div>

    <!-- 2. Low Stock Products Box matching mockup -->
    <div class="card low-stock-box">
      <div class="card-head-row">
        <h3 class="panel-card-title">Low Stock Products</h3>
        <router-link to="/products?stock=low" class="view-all-link">View all</router-link>
      </div>

      <div class="low-stock-list">
        <p v-if="metrics && !lowStockProducts.length" class="dashboard-empty">No low-stock products.</p>
        <div
          v-for="item in lowStockProducts"
          :key="item.id"
          class="low-stock-row"
        >
          <img :src="item.image_url" :alt="item.name" class="stock-item-thumb" />
          <div class="stock-item-meta">
            <strong>{{ item.name }}</strong>
            <span class="stock-left-sub">{{ item.stock }} left</span>
          </div>
          <span class="badge badge-amber">Low stock</span>
        </div>
      </div>
    </div>

    <!-- 3. Recent Returns List matching mockup -->
    <div class="card recent-returns-panel">
      <div class="card-head-row">
        <h3 class="panel-card-title">Recent Returns</h3>
        <router-link to="/returns" class="view-all-link">View all</router-link>
      </div>

      <div class="returns-items-list">
        <p v-if="metrics && !recentReturns.length" class="dashboard-empty">No returns yet.</p>
        <div
          v-for="ret in recentReturns"
          :key="ret.request_number"
          class="return-item-row"
        >
          <div class="return-id-reason">
            <strong class="return-hash">{{ ret.request_number }}</strong>
            <span class="return-reason-text">{{ ret.reason }}</span>
          </div>
          <StatusBadge :status="ret.status" />
        </div>
      </div>
    </div>
  </div>
</div>

    <!-- Atelier Footer Strip matching mockup -->
    <footer class="atelier-dashboard-footer">
      <div class="footer-left">
        <span>© 2025 Luméa. All rights reserved.</span>
        <div class="footer-links-row">
          <router-link to="/settings">Privacy Policy</router-link>
          <span>|</span>
          <router-link to="/settings">Terms of Service</router-link>
          <span>|</span>
          <a :href="getStorefrontUrl('/contact')" target="_blank" rel="noopener">Help & Support</a>
        </div>
      </div>

      <div class="footer-right">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="#84261B">
          <path d="M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1-2.3A4.49 4.49 0 0 0 8 20C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75C7 8 17 8 17 8z"/>
        </svg>
        <span class="footer-slogan">Skincare for a Brighter Tomorrow.</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 2-Column Split Layout matching mockup */
.dashboard-split-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 310px);
  gap: 1.5rem;
  align-items: flex-start;
}

@media (max-width: 1200px) {
  .dashboard-split-layout {
    grid-template-columns: minmax(0, 1fr);
  }
}

.dashboard-main-col {
  container-type: inline-size;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0;
}

.dashboard-side-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 0;
}

.hero-welcome-card {
  background: #FDF9F5;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 2rem 2.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.hero-content {
  max-width: 480px;
  z-index: 2;
}

.hero-eyebrow {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #A3978E;
  margin-bottom: 0.4rem;
}

.hero-heading {
  font-family: var(--font-serif);
  font-size: 1.85rem;
  color: var(--crimson);
  line-height: 1.25;
  margin-bottom: 0.5rem;
}

.hero-subtext {
  font-size: 0.88rem;
  color: var(--text-muted);
}

.hero-graphic-wrap {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 50%;
  pointer-events: none;
}

.hero-bottles-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Quick Actions */
.quick-actions-card {
  display: flex;
  flex-direction: column;
  padding: 1.25rem;
}

.panel-card-title {
  font-family: var(--font-sans);
  font-size: 0.96rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.85rem;
}

.actions-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.action-item-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.55rem 0.65rem;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: #FFFFFF;
  transition: all var(--transition-fast);
}

.action-item-row:hover {
  background: #FAF6F2;
  border-color: var(--crimson-border);
}

.action-icon-box {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-xs);
  background: var(--crimson-subtle);
  color: var(--crimson);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-label {
  flex: 1;
  font-size: 0.84rem;
  font-weight: 500;
  color: var(--text-main);
}

.action-arrow {
  color: var(--text-dim);
}

/* KPI Metrics */
.kpi-metrics-row {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.25rem;
}

@container (max-width: 780px) {
  .kpi-metrics-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@container (max-width: 400px) {
  .kpi-metrics-row {
    grid-template-columns: minmax(0, 1fr);
  }
}

.kpi-card {
  padding: 1.25rem 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.kpi-top {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.kpi-icon-box {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.red-icon {
  background-color: #FDF0EB;
  color: var(--crimson);
}

.kpi-numbers {
  display: flex;
  flex-direction: column;
}

.kpi-value {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.kpi-label {
  font-size: 0.76rem;
  color: var(--text-muted);
}

.kpi-bottom {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  border-top: 1px solid #FAF4EE;
  padding-top: 0.5rem;
}

.text-green {
  color: var(--emerald);
  font-weight: 600;
}

.kpi-period {
  color: var(--text-dim);
  flex: 1;
}

.mini-sparkline {
  width: 55px;
  height: 16px;
}

/* Mid Section: Chart + Donut */
.dashboard-mid-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  gap: 1.25rem;
}

@container (max-width: 760px) {
  .dashboard-mid-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

.card-head-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.view-all-link {
  font-size: 0.76rem;
  color: var(--crimson);
  font-weight: 600;
}

.select-timeframe select {
  font-size: 0.78rem;
  background: #FAF6F2;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xs);
  padding: 0.25rem 0.5rem;
  color: var(--text-main);
}

/* Sales Chart Box */
.sales-chart-wrap {
  display: flex;
  gap: 0.75rem;
  height: 180px;
}

.chart-y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-dim);
  padding-bottom: 22px;
}

.chart-drawing-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.sales-curve-svg {
  width: 100%;
  height: 155px;
}

.chart-callout-badge {
  position: absolute;
  background: var(--crimson);
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--radius-full);
}

.chart-x-axis {
  display: flex;
  justify-content: space-between;
  font-size: 0.72rem;
  color: var(--text-dim);
  margin-top: 4px;
}

/* Donut & Legend */
.donut-and-legend {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-height: 180px;
}

.donut-wrap {
  width: 120px;
  height: 120px;
  position: relative;
  flex-shrink: 0;
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
  text-align: center;
}

.donut-total {
  font-size: 1.25rem;
  color: var(--text-main);
  line-height: 1;
}

.donut-label {
  font-size: 0.65rem;
  color: var(--text-dim);
}

.donut-legend-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.76rem;
}

.dot-color {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-name {
  color: var(--text-muted);
  flex: 1;
}

.legend-val {
  color: var(--text-main);
  font-weight: 600;
}

/* Low Stock List */
.low-stock-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.low-stock-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.82rem;
}

.stock-item-thumb {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-xs);
  object-fit: cover;
  border: 1px solid var(--border-subtle);
}

.stock-item-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  line-height: 1.25;
}

.stock-item-meta strong {
  color: var(--text-main);
  font-size: 0.82rem;
}

.stock-left-sub {
  font-size: 0.72rem;
  color: var(--crimson);
}

/* Bottom Grid: Recent Orders + Top Products */
.dashboard-bottom-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(0, 1fr);
  gap: 1.25rem;
}

@container (max-width: 910px) {
  .dashboard-bottom-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

.dashboard-bottom-grid > .card {
  min-width: 0;
}
.dashboard-bottom-grid .table-container {
  overflow-x: auto;
}
.chart-period, .dashboard-empty {
  font-size: 0.8rem;
  color: var(--text-muted);
}
.chart-drawing-area {
  min-width: 0;
}
.chart-x-axis {
  gap: 0.25rem;
  flex-wrap: wrap;
}
.donut-wrap {
  border-radius: 50%;
  aspect-ratio: 1;
}
.donut-wrap .donut-center-text {
  inset: 12%;
  border-radius: 50%;
  background: #fff;
}
.donut-and-legend {
  flex-wrap: wrap;
}
.legend-name {
  text-transform: capitalize;
}

.order-hash-id {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--crimson);
  white-space: nowrap;
}

.customer-name-bold {
  font-weight: 500;
  color: var(--text-main);
  white-space: nowrap;
}

.mini-thumbs-stack {
  display: flex;
  gap: 4px;
}

.table-item-micro {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-xs);
  object-fit: cover;
  border: 1px solid var(--border-subtle);
}

.date-dim {
  font-size: 0.74rem;
  color: var(--text-dim);
  white-space: nowrap;
}

.product-cell-flex {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.prod-name-text {
  font-size: 0.82rem;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

.view-all-link {
  font-size: 0.76rem;
  color: var(--crimson);
  font-weight: 600;
  white-space: nowrap;
}

/* Returns Items List */
.returns-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.return-item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.return-item-row .badge {
  flex-shrink: 0;
  white-space: nowrap;
}

.return-id-reason {
  display: flex;
  flex-direction: column;
  line-height: 1.25;
}

.return-hash {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-main);
  white-space: nowrap;
}

.return-reason-text {
  font-size: 0.74rem;
  color: var(--text-muted);
  white-space: nowrap;
}

/* Dashboard Footer */
.atelier-dashboard-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1.25rem 0.5rem;
  border-top: 1px solid var(--border-subtle);
  font-size: 0.78rem;
  color: var(--text-muted);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.footer-links-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  color: var(--text-dim);
}

.footer-links-row a:hover {
  color: var(--crimson);
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.footer-slogan {
  font-family: var(--font-serif);
  font-style: italic;
  color: var(--crimson);
  font-size: 0.82rem;
}
</style>
