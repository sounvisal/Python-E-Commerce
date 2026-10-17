<template>
  <div class="lumea-return-wizard-page">
    <div class="container wizard-container">
      <!-- Breadcrumb Navigation -->
      <nav class="wizard-breadcrumb" aria-label="Breadcrumb">
        <router-link to="/">Home</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/returns">Returns &amp; Refunds</router-link>
        <span class="sep">&rsaquo;</span>
        <span class="cur-crumb">Request a Return</span>
      </nav>

      <!-- Page Header with Quote Box matching Screen #1 -->
      <header class="wizard-header-row">
        <div class="header-text-col">
          <h1 class="wizard-main-title">Request a Return or Refund</h1>
          <p class="wizard-subtitle">
            Let's make it right. Simply follow the steps below to submit your return request.
          </p>
        </div>

        <div class="header-quote-col">
          <div class="quote-box-frame">
            <img
              src="/images/returns-workflow-box1.jpg"
              alt="Good Skin Brighter Days - Luméa"
              class="quote-box-img"
            />
          </div>
        </div>
      </header>

      <!-- 5-Step Visual Stepper Bar -->
      <div class="wizard-stepper-bar">
        <div
          v-for="(st, idx) in steps"
          :key="st.num"
          class="stepper-node"
          :class="{
            'is-active': currentStep === st.num,
            'is-completed': currentStep > st.num
          }"
          @click="canNavigateTo(st.num) && (currentStep = st.num)"
        >
          <div class="step-circle">
            <span v-if="currentStep <= st.num">{{ st.num }}</span>
            <Check v-else :size="14" />
          </div>
          <span class="step-label">{{ st.label }}</span>
          <div v-if="idx < steps.length - 1" class="step-connector"></div>
        </div>
      </div>

      <!-- Main Layout: Form Steps (Left) + Atelier Value Card (Right) -->
      <div class="wizard-layout-grid">
        <!-- Left: Form Steps Container -->
        <div class="wizard-form-col">
          <form @submit.prevent="handleNextOrSubmit" class="wizard-form-card">
            <!-- Step 1: Select Order and Item -->
            <div v-show="currentStep === 1" class="step-pane">
              <div class="step-section-header">
                <div>
                  <h3 class="step-title">1. Select Order and Item</h3>
                  <p class="step-subtitle">Choose the order and item you'd like to return.</p>
                </div>
                <router-link to="/contact" class="cant-find-link">
                  Can't find your order? Contact us &rarr;
                </router-link>
              </div>

              <!-- Order Selector Dropdown -->
              <div class="order-select-box">
                <label class="field-label">Delivered Order</label>
                <div class="custom-select-wrap">
                  <select v-model="selectedOrderNumber" class="order-dropdown">
                    <option value="LM24081234">Order #LM24081234 &bull; Aug 12, 2024 &bull; 2 items &bull; Delivered</option>
                    <option value="LM-072646">Order #LM-072646 &bull; Oct 14, 2026 &bull; 2 items &bull; Delivered</option>
                  </select>
                  <ChevronDown :size="16" class="dropdown-chevron" />
                </div>
              </div>

              <!-- Items in Order Checkboxes -->
              <div class="order-items-list">
                <label
                  v-for="item in availableItems"
                  :key="item.id"
                  class="item-select-row"
                  :class="{ 'is-selected': selectedItemId === item.id }"
                >
                  <input
                    type="radio"
                    name="returnItem"
                    :value="item.id"
                    v-model="selectedItemId"
                    class="item-radio"
                  />
                  <img :src="item.image" :alt="item.name" class="item-thumb-img" />
                  <div class="item-text-info">
                    <h5 class="item-name">{{ item.name }}</h5>
                    <span class="item-variant">{{ item.variant }}</span>
                  </div>
                  <div class="item-price-tag">
                    ${{ item.price.toFixed(2) }}
                  </div>
                </label>
              </div>

              <div class="step-footer-actions">
                <button type="button" @click="currentStep = 2" class="btn-step-next" :disabled="!selectedItemId">
                  Next: Select Reason &rarr;
                </button>
              </div>
            </div>

            <!-- Step 2: Reason for Return -->
            <div v-show="currentStep === 2" class="step-pane">
              <div class="step-section-header">
                <div>
                  <h3 class="step-title">2. What's the reason for your return?</h3>
                  <p class="step-subtitle">Please tell us why you're returning this item.</p>
                </div>
              </div>

              <div class="reasons-radio-grid">
                <label
                  v-for="r in reasonsList"
                  :key="r"
                  class="reason-radio-card"
                  :class="{ 'is-checked': selectedReason === r }"
                >
                  <input
                    type="radio"
                    name="returnReason"
                    :value="r"
                    v-model="selectedReason"
                    class="radio-input"
                  />
                  <span class="custom-radio-mark"></span>
                  <span class="reason-text">{{ r }}</span>
                </label>
              </div>

              <div class="step-footer-actions dual">
                <button type="button" @click="currentStep = 1" class="btn-step-back">&larr; Back</button>
                <button type="button" @click="currentStep = 3" class="btn-step-next" :disabled="!selectedReason">
                  Next: Choose Resolution &rarr;
                </button>
              </div>
            </div>

            <!-- Step 3: Desired Resolution -->
            <div v-show="currentStep === 3" class="step-pane">
              <div class="step-section-header">
                <div>
                  <h3 class="step-title">3. What would you like?</h3>
                  <p class="step-subtitle">Choose how you'd like us to resolve this.</p>
                </div>
              </div>

              <div class="resolutions-list">
                <label
                  v-for="res in resolutionsList"
                  :key="res.title"
                  class="resolution-card"
                  :class="{ 'is-checked': selectedResolution === res.title }"
                >
                  <input
                    type="radio"
                    name="resolution"
                    :value="res.title"
                    v-model="selectedResolution"
                    class="radio-input"
                  />
                  <span class="custom-radio-mark"></span>
                  <div class="res-text-group">
                    <h5 class="res-title">{{ res.title }}</h5>
                    <p class="res-desc">{{ res.desc }}</p>
                  </div>
                </label>
              </div>

              <!-- Need Help Choosing Callout -->
              <div class="need-help-callout">
                <Leaf :size="20" class="callout-icon" />
                <div class="callout-text">
                  <h5>Need help choosing?</h5>
                  <p>If you're unsure, our customer care team is here to help.</p>
                </div>
                <router-link to="/contact" class="callout-contact-link">Contact Us &rarr;</router-link>
              </div>

              <div class="step-footer-actions dual">
                <button type="button" @click="currentStep = 2" class="btn-step-back">&larr; Back</button>
                <button type="button" @click="currentStep = 4" class="btn-step-next">
                  Next: Add Details &rarr;
                </button>
              </div>
            </div>

            <!-- Step 4: Details & Photo Attachments -->
            <div v-show="currentStep === 4" class="step-pane">
              <div class="step-section-header">
                <div>
                  <h3 class="step-title">4. Describe the Issue &amp; Upload Photos</h3>
                  <p class="step-subtitle">Please share additional details to expedite processing.</p>
                </div>
              </div>

              <div class="form-group-field">
                <label class="field-label">Description of Issue</label>
                <textarea
                  v-model="returnDescription"
                  rows="4"
                  class="details-textarea"
                  placeholder="e.g. The bottle arrived with a crack and some product leaked..."
                ></textarea>
              </div>

              <div class="photos-upload-group">
                <label class="field-label">Proof Photos (Optional)</label>
                <div class="photos-preview-row">
                  <div class="photo-preview-box" v-for="(photo, pidx) in uploadedPhotos" :key="pidx">
                    <img :src="photo" alt="Uploaded photo" class="preview-thumb" />
                  </div>
                  <label class="photo-add-box">
                    <Upload :size="20" />
                    <span>{{ isUploadingPhoto ? 'Uploading...' : 'Upload Photo' }}</span>
                    <input type="file" accept="image/*" class="file-hidden-input" @change="handlePhotoUpload" />
                  </label>
                </div>
                <span class="file-hint">JPG, PNG up to 10MB per image</span>
              </div>

              <div class="step-footer-actions dual">
                <button type="button" @click="currentStep = 3" class="btn-step-back">&larr; Back</button>
                <button type="button" @click="currentStep = 5" class="btn-step-next">
                  Next: Review &rarr;
                </button>
              </div>
            </div>

            <!-- Step 5: Review & Submit -->
            <div v-show="currentStep === 5" class="step-pane">
              <div class="step-section-header">
                <div>
                  <h3 class="step-title">5. Review &amp; Submit Request</h3>
                  <p class="step-subtitle">Please confirm the details below before submitting.</p>
                </div>
              </div>

              <div class="review-summary-card">
                <div class="review-row">
                  <span class="r-label">Order Number:</span>
                  <span class="r-value">#{{ selectedOrderNumber }}</span>
                </div>
                <div class="review-row">
                  <span class="r-label">Product to Return:</span>
                  <span class="r-value font-medium">{{ currentSelectedItem?.name }} ({{ currentSelectedItem?.variant }})</span>
                </div>
                <div class="review-row">
                  <span class="r-label">Item Value:</span>
                  <span class="r-value">${{ currentSelectedItem?.price.toFixed(2) }}</span>
                </div>
                <div class="review-row">
                  <span class="r-label">Reason:</span>
                  <span class="r-value">{{ selectedReason }}</span>
                </div>
                <div class="review-row">
                  <span class="r-label">Requested Resolution:</span>
                  <span class="r-value font-medium text-crimson">{{ selectedResolution }}</span>
                </div>
                <div v-if="returnDescription" class="review-row">
                  <span class="r-label">Notes:</span>
                  <span class="r-value">{{ returnDescription }}</span>
                </div>
              </div>

              <div class="step-footer-actions dual">
                <button type="button" @click="currentStep = 4" class="btn-step-back">&larr; Back</button>
                <button type="submit" class="btn-submit-return" :disabled="isSubmitting">
                  <span v-if="!isSubmitting">Submit Return Request &rarr;</span>
                  <span v-else>Submitting to Atelier...</span>
                </button>
              </div>
            </div>
          </form>
        </div>

        <!-- Right: Atelier Trust & Promise Sidebar matching Format -->
        <aside class="wizard-sidebar-col">
          <div class="atelier-promise-card">
            <div class="promise-image-frame">
              <img
                src="/images/returns-workflow-bottles.jpg"
                alt="A Smoother Return Experience"
                class="promise-bottles-img"
              />
            </div>

            <div class="promise-body">
              <h3 class="promise-title">A Smoother Return Experience.</h3>
              <p class="promise-desc">
                We handle every return with care, so you can shop with confidence again.
              </p>

              <div class="promise-features-list">
                <div class="promise-feature-item">
                  <div class="feat-icon-col">
                    <ShieldCheck :size="18" class="feat-icon" />
                  </div>
                  <div class="feat-text-col">
                    <h5>Hassle-Free</h5>
                    <p>A simple and clear process.</p>
                  </div>
                </div>

                <div class="promise-feature-item">
                  <div class="feat-icon-col">
                    <Package :size="18" class="feat-icon" />
                  </div>
                  <div class="feat-text-col">
                    <h5>Fair &amp; Transparent</h5>
                    <p>Quick refunds, no hidden fees.</p>
                  </div>
                </div>

                <div class="promise-feature-item">
                  <div class="feat-icon-col">
                    <HeartHandshake :size="18" class="feat-icon" />
                  </div>
                  <div class="feat-text-col">
                    <h5>Here to Help</h5>
                    <p>Our team is always ready to support you.</p>
                  </div>
                </div>
              </div>

              <div class="promise-cursive-footer">
                <span class="cursive-tag">A Kinder Shopping Experience.</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Check,
  ChevronDown,
  Leaf,
  Upload,
  ShieldCheck,
  Package,
  HeartHandshake
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

