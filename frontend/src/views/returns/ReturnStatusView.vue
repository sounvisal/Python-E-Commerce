<template>
  <div class="lumea-return-status-page">
    <div class="container status-container">
      <!-- Breadcrumbs -->
      <nav class="status-breadcrumb" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/returns">Returns &amp; Refunds</router-link>
        <span class="sep">&rsaquo;</span>
        <span class="cur-crumb">Return Request #{{ returnData.request_number }}</span>
      </nav>

      <!-- Page Header with Quote Box matching Screen #2 -->
      <header class="status-header-row">
        <div class="header-text-col">
          <h1 class="status-main-title">Return Request Status</h1>
          <p class="status-subtitle">You can track the progress of your return request below.</p>
        </div>

        <div class="header-quote-col">
          <div class="quote-box-frame">
            <img
              src="/images/returns-status-box2.jpg"
              alt="Taking care of you, always."
              class="quote-box-img"
            />
          </div>
        </div>
      </header>

      <!-- Return Request Highlight Card -->
      <div class="request-summary-banner">
        <div class="summary-left">
          <span class="req-label">Return Request</span>
          <div class="req-number-row">
            <h2 class="req-number">#{{ returnData.request_number }}</h2>
            <span class="status-badge-approved">{{ returnData.status }}</span>
          </div>
          <div class="req-meta-line">
            <span>Submitted on {{ returnData.submitted_date }}</span>
            <span class="meta-dot">&bull;</span>
            <span>Order #{{ returnData.order_number }}</span>
            <span class="meta-dot">&bull;</span>
            <router-link :to="`/account/orders/${returnData.order_number}`" class="view-order-link">
              View Order &rarr;
            </router-link>
          </div>
        </div>

        <div class="summary-right">
          <button @click="downloadReturnLabel" class="btn-download-label">
            <Download :size="16" />
            <span>Download Return Label</span>
          </button>
        </div>
      </div>

      <!-- 7-Stage Horizontal Progress Timeline -->
      <div class="progress-timeline-card">
        <div class="timeline-stages-wrapper">
          <div
            v-for="(stage, sIdx) in returnData.timeline"
            :key="stage.id"
            class="timeline-stage-node"
            :class="{
              'is-completed': stage.status === 'completed',
              'is-current': stage.status === 'current',
              'is-upcoming': stage.status === 'upcoming'
            }"
          >
            <!-- Stage Icon/Circle -->
            <div class="stage-circle">
              <Check v-if="stage.status === 'completed'" :size="14" />
              <Package v-else-if="stage.status === 'current'" :size="14" />
              <component v-else :is="getStageIcon(stage.id)" :size="14" />
            </div>

            <!-- Stage Text -->
            <div class="stage-info">
              <span class="stage-title">{{ stage.title }}</span>
              <span class="stage-date">{{ stage.date }}</span>
            </div>

            <!-- Connector Line -->
            <div v-if="sIdx < returnData.timeline.length - 1" class="stage-connector"></div>
          </div>
        </div>
      </div>

      <!-- Main 2-Column Grid: Return Details (Left) + Next Steps / Help (Right) -->
      <div class="status-content-grid">
        <!-- Left: Item & Return Details -->
        <div class="status-details-col">
          <div class="details-section-card">
            <h3 class="card-section-title">Return Details</h3>

            <!-- Item Row -->
            <div class="return-item-row">
              <img :src="returnData.product_image" :alt="returnData.product_name" class="item-img" />
              <div class="item-desc-col">
                <h4 class="item-title">{{ returnData.product_name }}</h4>
                <span class="item-meta">{{ returnData.product_variant }}</span>
                <span class="item-price">${{ returnData.price.toFixed(2) }}</span>
                <span class="item-qty">Qty: {{ returnData.quantity }}</span>
              </div>
            </div>

            <!-- Details Attributes -->
            <div class="details-attr-list">
              <div class="attr-block">
                <span class="attr-label">Reason for Return</span>
                <span class="attr-value">{{ returnData.reason }}</span>
              </div>

              <div class="attr-block">
                <span class="attr-label">Requested Resolution</span>
                <span class="attr-value">{{ returnData.resolution }}</span>
              </div>

              <div class="attr-block">
                <span class="attr-label">Description</span>
                <p class="attr-paragraph">{{ returnData.description }}</p>
              </div>

              <div class="attr-block">
                <span class="attr-label">Uploaded Photos</span>
                <div class="uploaded-photos-grid">
                  <div
                    v-for="(photo, pIdx) in returnData.photos"
                    :key="pIdx"
                    class="photo-thumb-frame"
                  >
                    <img :src="photo" :alt="'Proof photo ' + (pIdx + 1)" class="proof-photo" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: What's Next & Address & FAQs -->
        <aside class="status-sidebar-col">
          <!-- What's Next Card -->
          <div class="sidebar-box-card whats-next-box">
            <div class="box-header-row">
              <Truck :size="20" class="box-icon" />
              <h4>What's Next?</h4>
            </div>
            <p>
              Please ship the item back to us using the return label. Once we receive the item, we'll process your refund.
            </p>
            <button @click="downloadReturnLabel" class="btn-sidebar-download">
              Download Return Label
            </button>
          </div>

          <!-- 14 Days Notice -->
          <div class="info-alert-card">
            <Info :size="18" class="info-icon" />
            <p>
              Please send the item within 14 days of approval. Use the provided label to ensure a smooth return process.
            </p>
          </div>

          <!-- Return Shipping Address -->
          <div class="sidebar-box-card">
            <div class="box-header-row">
              <Shield :size="18" class="box-icon" />
              <h4>Return Shipping Address</h4>
            </div>
            <address class="shipping-address-text">
              Luméa Returns Center<br>
              #12, Street 271, Sangkat Toul Tom Poung<br>
              Phnom Penh, Cambodia 120801
            </address>
          </div>

          <!-- Need Help? -->
          <div class="sidebar-box-card need-help-box">
            <div class="box-header-row">
              <MessageSquare :size="18" class="box-icon" />
              <div>
                <h4>Need Help?</h4>
                <p class="sub-text">Our customer care team is here for you.</p>
              </div>
            </div>
            <router-link to="/contact" class="btn-outline-contact">
              Contact Us
            </router-link>
          </div>

          <!-- Frequently Asked Questions Link -->
          <div class="faq-link-strip">
            <span>Frequently Asked Questions</span>
            <router-link to="/faq" class="view-faqs-link">View All FAQs &rarr;</router-link>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  Download,
  Check,
  Package,
  Truck,
  RotateCcw,
  BadgeCheck,
  Info,
  Shield,
  MessageSquare
} from 'lucide-vue-next'

