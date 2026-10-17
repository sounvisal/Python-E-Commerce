<template>
  <div class="auth-page-view">
    <div class="container auth-container">
      <div class="auth-grid-wrapper">
        <!-- ========================================================= -->
        <!-- LEFT: EDITORIAL BRANDING & LUXURY STILL LIFE             -->
        <!-- ========================================================= -->
        <div class="auth-editorial-col">
          <div class="editorial-content-box">
            <!-- Brand Mark -->
            <div class="auth-brand-badge">
              <span class="brand-name-text">Luméa</span>
              <span class="brand-tagline-text">BEAUTY LIVES HERE</span>
            </div>

            <!-- Main Headline matching format/Login-Register.png -->
            <h1 class="auth-hero-title">
              More Beauty<br />
              for a Brighter<br />
              <span class="serif-italic-accent">You.</span>
            </h1>

            <div class="title-accent-divider"></div>

            <p class="auth-hero-desc">
              Sign in to your account to enjoy a personalized shopping experience, save your favorites, and get exclusive offers.
            </p>

            <!-- 4 Trust Badges matching mockup -->
            <div class="auth-perks-list">
              <div class="perk-item">
                <div class="perk-icon-circle">
                  <Heart :size="16" class="perk-icon" />
                </div>
                <div class="perk-text-wrap">
                  <strong class="perk-title">Save Your Favorites</strong>
                </div>
              </div>

              <div class="perk-item">
                <div class="perk-icon-circle">
                  <Package :size="16" class="perk-icon" />
                </div>
                <div class="perk-text-wrap">
                  <strong class="perk-title">Track Your Orders</strong>
                </div>
              </div>

              <div class="perk-item">
                <div class="perk-icon-circle">
                  <Tag :size="16" class="perk-icon" />
                </div>
                <div class="perk-text-wrap">
                  <strong class="perk-title">Exclusive Member Offers</strong>
                </div>
              </div>

              <div class="perk-item">
                <div class="perk-icon-circle">
                  <User :size="16" class="perk-icon" />
                </div>
                <div class="perk-text-wrap">
                  <strong class="perk-title">Personalized Recommendations</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- Editorial Photography Stage -->
          <div class="auth-photography-stage">
            <img
              src="/images/auth-editorial-bottles.jpg"
              alt="Luméa Luxury Skincare Collection"
              class="auth-editorial-img"
            />
          </div>
        </div>

        <!-- ========================================================= -->
        <!-- RIGHT: AUTHENTICATION CARD                                -->
        <!-- ========================================================= -->
        <div class="auth-card-col">
          <div class="auth-form-card">
            <!-- Tabs: Log In | Create an Account -->
            <div class="auth-tab-switch" role="tablist">
              <button
                type="button"
                role="tab"
                class="tab-btn"
                :class="{ active: currentTab === 'login' }"
                @click="currentTab = 'login'"
              >
                <span>Log In</span>
              </button>
              <button
                type="button"
                role="tab"
                class="tab-btn"
                :class="{ active: currentTab === 'register' }"
                @click="currentTab = 'register'"
              >
                <span>Create an Account</span>
              </button>
            </div>

            <!-- TAB 1: LOG IN FORM -->
            <div v-if="currentTab === 'login'" class="tab-pane-content">
              <div class="form-heading-group">
                <h2 class="form-title">Welcome Back</h2>
                <p class="form-subtitle">Sign in to continue your beauty journey.</p>
              </div>

              <form @submit.prevent="handleLogin" class="auth-form">
                <!-- Email or Phone -->
                <div class="form-field">
                  <label class="field-label" for="login-email">Email or Phone Number</label>
                  <div class="input-with-icon">
                    <User :size="17" class="field-prefix-icon" />
                    <input
                      id="login-email"
                      type="text"
                      v-model="loginForm.email"
                      placeholder="Enter your email or phone number"
                      class="auth-input"
                      required
                    />
                  </div>
                </div>

                <!-- Password -->
                <div class="form-field">
                  <div class="label-row-with-link">
                    <label class="field-label" for="login-password">Password</label>
                    <a href="#" class="forgot-pwd-link" @click.prevent="openForgotModal">
                      Forgot password?
                    </a>
                  </div>
                  <div class="input-with-icon">
                    <Lock :size="17" class="field-prefix-icon" />
                    <input
                      id="login-password"
                      :type="showPassword ? 'text' : 'password'"
                      v-model="loginForm.password"
                      placeholder="Enter your password"
                      class="auth-input"
                      required
                    />
                    <button
                      type="button"
                      class="pwd-toggle-btn"
                      @click="showPassword = !showPassword"
                      aria-label="Toggle password visibility"
                    >
                      <EyeOff v-if="showPassword" :size="17" />
                      <Eye v-else :size="17" />
                    </button>
                  </div>
                </div>

                <!-- Remember Me Checkbox -->
                <div class="form-options-row">
                  <label class="custom-check-label">
                    <input
                      type="checkbox"
                      v-model="loginForm.rememberMe"
                      class="custom-checkbox"
                    />
                    <span class="check-text">Keep me signed in</span>
                    <Info :size="14" class="info-bubble-icon" title="Save your session on this device" />
                  </label>
                </div>

                <!-- Primary Submit CTA -->
                <button type="submit" class="btn-auth-primary" :disabled="isSubmitting">
                  <span v-if="!isSubmitting">Log In</span>
                  <span v-else>Signing in...</span>
                </button>

                <!-- 1-Click Instant Demo Login Helper -->
                <button
                  type="button"
                  class="btn-demo-quick-login"
                  @click="fillDemoAccount"
                >
                  <Sparkles :size="14" />
                  <span>1-Click Demo Login (Sreynich Chan)</span>
                </button>
              </form>

              <!-- Social Login Options -->
              <div class="auth-divider">
                <span class="divider-text">or continue with</span>
              </div>

              <div class="social-login-grid">
                <button
                  type="button"
                  class="social-btn google-btn"
                  @click="handleSocialLogin('Google')"
                >
                  <svg class="social-svg-icon" viewBox="0 0 24 24" width="18" height="18">
                    <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"/>
                    <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/>
                    <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
                    <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
                  </svg>
                  <span>Continue with Google</span>
                </button>

                <button
                  type="button"
                  class="social-btn facebook-btn"
                  @click="handleSocialLogin('Facebook')"
                >
                  <svg class="social-svg-icon" viewBox="0 0 24 24" width="18" height="18" fill="#1877F2">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                  <span>Continue with Facebook</span>
                </button>

                <button
                  type="button"
                  class="social-btn apple-btn"
                  @click="handleSocialLogin('Apple')"
                >
                  <svg class="social-svg-icon" viewBox="0 0 24 24" width="18" height="18" fill="#000000">
                    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.62-.75 1.04-1.8 0.93-2.85-.9.04-1.99.6-2.64 1.36-.58.67-1.09 1.74-.95 2.78 1.01.08 2.03-.54 2.66-1.29z"/>
                  </svg>
                  <span>Continue with Apple</span>
                </button>
              </div>

              <!-- Switch to Register Link -->
              <div class="auth-switch-footer">
                <span>Don't have an account? </span>
                <button type="button" class="switch-link-btn" @click="currentTab = 'register'">
                  Create an account
                </button>
              </div>
            </div>

            <!-- TAB 2: CREATE AN ACCOUNT FORM -->
            <div v-else class="tab-pane-content">
              <div class="form-heading-group">
                <h2 class="form-title">Create an Account</h2>
                <p class="form-subtitle">Join Luméa to unlock personalized beauty routines & member perks.</p>
              </div>

              <form @submit.prevent="handleRegister" class="auth-form">
                <!-- Full Name -->
                <div class="form-field">
                  <label class="field-label" for="reg-name">Full Name</label>
                  <div class="input-with-icon">
                    <User :size="17" class="field-prefix-icon" />
                    <input
                      id="reg-name"
                      type="text"
                      v-model="registerForm.name"
                      placeholder="e.g. Sreynich Chan"
                      class="auth-input"
                      required
                    />
                  </div>
                </div>

                <!-- Email -->
                <div class="form-field">
                  <label class="field-label" for="reg-email">Email Address</label>
                  <div class="input-with-icon">
                    <Mail :size="17" class="field-prefix-icon" />
                    <input
                      id="reg-email"
                      type="email"
                      v-model="registerForm.email"
                      placeholder="Enter your email address"
                      class="auth-input"
                      required
                    />
                  </div>
                </div>

                <!-- Phone Number -->
                <div class="form-field">
                  <label class="field-label" for="reg-phone">Phone Number</label>
                  <div class="input-with-icon">
                    <Phone :size="17" class="field-prefix-icon" />
                    <input
                      id="reg-phone"
                      type="tel"
                      v-model="registerForm.phone"
                      placeholder="+855 12 345 678"
                      class="auth-input"
                      required
                    />
                  </div>
                </div>

                <!-- Password -->
                <div class="form-field">
                  <label class="field-label" for="reg-password">Password</label>
                  <div class="input-with-icon">
                    <Lock :size="17" class="field-prefix-icon" />
                    <input
                      id="reg-password"
                      :type="showPassword ? 'text' : 'password'"
                      v-model="registerForm.password"
                      placeholder="At least 8 characters"
                      class="auth-input"
                      minlength="8"
                      required
                    />
                    <button
                      type="button"
                      class="pwd-toggle-btn"
                      @click="showPassword = !showPassword"
                    >
                      <EyeOff v-if="showPassword" :size="17" />
                      <Eye v-else :size="17" />
                    </button>
                  </div>
                </div>

                <!-- Newsletter Checkbox -->
                <div class="form-options-row">
                  <label class="custom-check-label">
                    <input
                      type="checkbox"
                      v-model="registerForm.newsletter"
                      class="custom-checkbox"
                    />
                    <span class="check-text">Sign up for exclusive beauty tips, launches & member discounts</span>
                  </label>
                </div>

                <!-- Terms Checkbox -->
                <div class="form-options-row">
                  <label class="custom-check-label">
                    <input
                      type="checkbox"
                      v-model="registerForm.agreeTerms"
                      class="custom-checkbox"
                      required
                    />
                    <span class="check-text">I agree to Luméa's <router-link to="/terms-of-service" target="_blank" class="inline-text-link">Terms of Service</router-link> & <router-link to="/privacy-policy" target="_blank" class="inline-text-link">Privacy Policy</router-link></span>
                  </label>
                </div>

                <!-- Primary Register Submit -->
                <button type="submit" class="btn-auth-primary" :disabled="isSubmitting">
                  <span v-if="!isSubmitting">Create Account</span>
                  <span v-else>Creating Account...</span>
                </button>
              </form>

              <!-- Switch to Login Link -->
              <div class="auth-switch-footer">
                <span>Already have an account? </span>
                <button type="button" class="switch-link-btn" @click="currentTab = 'login'">
                  Log In
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'
import {
  Heart,
  Package,
  Tag,
  User,
  Lock,
  Mail,
  Phone,
  Eye,
  EyeOff,
  Info,
  Sparkles
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

// If navigated via /register query or prop, default to register tab
const currentTab = ref(route.path === '/register' ? 'register' : 'login')
const showPassword = ref(false)
const isSubmitting = ref(false)

const loginForm = ref({
  email: 'sreynich.chan@example.com',
  password: '••••••••••••',
  rememberMe: true
})

const registerForm = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  newsletter: true,
  agreeTerms: true
})