const steps = [
  { num: 1, label: 'Select Item' },
  { num: 2, label: 'Reason' },
  { num: 3, label: 'Resolution' },
  { num: 4, label: 'Details' },
  { num: 5, label: 'Review' }
]

const currentStep = ref(1)

const selectedOrderNumber = ref(route.query.order ? String(route.query.order) : 'LM24081234')
const selectedItemId = ref(1)
const uploadedPhotos = ref(['/images/returns-workflow-bottles.jpg'])
const isUploadingPhoto = ref(false)

const availableItems = ref([
  {
    id: 1,
    name: 'SK-II Facial Treatment Essence',
    variant: '230ml',
    price: 125.0,
    image: '/images/prod-sk2.jpg'
  },
  {
    id: 2,
    name: 'The Ordinary Niacinamide 10% + Zinc 1%',
    variant: '30ml',
    price: 12.0,
    image: '/images/prod-ordinary.jpg'
  }
])

const reasonsList = [
  'Product is damaged',
  'I changed my mind',
  'Wrong product received',
  'Experienced an allergic reaction',
  'Product is missing',
  'The product didn\'t work for me',
  'Product doesn\'t match description',
  'Other (please specify)'
]

const selectedReason = ref('Product is damaged')

const resolutionsList = [
  {
    title: 'Refund to original payment method',
    desc: 'Funds returned to your credit card or payment account within 3-5 business days.'
  },
  {
    title: 'Exchange for the same product',
    desc: 'We will ship a fresh, inspected replacement bottle immediately.'
  },
  {
    title: 'Replacement (same product)',
    desc: 'Receive immediate Luméa Atelier store credit with bonus loyalty points.'
  }
]

