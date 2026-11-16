<template>
  <div class="khqr-modal-backdrop" @click.self="handleClose">
    <section class="khqr-modal" role="dialog" aria-modal="true" aria-labelledby="khqr-title">
      <header class="khqr-header">
        <h2 id="khqr-title">{{ paywayUrl ? 'ABA KHQR' : 'KHQR Payment' }}</h2>
        <div v-if="!paymentApproved && !qrError" class="khqr-timer" role="timer" aria-label="Time remaining">
          <span class="khqr-timer-ring" aria-hidden="true"></span>
          {{ formattedTimer }}
        </div>
      </header>

      <div class="khqr-card">
        <div class="khqr-banner">
          <svg width="60" height="14" viewBox="0 0 60 14" aria-hidden="true" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M39.0058 5.19439V9.59764H34.5316C34.0727 9.59764 33.7285 9.2307 33.7285 8.80731V5.22264C33.7285 4.77103 34.1014 4.43231 34.5316 4.43231H38.174C38.6616 4.40408 39.0058 4.74278 39.0058 5.19439Z" fill="white"/>
          <path d="M59.9716 6.97176H57.7345C57.7345 4.34676 55.5547 2.20159 52.8874 2.20159C50.765 2.20159 48.9008 3.55645 48.2698 5.53225C48.1264 6.01209 48.0403 6.49192 48.0403 6.97176V13.9718H47.983C46.7784 13.9718 45.8032 13.0121 45.8032 11.8266V6.97176H45.8319C45.8319 5.05241 46.635 3.21773 48.069 1.89112C49.3883 0.677406 51.1092 0 52.9161 0C56.8167 0 59.9716 3.13305 59.9716 6.97176Z" fill="white"/>
          <path d="M59.9999 13.9713L56.845 13.9996L56.0706 13.2374L54.3497 11.5439L51.9692 9.20117H55.1241L59.9999 13.9713Z" fill="white"/>
          <path d="M39.7517 11.7702H33.0117C32.18 11.7702 31.5203 11.121 31.5203 10.3024V3.66936C31.5203 2.85081 32.18 2.20159 33.0117 2.20159H39.7517C40.5835 2.20159 41.2431 2.85081 41.2431 3.66936V10.3024L43.4802 12.504V2.14515C43.4802 0.959671 42.5051 0 41.3005 0H31.4629C30.2584 0 29.2832 0.959671 29.2832 2.14515V11.8266C29.2832 13.0121 30.2584 13.9718 31.4629 13.9718H41.9888L39.7517 11.7702Z" fill="white"/>
          <path d="M12.3614 14H9.20656L2.60996 7.47984V14H0V0H2.60996V6.2379L8.94843 0H12.046L5.16255 6.71772L12.3614 14Z" fill="white"/>
          <path d="M24.1491 0H26.7016V14H24.1491V7.93145H16.8641V14H14.3115V0H16.8641V5.84273H24.1491V0Z" fill="white"/>
          </svg>
        </div>
        <div class="khqr-details">
          <div class="khqr-merchant">{{ liveMerchantName }}</div>
          <div class="khqr-amount">{{ formattedAmount }} <span>USD</span></div>
        </div>
        <div class="khqr-divider" aria-hidden="true"></div>
        <div class="khqr-code">
          <div v-if="loadingQr" class="khqr-loading" role="status">
            <span class="khqr-spinner" aria-hidden="true"></span>
            Generating payment QR…
          </div>
          <p v-else-if="paymentApproved" class="khqr-approved" role="status">
            <strong>Payment approved</strong>
            <span>Opening your order confirmation…</span>
          </p>
          <p v-else-if="qrError" class="khqr-error" role="alert">{{ qrError }}</p>
          <div v-else class="khqr-canvas-holder">
            <canvas ref="canvasEl" class="khqr-canvas-img" role="img" aria-label="KHQR payment code"></canvas>
            <span class="khqr-currency-badge" aria-hidden="true">$</span>
          </div>
        </div>
      </div>

      <p v-if="!qrError && !paymentApproved" class="khqr-instructions">
        Scan with ABA Mobile or another banking app that supports KHQR.
      </p>
      <div v-if="!paymentApproved" class="khqr-actions">
        <button type="button" class="khqr-cancel" @click="handleClose">{{ requiresReview ? 'Close' : 'Cancel' }}</button>
        <button v-if="paywayUrl && !qrError" type="button" class="khqr-payway" @click="openAbaLink">
          Open ABA Pay Link
        </button>
        <button v-if="!qrError" type="button" class="khqr-copy-link" @click="copyPaymentLink">
          {{ copiedPaymentLink ? '✓ Payment Link Copied' : '📋 Copy Payment Link' }}
        </button>
      </div>

      <button
        v-if="!paymentApproved && !qrError"
        type="button"
        class="khqr-demo-approve"
        :disabled="isSimulating"
        @click="simulateApproval"
      >
        {{ isSimulating ? 'Verifying bank clearance…' : '⚡ Demo Mode: Simulate Instant Bank Approval' }}
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import QRCode from 'qrcode'
import axios from 'axios'
import { orderRequest } from '@/utils/orderAccess'

