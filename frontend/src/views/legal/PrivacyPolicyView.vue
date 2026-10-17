<template>
  <div class="lumea-editorial-policy-page">
    <!-- Header Banner -->
    <header class="policy-hero-banner">
      <div class="container hero-banner-inner">
        <div class="hero-left-text">
          <nav class="breadcrumb-nav" aria-label="Breadcrumb">
            <router-link to="/">Home</router-link>
            <span class="bc-sep">&rsaquo;</span>
            <span class="bc-current">Privacy Policy</span>
          </nav>

          <span class="policy-badge">LEGAL &amp; PRIVACY</span>
          <h1 class="policy-main-title">{{ pageData.title }}</h1>
          <p class="policy-subtitle">{{ pageData.subtitle }}</p>
          <span class="policy-date">Last updated: {{ pageData.last_updated }}</span>
        </div>

        <div class="hero-right-visual">
          <div class="hero-image-frame">
            <img
              :src="pageData.hero_image || '/images/privacy-header-bottles.jpg'"
              alt="Luméa Natural Beauty - Your Privacy Our Priority"
              class="hero-bottles-img"
            />
            <div class="hero-script-overlay">
              <span class="script-cursive">Your Privacy</span>
              <span class="script-cursive">Our Priority</span>
              <div class="script-underline"></div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Layout with 3 Columns: TOC / Content / Commitments -->
    <main class="container policy-body-grid">
      <!-- Left: Sticky Table of Contents -->
      <aside class="policy-toc-col">
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
      <article class="policy-article-content">
        <section
          v-for="sec in sections"
          :key="sec.id"
          :id="sec.slug"
          class="policy-section-block"
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

          <!-- Visual 4-Card Grid for Section 02 -->
          <div v-if="sec.cards && sec.cards.length" class="info-collect-grid">
            <div
              v-for="(card, cIdx) in sec.cards"
              :key="cIdx"
              class="info-card-atelier"
            >
              <div class="card-icon-bubble">
                <component :is="getCardIcon(card.icon)" :size="20" />
              </div>
              <h4 class="card-title">{{ card.title }}</h4>
              <p class="card-desc">{{ card.description }}</p>
            </div>
          </div>

          <!-- Bulleted List for Section 03 -->
          <ul v-if="sec.bullets && sec.bullets.length" class="policy-bullet-list">
            <li v-for="(b, bIdx) in sec.bullets" :key="bIdx" class="bullet-item">
              <span class="bullet-dot"></span>
              <span class="bullet-text">{{ b }}</span>
            </li>
          </ul>
        </section>
      </article>

      <!-- Right: Commitments & Concierge Help Column -->
      <aside class="policy-sidebar-col">
        <div class="sidebar-sticky-box">
          <!-- Privacy Commitment Card -->
          <div class="commitment-card">
            <span class="commitment-eyebrow">OUR PRIVACY COMMITMENT</span>
            <h3 class="commitment-title">Your Trust Matters</h3>
            <p class="commitment-intro">
              Your trust matters to us. We follow strict standards to keep your information safe and secure.
            </p>

            <div class="commitment-list">
              <div class="commit-item">
                <div class="commit-icon-col">
                  <ShieldCheck :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Secure &amp; Protected</h5>
                  <p>We use industry-standard security measures.</p>
                </div>
              </div>

              <div class="commit-item">
                <div class="commit-icon-col">
                  <EyeOff :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>We Never Sell Your Data</h5>
                  <p>We do not sell your personal information to third parties.</p>
                </div>
              </div>

              <div class="commit-item">
                <div class="commit-icon-col">
                  <Lock :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Transparent Practices</h5>
                  <p>We are clear about how we use your information.</p>
                </div>
              </div>

              <div class="commit-item">
                <div class="commit-icon-col">
                  <Users :size="18" class="c-icon" />
                </div>
                <div class="commit-text-col">
                  <h5>Your Choices Matter</h5>
                  <p>You can manage your preferences at any time.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Have Questions Card -->
          <div class="contact-box-card">
            <h4>Have Questions?</h4>
            <p>
              If you have any questions about this Privacy Policy or how we handle your data, please contact our privacy team.
            </p>
            <a href="mailto:privacy@lumea.com" class="btn-contact-mail">
              <Mail :size="16" />
              <span>privacy@lumea.com</span>
            </a>
          </div>

          <!-- Editorial Botanical Quote Card -->
          <div class="botanical-quote-card">
            <img
              src="/images/privacy-botanical-banner.jpg"
              alt="A Safer, Brighter Tomorrow"
              class="botanical-bg-img"
            />
            <div class="botanical-overlay">
              <h4 class="quote-title">A Safer,<br>Brighter Tomorrow</h4>
              <p class="quote-desc">Your privacy helps us create a better, more personalized beauty experience.</p>
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
  ShoppingCart,
  Leaf,
  Laptop,
  ShieldCheck,
  EyeOff,
  Lock,
  Users,
  Mail
} from 'lucide-vue-next'