const selectedResolution = ref('Refund to original payment method')
const returnDescription = ref('The bottle arrived with a crack and some product leaked. Please see the attached photos.')
const isSubmitting = ref(false)

const currentSelectedItem = computed(() => {
  return availableItems.value.find(i => i.id === selectedItemId.value) || availableItems.value[0]
})

function canNavigateTo(stepNum) {
  if (stepNum === 1) return true
  if (stepNum === 2) return Boolean(selectedItemId.value)
  if (stepNum === 3) return Boolean(selectedReason.value)
  if (stepNum === 4) return Boolean(selectedResolution.value)
  if (stepNum === 5) return Boolean(selectedResolution.value)
  return false
}

async function handlePhotoUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  isUploadingPhoto.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      const data = await res.json()
      if (data.data?.url) {
        uploadedPhotos.value.unshift(data.data.url)
      }
    }
  } catch (err) {
    console.error('Failed to upload proof photo:', err)
  } finally {
    isUploadingPhoto.value = false
  }
}

async function handleNextOrSubmit() {
  if (currentStep.value < 5) {
    currentStep.value++
    return
  }

  // Submit to FastAPI backend: POST /api/returns
  isSubmitting.value = true
  try {
    const payload = {
      order_number: selectedOrderNumber.value,
      product_name: currentSelectedItem.value.name,
      product_image: currentSelectedItem.value.image,
      product_variant: currentSelectedItem.value.variant,
      price: currentSelectedItem.value.price,
      quantity: 1,
      reason: selectedReason.value,
      resolution: selectedResolution.value,
      description: returnDescription.value,
      photos: uploadedPhotos.value,
      customer_name: 'Sreynich Chan',
      customer_email: 'sreynich.chan@example.com'
    }

    const res = await fetch('/api/returns', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      const created = await res.json()
      router.push(`/returns/status/${created.request_number}`)
    } else {
      // Fallback redirect to sample
      router.push('/returns/status/RR24081234')
    }
  } catch (err) {
    console.error('[ReturnWizard] Error submitting return:', err)
    router.push('/returns/status/RR24081234')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.lumea-return-wizard-page {
  background: #FCFAF7;
  min-height: 100vh;
  padding: 2rem 0 6rem;
  color: #1C1917;
}

.wizard-container {
  max-width: 1280px;
}

/* Breadcrumbs */
.wizard-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  color: #78716C;
  margin-bottom: 2rem;
}

.wizard-breadcrumb a {
  color: #78716C;
  text-decoration: none;
}

.wizard-breadcrumb a:hover {
  color: #7A2E22;
}

.sep {
  color: #A8A29E;
}

.cur-crumb {
  color: #1C1917;
  font-weight: 500;
}

/* Header Row */
.wizard-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.wizard-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 3.5vw, 2.8rem);
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
}

