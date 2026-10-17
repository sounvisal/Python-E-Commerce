<template>
  <div class="lumea-editorial-terms-page">
    <!-- Header Banner -->
    <header class="terms-hero-banner">
      <div class="container hero-banner-inner">
        <div class="hero-left-text">
          <nav class="breadcrumb-nav" aria-label="Breadcrumb">
            <router-link to="/">Home</router-link>
            <span class="bc-sep">&rsaquo;</span>
            <span class="bc-current">Terms of Service</span>
          </nav>

          <span class="terms-badge">TERMS OF SERVICE</span>
          <h1 class="terms-main-title">{{ pageData.title }}</h1>
          <p class="terms-subtitle">{{ pageData.subtitle }}</p>
          <span class="terms-date">Last updated: {{ pageData.last_updated }}</span>
        </div>

        <div class="hero-right-visual">
          <div class="hero-image-frame">
            <img
              :src="pageData.hero_image || '/images/terms-header-bottles.jpg'"
              alt="Luméa Atelier - Beauty Built on Trust"
              class="hero-bottles-img"
            />
            <div class="hero-script-overlay">
              <span class="script-cursive">Beauty</span>
              <span class="script-cursive">Built on Trust</span>
              <div class="script-underline"></div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Layout with 3 Columns: TOC / Content / Commitments -->
    <main class="container terms-body-grid">
      <!-- Left: Sticky Table of Contents -->
      <aside class="terms-toc-col">
        <div class="toc-sticky-box">
          <h3 class="toc-heading">In This Article</h3>
          <nav class="toc-nav-list">
            <button
              v-for="sec in sections"
              :key="sec.id"
              class="toc-nav-item"
              :class="{ 'is-active': activeSectionId === sec.slug }"
              @click="scrollToSection(sec.slug)"
            >
              <span class="toc-num">{{ sec.id }}</span>
              <span class="toc-label">{{ sec.title }}</span>
            </button>
          </nav>
        </div>
      </aside>

      <!-- Center: Main Article Content -->
      <article class="terms-article-content">
        <section
          v-for="sec in sections"
          :key="sec.id"
          :id="sec.slug"
          class="terms-section-block"
        >
          <div class="section-header-row">
            <span class="sec-num-prefix">{{ sec.id }}.</span>
            <h2 class="sec-title">{{ sec.title }}</h2>
          </div>

          <!-- Paragraph Text -->
          <div v-if="sec.content" class="sec-paragraph-text">
            <p v-for="(p, pIdx) in sec.content.split('\n\n')" :key="pIdx">
              {{ p }}
            </p>
          </div>

          <!-- Thoughtful Banner inside Section 01 -->
          <div v-if="sec.slug === 'introduction'" class="thoughtful-experience-banner">
            <img
              src="/images/terms-thoughtful-banner.jpg"
              alt="Thoughtful Beauty Experiences"
              class="thoughtful-img"
            />
            <div class="thoughtful-overlay">
              <h3 class="thoughtful-title">Thoughtful Beauty Experiences</h3>
              <p class="thoughtful-desc">
                Our services, products, and policies are designed to give you a safe, transparent, and enjoyable experience.
              </p>
            </div>
          </div>

          <!-- Visual 4-Card Grid for Section 02 (Your Account) -->
          <div v-if="sec.cards && sec.cards.length" class="account-rules-grid">
            <div
              v-for="(card, cIdx) in sec.cards"
              :key="cIdx"
              class="account-rule-card"
            >
              <div class="card-icon-bubble">
                <component :is="getCardIcon(card.icon)" :size="20" />
              </div>
              <h4 class="card-title">{{ card.title }}</h4>
              <p class="card-desc">{{ card.description }}</p>
            </div>
          </div>
        </section>
      </article>

      <!-- Right: Commitments & Concierge Help Column -->
      <aside class="terms-sidebar-col">
        <div class="sidebar-sticky-box">
          <!-- Commitment Card -->
          <div class="commitment-card">
            <span class="commitment-eyebrow">OUR COMMITMENT</span>
            <h3 class="commitment-title">A Fair and Transparent Experience</h3>
            <p class="commitment-intro">
              We aim to make our terms clear, fair, and easy to understand — so you can shop with confidence.
            </p>

            <div class="commitment-list">
              <div class="commit-item">
                <div class="commit-icon-col">
                  <Shield :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Fair and honest policies</h5>
                  <p>Transparent practices with no surprises.</p>
                </div>
              </div>

              <div class="commit-item">
                <div class="commit-icon-col">
                  <PackageCheck :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Clear ordering and return process</h5>
                  <p>Step-by-step guidance every order.</p>
                </div>
              </div>

              <div class="commit-item">
                <div class="commit-icon-col">
                  <Heart :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Respect for customers and brands</h5>
                  <p>Authentic products with curated respect.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Need Help? Card with Portrait -->
          <div class="contact-box-card">
            <div class="contact-card-top">
              <div class="contact-text-wrap">
                <h4>Need Help?</h4>
                <p>If you have any questions about these Terms of Service, our team is here to help.</p>
              </div>
              <img
                src="/images/terms-help-portrait.jpg"
                alt="Luméa Concierge Support"
                class="help-portrait-thumb"
              />
            </div>
            <router-link to="/contact" class="btn-contact-action">
              <Mail :size="15" />
              <span>Contact Us &rarr;</span>
            </router-link>
          </div>

          <!-- Editorial Quote Card with Leaves -->
          <div class="botanical-quote-card">
            <img
              src="/images/terms-integrity-banner.jpg"
              alt="Where skincare meets integrity"
              class="botanical-bg-img"
            />
            <div class="botanical-overlay">
              <h4 class="quote-title">&ldquo;Where skincare meets integrity.&rdquo;</h4>
              <div class="quote-dash"></div>
            </div>
          </div>
        </div>
      </aside>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import {
  User,
  Lock,
  Edit3,
  Users,
  Shield,
  PackageCheck,
  Heart,
  Mail
} from 'lucide-vue-next'