const route = useRoute()

const returnData = ref({
  request_number: 'RR24081234',
  order_number: 'LM24081234',
  product_name: 'SK-II Facial Treatment Essence',
  product_image: '/images/prod-sk2.jpg',
  product_variant: '230ml',
  price: 125.0,
  quantity: 1,
  reason: 'Product is damaged',
  resolution: 'Refund to original payment method',
  description: 'The bottle arrived with a crack and some product leaked. Please see the attached photos.',
  photos: [
    '/images/returns-workflow-bottles.jpg',
    '/images/prod-sk2.jpg',
    '/images/returns-status-box2.jpg'
  ],
  status: 'Approved',
  current_step: 3,
  submitted_date: 'Aug 14, 2024',
  timeline: [
    { id: 1, title: 'Submitted', date: 'Aug 14, 2024', status: 'completed' },
    { id: 2, title: 'Under Review', date: 'Aug 15, 2024', status: 'completed' },
    { id: 3, title: 'Approved', date: 'Aug 16, 2024', status: 'current' },
    { id: 4, title: 'Return in Transit', date: 'Pending', status: 'upcoming' },
    { id: 5, title: 'Item Received', date: 'Pending', status: 'upcoming' },
    { id: 6, title: 'Refund Processing', date: 'Pending', status: 'upcoming' },
    { id: 7, title: 'Refund Completed', date: 'Pending', status: 'upcoming' }
  ]
})

function getStageIcon(id) {
  switch (id) {
    case 1:
    case 2:
    case 3: return Package
    case 4: return Truck
    case 5: return Package
    case 6: return RotateCcw
    case 7: return BadgeCheck
    default: return Package
  }
}

function downloadReturnLabel() {
  alert(`Downloading Luméa Official Return Shipping Label for Request #${returnData.value.request_number}...`)
}

async function loadReturnRequest() {
  const reqId = route.params.requestId || 'RR24081234'
  try {
    const res = await fetch(`/api/returns/${reqId}`)
    if (res.ok) {
      const data = await res.json()
      returnData.value = data
    }
  } catch (err) {
    console.warn('[ReturnStatusView] Falling back to default data:', err)
  }
}

onMounted(() => {
  loadReturnRequest()
})
</script>

<style scoped>
.lumea-return-status-page {
  background: #FCFAF7;
  min-height: 100vh;
  padding: 2rem 0 6rem;
  color: #1C1917;
}

.status-container {
  max-width: 1280px;
}

/* Breadcrumbs */
.status-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
  margin-bottom: 2rem;
}

.status-breadcrumb a {
  color: #78716C;
  text-decoration: none;
}

.status-breadcrumb a:hover {
  color: #7A2E22;
}

.sep {
  color: #A8A29E;
}

.cur-crumb {
  color: #1C1917;
  font-weight: 500;
}

/* Header Row */
.status-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 2rem;
}

.status-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 3.5vw, 2.8rem);
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
}

.status-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #57534E;
  margin: 0;
}

.quote-box-frame {
  max-width: 320px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.quote-box-img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  display: block;
}