.wizard-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #57534E;
  margin: 0;
}

.quote-box-frame {
  max-width: 280px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.quote-box-img {
  width: 100%;
  height: 110px;
  object-fit: cover;
  display: block;
}

/* 5-Step Stepper Bar */
.wizard-stepper-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1rem 2rem;
  margin-bottom: 2.5rem;
}

.stepper-node {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
  cursor: pointer;
  flex: 1;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F5EFEB;
  border: 1px solid #D6D3D1;
  color: #78716C;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.stepper-node.is-active .step-circle {
  background: #7A2E22;
  border-color: #7A2E22;
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(122, 46, 34, 0.25);
}

.stepper-node.is-completed .step-circle {
  background: #7A2E22;
  border-color: #7A2E22;
  color: #FFFFFF;
}

.step-label {
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
  color: #78716C;
}

.stepper-node.is-active .step-label {
  color: #7A2E22;
  font-weight: 600;
}

.step-connector {
  flex: 1;
  height: 2px;
  background: #E7E5E4;
  margin: 0 1rem;
}

.stepper-node.is-completed .step-connector {
  background: #7A2E22;
}

/* Layout Grid */
.wizard-layout-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2.5rem;
  align-items: start;
}

/* Form Card */
.wizard-form-card {
  background: #FFFFFF;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 10px;
  padding: 2.25rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
}

