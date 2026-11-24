<template>
  <div class="product-card skeleton-product-card" aria-hidden="true">
    <!-- Image Stage Stencil -->
    <div class="image-wrapper skeleton-shimmer">
      <div class="skeleton-heart-placeholder"></div>
      <div class="skeleton-badge-placeholder"></div>
    </div>

    <!-- Product Info Stencil -->
    <div class="product-info">
      <div class="brand-row">
        <div class="skeleton-line skeleton-shimmer brand-line"></div>
      </div>

      <div class="title-wrap">
        <div class="skeleton-line skeleton-shimmer title-line-1"></div>
        <div class="skeleton-line skeleton-shimmer title-line-2"></div>
      </div>

      <div class="rating-wrap">
        <div class="skeleton-line skeleton-shimmer stars-line"></div>
      </div>

      <div class="price-action-group">
        <div class="skeleton-line skeleton-shimmer price-line"></div>
        <div class="skeleton-btn-placeholder skeleton-shimmer"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Pure presentation skeleton matching ProductCard dimensions
</script>

<style scoped>
.skeleton-product-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 12px;
  overflow: hidden;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  position: relative;
  user-select: none;
  pointer-events: none;
}

.image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 8px;
  background: #F4EFEB;
  margin-bottom: 0.85rem;
  overflow: hidden;
}

.skeleton-shimmer {
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

.skeleton-heart-placeholder {
  position: absolute;
  top: 0.65rem;
  right: 0.65rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
}

.skeleton-badge-placeholder {
  position: absolute;
  top: 0.65rem;
  left: 0.65rem;
  width: 48px;
  height: 18px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.7);
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  flex: 1;
}

.skeleton-line {
  border-radius: 4px;
  height: 12px;
}

.brand-line {
  width: 40%;
  height: 10px;
  margin-bottom: 2px;
}

.title-wrap {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 4px;
}

.title-line-1 {
  width: 88%;
  height: 14px;
}

.title-line-2 {
  width: 62%;
  height: 14px;
}

.rating-wrap {
  margin-bottom: 4px;
}

.stars-line {
  width: 36%;
  height: 10px;
}

.price-action-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 0.5rem;
}

.price-line {
  width: 38%;
  height: 16px;
  border-radius: 4px;
}

.skeleton-btn-placeholder {
  width: 34px;
  height: 34px;
  border-radius: 50%;
}
</style>
