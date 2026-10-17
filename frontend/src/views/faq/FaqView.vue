<template>
  <div class="faq-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">FAQ</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="faq-hero">
        <div class="hero-left">
          <span class="hero-eyebrow">FREQUENTLY ASKED QUESTIONS</span>
          <h1 class="hero-title">How Can We Help?</h1>
          <p class="hero-desc">
            Find answers to common questions about shopping, products, orders, and more at Luméa.
          </p>
        </div>

        <div class="hero-right">
          <div class="hero-stage-container">
            <img src="/images/banner-my-account.jpg" alt="Luméa Care and Answers" class="hero-banner-img" />
            <div class="hero-script-overlay">
              <span class="script-row">Real Answers.</span>
              <span class="script-row">A Brighter</span>
              <span class="script-row">You. <Heart :size="18" class="script-heart-icon" /></span>
            </div>
          </div>
        </div>
      </section>

      <!-- 3-Column FAQ Layout -->
      <div class="faq-layout-grid">
        <!-- Left Column: Category Navigation -->
        <aside class="faq-categories-col">
          <nav class="cat-nav-list">
            <button
              v-for="cat in categories"
              :key="cat.id"
              class="cat-item-btn"
              :class="{ active: selectedCategory === cat.id }"
              @click="selectedCategory = cat.id"
            >
              <component :is="cat.icon" :size="18" class="cat-icon" />
              <span>{{ cat.name }}</span>
            </button>
          </nav>
        </aside>

        <!-- Middle Column: Accordion Q&A -->
        <main class="faq-main-col">
          <div class="faq-top-bar">
            <div class="top-bar-titles">
              <span class="section-eyebrow">{{ currentCategoryName.toUpperCase() }}</span>
              <h2 class="faq-heading">Frequently Asked Questions</h2>
            </div>

            <!-- Search Input -->
            <div class="faq-search-pill">
              <Search :size="16" class="search-icon" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search FAQs..."
                class="search-input"
              />
            </div>
          </div>

          <!-- Question Rows -->
          <div class="faq-items-list">
            <div
              v-for="(item, index) in filteredFaqs"
              :key="index"
              class="faq-row-item"
              :class="{ expanded: openItems.includes(index) }"
            >
              <button
                class="faq-question-btn"
                @click="toggleItem(index)"
                :aria-expanded="openItems.includes(index)"
              >
                <span class="q-text">{{ item.question }}</span>
                <span class="q-plus-icon">{{ openItems.includes(index) ? '−' : '+' }}</span>
              </button>
              <div v-show="openItems.includes(index)" class="faq-answer-panel">
                <p>{{ item.answer }}</p>
              </div>
            </div>

            <div v-if="filteredFaqs.length === 0" class="no-results-panel">
              <p>No questions found matching "<strong>{{ searchQuery }}</strong>".</p>
              <button @click="searchQuery = ''" class="btn-clear-pill">Clear Search</button>
            </div>
          </div>
        </main>

        <!-- Right Column: Support Card -->
        <aside class="faq-support-col">
          <div class="support-card-inner">
            <span class="support-eyebrow">STILL HAVE QUESTIONS?</span>
            <h3 class="support-title">We’re Here for You.</h3>
            <p class="support-desc">Our customer care team is always happy to help.</p>

            <router-link to="/contact" class="btn-contact-action">
              <MessageSquare :size="17" />
              <span>Contact Us</span>
            </router-link>

            <div class="support-channels-list">
              <div class="channel-row">
                <div class="channel-icon-box">
                  <Mail :size="18" />
                </div>
                <div class="channel-meta">
                  <span class="channel-title">Email Us</span>
                  <a href="mailto:support@lumea.com" class="channel-link">support@lumea.com</a>
                </div>
              </div>

              <div class="channel-row">
                <div class="channel-icon-box">
                  <MessageCircle :size="18" />
                </div>
                <div class="channel-meta">
                  <span class="channel-title">Live Chat</span>
                  <span class="channel-text">Available 9AM – 9PM (ICT)</span>
                </div>
              </div>

              <div class="channel-row">
                <div class="channel-icon-box">
                  <HelpCircle :size="18" />
                </div>
                <div class="channel-meta">
                  <span class="channel-title">Help Center</span>
                  <span class="channel-text">Browse more support resources</span>
                </div>
              </div>
            </div>

            <div class="support-footer-script">
              <div class="footer-dash"></div>
              <span class="script-tagline">A Kinder, More Confident Tomorrow.</span>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Search,
  MessageSquare,
  Mail,
  MessageCircle,
  HelpCircle,
  Truck,
  RotateCcw,
  Sparkles,
  CreditCard,
  HeartHandshake,
  Gift,
  Leaf,
  Layers,
  Heart
} from 'lucide-vue-next'

