<script setup>
import { TrendingDown, TrendingUp } from 'lucide-vue-next'

defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  change: {
    type: String,
    default: '',
  },
  isPositive: {
    type: Boolean,
    default: true,
  },
  prefix: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: 'gold', // 'gold', 'emerald', 'amber', 'purple', 'blue'
  },
})
</script>

<template>
  <div class="metric-card card" :class="`metric-${color}`">
    <div class="metric-top">
      <span class="metric-title">{{ title }}</span>
      <div class="metric-icon-box">
        <slot name="icon"></slot>
      </div>
    </div>

    <div class="metric-value-row">
      <span class="metric-value">
        <span class="metric-prefix" v-if="prefix">{{ prefix }}</span>
        {{ typeof value === 'number' ? value.toLocaleString() : value }}
      </span>
    </div>

    <div class="metric-footer" v-if="change">
      <span class="metric-trend" :class="isPositive ? 'trend-up' : 'trend-down'">
        <TrendingUp v-if="isPositive" :size="14" />
        <TrendingDown v-else :size="14" />
        {{ change }}
      </span>
      <span class="metric-period">vs past 30 days</span>
    </div>
  </div>
</template>

<style scoped>
.metric-card {
  padding: 1.35rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: linear-gradient(180deg, var(--bg-surface) 0%, rgba(20, 23, 33, 0.7) 100%);
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent 0%, var(--accent-border) 50%, transparent 100%);
  opacity: 0.8;
}

.metric-gold { --accent-border: var(--gold); }
.metric-emerald { --accent-border: var(--emerald); }
.metric-amber { --accent-border: var(--amber); }
.metric-purple { --accent-border: var(--purple); }
.metric-blue { --accent-border: var(--blue); }

.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.metric-title {
  font-size: 0.82rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.metric-icon-box {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-medium);
  color: var(--text-main);
  transition: transform var(--transition-fast);
}

.metric-card:hover .metric-icon-box {
  transform: scale(1.08);
  border-color: var(--accent-border);
  color: var(--accent-border);
}

.metric-value-row {
  margin-top: 0.2rem;
}

.metric-value {
  font-family: var(--font-serif);
  font-size: 1.85rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.2;
}

.metric-prefix {
  font-size: 1.3rem;
  font-family: var(--font-sans);
  color: var(--text-muted);
  font-weight: 400;
  margin-right: 2px;
}

.metric-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.78rem;
}

.metric-trend {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-weight: 600;
}

.trend-up {
  color: var(--emerald);
}

.trend-down {
  color: var(--rose);
}

.metric-period {
  color: var(--text-dim);
}
</style>
