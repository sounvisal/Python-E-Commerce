<template>
  <div class="contact-page">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb-nav" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="bc-sep">›</span>
        <span class="bc-current">Contact Us</span>
      </nav>

      <!-- Full-Bleed Open Hero Section -->
      <section class="contact-hero">
        <div class="hero-left">
          <span class="hero-eyebrow">CONTACT US</span>
          <h1 class="hero-title">We’re Here for You.</h1>
          <p class="hero-desc">
            Have a question, need help, or just want to say hello? Our team is always happy to help.
          </p>
        </div>

        <div class="hero-right">
          <div class="hero-media-wrap">
            <img src="/images/banner-my-account.jpg" alt="Luméa Vanity and Care" class="hero-banner-img" />
            <div class="hero-script-overlay">
              <span class="script-row">Real People.</span>
              <span class="script-row">Real Care.</span>
              <span class="script-row">A Brighter</span>
              <span class="script-row">Tomorrow. <span class="heart-symbol">♡</span></span>
            </div>
          </div>
        </div>
      </section>

      <!-- 3-Column Content Layout -->
      <section class="contact-columns-section">
        <div class="contact-three-columns">
          <!-- Col 1: Get in Touch -->
          <div class="contact-white-card info-col">
            <span class="col-eyebrow">GET IN TOUCH</span>
            <h2 class="col-heading">Let’s Connect.</h2>
            <p class="col-subtext">Choose the way that works best for you.</p>

            <div class="channel-items-list">
              <div class="channel-row">
                <div class="channel-pink-circle">
                  <MessageSquare :size="20" />
                </div>
                <div class="channel-info">
                  <h4>Live Chat</h4>
                  <p class="channel-time">Available 9AM – 9PM (ICT)</p>
                  <p class="channel-hint">Chat with our team in real time.</p>
                </div>
              </div>

              <div class="channel-row">
                <div class="channel-pink-circle">
                  <Mail :size="20" />
                </div>
                <div class="channel-info">
                  <h4>Email Us</h4>
                  <a href="mailto:support@lumea.com" class="channel-mail-link">support@lumea.com</a>
                  <p class="channel-hint">We usually respond within 24 hours.</p>
                </div>
              </div>

              <div class="channel-row">
                <div class="channel-pink-circle">
                  <Phone :size="20" />
                </div>
                <div class="channel-info">
                  <h4>Call Us</h4>
                  <a href="tel:+85523900123" class="channel-phone-link">+855 23 900 123</a>
                  <p class="channel-hint">Mon – Fri, 9AM – 6PM (ICT)</p>
                </div>
              </div>

              <div class="channel-row">
                <div class="channel-pink-circle">
                  <MapPin :size="20" />
                </div>
                <div class="channel-info">
                  <h4>Visit Us</h4>
                  <p class="channel-time">Phnom Penh, Cambodia</p>
                  <p class="channel-hint">(By appointment only)</p>
                </div>
              </div>
            </div>

            <div class="col-footer-script">
              <div class="script-dash"></div>
              <span class="kinder-cursive">A Kinder,<br />More Confident Tomorrow.</span>
            </div>
          </div>

          <!-- Col 2: Send Us a Message Form -->
          <div class="contact-white-card form-col">
            <span class="col-eyebrow">SEND US A MESSAGE</span>
            <h2 class="col-heading">Message Our Team.</h2>
            <p class="col-subtext">Fill out the form below and we’ll get back to you as soon as possible.</p>

            <form @submit.prevent="handleSubmitMessage" class="contact-message-form">
              <div class="form-twin-row">
                <div class="form-field">
                  <label>First Name <span class="required-star">*</span></label>
                  <input v-model="form.firstName" type="text" placeholder="" required />
                </div>
                <div class="form-field">
                  <label>Last Name <span class="required-star">*</span></label>
                  <input v-model="form.lastName" type="text" placeholder="" required />
                </div>
              </div>

              <div class="form-field">
                <label>Email Address <span class="required-star">*</span></label>
                <input v-model="form.email" type="email" placeholder="" required />
              </div>

              <div class="form-field">
                <label>Subject <span class="required-star">*</span></label>
                <div class="select-wrapper">
                  <select v-model="form.subject" required>
                    <option value="" disabled selected></option>
                    <option value="order">Order Status & Shipping</option>
                    <option value="return">Returns & Refunds</option>
                    <option value="product">Product Advice & Routine</option>
                    <option value="account">Account & Payments</option>
                    <option value="other">General Question</option>
                  </select>
                  <ChevronDown :size="16" class="select-caret" />
                </div>
              </div>

              <div class="form-field">
                <div class="label-counter-row">
                  <label>Your Message <span class="required-star">*</span></label>
                  <span class="count-text">{{ form.message.length }}/500</span>
                </div>
                <textarea
                  v-model="form.message"
                  maxlength="500"
                  rows="6"
                  placeholder=""
                  required
                ></textarea>
              </div>

              <div class="checkbox-container">
                <label class="checkbox-inner">
                  <input v-model="form.consent" type="checkbox" required />
                  <span class="consent-msg">
                    I agree to the processing of my personal data in accordance with Luméa’s
                    <a href="#" class="policy-anchor">Privacy Policy</a>.
                  </span>
                </label>
              </div>

              <button type="submit" class="btn-send-rectangular" :disabled="submitted">
                <span v-if="!submitted">Send Message <span class="arrow-right">→</span></span>
                <span v-else>Message Sent Successfully! ✓</span>
              </button>
            </form>
          </div>

          <!-- Col 3: Common Topics / Quick Help -->
          <div class="contact-white-card topics-col">
            <span class="col-eyebrow">COMMON TOPICS</span>
            <h2 class="col-heading">Need Quick Help?</h2>
            <p class="col-subtext">Find answers to common questions.</p>

            <div class="topics-items-list">
              <router-link to="/shipping" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <Truck :size="18" />
                  </div>
                  <span>Orders & Shipping</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>

              <router-link to="/returns" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <Package :size="18" />
                  </div>
                  <span>Returns & Refunds</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>

              <router-link to="/shop" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <Sparkles :size="18" />
                  </div>
                  <span>Products & Brands</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>

              <router-link to="/faq" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <User :size="18" />
                  </div>
                  <span>Account & Payments</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>

              <router-link to="/skin-quiz" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <Leaf :size="18" />
                  </div>
                  <span>Skin Quiz & Recommendations</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>

              <router-link to="/deals" class="topic-box-link">
                <div class="topic-meta-left">
                  <div class="topic-pink-box">
                    <Gift :size="18" />
                  </div>
                  <span>Promotions & Rewards</span>
                </div>
                <ChevronRight :size="16" class="topic-chevron" />
              </router-link>
            </div>

            <!-- Soft Peach Card with flower photo -->
            <div class="conversations-banner-card">
              <h3 class="conv-heading">Beautiful<br />Conversations<br />Start Here.</h3>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import {
  MessageSquare,
  Mail,
  Phone,
  MapPin,
  Truck,
  Package,
  Sparkles,
  User,
  Leaf,
  Gift,
  ChevronRight,
  ChevronDown
} from 'lucide-vue-next'

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  subject: '',
  message: '',
  consent: false
})

