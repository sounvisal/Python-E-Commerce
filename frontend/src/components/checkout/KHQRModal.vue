<template>
  <div class="khqr-modal-backdrop" @click.self="handleClose">
    <div class="khqr-card-container">
      <!-- Authentic Bakong KHQR Card -->
      <div class="khqr-card">
        <!-- Top KHQR Red Header matching NBC Bakong specification -->
        <div class="khqr-header">
          <div class="khqr-logo-wrap">
            <span class="khqr-logo-kh">KH</span>
            <div class="khqr-logo-qr-box">
              <span class="khqr-logo-qr">QR</span>
              <div class="khqr-ribbon-cut"></div>
            </div>
          </div>
          <div class="khqr-currency-pill">
            <span>USD</span>
          </div>
        </div>

        <!-- Merchant & Amount Info -->
        <div class="khqr-body">
          <div class="khqr-merchant-info">
            <h3 class="khqr-merchant-name">{{ merchantName || 'SUON VISAL' }}</h3>
            <span class="khqr-merchant-sub">LUMÉA ATELIER &middot; OFFICIAL STORE</span>
            <div class="khqr-order-tag">Order #{{ orderNumber }}</div>
          </div>

          <div class="khqr-amount-row">
            <span class="khqr-currency-symbol">$</span>
            <span class="khqr-amount-val">{{ Number(amount).toFixed(2) }}</span>
            <span class="khqr-khr-equiv">(&asymp; {{ (Number(amount) * 4100).toLocaleString() }} KHR)</span>
          </div>

          <!-- Dynamic QR Code Frame -->
          <div class="khqr-frame-outer">
            <div class="khqr-frame-inner">
              <div v-if="loadingQr" class="khqr-loading-box">
                <div class="khqr-spinner"></div>
                <span>Generating dynamic KHQR...</span>
              </div>
              <div v-else class="canvas-wrap">
                <canvas ref="canvasEl" class="khqr-canvas"></canvas>
                <!-- Centered Bakong / Currency Badge -->
                <div class="khqr-center-badge">
                  <div class="center-badge-inner">
                    <span class="center-badge-symbol">$</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bank Slogan & Partner Apps -->
          <div class="khqr-banks-section">
            <p class="khqr-scan-slogan">Scan to pay with any mobile banking app supporting KHQR</p>
            <div class="khqr-bank-pills">
              <span class="bank-pill bank-aba">ABA'Mobile</span>
              <span class="bank-pill bank-bakong">Bakong</span>
              <span class="bank-pill bank-wing">Wing</span>
              <span class="bank-pill bank-acleda">ACLEDA</span>
              <span class="bank-pill bank-sathapana">Sathapana</span>
            </div>
          </div>

          <!-- Live Status & Countdown Timer -->
          <div class="khqr-status-card" :class="{ 'status-approved': paymentApproved }">
            <div v-if="!paymentApproved" class="status-pending-row">
              <div class="pulsing-indicator"></div>
              <div class="status-texts">
                <strong>Awaiting bank scan...</strong>
                <span>Expires in <span class="timer-countdown">{{ formattedTimer }}</span></span>
              </div>
            </div>
            <div v-else class="status-approved-row">
              <div class="success-icon-wrap">
                <svg viewBox="0 0 24 24" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <div class="status-texts">
                <strong class="text-success">Payment Approved!</strong>
                <span>Official transaction receipt cleared. Redirecting...</span>
              </div>
            </div>
          </div>

          <!-- Interactive Action Buttons -->
          <div class="khqr-actions">
            <!-- Demo Simulation Button for Academic Defense -->
            <button
              v-if="!paymentApproved"
              type="button"
              class="btn-demo-simulate"
              @click="handleSimulateApproval"
              :disabled="simulating"
            >
              <span class="btn-demo-icon">⚡</span>
              <span v-if="!simulating">Demo Mode: Simulate Instant Bank Approval</span>
              <span v-else>Clearing Transaction...</span>
            </button>

            <div class="khqr-secondary-actions">
              <button
                v-if="paywayUrl"
                type="button"
                class="btn-open-aba"
                @click="openAbaLink"
              >
                <span>Open ABA Pay Link</span>
              </button>
              <button
                type="button"
                class="btn-cancel-khqr"
                @click="handleClose"
              >
                <span>Cancel</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import QRCode from 'qrcode'
import axios from 'axios'

