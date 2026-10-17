<template>
  <div class="authenticity-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Why Shop With Us</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="auth-hero">
        <div class="hero-left">
          <span class="hero-eyebrow">WHY SHOP WITH US</span>
          <h1 class="hero-title">Your Skin Deserves<br />the Real Thing.</h1>
          <p class="hero-desc">
            We’re committed to authentic products, trusted brands, and a safer, more confident skincare journey.
          </p>
        </div>

        <div class="hero-right">
          <div class="hero-media-wrap">
            <img src="/images/banners/banner-best-sellers-clean.jpg" alt="Authentic Skincare Selection" class="hero-banner-img" />
            <div class="hero-script-overlay">
              <span class="script-row">Authentic</span>
              <span class="script-row">Skincare.</span>
              <span class="script-row">A Brighter</span>
              <span class="script-row">You. <Heart :size="18" class="script-heart-icon" /></span>
            </div>
          </div>
        </div>
      </section>

      <!-- 4 Pillars Strip with Vertical Dividers -->
      <section class="pillars-section">
        <div class="pillars-strip">
          <div class="pillar-col">
            <div class="p-pink-icon">
              <ShieldCheck :size="22" />
            </div>
            <div class="p-text">
              <h3>100% Authentic</h3>
              <p>Every product is sourced directly from authorized brand partners.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="pillar-col">
            <div class="p-pink-icon">
              <Award :size="22" />
            </div>
            <div class="p-text">
              <h3>Trusted Brands</h3>
              <p>Shop from over 100+ global and local skincare brands.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="pillar-col">
            <div class="p-pink-icon">
              <Truck :size="22" />
            </div>
            <div class="p-text">
              <h3>Careful Handling</h3>
              <p>Your products are stored and shipped with care.</p>
            </div>
          </div>

          <div class="p-divider"></div>

          <div class="pillar-col">
            <div class="p-pink-icon">
              <Leaf :size="22" />
            </div>
            <div class="p-text">
              <h3>A Safer, Kinder Choice</h3>
              <p>We promote responsible beauty for a healthier you and planet.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Authenticity You Can Trust 3-Column Showcase -->
      <section class="verification-section">
        <div class="verification-grid">
          <!-- Col 1: Narrative -->
          <div class="v-narrative-col">
            <span class="section-eyebrow">AUTHENTICITY YOU CAN TRUST</span>
            <h2 class="v-heading">Real Brands. Real Products.<br />Real Results.</h2>
            <p class="v-text">
              We work only with authorized distributors and brand partners to ensure every product you receive is genuine, safe, and high quality. From skincare essentials to expert-backed treatments, you can shop with confidence knowing it’s the real thing.
            </p>
            <router-link to="/brands" class="sourcing-link-pill">
              Learn More About Our Sourcing <span class="arrow-right">→</span>
            </router-link>
          </div>

          <!-- Col 2: Center Box Unboxing Image -->
          <div class="v-center-visual">
            <img src="/images/banner-deals.jpg" alt="Luméa Genuine Unboxing" class="v-unboxing-photo" />
          </div>

          <!-- Col 3: Criteria Items with Pink Circular Badges -->
          <div class="v-criteria-col">
            <div class="criteria-row">
              <div class="criteria-circle-icon">
                <Search :size="20" />
              </div>
              <div class="criteria-info">
                <h4>Verified Supply Chain</h4>
                <p>We partner directly with authorized distributors and official retailers.</p>
              </div>
            </div>

            <div class="criteria-row">
              <div class="criteria-circle-icon">
                <FileCheck :size="20" />
              </div>
              <div class="criteria-info">
                <h4>Quality Assurance</h4>
                <p>All products are handled, stored, and shipped according to brand standards.</p>
              </div>
            </div>

            <div class="criteria-row">
              <div class="criteria-circle-icon">
                <Heart :size="20" />
              </div>
              <div class="criteria-info">
                <h4>Transparent Information</h4>
                <p>We provide accurate product details, ingredients, and usage guidance.</p>
              </div>
            </div>

            <div class="criteria-row">
              <div class="criteria-circle-icon">
                <Leaf :size="20" />
              </div>
              <div class="criteria-info">
                <h4>Responsible Beauty</h4>
                <p>We support brands that care for people and the planet.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Brand Partners Strip -->
      <section class="brand-partners-section">
        <div class="brand-partners-strip">
          <span class="partners-label">SOME OF OUR<br />TRUSTED BRANDS</span>
          <div class="partners-divider"></div>
          <div class="partners-logos-row">
            <span class="b-logo serif-brand">SK-II</span>
            <span class="b-logo">LA ROCHE-POSAY</span>
            <span class="b-logo italic-brand">The Ordinary.</span>
            <span class="b-logo">CeraVe</span>
            <span class="b-logo serif-brand">CAUDALÍE</span>
            <span class="b-logo">BIODERMA</span>
            <span class="b-logo">Avène</span>
            <span class="b-logo">innisfree</span>
            <span class="b-logo spaced-brand">LANEIGE</span>
            <span class="b-logo serif-brand">ESTĒE LAUDER</span>
          </div>
        </div>
      </section>

      <!-- Travertine Sand Trust CTA Banner -->
      <section class="trust-cta-banner">
        <div class="trust-banner-inner">
          <div class="trust-text-block">
            <h2 class="trust-title">Beautiful Skin Starts with Trust.</h2>
            <p class="trust-sub">Shop with confidence at Luméa.</p>
          </div>
          <router-link to="/brands" class="btn-shop-brands-rect">
            Shop All Brands <span class="arrow-right">→</span>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ShieldCheck, Award, Truck, Leaf, Search, FileCheck, Heart } from 'lucide-vue-next'