const selectedCategory = ref('all')
const searchQuery = ref('')
const openItems = ref([0]) // First question open by default

const categories = [
  { id: 'all', name: 'All Questions', icon: Layers },
  { id: 'orders', name: 'Orders & Shipping', icon: Truck },
  { id: 'returns', name: 'Returns & Refunds', icon: RotateCcw },
  { id: 'products', name: 'Products & Brands', icon: Sparkles },
  { id: 'account', name: 'Account & Payments', icon: CreditCard },
  { id: 'quiz', name: 'Skin Quiz & Recommendations', icon: HeartHandshake },
  { id: 'rewards', name: 'Promotions & Rewards', icon: Gift },
  { id: 'sustainability', name: 'Sustainability', icon: Leaf },
  { id: 'general', name: 'General', icon: HelpCircle }
]

const currentCategoryName = computed(() => {
  const c = categories.find((cat) => cat.id === selectedCategory.value)
  return c ? c.name : 'All Questions'
})

const faqData = [
  {
    category: 'orders',
    question: 'How do I place an order?',
    answer:
      'Browse our curated catalog, add your desired skincare items to your cart, and proceed to checkout. Enter your delivery address and preferred payment method, then review and place your order. You will receive an instant confirmation email and SMS with your order number.'
  },
  {
    category: 'account',
    question: 'What payment methods do you accept?',
    answer:
      'We accept all major credit and debit cards (Visa, Mastercard), ABA Pay / KHQR mobile banking for seamless Cambodian payments, and Cash on Delivery (COD) for eligible local delivery zones.'
  },
  {
    category: 'orders',
    question: 'How long does shipping take?',
    answer:
      'Within Phnom Penh, deliveries typically arrive within 24 to 48 hours. For other provinces across Cambodia, standard delivery takes between 2 to 4 business days. Express same-day delivery options are also available for Phnom Penh orders placed before 11:00 AM.'
  },
  {
    category: 'orders',
    question: 'Do you offer free shipping?',
    answer:
      'Yes! We provide complimentary standard shipping on all orders over $35 within Phnom Penh, and on orders over $50 for all other provinces across Cambodia.'
  },
  {
    category: 'orders',
    question: 'How can I track my order?',
    answer:
      'Once your package has shipped, you will receive a tracking link via SMS and email. You can also visit our dedicated Shipping & Delivery page and enter your order number into the live tracking box.'
  },
  {
    category: 'returns',
    question: 'What is your return policy?',
    answer:
      'We offer a 14-day hassle-free return policy for unopened, unused products in their original packaging. If you experience an unexpected allergic reaction or receive a damaged item, our care team will resolve it immediately with a replacement or full refund.'
  },
  {
    category: 'products',
    question: 'How do I know if a product is authentic?',
    answer:
      '100% authenticity is our foundational promise. Luméa works exclusively with authorized distributors, official brand partners, and licensed manufacturers. Every item has genuine batch codes, verified seals, and tamper-proof packaging.'
  },
  {
    category: 'quiz',
    question: 'Can you help me find the right products for my skin?',
    answer:
      'Absolutely! We recommend taking our 2-minute personalized Skin Quiz. It assesses your skin type, environmental factors, and primary concerns to craft a custom morning and evening routine.'
  },
  {
    category: 'rewards',
    question: 'Do you offer discounts or promotions?',
    answer:
      'Yes, we regularly offer seasonal curated promotions, member-exclusive discounts, and loyalty reward points on every single dollar spent. Check out our Deals page for active offers.'
  },
  {
    category: 'general',
    question: 'How do I contact customer support?',
    answer:
      'You can reach our friendly support team via Live Chat (9AM–9PM ICT), email at support@lumea.com, or phone at +855 23 900 123 from Monday to Friday.'
  }
]

const filteredFaqs = computed(() => {
  return faqData.filter((item) => {
    const matchesCategory =
      selectedCategory.value === 'all' || item.category === selectedCategory.value
    const matchesSearch =
      searchQuery.value === '' ||
      item.question.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.answer.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCategory && matchesSearch
  })
})

function toggleItem(index) {
  if (openItems.value.includes(index)) {
    openItems.value = openItems.value.filter((i) => i !== index)
  } else {
    openItems.value.push(index)
  }
}
</script>

