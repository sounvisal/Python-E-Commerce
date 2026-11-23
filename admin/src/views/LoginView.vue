<script setup>
import { useAuthStore } from '@/stores/auth'
import { ArrowRight, Eye, EyeOff, Lock, Mail, ShieldCheck, Sparkles } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const errorMessage = ref('')
const showPassword = ref(false)

async function handleLogin(event) {
  if (authStore.isLoading) return

  const credentials = new FormData(event.currentTarget)
  const email = credentials.get('email').trim()
  const password = credentials.get('password')
  if (!email || !password) {
    errorMessage.value = 'Please enter both email and password.'
    return
  }

  errorMessage.value = ''

  const res = await authStore.login(email, password)

  if (res.success) {
    const redirect = route.query.redirect
    const isInternal = typeof redirect === 'string' && /^\/(?![/\\])/.test(redirect)
    const destination = isInternal && router.resolve(redirect).meta.requiresAuth ? redirect : '/dashboard'
    await router.replace(destination)
  } else {
    errorMessage.value = res.message || 'Login failed. Use a valid administrator account.'
  }
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
          <Sparkles :size="20" class="crest-icon-svg" />
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

        <form @submit.prevent="handleLogin" class="login-form" :aria-busy="authStore.isLoading">
          <div v-if="errorMessage" class="error-banner" role="alert">
            {{ errorMessage }}
          </div>

          <!-- Email -->
          <div class="form-group">
            <label for="email">Administrator Email</label>
            <div class="input-with-icon">
              <Mail :size="17" class="field-icon" aria-hidden="true" />
              <input
                id="email"
                name="email"
                class="atelier-input"
                type="email"
                placeholder="name@example.com"
                required
                autocomplete="username"
                autocapitalize="none"
                spellcheck="false"
              />
            </div>
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-with-icon password-field">
              <Lock :size="17" class="field-icon" aria-hidden="true" />
              <input
                id="password"
                name="password"
                class="atelier-input"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
              />
              <button
                class="password-toggle"
                type="button"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                aria-controls="password"
                @click="showPassword = !showPassword"
              >
                <component :is="showPassword ? EyeOff : Eye" :size="18" aria-hidden="true" />
              </button>
            </div>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="btn btn-primary login-btn" :disabled="authStore.isLoading">
            <span>{{ authStore.isLoading ? 'Signing in…' : 'Sign in' }}</span>
            <ArrowRight v-if="!authStore.isLoading" :size="16" aria-hidden="true" />
          </button>
        </form>

        <!-- Security Note -->
        <div class="security-note" role="status">
          <ShieldCheck :size="14" aria-hidden="true" />
          <span>{{ authStore.isLoading ? 'The server may take a minute to wake up.' : 'Administrator access only' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: var(--bg-app);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding: clamp(1rem, 4vw, 2rem);
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

.crest-icon-svg {
  color: #0B0C10;
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
  padding: clamp(1.25rem, 5vw, 2.25rem);
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
  background: var(--rose-bg);
  border: 1px solid var(--rose-border);
  border-radius: var(--radius-sm);
  color: var(--rose);
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
  min-height: 48px;
  font-size: 1rem;
  padding-left: 2.75rem;
}

.password-field input {
  padding-right: 3rem;
}

.password-toggle {
  position: absolute;
  right: 2px;
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  color: var(--text-muted);
  border-radius: var(--radius-sm);
}

.password-toggle:focus-visible,
.login-btn:focus-visible {
  outline: 2px solid var(--crimson);
  outline-offset: 2px;
}

.login-btn {
  width: 100%;
  min-height: 48px;
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
