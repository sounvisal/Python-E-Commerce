<template>
  <div class="about-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">About Luméa</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="about-hero">
        <div class="hero-left">
          <span class="hero-eyebrow">ABOUT LUMÉA</span>
          <h1 class="hero-title">Beauty Lives Here.</h1>
          <p class="hero-desc">
            Luméa is a curated skincare marketplace, bringing you trusted brands, expert guidance, and a more confident you.
          </p>
          <a href="#our-story" class="btn-story-pill">
            Our Story <span class="arrow-down">↓</span>
          </a>
        </div>

        <div class="hero-right">
          <div class="hero-image-container">
            <img src="/images/banners/banner-about-clean.jpg" alt="Luméa Radiant Beauty" class="hero-portrait-img" />
            <div class="hero-script-overlay">
              <span class="script-row">Real Care.</span>
              <span class="script-row">Real People.</span>
              <span class="script-row">A Brighter</span>
              <span class="script-row">Tomorrow. <Heart :size="18" class="script-heart-icon" /></span>
            </div>
          </div>
        </div>
      </section>

      <!-- Our Philosophy Strip -->
      <section class="philosophy-strip-section">
        <div class="philosophy-strip-inner">
          <div class="philosophy-header-col">
            <span class="section-eyebrow">OUR PHILOSOPHY</span>
            <h2 class="philosophy-title">Thoughtful Skincare<br />for a Brighter Tomorrow.</h2>
          </div>

          <div class="philosophy-items-row">
            <div class="philosophy-item">
              <div class="pink-circle-icon">
                <Leaf :size="22" />
              </div>
              <div class="item-content">
                <h3>Authentic Brands</h3>
                <p>Only genuine, trusted skincare brands you can rely on.</p>
              </div>
            </div>

            <div class="strip-divider"></div>

            <div class="philosophy-item">
              <div class="pink-circle-icon">
                <Users :size="22" />
              </div>
              <div class="item-content">
                <h3>Expert Guidance</h3>
                <p>Evidence-based advice for real skin needs.</p>
              </div>
            </div>

            <div class="strip-divider"></div>

            <div class="philosophy-item">
              <div class="pink-circle-icon">
                <Heart :size="22" />
              </div>
              <div class="item-content">
                <h3>Better Choices</h3>
                <p>Helping you make choices that are kinder to your skin and the planet.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Our Story Section (3-part layout) -->
      <section id="our-story" class="story-showcase-section">
        <div class="story-showcase-grid">
          <!-- Left: Product bottles on travertine stone -->
          <div class="story-product-stage">
            <img src="/images/brand-hero-bottles.jpg" alt="Curated Skincare Brands" class="story-bottles-img" />
          </div>

          <!-- Middle: Story narrative -->
          <div class="story-narrative-col">
            <span class="section-eyebrow">OUR STORY</span>
            <h2 class="story-heading">We Bring the World’s<br />Best Skincare Brands Together.</h2>
            <p class="story-body-text">
              Luméa was created for people who believe skincare is more than a routine — it’s a form of self-care. We curate the world’s most trusted skincare brands in one place, making it easier for you to discover, compare, and shop with confidence.
            </p>
            <router-link to="/brands" class="btn-explore-pill">
              Explore Our Brands <span class="arrow-right">→</span>
            </router-link>
          </div>

          <!-- Right: Quote / Life Card -->
          <div class="story-quote-card">
            <div class="quote-inner">
              <h3 class="quote-title">Skincare<br />for Real Life.</h3>
              <div class="quote-dash"></div>
              <p class="quote-lines">
                Trusted brands.<br />
                Real results.<br />
                A brighter you.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- What Makes Luméa Different Strip (4 items with dividers) -->
      <section class="differentiators-section">
        <span class="section-eyebrow diff-eyebrow">WHAT MAKES LUMÉA DIFFERENT</span>
        <div class="differentiators-strip">
          <div class="diff-col">
            <div class="diff-pink-icon">
              <ShieldCheck :size="22" />
            </div>
            <div class="diff-text">
              <h4>100% Authentic</h4>
              <p>Genuine products from authorized brands.</p>
            </div>
          </div>

          <div class="diff-divider"></div>

          <div class="diff-col">
            <div class="diff-pink-icon">
              <ShoppingBag :size="22" />
            </div>
            <div class="diff-text">
              <h4>100+ Brands</h4>
              <p>Global and local favorites in one place.</p>
            </div>
          </div>

          <div class="diff-divider"></div>

          <div class="diff-col">
            <div class="diff-pink-icon">
              <User :size="22" />
            </div>
            <div class="diff-text">
              <h4>Personalized Guidance</h4>
              <p>Find what works for your unique skin.</p>
            </div>
          </div>

          <div class="diff-divider"></div>

          <div class="diff-col">
            <div class="diff-pink-icon">
              <Truck :size="22" />
            </div>
            <div class="diff-text">
              <h4>Easy Shopping</h4>
              <p>A seamless, secure, and reliable experience.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Find Your Beauty Routine Travertine Banner -->
      <section class="beauty-routine-banner">
        <div class="routine-banner-content">
          <div class="routine-left">
            <h2 class="routine-heading">Find Your Beauty Routine.</h2>
            <p class="routine-desc">Skincare that fits your life, and your goals.</p>
            <router-link to="/skin-quiz" class="btn-routine-quiz">
              Take the Skin Quiz <span class="arrow-right">→</span>
            </router-link>
          </div>

          <div class="routine-right">
            <img src="/images/cat-kits.jpg" alt="Skincare routine products on stone" class="routine-products-img" />
            <div class="routine-callout">
              <span class="routine-callout-text">A Healthier<br />You, Day by Day.</span>
              <div class="callout-line"></div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { Leaf, Users, Heart, ShieldCheck, ShoppingBag, User, Truck } from 'lucide-vue-next'