const props = defineProps({
  orderNumber: {
    type: String,
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  merchantName: {
    type: String,
    default: 'SUON VISAL'
  }
})

const emit = defineEmits(['approved', 'cancelled'])

const canvasEl = ref(null)
const loadingQr = ref(true)
const paymentApproved = ref(false)
const simulating = ref(false)
const qrString = ref('')
const clientId = ref(null)
const paywayUrl = ref('https://link.payway.com.kh/ABAPAYaC455755m')
const timeLeft = ref(300) // 5 minutes (300 seconds)

let timerInterval = null
let pollInterval = null

const formattedTimer = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  const s = timeLeft.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

onMounted(async () => {
  await fetchAndRenderKHQR()
  startCountdown()
  startPolling()
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
  if (pollInterval) clearInterval(pollInterval)
})

async function fetchAndRenderKHQR() {
  loadingQr.value = true
  try {
    const res = await axios.post('/api/payments/khqr/generate', {
      order_number: props.orderNumber,
      amount: props.amount,
      try_live: true
    })
    
    if (res.data && res.data.data) {
      const d = res.data.data
      qrString.value = d.qr_string
      clientId.value = d.client_id
      if (d.payway_url) paywayUrl.value = d.payway_url
    }
  } catch (err) {
    console.warn('Live KHQR generate failed, falling back to local EMVCo string', err)
  } finally {
    loadingQr.value = false
    await nextTick()
    renderQR()
  }
}

function renderQR() {
  if (!canvasEl.value || !qrString.value) return

  QRCode.toCanvas(
    canvasEl.value,
    qrString.value,
    {
      width: 230,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      errorCorrectionLevel: 'H'
    },
    (error) => {
      if (error) console.error('KHQR Canvas render error:', error)
    }
  )
}

function startCountdown() {
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      clearInterval(timerInterval)
    }
  }, 1000)
}

function startPolling() {
  pollInterval = setInterval(async () => {
    if (paymentApproved.value) return
    try {
      const res = await axios.post('/api/payments/khqr/check', {
        order_number: props.orderNumber,
        client_id: clientId.value
      })
      if (res.data && res.data.paid) {
        onSuccess()
      }
    } catch (e) {}
  }, 2500)
}

async function handleSimulateApproval() {
  simulating.value = true
  try {
    const res = await axios.post('/api/payments/khqr/simulate-approve', {
      order_number: props.orderNumber
    })
    if (res.data && res.data.paid) {
      onSuccess()
    }
  } catch (err) {
    console.error('Simulation error:', err)
  } finally {
    simulating.value = false
  }
}

function onSuccess() {
  paymentApproved.value = true
  if (pollInterval) clearInterval(pollInterval)
  if (timerInterval) clearInterval(timerInterval)
  setTimeout(() => {
    emit('approved', {
      orderNumber: props.orderNumber,
      amount: props.amount,
      paid: true
    })
  }, 1600)
}

function openAbaLink() {
  if (paywayUrl.value) {
    window.open(paywayUrl.value, '_blank')
  }
}

function handleClose() {
  if (paymentApproved.value) return
  emit('cancelled')
}
</script>

<style scoped>
.khqr-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(18, 14, 13, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
  animation: fadeIn 0.25s ease-out;
}

