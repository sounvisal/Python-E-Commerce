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
  Sparkles,
  X
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
  // 1. General Info
  store_name: 'Luméa Botanical Atelier',
  store_email: 'support@lumea.com',
  store_phone: '12 345 678',
  phone_country_code: '+855',
  store_language: 'English (Default)',
  store_description: 'Contemporary Clinical Skincare & Botanical Beauty Atelier. Natural beauty, clinically proven results.',
  company_name: 'Luméa Co., Ltd.',
  business_reg_number: 'KH-123456789',
  business_address: '#123, Norodom Blvd, Phnom Penh, Cambodia',
  time_zone: '(UTC+07:00) Phnom Penh',
  currency: 'USD ($)',
  online_status: 'Online',
  store_logo: '/images/logo-lumea.png',
  store_favicon: '/favicon.ico',

  // 2. Store Operations
  order_prefix: 'LM-',
  low_stock_threshold: 5,
  auto_confirm_orders: true,
  allow_backorders: false,
  cart_expiration_minutes: 30,

  // 3. Payment Methods
  payment_methods: {
    aba_pay: {
      enabled: true,
      merchant_name: 'LUMEA ATELIER',
      merchant_id: 'lumea_khqr@aba',
      test_mode: false
    },
    credit_card: {
      enabled: true,
      test_mode: false,
      require_3ds: true
    },
    cod: {
      enabled: true,
      max_amount: 250.0,
      area: 'all'
    },
    wing: {
      enabled: true,
      account: '+855 12 345 678'
    }
  },

  // 4. Shipping & Delivery
  free_shipping_enabled: true,
  free_shipping_mode: 'threshold', // 'threshold' | 'all_orders' | 'disabled'
  free_shipping_threshold: 50.0,
  free_shipping_promo_text: 'Complimentary nationwide shipping on orders over $50',
  free_shipping_carriers: ['vet_express', 'jt_express', 'lumea_concierge'],
  grab_subsidy_enabled: true,

  // 5. Taxes & Compliance
  tax_rate: 10.0,
  tax_inclusive: false,
  tax_id_number: 'K008-902341254',
  auto_invoice: true,

  // 6. Notifications
  notifications: {
    order_confirmation_email: true,
    shipping_updates_email: true,
    return_status_email: true,
    admin_low_stock_email: true,
    admin_notification_email: 'ops@lumea.com',
    telegram_alerts: true
  },

  // 7. Integrations
  integrations: {
    google_analytics_id: 'G-LUMEA2026',
    facebook_pixel_id: '9876543210123',
    telegram_bot_token: 'bot612849102:AAE-lumea-secure-token',
    telegram_chat_id: '@lumea_atelier_orders',
    telegram_enabled: true,
    klaviyo_api_key: 'pk_live_lumea_botanical'
  },

  // 8. SEO & Social
  seo: {
    meta_title: 'Luméa — Luxury Clinical Skincare & Botanical Atelier',
    meta_description: 'Discover pure, clinically backed botanical skincare crafted to nurture skin barrier resilience and reveal radiant luminescence.',
    og_image: '/images/banner-home.jpg',
    canonical_url: 'https://lumeastore.vercel.app',
    indexing_enabled: true
  },

  // 9. Appearance & Branding
  appearance: {
    announcement_enabled: true,
    announcement_text: 'Complimentary nationwide shipping on orders over $50 | 100% Authentic Guaranteed',
    primary_brand_color: '#84261B',
    products_per_page: 12,
    show_stock_badge: true,
    show_discount_badge: true
  },

  // 10. Legal & Policies
  legal: {
    return_policy_days: 14,
    warranty_guarantee: '100% Authenticity Guarantee or Full Refund',
    support_hours: 'Mon - Sun: 8:00 AM - 9:00 PM (ICT)'
  },

  // 11. Advanced
  maintenance_mode: false
})

const staffMembers = ref([
  { id: 1, name: 'Sreynich Chan', email: 'sreynich.chan@example.com', role: 'Super Admin · Full Access', avatar: '/images/avatar-sreynich.jpg', status: 'Active' },
  { id: 2, name: 'Luméa Operations', email: 'ops@lumea.com', role: 'Store Manager', avatar: '/images/avatars/avatar-default.png', status: 'Active' },
  { id: 3, name: 'Sokunthea Keo', email: 'sokunthea@lumea.com', role: 'Customer Care Specialist', avatar: '/images/avatar-clientele-2.jpg', status: 'Active' }
])

// Add Staff Modal state
const showStaffModal = ref(false)
const staffForm = reactive({
  name: '',
  email: '',
  role: 'Store Manager',
  avatar: '/images/avatars/avatar-default.png'
})

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
      for (const [k, v] of Object.entries(d)) {
        if (v && typeof v === 'object' && !Array.isArray(v)) {
          form[k] = { ...(form[k] || {}), ...v }
        } else if (k === 'store_phone' && typeof v === 'string') {
          form.store_phone = v.replace(/^\+855\s*/, '')
        } else if (k === 'staff_members' && Array.isArray(v) && v.length) {
          staffMembers.value = v
        } else if (v !== undefined && v !== null) {
          form[k] = v
        }
      }
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
      ...form,
      store_phone: `${form.phone_country_code} ${form.store_phone}`.trim(),
      staff_members: staffMembers.value
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

