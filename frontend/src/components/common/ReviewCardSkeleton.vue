<template>
  <div class="review-skeleton-card" aria-hidden="true">
    <div class="review-card-header">
      <div class="reviewer-avatar shimmer"></div>
      <div class="reviewer-meta">
        <div class="reviewer-name shimmer"></div>
        <div class="reviewer-sub shimmer"></div>
      </div>
      <div class="verified-pill shimmer"></div>
    </div>

    <div class="stars-row">
      <div class="stars-line shimmer"></div>
      <div class="skin-chip shimmer"></div>
    </div>

    <div class="review-body">
      <div class="review-title-line shimmer"></div>
      <div class="review-text-line shimmer"></div>
      <div class="review-text-line shimmer"></div>
      <div class="review-text-line short shimmer"></div>
    </div>

    <div class="review-footer">
      <div class="footer-btn shimmer"></div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for Community Reviews cards
</script>

<style scoped>
.review-skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
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

.review-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reviewer-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  flex-shrink: 0;
}

.reviewer-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex: 1;
}

.reviewer-name {
  width: 100px;
  height: 14px;
  border-radius: 4px;
}

.reviewer-sub {
  width: 70px;
  height: 11px;
  border-radius: 3px;
}

.verified-pill {
  width: 75px;
  height: 20px;
  border-radius: 10px;
}

.stars-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stars-line {
  width: 85px;
  height: 14px;
  border-radius: 3px;
}

.skin-chip {
  width: 90px;
  height: 20px;
  border-radius: 10px;
}

.review-body {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.review-title-line {
  width: 60%;
  height: 16px;
  border-radius: 4px;
  margin-bottom: 0.25rem;
}

.review-text-line {
  width: 100%;
  height: 12px;
  border-radius: 3px;
}

.review-text-line.short {
  width: 65%;
}

.review-footer {
  margin-top: auto;
  padding-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
}

.footer-btn {
  width: 80px;
  height: 24px;
  border-radius: 12px;
}
</style>
