<template>
  <div class="home-skeleton-stencil" aria-hidden="true" role="status" aria-label="Loading Luméa atelier content">
    <!-- 1. Hero Section Stencil -->
    <section class="skeleton-hero-section">
      <div class="skeleton-container skeleton-hero-grid">
        <!-- Hero Left Column -->
        <div class="skeleton-hero-copy">
          <div class="stencil-pill shimmer eyebrow-pill"></div>
          <div class="stencil-line shimmer headline-1"></div>
          <div class="stencil-line shimmer headline-2"></div>
          <div class="stencil-line shimmer desc-1"></div>
          <div class="stencil-line shimmer desc-2"></div>

          <div class="skeleton-cta-row">
            <div class="stencil-pill shimmer cta-btn-dark"></div>
            <div class="stencil-pill shimmer cta-btn-outline"></div>
          </div>

          <div class="skeleton-slider-bar">
            <div class="stencil-line shimmer slider-track"></div>
            <div class="skeleton-dots-row">
              <span class="stencil-dot shimmer"></span>
              <span class="stencil-dot shimmer"></span>
              <span class="stencil-dot shimmer"></span>
            </div>
          </div>
        </div>

        <!-- Hero Right Column -->
        <div class="skeleton-hero-visual">
          <div class="stencil-stage shimmer">
            <div class="stencil-callout-pill shimmer"></div>
            <div class="stencil-bottle-silhouette"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Brand Horizon Marquee Stencil -->
    <section class="skeleton-brands-strip">
      <div class="skeleton-brands-track">
        <div v-for="n in 10" :key="n" class="stencil-brand-pill shimmer"></div>
      </div>
    </section>

    <!-- 3. Categories Stencil -->
    <section class="skeleton-categories-section">
      <div class="skeleton-container">
        <div class="skeleton-section-header">
          <div class="stencil-line shimmer section-title-line"></div>
          <div class="stencil-line shimmer section-link-line"></div>
        </div>

        <div class="skeleton-categories-grid">
          <div v-for="n in 8" :key="n" class="skeleton-cat-card">
            <div class="stencil-circle shimmer cat-circle"></div>
            <div class="stencil-line shimmer cat-label"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Best Sellers Carousel Stencil -->
    <section class="skeleton-bestsellers-section">
      <div class="skeleton-container">
        <div class="skeleton-section-header">
          <div class="stencil-line shimmer section-title-line"></div>
          <div class="stencil-line shimmer section-link-line"></div>
        </div>

        <div class="skeleton-products-grid">
          <ProductCardSkeleton v-for="n in 5" :key="n" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import ProductCardSkeleton from './ProductCardSkeleton.vue'
</script>

<style scoped>
.home-skeleton-stencil {
  width: 100%;
  background: #FAF8F5;
  overflow: hidden;
  user-select: none;
  pointer-events: none;
}

.skeleton-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

/* Universal Shimmer Effect with Luméa Bisque Palette */
.shimmer {
  background: linear-gradient(90deg, #E8DFD7 0%, #FAF8F5 50%, #E8DFD7 100%);
  background-size: 200% 100%;
  animation: lumeaShimmer 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  box-shadow: inset 0 0 0 1px rgba(28, 25, 23, 0.07);
}

@keyframes lumeaShimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.stencil-pill {
  border-radius: 999px;
}

.stencil-line {
  border-radius: 6px;
}

.stencil-circle {
  border-radius: 50%;
}

/* 1. Hero Stencil */
.skeleton-hero-section {
  padding: 3.5rem 0 3rem;
  background: #FAF8F5;
  border-bottom: 1px solid rgba(28, 25, 23, 0.05);
}

.skeleton-hero-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 3.5rem;
  align-items: center;
}

.skeleton-hero-copy {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.eyebrow-pill {
  width: 170px;
  height: 22px;
}

.headline-1 {
  width: 90%;
  height: 48px;
}

.headline-2 {
  width: 65%;
  height: 48px;
  margin-bottom: 0.5rem;
}

.desc-1 {
  width: 92%;
  height: 16px;
}

.desc-2 {
  width: 78%;
  height: 16px;
  margin-bottom: 1rem;
}

.skeleton-cta-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.cta-btn-dark {
  width: 140px;
  height: 44px;
}

.cta-btn-outline {
  width: 160px;
  height: 44px;
}

.skeleton-slider-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(28, 25, 23, 0.06);
}

.slider-track {
  width: 140px;
  height: 4px;
}

.skeleton-dots-row {
  display: flex;
  gap: 8px;
}

.stencil-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.skeleton-hero-visual {
  display: flex;
  justify-content: center;
}

.stencil-stage {
  width: 100%;
  max-width: 440px;
  height: 420px;
  border-radius: 24px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(28, 25, 23, 0.08);
  box-shadow: 0 12px 32px -8px rgba(28, 25, 23, 0.08);
}

.stencil-callout-pill {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 110px;
  height: 26px;
  border-radius: 999px;
  background: #FAF8F5;
  box-shadow: 0 4px 12px rgba(28, 25, 23, 0.08), inset 0 0 0 1px rgba(28, 25, 23, 0.05);
}

.stencil-bottle-silhouette {
  width: 140px;
  height: 260px;
  background: linear-gradient(180deg, #DFD6CD 0%, #E8DFD7 100%);
  border-radius: 40px 40px 18px 18px;
  box-shadow: 0 8px 24px -4px rgba(28, 25, 23, 0.12), inset 0 0 0 1px rgba(28, 25, 23, 0.06);
}

/* 2. Brand Horizon Marquee Stencil */
.skeleton-brands-strip {
  padding: 1.75rem 0;
  background: #FFFFFF;
  border-bottom: 1px solid rgba(28, 25, 23, 0.05);
  overflow: hidden;
}

.skeleton-brands-track {
  display: flex;
  gap: 2.5rem;
  align-items: center;
  justify-content: center;
}

.stencil-brand-pill {
  width: 110px;
  height: 38px;
  border-radius: 8px;
  flex-shrink: 0;
}

/* 3. Categories Stencil */
.skeleton-categories-section {
  padding: 4rem 0 3rem;
}

.skeleton-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.section-title-line {
  width: 180px;
  height: 20px;
}

.section-link-line {
  width: 110px;
  height: 14px;
}

.skeleton-categories-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 1.25rem;
}

.skeleton-cat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.cat-circle {
  width: 84px;
  height: 84px;
}

.cat-label {
  width: 60px;
  height: 12px;
}

/* 4. Best Sellers Stencil */
.skeleton-bestsellers-section {
  padding: 2rem 0 5rem;
}

.skeleton-products-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .skeleton-hero-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .skeleton-hero-visual {
    order: -1;
  }

  .stencil-stage {
    height: 300px;
  }

  .skeleton-categories-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .skeleton-products-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .skeleton-categories-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
  }

  .cat-circle {
    width: 64px;
    height: 64px;
  }

  .skeleton-products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.85rem;
  }
}
</style>