</script>

<style scoped>
.authenticity-page {
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

/* Open Hero Banner matching Authenticity-Why Shop With Us.png */
.auth-hero {
  display: grid;
  grid-template-columns: 1.1fr 1.15fr;
  align-items: center;
  gap: 2.5rem;
  margin-bottom: 2.25rem;
  min-height: 275px;
  padding: 1.75rem 2.5rem;
  background: linear-gradient(135deg, #FAF7F2 0%, #F6EFE7 50%, #ECE4DB 100%);
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

.script-heart-icon {
  display: inline-block;
  vertical-align: -2px;
  margin-left: 4px;
  color: #C25E4D;
  fill: #C25E4D;
}

/* 4 Pillars Strip with Vertical Dividers */
.pillars-section {
  margin-bottom: 3.5rem;
}

.pillars-strip {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.75rem 2rem;
  justify-content: space-between;
}

.pillar-col {
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

/* 3-Column Verification Showcase */
.verification-section {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 16px;
  padding: 3rem;
  margin-bottom: 3.5rem;
}

.verification-grid {
  display: grid;
  grid-template-columns: 1fr 1.25fr 1fr;
  gap: 2.75rem;
  align-items: center;
}

.section-eyebrow {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #8E4A3E;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.45rem;
}

.v-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #192A41;
  line-height: 1.25;
  margin-bottom: 1.15rem;
}

.v-text {
  font-size: 0.94rem;
  color: #57534E;
  line-height: 1.7;
  margin-bottom: 1.75rem;
}

.sourcing-link-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #8E4A3E;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
}

.sourcing-link-pill:hover {
  text-decoration: underline;
}

.v-center-visual {
  border-radius: 12px;
  overflow: hidden;
  height: 320px;
}

.v-unboxing-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.v-criteria-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.criteria-row {
  display: flex;
  align-items: flex-start;
  gap: 1.15rem;
}

.criteria-circle-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.criteria-info h4 {
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.criteria-info p {
  font-size: 0.82rem;
  color: #78716C;
  line-height: 1.45;
  margin: 0;
}

/* Brand Partners Strip */
.brand-partners-section {
  margin-bottom: 3.5rem;
}

.brand-partners-strip {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.5rem 2rem;
}

.partners-label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #78716C;
  white-space: nowrap;
  text-transform: uppercase;
  line-height: 1.35;
}

.partners-divider {
  width: 1px;
  height: 36px;
  background: #EAE5DF;
  margin: 0 2rem;
  flex-shrink: 0;
}

.partners-logos-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  gap: 1.5rem;
  overflow-x: auto;
}

.b-logo {
  font-size: 0.92rem;
  font-weight: 700;
  color: #292524;
  opacity: 0.8;
  white-space: nowrap;
}

.serif-brand {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.15rem;
}

.italic-brand {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-style: italic;
}

.spaced-brand {
  letter-spacing: 0.15em;
}

/* Travertine Trust CTA Banner */
.trust-cta-banner {
  background: linear-gradient(135deg, #F5EFEB 0%, #EDE4DE 100%);
  border: 1px solid #EAE5DF;
  border-radius: 16px;
  padding: 2.75rem 3.5rem;
}

.trust-banner-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.trust-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.3rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.35rem;
}

.trust-sub {
  font-size: 1.05rem;
  color: #57534E;
}

.btn-shop-brands-rect {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.8rem 1.85rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: background 0.2s ease;
  white-space: nowrap;
}

.btn-shop-brands-rect:hover {
  background: #73392E;
}

/* Responsive */
@media (max-width: 1024px) {
  .auth-hero {
    grid-template-columns: 1fr;
  }
  .pillars-strip {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .p-divider {
    display: none;
  }
  .verification-grid {
    grid-template-columns: 1fr;
  }
  .brand-partners-strip {
    flex-direction: column;
    align-items: flex-start;
  }
  .partners-divider {
    display: none;
  }
  .trust-banner-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
}
</style>