const props = defineProps({
  orderNumber: {
    type: String,
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  expiresAt: { type: String, default: '' },
  merchantName: {
    type: String,
    default: 'LUMÉA ATELIER'
  }
})

const emit = defineEmits(['approved', 'cancelled'])

const canvasEl = ref(null)
const loadingQr = ref(true)
const qrError = ref('')
const requiresReview = ref(false)
const paymentApproved = ref(false)
const qrString = ref('')
const clientId = ref(null)
const paywayUrl = ref('')
const liveMerchantName = ref(props.merchantName || 'LUMÉA ATELIER')
const timeLeft = ref(props.expiresAt ? Math.max(0, Math.floor((new Date(props.expiresAt).getTime() - Date.now()) / 1000)) : 300) // 5 minutes

let timerInterval = null
let pollInterval = null

const formattedAmount = computed(() => props.amount.toFixed(2))

const formattedTimer = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  const s = timeLeft.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

onMounted(async () => {
  await fetchAndRenderKHQR()
  startCountdown(); startPolling()
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
    }, orderRequest(props.orderNumber))
    
    if (res.data && res.data.data) {
      const d = res.data.data
      qrString.value = d.qr_string
      clientId.value = d.client_id
      if (d.payway_url) paywayUrl.value = d.payway_url
      if (d.merchant_name) liveMerchantName.value = d.merchant_name
    }
  } catch (err) {
    qrError.value = err.response?.data?.detail || 'Unable to generate your payment code. Close this attempt and try again.'
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
      width: 220,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      errorCorrectionLevel: 'H' // Allows for the central currency badge
    },
    (error) => {
      if (error) console.error('KHQR Canvas render error:', error)
      if (canvasEl.value) {
        canvasEl.value.style.width = '220px'
        canvasEl.value.style.height = '220px'
      }
    }
  )
  if (canvasEl.value) {
    canvasEl.value.style.width = '220px'
    canvasEl.value.style.height = '220px'
  }
}

function startCountdown() {
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      clearInterval(timerInterval)
      if (pollInterval) clearInterval(pollInterval)
      handleClose()
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
      }, orderRequest(props.orderNumber))
      if (res.data && res.data.paid) onSuccess()
      else if (res.data.action === 'review') {
        requiresReview.value = true; qrError.value = res.data.message
        clearInterval(pollInterval); clearInterval(timerInterval)
      } else if (['expired', 'cancelled'].includes(res.data.action)) handleClose()
    } catch (e) {}
  }, 2500)
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

const copiedPaymentLink = ref(false)

function copyPaymentLink() {
  const link = paywayUrl.value || `${window.location.origin}/account/orders/${props.orderNumber}`
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(link).then(() => {
      copiedPaymentLink.value = true
      setTimeout(() => { copiedPaymentLink.value = false }, 2500)
    }).catch(() => fallbackCopy(link))
  } else {
    fallbackCopy(link)
  }
}

function fallbackCopy(text) {
  const el = document.createElement('textarea')
  el.value = text
  el.setAttribute('readonly', '')
  el.style.position = 'absolute'
  el.style.left = '-9999px'
  document.body.appendChild(el)
  el.select()
  try {
    document.execCommand('copy')
    copiedPaymentLink.value = true
    setTimeout(() => { copiedPaymentLink.value = false }, 2500)
  } catch (e) {
    console.warn('Copy failed', e)
  }
  document.body.removeChild(el)
}

function openAbaLink() {
  if (paywayUrl.value) {
    window.open(paywayUrl.value, '_blank')
  }
}

const isSimulating = ref(false)

async function simulateApproval() {
  if (isSimulating.value || paymentApproved.value) return
  isSimulating.value = true
  try {
    const res = await axios.post('/api/payments/khqr/simulate-approve', {
      order_number: props.orderNumber
    }, orderRequest(props.orderNumber))
    if (res.data && res.data.paid) {
      onSuccess()
    }
  } catch (err) {
    console.error('Demo simulation error:', err)
  } finally {
    isSimulating.value = false
  }
}

function handleClose() {
  if (paymentApproved.value) return
  if (props.orderNumber && !requiresReview.value) {
    axios.post('/api/payments/khqr/cancel', { order_number: props.orderNumber }, orderRequest(props.orderNumber)).catch(() => {})
  }
  emit('cancelled', { requiresReview: requiresReview.value })
}
</script>