const submitted = ref(false)

function handleSubmitMessage() {
  submitted.value = true
  setTimeout(() => {
    form.firstName = ''
    form.lastName = ''
    form.email = ''
    form.subject = ''
    form.message = ''
    form.consent = false
    submitted.value = false
  }, 3500)
}
</script>

<style scoped>
.contact-page {
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

/* Open Hero Banner matching Contact Us.png */
.contact-hero {
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

.heart-symbol {
  font-style: normal;
  font-size: 1.4rem;
}

/* 3-Column Section */
.contact-columns-section {
  margin-bottom: 2rem;
}

.contact-three-columns {
  display: grid;
  grid-template-columns: 1fr 1.35fr 1fr;
  gap: 1.75rem;
  align-items: start;
}

.contact-white-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2.25rem 2rem;
}

.col-eyebrow {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #8E4A3E;
  text-transform: uppercase;
  display: block;
  margin-bottom: 0.45rem;
}

.col-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.95rem;
  font-weight: 700;
  color: #192A41;
  margin-bottom: 0.4rem;
}

.col-subtext {
  font-size: 0.88rem;
  color: #78716C;
  line-height: 1.5;
  margin-bottom: 2rem;
}

/* Col 1: Channels */
.channel-items-list {
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}

.channel-row {
  display: flex;
  align-items: flex-start;
  gap: 1.15rem;
}

