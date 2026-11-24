<template>
  <div class="order-detail-skeleton" aria-hidden="true">
    <div class="skeleton-container">
      <!-- Breadcrumbs -->
      <div class="skeleton-breadcrumbs">
        <div class="skeleton-line shimmer crumb-sm"></div>
        <div class="skeleton-line shimmer crumb-sep"></div>
        <div class="skeleton-line shimmer crumb-sm"></div>
        <div class="skeleton-line shimmer crumb-sep"></div>
        <div class="skeleton-line shimmer crumb-lg"></div>
      </div>

      <!-- Top Header Card -->
      <div class="skeleton-card header-card">
        <div class="header-left">
          <div class="skeleton-line shimmer order-title-line"></div>
          <div class="skeleton-line shimmer order-sub-line"></div>
        </div>
        <div class="header-right">
          <div class="skeleton-pill shimmer status-badge-pill"></div>
        </div>
      </div>

      <!-- Timeline Bar Stencil -->
      <div class="skeleton-card timeline-card">
        <div class="timeline-nodes-row">
          <div v-for="n in 5" :key="n" class="timeline-node">
            <div class="node-circle shimmer"></div>
            <div class="node-label shimmer"></div>
          </div>
        </div>
      </div>

      <!-- 2-Column Split: Items on Left, Invoice on Right -->
      <div class="skeleton-split-layout">
        <!-- Left: Items List -->
        <div class="skeleton-card items-card">
          <div class="skeleton-line shimmer card-title-line"></div>
          <div v-for="n in 2" :key="n" class="skeleton-item-row">
            <div class="item-thumb shimmer"></div>
            <div class="item-info">
              <div class="item-name shimmer"></div>
              <div class="item-sku shimmer"></div>
            </div>
            <div class="item-price shimmer"></div>
          </div>
        </div>

        <!-- Right: Summary Box -->
        <div class="skeleton-card summary-card">
          <div class="skeleton-line shimmer card-title-line"></div>
          <div class="summary-line-row" v-for="n in 3" :key="n">
            <div class="summary-label shimmer"></div>
            <div class="summary-val shimmer"></div>
          </div>
          <div class="summary-total-row">
            <div class="total-label shimmer"></div>
            <div class="total-val shimmer"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for Order Details & invoice view
</script>

<style scoped>
.order-detail-skeleton {
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
  width: 130px;
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

.order-title-line {
  width: 220px;
  height: 24px;
  border-radius: 6px;
}

.order-sub-line {
  width: 140px;
  height: 14px;
  border-radius: 4px;
}

.status-badge-pill {
  width: 110px;
  height: 30px;
  border-radius: 15px;
}

.timeline-nodes-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.timeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.node-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
}

.node-label {
  width: 60px;
  height: 10px;
  border-radius: 3px;
}

.skeleton-split-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 1.5rem;
}

.card-title-line {
  width: 120px;
  height: 18px;
  border-radius: 4px;
  margin-bottom: 1.25rem;
}

.skeleton-item-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid #F4EFEB;
}

.item-thumb {
  width: 54px;
  height: 54px;
  border-radius: 8px;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex: 1;
}

.item-name {
  width: 75%;
  height: 14px;
  border-radius: 4px;
}

.item-sku {
  width: 40%;
  height: 11px;
  border-radius: 3px;
}

.item-price {
  width: 50px;
  height: 16px;
  border-radius: 4px;
}

.summary-line-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.summary-label {
  width: 80px;
  height: 12px;
  border-radius: 3px;
}

.summary-val {
  width: 50px;
  height: 12px;
  border-radius: 3px;
}

.summary-total-row {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  margin-top: 0.5rem;
  border-top: 1px solid #EBE1D7;
}

.total-label {
  width: 60px;
  height: 18px;
  border-radius: 4px;
}

.total-val {
  width: 70px;
  height: 22px;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .skeleton-split-layout {
    grid-template-columns: 1fr;
  }
}
</style>
