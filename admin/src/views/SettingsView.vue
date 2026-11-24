<script setup>
import { ref, reactive, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
import { useAuthStore } from '@/stores/auth'
import { getStorefrontUrl } from '@/utils/storefront'
import {
  Settings as SettingsIcon,
  Store,
  CreditCard,
  Truck,
  Receipt,
  Bell,
  Users,
  Grid,
  Search,
  Palette,
  FileText,
  Cpu,
  RotateCcw,
  Save,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  Lightbulb,
  Database,
  RefreshCw,
  Download,
  Upload,
  Trash2,
  Image as ImageIcon,
  ArrowRight,
  ShieldCheck,
  Globe,
  Sliders,
  ChevronDown,
  Sparkles
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// Active tab
const activeTab = ref('general')
const isSaving = ref(false)
const isClearingCache = ref(false)

// Navigation Tabs
const tabs = [
  { id: 'general', name: 'General', desc: 'Store information and basic settings', icon: SettingsIcon },
  { id: 'store_settings', name: 'Store Settings', desc: 'Store details, contact, currency', icon: Store },
  { id: 'payments', name: 'Payments', desc: 'Payment gateways and methods', icon: CreditCard },
  { id: 'shipping', name: 'Shipping', desc: 'Shipping methods and rates', icon: Truck },
  { id: 'taxes', name: 'Taxes', desc: 'Tax rates and rules', icon: Receipt },
  { id: 'notifications', name: 'Notifications', desc: 'Email and system notifications', icon: Bell },
  { id: 'users', name: 'Users & Permissions', desc: 'Manage team members', icon: Users },
  { id: 'integrations', name: 'Integrations', desc: 'Third-party apps and services', icon: Grid },
  { id: 'seo', name: 'SEO', desc: 'Search engine optimization', icon: Search },
  { id: 'appearance', name: 'Appearance', desc: 'Theme and visual settings', icon: Palette },
  { id: 'legal', name: 'Legal & Policies', desc: 'Terms, privacy, and policies', icon: FileText },
  { id: 'advanced', name: 'Advanced', desc: 'Developer and system settings', icon: Cpu }
]

// General Form Settings matching exact mockup
const form = reactive({
  store_name: 'Luméa',
  store_email: 'support@lumea.com',
  store_phone: '12 345 678',
  phone_country_code: '+855',
  store_language: 'English (Default)',
  store_description: 'Premium skincare for a healthier, brighter you. Natural beauty, real results.',
  company_name: 'Luméa Co., Ltd.',
  business_reg_number: 'KH-123456789',
  business_address: '#123, Norodom Blvd, Phnom Penh, Cambodia',
  time_zone: '(UTC+07:00) Phnom Penh',
  currency: 'USD ($)',
  free_shipping_enabled: true,
  free_shipping_mode: 'threshold', // 'threshold' | 'all_orders' | 'disabled'
  free_shipping_threshold: 50.0,
  free_shipping_promo_text: 'Complimentary nationwide shipping on orders over $50',
  free_shipping_carriers: ['vet_express', 'jt_express', 'lumea_concierge'],
  grab_subsidy_enabled: true,
  tax_rate: 10.0,
  online_status: 'Online',
  store_logo: '',
  store_favicon: ''
})

const staffMembers = ref([
  { id: 1, name: 'Sreynich Chan', email: 'sreynich.chan@example.com', role: 'Super Admin · Full Access', avatar: '/images/avatar-sreynich.jpg', status: 'Active' },
  { id: 2, name: 'Luméa Operations', email: 'ops@lumea.com', role: 'Store Manager', avatar: '/images/avatars/avatar-default.png', status: 'Active' },
])

const uploadStatus = ref({
  enabled: null,
  storage_type: 'unknown',
  max_image_mb: 0,
  max_video_mb: 0,
  allowed_formats: []
})

async function loadUploadStatus() {
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    uploadStatus.value = { enabled: false, storage_type: 'unknown', max_image_mb: 0, max_video_mb: 0, allowed_formats: [] }
    return
  }
  try {
    const res = await apiClient.get('/upload/status')
    if (res.data?.status === 'success' && res.data.data) {
      uploadStatus.value = res.data.data
    } else {
      uploadStatus.value = { enabled: false, storage_type: 'unknown', max_image_mb: 0, max_video_mb: 0, allowed_formats: [] }
    }
  } catch (err) {
    console.warn('Could not load upload status:', err)
    uploadStatus.value = { enabled: false, storage_type: 'unknown', max_image_mb: 0, max_video_mb: 0, allowed_formats: [] }
  }
}

// Load settings from backend API
onMounted(async () => {
  await Promise.all([loadSettings(), loadUploadStatus()])
})

async function loadSettings() {
  try {
    const res = await apiClient.get('/admin/settings')
    if (res.data?.status === 'success' && res.data.data) {
      const d = res.data.data
      form.store_name = d.store_name || form.store_name
      form.store_email = d.store_email || form.store_email
      form.store_phone = d.store_phone ? d.store_phone.replace('+855 ', '') : form.store_phone
      form.store_language = d.store_language || form.store_language
      form.store_description = d.store_description || form.store_description
      form.company_name = d.company_name || form.company_name
      form.business_reg_number = d.business_reg_number || form.business_reg_number
      form.business_address = d.business_address || form.business_address
      form.time_zone = d.time_zone || form.time_zone
      form.currency = d.currency || form.currency
      form.free_shipping_enabled = d.free_shipping_enabled ?? form.free_shipping_enabled
      form.free_shipping_mode = d.free_shipping_mode || form.free_shipping_mode
      form.free_shipping_threshold = d.free_shipping_threshold ?? form.free_shipping_threshold
      form.free_shipping_promo_text = d.free_shipping_promo_text || form.free_shipping_promo_text
      form.free_shipping_carriers = d.free_shipping_carriers || form.free_shipping_carriers
      form.grab_subsidy_enabled = d.grab_subsidy_enabled ?? form.grab_subsidy_enabled
      form.tax_rate = d.tax_rate ?? form.tax_rate
      form.online_status = d.online_status || form.online_status
      form.store_logo = d.store_logo || ''
      form.store_favicon = d.store_favicon || ''
    }
  } catch (err) {
    console.error('Failed to load settings:', err)
  }
}

// Save Settings to Backend API
async function saveSettings() {
  isSaving.value = true
  try {
    const payload = {
      store_name: form.store_name,
      store_email: form.store_email,
      store_phone: `${form.phone_country_code} ${form.store_phone}`,
      store_language: form.store_language,
      store_description: form.store_description,
      store_logo: form.store_logo,
      store_favicon: form.store_favicon,
      company_name: form.company_name,
      business_reg_number: form.business_reg_number,
      business_address: form.business_address,
      time_zone: form.time_zone,
      currency: form.currency,
      free_shipping_enabled: form.free_shipping_enabled,
      free_shipping_mode: form.free_shipping_mode,
      free_shipping_threshold: form.free_shipping_threshold,
      free_shipping_promo_text: form.free_shipping_promo_text,
      free_shipping_carriers: form.free_shipping_carriers,
      grab_subsidy_enabled: form.grab_subsidy_enabled,
      tax_rate: form.tax_rate,
      online_status: form.online_status
    }
    const res = await apiClient.put('/admin/settings', payload)
    if (res.data?.status === 'success') {
      adminStore.addToast('Settings saved and persisted to database successfully', 'success')
    }
  } catch (err) {
    adminStore.addToast('Failed to save settings', 'error')
  } finally {
    isSaving.value = false
  }
}

// Reset Settings
function resetSettings() {
  form.store_name = 'Luméa'
  form.store_email = 'support@lumea.com'
  form.store_phone = '12 345 678'
  form.phone_country_code = '+855'
  form.store_language = 'English (Default)'
  form.store_description = 'Premium skincare for a healthier, brighter you. Natural beauty, real results.'
  form.company_name = 'Luméa Co., Ltd.'
  form.business_reg_number = 'KH-123456789'
  form.business_address = '#123, Norodom Blvd, Phnom Penh, Cambodia'
  form.time_zone = '(UTC+07:00) Phnom Penh'
  adminStore.addToast('Settings reset to default atelier values', 'info')
}

// Free Delivery & Shipping Controls
function onToggleFreeShipping() {
  if (form.free_shipping_enabled && form.free_shipping_mode === 'disabled') {
    form.free_shipping_mode = 'threshold'
  }
}

function setPromoMode(mode) {
  form.free_shipping_mode = mode
  if (mode === 'all_orders') {
    form.free_shipping_enabled = true
    form.free_shipping_promo_text = 'Atelier Special: Complimentary Free Delivery on All Orders!'
  } else if (mode === 'threshold') {
    form.free_shipping_enabled = true
    if (!form.free_shipping_promo_text || form.free_shipping_promo_text.includes('All Orders')) {
      form.free_shipping_promo_text = `Complimentary nationwide shipping on orders over $${form.free_shipping_threshold}`
    }
  } else if (mode === 'disabled') {
    form.free_shipping_enabled = false
  }
}

function toggleCarrierEligibility(carrierId) {
  const list = form.free_shipping_carriers || []
  const idx = list.indexOf(carrierId)
  if (idx >= 0) {
    list.splice(idx, 1)
  } else {
    list.push(carrierId)
  }
  form.free_shipping_carriers = [...list]
}

function applyPromoPreset(text, threshold = null) {
  form.free_shipping_promo_text = text
  if (threshold !== null) {
    form.free_shipping_threshold = threshold
    if (threshold === 0) {
      form.free_shipping_mode = 'all_orders'
      form.free_shipping_enabled = true
    } else {
      form.free_shipping_mode = 'threshold'
      form.free_shipping_enabled = true
    }
  }
}

function resetShippingSettings() {
  form.free_shipping_enabled = true
  form.free_shipping_mode = 'threshold'
  form.free_shipping_threshold = 50.0
  form.free_shipping_promo_text = 'Complimentary nationwide shipping on orders over $50'
  form.free_shipping_carriers = ['vet_express', 'jt_express', 'lumea_concierge']
  form.grab_subsidy_enabled = true
  adminStore.addToast('Shipping settings reset to standard atelier configuration', 'info')
}

// Clear Cache Action
async function handleClearCache() {
  isClearingCache.value = true
  try {
    const res = await apiClient.post('/admin/cache/clear')
    if (res.data?.status === 'success') {
      adminStore.addToast('System cache cleared! Buffers refreshed.', 'success')
    }
  } catch (err) {
    adminStore.addToast('Failed to clear system cache', 'error')
  } finally {
    isClearingCache.value = false
  }
}

// Export Settings JSON
function exportSettingsFile() {
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(form, null, 2))
  const link = document.createElement('a')
  link.setAttribute('href', dataStr)
  link.setAttribute('download', `lumea_atelier_settings_${Date.now()}.json`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  adminStore.addToast('Settings configuration exported (JSON)', 'success')
}

// Backup Store Data
function backupStoreData() {
  const backup = {
    settings: form,
    timestamp: new Date().toISOString(),
    system: 'Luméa Atelier E-Commerce Python FastAPI'
  }
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(backup, null, 2))
  const link = document.createElement('a')
  link.setAttribute('href', dataStr)
  link.setAttribute('download', `lumea_backup_${Date.now()}.json`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  adminStore.addToast('Settings snapshot downloaded (does not include orders or customers)', 'success')
}

function importSettingsFile() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        try {
          const parsed = JSON.parse(event.target.result)
          const target = parsed.settings || parsed
          Object.assign(form, target)
          adminStore.addToast('Settings imported successfully from file', 'success')
        } catch {
          adminStore.addToast('Invalid JSON file format', 'error')
        }
      }
      reader.readAsText(file)
    }
  }
  input.click()
}

