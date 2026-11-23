<template>
  <div class="khqr-modal-backdrop" @click.self="handleClose">
    <div
      ref="modalContainerRef"
      class="khqr-modal-container"
      role="dialog"
      aria-modal="true"
      aria-labelledby="khqr-dialog-title"
      tabindex="-1"
    >
      <!-- Modal Header -->
      <div class="khqr-modal-top-bar">
        <h2 id="khqr-dialog-title" class="khqr-modal-heading">KHQR Payment</h2>
        <div v-if="!paymentApproved && !qrError" class="khqr-timer-pill">
          <span class="timer-dot"></span>
          <span>{{ formattedTimer }}</span>
        </div>
      </div>

      <!-- Exact Official Card from checkout.html (width: 273px, height: 396px) -->
      <div class="khqr-content">
        <!-- Top Red Banner -->
        <div class="khqr-banner">
          <svg width="60" height="14" viewBox="0 0 60 14" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M39.0058 5.19439V9.59764H34.5316C34.0727 9.59764 33.7285 9.2307 33.7285 8.80731V5.22264C33.7285 4.77103 34.1014 4.43231 34.5316 4.43231H38.174C38.6616 4.40408 39.0058 4.74278 39.0058 5.19439Z" fill="white"/>
            <path d="M59.9716 6.97176H57.7345C57.7345 4.34676 55.5547 2.20159 52.8874 2.20159C50.765 2.20159 48.9008 3.55645 48.2698 5.53225C48.1264 6.01209 48.0403 6.49192 48.0403 6.97176V13.9718H47.983C46.7784 13.9718 45.8032 13.0121 45.8032 11.8266V6.97176H45.8319C45.8319 5.05241 46.635 3.21773 48.069 1.89112C49.3883 0.677406 51.1092 0 52.9161 0C56.8167 0 59.9716 3.13305 59.9716 6.97176Z" fill="white"/>
            <path d="M59.9999 13.9713L56.845 13.9996L56.0706 13.2374L54.3497 11.5439L51.9692 9.20117H55.1241L59.9999 13.9713Z" fill="white"/>
            <path d="M39.7517 11.7702H33.0117C32.18 11.7702 31.5203 11.121 31.5203 10.3024V3.66936C31.5203 2.85081 32.18 2.20159 33.0117 2.20159H39.7517C40.5835 2.20159 41.2431 2.85081 41.2431 3.66936V10.3024L43.4802 12.504V2.14515C43.4802 0.959671 42.5051 0 41.3005 0H31.4629C30.2584 0 29.2832 0.959671 29.2832 2.14515V11.8266C29.2832 13.0121 30.2584 13.9718 31.4629 13.9718H41.9888L39.7517 11.7702Z" fill="white"/>
            <path d="M12.3614 14H9.20656L2.60996 7.47984V14H0V0H2.60996V6.2379L8.94843 0H12.046L5.16255 6.71772L12.3614 14Z" fill="white"/>
            <path d="M24.1491 0H26.7016V14H24.1491V7.93145H16.8641V14H14.3115V0H16.8641V5.84273H24.1491V0Z" fill="white"/>
          </svg>
        </div>

        <!-- Official Triangle Corner Cut -->
        <div class="triangle-row">
          <div class="triangle-top-right"></div>
        </div>

        <!-- Merchant & Amount Info (from checkout.html) -->
        <div class="merc-khqr-info">
          <div class="merc-name">{{ liveMerchantName }}</div>
          <div class="total-amount-khqr">
            <span class="amount-value">
              {{ formattedAmount }}
              <span class="amount-currency">USD</span>
            </span>
          </div>
        </div>

        <!-- Line Divider SVG (from checkout.html) -->
        <div class="line-divider">
          <svg width="273" height="2" viewBox="0 0 273 2" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 0.845703H273" stroke="black" stroke-opacity="0.3" stroke-dasharray="8 8"/>
          </svg>
        </div>

        <!-- QR Code Canvas Area with Central USD Logo -->
        <div class="qr-canvas-box">
          <div v-if="loadingQr" class="khqr-state-box">
            <div class="khqr-spinner"></div>
            <span>Generating QR code…</span>
          </div>
          <div v-else-if="paymentApproved" class="khqr-state-box status-success">
            <div class="success-checkmark"><Check :size="24" /></div>
            <strong>Payment Approved</strong>
            <span>Redirecting to receipt…</span>
          </div>
          <div v-else-if="qrError" class="khqr-state-box status-err">
            <p>{{ qrError }}</p>
            <button v-if="!reviewRequired && !closing" type="button" class="btn-retry-khqr" @click="fetchAndRenderKHQR">Retry</button>
          </div>
          <div v-else class="qr-canvas-holder">
            <canvas ref="canvasEl" class="qr-canvas-element"></canvas>
            <div class="usd-khqr-badge">
              <span class="badge-dollar">$</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Slogan (from checkout.html) -->
      <p class="khqr-text-desc">
        Scan with ABA Mobile, or other Mobile Banking App supporting KHQR
      </p>

      <!-- Action buttons -->
      <div class="khqr-button-group">
        <button
          v-if="!paymentApproved"
          type="button"
          class="btn-khqr-close"
          :disabled="closing"
          @click="handleClose"
        >
          {{ reviewRequired ? 'Close' : closing ? 'Cancelling…' : 'Cancel' }}
        </button>
        <button
          v-if="paywayUrl && !paymentApproved && !qrError"
          type="button"
          class="btn-khqr-aba"
          @click="openAbaLink"
        >
          Open ABA Mobile
        </button>
        <button
          v-if="paywayUrl && !paymentApproved && !qrError"
          type="button"
          class="btn-khqr-copy"
          @click="copyPaymentLink"
        >
          <span class="btn-copy-inner">
            <Check v-if="copiedPaymentLink" :size="13" class="copy-icon-svg" />
            <Copy v-else :size="13" class="copy-icon-svg" />
            <span>{{ copiedPaymentLink ? 'Copied' : 'Copy Link' }}</span>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import QRCode from 'qrcode'
