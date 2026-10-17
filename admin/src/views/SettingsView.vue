<script setup>
import { ref, reactive, onMounted } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
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
  ChevronDown
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
  free_shipping_threshold: 50.0,
  tax_rate: 10.0,
  online_status: 'Online'
})

// Load settings from backend API
onMounted(async () => {
  await loadSettings()
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
      form.free_shipping_threshold = d.free_shipping_threshold ?? form.free_shipping_threshold
      form.tax_rate = d.tax_rate ?? form.tax_rate
      form.online_status = d.online_status || form.online_status
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
      company_name: form.company_name,
      business_reg_number: form.business_reg_number,
      business_address: form.business_address,
      time_zone: form.time_zone,
      currency: form.currency,
      free_shipping_threshold: form.free_shipping_threshold,
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
  adminStore.addToast('Store database backup generated and downloaded', 'success')
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
                      <span class="logo-text-display">Luméa</span>
                    </div>
                    <div class="logo-btn-col">
                      <button class="btn-change-box" @click="alert('Upload new atelier store logo...')">
                        <Upload class="w-3 h-3 mr-1" />
                        <span>Change Logo</span>
                      </button>
                      <button class="btn-remove-box" @click="alert('Logo reset to default')">
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
                      <svg viewBox="0 0 24 24" class="w-5 h-5 text-crimson fill-crimson">
                        <path d="M12 2C6.5 2 2 6.5 2 12c0 5.5 4.5 10 10 10s10-4.5 10-10c0-5.5-4.5-10-10-10zm-1 14.5c-2.5 0-4.5-2-4.5-4.5S8.5 7.5 11 7.5s4.5 2 4.5 4.5-2 4.5-4.5 4.5z"/>
                      </svg>
                    </div>
                    <div class="logo-btn-col">
                      <button class="btn-change-box" @click="alert('Upload new favicon...')">
                        <Upload class="w-3 h-3 mr-1" />
                        <span>Change Favicon</span>
                      </button>
                      <button class="btn-remove-box" @click="alert('Favicon reset to default')">
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

          <!-- TAB 4: SHIPPING -->
          <div v-else-if="activeTab === 'shipping'" class="config-content">
            <div class="pane-header-row">
              <div>
                <h2 class="pane-heading">Shipping & Delivery Rates</h2>
                <p class="pane-subheading">Manage courier fees and free delivery rules.</p>
              </div>
              <button class="btn-save" @click="saveSettings">
                <Save class="w-3.5 h-3.5 mr-1" />
                <span>Save Changes</span>
              </button>
            </div>
            <div class="form-body-grid mt-4">
              <div class="form-field">
                <label class="field-label">Free Shipping Minimum Threshold ($)</label>
                <input v-model="form.free_shipping_threshold" type="number" class="field-input" />
              </div>
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
              <button class="btn-save" @click="alert('Invite staff member...')">
                <Users class="w-3.5 h-3.5 mr-1" />
                <span>Add Staff</span>
              </button>
            </div>
            <div class="staff-list mt-4">
              <div class="staff-card">
                <img src="/images/avatar-sreynich.jpg" class="w-10 h-10 rounded-full object-cover" />
                <div class="ml-3 flex-1">
                  <span class="font-semibold text-sm text-charcoal block">Sreynich Chan</span>
                  <span class="text-xs text-taupe">Super Admin · Full Access</span>
                </div>
                <span class="badge-status status-active">Active</span>
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
              <a href="http://localhost:5173" target="_blank" class="btn-view-store">
                <ExternalLink class="w-4 h-4 mr-1.5" />
                <span>View Store</span>
              </a>
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
                  <span class="action-desc">Download a backup of your store data.</span>
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
              <div class="quick-action-item" @click="alert('Import settings JSON dialog...')">
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

@media (max-width: 1200px) {
  .settings-workspace {
    grid-template-columns: 1fr;
  }
}
</style>