/* Request Summary Highlight Card */
.request-summary-banner {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
}

.req-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: #78716C;
  display: block;
  margin-bottom: 0.25rem;
}

.req-number-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.4rem;
}

.req-number {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.7rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.status-badge-approved {
  background: #DCFCE7;
  color: #15803D;
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.req-meta-line {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
}

.meta-dot {
  color: #A8A29E;
}

.view-order-link {
  color: #7A2E22;
  font-weight: 600;
  text-decoration: none;
}

.btn-download-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #FFFFFF;
  border: 1.5px solid #7A2E22;
  color: #7A2E22;
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  font-weight: 600;
  padding: 0.7rem 1.4rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-download-label:hover {
  background: #7A2E22;
  color: #FFFFFF;
}

/* 7-Stage Horizontal Progress Timeline */
.progress-timeline-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  padding: 2.25rem 2rem;
  margin-bottom: 2.5rem;
  overflow-x: auto;
}

.timeline-stages-wrapper {
  display: flex;
  align-items: flex-start;
  min-width: 820px;
}

.timeline-stage-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  flex: 1;
}

.stage-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #F5EFEB;
  color: #A8A29E;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  z-index: 2;
  transition: all 0.2s;
}

.timeline-stage-node.is-completed .stage-circle {
  background: #7A2E22;
  color: #FFFFFF;
}

.timeline-stage-node.is-current .stage-circle {
  background: #7A2E22;
  color: #FFFFFF;
  box-shadow: 0 0 0 4px rgba(122, 46, 34, 0.15);
}

.stage-info {
  display: flex;
  flex-direction: column;
}

.stage-title {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #78716C;
  line-height: 1.3;
}

.timeline-stage-node.is-completed .stage-title,
.timeline-stage-node.is-current .stage-title {
  color: #1C1917;
}

.stage-date {
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  color: #A8A29E;
  margin-top: 0.2rem;
}

.stage-connector {
  position: absolute;
  top: 18px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #E7E5E4;
  z-index: 1;
}

.timeline-stage-node.is-completed .stage-connector {
  background: #7A2E22;
}

/* 2-Column Content Grid */
.status-content-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2.5rem;
  align-items: start;
}

/* Return Details Card */
.details-section-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  padding: 2.25rem;
}

.card-section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 1.5rem;
}

.return-item-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem;
  background: #FAF7F2;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.item-img {
  width: 72px;
  height: 72px;
  border-radius: 6px;
  object-fit: cover;
}

.item-desc-col {
  display: flex;
  flex-direction: column;
}

.item-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.2rem;
}

.item-meta {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #78716C;
}

.item-price {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #7A2E22;
  margin-top: 0.2rem;
}

.item-qty {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #78716C;
}

.details-attr-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.attr-block {
  display: flex;
  flex-direction: column;
}

.attr-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #78716C;
  margin-bottom: 0.35rem;
}

.attr-value {
  font-family: 'Inter', sans-serif;
  font-size: 0.92rem;
  font-weight: 500;
  color: #1C1917;
}

.attr-paragraph {
  font-family: 'Inter', sans-serif;
  font-size: 0.9rem;
  color: #44403C;
  line-height: 1.6;
  margin: 0;
}

.uploaded-photos-grid {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.photo-thumb-frame {
  width: 84px;
  height: 84px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #E7E5E4;
}

.proof-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Sidebar Column */
.status-sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.sidebar-box-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
}

.box-header-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.75rem;
}

.box-icon {
  color: #7A2E22;
}

.box-header-row h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0;
}

.whats-next-box p {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.25rem;
}

.btn-sidebar-download {
  width: 100%;
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-sidebar-download:hover {
  background: #5E2117;
}

.info-alert-card {
  background: #F0F9FF;
  border: 1px solid #BAE6FD;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.info-icon {
  color: #0284C7;
  flex-shrink: 0;
  margin-top: 0.15rem;
}

.info-alert-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #0369A1;
  line-height: 1.45;
  margin: 0;
}

.shipping-address-text {
  font-family: 'Inter', sans-serif;
  font-style: normal;
  font-size: 0.84rem;
  color: #44403C;
  line-height: 1.6;
}

.need-help-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.need-help-box .box-header-row {
  margin-bottom: 0;
}

.sub-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.76rem;
  color: #78716C;
  margin: 0;
}

.btn-outline-contact {
  border: 1px solid #7A2E22;
  color: #7A2E22;
  background: transparent;
  padding: 0.55rem 1rem;
  border-radius: 4px;
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-outline-contact:hover {
  background: #7A2E22;
  color: #FFFFFF;
}

.faq-link-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.25rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #1C1917;
}

.view-faqs-link {
  color: #7A2E22;
  font-weight: 600;
  text-decoration: none;
}

/* Responsive */
@media (max-width: 992px) {
  .status-content-grid {
    grid-template-columns: 1fr;
  }
  .request-summary-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
}
</style>