.step-section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding-bottom: 1.25rem;
  margin-bottom: 1.75rem;
}

.step-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.45rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.35rem;
}

.step-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  color: #57534E;
  margin: 0;
}

.cant-find-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
}

/* Order Select */
.order-select-box {
  margin-bottom: 1.5rem;
}

.field-label {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #44403C;
  margin-bottom: 0.5rem;
}

.custom-select-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.order-dropdown {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 1px solid #D6D3D1;
  border-radius: 6px;
  background: #FAF9F6;
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  color: #1C1917;
  outline: none;
  appearance: none;
  cursor: pointer;
}

.dropdown-chevron {
  position: absolute;
  right: 1rem;
  pointer-events: none;
  color: #78716C;
}

/* Order Items Radio List */
.order-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin-bottom: 2rem;
}

.item-select-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1.5px solid #E7E5E4;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
}

.item-select-row:hover {
  border-color: #7A2E22;
}

.item-select-row.is-selected {
  border-color: #7A2E22;
  background: #FFFBF8;
}

.item-radio {
  accent-color: #7A2E22;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.item-thumb-img {
  width: 52px;
  height: 52px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

.item-text-info {
  flex: 1;
}

.item-name {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.2rem;
}

.item-variant {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #78716C;
}

.item-price-tag {
  font-family: 'Inter', sans-serif;
  font-size: 0.92rem;
  font-weight: 600;
  color: #1C1917;
}

/* Reasons Grid */
.reasons-radio-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.reason-radio-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid #E7E5E4;
  border-radius: 6px;
  padding: 0.85rem 1rem;
  cursor: pointer;
  transition: all 0.2s;
  background: #FAF9F6;
}

.reason-radio-card:hover {
  border-color: #7A2E22;
}

.reason-radio-card.is-checked {
  border-color: #7A2E22;
  background: #FFF8F6;
}

.radio-input {
  accent-color: #7A2E22;
  cursor: pointer;
}

.reason-text {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #292524;
}

/* Resolutions List */
.resolutions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.resolution-card {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  border: 1px solid #E7E5E4;
  border-radius: 8px;
  padding: 1.25rem;
  cursor: pointer;
  background: #FAF9F6;
  transition: all 0.2s;
}

.resolution-card:hover {
  border-color: #7A2E22;
}

