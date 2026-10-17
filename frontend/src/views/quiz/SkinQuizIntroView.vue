<template>
  <div class="lumea-quiz-intro-view">
    <!-- ================================================================= -->
    <!-- 1. HERO SECTION                                                  -->
    <!-- ================================================================= -->
    <section class="quiz-hero-section">
      <div class="container hero-container">
        <div class="hero-left-col">
          <div class="hero-eyebrow">
            <span class="eyebrow-line"></span>
            <span>LUMÉA SKIN QUIZ</span>
          </div>

          <h1 class="hero-title">
            Discover Your Skin.<br>
            <span class="text-terracotta">Find What Truly Works.</span>
          </h1>

          <p class="hero-desc">
            Take a quick, personalized quiz to understand your skin and get product recommendations made just for you.
          </p>

          <!-- 4 Feature Badges -->
          <div class="hero-feature-badges">
            <div class="feature-badge-item">
              <div class="badge-icon-circle">
                <Sparkles :size="20" class="badge-icon" />
              </div>
              <span class="badge-label">Personalized Recommendations</span>
            </div>

            <div class="feature-badge-item">
              <div class="badge-icon-circle">
                <Smile :size="20" class="badge-icon" />
              </div>
              <span class="badge-label">Understand Your Skin Better</span>
            </div>

            <div class="feature-badge-item">
              <div class="badge-icon-circle">
                <FlaskConical :size="20" class="badge-icon" />
              </div>
              <span class="badge-label">Curated by Beauty Experts</span>
            </div>

            <div class="feature-badge-item">
              <div class="badge-icon-circle">
                <Clock :size="20" class="badge-icon" />
              </div>
              <span class="badge-label">Takes Only 2–3 Minutes</span>
            </div>
          </div>

          <!-- CTA Group -->
          <div class="hero-action-group">
            <router-link to="/quiz/questions" class="btn-start-quiz">
              <span>Start Skin Quiz</span>
              <ArrowRight :size="18" />
            </router-link>

            <div class="browse-sublink">
              <span>Already know your skin type?</span>
              <router-link to="/shop" class="link-browse">Browse Products Instead</router-link>
            </div>
          </div>
        </div>

        <div class="hero-right-col">
          <div class="hero-image-stage">
            <img
              src="/images/banners/banner-skin-concerns-clean.jpg"
              alt="Luméa Radiant Skin Care"
              class="hero-model-img"
            />
            <div class="hero-soft-fade"></div>
            <div class="script-overlay">
              <span class="script-text">Healthier<br>Happier<br>You. ♡</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 2. TRUST VALUE BAR                                               -->
    <!-- ================================================================= -->
    <section class="trust-bar-section">
      <div class="container trust-container">
        <div class="trust-item">
          <ShieldCheck :size="22" class="trust-icon" />
          <span class="trust-text">Trusted Beauty Marketplace</span>
        </div>
        <div class="trust-divider"></div>

        <div class="trust-item">
          <Sprout :size="22" class="trust-icon" />
          <span class="trust-text">100% Authentic Products</span>
        </div>
        <div class="trust-divider"></div>

        <div class="trust-item">
          <Truck :size="22" class="trust-icon" />
          <span class="trust-text">Fast & Reliable Delivery</span>
        </div>
        <div class="trust-divider"></div>

        <div class="trust-item">
          <Heart :size="22" class="trust-icon" />
          <span class="trust-text">Loved by Thousands</span>
        </div>
        <div class="trust-divider"></div>

        <div class="trust-item">
          <Users :size="22" class="trust-icon" />
          <span class="trust-text">Expert Care & Support</span>
        </div>
      </div>
    </section>

    <!-- ================================================================= -->
    <!-- 3. HOW IT WORKS SECTION                                          -->
    <!-- ================================================================= -->
    <section class="how-it-works-section">
      <div class="container">
        <div class="section-heading text-center">
          <h2 class="section-title">How It Works</h2>
          <p class="section-subtitle">Get your personalized recommendations in 3 simple steps.</p>
        </div>

        <div class="steps-flow-grid">
          <!-- Step 1 -->
          <div class="step-card">
            <div class="step-icon-box">
              <FileText :size="28" class="step-icon" />
            </div>
            <div class="step-content">
              <h3 class="step-title">1. Answer Questions</h3>
              <p class="step-desc">Tell us about your skin, lifestyle, and skincare goals.</p>
            </div>
          </div>

          <div class="step-arrow-divider">
            <ArrowRight :size="22" />
          </div>

          <!-- Step 2 -->
          <div class="step-card">
            <div class="step-icon-box">
              <Sparkles :size="28" class="step-icon" />
            </div>
            <div class="step-content">
              <h3 class="step-title">2. Get Your Results</h3>
              <p class="step-desc">Discover your skin type, key concerns, and personalized advice.</p>
            </div>
          </div>

          <div class="step-arrow-divider">
            <ArrowRight :size="22" />
          </div>

          <!-- Step 3 -->
          <div class="step-card">
            <div class="step-icon-box">
              <ShoppingBag :size="28" class="step-icon" />
            </div>
            <div class="step-content">
              <h3 class="step-title">3. Shop with Confidence</h3>
              <p class="step-desc">Explore curated products made for your unique skin.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import {
  ArrowRight,
  Clock,
  FileText,
  FlaskConical,
  Heart,
  ShieldCheck,
  ShoppingBag,
  Smile,
  Sparkles,
  Sprout,
  Truck,
  Users
} from 'lucide-vue-next'
</script>