const pageData = ref({
  title: 'Privacy Policy',
  subtitle: 'We respect your privacy and are committed to protecting your personal information.',
  last_updated: 'August 15, 2025',
  hero_image: '/images/privacy-header-bottles.jpg'
})

const sections = ref([
  {
    id: '01',
    slug: 'introduction',
    title: 'Introduction',
    content: `Luméa ("we", "us", or "our") respects your privacy and is committed to protecting your personal information. This Privacy Policy explains how we collect, use, share, and safeguard your information when you visit our website, create an account, place an order, or use any of our services.\n\nBy using our website and services, you agree to the practices described in this Privacy Policy. If you do not agree, please do not use our website.`
  },
  {
    id: '02',
    slug: 'information-we-collect',
    title: 'Information We Collect',
    content: `We may collect different types of information depending on how you use our website and services.`,
    cards: [
      {
        icon: 'User',
        title: 'Account Information',
        description: 'Name, email address, phone number, and password when you create an account.'
      },
      {
        icon: 'ShoppingCart',
        title: 'Order Information',
        description: 'Shipping address, billing address, order history, and payment information.'
      },
      {
        icon: 'Leaf',
        title: 'Skin Profile Information',
        description: 'Skin type, skin concerns, and quiz results when you use our skin quiz feature.'
      },
      {
        icon: 'Laptop',
        title: 'Device and Usage Information',
        description: 'IP address, device type, browser, pages visited, and other analytics data.'
      }
    ]
  },
  {
    id: '03',
    slug: 'how-we-use-your-information',
    title: 'How We Use Your Information',
    content: `We use your information for the following purposes:`,
    bullets: [
      'To create and manage your account',
      'To process and fulfill your orders',
      'To provide customer support and respond to your inquiries',
      'To personalize your shopping experience and product recommendations',
      'To send transactional notifications, order confirmations, and shipment updates',
      'To continuously refine our skincare formulas catalog and digital experience'
    ]
  },
  {
    id: '04',
    slug: 'legal-bases',
    title: 'Legal Bases for Processing (For EU/EEA Users)',
    content: `We process personal information under defined legal bases: Contractual Necessity (order delivery and account access), Legitimate Interests (fraud detection, platform stability), Legal Obligation (accounting, taxation records), and Explicit Consent (custom diagnostic quiz and newsletter subscription).`
  },
  {
    id: '05',
    slug: 'sharing-information',
    title: 'How We Share Your Information',
    content: `We never sell, rent, or trade your personal information to third parties. We share data solely with verified infrastructure partners who assist in our daily operations (secure payment processors, licensed global couriers like DHL/Cambodia Post, and encrypted cloud hosts) under strict confidentiality agreements.`
  },
  {
    id: '06',
    slug: 'cookies',
    title: 'Cookies and Similar Technologies',
    content: `We utilize essential cookies to retain cart contents, maintain authentication state, and store user preferences. Analytical cookies help us measure user journeys to improve site speed. You can manage or revoke cookie permissions via your browser controls.`
  },
  {
    id: '07',
    slug: 'data-security',
    title: 'Data Security',
    content: `All network transactions are secured with TLS 1.3 encryption. Customer passwords and sensitive secrets are stored using cryptographic hashes (bcrypt). Our database backups are encrypted and stored in secure facilities.`
  },
  {
    id: '08',
    slug: 'your-rights',
    title: 'Your Rights and Choices',
    content: `You retain full control over your personal data. You have the right to request a copy of your records, correct inaccurate details, request account deletion, or opt out of promotional messages at any time directly in your account dashboard.`
  },
  {
    id: '09',
    slug: 'data-retention',
    title: 'Data Retention',
    content: `We retain your order histories and profile metrics as long as your account remains active or as required by law for taxation and financial audit periods.`
  },
  {
    id: '10',
    slug: 'children-privacy',
    title: "Children's Privacy",
    content: `Luméa does not target or knowingly collect data from children under 16 years of age. If we identify that a minor has provided data without guardian consent, we will promptly purge the records.`
  },
  {
    id: '11',
    slug: 'international-transfers',
    title: 'International Data Transfers',
    content: `Where cross-border data transfer occurs for logistics and cloud hosting, we ensure that adequate protection standards and contractual clauses are maintained.`
  },
  {
    id: '12',
    slug: 'changes-to-policy',
    title: 'Changes to This Privacy Policy',
    content: `We may update this policy periodically to align with evolving international data laws. Major revisions will be highlighted on our homepage.`
  },
  {
    id: '13',
    slug: 'contact-us',
    title: 'Contact Us',
    content: `If you have questions regarding this Privacy Policy or wish to exercise your data rights, please contact our concierge team at privacy@lumea.com.`
  }
])