<style scoped>
.khqr-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  overflow-y: auto;
  padding: 16px;
  background: rgb(8 27 55 / 60%);
}

.khqr-modal {
  width: min(100%, 396px);
  margin: auto;
  padding: 24px;
  border-radius: 24px;
  background: #fff;
  color: #081b37;
  box-shadow: 0 16px 48px rgb(8 27 55 / 20%);
  font-family: system-ui, sans-serif;
}

.khqr-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 24px;
}

.khqr-header h2 {
  margin: 0;
  font: 600 24px/1.2 system-ui, sans-serif;
}

.khqr-timer {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.khqr-timer-ring,
.khqr-spinner {
  width: 22px;
  height: 22px;
  border: 4px solid #e8eef1;
  border-right-color: #0bbcd4;
  border-radius: 50%;
}

.khqr-card {
  width: min(100%, 280px);
  margin-inline: auto;
  border-radius: 22px;
  background: #fff;
  color: #171717;
  box-shadow: 0 8px 16px rgb(0 0 0 / 8%), 0 0 0 1px rgb(8 27 55 / 5%);
  overflow: hidden;
}

.khqr-banner {
  position: relative;
  display: grid;
  height: 48px;
  place-items: center;
  border-radius: 22px 22px 0 0;
  background: #e21a1a;
}

.khqr-banner::after {
  position: absolute;
  top: 100%;
  right: 0;
  border-top: 23px solid #e21a1a;
  border-left: 23px solid transparent;
  content: '';
}

.khqr-details {
  padding: 26px 38px 18px;
}

.khqr-merchant {
  font-size: 11px;
  overflow-wrap: anywhere;
}

.khqr-amount {
  margin-top: 8px;
  font-size: 21px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.khqr-amount span {
  margin-left: 6px;
  font-size: 10px;
  font-weight: 400;
  vertical-align: middle;
}

.khqr-divider {
  height: 1px;
  background: repeating-linear-gradient(to right, #808080 0 8px, transparent 8px 16px);
}

.khqr-code {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 242px;
  padding: 16px;
  text-align: center;
  overflow: hidden;
}

.khqr-canvas-holder {
  position: relative;
  width: 220px;
  height: 220px;
  max-width: 100%;
  aspect-ratio: 1;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-sizing: border-box;
}

.khqr-canvas-img {
  display: block !important;
  width: 220px !important;
  height: 220px !important;
  max-width: 100% !important;
  max-height: 100% !important;
  aspect-ratio: 1;
  object-fit: contain;
  image-rendering: pixelated;
  box-sizing: border-box;
}

.khqr-currency-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: grid;
  width: 26px;
  height: 26px;
  place-items: center;
  border: 2px solid #fff;
  border-radius: 50%;
  background: #111;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
  pointer-events: none;
  z-index: 2;
}

.khqr-loading,
.khqr-approved {
  display: grid;
  justify-items: center;
  gap: 8px;
  font-size: 14px;
}

.khqr-spinner {
  animation: khqr-spin 0.8s linear infinite;
}

.khqr-approved strong {
  color: #15803d;
}

.khqr-error {
  color: #a32020;
  font-size: 14px;
  overflow-wrap: anywhere;
}

.khqr-instructions {
  max-width: 273px;
  margin: 24px auto 0;
  font-size: 14px;
  line-height: 1.4;
  text-align: center;
}

.khqr-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  margin-top: 20px;
}

.khqr-actions button {
  min-height: 44px;
  padding: 8px 16px;
  border: 1px solid #d6e1e8;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
}

.khqr-actions .khqr-payway {
  border-color: #00567b;
  background: #00567b;
  color: #fff;
  cursor: pointer;
}

.khqr-actions .khqr-copy-link {
  border-color: #7a2e22;
  background: #fbf6f3;
  color: #7a2e22;
  cursor: pointer;
  transition: all 0.2s ease;
}

.khqr-actions .khqr-copy-link:hover {
  background: #f5ebe6;
}

.khqr-cancel {
  background: #fff;
  color: inherit;
  cursor: pointer;
}

.khqr-demo-approve {
  display: block;
  width: 100%;
  margin-top: 14px;
  padding: 10px 14px;
  background: #fdf8f0;
  color: #925e1a;
  border: 1px dashed #dca550;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.khqr-demo-approve:hover:not(:disabled) {
  background: #faecd8;
  color: #70450d;
}

.khqr-demo-approve:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes khqr-spin {
  to { transform: rotate(360deg); }
}

@media (prefers-reduced-motion: reduce) {
  .khqr-spinner {
    animation: none;
  }
}
</style>