function changeStoreLogo() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e) => {
    const file = e.target.files?.[0]
    if (file) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const res = await apiClient.post('/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        const url = res.data?.data?.url || res.data?.url
        if (url) {
          form.store_logo = url
          adminStore.addToast('Store logo uploaded! Click Save to apply.', 'success')
        }
      } catch (err) {
        adminStore.addToast('Failed to upload store logo', 'error')
      }
    }
  }
  input.click()
}

function removeStoreLogo() {
  form.store_logo = ''
  adminStore.addToast('Store logo reset to default Luméa typography. Click Save to apply.', 'info')
}

function changeFavicon() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.ico,.png,.svg,.jpg'
  input.onchange = async (e) => {
    const file = e.target.files?.[0]
    if (file) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const res = await apiClient.post('/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        const url = res.data?.data?.url || res.data?.url
        if (url) {
          form.store_favicon = url
          adminStore.addToast('Store favicon uploaded! Click Save to apply.', 'success')
        }
      } catch (err) {
        adminStore.addToast('Failed to upload store favicon', 'error')
      }
    }
  }
  input.click()
}

function removeFavicon() {
  form.store_favicon = ''
  adminStore.addToast('Store favicon reset to default. Click Save to apply.', 'info')
}

function inviteStaffMember() {
  const email = prompt('Enter staff member email address:')
  if (email && email.trim()) {
    const role = prompt('Assign role (Administrator, Order Fulfillment, Content Editor):', 'Order Fulfillment') || 'Staff Member'
    staffMembers.value.push({
      id: Date.now(),
      name: email.split('@')[0].replace(/[._]/g, ' '),
      email: email.trim(),
      role: role.trim(),
      avatar: '/images/avatar-sreynich.jpg',
      status: 'Invited'
    })
    adminStore.addToast(`Invitation dispatched to ${email.trim()} as ${role.trim()}`, 'success')
  }
}
</script>

