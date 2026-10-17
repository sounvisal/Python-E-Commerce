<template>
  <div class="returns-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Returns & Refunds</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="returns-hero">
        <div class="hero-left">
          <h1 class="hero-title">Returns & Refunds</h1>
          <p class="hero-tagline">Shop with confidence. We’re here to make things right.</p>
          <p class="hero-desc">
            If something isn’t quite right, our returns and refunds process is simple, fair, and hassle-free.
          </p>
        </div>

        <div class="hero-right">
          <div class="hero-media-wrap">
            <img src="/images/banner-my-orders.jpg" alt="Luméa Hassle-Free Returns" class="hero-banner-img" />
            <div class="hero-script-overlay">
              <span class="script-row">A Kinder</span>
              <span class="script-row">Shopping</span>
              <span class="script-row">Experience.</span>
              <div class="script-dash-sub"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 4 Principles Strip with Vertical Dividers -->
      <section class="principles-section">
        <div class="principles-strip">
          <div class="principle-col">
            <div class="p-pink-icon">
              <RotateCcw :size="22" />
            </div>
            <div class="p-text">
              <h3>Easy Returns</h3>
              <p>A simple and straightforward process.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="principle-col">
            <div class="p-pink-icon">
              <ShieldCheck :size="22" />
            </div>
            <div class="p-text">
              <h3>Fair Refunds</h3>
              <p>We make it right, quickly and transparently.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="principle-col">
            <div class="p-pink-icon">
              <Truck :size="22" />
            </div>
            <div class="p-text">
              <h3>Hassle-Free</h3>
              <p>Clear guidelines and support at every step.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="principle-col">
            <div class="p-pink-icon">
              <Leaf :size="22" />
            </div>
            <div class="p-text">
              <h3>A More Sustainable Approach</h3>
              <p>We responsibly handle returned products to reduce waste.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 3-Column Section: Vertical Stage + 4-Step Flow + FAQ -->
      <section class="returns-details-section">
        <div class="returns-three-layout">
          <!-- Col 1: Vertical Stage Photo Card -->
          <div class="returns-stage-col">
            <div class="stage-card-inner">
              <img src="/images/banner-deals.jpg" alt="Shop Confidently with Luméa" class="stage-photo" />
              <div class="stage-top-text">
                <h3 class="stage-script-headline">Real Care<br />Goes Both Ways.</h3>
                <div class="stage-dash"></div>
              </div>
              <div class="stage-bottom-text">
                <span>SHOP CONFIDENTLY<br />WITH LUMÉA.</span>
              </div>
            </div>
          </div>

          <!-- Col 2: 4-Step Process & Sustainability -->
          <div class="returns-flow-col">
            <div class="col-head-block">
              <span class="section-eyebrow">HOW TO RETURN</span>
              <h2 class="col-main-heading">A Simple 4-Step Process</h2>
              <p class="col-desc-text">Returning an item is easy. Just follow these steps:</p>
            </div>

            <!-- 4-Step Connected Timeline -->
            <div class="timeline-connected-row">
              <div class="t-line-step">
                <div class="t-icon-circle">
                  <ShoppingCart :size="18" />
                </div>
                <h4>1. Start a Return</h4>
                <p>Log in to your account and request a return.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle">
                  <Package :size="18" />
                </div>
                <h4>2. Pack Your Item</h4>
                <p>Securely pack the product in its original condition.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle">
                  <Truck :size="18" />
                </div>
                <h4>3. Ship It Back</h4>
                <p>Use the provided return instructions.</p>
              </div>

              <div class="t-connecting-bar"></div>

              <div class="t-line-step">
                <div class="t-icon-circle">
                  <CreditCard :size="18" />
                </div>
                <h4>4. Receive Your Refund</h4>
                <p>Once inspected, we’ll process your refund.</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons-row">
              <router-link to="/returns/request" class="btn-start-rect">Start a Return</router-link>
              <a href="#policy" class="btn-policy-link">
                View Full Return Policy <span class="arrow-right">→</span>
              </a>
            </div>

            <!-- Sustainable Promise Card (Peach background with vertical separator) -->
            <div class="peach-thoughtful-card">
              <div class="thoughtful-left">
                <div class="thoughtful-pink-icon">
                  <Leaf :size="20" />
                </div>
                <div class="thoughtful-text">
                  <h4>A More Thoughtful Tomorrow</h4>
                  <p>
                    Returned products that cannot be resold are carefully handled through responsible recycling or donation programs whenever possible.
                  </p>
                </div>
              </div>
              <div class="thoughtful-divider"></div>
              <div class="thoughtful-badge-col">
                <span>Better Choices<br />for a Brighter<br />Tomorrow.</span>
              </div>
            </div>
          </div>

          <!-- Col 3: Returns FAQs Accordion -->
          <div class="returns-faq-col">
            <div class="col-head-block">
              <span class="section-eyebrow">FREQUENTLY ASKED QUESTIONS</span>
              <h2 class="col-main-heading">Return Questions</h2>
            </div>

            <div class="clean-accordion-list">
              <div
                v-for="(item, idx) in returnFaqs"
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
  RotateCcw,
  ShieldCheck,
  Truck,
  Leaf,
  ShoppingCart,
  Package,
  CreditCard,
  ChevronDown,
  Mail
} from 'lucide-vue-next'