import axios from 'axios'
import { orderRequest } from '@/utils/orderAccess'
import { Copy, Check } from 'lucide-vue-next'

const props = defineProps({
  orderNumber: { type: String, required: true },
  amount: { type: Number, required: true },
  expiresAt: { type: String, required: true },
  merchantName: { type: String, default: 'LUMÉA ATELIER' }
})

const emit = defineEmits(['approved', 'cancelled'])
const modalContainerRef = ref(null)
const canvasEl = ref(null)
const loadingQr = ref(true)
const qrError = ref('')
const paymentApproved = ref(false)
const closing = ref(false)
const reviewRequired = ref(false)
const paywayUrl = ref('')
const liveMerchantName = ref(props.merchantName)
const expires = Date.parse(props.expiresAt)
const timeLeft = ref(remainingSeconds())
const copiedPaymentLink = ref(false)
const controller = new AbortController()
const request = { ...orderRequest(props.orderNumber), signal: controller.signal }

let timerInterval
let pollTimeout
let successTimeout
let copyTimeout
let issuing = false
let previousActiveElement = null

const formattedAmount = computed(() => props.amount.toFixed(2))
const formattedTimer = computed(() => {
  const minutes = String(Math.floor(timeLeft.value / 60)).padStart(2, '0')
  const seconds = String(timeLeft.value % 60).padStart(2, '0')
  return minutes + ':' + seconds
})

function handleKeydown(e) {
  if (e.key === 'Escape') {
    e.preventDefault()
    handleClose()
    return
  }
  if (e.key === 'Tab') {
    if (!modalContainerRef.value) return
    const focusable = Array.from(modalContainerRef.value.querySelectorAll(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    ))
    if (focusable.length === 0) return
    const first = focusable[0]
    const last = focusable[focusable.length - 1]
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault()
      last.focus()
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault()
      first.focus()
    }
  }
}

