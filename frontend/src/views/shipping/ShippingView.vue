<template>
  <div class="shipping-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Shipping & Delivery</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="shipping-hero">
        <div class="hero-left">
          <h1 class="hero-title">Shipping & Delivery</h1>
          <p class="hero-tagline">We deliver your favorite skincare, with care.</p>
          <p class="hero-desc">
            From our shelves to your doorstep, we make sure your beauty arrives safely, quickly, and reliably.
          </p>
        </div>

        <div class="hero-right">
          <div class="hero-media-wrap">
            <img src="/images/banner-my-orders.jpg" alt="Luméa Delivery" class="hero-banner-img" />
            <div class="hero-script-overlay">
              <span class="script-row">Skincare</span>
              <span class="script-row">Arrives</span>
              <span class="script-row">Happier</span>
              <span class="script-row">Here. <span class="heart-symbol">♡</span></span>
            </div>
          </div>
        </div>
      </section>

      <!-- 4 Guarantees Strip with Vertical Dividers -->
      <section class="guarantees-section">
        <div class="guarantees-strip">
          <div class="guarantee-item">
            <div class="g-pink-icon">
              <Truck :size="22" />
            </div>
            <div class="g-text">
              <h3>Reliable Delivery</h3>
              <p>Fast and secure shipping across Cambodia.</p>
            </div>
          </div>

          <div class="g-divider"></div>

          <div class="guarantee-item">
            <div class="g-pink-icon">
              <ShieldCheck :size="22" />
            </div>
            <div class="g-text">
              <h3>Careful Packaging</h3>
              <p>Your skincare is packed with extra care.</p>
            </div>
          </div>

          <div class="g-divider"></div>

          <div class="guarantee-item">
            <div class="g-pink-icon">
              <Box :size="22" />
            </div>
            <div class="g-text">
              <h3>Real-Time Updates</h3>
              <p>Track your order at every step.</p>
            </div>
          </div>

          <div class="g-divider"></div>

          <div class="guarantee-item">
            <div class="g-pink-icon">
              <Leaf :size="22" />
            </div>
            <div class="g-text">
              <h3>A Kinder Footprint</h3>
              <p>We’re working toward more sustainable shipping options.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 3-Column Section: Vertical Stage + Process/Tracking + FAQ -->
      <section class="delivery-details-section">
        <div class="delivery-three-layout">
          <!-- Col 1: Vertical Stage Photo Card -->
          <div class="vertical-stage-card">
            <div class="stage-card-inner">
              <img src="/images/banner-deals.jpg" alt="Beauty Delivered with Care" class="stage-photo" />
              <div class="stage-overlay-text">
                <h3 class="stage-script-title">More<br />Good Skin<br />Days Ahead.</h3>
                <div class="stage-dash"></div>
              </div>
              <div class="stage-bottom-tag">
                <span>BEAUTY DELIVERED WITH CARE.</span>
              </div>
            </div>
          </div>

          <!-- Col 2: Process Timeline & Live Tracking -->
          <div class="process-tracking-col">
            <div class="col-head-block">
              <span class="section-eyebrow">DELIVERY PROCESS</span>
              <h2 class="col-main-heading">From Order to Your Doorstep</h2>
              <p class="col-desc-text">Here’s what happens after you place your order.</p>
            </div>

            <!-- 4-Step Horizontal Timeline with Connected Line -->
            <div class="timeline-connected-row">
              <div class="t-line-step">
                <div class="t-icon-circle active">
                  <FileText :size="18" />
                </div>
                <h4>Order Confirmed</h4>
                <p>We’ve received your order.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle active">
                  <Package :size="18" />
                </div>
                <h4>Preparing Your Items</h4>
                <p>We carefully pick and pack your products.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle">
                  <Truck :size="18" />
                </div>
                <h4>On the Way</h4>
                <p>Your order is shipped and in transit.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle">
                  <Home :size="18" />
                </div>
                <h4>Delivered</h4>
                <p>Your beauty has arrived!</p>
              </div>
            </div>

            <!-- Live Tracking Card (Soft Peach with Photo) -->
            <div class="peach-tracking-card">
              <div class="peach-visual-thumb">
                <img src="/images/banner-deals.jpg" alt="Luméa Note" class="thumb-img" />
              </div>

              <div class="peach-form-area">
                <h3 class="peach-title">Track Your Order</h3>
                <p class="peach-sub">Enter your order number to see the latest delivery status.</p>

                <form @submit.prevent="handleTrackOrder" class="peach-input-form">
                  <input
                    v-model="trackingNumber"
                    type="text"
                    placeholder="Enter your order number"
                    class="peach-text-input"
                    required
                  />
                  <button type="submit" class="btn-track-rect">Track Order</button>
                </form>

                <div v-if="trackingResult" class="tracking-live-alert">
                  <span class="live-dot"></span>
                  <span>{{ trackingResult }}</span>
                </div>

                <router-link to="/contact" class="peach-help-anchor">
                  Need help? Contact our support team <span class="arrow-right">→</span>
                </router-link>
              </div>
            </div>
          </div>

          <!-- Col 3: Shipping FAQ Accordion -->
          <div class="shipping-faq-col">
            <div class="col-head-block">
              <span class="section-eyebrow">SHIPPING INFORMATION</span>
              <h2 class="col-main-heading">Frequently Asked Questions</h2>
            </div>

            <div class="clean-accordion-list">
              <div
                v-for="(item, idx) in shippingFaqs"
                :key="idx"
                class="clean-acc-item"
                :class="{ active: openFaqIdx === idx }"
              >
                <button class="clean-acc-btn" @click="toggleFaq(idx)">
                  <span>{{ item.question }}</span>
                  <ChevronDown :size="16" class="acc-chevron" />
                </button>
                <div v-show="openFaqIdx === idx" class="clean-acc-body">
                  <p>{{ item.answer }}</p>
                </div>
              </div>
            </div>

            <!-- Still Have Questions Card -->
            <router-link to="/contact" class="white-help-card-link">
              <div class="card-left-icon">
                <Mail :size="20" class="red-mail" />
                <div class="card-meta">
                  <h4>Still have questions?</h4>
                  <p>Our support team is here to help.</p>
                </div>
              </div>
              <span class="card-right-arrow">→</span>
            </router-link>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  Truck,
  ShieldCheck,
  Box,
  Leaf,
  FileText,
  Package,
  Home,
  ChevronDown,
  Mail
} from 'lucide-vue-next'

