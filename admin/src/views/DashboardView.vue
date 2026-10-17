<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import StatusBadge from '@/components/common/StatusBadge.vue'
import {
  TrendingUp,
  ShoppingBag,
  Users,
  Package,
  Plus,
  Store,
  Tag,
  FileText,
  ChevronRight,
  ArrowRight,
  Clock,
  RotateCcw,
  Sparkles
} from 'lucide-vue-next'

const router = useRouter()
const adminStore = useAdminStore()

const salesTimeframe = ref('this-month')

onMounted(async () => {
  await Promise.all([
    adminStore.fetchStats(),
    adminStore.fetchOrders({ limit: 10 }),
    adminStore.fetchProducts({ limit: 10 })
  ])
})

const metrics = computed(() => {
  return adminStore.stats?.metrics || {
    total_revenue: 24580,
    total_orders: 320,
    total_customers: 4125,
    total_products: 560,
  }
})

// Quick Actions
const quickActions = [
  { name: 'Add Product', path: '/products', icon: Package },
  { name: 'Add Brand', path: '/brands', icon: Store },
  { name: 'Create Promotion', path: '/promotions', icon: Tag },
  { name: 'View Orders', path: '/orders', icon: FileText },
]

// Low Stock Products matching mockup
const lowStockProducts = [
  { id: 1, name: 'Hydrating Toner', stock: 5, status: 'Low Stock', class: 'badge-amber', img: '/images/prod-sk2.jpg' },
  { id: 2, name: 'Vitamin C Serum', stock: 8, status: 'Low Stock', class: 'badge-amber', img: '/images/prod-ordinary.jpg' },
  { id: 3, name: 'Gentle Cleanser', stock: 12, status: 'Normal', class: 'badge-emerald', img: '/images/prod-cosrx.jpg' },
  { id: 4, name: 'Daily Sunscreen', stock: 3, status: 'Low Stock', class: 'badge-amber', img: '/images/prod-laneige.jpg' },
]

// Top Products matching mockup
const topProducts = [
  { rank: 1, name: 'Hydrating Toner', sold: 320, revenue: 1240, img: '/images/prod-sk2.jpg' },
  { rank: 2, name: 'Vitamin C Serum', sold: 210, revenue: 980, img: '/images/prod-ordinary.jpg' },
  { rank: 3, name: 'Gentle Cleanser', sold: 180, revenue: 870, img: '/images/prod-cosrx.jpg' },
  { rank: 4, name: 'Daily Sunscreen', sold: 150, revenue: 760, img: '/images/prod-laneige.jpg' },
  { rank: 5, name: 'Acne Treatment', sold: 120, revenue: 680, img: '/images/prod-sk2.jpg' },
]

// Recent Returns matching mockup
const recentReturns = [
  { id: '#RT-0012', reason: 'Wrong item', status: 'Under Review', class: 'badge-amber' },
  { id: '#RT-0011', reason: 'Product damaged', status: 'Approved', class: 'badge-emerald' },
  { id: '#RT-0010', reason: 'Not suitable', status: 'Processing', class: 'badge-blue' },
  { id: '#RT-0009', reason: 'Change of mind', status: 'Completed', class: 'badge-emerald' },
]

// Recent Orders matching mockup or fallback to live DB
const recentOrders = computed(() => {
  if (adminStore.orders && adminStore.orders.length > 0) {
    return adminStore.orders.slice(0, 5)
  }
  return [
    { order_number: 'LUM-00124', customer_name: 'Sophea Chan', total: 58.0, status: 'Processing', created_at: 'Aug 30, 2025' },
    { order_number: 'LUM-00123', customer_name: 'Dara Kim', total: 24.5, status: 'Shipped', created_at: 'Aug 30, 2025' },
    { order_number: 'LUM-00122', customer_name: 'Kimheang Lim', total: 96.0, status: 'Pending', created_at: 'Aug 29, 2025' },
    { order_number: 'LUM-00121', customer_name: 'Sreypov Neang', total: 48.0, status: 'Delivered', created_at: 'Aug 29, 2025' },
    { order_number: 'LUM-00120', customer_name: 'Vannak Sok', total: 32.0, status: 'Processing', created_at: 'Aug 28, 2025' },
  ]
})