.resolution-card.is-checked {
  border-color: #7A2E22;
  background: #FFF8F6;
}

.res-text-group {
  flex: 1;
}

.res-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.25rem;
}

.res-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  color: #57534E;
  margin: 0;
  line-height: 1.4;
}

/* Need Help Callout */
.need-help-callout {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #F5EFEB;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 2rem;
}

.callout-icon {
  color: #7A2E22;
  flex-shrink: 0;
}

.callout-text h5 {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.15rem;
}

.callout-text p {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #57534E;
  margin: 0;
}

.callout-contact-link {
  margin-left: auto;
  font-family: 'Inter', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
  white-space: nowrap;
}

/* Details Step */
.details-textarea {
  width: 100%;
  padding: 0.85rem;
  border: 1px solid #D6D3D1;
  border-radius: 6px;
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
  color: #1C1917;
  outline: none;
  margin-bottom: 1.5rem;
}

.details-textarea:focus {
  border-color: #7A2E22;
}

.photos-preview-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.photo-preview-box {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #D6D3D1;
}

.preview-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-add-box {
  width: 80px;
  height: 80px;
  border: 1.5px dashed #7A2E22;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  color: #7A2E22;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 0.65rem;
  text-align: center;
}

.file-hidden-input {
  display: none;
}

.file-hint {
  font-family: 'Inter', sans-serif;
  font-size: 0.72rem;
  color: #78716C;
}

/* Step 5 Review */
.review-summary-card {
  background: #FAF7F2;
  border: 1px solid rgba(122, 46, 34, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.review-row {
  display: flex;
  justify-content: space-between;
  font-family: 'Inter', sans-serif;
  font-size: 0.86rem;
}

.r-label {
  color: #78716C;
}

.r-value {
  color: #1C1917;
  text-align: right;
}

.font-medium {
  font-weight: 600;
}

.text-crimson {
  color: #7A2E22;
}

/* Action Buttons */
.step-footer-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.step-footer-actions.dual {
  justify-content: space-between;
}

.btn-step-next {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  font-weight: 500;
  padding: 0.75rem 1.6rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-step-next:hover:not(:disabled) {
  background: #5E2117;
}

.btn-step-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-step-back {
  background: transparent;
  color: #57534E;
  border: 1px solid #D6D3D1;
  font-family: 'Inter', sans-serif;
  font-size: 0.85rem;
  padding: 0.7rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit-return {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  padding: 0.8rem 1.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit-return:hover:not(:disabled) {
  background: #5E2117;
  transform: translateY(-1px);
}

/* Right Sidebar: Atelier Promise Card */
.atelier-promise-card {
  background: #FFFBF8;
  border: 1px solid rgba(122, 46, 34, 0.12);
  border-radius: 10px;
  overflow: hidden;
}

.promise-image-frame {
  height: 180px;
}

.promise-bottles-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.promise-body {
  padding: 1.75rem 1.5rem;
}

.promise-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: #7A2E22;
  margin: 0 0 0.5rem;
}

.promise-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.84rem;
  color: #57534E;
  line-height: 1.5;
  margin: 0 0 1.5rem;
}

.promise-features-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.promise-feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.feat-icon-col {
  color: #7A2E22;
  margin-top: 0.15rem;
}

.feat-text-col h5 {
  font-family: 'Inter', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  color: #1C1917;
  margin: 0 0 0.15rem;
}

.feat-text-col p {
  font-family: 'Inter', sans-serif;
  font-size: 0.78rem;
  color: #78716C;
  margin: 0;
}

.promise-cursive-footer {
  text-align: center;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(122, 46, 34, 0.1);
}

.cursive-tag {
  font-family: 'Playfair Display', Georgia, cursive, serif;
  font-style: italic;
  font-size: 1.15rem;
  color: #8C4334;
}

/* Responsive */
@media (max-width: 992px) {
  .wizard-layout-grid {
    grid-template-columns: 1fr;
  }
  .reasons-radio-grid {
    grid-template-columns: 1fr;
  }
}
</style>
