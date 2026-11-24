<template>
  <div class="order-skeleton-card" aria-hidden="true">
    <div class="order-meta-col">
      <div class="order-num-line shimmer"></div>
      <div class="order-date-line shimmer"></div>
    </div>

    <div class="order-thumbs-row">
      <div v-for="n in 3" :key="n" class="thumb-square shimmer"></div>
    </div>

    <div class="order-status-col">
      <div class="status-pill shimmer"></div>
      <div class="status-desc-line shimmer"></div>
    </div>

    <div class="order-actions-col">
      <div class="action-btn-line shimmer"></div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for My Orders record cards
</script>

<style scoped>
.order-skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1rem;
  user-select: none;
  pointer-events: none;
}

.shimmer {
  background: linear-gradient(90deg, #F4EFEB 0%, #E8DFD7 50%, #F4EFEB 100%);
  background-size: 200% 100%;
  animation: lumeaShimmer 1.6s ease-in-out infinite;
}

@keyframes lumeaShimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.order-meta-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  min-width: 130px;
}

.order-num-line {
  width: 120px;
  height: 16px;
  border-radius: 4px;
}

.order-date-line {
  width: 90px;
  height: 12px;
  border-radius: 3px;
}

.order-thumbs-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.thumb-square {
  width: 48px;
  height: 48px;
  border-radius: 8px;
}

.order-status-col {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.status-pill {
  width: 100px;
  height: 22px;
  border-radius: 11px;
}

.status-desc-line {
  width: 140px;
  height: 11px;
  border-radius: 3px;
}

.order-actions-col {
  display: flex;
  align-items: center;
}

.action-btn-line {
  width: 95px;
  height: 34px;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .order-skeleton-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