<template>
  <div class="settings-page">
      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">Settings</h1>
          <p class="hero-subtitle">Manage your store preferences, configurations, and integrations.</p>
        </div>

        <div class="hero-art-side">
          <img src="/images/admin-hero-bottles.jpg" alt="Luméa Atelier" class="hero-art-img" />
          <div class="hero-quote">
            <span class="quote-line-1">A smoother</span>
            <span class="quote-line-2">operation for a</span>
            <span class="quote-line-3">brighter tomorrow.</span>
          </div>
        </div>
      </div>

      <!-- MAIN 3-PANEL SETTINGS WORKSPACE -->
      <div class="settings-workspace">
        <!-- 1. LEFT COLUMN: VERTICAL TABS (12 ITEMS) -->
        <div class="tabs-nav-column">
          <div
            v-for="tab in tabs"
            :key="tab.id"
            class="tab-nav-item"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <div class="tab-icon-wrap">
              <component :is="tab.icon" class="w-4 h-4" />
            </div>
            <div class="tab-text-wrap">
              <span class="tab-title">{{ tab.name }}</span>
              <span class="tab-sub">{{ tab.desc }}</span>
            </div>
          </div>
        </div>

        <!-- 2. MIDDLE COLUMN: MAIN CONFIGURATION PANE -->
        <div class="center-config-pane">
          <!-- TAB 1: GENERAL SETTINGS (MATCHING EXACT MOCKUP) -->
          <div v-if="activeTab === 'general'" class="config-content">
            <!-- Header Row -->
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">General Settings</h2>
                <p class="pane-subheading">Basic information about your store and business.</p>
              </div>

              <div class="header-buttons">
                <button class="btn-reset" @click="resetSettings">
                  <RotateCcw class="w-3.5 h-3.5 mr-1" />
                  <span>Reset</span>
                </button>
                <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                  <Save class="w-3.5 h-3.5 mr-1" />
                  <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
                </button>
              </div>
            </div>

            <!-- Form Body -->
            <div class="form-body-grid">
              <!-- Store Name & Email -->
              <div class="form-row-two">
                <div class="form-field">
                  <label class="field-label">Store Name <span class="text-crimson">*</span></label>
                  <input v-model="form.store_name" type="text" class="field-input" />
                  <span class="field-hint">This name will appear on your website and emails.</span>
                </div>

                <div class="form-field">
                  <label class="field-label">Store Email <span class="text-crimson">*</span></label>
                  <input v-model="form.store_email" type="email" class="field-input" />
                  <span class="field-hint">Used for customer communication and notifications.</span>
                </div>
              </div>

              <!-- Store Phone & Store Language -->
              <div class="form-row-two mt-3">
                <div class="form-field">
                  <label class="field-label">Store Phone</label>
                  <div class="phone-input-wrap">
                    <div class="country-prefix">
                      <span class="country-code-pill">KH</span>
                      <span class="prefix-text">{{ form.phone_country_code }}</span>
                      <ChevronDown :size="12" class="prefix-arrow-svg" />
                    </div>
                    <input v-model="form.store_phone" type="text" class="field-input phone-input" />
                  </div>
                  <span class="field-hint">Your customer support phone number.</span>
                </div>

                <div class="form-field">
                  <label class="field-label">Store Language</label>
                  <select v-model="form.store_language" class="field-select">
                    <option value="English (Default)">English (Default)</option>
                    <option value="Khmer">Khmer</option>
                    <option value="French">French</option>
                  </select>
                  <span class="field-hint">Default language for your store.</span>
                </div>
              </div>

              <!-- Store Description -->
              <div class="form-field mt-3">
                <div class="label-with-count">
                  <label class="field-label">Store Description</label>
                  <span class="count-text">{{ form.store_description.length }}/200</span>
                </div>
                <textarea
                  v-model="form.store_description"
                  class="field-textarea"
                  rows="2"
                  maxlength="200"
                ></textarea>
                <span class="field-hint">A short description about your store.</span>
              </div>

              <!-- Store Logo & Favicon Row -->
              <div class="form-row-two mt-4">
                <!-- Store Logo -->
                <div class="form-field">
                  <label class="field-label">Store Logo</label>
                  <div class="logo-box-row">
                    <div class="logo-preview-card">
                      <img v-if="form.store_logo" :src="form.store_logo" alt="Store Logo" class="max-h-8 max-w-full object-contain" />
                      <span v-else class="logo-text-display">Luméa</span>
                    </div>
                    <div class="logo-btn-col">
                      <button class="btn-change-box" @click="changeStoreLogo">
                        <Upload class="w-3 h-3 mr-1" />
                        <span>Change Logo</span>
                      </button>
                      <button class="btn-remove-box" @click="removeStoreLogo">
                        <Trash2 class="w-3 h-3 mr-1" />
                        <span>Remove</span>
                      </button>
                    </div>
                  </div>
                  <span class="field-hint">Recommended size: 300 x 100 px (PNG, SVG)</span>
                </div>

                <!-- Store Favicon -->
                <div class="form-field">
                  <label class="field-label">Store Favicon</label>
                  <div class="logo-box-row">
                    <div class="favicon-preview-card">
                      <img v-if="form.store_favicon" :src="form.store_favicon" alt="Store Favicon" class="w-6 h-6 object-contain" />
                      <svg v-else viewBox="0 0 24 24" class="w-5 h-5 text-crimson fill-crimson">
                        <path d="M12 2C6.5 2 2 6.5 2 12c0 5.5 4.5 10 10 10s10-4.5 10-10c0-5.5-4.5-10-10-10zm-1 14.5c-2.5 0-4.5-2-4.5-4.5S8.5 7.5 11 7.5s4.5 2 4.5 4.5-2 4.5-4.5 4.5z"/>
                      </svg>
                    </div>
                    <div class="logo-btn-col">
                      <button class="btn-change-box" @click="changeFavicon">
                        <Upload class="w-3 h-3 mr-1" />
                        <span>Change Favicon</span>
                      </button>
                      <button class="btn-remove-box" @click="removeFavicon">
                        <Trash2 class="w-3 h-3 mr-1" />
                        <span>Remove</span>
                      </button>
                    </div>
                  </div>
                  <span class="field-hint">Recommended size: 32 x 32 px (PNG, ICO)</span>
                </div>
              </div>

              <!-- BUSINESS INFORMATION SECTION -->
              <div class="business-section-divider"></div>

              <div class="business-header">
                <h3 class="business-heading">Business Information</h3>
                <p class="business-subheading">Your business details will be shown on invoices and legal documents.</p>
              </div>

              <!-- Company Name & Business Registration Number -->
              <div class="form-row-two mt-3">
                <div class="form-field">
                  <label class="field-label">Company Name</label>
                  <input v-model="form.company_name" type="text" class="field-input" />
                </div>

                <div class="form-field">
                  <label class="field-label">Business Registration Number</label>
                  <input v-model="form.business_reg_number" type="text" class="field-input" />
                  <span class="field-hint">Your official business registration number.</span>
                </div>
              </div>

              <!-- Business Address & Time Zone -->
              <div class="form-row-two mt-3">
                <div class="form-field">
                  <label class="field-label">Business Address</label>
                  <textarea
                    v-model="form.business_address"
                    class="field-textarea"
                    rows="2"
                  ></textarea>
                  <span class="field-hint">Your registered business address.</span>
                </div>

                <div class="form-field">
                  <label class="field-label">Time Zone</label>
                  <select v-model="form.time_zone" class="field-select">
                    <option value="(UTC+07:00) Phnom Penh">(UTC+07:00) Phnom Penh</option>
                    <option value="(UTC+07:00) Bangkok">(UTC+07:00) Bangkok</option>
                    <option value="(UTC+08:00) Singapore">(UTC+08:00) Singapore</option>
                    <option value="(UTC+09:00) Tokyo">(UTC+09:00) Tokyo</option>
                  </select>
                  <span class="field-hint">Used for orders, reports, and notifications.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 2: STORE SETTINGS -->
          <div v-else-if="activeTab === 'store_settings'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Store Settings</h2>
                <p class="pane-subheading">Currency preferences and operational policies.</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Operating Currency</label>
                <select v-model="form.currency" class="field-select">
                  <option value="USD ($)">USD ($)</option>
                  <option value="KHR (៛)">KHR (៛)</option>
                  <option value="EUR (€)">EUR (€)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- TAB 3: PAYMENTS -->
          <div v-else-if="activeTab === 'payments'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Payment Gateways & Methods</h2>
                <p class="pane-subheading">Configure enabled checkout methods for clientele.</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="payment-methods-grid mt-4">
              <div class="payment-card">
                <div class="pay-top">
                  <span class="font-semibold text-charcoal">ABA PAY (Bakong QR)</span>
                  <span class="badge-status status-active">Active</span>
                </div>
                <p class="text-xs text-taupe mt-1">Instant QR settlement with Cambodian banks.</p>
              </div>
              <div class="payment-card mt-2">
                <div class="pay-top">
                  <span class="font-semibold text-charcoal">Credit / Debit Card (Visa / Mastercard)</span>
                  <span class="badge-status status-active">Active</span>
                </div>
                <p class="text-xs text-taupe mt-1">Stripe / Merchant payment processor.</p>
              </div>
              <div class="payment-card mt-2">
                <div class="pay-top">
                  <span class="font-semibold text-charcoal">Cash on Delivery (COD)</span>
                  <span class="badge-status status-active">Active</span>
                </div>
                <p class="text-xs text-taupe mt-1">Pay courier in cash upon package handover in Phnom Penh.</p>
              </div>
            </div>
          </div>

          <!-- TAB 4: SHIPPING & DELIVERY ATELIER STUDIO -->
          <div v-else-if="activeTab === 'shipping'" class="config-content shipping-studio-content">
            <!-- Header Row -->
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Shipping & Delivery Management</h2>
                <p class="pane-subheading">Configure nationwide courier tariffs, dynamic free delivery rules, and promotional subsidies.</p>
              </div>

              <div class="header-buttons">
                <button class="btn-reset" @click="resetShippingSettings">
                  <RotateCcw class="w-3.5 h-3.5 mr-1" />
                  <span>Reset</span>
                </button>
                <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                  <Save class="w-3.5 h-3.5 mr-1" />
                  <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
                </button>
              </div>
            </div>

            <!-- Master Campaign Status Bar -->
            <div class="shipping-status-banner" :class="{ 'status-promo-active': form.free_shipping_enabled && form.free_shipping_mode !== 'disabled' }">
              <div class="status-banner-left">
                <div class="status-indicator-dot" :class="{ active: form.free_shipping_enabled && form.free_shipping_mode !== 'disabled' }"></div>
                <div>
                  <h4 class="status-banner-title">
                    {{ !form.free_shipping_enabled || form.free_shipping_mode === 'disabled'
                      ? 'Free Delivery is Currently Disabled'
                      : form.free_shipping_mode === 'all_orders'
                      ? 'Storewide Free Delivery Active (All Orders - $0 Min)'
                      : `Free Delivery Active for Orders Over $${Number(form.free_shipping_threshold).toFixed(2)}` }}
                  </h4>
                  <p class="status-banner-sub">
                    {{ !form.free_shipping_enabled || form.free_shipping_mode === 'disabled'
                      ? 'Customers are charged full courier tariffs regardless of bag total.'
                      : form.free_shipping_mode === 'all_orders'
                      ? 'All customers receive 100% complimentary delivery on eligible couriers.'
                      : `Orders reaching $${Number(form.free_shipping_threshold).toFixed(2)} automatically unlock free nationwide shipping.` }}
                  </p>
                </div>
              </div>
              <div class="status-toggle-wrap">
                <label class="switch-control">
                  <input type="checkbox" v-model="form.free_shipping_enabled" @change="onToggleFreeShipping" />
                  <span class="slider-round"></span>
                </label>
                <span class="switch-label">{{ form.free_shipping_enabled ? 'Active' : 'Disabled' }}</span>
              </div>
            </div>

            <!-- Section 1: Choose Free Delivery Mode -->
            <div class="studio-section mt-5">
              <div class="section-title-row">
                <h3 class="studio-section-title">1. Free Delivery Policy Mode</h3>
                <span class="studio-section-badge">Admin Configurable Anytime</span>
              </div>
              <p class="studio-section-sub">Choose when customers qualify for free shipping. You can change this whenever you want (e.g. flash sales, weekend promos, or threshold changes).</p>

              <div class="modes-three-grid mt-3">
                <!-- Mode 1: Minimum Order Threshold -->
                <div
                  class="mode-card"
                  :class="{ selected: form.free_shipping_mode === 'threshold' && form.free_shipping_enabled }"
                  @click="setPromoMode('threshold')"
                >
                  <div class="mode-card-header">
                    <span class="mode-radio-circle" :class="{ active: form.free_shipping_mode === 'threshold' && form.free_shipping_enabled }"></span>
                    <span class="mode-badge badge-standard">Custom Threshold</span>
                  </div>
                  <h4 class="mode-title">Orders Over Threshold</h4>
                  <p class="mode-desc">Free delivery when customer cart subtotal reaches a specified minimum dollar amount.</p>
                  
                  <div class="mode-threshold-input-wrap" @click.stop>
                    <label class="threshold-label">Threshold ($):</label>
                    <div class="currency-input-box">
                      <span class="currency-symbol">$</span>
                      <input
                        v-model.number="form.free_shipping_threshold"
                        type="number"
                        min="0"
                        step="5"
                        class="threshold-input"
                        placeholder="50.00"
                      />
                    </div>
                  </div>
                </div>

                <!-- Mode 2: All Orders Promo (100% Free Shipping) -->
                <div
                  class="mode-card"
                  :class="{ selected: form.free_shipping_mode === 'all_orders' && form.free_shipping_enabled }"
                  @click="setPromoMode('all_orders')"
                >
                  <div class="mode-card-header">
                    <span class="mode-radio-circle" :class="{ active: form.free_shipping_mode === 'all_orders' && form.free_shipping_enabled }"></span>
                    <span class="mode-badge badge-promo">Campaign Promo</span>
                  </div>
                  <h4 class="mode-title">All Orders (Storewide Free)</h4>
                  <p class="mode-desc">100% Free delivery for every order ($0 minimum). Boosts sales during promotions & launches.</p>
                  <div class="mode-perk-pill">
                    <Sparkles class="w-3 h-3 text-gold mr-1" />
                    <span>$0 Minimum Order Required</span>
                  </div>
                </div>

                <!-- Mode 3: Disabled -->
                <div
                  class="mode-card"
                  :class="{ selected: !form.free_shipping_enabled || form.free_shipping_mode === 'disabled' }"
                  @click="setPromoMode('disabled')"
                >
                  <div class="mode-card-header">
                    <span class="mode-radio-circle" :class="{ active: !form.free_shipping_enabled || form.free_shipping_mode === 'disabled' }"></span>
                    <span class="mode-badge badge-muted">Standard</span>
                  </div>
                  <h4 class="mode-title">Disabled (Full Tariffs)</h4>
                  <p class="mode-desc">Free delivery promotion is turned off. Customers always pay the courier fee for every order.</p>
                  <div class="mode-perk-pill text-taupe">
                    <span>Standard Courier Rates Apply</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section 2: Eligible Couriers Configuration -->
            <div class="studio-section mt-5">
              <div class="section-title-row">
                <h3 class="studio-section-title">2. Cambodian Couriers & Free Delivery Eligibility</h3>
                <span class="studio-section-badge">Carrier Tariffs</span>
              </div>
              <p class="studio-section-sub">Select which delivery carriers offer complimentary delivery when customer qualifies.</p>

              <div class="couriers-config-list mt-3">
                <!-- VET -->
                <div class="courier-config-item">
                  <div class="courier-item-left">
                    <img src="/images/couriers/vet_express.png" alt="VET Logistics" class="courier-item-logo" />
                    <div class="courier-item-details">
                      <div class="courier-item-title-row">
                        <h4 class="courier-item-name">Vireak Buntham (VET Logistics)</h4>
                        <span class="courier-item-badge">Nationwide #1</span>
                      </div>
                      <p class="courier-item-meta">Standard Flat Rate: <strong>$1.50 nationwide</strong> (All 25 provinces and Phnom Penh) • 1–2 Business Days</p>
                    </div>
                  </div>
                  <div class="courier-item-right">
                    <label class="eligibility-checkbox-label">
                      <input
                        type="checkbox"
                        :checked="form.free_shipping_carriers.includes('vet_express')"
                        @change="toggleCarrierEligibility('vet_express')"
                      />
                      <span>Qualifies for Free Delivery</span>
                    </label>
                  </div>
                </div>

                <!-- J&T -->
                <div class="courier-config-item">
                  <div class="courier-item-left">
                    <img src="/images/couriers/jt_express.png" alt="J&T Express" class="courier-item-logo" />
                    <div class="courier-item-details">
                      <div class="courier-item-title-row">
                        <h4 class="courier-item-name">J&T Express Cambodia</h4>
                        <span class="courier-item-badge">Fast Domestic</span>
                      </div>
                      <p class="courier-item-meta">Standard Flat Rate: <strong>$1.75 nationwide</strong> (All 25 provinces and Phnom Penh) • Next-Day Delivery</p>
                    </div>
                  </div>
                  <div class="courier-item-right">
                    <label class="eligibility-checkbox-label">
                      <input
                        type="checkbox"
                        :checked="form.free_shipping_carriers.includes('jt_express')"
                        @change="toggleCarrierEligibility('jt_express')"
                      />
                      <span>Qualifies for Free Delivery</span>
                    </label>
                  </div>
                </div>

                <!-- GrabExpress -->
                <div class="courier-config-item">
                  <div class="courier-item-left">
                    <img src="/images/couriers/grab_express.png" alt="GrabExpress" class="courier-item-logo" />
                    <div class="courier-item-details">
                      <div class="courier-item-title-row">
                        <h4 class="courier-item-name">GrabExpress On-Demand</h4>
                        <span class="courier-item-badge badge-grab">Instant Express (PP Only)</span>
                      </div>
                      <p class="courier-item-meta">Distance Tariff: <strong>$2.00 base + $0.40/km</strong> • 60–90 Mins Motorbike Handover</p>
                    </div>
                  </div>
                  <div class="courier-item-right">
                    <label class="eligibility-checkbox-label">
                      <input
                        type="checkbox"
                        v-model="form.grab_subsidy_enabled"
                      />
                      <span>Apply $1.50 Free Delivery Subsidy Credit</span>
                    </label>
                  </div>
                </div>

                <!-- Luméa Concierge -->
                <div class="courier-config-item">
                  <div class="courier-item-left">
                    <div class="courier-item-logo concierge-logo-placeholder">
                      <Sparkles :size="16" />
                    </div>
                    <div class="courier-item-details">
                      <div class="courier-item-title-row">
                        <h4 class="courier-item-name">Luméa Atelier Concierge</h4>
                        <span class="courier-item-badge badge-signature">Atelier Signature</span>
                      </div>
                      <p class="courier-item-meta">White-Glove Rate: <strong>$3.00 flat</strong> • Signature silk-ribbon box presentation</p>
                    </div>
                  </div>
                  <div class="courier-item-right">
                    <label class="eligibility-checkbox-label">
                      <input
                        type="checkbox"
                        :checked="form.free_shipping_carriers.includes('lumea_concierge')"
                        @change="toggleCarrierEligibility('lumea_concierge')"
                      />
                      <span>Qualifies for Free Delivery</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Section 3: Promotional Announcement Copy -->
            <div class="studio-section mt-5">
              <div class="section-title-row">
                <h3 class="studio-section-title">3. Customer Promotional Announcement Banner</h3>
                <span class="studio-section-badge">Storefront Display</span>
              </div>
              <p class="studio-section-sub">Announcement displayed in the customer cart drawer and checkout page header.</p>

              <div class="promo-text-field-wrap mt-3">
                <input
                  v-model="form.free_shipping_promo_text"
                  type="text"
                  class="field-input promo-input"
                  placeholder="e.g. Complimentary nationwide shipping on orders over $50"
                />
                <div class="promo-presets-row mt-2">
                  <span class="presets-label">Quick Presets:</span>
                  <button type="button" class="preset-pill" @click="applyPromoPreset('Complimentary nationwide shipping on orders over $50', 50)">Orders over $50</button>
                  <button type="button" class="preset-pill" @click="applyPromoPreset('Complimentary nationwide shipping on orders over $35', 35)">Orders over $35</button>
                  <button type="button" class="preset-pill" @click="applyPromoPreset('Atelier Special: Complimentary Free Delivery on All Orders!', 0)">Storewide Free Delivery</button>
                  <button type="button" class="preset-pill" @click="applyPromoPreset('Weekend Flash Promotion: Free Shipping Active!', 0)">Weekend Flash</button>
                </div>
              </div>
            </div>

            <!-- Section 4: Live Storefront Checkout Preview -->
            <div class="studio-section mt-5 preview-studio-section">
              <div class="section-title-row">
                <h3 class="studio-section-title">4. Live Storefront Preview</h3>
                <span class="studio-section-badge badge-live">Live Preview</span>
              </div>
              <p class="studio-section-sub">This is exactly how patrons see your shipping configuration at checkout right now:</p>

              <div class="checkout-simulation-box mt-3">
                <div class="simulation-banner">
                  <Sparkles class="w-4 h-4 text-gold mr-2" />
                  <span v-if="!form.free_shipping_enabled || form.free_shipping_mode === 'disabled'">
                    Standard nationwide courier rates applied.
                  </span>
                  <span v-else-if="form.free_shipping_mode === 'all_orders'">
                    {{ form.free_shipping_promo_text || 'Free nationwide delivery on all orders!' }}
                  </span>
                  <span v-else>
                    {{ form.free_shipping_promo_text || `Complimentary nationwide shipping on orders over $${Number(form.free_shipping_threshold).toFixed(2)}` }}
                  </span>
                </div>

                <div class="simulation-cards-row mt-3">
                  <div class="sim-card">
                    <span class="sim-name">VET Express</span>
                    <span class="sim-rate" :class="{ 'sim-free': form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('vet_express') }">
                      {{ form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('vet_express') ? 'FREE ($0.00)' : '$1.50' }}
                    </span>
                  </div>
                  <div class="sim-card">
                    <span class="sim-name">J&T Express</span>
                    <span class="sim-rate" :class="{ 'sim-free': form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('jt_express') }">
                      {{ form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('jt_express') ? 'FREE ($0.00)' : '$1.75' }}
                    </span>
                  </div>
                  <div class="sim-card">
                    <span class="sim-name">GrabExpress</span>
                    <span class="sim-rate">
                      {{ form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.grab_subsidy_enabled ? '$2.00 ($1.50 credit)' : '$3.50 (GPS)' }}
                    </span>
                  </div>
                  <div class="sim-card">
                    <span class="sim-name">Concierge</span>
                    <span class="sim-rate" :class="{ 'sim-free': form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('lumea_concierge') }">
                      {{ form.free_shipping_enabled && form.free_shipping_mode === 'all_orders' && form.free_shipping_carriers.includes('lumea_concierge') ? 'FREE ($0.00)' : '$3.00' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Save Bar -->
            <div class="pane-footer-save-bar mt-6">
              <button class="btn-save btn-save-large" :disabled="isSaving" @click="saveSettings">
                <Save class="w-4 h-4 mr-2" />
                <span>{{ isSaving ? 'Saving Configurations...' : 'Save & Publish Shipping Settings' }}</span>
              </button>
            </div>
          </div>

          <!-- TAB 5: TAXES -->
          <div v-else-if="activeTab === 'taxes'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Tax & VAT Rates</h2>
                <p class="pane-subheading">Configure tax calculation and invoice compliance.</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Value Added Tax (VAT) %</label>
                <input v-model="form.tax_rate" type="number" class="field-input" />
              </div>
            </div>
          </div>

          <!-- TAB 6: NOTIFICATIONS -->
          <div v-else-if="activeTab === 'notifications'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Automated Notifications</h2>
                <p class="pane-subheading">Manage transactional email alerts sent to patrons.</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="toggle-list mt-4">
              <div class="toggle-item">
                <span class="font-medium text-sm text-charcoal">Order Confirmation Email</span>
                <span class="text-xs text-green font-semibold">Enabled</span>
              </div>
              <div class="toggle-item mt-2">
                <span class="font-medium text-sm text-charcoal">Fulfillment & Tracking Alert</span>
                <span class="text-xs text-green font-semibold">Enabled</span>
              </div>
              <div class="toggle-item mt-2">
                <span class="font-medium text-sm text-charcoal">Return Status Updates</span>
                <span class="text-xs text-green font-semibold">Enabled</span>
              </div>
            </div>
          </div>

          <!-- TAB 7: USERS & PERMISSIONS -->
          <div v-else-if="activeTab === 'users'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Staff & Permissions</h2>
                <p class="pane-subheading">Atelier administrators and operators.</p>
              </div>
              <button class="btn-save" @click="inviteStaffMember">
                <Users class="w-3.5 h-3.5 mr-1" />
                <span>Add Staff</span>
              </button>
            </div>
            <div class="staff-list mt-4">
              <div v-for="staff in staffMembers" :key="staff.id" class="staff-card mb-2">
                <img :src="staff.avatar" class="w-10 h-10 rounded-full object-cover" />
                <div class="ml-3 flex-1">
                  <span class="font-semibold text-sm text-charcoal block">{{ staff.name }}</span>
                  <span class="text-xs text-taupe">{{ staff.role }} · {{ staff.email }}</span>
                </div>
                <span class="badge-status" :class="staff.status === 'Active' ? 'status-active' : 'status-pending'">{{ staff.status }}</span>
              </div>
            </div>
          </div>

          <!-- OTHER TABS FALLBACK -->
          <div v-else class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">{{ tabs.find(t => t.id === activeTab)?.name }}</h2>
                <p class="pane-subheading">{{ tabs.find(t => t.id === activeTab)?.desc }}</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="p-6 text-center text-taupe mt-4 bg-warm-white rounded-lg border border-sand">
              <Sliders class="w-10 h-10 mx-auto mb-2 opacity-40 text-charcoal" />
              <p class="text-sm font-medium text-charcoal">Configurations are synchronized with the Luméa SQLite database.</p>
            </div>
          </div>
        </div>

        <!-- 3. RIGHT COLUMN: SIDEBAR WIDGETS (MATCHING EXACT MOCKUP) -->
        <div class="right-widgets-column">
          <!-- Widget 1: Store Status -->
          <div class="widget-card">
            <h4 class="widget-heading">Store Status</h4>
            <div class="status-banner-box">
              <div class="status-badge-live">
                <CheckCircle2 class="w-4 h-4 text-green" />
                <span class="status-text-live">Online</span>
              </div>
              <p class="status-desc-text">Your store is currently live and visible to customers.</p>
              <a :href="getStorefrontUrl()" target="_blank" class="btn-view-store">
                <ExternalLink class="w-4 h-4 mr-1.5" />
                <span>View Store</span>
              </a>
            </div>
          </div>

          <!-- Widget: Media & Upload Storage -->
          <div class="widget-card mt-3">
            <h4 class="widget-heading">Media & Upload Storage</h4>
            <div class="status-banner-box">
              <div :class="uploadStatus.storage_type === 'unknown' ? 'status-badge-neutral' : (uploadStatus.enabled ? 'status-badge-live' : 'status-badge-warning')">
                <component :is="uploadStatus.storage_type === 'unknown' ? RefreshCw : (uploadStatus.enabled ? CheckCircle2 : AlertCircle)" class="w-4 h-4" :class="uploadStatus.storage_type === 'unknown' ? 'text-taupe' : (uploadStatus.enabled ? 'text-green' : 'text-crimson')" />
                <span :class="uploadStatus.storage_type === 'unknown' ? 'text-taupe font-medium text-xs' : (uploadStatus.enabled ? 'status-text-live' : 'text-crimson font-medium text-xs')">
                  {{ uploadStatus.storage_type === 'unknown' ? 'Storage Unknown' : (uploadStatus.enabled ? (uploadStatus.storage_type === 'persistent' ? 'Persistent Storage' : 'Local Storage (Dev)') : 'Storage Read-Only') }}
                </span>
              </div>
              <p class="status-desc-text" style="font-size: 0.75rem; line-height: 1.3; margin-top: 0.25rem;">
                <template v-if="uploadStatus.storage_type !== 'unknown'">
                  Safe Formats: {{ (uploadStatus.allowed_formats || []).join(', ') }}<br/>
                  Max Image: {{ uploadStatus.max_image_mb }}MB | Max Video: {{ uploadStatus.max_video_mb }}MB
                </template>
                <template v-else>
                  Verifying storage backend readiness...
                </template>
              </p>
            </div>
          </div>

          <!-- Widget 2: Need Help? -->
          <div class="widget-card help-card mt-3">
            <div class="help-header">
              <Lightbulb class="w-5 h-5 text-crimson mr-2" />
              <h4 class="help-heading">Need Help?</h4>
            </div>
            <p class="help-body">
              Check out our documentation or contact support if you need assistance with your settings.
            </p>
            <a href="javascript:void(0)" class="help-link">
              <span>Visit Help Center</span>
              <ArrowRight class="w-3.5 h-3.5 ml-1" />
            </a>
          </div>

          <!-- Widget 3: Quick Actions -->
          <div class="widget-card quick-actions-card mt-3">
            <h4 class="widget-heading">Quick Actions</h4>

            <div class="action-items-list">
              <!-- Backup Store Data -->
              <div class="quick-action-item" @click="backupStoreData">
                <div class="action-icon-wrap">
                  <Database class="w-4 h-4 text-charcoal" />
                </div>
                <div class="action-text-wrap">
                  <span class="action-title">Backup Store Data</span>
                  <span class="action-desc">Download settings only. Orders, customers, and files are excluded.</span>
                </div>
              </div>

              <!-- Clear Cache -->
              <div class="quick-action-item" @click="handleClearCache">
                <div class="action-icon-wrap">
                  <RefreshCw class="w-4 h-4 text-charcoal" :class="{ 'animate-spin': isClearingCache }" />
                </div>
                <div class="action-text-wrap">
                  <span class="action-title">Clear Cache</span>
                  <span class="action-desc">Clear system cache to refresh your store.</span>
                </div>
              </div>

              <!-- Export Settings -->
              <div class="quick-action-item" @click="exportSettingsFile">
                <div class="action-icon-wrap">
                  <Download class="w-4 h-4 text-charcoal" />
                </div>
                <div class="action-text-wrap">
                  <span class="action-title">Export Settings</span>
                  <span class="action-desc">Download your current settings.</span>
                </div>
              </div>

              <!-- Import Settings -->
              <div class="quick-action-item" @click="importSettingsFile">
                <div class="action-icon-wrap">
                  <Upload class="w-4 h-4 text-charcoal" />
                </div>
                <div class="action-text-wrap">
                  <span class="action-title">Import Settings</span>
                  <span class="action-desc">Import settings from a backup file.</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.settings-page {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Hero Banner */
.hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FBF8F5 0%, #F5ECE6 100%);
  border: 1px solid #EBE1D7;
  border-radius: 12px;
  padding: 1.5rem 2rem;
  min-height: 120px;
}

.hero-content {
  max-width: 550px;
}

.hero-title {
  font-family: var(--font-serif, 'Playfair Display', Georgia, serif);
  font-size: 2rem;
  font-weight: 600;
  color: #84261B;
  margin: 0 0 0.35rem 0;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 0.875rem;
  color: #6E635E;
  margin: 0;
  line-height: 1.45;
}

.hero-art-side {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.hero-art-img {
  width: 90px;
  height: 65px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(45, 36, 34, 0.08);
}

.hero-quote {
  display: flex;
  flex-direction: column;
}

.quote-line-1, .quote-line-2, .quote-line-3 {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 0.9375rem;
  font-weight: 600;
  color: #84261B;
  line-height: 1.25;
}

/* Workspace 3 Columns */
.settings-workspace {
  display: grid;
  grid-template-columns: 260px 1fr 280px;
  gap: 1.25rem;
  align-items: flex-start;
}

/* 1. Tabs Nav Column */
.tabs-nav-column {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tab-nav-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.65rem 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.tab-nav-item:hover {
  background: #FAF6F2;
}

.tab-nav-item.active {
  background: #FDF2EE;
}

.tab-icon-wrap {
  color: #8C827A;
  margin-top: 0.15rem;
}

.tab-nav-item.active .tab-icon-wrap {
  color: #84261B;
}

.tab-text-wrap {
  display: flex;
  flex-direction: column;
}

.tab-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2D2422;
}

.tab-nav-item.active .tab-title {
  color: #84261B;
}

.tab-sub {
  font-size: 0.6875rem;
  color: #8C827A;
  line-height: 1.25;
}

/* 2. Center Configuration Pane */
.center-config-pane {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.5rem;
}

.pane-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #F5ECE6;
}

.pane-heading {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.pane-subheading {
  font-size: 0.75rem;
  color: #8C827A;
  margin: 0.25rem 0 0 0;
}

.header-buttons {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-reset {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.45rem 0.85rem;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #6E635E;
  cursor: pointer;
}

.btn-save {
  display: inline-flex;
  align-items: center;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.45rem 1.125rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
}

/* Form Body */
.form-body-grid {
  margin-top: 1.25rem;
}

.form-row-two {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.field-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
  margin-bottom: 0.35rem;
}

.text-crimson { color: #84261B; }

.field-input, .field-select, .field-textarea {
  width: 100%;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0.55rem 0.75rem;
  font-size: 0.8125rem;
  background: #FAF6F2;
  color: #2D2422;
  outline: none;
}

.field-input:focus, .field-select:focus, .field-textarea:focus {
  background: #FFFFFF;
  border-color: #84261B;
}

.field-hint {
  font-size: 0.6875rem;
  color: #8C827A;
  margin-top: 0.35rem;
}

.phone-input-wrap {
  display: flex;
  align-items: center;
  background: #FAF6F2;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  overflow: hidden;
}

.country-prefix {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.55rem 0.65rem;
  border-right: 1px solid #E4D8CE;
  font-size: 0.8125rem;
  color: #2D2422;
}

.country-code-pill {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 1.5px 5px;
  border-radius: 4px;
  background: #F4EBE3;
  color: #84261B;
}

.prefix-arrow-svg {
  color: #8C847E;
}

.phone-input {
  border: none;
  background: transparent;
}

.label-with-count {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.count-text {
  font-size: 0.6875rem;
  color: #B5ABA4;
}

/* Logo & Favicon */
.logo-box-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-preview-card {
  width: 130px;
  height: 52px;
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text-display {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.25rem;
  font-weight: 600;
  color: #84261B;
}

.favicon-preview-card {
  width: 52px;
  height: 52px;
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-btn-col {
  display: flex;
  gap: 0.35rem;
}

.btn-change-box, .btn-remove-box {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.6875rem;
  color: #2D2422;
  cursor: pointer;
}

.btn-remove-box {
  color: #C0392B;
}

/* Business Section */
.business-section-divider {
  height: 1px;
  background: #F5ECE6;
  margin: 1.5rem 0;
}

.business-heading {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.business-subheading {
  font-size: 0.75rem;
  color: #8C827A;
  margin: 0.2rem 0 0 0;
}

/* 3. Right Widgets Column */
.right-widgets-column {
  display: flex;
  flex-direction: column;
}

.widget-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.125rem;
}

.widget-heading {
  font-size: 0.875rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0 0 0.875rem 0;
}

/* Status Box */
.status-banner-box {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.status-badge-live {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #EAF5EE;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  margin-bottom: 0.5rem;
}

.text-green { color: #2D8A4E; }

.status-text-live {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D8A4E;
}

.status-desc-text {
  font-size: 0.6875rem;
  color: #6E635E;
  margin: 0 0 0.75rem 0;
  line-height: 1.35;
}

.btn-view-store {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  padding: 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #2D2422;
  text-decoration: none;
}

/* Help Card */
.help-card {
  background: #FAF6F2;
}

.help-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.35rem;
}

.help-heading {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.help-body {
  font-size: 0.6875rem;
  color: #6E635E;
  line-height: 1.4;
  margin: 0 0 0.75rem 0;
}

.help-link {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  color: #84261B;
  font-weight: 600;
  text-decoration: none;
}

/* Quick Actions */
.action-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.quick-action-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.55rem;
  border: 1px solid #EBE1D7;
  border-radius: 6px;
  background: #FAF6F2;
  cursor: pointer;
  transition: all 0.15s ease;
}

.quick-action-item:hover {
  background: #FDF4F0;
  border-color: #84261B;
}

.action-icon-wrap {
  margin-top: 0.15rem;
}

.action-text-wrap {
  display: flex;
  flex-direction: column;
}

.action-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

.action-desc {
  font-size: 0.625rem;
  color: #8C827A;
  line-height: 1.25;
}

/* ==========================================================================
   SHIPPING & FREE DELIVERY ATELIER STUDIO STYLES
   ========================================================================== */
.shipping-studio-content {
  padding-bottom: 2rem;
}

.shipping-status-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-top: 1.25rem;
  transition: all 0.2s ease;
}

.shipping-status-banner.status-promo-active {
  background: #FDF9F3;
  border-color: #D97706;
}

.status-banner-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.status-indicator-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #9CA3AF;
  flex-shrink: 0;
}

.status-indicator-dot.active {
  background: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.status-banner-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.status-banner-sub {
  font-size: 0.75rem;
  color: #8C827A;
  margin: 0.15rem 0 0 0;
}

.status-toggle-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Switch Slider */
.switch-control {
  position: relative;
  display: inline-block;
  width: 36px;
  height: 20px;
}

.switch-control input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider-round {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #D1D5DB;
  transition: 0.2s;
  border-radius: 20px;
}

.slider-round:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.2s;
  border-radius: 50%;
}

input:checked + .slider-round {
  background-color: #84261B;
}

input:checked + .slider-round:before {
  transform: translateX(16px);
}

.switch-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

/* Studio Sections */
.studio-section {
  border-top: 1px solid #F5ECE6;
  padding-top: 1.25rem;
}

.section-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.studio-section-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.studio-section-badge {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  background: #F5ECE6;
  color: #84261B;
}

.studio-section-sub {
  font-size: 0.75rem;
  color: #8C827A;
  margin: 0.25rem 0 0 0;
}

/* Modes Grid */
.modes-three-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.mode-card {
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem;
  background: #FFFFFF;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.15s ease;
}

.mode-card:hover {
  border-color: #CDBEB5;
}

.mode-card.selected {
  border-color: #84261B;
  background: #FFFDFB;
  box-shadow: 0 0 0 1px #84261B;
}

.mode-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.65rem;
}

.mode-radio-circle {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid #D1D5DB;
  position: relative;
  display: inline-block;
}

.mode-radio-circle.active {
  border-color: #84261B;
}

.mode-radio-circle.active::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #84261B;
}

.mode-badge {
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
}

.badge-standard { background: #E0E7FF; color: #3730A3; }
.badge-promo { background: #FEF3C7; color: #92400E; }
.badge-muted { background: #F3F4F6; color: #4B5563; }

.mode-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.mode-desc {
  font-size: 0.6875rem;
  color: #8C827A;
  margin: 0.35rem 0 0.75rem 0;
  line-height: 1.35;
}

.mode-threshold-input-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 0.5rem;
  border-top: 1px dashed #EBE1D7;
}

.threshold-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #6E635E;
}

.currency-input-box {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
}

.currency-symbol {
  position: absolute;
  left: 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #8C827A;
}

.threshold-input {
  width: 100%;
  padding: 0.35rem 0.5rem 0.35rem 1.25rem;
  border: 1px solid #E4D8CE;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #FAF6F2;
  color: #2D2422;
}

.mode-perk-pill {
  display: flex;
  align-items: center;
  font-size: 0.6875rem;
  font-weight: 600;
  color: #92400E;
  margin-top: auto;
  padding-top: 0.5rem;
}

/* Couriers List */
.couriers-config-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.courier-config-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  background: #FFFFFF;
}

.courier-item-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.courier-item-logo {
  width: 38px;
  height: 24px;
  object-fit: contain;
  background: #FFFFFF;
  padding: 2px;
  border: 1px solid #F0E8E2;
  border-radius: 4px;
}

.concierge-logo-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  background: #FAF6F2;
}

.courier-item-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.courier-item-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.courier-item-badge {
  font-size: 0.5625rem;
  font-weight: 600;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  background: #F3F4F6;
  color: #4B5563;
}

.badge-grab { background: #DCFCE7; color: #166534; }
.badge-signature { background: #FEF3C7; color: #92400E; }

.courier-item-meta {
  font-size: 0.6875rem;
  color: #8C827A;
  margin: 0.15rem 0 0 0;
}

.eligibility-checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #2D2422;
  cursor: pointer;
}

/* Promo Text Presets */
.promo-input {
  background: #FAF6F2;
}

.promo-presets-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.presets-label {
  font-size: 0.6875rem;
  color: #8C827A;
}

.preset-pill {
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  border-radius: 12px;
  padding: 0.2rem 0.6rem;
  font-size: 0.6875rem;
  color: #6E635E;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preset-pill:hover {
  background: #FAF6F2;
  border-color: #84261B;
  color: #84261B;
}

/* Simulation Preview */
.preview-studio-section {
  background: #FAF6F2;
  border: 1px dashed #E0D4C8;
  border-radius: 8px;
  padding: 1.25rem;
}

.badge-live {
  background: #ECFDF5;
  color: #065F46;
}

.checkout-simulation-box {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem;
}

.simulation-banner {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  font-weight: 600;
  color: #84261B;
  background: #FFF9F6;
  border: 1px solid #FCD7CE;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
}

.simulation-cards-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
}

.sim-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.6rem;
  border: 1px solid #EBE1D7;
  border-radius: 6px;
  background: #FAF6F2;
}

.sim-name {
  font-size: 0.6875rem;
  font-weight: 500;
  color: #6E635E;
}

.sim-rate {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
  margin-top: 0.15rem;
}

.sim-rate.sim-free {
  color: #059669;
  font-weight: 700;
}

.pane-footer-save-bar {
  display: flex;
  justify-content: flex-end;
}

.btn-save-large {
  padding: 0.65rem 1.5rem;
  font-size: 0.8125rem;
}

@media (max-width: 1400px) {
  .settings-workspace {
    grid-template-columns: 240px 1fr;
  }
  .right-widgets-column {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
  }
}

@media (max-width: 900px) {
  .settings-workspace {
    grid-template-columns: 1fr;
  }
  .shipping-modes-grid {
    grid-template-columns: 1fr !important;
  }
}

@media (max-width: 640px) {
  .form-row-two {
    grid-template-columns: 1fr;
  }
  .courier-config-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
</style>
