<template>
  <div class="shop-skeleton-stencil" aria-hidden="true" role="status" aria-label="Loading catalog">
    <div class="skeleton-container">
      <!-- 1. Breadcrumbs Stencil -->
      <div class="skeleton-breadcrumbs">
        <div class="stencil-line shimmer breadcrumb-item"></div>
        <div class="stencil-line shimmer breadcrumb-sep"></div>
        <div class="stencil-line shimmer breadcrumb-current"></div>
      </div>

      <!-- 2. Hero Banner Stencil -->
      <div class="skeleton-shop-hero shimmer">
        <div class="skeleton-hero-left">
          <div class="stencil-line shimmer shop-title-line"></div>
          <div class="stencil-line shimmer shop-sub-line"></div>
          <div class="skeleton-badges-row">
            <div v-for="n in 4" :key="n" class="stencil-pill shimmer badge-pill"></div>
          </div>
        </div>
        <div class="skeleton-hero-right">
          <div class="stencil-hero-circle shimmer"></div>
        </div>
      </div>

      <!-- 3. Popular Brands Row Stencil -->
      <div class="skeleton-brands-bar">
        <div class="stencil-line shimmer brands-heading"></div>
        <div class="skeleton-brands-carousel">
          <div v-for="n in 8" :key="n" class="stencil-circle shimmer brand-circle-stencil"></div>
        </div>
      </div>

      <!-- 4. Two-Column Catalog Layout Stencil -->
      <div class="skeleton-catalog-layout">
        <!-- Left Sidebar Filter Stencil -->
        <aside class="skeleton-sidebar">
          <div class="skeleton-sidebar-card">
            <div class="stencil-line shimmer filter-title"></div>
            <div class="skeleton-filter-block" v-for="b in 3" :key="b">
              <div class="stencil-line shimmer filter-heading"></div>
              <div class="stencil-line shimmer filter-row" v-for="r in 4" :key="r"></div>
            </div>
          </div>
        </aside>

        <!-- Right Catalog Main Stencil -->
        <main class="skeleton-catalog-main">
          <div class="skeleton-sort-bar">
            <div class="stencil-line shimmer count-line"></div>
            <div class="stencil-pill shimmer sort-pill"></div>
          </div>

          <div class="skeleton-products-grid">
            <ProductCardSkeleton v-for="n in 9" :key="n" />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import ProductCardSkeleton from './ProductCardSkeleton.vue'
</script>

<style scoped>
.shop-skeleton-stencil {
  width: 100%;
  background: #FAF8F5;
  padding: 1.5rem 0 5rem;
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
  background: linear-gradient(90deg, #E8DFD7 0%, #FAF8F5 50%, #E8DFD7 100%);
  background-size: 200% 100%;
  animation: lumeaShimmer 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  box-shadow: inset 0 0 0 1px rgba(28, 25, 23, 0.07);
}

@keyframes lumeaShimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.stencil-line { border-radius: 6px; }
.stencil-pill { border-radius: 999px; }
.stencil-circle { border-radius: 50%; }

/* 1. Breadcrumbs */
.skeleton-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 1.5rem;
}

.breadcrumb-item { width: 50px; height: 12px; }
.breadcrumb-sep { width: 10px; height: 12px; }
.breadcrumb-current { width: 60px; height: 12px; }

/* 2. Hero Banner */
.skeleton-shop-hero {
  border-radius: 16px;
  padding: 2.5rem 3rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  min-height: 180px;
}

.skeleton-hero-left {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  max-width: 60%;
}

.shop-title-line { width: 280px; height: 38px; }
.shop-sub-line { width: 420px; height: 16px; margin-bottom: 0.5rem; }

.skeleton-badges-row {
  display: flex;
  gap: 1rem;
}

.badge-pill { width: 110px; height: 26px; }

.skeleton-hero-right {
  display: flex;
  align-items: center;
  justify-content: center;
}

.stencil-hero-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
}

/* 3. Brands Bar */
.skeleton-brands-bar {
  margin-bottom: 2.5rem;
}

.brands-heading { width: 140px; height: 18px; margin-bottom: 1rem; }

.skeleton-brands-carousel {
  display: flex;
  gap: 1.25rem;
}

.brand-circle-stencil { width: 62px; height: 62px; flex-shrink: 0; }

/* 4. Two-Column Catalog */
.skeleton-catalog-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 2.5rem;
}

.skeleton-sidebar-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.filter-title { width: 90px; height: 20px; }

.skeleton-filter-block {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-heading { width: 120px; height: 14px; margin-bottom: 4px; }
.filter-row { width: 85%; height: 12px; }

.skeleton-sort-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
}

.count-line { width: 120px; height: 14px; }
.sort-pill { width: 150px; height: 32px; }

.skeleton-products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

@media (max-width: 900px) {
  .skeleton-catalog-layout {
    grid-template-columns: 1fr;
  }
  .skeleton-sidebar {
    display: none;
  }
  .skeleton-products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