const pageData = ref({
  title: 'Terms of Service',
  subtitle: 'These Terms of Service govern your use of the Luméa website and our products and services.',
  last_updated: 'August 15, 2025',
  hero_image: '/images/terms-header-bottles.jpg'
})

const sections = ref([
  {
    id: '01',
    slug: 'introduction',
    title: 'Introduction',
    content: `Welcome to Luméa. These Terms of Service ("Terms") govern your access to and use of our website, products, and services, including any purchases, content, and features available through our platform.\n\nBy creating an account, browsing our website, or placing an order, you agree to be bound by these Terms. If you do not agree with any part of these Terms, please do not use our website.`
  },
  {
    id: '02',
    slug: 'your-account',
    title: 'Your Account',
    content: `You may be required to create an account to access certain features, such as placing orders, saving your wishlist, or using the Skin Quiz.`,
    cards: [
      {
        icon: 'User',
        title: 'Accurate Information',
        description: 'You agree to provide accurate, complete, and up-to-date information.'
      },
      {
        icon: 'Lock',
        title: 'Account Security',
        description: 'You are responsible for keeping your login credentials secure.'
      },
      {
        icon: 'Edit3',
        title: 'One Account Per User',
        description: 'Each user may only maintain one account. We reserve the right to suspend duplicate accounts.'
      },
      {
        icon: 'Users',
        title: 'Notify Us of Changes',
        description: 'Please update your information if there are any changes (e.g. email address, phone number).'
      }
    ]
  },
  {
    id: '03',
    slug: 'placing-orders',
    title: 'Placing Orders',
    content: `When you place an order on Luméa, you agree to provide complete and accurate information, including shipping address, contact details, and payment information. All orders are subject to availability and confirmation.`
  },
  {
    id: '04',
    slug: 'prices-and-payment',
    title: 'Prices and Payment',
    content: `All catalog prices are denominated in USD ($). We accept major credit cards, Apple Pay, and authorized regional payment methods. Prices are subject to revision without prior notice, though pending orders are honored at the checked-out price.`
  },
  {
    id: '05',
    slug: 'order-confirmation',
    title: 'Order Confirmation',
    content: `Upon submitting checkout, you will receive an automated confirmation with an assigned order reference (e.g. LUM-XXXXXX). Receipt of confirmation indicates your order has entered preparation.`
  },
  {
    id: '06',
    slug: 'cancellation-and-changes',
    title: 'Cancellation and Changes',
    content: `Orders enter atelier fulfillment swiftly. If you need to revise shipping details or cancel an item, please submit a request within 1 hour of placement.`
  },
  {
    id: '07',
    slug: 'delivery-and-shipping',
    title: 'Delivery and Shipping',
    content: `Estimated delivery times are calculated upon courier handover. While we aim for prompt dispatch within 24-48 hours, transit schedules may fluctuate due to customs clearance or regional logistics.`
  },
  {
    id: '08',
    slug: 'returns-and-refunds',
    title: 'Returns and Refunds',
    content: `We offer a 30-day return window for unopened items in original laboratory packaging. Return requests can be filed through our dedicated Return Request Wizard.`
  },
  {
    id: '09',
    slug: 'product-information',
    title: 'Product Information',
    content: `We curate 100% authentic dermatological formulations. Customers with hyper-reactive skin or allergies are encouraged to check complete ingredient lists and perform patch tests.`
  },
  {
    id: '10',
    slug: 'intellectual-property',
    title: 'Intellectual Property',
    content: `All logos, photography, formulations catalogs, and editorial journal articles are protected under copyright and trademark treaties.`
  },
  {
    id: '11',
    slug: 'prohibited-use',
    title: 'Prohibited Use',
    content: `You may not misuse our platform to distribute malware, reverse-engineer proprietary algorithms, conduct unauthorized bulk scraping, or engage in resale speculation.`
  },
  {
    id: '12',
    slug: 'limitation-of-liability',
    title: 'Limitation of Liability',
    content: `Luméa shall not be held liable for indirect or consequential damages arising from unforeseen platform interruptions or third-party delivery delays.`
  },
  {
    id: '13',
    slug: 'changes-to-these-terms',
    title: 'Changes to These Terms',
    content: `We reserve the right to amend these Terms to reflect service enhancements. Continued use of our site signifies acceptance of amended terms.`
  },
  {
    id: '14',
    slug: 'governing-law',
    title: 'Governing Law',
    content: `These Terms are governed by and construed in accordance with the laws of Cambodia and applicable international consumer treaties.`
  },
  {
    id: '15',
    slug: 'contact-us',
    title: 'Contact Us',
    content: `If you have any questions about these Terms of Service, our customer care team is here to assist at contact@lumea.com.`
  }
])