<style scoped>
.faq-page {
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

/* Open Hero Banner */
.faq-hero {
  display: grid;
  grid-template-columns: 1.1fr 1.15fr;
  align-items: center;
  gap: 2.5rem;
  margin-bottom: 2.25rem;
  padding: 1.75rem 2.5rem;
  min-height: 275px;
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

.hero-eyebrow {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #8E4A3E;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.75rem;
  font-weight: 700;
  line-height: 1.12;
  color: #111C38;
  margin-bottom: 0.75rem;
  letter-spacing: -0.01em;
}

.hero-desc {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 1.15rem;
  line-height: 1.55;
  color: #44403C;
  max-width: 520px;
}

.hero-stage-container {
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
  animation: heroFloat 6s ease-in-out infinite alternate;
}

@keyframes heroFloat {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-6px); }
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

.script-heart-icon {
  display: inline-block;
  vertical-align: -2px;
  margin-left: 4px;
  color: #C25E4D;
  fill: #C25E4D;
}

/* 3-Column Layout */
.faq-layout-grid {
  display: grid;
  grid-template-columns: 220px 1fr 280px;
  gap: 2.5rem;
  align-items: start;
}

/* Left: Category Nav without card box */
.cat-nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.cat-item-btn {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #44403C;
  font-size: 0.88rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-item-btn:hover {
  background: #F4EFEB;
  color: #192A41;
}

.cat-item-btn.active {
  background: #FDF2EE;
  color: #8E4A3E;
  font-weight: 700;
}

.cat-icon {
  flex-shrink: 0;
}

/* Middle: Main Q&A */
.faq-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  gap: 1.5rem;
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

.faq-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #192A41;
  margin: 0;
}

.faq-search-pill {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 24px;
  padding: 0.55rem 1.15rem;
  width: 250px;
}

.search-icon {
  color: #78716C;
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.88rem;
  color: #1C1917;
  width: 100%;
}

.faq-items-list {
  display: flex;
  flex-direction: column;
}

.faq-row-item {
  border-bottom: 1px solid #EAE5DF;
}

.faq-question-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.35rem 0;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  gap: 1.5rem;
}

.q-text {
  font-size: 1.05rem;
  font-weight: 600;
  color: #192A41;
  transition: color 0.2s ease;
}

.faq-question-btn:hover .q-text {
  color: #8E4A3E;
}

.q-plus-icon {
  font-size: 1.5rem;
  color: #C4623C;
  font-weight: 400;
  line-height: 1;
  flex-shrink: 0;
}

.faq-answer-panel {
  padding: 0 0 1.5rem 0;
  animation: fadeIn 0.25s ease;
}

.faq-answer-panel p {
  font-size: 0.94rem;
  line-height: 1.65;
  color: #57534E;
  margin: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.no-results-panel {
  padding: 3rem 1rem;
  text-align: center;
  color: #78716C;
}

.btn-clear-pill {
  margin-top: 1rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1.25rem;
  font-size: 0.85rem;
  cursor: pointer;
}

/* Right Column: Support Card */
.faq-support-col {
  position: sticky;
  top: 5.5rem;
}

.support-card-inner {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2.2rem 1.75rem;
  box-shadow: 0 4px 16px rgba(28, 25, 23, 0.03);
}

.support-eyebrow {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #8E4A3E;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.5rem;
}

.support-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.75rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.35rem;
}

.support-desc {
  font-size: 0.86rem;
  color: #78716C;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.btn-contact-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.8rem 1.25rem;
  border-radius: 8px;
  font-size: 0.92rem;
  font-weight: 600;
  text-decoration: none;
  margin-bottom: 1.75rem;
  transition: all 0.2s ease;
}

.btn-contact-action:hover {
  background: #73392E;
  transform: translateY(-1px);
}

.support-channels-list {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.channel-row {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
}

.channel-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.channel-meta {
  display: flex;
  flex-direction: column;
}

.channel-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
}

.channel-link {
  font-size: 0.82rem;
  color: #8E4A3E;
  text-decoration: none;
}

.channel-text {
  font-size: 0.8rem;
  color: #78716C;
}

.support-footer-script {
  margin-top: 2rem;
}

.footer-dash {
  width: 32px;
  height: 2px;
  background: #C4623C;
  margin-bottom: 0.85rem;
}

.script-tagline {
  font-family: var(--font-script, 'Cormorant Garamond', Georgia, serif);
  font-style: italic;
  font-size: 1.35rem;
  line-height: 1.25;
  color: #C25E4D;
  display: block;
}

/* Responsive */
@media (max-width: 1024px) {
  .faq-hero {
    grid-template-columns: 1fr;
  }
  .faq-layout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
