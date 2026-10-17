<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
})

const activeIndex = ref(null)

// Fallback timeline data if API data empty
const chartData = computed(() => {
  if (props.data && props.data.length > 0) {
    return props.data
  }
  return [
    { label: 'Mon', revenue: 495, orders: 1 },
    { label: 'Tue', revenue: 780, orders: 2 },
    { label: 'Wed', revenue: 1044, orders: 2 },
    { label: 'Thu', revenue: 620, orders: 1 },
    { label: 'Fri', revenue: 1645, orders: 2 },
    { label: 'Sat', revenue: 980, orders: 2 },
    { label: 'Sun', revenue: 1320, orders: 3 },
  ]
})

const width = 600
const height = 220
const padding = { top: 20, right: 20, bottom: 35, left: 45 }

const innerWidth = width - padding.left - padding.right
const innerHeight = height - padding.top - padding.bottom

const maxRevenue = computed(() => {
  const max = Math.max(...chartData.value.map((d) => d.revenue || 0), 100)
  return Math.ceil(max / 500) * 500
})

const points = computed(() => {
  const count = chartData.value.length
  if (count === 0) return []

  return chartData.value.map((d, index) => {
    const x = padding.left + (index / (count - 1 || 1)) * innerWidth
    const y = padding.top + innerHeight - ((d.revenue || 0) / maxRevenue.value) * innerHeight
    return { x, y, data: d, index }
  })
})

const pathD = computed(() => {
  const pts = points.value
  if (pts.length === 0) return ''

  let d = `M ${pts[0].x} ${pts[0].y}`
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i]
    const p1 = pts[i + 1]
    const cx = (p0.x + p1.x) / 2
    d += ` C ${cx} ${p0.y}, ${cx} ${p1.y}, ${p1.x} ${p1.y}`
  }
  return d
})

const areaD = computed(() => {
  const line = pathD.value
  if (!line) return ''
  const pts = points.value
  const first = pts[0]
  const last = pts[pts.length - 1]
  const bottomY = padding.top + innerHeight
  return `${line} L ${last.x} ${bottomY} L ${first.x} ${bottomY} Z`
})

const yTicks = computed(() => {
  return [0, maxRevenue.value / 2, maxRevenue.value]
})

function formatCurrency(val) {
  return '$' + Number(val).toLocaleString()
}
</script>

<template>
  <div class="revenue-chart-container">
    <div class="chart-tooltip" v-if="activeIndex !== null && points[activeIndex]">
      <div class="tooltip-date">{{ points[activeIndex].data.label }}</div>
      <div class="tooltip-val">
        <span class="tooltip-revenue">{{ formatCurrency(points[activeIndex].data.revenue) }}</span>
        <span class="tooltip-orders">{{ points[activeIndex].data.orders || 0 }} orders</span>
      </div>
    </div>

    <svg :viewBox="`0 0 ${width} ${height}`" preserveAspectRatio="none" class="chart-svg">
      <defs>
        <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#C29B38" stop-opacity="0.38" />
          <stop offset="100%" stop-color="#C29B38" stop-opacity="0.0" />
        </linearGradient>
      </defs>

      <!-- Grid lines -->
      <g class="chart-grid">
        <line
          v-for="tick in yTicks"
          :key="tick"
          :x1="padding.left"
          :y1="padding.top + innerHeight - (tick / maxRevenue) * innerHeight"
          :x2="width - padding.right"
          :y2="padding.top + innerHeight - (tick / maxRevenue) * innerHeight"
          stroke="rgba(255,255,255,0.06)"
          stroke-dasharray="3,3"
        />
        <!-- Y-axis labels -->
        <text
          v-for="tick in yTicks"
          :key="`lbl-${tick}`"
          :x="padding.left - 8"
          :y="padding.top + innerHeight - (tick / maxRevenue) * innerHeight + 4"
          text-anchor="end"
          class="axis-label"
        >
          ${{ tick }}
        </text>
      </g>

      <!-- Area fill -->
      <path :d="areaD" fill="url(#chartGradient)" />

      <!-- Curved line -->
      <path :d="pathD" fill="none" stroke="#C29B38" stroke-width="2.5" class="chart-line" />

      <!-- Interactive points -->
      <g v-for="pt in points" :key="pt.index">
        <!-- Vertical guide line on active -->
        <line
          v-if="activeIndex === pt.index"
          :x1="pt.x"
          :y1="padding.top"
          :x2="pt.x"
          :y2="padding.top + innerHeight"
          stroke="rgba(194, 155, 56, 0.4)"
          stroke-width="1.5"
          stroke-dasharray="2,2"
        />

        <!-- Point dot -->
        <circle
          :cx="pt.x"
          :cy="pt.y"
          :r="activeIndex === pt.index ? 6 : 4"
          fill="#141721"
          stroke="#C29B38"
          :stroke-width="activeIndex === pt.index ? 3 : 2"
          class="point-circle"
        />

        <!-- Invisible hover target -->
        <rect
          :x="pt.x - 20"
          :y="padding.top"
          width="40"
          :height="innerHeight + padding.bottom"
          fill="transparent"
          style="cursor: pointer"
          @mouseenter="activeIndex = pt.index"
          @mouseleave="activeIndex = null"
        />

        <!-- X-axis label -->
        <text
          :x="pt.x"
          :y="height - 10"
          text-anchor="middle"
          class="axis-label"
          :class="{ 'label-active': activeIndex === pt.index }"
        >
          {{ pt.data.label }}
        </text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.revenue-chart-container {
  position: relative;
  width: 100%;
  height: 240px;
}

.chart-svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.axis-label {
  font-family: var(--font-sans);
  font-size: 11px;
  fill: var(--text-dim);
  user-select: none;
}

.label-active {
  fill: var(--gold);
  font-weight: 600;
}

.point-circle {
  transition: r 0.2s ease, stroke-width 0.2s ease;
}

.chart-tooltip {
  position: absolute;
  top: -10px;
  right: 10px;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--gold-border);
  box-shadow: var(--shadow-md);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  pointer-events: none;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: fadeIn 0.15s ease;
}

.tooltip-date {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.tooltip-val {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.tooltip-revenue {
  font-family: var(--font-serif);
  font-weight: 600;
  color: var(--gold);
  font-size: 0.95rem;
}

.tooltip-orders {
  font-size: 0.72rem;
  color: var(--text-dim);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