const activeSectionId = ref('introduction')

function getCardIcon(iconName) {
  switch (iconName) {
    case 'User': return User
    case 'Lock': return Lock
    case 'Edit3': return Edit3
    case 'Users': return Users
    default: return User
  }
}

function scrollToSection(slug) {
  activeSectionId.value = slug
  const el = document.getElementById(slug)
  if (el) {
    const yOffset = -90
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

let observer = null

async function loadPageFromAPI() {
  try {
    const res = await fetch('/api/pages/terms-of-service')
    if (res.ok) {
      const data = await res.json()
      pageData.value = {
        title: data.title || pageData.value.title,
        subtitle: data.subtitle || pageData.value.subtitle,
        last_updated: data.last_updated || pageData.value.last_updated,
        hero_image: data.hero_image || pageData.value.hero_image
      }
      if (data.content_json?.sections) {
        sections.value = data.content_json.sections
      }
    }
  } catch (err) {
    console.warn('[TermsOfService] Falling back to local content schema:', err)
  }
}

onMounted(() => {
  loadPageFromAPI()

  const sectionElements = document.querySelectorAll('.terms-section-block')
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeSectionId.value = entry.target.id
        }
      })
    },
    { rootMargin: '-20% 0px -70% 0px' }
  )

  sectionElements.forEach((el) => observer.observe(el))
})

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.lumea-editorial-terms-page {
  background: #FCFAF7;
  min-height: 100vh;
  color: #1C1917;
  padding-bottom: 6rem;
}

/* Hero Banner */
.terms-hero-banner {
  background: #F5EFEB;
  border-bottom: 1px solid rgba(122, 46, 34, 0.08);
  padding: 2.5rem 0 3.5rem;
  margin-bottom: 3.5rem;
}

.hero-banner-inner {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  align-items: center;
  gap: 3rem;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
  margin-bottom: 1.25rem;
}

.breadcrumb-nav a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb-nav a:hover {
  color: #7A2E22;
}

.bc-sep {
  color: #A8A29E;
}

.bc-current {
  color: #1C1917;
  font-weight: 500;
}

.terms-badge {
  display: inline-block;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #7A2E22;
  margin-bottom: 0.75rem;
}

.terms-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.4rem, 4vw, 3.4rem);
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 1rem;
  line-height: 1.15;
}

.terms-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  color: #57534E;
  line-height: 1.6;
  margin: 0 0 1.25rem;
  max-width: 580px;
}

.terms-date {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
}

/* Right Hero Visual */
.hero-right-visual {
  display: flex;
  justify-content: flex-end;
}

.hero-image-frame {
  position: relative;
  max-width: 480px;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 12px 30px -8px rgba(122, 46, 34, 0.15);
}

.hero-bottles-img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.hero-script-overlay {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  text-align: right;
  pointer-events: none;
}

