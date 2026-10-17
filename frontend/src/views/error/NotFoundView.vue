<template>
  <div class="lumea-not-found-page">
    <div class="not-found-container">
      <!-- Left Content Column -->
      <div class="not-found-content">
        <h1 class="error-code">404</h1>
        <h2 class="error-heading">Oops! Page Not Found</h2>
        <p class="error-description">
          The page you're looking for might have been moved, renamed, or doesn't exist.
          But don't worry — there's still more beauty to discover at Luméa.
        </p>

        <!-- Action CTAs -->
        <div class="error-actions">
          <router-link to="/" class="btn-primary-atelier">
            Go to Homepage &rarr;
          </router-link>
          <router-link to="/shop" class="btn-secondary-atelier">
            Shop Now &rarr;
          </router-link>
        </div>

        <!-- Secondary Navigation Divider -->
        <div class="you-can-also-divider">
          <span class="divider-line"></span>
          <span class="divider-label">YOU CAN ALSO</span>
          <span class="divider-line"></span>
        </div>

        <!-- 4 Quick-Action Exploration Circles -->
        <div class="quick-nav-grid">
          <router-link to="/shop" class="quick-nav-item">
            <div class="quick-nav-circle">
              <ShoppingBag :size="20" class="nav-icon" />
            </div>
            <span class="quick-nav-label">Shop Skincare</span>
          </router-link>

          <router-link to="/brands" class="quick-nav-item">
            <div class="quick-nav-circle">
              <Leaf :size="20" class="nav-icon" />
            </div>
            <span class="quick-nav-label">Explore Brands</span>
          </router-link>

          <router-link to="/articles" class="quick-nav-item">
            <div class="quick-nav-circle">
              <BookOpen :size="20" class="nav-icon" />
            </div>
            <span class="quick-nav-label">Read Articles</span>
          </router-link>

          <router-link to="/quiz" class="quick-nav-item">
            <div class="quick-nav-circle">
              <Sparkles :size="20" class="nav-icon" />
            </div>
            <span class="quick-nav-label">Take the Skin Quiz</span>
          </router-link>
        </div>
      </div>

      <!-- Right Visual Column with Arch & Floral Luméa Box -->
      <div class="not-found-visual-wrap">
        <div class="visual-inner">
          <img
            src="/images/visual-404-arch.jpg"
            alt="Still More Beauty To Discover - Luméa Atelier"
            class="visual-scene-img"
          />
          <div class="handwritten-accent">
            <span class="cursive-phrase">Still More Beauty To Discover</span>
            <div class="phrase-underline"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ShoppingBag, Leaf, BookOpen, Sparkles } from 'lucide-vue-next'
</script>

<style scoped>
.lumea-not-found-page {
  background: #F9F6F0; /* Warm bisque canvas matching mockups */
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  padding: 3rem 0;
}

.not-found-container {
  max-width: 1360px;
  width: 92%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 4rem;
  position: relative;
  z-index: 2;
}

/* Left Content Column */
.not-found-content {
  max-width: 540px;
  padding: 1rem 0;
}

.error-code {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(6.5rem, 11vw, 10rem);
  line-height: 0.9;
  font-weight: 600;
  color: #7A2E22; /* Luméa Signature Atelier Burgundy */
  margin: 0 0 1rem -0.3rem;
  letter-spacing: -2px;
}

.error-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.8rem, 3.2vw, 2.5rem);
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 1.25rem;
  line-height: 1.2;
}

.error-description {
  font-family: 'Inter', -apple-system, sans-serif;
  font-size: 1.05rem;
  color: #57534E;
  line-height: 1.65;
  margin: 0 0 2.25rem;
}

.error-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 3.5rem;
}

.btn-primary-atelier {
  background: #7A2E22;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.85rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary-atelier:hover {
  background: #5E2117;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(122, 46, 34, 0.25);
}

.btn-secondary-atelier {
  background: transparent;
  color: #7A2E22;
  border: 1.5px solid #7A2E22;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.82rem 2rem;
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary-atelier:hover {
  background: rgba(122, 46, 34, 0.06);
  transform: translateY(-1px);
}

/* Secondary Navigation Divider */
.you-can-also-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  max-width: 480px;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: rgba(87, 83, 78, 0.25);
}

.divider-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: #78716C;
}

/* 4 Quick Nav Circles Grid */
.quick-nav-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  max-width: 480px;
}

.quick-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  text-decoration: none;
  group: hover;
  transition: transform 0.2s ease;
}

.quick-nav-item:hover {
  transform: translateY(-3px);
}

.quick-nav-circle {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #F0E6DE;
  border: 1px solid rgba(122, 46, 34, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #7A2E22;
  margin-bottom: 0.75rem;
  transition: all 0.25s ease;
}

.quick-nav-item:hover .quick-nav-circle {
  background: #7A2E22;
  color: #FFFFFF;
  box-shadow: 0 4px 10px rgba(122, 46, 34, 0.2);
}

.quick-nav-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 500;
  color: #1C1917;
  line-height: 1.3;
}

/* Right Visual Column */
.not-found-visual-wrap {
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.visual-inner {
  position: relative;
  width: 100%;
  max-width: 620px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 16px 40px -10px rgba(28, 25, 23, 0.15);
}

.visual-scene-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.visual-inner:hover .visual-scene-img {
  transform: scale(1.02);
}

.handwritten-accent {
  position: absolute;
  top: 1.5rem;
  right: 1.8rem;
  text-align: right;
  pointer-events: none;
}

.cursive-phrase {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: clamp(1.4rem, 2.2vw, 1.85rem);
  color: #8C4334;
  display: block;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
}

.phrase-underline {
  width: 70px;
  height: 2px;
  background: #8C4334;
  margin-left: auto;
  margin-top: 0.35rem;
}

/* Responsive Breakpoints */
@media (max-width: 992px) {
  .not-found-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  .not-found-content {
    max-width: 100%;
    text-align: center;
  }
  .error-actions {
    justify-content: center;
  }
  .you-can-also-divider {
    margin-left: auto;
    margin-right: auto;
  }
  .quick-nav-grid {
    margin: 0 auto;
  }
  .not-found-visual-wrap {
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .quick-nav-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  .error-actions {
    flex-direction: column;
    width: 100%;
  }
  .btn-primary-atelier, .btn-secondary-atelier {
    width: 100%;
    justify-content: center;
  }
}
</style>