function formatCurrency(val) {
  return Number(val || 0).toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 2 })
}
</script>

<template>
  <div class="dashboard-page">
    <!-- Top Row: Welcome Banner + Quick Actions matching format/Luméa Beauty Admin Dashboard.png -->
    <div class="dashboard-top-grid">
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

      <!-- Quick Actions Card matching mockup -->
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
            <strong class="kpi-value">${{ formatCurrency(metrics.total_revenue || 24580) }}</strong>
            <span class="kpi-label">Total Sales</span>
          </div>
        </div>
        <div class="kpi-bottom">
          <span class="kpi-trend text-green">↑ +12%</span>
          <span class="kpi-period">vs last month</span>
          <svg class="mini-sparkline" viewBox="0 0 70 20" fill="none">
            <path d="M2 16 Q 20 18, 35 12 T 68 4" stroke="#C4623C" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
      </div>

      <!-- 2. Orders -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Package :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ metrics.total_orders || 320 }}</strong>
            <span class="kpi-label">Orders</span>
          </div>
        </div>
        <div class="kpi-bottom">
          <span class="kpi-trend text-green">↑ +8%</span>
          <span class="kpi-period">vs last month</span>
          <svg class="mini-sparkline" viewBox="0 0 70 20" fill="none">
            <path d="M2 17 Q 25 15, 40 10 T 68 5" stroke="#C4623C" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
      </div>

      <!-- 3. Customers -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Users :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ formatCurrency(metrics.total_customers || 4125) }}</strong>
            <span class="kpi-label">Customers</span>
          </div>
        </div>
        <div class="kpi-bottom">
          <span class="kpi-trend text-green">↑ +15%</span>
          <span class="kpi-period">vs last month</span>
          <svg class="mini-sparkline" viewBox="0 0 70 20" fill="none">
            <path d="M2 18 Q 20 14, 45 12 T 68 3" stroke="#C4623C" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
      </div>

      <!-- 4. Products -->
      <div class="card kpi-card">
        <div class="kpi-top">
          <div class="kpi-icon-box red-icon">
            <Tag :size="18" />
          </div>
          <div class="kpi-numbers">
            <strong class="kpi-value">{{ metrics.total_products || 560 }}</strong>
            <span class="kpi-label">Products</span>
          </div>
        </div>
        <div class="kpi-bottom">
          <span class="kpi-trend text-green">↑ +6%</span>
          <span class="kpi-period">vs last month</span>
          <svg class="mini-sparkline" viewBox="0 0 70 20" fill="none">
            <path d="M2 16 Q 25 16, 45 11 T 68 6" stroke="#C4623C" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Mid Section: Sales Overview Chart + Order Status Donut + Low Stock Widget -->
    <div class="dashboard-mid-grid">
      <!-- Sales Overview Chart Box -->
      <div class="card sales-overview-box">
        <div class="card-head-row">
          <h3 class="panel-card-title">Sales Overview</h3>
          <div class="select-timeframe">
            <select v-model="salesTimeframe">
              <option value="this-month">This Month</option>
              <option value="last-30">Last 30 Days</option>
              <option value="this-year">This Year</option>
            </select>
          </div>
        </div>

        <!-- Sales Chart Canvas SVG matching mockup -->
        <div class="sales-chart-wrap">
          <div class="chart-y-axis">
            <span>30K</span>
            <span>20K</span>
            <span>10K</span>
            <span>0</span>
          </div>
          <div class="chart-drawing-area">
            <svg class="sales-curve-svg" viewBox="0 0 500 160" preserveAspectRatio="none">
              <!-- Gradient definition -->
              <defs>
                <linearGradient id="salesGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#84261B" stop-opacity="0.25" />
                  <stop offset="100%" stop-color="#84261B" stop-opacity="0.0" />
                </linearGradient>
              </defs>
              <!-- Filled Area -->
              <path
                d="M 10 145 C 50 140, 70 100, 110 88 C 150 78, 170 115, 220 95 C 270 75, 310 100, 360 82 C 410 65, 450 72, 485 35 L 485 155 L 10 155 Z"
                fill="url(#salesGrad)"
              />
              <!-- Smooth Curve Line -->
              <path
                d="M 10 145 C 50 140, 70 100, 110 88 C 150 78, 170 115, 220 95 C 270 75, 310 100, 360 82 C 410 65, 450 72, 485 35"
                fill="none"
                stroke="#84261B"
                stroke-width="2.5"
                stroke-linecap="round"
              />
              <!-- Active Highlight Dot -->
              <circle cx="485" cy="35" r="5" fill="#84261B" />
              <circle cx="485" cy="35" r="9" fill="none" stroke="rgba(132, 38, 27, 0.3)" stroke-width="2" />
            </svg>

            <!-- Peak Callout Badge -->
            <div class="chart-callout-badge" style="top: 15px; right: 5px;">
              $24,580
            </div>

            <div class="chart-x-axis">
              <span>Aug 1</span>
              <span>Aug 7</span>
              <span>Aug 14</span>
              <span>Aug 21</span>
              <span>Aug 31</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Status Donut Card matching mockup -->
      <div class="card order-status-box">
        <h3 class="panel-card-title">Order Status</h3>

        <div class="donut-and-legend">
          <!-- Donut SVG -->
          <div class="donut-wrap">
            <svg class="donut-svg" viewBox="0 0 120 120">
              <!-- Background Ring -->
              <circle cx="60" cy="60" r="46" fill="none" stroke="#F6EFE9" stroke-width="14"/>
              <!-- Delivered Segment (Crimson #84261B) -->
              <circle cx="60" cy="60" r="46" fill="none" stroke="#84261B" stroke-width="14"
                stroke-dasharray="144 289" stroke-dashoffset="0"/>
              <!-- Shipped Segment (Coral #C4623C) -->
              <circle cx="60" cy="60" r="46" fill="none" stroke="#C4623C" stroke-width="14"
                stroke-dasharray="65 289" stroke-dashoffset="-144"/>
              <!-- Processing Segment (Peach #E89E88) -->
              <circle cx="60" cy="60" r="46" fill="none" stroke="#E89E88" stroke-width="14"
                stroke-dasharray="45 289" stroke-dashoffset="-209"/>
              <!-- Pending Segment (Gold #D9B36C) -->
              <circle cx="60" cy="60" r="46" fill="none" stroke="#D9B36C" stroke-width="14"
                stroke-dasharray="35 289" stroke-dashoffset="-254"/>
            </svg>
            <div class="donut-center-text">
              <strong class="donut-total">320</strong>
              <span class="donut-label">Total Orders</span>
            </div>
          </div>

          <!-- Status Legend matching mockup -->
          <div class="donut-legend-col">
            <div class="legend-row">
              <span class="dot-color" style="background-color: #D9B36C;"></span>
              <span class="legend-name">Pending</span>
              <strong class="legend-val">48</strong>
            </div>
            <div class="legend-row">
              <span class="dot-color" style="background-color: #E89E88;"></span>
              <span class="legend-name">Processing</span>
              <strong class="legend-val">72</strong>
            </div>
            <div class="legend-row">
              <span class="dot-color" style="background-color: #C4623C;"></span>
              <span class="legend-name">Shipped</span>
              <strong class="legend-val">120</strong>
            </div>
            <div class="legend-row">
              <span class="dot-color" style="background-color: #84261B;"></span>
              <span class="legend-name">Delivered</span>
              <strong class="legend-val">320</strong>
            </div>
            <div class="legend-row">
              <span class="dot-color" style="background-color: #A89D95;"></span>
              <span class="legend-name">Cancelled</span>
              <strong class="legend-val">12</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Low Stock Products Box matching mockup -->
      <div class="card low-stock-box">
        <div class="card-head-row">
          <h3 class="panel-card-title">Low Stock Products</h3>
          <router-link to="/products?stock=low" class="view-all-link">View all</router-link>
        </div>

        <div class="low-stock-list">
          <div
            v-for="item in lowStockProducts"
            :key="item.id"
            class="low-stock-row"
          >
            <img :src="item.img" :alt="item.name" class="stock-item-thumb" />
            <div class="stock-item-meta">
              <strong>{{ item.name }}</strong>
              <span class="stock-left-sub">{{ item.stock }} left</span>
            </div>
            <span class="badge" :class="item.class">{{ item.status }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Section: Recent Orders + Top Products + Recent Returns -->
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
              <tr v-for="order in recentOrders" :key="order.order_number || order.id">
                <td>
                  <span class="order-hash-id">#{{ order.order_number }}</span>
                </td>
                <td>
                  <span class="customer-name-bold">{{ order.customer_name }}</span>
                </td>
                <td>
                  <div class="mini-thumbs-stack">
                    <img src="/images/prod-sk2.jpg" alt="Item" class="table-item-micro" />
                    <img src="/images/prod-ordinary.jpg" alt="Item" class="table-item-micro" />
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
                <th>Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in topProducts" :key="prod.rank">
                <td>{{ prod.rank }}</td>
                <td>
                  <div class="product-cell-flex">
                    <img :src="prod.img" :alt="prod.name" class="table-item-micro" />
                    <span class="prod-name-text">{{ prod.name }}</span>
                  </div>
                </td>
                <td>{{ prod.sold }}</td>
                <td>
                  <strong>${{ Number(prod.revenue).toLocaleString() }}</strong>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Recent Returns List matching mockup -->
      <div class="card recent-returns-panel">
        <div class="card-head-row">
          <h3 class="panel-card-title">Recent Returns</h3>
          <router-link to="/returns" class="view-all-link">View all</router-link>
        </div>

        <div class="returns-items-list">
          <div
            v-for="ret in recentReturns"
            :key="ret.id"
            class="return-item-row"
          >
            <div class="return-id-reason">
              <strong class="return-hash">{{ ret.id }}</strong>
              <span class="return-reason-text">{{ ret.reason }}</span>
            </div>
            <span class="badge" :class="ret.class">{{ ret.status }}</span>
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
          <a href="http://localhost:5173/contact" target="_blank" rel="noopener">Help & Support</a>
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

/* Top Row: Welcome Banner + Quick Actions */
.dashboard-top-grid {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 1.5rem;
}

@media (max-width: 1100px) {
  .dashboard-top-grid {
    grid-template-columns: 1fr;
  }
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
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

@media (max-width: 900px) {
  .kpi-metrics-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 550px) {
  .kpi-metrics-row {
    grid-template-columns: 1fr;
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

/* Mid Section: Chart + Donut + Low Stock */
.dashboard-mid-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1fr;
  gap: 1.25rem;
}

@media (max-width: 1200px) {
  .dashboard-mid-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-mid-grid {
    grid-template-columns: 1fr;
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
  height: 180px;
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

/* Bottom Grid: Recent Orders + Top Products + Returns */
.dashboard-bottom-grid {
  display: grid;
  grid-template-columns: 1.4fr 1.1fr 1fr;
  gap: 1.25rem;
}

@media (max-width: 1200px) {
  .dashboard-bottom-grid {
    grid-template-columns: 1fr;
  }
}

.order-hash-id {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--crimson);
}

.customer-name-bold {
  font-weight: 500;
  color: var(--text-main);
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
}

.product-cell-flex {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.prod-name-text {
  font-size: 0.82rem;
  color: var(--text-main);
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

.return-id-reason {
  display: flex;
  flex-direction: column;
  line-height: 1.25;
}

.return-hash {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-main);
}

.return-reason-text {
  font-size: 0.74rem;
  color: var(--text-muted);
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