const trackingNumber = ref('')
const trackingResult = ref(null)
const openFaqIdx = ref(0)

const shippingFaqs = [
  {
    question: 'How long does delivery take?',
    answer:
      'Within Phnom Penh, deliveries typically take 24–48 hours. For provinces across Cambodia, standard shipping takes 2–4 business days. Same-day delivery is available in Phnom Penh for orders placed before 11:00 AM.'
  },
  {
    question: 'How much is the shipping fee?',
    answer:
      'We offer complimentary standard shipping on all orders over $35 in Phnom Penh, and over $50 nationwide. For orders under the minimum threshold, shipping is a flat rate of $1.50 in Phnom Penh and $2.50 for other provinces.'
  },
  {
    question: 'Do you deliver outside Phnom Penh?',
    answer:
      'Yes! We ship across all 24 provinces in Cambodia using trusted express logistics partners including J&T Express and Virak Buntham.'
  },
  {
    question: 'How can I track my order?',
    answer:
      'Once your order has been dispatched, you will receive an SMS and email notification containing your live tracking code and real-time transit updates.'
  },
  {
    question: 'What if my order is delayed?',
    answer:
      'If your package hasn’t arrived within the estimated timeframe, please contact our support team via live chat or email. We will immediately investigate and coordinate with the courier.'
  },
  {
    question: 'Can I change my shipping address?',
    answer:
      'You can update your delivery address as long as your order status is still "Order Confirmed" or "Preparing". Once it is "On the Way", address changes cannot be guaranteed.'
  },
  {
    question: 'What happens if my package is lost or damaged?',
    answer:
      'Every Luméa package is fully insured. In the unlikely event that your order arrives damaged or is lost in transit, we will issue an immediate replacement or 100% full refund.'
  }
]