.script-cursive {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: 1.45rem;
  color: #8C4334;
  display: block;
  line-height: 1.15;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.9);
}

.script-underline {
  width: 50px;
  height: 2px;
  background: #8C4334;
  margin-left: auto;
  margin-top: 0.35rem;
}

/* Main 3-Column Grid */
.terms-body-grid {
  display: grid;
  grid-template-columns: 240px 1fr 310px;
  gap: 3.5rem;
  align-items: start;
}

/* Left Column: TOC */
.toc-sticky-box {
  position: sticky;
  top: 100px;
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
}

.toc-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 1.25rem;
  padding-left: 0.5rem;
}

.toc-nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.toc-nav-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: transparent;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 0.6rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', sans-serif;
  width: 100%;
}

.toc-nav-item:hover {
  background: #F5EFEB;
}

.toc-nav-item.is-active {
  background: #F5E8E5;
}

.toc-num {
  font-size: 0.78rem;
  font-weight: 600;
  color: #78716C;
  min-width: 18px;
}

.toc-nav-item.is-active .toc-num {
  color: #7A2E22;
}

.toc-label {
  font-size: 0.82rem;
  color: #44403C;
  line-height: 1.35;
}

.toc-nav-item.is-active .toc-label {
  color: #7A2E22;
  font-weight: 600;
}

/* Center Article Content */
.terms-article-content {
  max-width: 680px;
}

.terms-section-block {
  margin-bottom: 3.5rem;
  scroll-margin-top: 100px;
}

.section-header-row {
  margin-bottom: 1.25rem;
}

.sec-num-prefix {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: #7A2E22;
  display: block;
  margin-bottom: 0.25rem;
}

.sec-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.85rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0;
  line-height: 1.25;
}

.sec-paragraph-text p {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  color: #44403C;
  line-height: 1.7;
  margin: 0 0 1.25rem;
}

/* Thoughtful Banner inside Section 01 */
.thoughtful-experience-banner {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  margin: 1.75rem 0 2.5rem;
  box-shadow: 0 8px 24px rgba(122, 46, 34, 0.08);
}

.thoughtful-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
}

.thoughtful-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.9) 35%, rgba(255, 255, 255, 0.5) 100%);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 440px;
}

.thoughtful-title {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: 1.35rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.4rem;
}

.thoughtful-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #44403C;
  line-height: 1.45;
  margin: 0;
}

/* Visual 4-Card Grid for Your Account */
.account-rules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin: 1.75rem 0 2rem;
}

.account-rule-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.account-rule-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(122, 46, 34, 0.08);
}

.card-icon-bubble {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #F9EFEF;
  color: #7A2E22;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.5rem;
}

.card-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0;
}

/* Right Column: Commitments & Concierge */
.sidebar-sticky-box {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.commitment-card {
  background: #FFFBF8;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.75rem 1.5rem;
}

.commitment-eyebrow {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #7A2E22;
  margin-bottom: 0.4rem;
}

.commitment-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.75rem;
  line-height: 1.25;
}

.commitment-intro {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.5rem;
}

.commitment-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.commit-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.commit-icon-col {
  color: #7A2E22;
  margin-top: 0.15rem;
}

.commit-text-col h5 {
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.2rem;
}

.commit-text-col p {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #78716C;
  line-height: 1.4;
  margin: 0;
}

/* Need Help? Card */
.contact-box-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
}

.contact-card-top {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.contact-text-wrap h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.4rem;
}

.contact-text-wrap p {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.45;
  margin: 0;
}

.help-portrait-thumb {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid #F5EFEB;
}

.btn-contact-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-contact-action:hover {
  background: #5E2117;
}

/* Botanical Quote Card */
.botanical-quote-card {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.botanical-bg-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
}

.botanical-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.88) 50%, rgba(255, 255, 255, 0.4) 100%);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.quote-title {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: 1.25rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
  line-height: 1.25;
}

.quote-dash {
  width: 32px;
  height: 2px;
  background: #7A2E22;
}

/* Responsive */
@media (max-width: 1200px) {
  .terms-body-grid {
    grid-template-columns: 220px 1fr;
  }
  .terms-sidebar-col {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 860px) {
  .hero-banner-inner {
    grid-template-columns: 1fr;
  }
  .hero-right-visual {
    justify-content: center;
  }
  .terms-body-grid {
    grid-template-columns: 1fr;
  }
  .terms-toc-col {
    display: none;
  }
  .account-rules-grid {
    grid-template-columns: 1fr;
  }
}
</style>