.channel-pink-circle {
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

.channel-info h4 {
  font-size: 0.96rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.channel-time {
  font-size: 0.85rem;
  color: #44403C;
  font-weight: 500;
  margin-bottom: 0.15rem;
}

.channel-hint {
  font-size: 0.82rem;
  color: #78716C;
  margin: 0;
}

.channel-mail-link,
.channel-phone-link {
  font-size: 0.92rem;
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
  display: block;
  margin-bottom: 0.15rem;
}

.channel-mail-link:hover,
.channel-phone-link:hover {
  text-decoration: underline;
}

.col-footer-script {
  margin-top: 2.75rem;
}

.script-dash {
  width: 36px;
  height: 2px;
  background: #C4623C;
  margin-bottom: 1rem;
}

.kinder-cursive {
  font-family: var(--font-script, 'Cormorant Garamond', Georgia, serif);
  font-style: italic;
  font-size: 1.65rem;
  line-height: 1.25;
  color: #C25E4D;
  display: block;
}

/* Col 2: Message Form */
.contact-message-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-twin-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-field label {
  font-size: 0.84rem;
  font-weight: 600;
  color: #292524;
}

.required-star {
  color: #C25E4D;
}

.label-counter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.count-text {
  font-size: 0.78rem;
  color: #A8A29E;
}

.form-field input,
.form-field select,
.form-field textarea {
  width: 100%;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.92rem;
  font-family: inherit;
  color: #1C1917;
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-field input:focus,
.form-field select:focus,
.form-field textarea:focus {
  border-color: #8E4A3E;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  appearance: none;
  cursor: pointer;
}

.select-caret {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #78716C;
  pointer-events: none;
}

.checkbox-container {
  margin-top: 0.25rem;
}

.checkbox-inner {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  font-size: 0.82rem;
  color: #57534E;
  line-height: 1.45;
  cursor: pointer;
}

.checkbox-inner input {
  margin-top: 0.15rem;
  accent-color: #8E4A3E;
}

.policy-anchor {
  color: #8E4A3E;
  text-decoration: underline;
}

/* Red Rectangular Button (Matching Contact Us.png: border-radius: 6px) */
.btn-send-rectangular {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  background: #8E4A3E;
  color: #FFFFFF;
  padding: 0.85rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.btn-send-rectangular:hover:not(:disabled) {
  background: #73392E;
  transform: translateY(-1px);
}

.btn-send-rectangular:disabled {
  background: #4A6B4A;
  cursor: default;
}

/* Col 3: Common Topics */
.topics-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 2rem;
}

.topic-box-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0.9rem;
  background: #FAF7F4;
  border-radius: 8px;
  text-decoration: none;
  color: #292524;
  font-size: 0.88rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.topic-box-link:hover {
  background: #F4EFEB;
  transform: translateX(3px);
}

.topic-meta-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.topic-pink-box {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #FDF2EE;
  color: #C4623C;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.topic-chevron {
  color: #A8A29E;
}

.conversations-banner-card {
  background: linear-gradient(135deg, #FBF4F0 0%, #F5EAE4 100%);
  border: 1px solid rgba(196, 98, 60, 0.25);
  border-radius: 12px;
  padding: 2.25rem 1.75rem;
  position: relative;
  overflow: hidden;
}

.conv-heading {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 1.55rem;
  font-weight: 700;
  color: #192A41;
  line-height: 1.3;
  margin: 0;
}

/* Responsive */
@media (max-width: 1024px) {
  .contact-hero {
    grid-template-columns: 1fr;
  }
  .contact-three-columns {
    grid-template-columns: 1fr;
  }
}
</style>