const openFaqIdx = ref(0)

const returnFaqs = [
  {
    question: 'What items can be returned?',
    answer:
      'We accept returns on unopened, unused skincare products in their original manufacturer packaging within 14 days of delivery. For hygienic reasons, opened beauty items cannot be returned unless you experienced an unexpected allergic reaction.'
  },
  {
    question: 'How long do I have to return an item?',
    answer:
      'You have 14 calendar days from the date your package was delivered to initiate a return request through your Luméa account or customer service.'
  },
  {
    question: 'When will I receive my refund?',
    answer:
      'Once our inspection team receives and verifies your returned package, your refund will be processed within 2 to 3 business days back to your original payment method.'
  },
  {
    question: 'Do I need the original packaging?',
    answer:
      'Yes, products must be returned in their original branded boxes with intact seals, batch codes, and included accessories or documentation.'
  },
  {
    question: 'Can I exchange my item?',
    answer:
      'Yes! If you would like a different shade, formula, or product, you can choose store credit or an exchange during the return setup process.'
  },
  {
    question: 'What if my item is damaged or incorrect?',
    answer:
      'If you received a damaged or incorrect product, contact us within 48 hours of delivery with a photo. We will immediately ship out a free replacement with priority express delivery.'
  },
  {
    question: 'Do you cover return shipping costs?',
    answer:
      'Return shipping is 100% free if the return is due to our error or a damaged product. For general preference returns, a flat $2.00 return handling fee is deducted from the refund.'
  },
  {
    question: 'How will I be refunded?',
    answer:
      'Refunds are credited to your original payment method (Credit/Debit Card, ABA Pay mobile account, or Luméa store credit).'
  }
]

function toggleFaq(idx) {
  openFaqIdx.value = openFaqIdx.value === idx ? null : idx
}
</script>

<style scoped>
.returns-page {
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

/* Open Hero Banner matching Returns & Refunds.png */
.returns-hero {
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
  font-size: 1.65rem;
  font-weight: 700;
  line-height: 1.2;
  color: #8E4A3E;
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.85);
}

.script-dash-sub {
  width: 32px;
  height: 2px;
  background: #8E4A3E;
  margin-top: 0.6rem;
}

/* 4 Principles Strip with Vertical Dividers */
.principles-section {
  margin-bottom: 3.5rem;
}

.principles-strip {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.75rem 2rem;
  justify-content: space-between;
}

.principle-col {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex: 1;
}

.p-pink-icon {
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

.p-text h3 {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.p-text p {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.4;
  margin: 0;
}

.p-divider {
  width: 1px;
  height: 48px;
  background: #EAE5DF;
  margin: 0 1.5rem;
  flex-shrink: 0;
}

/* 3-Column Layout */
.returns-details-section {
  margin-bottom: 2rem;
}

.returns-three-layout {
  display: grid;
  grid-template-columns: 280px 1.35fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Col 1: Vertical Stage Card */
.returns-stage-col {
  position: relative;
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

.stage-top-text {
  position: absolute;
  top: 2rem;
  left: 1.75rem;
}

.stage-script-headline {
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
  margin-top: 0.75rem;
}

.stage-bottom-text {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #57534E;
}

/* Col 2: 4-Step Process & Sustainability */
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
  margin-bottom: 1.75rem;
  padding: 1rem 0;
}

.t-line-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 115px;
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

/* Action Buttons */
.action-buttons-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.btn-start-rect {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.75rem 1.65rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-start-rect:hover {
  background: #73392E;
}

.btn-policy-link {
  font-size: 0.88rem;
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
}

.btn-policy-link:hover {
  text-decoration: underline;
}

/* Peach Thoughtful Card */
.peach-thoughtful-card {
  background: #FDF7F4;
  border: 1px solid #F3E6E0;
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.thoughtful-left {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.thoughtful-pink-icon {
  color: #C4623C;
  margin-top: 0.15rem;
  flex-shrink: 0;
}

.thoughtful-text h4 {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.1rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 0.25rem;
}

.thoughtful-text p {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0;
}

.thoughtful-divider {
  width: 1px;
  height: 50px;
  background: #EAE5DF;
  flex-shrink: 0;
}

.thoughtful-badge-col {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 0.85rem;
  color: #8E4A3E;
  font-weight: 600;
  line-height: 1.35;
  flex-shrink: 0;
}

/* Col 3: FAQ */
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
  .returns-hero {
    grid-template-columns: 1fr;
  }
  .principles-strip {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .p-divider {
    display: none;
  }
  .returns-three-layout {
    grid-template-columns: 1fr;
  }
}
</style>