// Staff Member Handlers
function inviteStaffMember() {
  staffForm.name = ''
  staffForm.email = ''
  staffForm.role = 'Store Manager'
  staffForm.avatar = '/images/avatars/avatar-default.png'
  showStaffModal.value = true
}

function submitNewStaff() {
  if (!staffForm.name || !staffForm.email) {
    adminStore.addToast('Please enter both name and email for the staff member', 'error')
    return
  }
  const newId = staffMembers.value.length ? Math.max(...staffMembers.value.map(s => s.id)) + 1 : 1
  staffMembers.value.push({
    id: newId,
    name: staffForm.name.trim(),
    email: staffForm.email.trim(),
    role: staffForm.role,
    avatar: staffForm.avatar || '/images/avatars/avatar-default.png',
    status: 'Active'
  })
  showStaffModal.value = false
  adminStore.addToast(`Added ${staffForm.name} to atelier team`, 'success')
  saveSettings()
}

function toggleStaffStatus(id) {
  const staff = staffMembers.value.find(s => s.id === id)
  if (staff) {
    staff.status = staff.status === 'Active' ? 'Suspended' : 'Active'
    adminStore.addToast(`${staff.name} is now ${staff.status}`, 'info')
    saveSettings()
  }
}

function removeStaffMember(id) {
  if (staffMembers.value.length <= 1) {
    adminStore.addToast('Cannot remove the last remaining administrator', 'error')
    return
  }
  const staff = staffMembers.value.find(s => s.id === id)
  if (confirm(`Remove ${staff?.name || 'this team member'} from atelier operations?`)) {
    staffMembers.value = staffMembers.value.filter(s => s.id !== id)
    adminStore.addToast('Staff member removed', 'info')
    saveSettings()
  }
}