function fillDemoAccount() {
  loginForm.value.email = 'sreynich.chan@example.com'
  loginForm.value.password = 'password123'
  handleLogin()
}

function handleLogin() {
  isSubmitting.value = true
  setTimeout(() => {
    authStore.login({
      email: loginForm.value.email,
      password: loginForm.value.password,
      remember: loginForm.value.rememberMe
    })
    isSubmitting.value = false
    router.push('/account')
  }, 400)
}

function handleRegister() {
  isSubmitting.value = true
  setTimeout(() => {
    authStore.register({
      name: registerForm.value.name,
      email: registerForm.value.email,
      phone: registerForm.value.phone,
      password: registerForm.value.password
    })
    isSubmitting.value = false
    router.push('/account')
  }, 400)
}

function handleSocialLogin(provider) {
  notificationStore.addToast(`Connected with ${provider}. Welcome back, Sreynich!`, 'success')
  authStore.login({ email: 'sreynich.chan@example.com' })
  router.push('/account')
}

function openForgotModal() {
  notificationStore.addToast('Password reset link sent to your email address.', 'info')
}
</script>

<style scoped>
/* ==========================================================================
   AUTH PAGE VIEW (Strictly matching format/Login-Register.png)
   ========================================================================== */

.auth-page-view {
  background-color: #FAF8F5;
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  padding: 3.5rem 0 5rem;
}

