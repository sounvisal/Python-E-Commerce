<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
})

const hoveredIndex = ref(null)

const colors = [
  '#C29B38', // Gold
  '#C4623C', // Terracotta
  '#10B981', // Emerald
  '#3B82F6', // Blue
  '#8B5CF6', // Purple
  '#EC4899', // Pink
]

const items = computed(() => {
  if (props.categories && props.categories.length > 0) {
    return props.categories.map((c, i) => ({
      name: c.name,
      count: c.products_count || 1,
      color: colors[i % colors.length],
    }))
  }
  return [
    { name: 'Living & Furniture', count: 2, color: colors[0] },
    { name: 'Lighting & Ambience', count: 2, color: colors[1] },
    { name: 'Audio & Acoustics', count: 1, color: colors[2] },
    { name: 'Ceramics & Objects', count: 2, color: colors[3] },
    { name: 'Fragrance & Care', count: 1, color: colors[4] },
  ]
})

const total = computed(() => {
  return items.value.reduce((sum, item) => sum + item.count, 0) || 1
})

const radius = 65
const strokeWidth = 24
const circumference = 2 * Math.PI * radius

const slices = computed(() => {
  let accumulatedAngle = 0
  return items.value.map((item, index) => {
    const percentage = item.count / total.value
    const strokeDasharray = `${percentage * circumference} ${circumference}`
    const strokeDashoffset = -accumulatedAngle * circumference
    accumulatedAngle += percentage

    return {
      ...item,
      percentage: Math.round(percentage * 100),
      strokeDasharray,
      strokeDashoffset,
      index,
    }
  })
})
</script>

<template>
  <div class="donut-wrapper">
    <div class="donut-chart-box">
      <svg viewBox="0 0 180 180" class="donut-svg">
        <circle
          cx="90"
          cy="90"
          :r="radius"
          fill="none"
          stroke="rgba(255, 255, 255, 0.05)"
          :stroke-width="strokeWidth"
        />

        <circle
          v-for="slice in slices"
          :key="slice.index"
          cx="90"
          cy="90"
          :r="radius"
          fill="none"
          :stroke="slice.color"
          :stroke-width="hoveredIndex === slice.index ? strokeWidth + 4 : strokeWidth"
          :stroke-dasharray="slice.strokeDasharray"
          :stroke-dashoffset="slice.strokeDashoffset"
          stroke-linecap="butt"
          class="donut-slice"
          @mouseenter="hoveredIndex = slice.index"
          @mouseleave="hoveredIndex = null"
        />
      </svg>

      <div class="donut-center">
        <span class="donut-center-total">
          {{ hoveredIndex !== null ? slices[hoveredIndex].count : total }}
        </span>
        <span class="donut-center-label">
          {{ hoveredIndex !== null ? slices[hoveredIndex].name.split(' ')[0] : 'Works' }}
        </span>
      </div>
    </div>

    <!-- Legend list -->
    <div class="donut-legend">
      <div
        v-for="slice in slices"
        :key="`legend-${slice.index}`"
        class="legend-item"
        :class="{ 'legend-hovered': hoveredIndex === slice.index }"
        @mouseenter="hoveredIndex = slice.index"
        @mouseleave="hoveredIndex = null"
      >
        <div class="legend-indicator" :style="{ backgroundColor: slice.color }"></div>
        <span class="legend-name">{{ slice.name }}</span>
        <span class="legend-count">{{ slice.count }}</span>
        <span class="legend-pct">{{ slice.percentage }}%</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.donut-wrapper {
  display: flex;
  align-items: center;
  gap: 24px;
}

.donut-chart-box {
  position: relative;
  width: 150px;
  height: 150px;
  flex-shrink: 0;
}

.donut-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.donut-slice {
  cursor: pointer;
  transition: stroke-width 0.2s ease, opacity 0.2s ease;
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  pointer-events: none;
}

.donut-center-total {
  font-family: var(--font-serif);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1;
}

.donut-center-label {
  display: block;
  font-size: 0.7rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 2px;
}

.donut-legend {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: var(--radius-xs);
  transition: background-color var(--transition-fast);
  cursor: pointer;
}

.legend-item:hover,
.legend-hovered {
  background-color: rgba(255, 255, 255, 0.05);
}

.legend-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-name {
  flex: 1;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.legend-item:hover .legend-name,
.legend-hovered .legend-name {
  color: var(--text-main);
}

.legend-count {
  font-weight: 600;
  color: var(--text-main);
}

.legend-pct {
  color: var(--text-dim);
  font-size: 0.72rem;
  width: 30px;
  text-align: right;
}
</style>