.khqr-card-container {
  width: 100%;
  max-width: 390px;
  animation: cardSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Authentic Bakong KHQR Card */
.khqr-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* Red KHQR Top Banner */
.khqr-header {
  background: #e1251b;
  color: #ffffff;
  padding: 0.9rem 1.4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.khqr-logo-wrap {
  display: flex;
  align-items: center;
  gap: 3px;
}

.khqr-logo-kh {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 1.6rem;
  font-weight: 900;
  letter-spacing: -0.5px;
  color: #ffffff;
  line-height: 1;
}

.khqr-logo-qr-box {
  background: #ffffff;
  color: #e1251b;
  padding: 2px 7px 3px 5px;
  border-radius: 4px;
  position: relative;
  display: flex;
  align-items: center;
  margin-left: 2px;
}

.khqr-logo-qr {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 1.15rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.5px;
}

.khqr-ribbon-cut {
  position: absolute;
  right: -4px;
  top: 0;
  bottom: 0;
  width: 5px;
  background: #e1251b;
  clip-path: polygon(100% 0, 0 50%, 100% 100%);
}

.khqr-currency-pill {
  background: rgba(255, 255, 255, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 3px 8px;
  border-radius: 12px;
}

/* Card Body */
.khqr-body {
  padding: 1.25rem 1.4rem 1.4rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.khqr-merchant-info {
  margin-bottom: 0.5rem;
}

.khqr-merchant-name {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 1.15rem;
  font-weight: 800;
  color: #111827;
  letter-spacing: 0.5px;
  margin: 0 0 2px 0;
  text-transform: uppercase;
}

.khqr-merchant-sub {
  font-size: 0.68rem;
  letter-spacing: 1.2px;
  color: #7A2E22;
  font-weight: 700;
  display: block;
  text-transform: uppercase;
}

.khqr-order-tag {
  display: inline-block;
  background: #F5EFEB;
  color: #555555;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  margin-top: 4px;
}

/* Amount Row */
.khqr-amount-row {
  margin: 0.4rem 0 0.9rem;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 3px;
}

.khqr-currency-symbol {
  font-size: 1.2rem;
  font-weight: 700;
  color: #111827;
}

.khqr-amount-val {
  font-size: 1.85rem;
  font-weight: 900;
  color: #111827;
  letter-spacing: -0.5px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.khqr-khr-equiv {
  font-size: 0.72rem;
  color: #6B7280;
  font-weight: 500;
  margin-left: 4px;
}

/* QR Outer Frame */
.khqr-frame-outer {
  background: #ffffff;
  padding: 8px;
  border-radius: 16px;
  border: 1px solid #E5E7EB;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  margin-bottom: 0.9rem;
}

.khqr-frame-inner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 230px;
  min-height: 230px;
}

.khqr-loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #666;
}

.khqr-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #F5EFEB;
  border-top-color: #E1251B;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.canvas-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.khqr-canvas {
  display: block;
  border-radius: 6px;
}

/* Center Emblem */
.khqr-center-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
  background: #ffffff;
  border: 2.5px solid #E1251B;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.center-badge-inner {
  width: 32px;
  height: 32px;
  background: #E1251B;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.center-badge-symbol {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 900;
  line-height: 1;
}

/* Banks Section */
.khqr-banks-section {
  width: 100%;
  margin-bottom: 0.9rem;
}

.khqr-scan-slogan {
  font-size: 0.72rem;
  color: #4B5563;
  font-weight: 500;
  margin: 0 0 0.5rem 0;
}

.khqr-bank-pills {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  flex-wrap: wrap;
}

.bank-pill {
  font-size: 0.62rem;
  font-weight: 700;
  padding: 3px 7px;
  border-radius: 4px;
  letter-spacing: 0.2px;
}

.bank-aba {
  background: #005D7B;
  color: #ffffff;
}

.bank-bakong {
  background: #E1251B;
  color: #ffffff;
}

.bank-wing {
  background: #8EC03F;
  color: #111827;
}

.bank-acleda {
  background: #0C3C60;
  color: #F8C300;
}

.bank-sathapana {
  background: #0D2E5C;
  color: #ffffff;
}

/* Status Card */
.khqr-status-card {
  width: 100%;
  background: #FDF9F6;
  border: 1px solid #F0E6DD;
  border-radius: 10px;
  padding: 0.6rem 0.8rem;
  margin-bottom: 0.9rem;
  transition: all 0.3s ease;
}

.status-approved {
  background: #F0FDF4;
  border-color: #BBF7D0;
}

.status-pending-row, .status-approved-row {
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
}

.pulsing-indicator {
  width: 12px;
  height: 12px;
  background: #EAB308;
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(234, 179, 8, 0.7);
  animation: pulseGold 1.6s infinite;
  flex-shrink: 0;
}

.success-icon-wrap {
  width: 24px;
  height: 24px;
  background: #22C55E;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-texts {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
}

.status-texts strong {
  color: #1F2937;
  font-size: 0.8rem;
}

.text-success {
  color: #16A34A !important;
}

.status-texts span {
  color: #6B7280;
}

.timer-countdown {
  font-weight: 700;
  color: #E1251B;
}

/* Actions */
.khqr-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.btn-demo-simulate {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border: 1.5px solid #F59E0B;
  color: #92400E;
  font-weight: 700;
  font-size: 0.78rem;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.15);
}

.btn-demo-simulate:hover {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(245, 158, 11, 0.25);
}

.btn-demo-icon {
  font-size: 0.95rem;
}

.khqr-secondary-actions {
  display: flex;
  gap: 8px;
}

.btn-open-aba {
  flex: 1;
  background: #005D7B;
  color: #ffffff;
  border: none;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.55rem;
  border-radius: 6px;
  cursor: pointer;
}

.btn-open-aba:hover {
  background: #004d66;
}

.btn-cancel-khqr {
  flex: 1;
  background: #F3F4F6;
  color: #4B5563;
  border: none;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.55rem;
  border-radius: 6px;
  cursor: pointer;
}

.btn-cancel-khqr:hover {
  background: #E5E7EB;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulseGold {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(234, 179, 8, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(234, 179, 8, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(234, 179, 8, 0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes cardSlideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
