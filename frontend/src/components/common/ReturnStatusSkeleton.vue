<template>
  <div class="return-status-skeleton" aria-hidden="true">
    <div class="skeleton-container">
      <!-- Breadcrumbs -->
      <div class="skeleton-breadcrumbs">
        <div class="skeleton-line shimmer crumb-sm"></div>
        <div class="skeleton-line shimmer crumb-sep"></div>
        <div class="skeleton-line shimmer crumb-lg"></div>
      </div>

      <!-- Top Return Status Card -->
      <div class="skeleton-card header-card">
        <div class="header-left">
          <div class="skeleton-line shimmer return-id-line"></div>
          <div class="skeleton-line shimmer return-sub-line"></div>
        </div>
        <div class="header-right">
          <div class="skeleton-pill shimmer status-pill"></div>
        </div>
      </div>

      <!-- 7-Stage Timeline Stencil -->
      <div class="skeleton-card timeline-card">
        <div class="timeline-nodes-track">
          <div v-for="n in 7" :key="n" class="stage-node-item">
            <div class="stage-circle shimmer"></div>
            <div class="stage-label shimmer"></div>
          </div>
        </div>
      </div>

      <!-- 2-Column Split: Item Info & Return Instructions -->
      <div class="skeleton-split-layout">
        <div class="skeleton-card item-card">
          <div class="skeleton-line shimmer card-heading"></div>
          <div class="item-preview-row">
            <div class="item-square shimmer"></div>
            <div class="item-meta">
              <div class="skeleton-line shimmer item-title"></div>
              <div class="skeleton-line shimmer item-reason"></div>
              <div class="skeleton-line shimmer item-amount"></div>
            </div>
          </div>
        </div>

        <div class="skeleton-card guide-card">
          <div class="skeleton-line shimmer card-heading"></div>
          <div v-for="n in 3" :key="n" class="guide-step-row">
            <div class="step-num-circle shimmer"></div>
            <div class="step-desc-lines">
              <div class="skeleton-line shimmer step-line-1"></div>
              <div class="skeleton-line shimmer step-line-2"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for Return Status tracking view
</script>

<style scoped>
.return-status-skeleton {
  width: 100%;
  background: #FAF8F5;
  padding: 1.5rem 0 5rem;
  user-select: none;
  pointer-events: none;
}

.skeleton-container {
  max-width: 1100px;
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
  margin-bottom: 1.5rem;
}

.crumb-sm {
  width: 50px;
  height: 12px;
  border-radius: 4px;
}

.crumb-sep {
  width: 8px;
  height: 12px;
  border-radius: 2px;
}

.crumb-lg {
  width: 120px;
  height: 12px;
  border-radius: 4px;
}

.skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.header-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.return-id-line {
  width: 200px;
  height: 24px;
  border-radius: 6px;
}

.return-sub-line {
  width: 150px;
  height: 13px;
  border-radius: 3px;
}

.status-pill {
  width: 110px;
  height: 30px;
  border-radius: 15px;
}

.timeline-nodes-track {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  overflow-x: auto;
}

.stage-node-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.45rem;
  min-width: 80px;
}

.stage-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.stage-label {
  width: 65px;
  height: 10px;
  border-radius: 3px;
}

.skeleton-split-layout {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 1.5rem;
}

.card-heading {
  width: 130px;
  height: 18px;
  border-radius: 4px;
  margin-bottom: 1.25rem;
}

.item-preview-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.item-square {
  width: 64px;
  height: 64px;
  border-radius: 8px;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  flex: 1;
}

.item-title {
  width: 80%;
  height: 16px;
  border-radius: 4px;
}

.item-reason {
  width: 50%;
  height: 12px;
  border-radius: 3px;
}

.item-amount {
  width: 60px;
  height: 16px;
  border-radius: 4px;
}

.guide-step-row {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1rem;
}

.step-num-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  flex-shrink: 0;
}

.step-desc-lines {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex: 1;
}

.step-line-1 {
  width: 90%;
  height: 12px;
  border-radius: 3px;
}

.step-line-2 {
  width: 60%;
  height: 12px;
  border-radius: 3px;
}

@media (max-width: 768px) {
  .skeleton-split-layout {
    grid-template-columns: 1fr;
  }
}
</style>