<style scoped>
.lumea-quiz-intro-view {
  background-color: #FAF8F5;
  min-height: 100vh;
  color: #242721;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ================= HERO SECTION ================= */
.quiz-hero-section {
  padding: 28px 0 24px;
  background: linear-gradient(135deg, #FAF8F5 0%, #F5EFEA 100%);
  border-bottom: 1px solid #ECE4DC;
  position: relative;
  overflow: hidden;
}

.hero-container {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 36px;
  align-items: center;
}

.hero-eyebrow {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #8C7B70;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.eyebrow-line {
  width: 24px;
  height: 1.5px;
  background-color: #9E3332;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.75rem;
  line-height: 1.15;
  font-weight: 700;
  color: #111C38;
  margin-bottom: 12px;
  letter-spacing: -0.5px;
}

.text-terracotta {
  color: #8E4A3E;
  font-style: italic;
}

.hero-desc {
  font-size: 1.1rem;
  line-height: 1.55;
  color: #5C5852;
  max-width: 520px;
  margin-bottom: 20px;
}

/* 4 Feature Badges */
.hero-feature-badges {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.feature-badge-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.badge-icon-circle {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #F4ECE6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  border: 1px solid #EADBCE;
  transition: transform 0.2s ease, background 0.2s ease;
}

.feature-badge-item:hover .badge-icon-circle {
  transform: translateY(-2px);
  background: #EEDCD0;
}

.badge-label {
  font-size: 11px;
  font-weight: 600;
  color: #3C3833;
  line-height: 1.3;
}

/* Actions */
.hero-action-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
}

.btn-start-quiz {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background-color: #9E3332;
  color: #FFFFFF;
  padding: 12px 28px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(158, 51, 50, 0.25);
  transition: all 0.25s ease;
}

.btn-start-quiz:hover {
  background-color: #832726;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(158, 51, 50, 0.35);
}

.browse-sublink {
  font-size: 12px;
  color: #7A7269;
  display: flex;
  gap: 6px;
}

.link-browse {
  color: #9E3332;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.link-browse:hover {
  color: #7C2423;
}

/* Right Stage Image */
.hero-right-col {
  display: flex;
  justify-content: center;
}

.hero-image-stage {
  position: relative;
  width: 100%;
  max-width: 440px;
  height: 340px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(36, 39, 33, 0.1);
  border: 1px solid rgba(236, 228, 220, 0.85);
}

.hero-model-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
  display: block;
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 15%);
  mask-image: linear-gradient(to right, transparent 0%, black 15%);
}

.hero-soft-fade {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 60px;
  background: linear-gradient(to right, rgba(250, 248, 245, 0.35), transparent);
  pointer-events: none;
}

.script-overlay {
  position: absolute;
  top: 18px;
  right: 18px;
  transform: rotate(4deg);
  pointer-events: none;
  z-index: 2;
}

.script-text {
  font-family: 'Cormorant Garamond', 'Playfair Display', cursive, serif;
  font-size: 34px;
  font-style: italic;
  font-weight: 600;
  line-height: 1.05;
  color: #9E3332;
  text-shadow: 0 2px 12px rgba(255, 255, 255, 0.95);
}

/* ================= TRUST VALUE BAR ================= */
.trust-bar-section {
  background-color: #FFFFFF;
  border-bottom: 1px solid #EFE8E1;
  padding: 22px 0;
}

.trust-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.trust-icon {
  color: #9E3332;
  flex-shrink: 0;
}

.trust-text {
  font-size: 13.5px;
  font-weight: 600;
  color: #38342F;
}

.trust-divider {
  width: 1px;
  height: 24px;
  background-color: #EFE8E1;
}

/* ================= HOW IT WORKS ================= */
.how-it-works-section {
  padding: 80px 0;
  background-color: #FAF8F5;
}

.section-heading {
  margin-bottom: 50px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 34px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 10px;
}

.section-subtitle {
  font-size: 15px;
  color: #736C63;
}

.text-center {
  text-align: center;
}

.steps-flow-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
}

.step-card {
  flex: 1;
  max-width: 320px;
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.step-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(36, 39, 33, 0.08);
}

.step-icon-box {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #F9EFE9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  border: 1px solid #F0DFD3;
}

.step-title {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 600;
  color: #242721;
  margin-bottom: 8px;
}

.step-desc {
  font-size: 13.5px;
  line-height: 1.5;
  color: #6C665D;
}

.step-arrow-divider {
  color: #B5ABA0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Responsive */
@media (max-width: 992px) {
  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .hero-eyebrow,
  .hero-action-group,
  .feature-badge-item {
    align-items: center;
  }
  .hero-desc {
    margin-left: auto;
    margin-right: auto;
  }
  .hero-feature-badges {
    grid-template-columns: repeat(2, 1fr);
  }
  .trust-container {
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
  }
  .trust-divider {
    display: none;
  }
  .steps-flow-grid {
    flex-direction: column;
  }
  .step-arrow-divider {
    transform: rotate(90deg);
  }
}
</style>
