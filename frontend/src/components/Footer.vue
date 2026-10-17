<template>
  <footer class="lumea-beauty-footer">
    <div class="container footer-inner">
      <div class="footer-top-grid">
        <!-- Brand Column -->
        <div class="footer-brand-col">
          <div class="brand-block">
            <img src="/images/logo-lumea.png" alt="Luméa - Beauty Lives Here" class="footer-logo-img" />
          </div>

          <!-- Social Links -->
          <div class="footer-social-icons">
            <a href="https://instagram.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="Instagram">
              <Instagram :size="18" />
            </a>
            <a href="https://facebook.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="Facebook">
              <Facebook :size="18" />
            </a>
            <a href="https://youtube.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="YouTube">
              <Youtube :size="18" />
            </a>
            <a href="https://tiktok.com" target="_blank" rel="noopener" class="social-icon-btn" aria-label="TikTok">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 0 0-1-.08A6.34 6.34 0 0 0 3 15.66a6.34 6.34 0 0 0 10.86 4.43V12.1a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1.04-.04c-.66-.14-1.3-.4-1.87-.79z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Shop Column -->
        <div class="footer-nav-col">
          <h4>Shop</h4>
          <ul>
            <li><router-link to="/shop">All Products</router-link></li>
            <li><router-link to="/new-arrivals">New Arrivals</router-link></li>
            <li><router-link to="/best-sellers">Best Sellers</router-link></li>
            <li><router-link to="/deals">Deals</router-link></li>
            <li><router-link to="/quiz">Skin Diagnostic Quiz</router-link></li>
          </ul>
        </div>

        <!-- Help Column -->
        <div class="footer-nav-col">
          <h4>Help</h4>
          <ul>
            <li><router-link to="/shipping">Shipping</router-link></li>
            <li><router-link to="/returns">Return Policy</router-link></li>
            <li><router-link to="/returns/request">Request a Return</router-link></li>
            <li><router-link to="/faq">FAQ Center</router-link></li>
            <li><router-link to="/contact">Contact Us</router-link></li>
          </ul>
        </div>

        <!-- About Column -->
        <div class="footer-nav-col">
          <h4>About</h4>
          <ul>
            <li><router-link to="/about">Our Story</router-link></li>
            <li><router-link to="/authenticity">Authenticity</router-link></li>
            <li><router-link to="/sustainability">Sustainability</router-link></li>
            <li><router-link to="/articles">Journal</router-link></li>
          </ul>
        </div>

        <!-- Mission Column -->
        <div class="footer-mission-col">
          <div class="mission-leaf">
            <Leaf :size="20" class="leaf-icon" />
            <span class="mission-text">Skincare for a<br>Brighter Tomorrow.</span>
          </div>
          <div class="admin-entry-link">
            <span class="pulse-indicator"></span>
            <a href="http://localhost:5174" target="_blank" rel="noopener">Atelier Console (:5174)</a>
          </div>
        </div>
      </div>

      <!-- Footer Bottom Row -->
      <div class="footer-bottom-bar">
        <p class="copyright-text">&copy; {{ new Date().getFullYear() }} Luméa. All rights reserved.</p>
        <div class="legal-links">
          <router-link to="/privacy-policy">Privacy Policy</router-link>
          <router-link to="/terms-of-service">Terms of Service</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Facebook, Instagram, Leaf, Youtube } from 'lucide-vue-next'
</script>

<style scoped>
.lumea-beauty-footer {
  background: #F5EFEB; /* Warm sand/bisque as shown in the design */
  border-top: 1px solid rgba(28, 25, 23, 0.08);
  padding: 4.5rem 0 2rem;
  margin-top: 5rem;
}

.footer-top-grid {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1.2fr 1.2fr 1.8fr;
  gap: 3rem;
  padding-bottom: 3.5rem;
  border-bottom: 1px solid rgba(28, 25, 23, 0.1);
}

.brand-block {
  display: flex;
  margin-bottom: 1.5rem;
}

.footer-logo-img {
  height: 42px;
  width: auto;
  object-fit: contain;
  display: block;
}

.footer-social-icons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.social-icon-btn {
  color: #57534E;
  transition: color var(--transition-fast), transform var(--transition-fast);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.social-icon-btn:hover {
  color: #7A2E22;
  transform: translateY(-2px);
}

.footer-nav-col h4 {
  font-family: var(--font-sans);
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
  margin-bottom: 1.25rem;
}

.footer-nav-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-nav-col a {
  font-size: 0.82rem;
  color: #57534E;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-nav-col a:hover {
  color: #7A2E22;
}

.footer-mission-col {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mission-leaf {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.leaf-icon {
  color: #556B2F;
  flex-shrink: 0;
  margin-top: 2px;
}

.mission-text {
  font-size: 0.88rem;
  font-weight: 500;
  color: #1C1917;
  line-height: 1.4;
}

.admin-entry-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  color: #8C877F;
}

.admin-entry-link a {
  color: #8C877F;
  text-decoration: underline;
  transition: color var(--transition-fast);
}

.admin-entry-link a:hover {
  color: #8E4A3E;
}

.pulse-indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #10B981;
}

.footer-bottom-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 2rem;
  font-size: 0.78rem;
  color: #8C877F;
}

.legal-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.legal-links a {
  color: #8C877F;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.legal-links a:hover {
  color: #1C1917;
}

@media (max-width: 900px) {
  .footer-top-grid {
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
}

@media (max-width: 600px) {
  .footer-top-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom-bar {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