function testTelegramAlert() {
  const target = form.integrations?.telegram_chat_id || '@lumea_atelier_orders'
  adminStore.addToast(`Simulated dispatch alert sent to Telegram channel: ${target}`, 'success')
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
                <h2 class="pane-heading">Store Operations &amp; Policies</h2>
                <p class="pane-subheading">Operating currency, order numbering, and inventory thresholds.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Operating Currency</label>
                <select v-model="form.currency" class="field-select">
                  <option value="USD ($)">USD ($) — United States Dollar</option>
                  <option value="KHR (៛)">KHR (៛) — Cambodian Riel</option>
                  <option value="EUR (€)">EUR (€) — Euro</option>
                </select>
                <span class="field-hint">Primary currency used on product price tags and invoices.</span>
              </div>

              <div class="form-field">
                <label class="field-label">Order Number Prefix</label>
                <input v-model="form.order_prefix" type="text" class="field-input" placeholder="LM-" />
                <span class="field-hint">Appended before sequential order numbers (e.g. LM-10024).</span>
              </div>

              <div class="form-field">
                <label class="field-label">Low Stock Warning Threshold</label>
                <input v-model.number="form.low_stock_threshold" type="number" min="1" max="100" class="field-input" />
                <span class="field-hint">Products with inventory below this count trigger staff restock alerts.</span>
              </div>

              <div class="form-field">
                <label class="field-label">Cart Session Lifetime (Minutes)</label>
                <input v-model.number="form.cart_expiration_minutes" type="number" min="5" max="1440" class="field-input" />
                <span class="field-hint">Time before an inactive client shopping bag releases stock reservations.</span>
              </div>

              <div class="form-field col-span-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Auto-Confirm Paid Orders</strong>
                    <p class="toggle-desc">Automatically move orders with successful KHQR or card settlements to confirmed fulfillment status.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.auto_confirm_orders" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>

              <div class="form-field col-span-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Allow Backorders / Out-of-Stock Checkout</strong>
                    <p class="toggle-desc">Permit patrons to order newly arriving boutique stock when on-hand quantity is zero.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.allow_backorders" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 3: PAYMENTS -->
          <div v-else-if="activeTab === 'payments'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Payment Gateways &amp; Methods</h2>
                <p class="pane-subheading">Configure enabled checkout methods for storefront clientele.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="payment-methods-stack mt-4">
              <!-- Method 1: ABA PAY KHQR -->
              <div class="payment-method-box" :class="{ 'method-enabled': form.payment_methods?.aba_pay?.enabled }">
                <div class="method-header">
                  <div class="method-title-wrap">
                    <div class="method-icon-pill">KHQR</div>
                    <div>
                      <h4 class="method-name">ABA PAY (Bakong QR)</h4>
                      <p class="method-sub">Instant QR settlement with Cambodian banks and Bakong e-wallets.</p>
                    </div>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.payment_methods.aba_pay.enabled" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div v-if="form.payment_methods?.aba_pay?.enabled" class="method-fields-grid">
                  <div class="form-field">
                    <label class="field-label">Merchant Account Display Name</label>
                    <input v-model="form.payment_methods.aba_pay.merchant_name" type="text" class="field-input" placeholder="LUMEA ATELIER" />
                  </div>
                  <div class="form-field">
                    <label class="field-label">Bakong Account / Merchant ID</label>
                    <input v-model="form.payment_methods.aba_pay.merchant_id" type="text" class="field-input" placeholder="lumea_khqr@aba" />
                  </div>
                  <div class="form-field col-span-2">
                    <label class="field-checkbox-inline">
                      <input type="checkbox" v-model="form.payment_methods.aba_pay.test_mode" class="custom-checkbox" />
                      <span>Sandbox / Test Mode (Simulates instant scan verification without charging real accounts)</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Method 2: Credit / Debit Card -->
              <div class="payment-method-box mt-3" :class="{ 'method-enabled': form.payment_methods?.credit_card?.enabled }">
                <div class="method-header">
                  <div class="method-title-wrap">
                    <div class="method-icon-pill">CARD</div>
                    <div>
                      <h4 class="method-name">Credit &amp; Debit Cards (Visa / Mastercard)</h4>
                      <p class="method-sub">Direct international card payment processor via Stripe integration.</p>
                    </div>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.payment_methods.credit_card.enabled" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div v-if="form.payment_methods?.credit_card?.enabled" class="method-fields-grid">
                  <div class="form-field">
                    <label class="field-checkbox-inline">
                      <input type="checkbox" v-model="form.payment_methods.credit_card.require_3ds" class="custom-checkbox" />
                      <span>Enforce 3D Secure Verification on all international transactions</span>
                    </label>
                  </div>
                  <div class="form-field">
                    <label class="field-checkbox-inline">
                      <input type="checkbox" v-model="form.payment_methods.credit_card.test_mode" class="custom-checkbox" />
                      <span>Stripe Test Mode active (Accepts 4242 test card credentials)</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- Method 3: Cash on Delivery (COD) -->
              <div class="payment-method-box mt-3" :class="{ 'method-enabled': form.payment_methods?.cod?.enabled }">
                <div class="method-header">
                  <div class="method-title-wrap">
                    <div class="method-icon-pill">COD</div>
                    <div>
                      <h4 class="method-name">Cash on Delivery (COD)</h4>
                      <p class="method-sub">Client pays courier in cash upon package handover.</p>
                    </div>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.payment_methods.cod.enabled" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div v-if="form.payment_methods?.cod?.enabled" class="method-fields-grid">
                  <div class="form-field">
                    <label class="field-label">Maximum Allowed COD Total ($)</label>
                    <input v-model.number="form.payment_methods.cod.max_amount" type="number" step="10" class="field-input" placeholder="250.00" />
                    <span class="field-hint">Orders exceeding this total require digital pre-payment.</span>
                  </div>
                  <div class="form-field">
                    <label class="field-label">Delivery Coverage</label>
                    <select v-model="form.payment_methods.cod.area" class="field-select">
                      <option value="all">Nationwide (All 25 Provinces &amp; Cities)</option>
                      <option value="local_only">Phnom Penh Inner Ring Districts Only</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Method 4: Wing / TrueMoney -->
              <div class="payment-method-box mt-3" :class="{ 'method-enabled': form.payment_methods?.wing?.enabled }">
                <div class="method-header">
                  <div class="method-title-wrap">
                    <div class="method-icon-pill">WING</div>
                    <div>
                      <h4 class="method-name">Wing Bank &amp; TrueMoney</h4>
                      <p class="method-sub">Local mobile wallet settlement for Cambodian clientele.</p>
                    </div>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.payment_methods.wing.enabled" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div v-if="form.payment_methods?.wing?.enabled" class="method-fields-grid">
                  <div class="form-field">
                    <label class="field-label">Registered Merchant Phone / Account</label>
                    <input v-model="form.payment_methods.wing.account" type="text" class="field-input" placeholder="+855 12 345 678" />
                  </div>
                </div>
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
                <h2 class="pane-heading">Tax &amp; VAT Compliance</h2>
                <p class="pane-subheading">Configure value added tax calculation and invoice compliance.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Value Added Tax (VAT) %</label>
                <input v-model.number="form.tax_rate" type="number" step="0.5" class="field-input" placeholder="10.0" />
                <span class="field-hint">Standard Cambodian VAT applied to taxable beauty goods (Default 10%).</span>
              </div>

              <div class="form-field">
                <label class="field-label">Tax Identification Number (TIN)</label>
                <input v-model="form.tax_id_number" type="text" class="field-input" placeholder="K008-902341254" />
                <span class="field-hint">Printed on customer receipts and official merchant statements.</span>
              </div>

              <div class="form-field col-span-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Tax-Inclusive Product Pricing</strong>
                    <p class="toggle-desc">When enabled, storefront prices displayed to shoppers already include VAT. If disabled, tax is added at checkout.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.tax_inclusive" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>

              <div class="form-field col-span-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Automated Tax Invoice Generation</strong>
                    <p class="toggle-desc">Automatically generate itemized PDF invoices for customer orders upon payment verification.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.auto_invoice" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 6: NOTIFICATIONS -->
          <div v-else-if="activeTab === 'notifications'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Automated Notifications &amp; Alerts</h2>
                <p class="pane-subheading">Manage transactional email alerts sent to patrons and atelier staff.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="notifications-section mt-4">
              <h3 class="section-group-heading">Patron Transactional Emails</h3>
              <div class="toggles-stack mt-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Order Confirmation Email</strong>
                    <p class="toggle-desc">Dispatched immediately after payment authorization with receipt and ordered items.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.notifications.order_confirmation_email" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div class="atelier-toggle-card mt-2">
                  <div class="toggle-info">
                    <strong class="toggle-title">Fulfillment &amp; Courier Tracking Link</strong>
                    <p class="toggle-desc">Notifies the patron when their order package leaves our Phnom Penh atelier with courier waybill.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.notifications.shipping_updates_email" />
                    <span class="slider-round"></span>
                  </label>
                </div>

                <div class="atelier-toggle-card mt-2">
                  <div class="toggle-info">
                    <strong class="toggle-title">Return &amp; Refund Status Updates</strong>
                    <p class="toggle-desc">Alerts patron on return approval, package transit receipt, and completed refund vouchers.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.notifications.return_status_email" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>

              <h3 class="section-group-heading mt-6">Atelier Staff Operations Alerts</h3>
              <div class="form-body-grid mt-2">
                <div class="form-field col-span-2">
                  <label class="field-label">Staff Operations Alert Email</label>
                  <input v-model="form.notifications.admin_notification_email" type="email" class="field-input" placeholder="ops@lumea.com" />
                  <span class="field-hint">Receives low inventory notices, high value order reviews, and customer inquiries.</span>
                </div>

                <div class="form-field col-span-2">
                  <div class="atelier-toggle-card">
                    <div class="toggle-info">
                      <strong class="toggle-title">Low Inventory Stock Threshold Alerts</strong>
                      <p class="toggle-desc">Sends daily recap of boutique products with inventory below minimum safe stock.</p>
                    </div>
                    <label class="switch-control">
                      <input type="checkbox" v-model="form.notifications.admin_low_stock_email" />
                      <span class="slider-round"></span>
                    </label>
                  </div>
                </div>

                <div class="form-field col-span-2">
                  <div class="atelier-toggle-card">
                    <div class="toggle-info">
                      <strong class="toggle-title">Instant Telegram Order Alerts</strong>
                      <p class="toggle-desc">Broadcasts new order alerts to the private atelier Telegram channel for rapid dispatch.</p>
                    </div>
                    <label class="switch-control">
                      <input type="checkbox" v-model="form.notifications.telegram_alerts" />
                      <span class="slider-round"></span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 7: USERS & PERMISSIONS -->
          <div v-else-if="activeTab === 'users'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Staff &amp; Permissions</h2>
                <p class="pane-subheading">Atelier administrators, managers, and fulfillment team members.</p>
              </div>
              <button class="btn-save" @click="inviteStaffMember">
                <Users class="w-3.5 h-3.5 mr-1" />
                <span>Invite Team Member</span>
              </button>
            </div>

            <div class="staff-cards-grid mt-4">
              <div v-for="staff in staffMembers" :key="staff.id" class="staff-member-card">
                <img :src="staff.avatar" :alt="staff.name" class="staff-avatar-img" @error="$event.target.src = '/images/avatars/avatar-default.png'" />
                <div class="staff-details">
                  <div class="staff-top-line">
                    <strong class="staff-name-text">{{ staff.name }}</strong>
                    <span class="badge-status" :class="staff.status === 'Active' ? 'status-active' : 'status-pending'">{{ staff.status }}</span>
                  </div>
                  <span class="staff-role-text">{{ staff.role }}</span>
                  <span class="staff-email-text">{{ staff.email }}</span>
                </div>
                <div class="staff-actions-bar">
                  <button type="button" class="btn-action-text" @click="toggleStaffStatus(staff.id)">
                    {{ staff.status === 'Active' ? 'Suspend' : 'Activate' }}
                  </button>
                  <button type="button" class="btn-action-danger" title="Remove staff member" @click="removeStaffMember(staff.id)">
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 8: INTEGRATIONS -->
          <div v-else-if="activeTab === 'integrations'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Integrations &amp; Analytics</h2>
                <p class="pane-subheading">Connect third-party marketing, analytics, and messaging channels.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="integrations-grid mt-4">
              <!-- Google Analytics 4 -->
              <div class="integration-item-card">
                <div class="int-header">
                  <div class="int-brand">
                    <div class="int-icon-pill">GA4</div>
                    <div>
                      <h4 class="int-title">Google Analytics 4 &amp; GTM</h4>
                      <p class="int-desc">Track storefront patron visits, bounce rate, and conversion paths.</p>
                    </div>
                  </div>
                  <span class="badge-status status-active">Connected</span>
                </div>
                <div class="form-field mt-3">
                  <label class="field-label">Measurement ID (G-XXXXXXXXXX)</label>
                  <input v-model="form.integrations.google_analytics_id" type="text" class="field-input" placeholder="G-LUMEA2026" />
                </div>
              </div>

              <!-- Meta Pixel -->
              <div class="integration-item-card mt-3">
                <div class="int-header">
                  <div class="int-brand">
                    <div class="int-icon-pill">META</div>
                    <div>
                      <h4 class="int-title">Meta / Facebook Pixel</h4>
                      <p class="int-desc">Attribute Instagram &amp; Facebook campaign conversions and cart adds.</p>
                    </div>
                  </div>
                  <span class="badge-status status-active">Active</span>
                </div>
                <div class="form-field mt-3">
                  <label class="field-label">Pixel ID</label>
                  <input v-model="form.integrations.facebook_pixel_id" type="text" class="field-input" placeholder="9876543210123" />
                </div>
              </div>

              <!-- Telegram Alert Bot -->
              <div class="integration-item-card mt-3">
                <div class="int-header">
                  <div class="int-brand">
                    <div class="int-icon-pill">TG</div>
                    <div>
                      <h4 class="int-title">Telegram Order Notification Bot</h4>
                      <p class="int-desc">Push order notifications and high-priority returns to your phone.</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2">
                    <button type="button" class="btn-test-mini" @click="testTelegramAlert">Test Ping</button>
                    <label class="switch-control">
                      <input type="checkbox" v-model="form.integrations.telegram_enabled" />
                      <span class="slider-round"></span>
                    </label>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3 mt-3">
                  <div class="form-field">
                    <label class="field-label">Bot API Token</label>
                    <input v-model="form.integrations.telegram_bot_token" type="text" class="field-input" placeholder="bot612849102:AAE..." />
                  </div>
                  <div class="form-field">
                    <label class="field-label">Target Channel / Chat ID</label>
                    <input v-model="form.integrations.telegram_chat_id" type="text" class="field-input" placeholder="@lumea_atelier_orders" />
                  </div>
                </div>
              </div>

              <!-- Klaviyo / Mailchimp -->
              <div class="integration-item-card mt-3">
                <div class="int-header">
                  <div class="int-brand">
                    <div class="int-icon-pill">MAIL</div>
                    <div>
                      <h4 class="int-title">Klaviyo / Newsletter Marketing</h4>
                      <p class="int-desc">Sync customer newsletter subscribers and skin quiz lead contacts.</p>
                    </div>
                  </div>
                  <span class="badge-status status-active">Ready</span>
                </div>
                <div class="form-field mt-3">
                  <label class="field-label">Public API Key</label>
                  <input v-model="form.integrations.klaviyo_api_key" type="text" class="field-input" placeholder="pk_live_lumea_botanical" />
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 9: SEO & SOCIAL -->
          <div v-else-if="activeTab === 'seo'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Search Engine Optimization (SEO)</h2>
                <p class="pane-subheading">Manage organic search indexing, metadata, and social media share previews.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <!-- Live Google Snippet Preview -->
            <div class="google-snippet-preview mt-4">
              <span class="snippet-preview-label">Live Google Search Snippet Preview</span>
              <div class="google-card">
                <div class="google-top-line">
                  <img src="/favicon.ico" alt="Luméa" class="w-4 h-4 rounded-full" />
                  <span class="google-url">{{ form.seo?.canonical_url || 'https://lumeastore.vercel.app' }}</span>
                </div>
                <h3 class="google-title">{{ form.seo?.meta_title || 'Luméa — Luxury Clinical Skincare &amp; Botanical Atelier' }}</h3>
                <p class="google-desc">{{ form.seo?.meta_description || 'Discover pure, clinically backed botanical skincare crafted to nurture skin barrier resilience and reveal radiant luminescence.' }}</p>
              </div>
            </div>

            <div class="form-body-grid mt-4">
              <div class="form-field col-span-2">
                <label class="field-label">Default Meta Title</label>
                <input v-model="form.seo.meta_title" type="text" class="field-input" placeholder="Luméa — Luxury Clinical Skincare &amp; Botanical Atelier" />
                <span class="field-hint">Recommended under 60 characters for optimal display on search result pages.</span>
              </div>

              <div class="form-field col-span-2">
                <label class="field-label">Default Meta Description</label>
                <textarea v-model="form.seo.meta_description" rows="3" class="field-textarea" placeholder="Discover pure, clinically backed botanical skincare..."></textarea>
                <span class="field-hint">Brief summary shown under the page title in search engine results.</span>
              </div>

              <div class="form-field">
                <label class="field-label">Social Share (Open Graph) Image URL</label>
                <input v-model="form.seo.og_image" type="text" class="field-input" placeholder="/images/banner-home.jpg" />
              </div>

              <div class="form-field">
                <label class="field-label">Canonical Store URL</label>
                <input v-model="form.seo.canonical_url" type="text" class="field-input" placeholder="https://lumeastore.vercel.app" />
              </div>

              <div class="form-field col-span-2">
                <div class="atelier-toggle-card">
                  <div class="toggle-info">
                    <strong class="toggle-title">Allow Search Engine Indexing</strong>
                    <p class="toggle-desc">Instruct Google, Bing, and search crawlers to index your storefront catalog in search results.</p>
                  </div>
                  <label class="switch-control">
                    <input type="checkbox" v-model="form.seo.indexing_enabled" />
                    <span class="slider-round"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 10: APPEARANCE & BRANDING -->
          <div v-else-if="activeTab === 'appearance'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Storefront Appearance &amp; Branding</h2>
                <p class="pane-subheading">Customize announcement bar banner, brand palette, and product display rules.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <!-- Section 1: Announcement Bar -->
            <div class="appearance-card mt-4">
              <div class="appearance-header-row">
                <div>
                  <h4 class="appearance-sec-title">Storefront Announcement Bar Banner</h4>
                  <p class="appearance-sec-sub">Top bar visible across the storefront homepage, catalog, and checkout.</p>
                </div>
                <label class="switch-control">
                  <input type="checkbox" v-model="form.appearance.announcement_enabled" />
                  <span class="slider-round"></span>
                </label>
              </div>

              <div v-if="form.appearance.announcement_enabled" class="mt-3">
                <label class="field-label">Announcement Banner Text</label>
                <input v-model="form.appearance.announcement_text" type="text" class="field-input" placeholder="Complimentary nationwide shipping on orders over $50 | 100% Authentic Guaranteed" />
                
                <!-- Live preview banner -->
                <div class="live-announcement-preview mt-2">
                  <Sparkles class="w-3.5 h-3.5 text-crimson" />
                  <span>{{ form.appearance.announcement_text || 'Complimentary nationwide shipping on orders over $50' }}</span>
                </div>
              </div>
            </div>

            <!-- Section 2: Catalog Rules -->
            <div class="appearance-card mt-4">
              <h4 class="appearance-sec-title">Catalog &amp; Product Display Rules</h4>
              <div class="form-body-grid mt-3">
                <div class="form-field">
                  <label class="field-label">Products Per Page (Catalog Grid)</label>
                  <select v-model.number="form.appearance.products_per_page" class="field-select">
                    <option :value="8">8 Products per page</option>
                    <option :value="12">12 Products per page (Recommended)</option>
                    <option :value="16">16 Products per page</option>
                    <option :value="24">24 Products per page</option>
                  </select>
                </div>

                <div class="form-field">
                  <label class="field-label">Primary Brand Accent Color</label>
                  <div class="flex items-center gap-2">
                    <input v-model="form.appearance.primary_brand_color" type="color" class="color-picker-box" />
                    <input v-model="form.appearance.primary_brand_color" type="text" class="field-input" />
                  </div>
                </div>

                <div class="form-field col-span-2">
                  <div class="atelier-toggle-card">
                    <div class="toggle-info">
                      <strong class="toggle-title">Show Low-Stock Warning Pill</strong>
                      <p class="toggle-desc">Show "Only X left in stock" badge on product cards when stock drops below threshold.</p>
                    </div>
                    <label class="switch-control">
                      <input type="checkbox" v-model="form.appearance.show_stock_badge" />
                      <span class="slider-round"></span>
                    </label>
                  </div>
                </div>

                <div class="form-field col-span-2">
                  <div class="atelier-toggle-card">
                    <div class="toggle-info">
                      <strong class="toggle-title">Show Promotional Discount Badges</strong>
                      <p class="toggle-desc">Display promotional percentage badges (e.g. "-15% OFF") on discounted products.</p>
                    </div>
                    <label class="switch-control">
                      <input type="checkbox" v-model="form.appearance.show_discount_badge" />
                      <span class="slider-round"></span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 11: LEGAL & POLICIES -->
          <div v-else-if="activeTab === 'legal'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Legal &amp; Storefront Policies</h2>
                <p class="pane-subheading">Manage return timeframes, guarantee commitments, and policy links.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Return &amp; Exchange Window (Days)</label>
                <input v-model.number="form.legal.return_policy_days" type="number" min="1" max="90" class="field-input" placeholder="14" />
                <span class="field-hint">Days from delivery date within which patrons may submit return requests.</span>
              </div>

              <div class="form-field">
                <label class="field-label">Client Care Operating Hours</label>
                <input v-model="form.legal.support_hours" type="text" class="field-input" placeholder="Mon - Sun: 8:00 AM - 9:00 PM (ICT)" />
              </div>

              <div class="form-field col-span-2">
                <label class="field-label">Authenticity Warranty Guarantee</label>
                <input v-model="form.legal.warranty_guarantee" type="text" class="field-input" placeholder="100% Authenticity Guarantee or Full Refund" />
                <span class="field-hint">Highlighted on storefront product detail and checkout guarantees.</span>
              </div>
            </div>

            <!-- Direct links to Storefront Policy Pages -->
            <div class="policy-links-card mt-4">
              <h4 class="appearance-sec-title">Storefront Legal Pages</h4>
              <p class="appearance-sec-sub">Clients can view complete policy documents directly through these published routes.</p>
              <div class="policy-routes-grid mt-3">
                <a :href="getStorefrontUrl() + '/returns'" target="_blank" class="policy-route-item">
                  <FileText class="w-4 h-4 text-crimson" />
                  <span>Return &amp; Refund Policy</span>
                  <ExternalLink class="w-3.5 h-3.5 text-taupe ml-auto" />
                </a>
                <a :href="getStorefrontUrl() + '/shipping'" target="_blank" class="policy-route-item">
                  <Truck class="w-4 h-4 text-crimson" />
                  <span>Shipping &amp; Delivery Guide</span>
                  <ExternalLink class="w-3.5 h-3.5 text-taupe ml-auto" />
                </a>
                <a :href="getStorefrontUrl() + '/privacy-policy'" target="_blank" class="policy-route-item">
                  <ShieldCheck class="w-4 h-4 text-crimson" />
                  <span>Privacy Policy &amp; GDPR</span>
                  <ExternalLink class="w-3.5 h-3.5 text-taupe ml-auto" />
                </a>
                <a :href="getStorefrontUrl() + '/terms-of-service'" target="_blank" class="policy-route-item">
                  <FileText class="w-4 h-4 text-crimson" />
                  <span>Terms &amp; Conditions of Service</span>
                  <ExternalLink class="w-3.5 h-3.5 text-taupe ml-auto" />
                </a>
              </div>
            </div>
          </div>

          <!-- TAB 12: ADVANCED & SYSTEM -->
          <div v-else-if="activeTab === 'advanced'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Advanced System Controls</h2>
                <p class="pane-subheading">Maintenance mode, system diagnostics, and database snapshots.</p>
              </div>
              <button class="btn-save" :disabled="isSaving" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
              </button>
            </div>

            <!-- Maintenance Mode Card -->
            <div class="appearance-card mt-4" :class="{ 'card-warning': form.maintenance_mode }">
              <div class="appearance-header-row">
                <div>
                  <h4 class="appearance-sec-title">Storefront Maintenance Mode</h4>
                  <p class="appearance-sec-sub">Temporarily close storefront access to visitors during atelier inventory audits.</p>
                </div>
                <label class="switch-control">
                  <input type="checkbox" v-model="form.maintenance_mode" />
                  <span class="slider-round"></span>
                </label>
              </div>
              <div v-if="form.maintenance_mode" class="warning-callout mt-2">
                <AlertCircle class="w-4 h-4 text-crimson" />
                <span>Storefront is currently in Maintenance Mode. Non-admin visitors receive a maintenance notice.</span>
              </div>
            </div>

            <!-- System Cache Management -->
            <div class="appearance-card mt-4">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="appearance-sec-title">System Cache &amp; Query Buffers</h4>
                  <p class="appearance-sec-sub">Clear temporary cache buffers to force reload of product categories and settings.</p>
                </div>
                <button type="button" class="btn-save" :disabled="isClearingCache" @click="handleClearCache">
                  <RefreshCw class="w-3.5 h-3.5 mr-1" :class="{ 'animate-spin': isClearingCache }" />
                  <span>{{ isClearingCache ? 'Clearing...' : 'Clear System Cache' }}</span>
                </button>
              </div>
            </div>

            <!-- Data Export & Backups -->
            <div class="appearance-card mt-4">
              <h4 class="appearance-sec-title">Data Snapshots &amp; Configuration Backups</h4>
              <p class="appearance-sec-sub">Export or reset your atelier configurations.</p>
              <div class="flex flex-wrap gap-2 mt-3">
                <button type="button" class="btn-outline-action" @click="exportSettingsFile">
                  <Download class="w-3.5 h-3.5 mr-1" />
                  <span>Export Settings JSON</span>
                </button>
                <button type="button" class="btn-outline-action" @click="backupStoreData">
                  <Database class="w-3.5 h-3.5 mr-1" />
                  <span>Download Store Backup</span>
                </button>
                <button type="button" class="btn-outline-action danger" @click="resetSettings">
                  <RotateCcw class="w-3.5 h-3.5 mr-1" />
                  <span>Reset to Factory Defaults</span>
                </button>
              </div>
            </div>

            <!-- Diagnostics -->
            <div class="appearance-card mt-4">
              <h4 class="appearance-sec-title">Environment Diagnostics</h4>
              <div class="diagnostics-grid mt-2">
                <div class="diag-item">
                  <span class="diag-label">Application Framework:</span>
                  <span class="diag-val">Python 3.12 · FastAPI</span>
                </div>
                <div class="diag-item">
                  <span class="diag-label">Database Engine:</span>
                  <span class="diag-val">SQLite (Local) / PostgreSQL (Neon)</span>
                </div>
                <div class="diag-item">
                  <span class="diag-label">Storefront Architecture:</span>
                  <span class="diag-val">Vue.js 3 Composition API · Pinia</span>
                </div>
                <div class="diag-item">
                  <span class="diag-label">Media Asset Storage:</span>
                  <span class="diag-val">{{ uploadStatus.enabled ? 'Active (' + uploadStatus.storage_type + ')' : 'Local File Storage' }}</span>
                </div>
              </div>
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
      <!-- Add Staff Modal Dialog -->
      <div v-if="showStaffModal" class="modal-backdrop" @click="showStaffModal = false">
        <div class="staff-modal-card" @click.stop>
          <div class="staff-modal-header">
            <div>
              <h3 class="modal-title font-serif text-lg font-bold text-charcoal">Invite Atelier Staff Member</h3>
              <p class="text-xs text-taupe mt-0.5">Grant console management access to team members.</p>
            </div>
            <button class="btn-close-modal" @click="showStaffModal = false" aria-label="Close dialog">
              <X :size="18" />
            </button>
          </div>

          <form @submit.prevent="submitNewStaff" class="modal-body-form">
            <div class="form-field">
              <label class="field-label">Full Name *</label>
              <input v-model="staffForm.name" type="text" class="field-input" placeholder="e.g. Sreymom Meas" required />
            </div>

            <div class="form-field mt-3">
              <label class="field-label">Email Address *</label>
              <input v-model="staffForm.email" type="email" class="field-input" placeholder="sreymom@lumea.com" required />
            </div>

            <div class="form-field mt-3">
              <label class="field-label">Role &amp; Permissions</label>
              <select v-model="staffForm.role" class="field-select">
                <option value="Super Admin · Full Access">Super Admin · Full Access</option>
                <option value="Store Manager">Store Manager · Orders &amp; Catalog</option>
                <option value="Customer Care Specialist">Customer Care Specialist · Inquiries &amp; Returns</option>
                <option value="Content Editor">Content Editor · Articles &amp; Banners</option>
              </select>
            </div>

            <div class="modal-actions-footer mt-4">
              <button type="button" class="btn-reset" @click="showStaffModal = false">Cancel</button>
              <button type="submit" class="btn-save">
                <Users class="w-3.5 h-3.5 mr-1" />
                <span>Save Staff Member</span>
              </button>
            </div>
          </form>
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
/* ========================================================
   ATELIER COMPLETE SETTINGS STYLES (TABS 2 - 12)
   ======================================================== */
.atelier-toggle-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 14px 18px;
}
.toggle-info {
  display: flex;
  flex-direction: column;
}
.toggle-title {
  font-size: 13px;
  font-weight: 700;
  color: #2D2621;
}
.toggle-desc {
  font-size: 11.5px;
  color: #786F68;
  margin-top: 2px;
}

