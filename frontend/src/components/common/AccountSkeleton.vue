<template>
  <div class="account-skeleton-page" aria-hidden="true">
    <div class="skeleton-container">
      <!-- Breadcrumbs -->
      <div class="skeleton-breadcrumbs">
        <div class="skeleton-line shimmer crumb-sm"></div>
        <div class="skeleton-line shimmer crumb-sep"></div>
        <div class="skeleton-line shimmer crumb-lg"></div>
      </div>

      <!-- Hero Banner Stencil -->
      <div class="skeleton-hero shimmer">
        <div class="hero-text-col">
          <div class="skeleton-line shimmer hero-title-line"></div>
          <div class="skeleton-line shimmer hero-sub-line"></div>
        </div>
      </div>

      <!-- 3-Column Layout -->
      <div class="skeleton-3col-grid">
        <!-- Left: Sidebar Stencil -->
        <aside class="skeleton-sidebar-card">
          <div class="sidebar-user-block">
            <div class="skeleton-avatar shimmer"></div>
            <div class="skeleton-line shimmer user-name-line"></div>
            <div class="skeleton-pill shimmer tier-pill"></div>
          </div>
          <div class="sidebar-links-list">
            <div v-for="n in 6" :key="n" class="skeleton-line shimmer sidebar-link-line"></div>
          </div>
        </aside>

        <!-- Center: Main Dashboard Stencil -->
        <main class="skeleton-main-column">
          <!-- Greeting Card -->
          <div class="skeleton-card greeting-card">
            <div class="skeleton-line shimmer greeting-line-1"></div>
            <div class="skeleton-line shimmer greeting-line-2"></div>
          </div>

          <!-- 3 KPI Cards -->
          <div class="skeleton-kpi-row">
            <div v-for="n in 3" :key="n" class="skeleton-card kpi-card">
              <div class="kpi-icon-circle shimmer"></div>
              <div class="skeleton-line shimmer kpi-val-line"></div>
              <div class="skeleton-line shimmer kpi-lbl-line"></div>
            </div>
          </div>

          <!-- Recent Orders Card -->
          <div class="skeleton-card orders-preview-card">
            <div class="card-header-line">
              <div class="skeleton-line shimmer section-heading"></div>
              <div class="skeleton-line shimmer view-all-line"></div>
            </div>
            <div v-for="n in 2" :key="n" class="order-stub-row">
              <div class="order-stub-left">
                <div class="skeleton-line shimmer stub-num"></div>
                <div class="skeleton-line shimmer stub-date"></div>
              </div>
              <div class="stub-thumbs-row">
                <div v-for="t in 3" :key="t" class="stub-thumb shimmer"></div>
              </div>
              <div class="skeleton-pill shimmer stub-badge"></div>
            </div>
          </div>
        </main>

        <!-- Right: Loyalty Tier Widget -->
        <aside class="skeleton-right-widget">
          <div class="skeleton-card privilege-card shimmer"></div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
// Presentation skeleton for My Account customer dashboard
</script>

<style scoped>
.account-skeleton-page {
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
  width: 100px;
  height: 12px;
  border-radius: 4px;
}

.skeleton-hero {
  width: 100%;
  height: 160px;
  border-radius: 14px;
  margin-bottom: 2rem;
  padding: 2.5rem;
  box-sizing: border-box;
  display: flex;
  align-items: center;
}

.hero-text-col {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.hero-title-line {
  width: 220px;
  height: 32px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.6);
}

.hero-sub-line {
  width: 320px;
  height: 16px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.5);
}

.skeleton-3col-grid {
  display: grid;
  grid-template-columns: 240px 1fr 280px;
  gap: 1.5rem;
  align-items: flex-start;
}

.skeleton-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.5rem;
}

.skeleton-sidebar-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.08);
  border-radius: 12px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-user-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.65rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #F4EFEB;
}

.skeleton-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
}

.user-name-line {
  width: 120px;
  height: 16px;
  border-radius: 4px;
}

.tier-pill {
  width: 100px;
  height: 22px;
  border-radius: 11px;
}

.sidebar-links-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-link-line {
  width: 80%;
  height: 14px;
  border-radius: 4px;
}

.skeleton-main-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.greeting-card {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.greeting-line-1 {
  width: 180px;
  height: 24px;
  border-radius: 6px;
}

.greeting-line-2 {
  width: 300px;
  height: 14px;
  border-radius: 4px;
}

.skeleton-kpi-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.kpi-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
  padding: 1.25rem;
}

.kpi-icon-circle {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  margin-bottom: 0.25rem;
}

.kpi-val-line {
  width: 60px;
  height: 20px;
  border-radius: 4px;
}

.kpi-lbl-line {
  width: 80px;
  height: 12px;
  border-radius: 3px;
}

.orders-preview-card {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.card-header-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-heading {
  width: 140px;
  height: 18px;
  border-radius: 4px;
}

.view-all-line {
  width: 70px;
  height: 14px;
  border-radius: 3px;
}

.order-stub-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 0;
  border-bottom: 1px solid #F4EFEB;
}

.order-stub-left {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.stub-num {
  width: 110px;
  height: 14px;
  border-radius: 3px;
}

.stub-date {
  width: 75px;
  height: 11px;
  border-radius: 3px;
}

.stub-thumbs-row {
  display: flex;
  gap: 0.35rem;
}

.stub-thumb {
  width: 40px;
  height: 40px;
  border-radius: 6px;
}

.stub-badge {
  width: 80px;
  height: 22px;
  border-radius: 11px;
}

.privilege-card {
  height: 320px;
}

@media (max-width: 1100px) {
  .skeleton-3col-grid {
    grid-template-columns: 1fr;
  }
}
</style>