onMounted(() => {
  previousActiveElement = document.activeElement
  window.addEventListener('keydown', handleKeydown)
  fetchAndRenderKHQR()
  nextTick(() => {
    const focusable = modalContainerRef.value?.querySelectorAll(
      'button:not([disabled]), [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    if (focusable && focusable.length > 0) {
      focusable[0].focus()
    } else {
      modalContainerRef.value?.focus()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  controller.abort()
  stopMonitoring()
  clearTimeout(successTimeout)
  clearTimeout(copyTimeout)
  if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
    previousActiveElement.focus()
  }
})

function remainingSeconds() {
  return Number.isFinite(expires) ? Math.max(0, Math.ceil((expires - Date.now()) / 1000)) : 0
}

function message(error, fallback) {
  const detail = error.response?.data?.detail
  return typeof detail === 'string' ? detail : fallback
}

async function fetchAndRenderKHQR() {
  if (issuing || closing.value) return
  issuing = true
  stopMonitoring()
  loadingQr.value = true
  qrError.value = ''
  try {
    const { data } = await axios.post('/api/payments/khqr/generate', {
      order_number: props.orderNumber,
      amount: props.amount
    }, request)
    const payment = data.data
    if (!payment?.qr_string) throw new Error('Missing payment code')
    if (payment.payway_url) {
      paywayUrl.value = payment.payway_url
    } else if (payment.qr_string) {
      const deeplink = new URL('abamobilebank://ababank.com')
      deeplink.searchParams.set('type', 'payway')
      deeplink.searchParams.set('qrcode', payment.qr_string)
      paywayUrl.value = deeplink.toString()
    }
    if (payment.merchant_name) liveMerchantName.value = payment.merchant_name
    loadingQr.value = false
    await nextTick()
    if (controller.signal.aborted || closing.value) return
    await QRCode.toCanvas(canvasEl.value, payment.qr_string, {
      width: 200,
      margin: 4,
      errorCorrectionLevel: 'H'
    })
    if (controller.signal.aborted || closing.value) return
    timeLeft.value = remainingSeconds()
    timerInterval = setInterval(() => { timeLeft.value = remainingSeconds() }, 1000)
    pollTimeout = setTimeout(poll, 2000)
  } catch (error) {
    if (controller.signal.aborted || closing.value) return
    qrError.value = message(error, 'Unable to generate the payment code. Please retry.')
    // A verified payment can arrive while the QR request is still in flight.
    await poll(false)
  } finally {
    issuing = false
    loadingQr.value = false
  }
}

function stopMonitoring() {
  clearInterval(timerInterval)
  clearTimeout(pollTimeout)
}

function applyStatus(status) {
  if (status.action === 'review') {
    reviewRequired.value = true
    qrError.value = status.message
    stopMonitoring()
    return true
  }
  if (status.paid) {
    onSuccess()
    return true
  }
  if (['expired', 'cancelled'].includes(status.action)) {
    stopMonitoring()
    emit('cancelled', { closed: true })
    return true
  }
  return false
}

async function poll(reschedule = true) {
  if (controller.signal.aborted || paymentApproved.value || closing.value) return
  try {
    const { data } = await axios.post('/api/payments/khqr/check', { order_number: props.orderNumber }, request)
    if (controller.signal.aborted || closing.value || applyStatus(data)) return
  } catch (error) {
    if (controller.signal.aborted || closing.value) return
    if (remainingSeconds() === 0) qrError.value = 'Payment verification is temporarily unavailable. Check the order before paying again.'
  }
  if (remainingSeconds() === 0) {
    stopMonitoring()
    qrError.value ||= 'This QR has expired. Check the order status before starting another payment.'
    return
  }
  if (reschedule) pollTimeout = setTimeout(poll, 5000)
}

function onSuccess() {
  if (paymentApproved.value) return
  paymentApproved.value = true
  stopMonitoring()
  successTimeout = setTimeout(() => {
    emit('approved', { orderNumber: props.orderNumber, amount: props.amount, paid: true })
  }, 1000)
}

function openAbaLink() {
  if (paywayUrl.value) {
    if (paywayUrl.value.startsWith('http')) {
      window.open(paywayUrl.value, '_blank')
    } else {
      window.location.assign(paywayUrl.value)
    }
  }
}

async function copyPaymentLink() {
  if (!paywayUrl.value) return
  try {
    await navigator.clipboard.writeText(paywayUrl.value)
    copiedPaymentLink.value = true
    clearTimeout(copyTimeout)
    copyTimeout = setTimeout(() => { copiedPaymentLink.value = false }, 2500)
  } catch {
    copiedPaymentLink.value = false
  }
}

async function handleClose() {
  if (paymentApproved.value || closing.value) return
  if (reviewRequired.value) {
    emit('cancelled', { closed: false, message: qrError.value })
    return
  }
  closing.value = true
  stopMonitoring()
  try {
    const { data } = await axios.post('/api/payments/khqr/cancel', { order_number: props.orderNumber }, request)
    if (!controller.signal.aborted) applyStatus(data)
  } catch (error) {
    if (controller.signal.aborted) return
    qrError.value = message(error, 'Cancellation could not be confirmed. Check the order before paying again.')
    closing.value = false
    await poll(false)
  } finally {
    closing.value = false
  }
}
</script>

<style scoped>
/* Backdrop */
.khqr-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(8, 27, 55, 0.65);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
  overflow-y: auto;
}

/* Modal Container */
.khqr-modal-container {
  width: min(100%, 380px);
  margin: auto;
  padding: 24px;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 16px 48px rgba(8, 27, 55, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  box-sizing: border-box;
}

/* Top bar with Heading & Timer */
.khqr-modal-top-bar {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.khqr-modal-heading {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #081b37;
}

.khqr-timer-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
  color: #081b37;
  font-variant-numeric: tabular-nums;
}

.timer-dot {
  width: 8px;
  height: 8px;
  background: #0bbcd4;
  border-radius: 50%;
  animation: pulseDot 1.5s infinite;
}

/* ============================================================
   EXACT SPECIFICATIONS FROM checkout.html (.khqr-content)
   width: 273px, height: 396px, border-radius: 22px
   ============================================================ */
.khqr-content {
  border-radius: 22px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  height: 396px;
  width: 273px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

/* Top Red Banner (height: 47.52px, background: #e21a1a) */
.khqr-banner {
  background: #e21a1a;
  border-top-left-radius: 22px;
  border-top-right-radius: 22px;
  height: 47.52px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Official Triangle Ribbon Cut */
.triangle-row {
  display: flex;
  justify-content: flex-end;
  height: 0;
}

.triangle-top-right {
  border-left: 22.86px solid transparent;
  border-top: 22.86px solid #e21a1a;
  height: 0;
  width: 0;
}

/* Merchant Info & Amount */
.merc-khqr-info {
  padding: 8px 16px 4px;
  text-align: left;
}

.merc-name {
  font-size: 11px;
  color: #737373;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.total-amount-khqr {
  margin-top: 4px;
}

.amount-value {
  font-size: 21px;
  font-weight: 700;
  color: #171717;
  position: relative;
  display: inline-flex;
  align-items: baseline;
  gap: 6px;
}

.amount-currency {
  font-size: 10px;
  font-weight: 400;
  color: #525252;
}

/* Line Divider (from checkout.html) */
.line-divider {
  height: 2px;
  width: 100%;
  margin-top: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.line-divider svg {
  display: block;
  width: 100%;
}

/* QR Code Canvas Area */
.qr-canvas-box {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 8px;
  overflow: hidden;
}

.qr-canvas-holder {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-canvas-element {
  display: block !important;
  width: 200px !important;
  height: 200px !important;
  max-width: 100% !important;
  max-height: 100% !important;
  border-radius: 4px;
  object-fit: contain;
}

/* Center USD Emblem */
.usd-khqr-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 32px;
  height: 32px;
  background: #ffffff;
  border: 2px solid #e21a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  pointer-events: none;
}

.badge-dollar {
  color: #e21a1a;
  font-weight: 900;
  font-size: 14px;
  line-height: 1;
}

/* States */
.khqr-state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #666;
  text-align: center;
}

.status-success strong {
  color: #16a34a;
  font-size: 14px;
}

.status-err p {
  color: #dc2626;
  font-size: 12px;
  margin: 0;
}

.btn-retry-khqr {
  background: #081b37;
  color: #fff;
  border: none;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.khqr-spinner {
  width: 26px;
  height: 26px;
  border: 3px solid #e2e8f0;
  border-top-color: #e21a1a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Description from checkout.html */
.khqr-text-desc {
  font-size: 13px;
  line-height: 1.4;
  color: #555555;
  text-align: center;
  max-width: 273px;
  margin: 16px 0 14px;
}

/* Actions */
.khqr-button-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  flex-wrap: wrap;
}

.btn-khqr-close, .btn-khqr-copy, .btn-khqr-aba {
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-khqr-close {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #334155;
}

.btn-khqr-close:hover {
  background: #e2e8f0;
}

.btn-khqr-aba {
  background: #005d7b;
  border: none;
  color: #ffffff;
}

.btn-khqr-aba:hover {
  background: #004d66;
}

.btn-khqr-copy {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
}

.btn-khqr-copy:hover {
  background: #f8fafc;
}

.btn-copy-inner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.btn-demo-sim {
  margin-top: 12px;
  width: 100%;
  padding: 8px 12px;
  background: #fffbeb;
  border: 1px solid #fcd34d;
  color: #92400e;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
}

.demo-btn-inner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-demo-sim:hover:not(:disabled) {
  background: #fef3c7;
}

.btn-demo-sim:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulseDot {
  0% { transform: scale(0.9); opacity: 0.7; }
  50% { transform: scale(1.15); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.7; }
}

@media (max-width: 480px) {
  .khqr-modal-backdrop {
    padding: 10px 8px;
  }
  .khqr-modal-container {
    padding: 16px 12px;
    max-width: calc(100vw - 16px);
    max-height: 94vh;
    overflow-y: auto;
  }
}

@media (max-width: 360px) {
  .khqr-modal-backdrop {
    padding: 6px;
  }
  .khqr-modal-container {
    padding: 12px 8px;
    border-radius: 18px;
    max-width: calc(100vw - 12px);
  }
  .khqr-content {
    width: 260px;
    height: 380px;
    border-radius: 18px;
  }
  .qr-canvas-holder {
    width: 180px;
    height: 180px;
  }
  .qr-canvas-element {
    width: 180px !important;
    height: 180px !important;
  }
}
</style>
