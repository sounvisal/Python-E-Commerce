<template>
  <div class="article-skeleton-card" aria-hidden="true">
    <!-- Thumbnail Stencil -->
    <div class="skeleton-thumb shimmer">
      <div class="skeleton-pill-mini"></div>
    </div>

    <!-- Content Stencil -->
    <div class="skeleton-content">
      <div class="skeleton-meta-row">
        <div class="skeleton-tag shimmer"></div>
        <div class="skeleton-date shimmer"></div>
      </div>

      <div class="skeleton-title-1 shimmer"></div>
      <div class="skeleton-title-2 shimmer"></div>

      <div class="skeleton-excerpt-1 shimmer"></div>
      <div class="skeleton-excerpt-2 shimmer"></div>

      <div class="skeleton-footer-row">
        <div class="skeleton-avatar shimmer"></div>
        <div class="skeleton-author-name shimmer"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for Skincare Journal cards
</script>

<style scoped>
.article-skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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

.skeleton-thumb {
  width: 100%;
  height: 210px;
  position: relative;
}

.skeleton-pill-mini {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 60px;
  height: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.7);
}

.skeleton-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  flex: 1;
}

.skeleton-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.skeleton-tag {
  width: 75px;
  height: 18px;
  border-radius: 4px;
}

.skeleton-date {
  width: 65px;
  height: 12px;
  border-radius: 4px;
}

.skeleton-title-1 {
  width: 90%;
  height: 18px;
  border-radius: 4px;
}

.skeleton-title-2 {
  width: 65%;
  height: 18px;
  border-radius: 4px;
}

.skeleton-excerpt-1 {
  width: 100%;
  height: 12px;
  border-radius: 4px;
  margin-top: 0.35rem;
}

.skeleton-excerpt-2 {
  width: 80%;
  height: 12px;
  border-radius: 4px;
}

.skeleton-footer-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-top: auto;
  padding-top: 0.85rem;
  border-top: 1px solid #F4EFEB;
}

.skeleton-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.skeleton-author-name {
  width: 90px;
  height: 12px;
  border-radius: 4px;
}
</style>
