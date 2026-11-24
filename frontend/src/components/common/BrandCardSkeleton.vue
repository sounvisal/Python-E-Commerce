<template>
  <div class="brand-skeleton-card" aria-hidden="true">
    <div class="skeleton-logo-wrap shimmer"></div>
    <div class="skeleton-count-line shimmer"></div>
  </div>
</template>

<script setup>
// Presentation skeleton for brand directory cards
</script>

<style scoped>
.brand-skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.85rem;
  min-height: 140px;
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

.skeleton-logo-wrap {
  width: 60px;
  height: 60px;
  border-radius: 50%;
}

.skeleton-count-line {
  width: 70px;
  height: 12px;
  border-radius: 4px;
}
</style>
