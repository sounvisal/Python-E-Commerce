<template>
  <div class="article-detail-skeleton" aria-hidden="true">
    <div class="skeleton-container">
      <!-- Breadcrumbs Stencil -->
      <div class="skeleton-breadcrumbs">
        <div class="skeleton-line shimmer breadcrumb-sm"></div>
        <div class="skeleton-line shimmer breadcrumb-sep"></div>
        <div class="skeleton-line shimmer breadcrumb-sm"></div>
        <div class="skeleton-line shimmer breadcrumb-sep"></div>
        <div class="skeleton-line shimmer breadcrumb-lg"></div>
      </div>

      <!-- Header Stencil -->
      <div class="skeleton-header">
        <div class="skeleton-pill shimmer category-pill"></div>
        <div class="skeleton-line shimmer main-title-1"></div>
        <div class="skeleton-line shimmer main-title-2"></div>
        <div class="skeleton-line shimmer subtitle-line"></div>

        <div class="skeleton-author-strip">
          <div class="skeleton-circle shimmer author-avatar"></div>
          <div class="skeleton-line shimmer author-name"></div>
          <div class="skeleton-line shimmer meta-pill"></div>
        </div>
      </div>

      <!-- Hero Visual Stencil -->
      <div class="skeleton-hero-image shimmer"></div>

      <!-- Main Body 2-Column Grid -->
      <div class="skeleton-body-layout">
        <!-- Left TOC -->
        <aside class="skeleton-toc-sidebar">
          <div class="skeleton-toc-card">
            <div class="skeleton-line shimmer toc-heading"></div>
            <div v-for="n in 5" :key="n" class="skeleton-line shimmer toc-item"></div>
          </div>
        </aside>

        <!-- Right Article Content -->
        <article class="skeleton-article-main">
          <div class="skeleton-line shimmer heading-line"></div>
          <div class="skeleton-line shimmer para-line" v-for="p in 4" :key="`p1-${p}`"></div>

          <div class="skeleton-callout-box shimmer"></div>

          <div class="skeleton-line shimmer heading-line mt-4"></div>
          <div class="skeleton-line shimmer para-line" v-for="p in 5" :key="`p2-${p}`"></div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for Skincare Journal Article reader view
</script>

<style scoped>
.article-detail-skeleton {
  width: 100%;
  background: #FAF8F5;
  padding: 1.5rem 0 5rem;
  user-select: none;
  pointer-events: none;
}

.skeleton-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
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

.skeleton-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.breadcrumb-sm {
  width: 50px;
  height: 12px;
  border-radius: 4px;
}

.breadcrumb-sep {
  width: 10px;
  height: 12px;
  border-radius: 2px;
}

.breadcrumb-lg {
  width: 120px;
  height: 12px;
  border-radius: 4px;
}

.skeleton-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 2.5rem;
}

.category-pill {
  width: 100px;
  height: 24px;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.main-title-1 {
  width: 75%;
  height: 32px;
  border-radius: 6px;
  margin-bottom: 0.65rem;
}

.main-title-2 {
  width: 50%;
  height: 32px;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.subtitle-line {
  width: 60%;
  height: 16px;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.skeleton-author-strip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.author-name {
  width: 110px;
  height: 14px;
  border-radius: 4px;
}

.meta-pill {
  width: 130px;
  height: 14px;
  border-radius: 4px;
}

.skeleton-hero-image {
  width: 100%;
  height: 420px;
  border-radius: 16px;
  margin-bottom: 3rem;
}

.skeleton-body-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 3rem;
  align-items: flex-start;
}

.skeleton-toc-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.toc-heading {
  width: 120px;
  height: 16px;
  border-radius: 4px;
}

.toc-item {
  width: 100%;
  height: 14px;
  border-radius: 4px;
}

.skeleton-article-main {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 14px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.heading-line {
  width: 45%;
  height: 24px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.para-line {
  width: 100%;
  height: 14px;
  border-radius: 4px;
}

.skeleton-callout-box {
  width: 100%;
  height: 90px;
  border-radius: 10px;
  margin: 1rem 0;
}

.mt-4 {
  margin-top: 1.5rem;
}

@media (max-width: 900px) {
  .skeleton-body-layout {
    grid-template-columns: 1fr;
  }
}
</style>
