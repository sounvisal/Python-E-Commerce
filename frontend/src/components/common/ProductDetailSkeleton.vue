<template>
  <div class="product-detail-skeleton" aria-hidden="true" role="status" aria-label="Loading formulation details">
    <div class="skeleton-container">
      <!-- Breadcrumb Stencil -->
      <div class="skeleton-breadcrumbs">
        <div class="stencil-line shimmer breadcrumb-item"></div>
        <div class="stencil-line shimmer breadcrumb-sep"></div>
        <div class="stencil-line shimmer breadcrumb-item"></div>
        <div class="stencil-line shimmer breadcrumb-sep"></div>
        <div class="stencil-line shimmer breadcrumb-current"></div>
      </div>

      <!-- Main Product Stage -->
      <div class="skeleton-product-stage">
        <!-- Left Column: Gallery Stencil -->
        <div class="skeleton-gallery-col">
          <div class="stencil-main-image shimmer"></div>
          <div class="skeleton-thumbs-row">
            <div v-for="n in 4" :key="n" class="stencil-thumb shimmer"></div>
          </div>
        </div>

        <!-- Right Column: Specs & Purchase Stencil -->
        <div class="skeleton-specs-col">
          <div class="stencil-line shimmer brand-chip"></div>
          <div class="stencil-line shimmer product-headline-1"></div>
          <div class="stencil-line shimmer product-headline-2"></div>
          
          <div class="skeleton-rating-row">
            <div class="stencil-line shimmer rating-stars"></div>
            <div class="stencil-line shimmer rating-count"></div>
          </div>

          <div class="stencil-line shimmer price-box"></div>

          <div class="skeleton-benefits-box">
            <div class="stencil-line shimmer benefit-row" v-for="n in 4" :key="n"></div>
          </div>

          <div class="skeleton-actions-row">
            <div class="stencil-pill shimmer qty-selector"></div>
            <div class="stencil-pill shimmer add-bag-btn"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for ProductDetailView
</script>

<style scoped>
.product-detail-skeleton {
  width: 100%;
  background: #FAF8F5;
  padding: 2rem 0 5rem;
  user-select: none;
  pointer-events: none;
}

.skeleton-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

.shimmer {
  background: linear-gradient(90deg, #F3ECE6 0%, #FAF6F2 50%, #F3ECE6 100%);
  background-size: 200% 100%;
  animation: lumeaShimmer 1.6s ease-in-out infinite;
}

@keyframes lumeaShimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.stencil-line { border-radius: 6px; }
.stencil-pill { border-radius: 999px; }

/* Breadcrumbs */
.skeleton-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2rem;
}

.breadcrumb-item { width: 55px; height: 12px; }
.breadcrumb-sep { width: 8px; height: 12px; }
.breadcrumb-current { width: 120px; height: 12px; }

/* Main Stage */
.skeleton-product-stage {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: flex-start;
}

/* Gallery */
.skeleton-gallery-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.stencil-main-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 16px;
  background: #F4EFEB;
}

.skeleton-thumbs-row {
  display: flex;
  gap: 1rem;
}

.stencil-thumb {
  width: 80px;
  height: 80px;
  border-radius: 10px;
  background: #F4EFEB;
}

/* Specs */
.skeleton-specs-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.brand-chip { width: 110px; height: 14px; }
.product-headline-1 { width: 90%; height: 36px; }
.product-headline-2 { width: 65%; height: 36px; }

.skeleton-rating-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.rating-stars { width: 90px; height: 14px; }
.rating-count { width: 70px; height: 14px; }
.price-box { width: 140px; height: 32px; margin: 0.5rem 0; }

.skeleton-benefits-box {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.benefit-row { width: 85%; height: 12px; }

.skeleton-actions-row {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.qty-selector { width: 110px; height: 48px; }
.add-bag-btn { flex: 1; height: 48px; }

@media (max-width: 850px) {
  .skeleton-product-stage {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