.auth-container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.auth-grid-wrapper {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 3.5rem;
  align-items: center;
}

/* ================= LEFT EDITORIAL COLUMN ================= */
.auth-editorial-col {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.editorial-content-box {
  display: flex;
  flex-direction: column;
}

.auth-brand-badge {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.brand-name-text {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 2.2rem;
  font-weight: 700;
  color: #8E4A3E;
  letter-spacing: -0.02em;
  line-height: 1;
}

.brand-tagline-text {
  font-family: var(--font-sans, 'Plus Jakarta Sans', sans-serif);
  font-size: 0.65rem;
  font-weight: 700;
  color: #8E4A3E;
  letter-spacing: 0.22em;
  margin-top: 3px;
}

.auth-hero-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: clamp(2.4rem, 3.8vw, 3.4rem);
  font-weight: 600;
  color: #1C1917;
  line-height: 1.14;
  letter-spacing: -0.02em;
  margin-bottom: 1.25rem;
}

.serif-italic-accent {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
  font-weight: 600;
  color: #8E4A3E;
}

.title-accent-divider {
  width: 36px;
  height: 2px;
  background-color: #1C1917;
  margin-bottom: 1.25rem;
}

.auth-hero-desc {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #57534E;
  margin-bottom: 2rem;
}

/* Perks List */
.auth-perks-list {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.perk-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.perk-icon-circle {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #FFF5F2;
  border: 1px solid #F6D7D0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.perk-icon {
  color: #8E4A3E;
}

.perk-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
}

/* Photography Stage */
.auth-photography-stage {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 12px 36px rgba(28, 25, 23, 0.08);
  height: 480px;
  background: #F2ECE6;
}

.auth-editorial-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.auth-photography-stage:hover .auth-editorial-img {
  transform: scale(1.03);
}

/* ================= RIGHT AUTH CARD ================= */
.auth-card-col {
  display: flex;
  justify-content: center;
}

.auth-form-card {
  background: #FFFFFF;
  border-radius: 20px;
  border: 1px solid #EFE6DD;
  box-shadow: 0 8px 32px rgba(28, 25, 23, 0.05);
  padding: 2.75rem 2.5rem;
  width: 100%;
  max-width: 500px;
}

/* Tab Switcher */
.auth-tab-switch {
  display: flex;
  border-bottom: 2px solid #F0EAE3;
  margin-bottom: 2rem;
}

.tab-btn {
  flex: 1;
  padding: 0.85rem 1rem;
  background: transparent;
  border: none;
  font-size: 1.05rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  position: relative;
  transition: color 0.2s ease;
  text-align: center;
}

.tab-btn.active {
  color: #8E4A3E;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2.5px;
  background-color: #8E4A3E;
  border-radius: 2px 2px 0 0;
}

/* Form Headings */
.form-heading-group {
  text-align: center;
  margin-bottom: 1.75rem;
}

.form-title {
  font-family: var(--font-serif, 'Playfair Display', serif);
  font-size: 1.9rem;
  font-weight: 600;
  color: #1C1917;
  letter-spacing: -0.01em;
  margin-bottom: 0.35rem;
}

.form-subtitle {
  font-size: 0.88rem;
  color: #78716C;
}

/* Form Styles */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.field-label {
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
}

.label-row-with-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-pwd-link {
  font-size: 0.82rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
  transition: color 0.15s ease;
}

.forgot-pwd-link:hover {
  text-decoration: underline;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.field-prefix-icon {
  position: absolute;
  left: 14px;
  color: #8C877F;
  pointer-events: none;
}

.auth-input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.6rem;
  border: 1px solid #D6CECE;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #1C1917;
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.auth-input:focus {
  border-color: #8E4A3E;
  box-shadow: 0 0 0 3px rgba(142, 74, 62, 0.12);
}

.pwd-toggle-btn {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  color: #8C877F;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 4px;
}

.pwd-toggle-btn:hover {
  color: #1C1917;
}

/* Checkbox */
.form-options-row {
  display: flex;
  align-items: center;
}

.custom-check-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.84rem;
  color: #57534E;
  cursor: pointer;
  user-select: none;
}

.custom-checkbox {
  accent-color: #8E4A3E;
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.info-bubble-icon {
  color: #A8A29E;
  cursor: help;
}

.inline-text-link {
  color: #8E4A3E;
  text-decoration: underline;
}

/* Primary Button */
.btn-auth-primary {
  width: 100%;
  padding: 0.9rem 1.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.25);
  transition: all 0.2s ease;
  margin-top: 0.25rem;
}

.btn-auth-primary:hover:not(:disabled) {
  background: #76392F;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(142, 74, 62, 0.32);
}

.btn-auth-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 1-Click Demo Button */
.btn-demo-quick-login {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.65rem 1rem;
  background: #F8F3ED;
  border: 1px dashed #D4BAA8;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #8E4A3E;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-demo-quick-login:hover {
  background: #F1E5DA;
  border-color: #8E4A3E;
}

/* Divider */
.auth-divider {
  display: flex;
  align-items: center;
  margin: 1.75rem 0 1.25rem;
  position: relative;
}

.auth-divider::before {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #EFE6DD;
}

.auth-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #EFE6DD;
}

.divider-text {
  padding: 0 1rem;
  font-size: 0.8rem;
  color: #8C877F;
  background: #FFFFFF;
}

/* Social Login Grid */
.social-login-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1.75rem;
}

.social-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.75rem 0.5rem;
  border: 1px solid #EFE6DD;
  border-radius: 8px;
  background: #FFFFFF;
  cursor: pointer;
  transition: all 0.18s ease;
}

.social-btn span {
  font-size: 0.72rem;
  font-weight: 500;
  color: #57534E;
  text-align: center;
  line-height: 1.2;
}

.social-btn:hover {
  background: #FAF7F2;
  border-color: #D6CECE;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(28, 25, 23, 0.05);
}

/* Footer Switch */
.auth-switch-footer {
  text-align: center;
  font-size: 0.88rem;
  color: #57534E;
}

.switch-link-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.88rem;
  font-weight: 700;
  color: #8E4A3E;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.15s ease;
}

.switch-link-btn:hover {
  color: #6C332A;
}

/* Responsive */
@media (max-width: 1024px) {
  .auth-grid-wrapper {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
  .auth-editorial-col {
    display: none;
  }
  .auth-form-card {
    max-width: 480px;
    margin: 0 auto;
  }
}
</style>