</script>

<style scoped>
.about-page {
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

/* Hero Section: Warm travertine banner matching format */
.about-hero {
  display: grid;
  grid-template-columns: 1.15fr 1.1fr;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2.25rem;
  padding: 1.75rem 2.5rem;
  min-height: 275px;
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
  align-items: flex-start;
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
  font-size: 1.1rem;
  line-height: 1.55;
  color: #44403C;
  font-weight: 400;
  margin-bottom: 1.35rem;
  max-width: 520px;
}

.btn-story-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.6rem 1.45rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.88rem;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.2);
}

.btn-story-pill:hover {
  background: #73392E;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(142, 74, 62, 0.3);
}

.hero-right {
  position: relative;
}

.hero-image-container {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.hero-portrait-img {
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
  top: 1.75rem;
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
  font-size: 1.85rem;
  line-height: 1.18;
  color: #C25E4D;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.9);
}

.script-heart-icon {
  display: inline-block;
  vertical-align: -2px;
  margin-left: 4px;
  color: #C25E4D;
  fill: #C25E4D;
}

/* Philosophy Strip: Single white card with vertical dividers */
.philosophy-strip-section {
  margin-bottom: 3.5rem;
}

.philosophy-strip-inner {
  display: grid;
  grid-template-columns: 1.15fr 2.3fr;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2.25rem 2.5rem;
  gap: 2.5rem;
}

.section-eyebrow {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #8E4A3E;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.4rem;
}

.philosophy-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.85rem;
  font-weight: 700;
  color: #192A41;
  line-height: 1.25;
}

.philosophy-items-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.philosophy-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.pink-circle-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.item-content h3 {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.25rem;
}

.item-content p {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.45;
  margin: 0;
}

.strip-divider {
  width: 1px;
  height: 60px;
  background: #EAE5DF;
  flex-shrink: 0;
}

/* Our Story Showcase: 3 parts (Borderless Open Layout) */
.story-showcase-section {
  padding: 1.5rem 0;
  margin-bottom: 3.5rem;
}

.story-showcase-grid {
  display: grid;
  grid-template-columns: 1fr 1.35fr 0.75fr;
  gap: 2.5rem;
  align-items: center;
}

.story-product-stage {
  border-radius: 12px;
  overflow: hidden;
  height: 310px;
}

.story-bottles-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.story-product-stage:hover .story-bottles-img {
  transform: scale(1.03);
}

.story-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #192A41;
  line-height: 1.25;
  margin: 0.4rem 0 1.15rem;
}

.story-body-text {
  font-size: 0.95rem;
  color: #57534E;
  line-height: 1.7;
  margin-bottom: 1.75rem;
}

.btn-explore-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.75rem 1.65rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  transition: all 0.25s ease;
}

.btn-explore-pill:hover {
  background: #73392E;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.25);
}

.story-quote-card {
  border-left: 1px solid #EAE5DF;
  padding-left: 2.25rem;
  height: 100%;
  display: flex;
  align-items: center;
}

.quote-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.55rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.3;
}

.quote-dash {
  width: 36px;
  height: 2px;
  background: #8E4A3E;
  margin: 1.2rem 0;
}

.quote-lines {
  font-size: 0.92rem;
  color: #57534E;
  line-height: 1.65;
  margin: 0;
}

/* Differentiators: 4 items separated by vertical lines */
.differentiators-section {
  margin-bottom: 3.5rem;
}

.diff-eyebrow {
  margin-bottom: 0.75rem;
}

.differentiators-strip {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 1.75rem 2rem;
  justify-content: space-between;
}

.diff-col {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex: 1;
}

.diff-pink-icon {
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

.diff-text h4 {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.diff-text p {
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.4;
  margin: 0;
}

.diff-divider {
  width: 1px;
  height: 48px;
  background: #EAE5DF;
  margin: 0 1.5rem;
  flex-shrink: 0;
}

/* Routine Banner: Travertine background */
.beauty-routine-banner {
  background: linear-gradient(135deg, #F5EFEB 0%, #EDE4DE 100%);
  border-radius: 16px;
  border: 1px solid #EAE5DF;
  padding: 3rem 3.5rem;
  overflow: hidden;
}

.routine-banner-content {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  align-items: center;
  gap: 3rem;
}

.routine-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2.6rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.65rem;
}

.routine-desc {
  font-size: 1.05rem;
  color: #57534E;
  margin-bottom: 1.75rem;
}

.btn-routine-quiz {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.8rem 1.85rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.25);
}

.btn-routine-quiz:hover {
  background: #73392E;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(142, 74, 62, 0.32);
}

.routine-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.routine-products-img {
  width: 270px;
  height: 180px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(28, 25, 23, 0.1);
}

.routine-callout {
  margin-left: 1.75rem;
}

.routine-callout-text {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.25rem;
  color: #192A41;
  font-weight: 600;
  line-height: 1.35;
}

.callout-line {
  width: 36px;
  height: 2px;
  background: #8E4A3E;
  margin-top: 0.75rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .about-hero {
    grid-template-columns: 1fr;
  }
  .philosophy-strip-inner {
    grid-template-columns: 1fr;
  }
  .story-showcase-grid {
    grid-template-columns: 1fr;
  }
  .differentiators-strip {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .diff-divider {
    display: none;
  }
  .routine-banner-content {
    grid-template-columns: 1fr;
  }
}
</style>