function toggleFaq(idx) {
  openFaqIdx.value = openFaqIdx.value === idx ? null : idx
}

function handleTrackOrder() {
  trackingResult.value = `Order #${trackingNumber.value.toUpperCase()} is currently On the Way — Estimated delivery tomorrow by 3:00 PM.`
}
</script>

<style scoped>
.shipping-page {
  padding-top: 1rem;
  padding-bottom: 5rem;
  background-color: #FAF8F5;
  min-height: 100vh;
}

/* Breadcrumb */
.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #78716C;
  margin-bottom: 0.85rem;
}

.breadcrumb-nav a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-nav a:hover {
  color: #8E4A3E;
}

.bc-sep {
  color: #A8A29E;
}

.bc-current {
  color: #8E4A3E;
  font-weight: 500;
}

/* Open Hero Banner matching Shipping & Delivery.png */
.shipping-hero {
  display: grid;
  grid-template-columns: 1.15fr 1.1fr;
  align-items: center;
  gap: 2.5rem;
  margin-bottom: 2.25rem;
  min-height: 275px;
  padding: 1.75rem 2.5rem;
  background: linear-gradient(135deg, #FAF7F2 0%, #F5EFE7 50%, #ECE4DB 100%);
  border-radius: 18px;
  border: 1px solid rgba(234, 229, 223, 0.7);
  box-shadow: 0 4px 20px rgba(28, 25, 23, 0.03);
  position: relative;
  overflow: hidden;
  animation: heroEntrance 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes heroEntrance {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-left {
  display: flex;
  flex-direction: column;
  padding-right: 1rem;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.75rem;
  font-weight: 700;
  line-height: 1.12;
  color: #111C38;
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}

.hero-tagline {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.15rem;
  font-weight: 600;
  color: #8E4A3E;
  margin-bottom: 0.5rem;
}

.hero-desc {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.05rem;
  line-height: 1.55;
  color: #57534E;
  max-width: 520px;
}

.hero-media-wrap {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.hero-banner-img {
  width: 100%;
  max-height: 255px;
  object-fit: cover;
  border-radius: 14px;
  box-shadow: 0 12px 32px rgba(28, 25, 23, 0.07);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 15%);
  mask-image: linear-gradient(to right, transparent 0%, black 15%);
}

.hero-script-overlay {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  pointer-events: none;
}

.script-row {
  font-family: var(--font-script, 'Cormorant Garamond', Georgia, serif);
  font-style: italic;
  font-weight: 700;
  font-size: 1.7rem;
  line-height: 1.15;
  color: #C25E4D;
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.85);
}

.heart-symbol {
  font-style: normal;
  font-size: 1.4rem;
}

/* 4 Guarantees Strip with Vertical Dividers */
.guarantees-section {
  margin-bottom: 3.5rem;
}

.guarantees-strip {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.75rem 2rem;
  justify-content: space-between;
}

.guarantee-item {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex: 1;
}

.g-pink-icon {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.g-text h3 {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.g-text p {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.4;
  margin: 0;
}

.g-divider {
  width: 1px;
  height: 48px;
  background: #EAE5DF;
  margin: 0 1.5rem;
  flex-shrink: 0;
}

/* 3-Column Details Layout */
.delivery-details-section {
  margin-bottom: 2rem;
}

.delivery-three-layout {
  display: grid;
  grid-template-columns: 280px 1.35fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Col 1: Vertical Stage Card */
.vertical-stage-card {
  position: relative;
  height: 100%;
}

.stage-card-inner {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  height: 440px;
}

.stage-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stage-overlay-text {
  position: absolute;
  top: 2rem;
  right: 1.75rem;
  text-align: right;
}

.stage-script-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.55rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.25;
}

.stage-dash {
  width: 32px;
  height: 2px;
  background: #8E4A3E;
  margin: 0.75rem 0 0 auto;
}

.stage-bottom-tag {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #57534E;
}

/* Col 2: Process Timeline & Live Tracking */
.col-head-block {
  margin-bottom: 1.5rem;
}

.section-eyebrow {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #8E4A3E;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.35rem;
}

.col-main-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.95rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.35rem;
}

.col-desc-text {
  font-size: 0.88rem;
  color: #78716C;
}

/* Timeline with Connecting Bar */
.timeline-connected-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding: 1.25rem 0;
}

.t-line-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 110px;
}

.t-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.65rem;
}