const activeSectionId = ref('introduction')

function getCardIcon(iconName) {
  switch (iconName) {
    case 'User': return User
    case 'ShoppingCart': return ShoppingCart
    case 'Leaf': return Leaf
    case 'Laptop': return Laptop
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
    const res = await fetch('/api/pages/privacy-policy')
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
    console.warn('[PrivacyPolicy] Falling back to local content schema:', err)
  }
}

onMounted(() => {
  loadPageFromAPI()

  // IntersectionObserver for active TOC highlight
  const sectionElements = document.querySelectorAll('.policy-section-block')
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
.lumea-editorial-policy-page {
  background: #FCFAF7;
  min-height: 100vh;
  color: #1C1917;
  padding-bottom: 6rem;
}

/* Hero Banner */
.policy-hero-banner {
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

.policy-badge {
  display: inline-block;
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #7A2E22;
  margin-bottom: 0.75rem;
}

.policy-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.4rem, 4vw, 3.4rem);
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 1rem;
  line-height: 1.15;
}

.policy-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.05rem;
  color: #57534E;
  line-height: 1.6;
  margin: 0 0 1.25rem;
  max-width: 580px;
}

.policy-date {
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
.policy-body-grid {
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
.policy-article-content {
  max-width: 680px;
}

.policy-section-block {
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

/* 4-Card Visual Grid for Information We Collect */
.info-collect-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin: 1.75rem 0 2rem;
}

.info-card-atelier {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.info-card-atelier:hover {
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

/* Bulleted List */
.policy-bullet-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.bullet-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.85rem;
}

.bullet-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #7A2E22;
  margin-top: 0.55rem;
  flex-shrink: 0;
}

.bullet-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  color: #44403C;
  line-height: 1.6;
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
  font-size: 1.4rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.75rem;
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

/* Have Questions Card */
.contact-box-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
}

.contact-box-card h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.5rem;
}

.contact-box-card p {
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.25rem;
}

.btn-contact-mail {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  background: #FDF4F2;
  border: 1px solid #7A2E22;
  color: #7A2E22;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-contact-mail:hover {
  background: #7A2E22;
  color: #FFFFFF;
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
  height: 180px;
  object-fit: cover;
  display: block;
}

.botanical-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.92) 40%, rgba(255, 255, 255, 0.6) 100%);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.quote-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
  line-height: 1.2;
}

.quote-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #44403C;
  line-height: 1.45;
  margin: 0 0 0.5rem;
}

.quote-dash {
  width: 32px;
  height: 2px;
  background: #7A2E22;
}

/* Responsive */
@media (max-width: 1200px) {
  .policy-body-grid {
    grid-template-columns: 220px 1fr;
  }
  .policy-sidebar-col {
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
  .policy-body-grid {
    grid-template-columns: 1fr;
  }
  .policy-toc-col {
    display: none; /* Collapsible or hidden on small mobile */
  }
  .info-collect-grid {
    grid-template-columns: 1fr;
  }
}
</style>