/* Payment Methods */
.payment-methods-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.payment-method-box {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 16px 20px;
  transition: all 0.2s ease;
}
.payment-method-box.method-enabled {
  border-color: #84261B;
  background: #FFFDFD;
}
.method-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.method-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}
.method-icon-pill {
  font-family: monospace;
  font-size: 11px;
  font-weight: 800;
  background: #FAF2EE;
  color: #84261B;
  border: 1px solid #E8D7D2;
  padding: 4px 8px;
  border-radius: 6px;
}
.method-name {
  font-size: 14px;
  font-weight: 700;
  color: #2D2621;
  margin: 0;
}
.method-sub {
  font-size: 12px;
  color: #8C847E;
  margin: 2px 0 0 0;
}
.method-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px dashed #EFE7E0;
}
.field-checkbox-inline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #5C554F;
  cursor: pointer;
}

/* Staff Cards */
.staff-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}
.staff-member-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.staff-avatar-img {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EFE7E0;
}
.staff-details {
  display: flex;
  flex-direction: column;
}
.staff-top-line {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.staff-name-text {
  font-size: 14px;
  color: #2D2621;
}
.staff-role-text {
  font-size: 12px;
  font-weight: 600;
  color: #84261B;
  margin-top: 2px;
}
.staff-email-text {
  font-size: 11.5px;
  color: #8C847E;
  margin-top: 2px;
}
.staff-actions-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid #F3EDE7;
}
.btn-action-text {
  background: none;
  border: none;
  font-size: 12px;
  font-weight: 600;
  color: #84261B;
  cursor: pointer;
  padding: 0;
}
.btn-action-text:hover {
  text-decoration: underline;
}
.btn-action-danger {
  background: #FEF2F2;
  border: 1px solid #FEE2E2;
  color: #DC2626;
  padding: 5px;
  border-radius: 6px;
  cursor: pointer;
}

