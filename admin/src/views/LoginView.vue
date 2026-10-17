<script setup>
import { useAuthStore } from '@/stores/auth'
import { ArrowRight, KeyRound, Lock, Mail, ShieldCheck, Sparkles } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('admin@lumea.com')
const password = ref('admin123')
const errorMessage = ref('')
const isSubmitting = ref(false)

function fillDemoCredentials() {
  email.value = 'admin@lumea.com'
  password.value = 'admin123'
}

async function handleLogin() {
  if (!email.value || !password.value) {
    errorMessage.value = 'Please enter both email and password.'
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  const res = await authStore.login(email.value, password.value)
  isSubmitting.value = false

  if (res.success) {
    const redirectPath = route.query.redirect || '/dashboard'
    router.push(redirectPath)
  } else {
    // If backend isn't reachable or password mismatch, offer 1-click fallback
    errorMessage.value = res.message || 'Login failed. Try the 1-Click Demo Login below.'
  }
}

function handleDemoInstantLogin() {
  authStore.demoLogin()
  const redirectPath = route.query.redirect || '/dashboard'
  router.push(redirectPath)
}
</script>

<template>
  <div class="login-wrapper">
    <!-- Ambient Background Lighting -->
    <div class="glow-orb glow-top"></div>
    <div class="glow-orb glow-bottom"></div>

    <div class="login-container">
      <!-- Brand Crest -->
      <div class="login-brand">
        <div class="brand-crest">
          <span class="crest-icon">✦</span>
        </div>
        <h1 class="brand-title">LUMEA</h1>
        <p class="brand-subtitle">Atelier Administration & Curator Console</p>
      </div>

      <!-- Login Card -->
      <div class="login-card">
        <div class="card-headline">
          <h2>Console Authentication</h2>
          <p>Enter your administrator credentials to access store analytics and inventory control.</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div v-if="errorMessage" class="error-banner">
            {{ errorMessage }}
          </div>

          <!-- Email -->
          <div class="form-group">
            <label for="email">Administrator Email</label>
            <div class="input-with-icon">
              <Mail :size="17" class="field-icon" />
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="admin@lumea.com"
                required
                autocomplete="email"
              />
            </div>
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password">Security Passcode</label>
            <div class="input-with-icon">
              <Lock :size="17" class="field-icon" />
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="••••••••"
                required
                autocomplete="current-password"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="btn btn-primary login-btn" :disabled="isSubmitting">
            <span v-if="!isSubmitting">Authenticate & Enter Console</span>
            <span v-else>Verifying Credentials...</span>
            <ArrowRight :size="16" v-if="!isSubmitting" />
          </button>
        </form>

        <!-- Demo Helpers Divider -->
        <div class="demo-divider">
          <span>Demo Access Options</span>
        </div>

        <!-- Demo Quick Actions -->
        <div class="demo-actions">
          <button type="button" class="btn btn-secondary demo-btn" @click="fillDemoCredentials">
            <KeyRound :size="15" />
            <span>Autofill Seeded Credentials</span>
          </button>

          <button type="button" class="btn demo-instant-btn" @click="handleDemoInstantLogin">
            <Sparkles :size="15" />
            <span>1-Click Instant Demo Login</span>
          </button>
        </div>

        <!-- Security Note -->
        <div class="security-note">
          <ShieldCheck :size="14" />
          <span>Protected by Sanctum Token Authentication & Role Verification</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  width: 100vw;
  background-color: var(--bg-app);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: 2rem;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
}

.glow-top {
  top: -10%;
  left: 20%;
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(194, 155, 56, 0.15) 0%, transparent 70%);
}

.glow-bottom {
  bottom: -15%;
  right: 15%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(196, 98, 60, 0.12) 0%, transparent 70%);
}

.login-container {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 10;
}

.login-brand {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-crest {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #C29B38 0%, #D8B24C 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  box-shadow: 0 8px 24px rgba(194, 155, 56, 0.3);
}

.crest-icon {
  color: #0B0C10;
  font-size: 1.5rem;
  font-weight: 800;
}

.brand-title {
  font-family: var(--font-serif);
  font-size: 2.2rem;
  letter-spacing: 0.18em;
  font-weight: 700;
  color: var(--text-main);
}

.brand-subtitle {
  font-size: 0.82rem;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 0.3rem;
}

.login-card {
  width: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  padding: 2.25rem 2rem;
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(16px);
}

.card-headline {
  margin-bottom: 1.75rem;
}

.card-headline h2 {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  color: var(--text-main);
  margin-bottom: 0.35rem;
}

.card-headline p {
  font-size: 0.82rem;
  color: var(--text-muted);
  line-height: 1.4;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.error-banner {
  padding: 0.75rem 1rem;
  background: rgba(244, 63, 94, 0.12);
  border: 1px solid rgba(244, 63, 94, 0.3);
  border-radius: var(--radius-sm);
  color: #FB7185;
  font-size: 0.82rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-dim);
  pointer-events: none;
}

.input-with-icon input {
  width: 100%;
  padding-left: 2.75rem;
}

.login-btn {
  width: 100%;
  padding: 0.85rem;
  margin-top: 0.5rem;
  font-size: 0.92rem;
}

.demo-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.75rem 0 1.25rem;
  color: var(--text-dim);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.demo-divider::before,
.demo-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-subtle);
}

.demo-divider span {
  padding: 0 12px;
}

.demo-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.demo-btn {
  font-size: 0.82rem;
  padding: 0.65rem;
  width: 100%;
}

.demo-instant-btn {
  background: rgba(194, 155, 56, 0.1);
  border: 1px dashed var(--gold-border);
  color: var(--gold);
  font-size: 0.82rem;
  padding: 0.65rem;
  width: 100%;
  transition: all var(--transition-fast);
}

.demo-instant-btn:hover {
  background: rgba(194, 155, 56, 0.2);
  border-style: solid;
}

.security-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 1.75rem;
  font-size: 0.72rem;
  color: var(--text-dim);
  text-align: center;
}
</style>