.t-icon-circle.active {
  background: #FDF2EE;
  color: #8E4A3E;
}

.t-connecting-bar {
  flex: 1;
  height: 1px;
  background: #EAE5DF;
  margin-top: 22px;
}

.t-line-step h4 {
  font-size: 0.86rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.t-line-step p {
  font-size: 0.76rem;
  color: #78716C;
  line-height: 1.35;
  margin: 0;
}

/* Soft Peach Tracking Card */
.peach-tracking-card {
  background: #FBF7F4;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 1.5rem;
  align-items: center;
}

.peach-visual-thumb {
  height: 110px;
  border-radius: 8px;
  overflow: hidden;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.peach-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.35rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.25rem;
}

.peach-sub {
  font-size: 0.84rem;
  color: #57534E;
  margin-bottom: 1rem;
}

.peach-input-form {
  display: flex;
  gap: 0.6rem;
  margin-bottom: 0.85rem;
}

.peach-text-input {
  flex: 1;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.65rem 1rem;
  font-size: 0.88rem;
  background: #FFFFFF;
  outline: none;
}

.btn-track-rect {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 0.65rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
  white-space: nowrap;
}

.btn-track-rect:hover {
  background: #73392E;
}

.tracking-live-alert {
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  color: #166534;
  padding: 0.5rem 0.85rem;
  border-radius: 6px;
  font-size: 0.84rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #16A34A;
}

.peach-help-anchor {
  font-size: 0.82rem;
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
}

.peach-help-anchor:hover {
  text-decoration: underline;
}

/* Col 3: Shipping FAQ */
.clean-accordion-list {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.clean-acc-item {
  border-bottom: 1px solid #EAE5DF;
}

.clean-acc-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.05rem 0;
  background: none;
  border: none;
  text-align: left;
  font-size: 0.94rem;
  font-weight: 600;
  color: #192A41;
  cursor: pointer;
  gap: 1rem;
}

.acc-chevron {
  color: #8E4A3E;
  transition: transform 0.2s ease;
}

.clean-acc-item.active .acc-chevron {
  transform: rotate(180deg);
}

.clean-acc-body {
  padding: 0 0 1rem 0;
}

.clean-acc-body p {
  font-size: 0.86rem;
  line-height: 1.6;
  color: #57534E;
  margin: 0;
}

.white-help-card-link {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 1.15rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
  transition: border-color 0.2s ease;
}

.white-help-card-link:hover {
  border-color: #8E4A3E;
}

.card-left-icon {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.red-mail {
  color: #8E4A3E;
}

.card-meta h4 {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.15rem;
}

.card-meta p {
  font-size: 0.8rem;
  color: #78716C;
  margin: 0;
}

.card-right-arrow {
  color: #8E4A3E;
  font-size: 1.1rem;
  font-weight: 700;
}

/* Responsive */
@media (max-width: 1024px) {
  .shipping-hero {
    grid-template-columns: 1fr;
  }
  .guarantees-strip {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .g-divider {
    display: none;
  }
  .delivery-three-layout {
    grid-template-columns: 1fr;
  }
}
</style>