/* Integrations */
.integrations-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.integration-item-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 18px 20px;
}
.int-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.int-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.int-icon-pill {
  font-family: monospace;
  font-size: 11px;
  font-weight: 800;
  background: #FAF2EE;
  color: #84261B;
  border: 1px solid #E8D7D2;
  padding: 4px 8px;
  border-radius: 6px;
}
.int-title {
  font-size: 14px;
  font-weight: 700;
  color: #2D2621;
  margin: 0;
}
.int-desc {
  font-size: 12px;
  color: #8C847E;
  margin: 2px 0 0 0;
}
.btn-test-mini {
  background: #FAF7F4;
  border: 1px solid #D6CEC7;
  font-size: 11.5px;
  font-weight: 600;
  color: #5C554F;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-test-mini:hover {
  background: #FAF0EC;
  border-color: #84261B;
  color: #84261B;
}

/* Google Snippet Preview */
.google-snippet-preview {
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 16px 20px;
}
.snippet-preview-label {
  display: block;
  font-size: 11.5px;
  font-weight: 700;
  color: #8C847E;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}
.google-card {
  background: #FFFFFF;
  border: 1px solid #E5DFD9;
  border-radius: 8px;
  padding: 14px 18px;
}
.google-top-line {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.google-url {
  font-size: 12px;
  color: #202124;
}
.google-title {
  font-size: 16px;
  font-weight: 600;
  color: #1A0DAB;
  margin: 2px 0 4px 0;
  line-height: 1.3;
}
.google-desc {
  font-size: 12.5px;
  color: #4D5156;
  margin: 0;
  line-height: 1.4;
}

/* Appearance */
.appearance-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 18px 20px;
}
.appearance-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.appearance-sec-title {
  font-size: 14px;
  font-weight: 700;
  color: #2D2621;
  margin: 0;
}
.appearance-sec-sub {
  font-size: 12px;
  color: #8C847E;
  margin: 2px 0 0 0;
}
.live-announcement-preview {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #84261B;
  color: #FFFFFF;
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 8px;
  width: 100%;
}
.live-announcement-preview .text-crimson {
  color: #FBBF24 !important;
}
.color-picker-box {
  width: 40px;
  height: 40px;
  padding: 2px;
  border-radius: 8px;
  border: 1px solid #E5DFD9;
  cursor: pointer;
}

/* Policy Routes */
.policy-links-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 18px 20px;
}
.policy-routes-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.policy-route-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 12px 14px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
  color: #2D2621;
  transition: all 0.2s ease;
}
.policy-route-item:hover {
  background: #FAF0EC;
  border-color: #84261B;
  color: #84261B;
}

/* Advanced */
.card-warning {
  border-color: #F59E0B !important;
  background: #FFFDF9 !important;
}
.warning-callout {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FEF3C7;
  border: 1px solid #FDE68A;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12.5px;
  color: #92400E;
}
.btn-outline-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFFFFF;
  border: 1px solid #D6CEC7;
  color: #2D2621;
  font-size: 12.5px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}
.btn-outline-action:hover {
  background: #FAF7F4;
}
.btn-outline-action.danger {
  color: #DC2626;
  border-color: #FCA5A5;
}
.btn-outline-action.danger:hover {
  background: #FEF2F2;
}
.diagnostics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.diag-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
}
.diag-label {
  color: #786F68;
}
.diag-val {
  font-weight: 600;
  color: #2D2621;
}

/* Staff Modal */
.staff-modal-card {
  background: #FFFFFF;
  border-radius: 16px;
  width: 100%;
  max-width: 480px;
  overflow: hidden;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
}
.staff-modal-header {
  padding: 18px 24px;
  border-bottom: 1px solid #EFE7E0;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.modal-body-form {
  padding: 20px 24px;
}
.modal-actions-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid #EFE7E0;
}
</style>
