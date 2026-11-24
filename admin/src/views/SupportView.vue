<script setup>
import { onMounted, ref, computed } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
import {
  MessageSquare,
  Clock,
  CheckCircle2,
  ShieldCheck,
  Search,
  RefreshCw,
  Mail,
  Send,
  Trash2,
  X,
  ExternalLink,
  Sparkles,
  User,
  Calendar,
  AlertCircle
} from 'lucide-vue-next'

const adminStore = useAdminStore()

const messages = ref([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const activeTab = ref('all') // 'all' | 'pending' | 'replied' | 'resolved'
const isSubmittingReply = ref(false)
const isSeeding = ref(false)

// Active Modal for viewing / replying to an inquiry
const selectedInquiry = ref(null)
const replyText = ref('')
const replyStatus = ref('replied')

async function load() {
  loading.value = true
  error.value = ''
  try {
    const res = await apiClient.get('/contact')
    const list = Array.isArray(res.data) ? res.data : (res.data?.data || [])
    messages.value = list
  } catch (err) {
    error.value = 'Unable to load customer inquiries. Please verify authentication or server connection.'
    console.error('Failed to load inquiries:', err)
  } finally {
    loading.value = false
  }
}

onMounted(load)

// Helper to normalize status
function normalizeStatus(st) {
  const s = (st || '').toLowerCase().trim()
  if (s === 'replied' || s === 'in_progress') return 'replied'
  if (s === 'resolved' || s === 'closed') return 'resolved'
  return 'pending'
}

// KPI Counts
const countAll = computed(() => messages.value.length)
const countPending = computed(() => messages.value.filter(m => normalizeStatus(m.status) === 'pending').length)
const countReplied = computed(() => messages.value.filter(m => normalizeStatus(m.status) === 'replied').length)
const countResolved = computed(() => messages.value.filter(m => normalizeStatus(m.status) === 'resolved').length)

// Filtered List
const filteredMessages = computed(() => {
  let list = messages.value || []

  // Tab filter
  if (activeTab.value !== 'all') {
    list = list.filter(m => normalizeStatus(m.status) === activeTab.value)
  }

  // Search filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(m =>
      (m.reference || '').toLowerCase().includes(q) ||
      (m.name || '').toLowerCase().includes(q) ||
      (m.email || '').toLowerCase().includes(q) ||
      (m.subject || '').toLowerCase().includes(q) ||
      (m.message || '').toLowerCase().includes(q)
    )
  }

  return list
})

// Open Inspection / Reply Dialog
function openInquiryModal(inquiry) {
  selectedInquiry.value = { ...inquiry }
  replyText.value = inquiry.admin_reply || ''
  replyStatus.value = normalizeStatus(inquiry.status) === 'resolved' ? 'resolved' : 'replied'
}

function closeInquiryModal() {
  selectedInquiry.value = null
  replyText.value = ''
}

// Quick reply preset filler
function applyTemplate(type) {
  if (type === 'delivery') {
    replyText.value = `Warm greetings ${selectedInquiry.value?.name || 'Valued Patron'}, our Luméa concierge team has reviewed your order details. Your package is dispatched with express handling and the courier will contact you prior to arrival.`
  } else if (type === 'skincare') {
    replyText.value = `Warm greetings ${selectedInquiry.value?.name || 'Valued Patron'}, thank you for consulting our skincare atelier. Our clinical formulas are crafted with gentle botanicals suitable for sensitive skin. We recommend introducing active serums gradually into your evening ritual.`
  } else if (type === 'stock') {
    replyText.value = `Warm greetings ${selectedInquiry.value?.name || 'Valued Patron'}, this item has just arrived at our Phnom Penh atelier and fresh batches are now available for purchase on our storefront.`
  }
}

// Submit Reply / Update Status
async function submitReply() {
  if (!selectedInquiry.value) return
  isSubmittingReply.value = true
  try {
    const payload = {
      status: replyStatus.value,
      admin_reply: replyText.value
    }
    const res = await apiClient.patch(`/contact/${selectedInquiry.value.id}/status`, payload)
    if (res.data?.status === 'success') {
      adminStore.addToast(`Inquiry #${selectedInquiry.value.reference} updated to ${replyStatus.value}`, 'success')
      // Update local item
      const idx = messages.value.findIndex(m => m.id === selectedInquiry.value.id)
      if (idx !== -1) {
        messages.value[idx].status = replyStatus.value
        messages.value[idx].admin_reply = replyText.value
      }
      closeInquiryModal()
    }
  } catch (err) {
    adminStore.addToast('Failed to update inquiry status', 'error')
    console.error('Update status error:', err)
  } finally {
    isSubmittingReply.value = false
  }
}

// Quick Mark Resolved
async function quickResolve(inquiry) {
  try {
    const payload = {
      status: 'resolved',
      admin_reply: inquiry.admin_reply || 'Resolved by atelier operations.'
    }
    await apiClient.patch(`/contact/${inquiry.id}/status`, payload)
    inquiry.status = 'resolved'
    adminStore.addToast(`Inquiry #${inquiry.reference} marked as resolved`, 'success')
  } catch (err) {
    adminStore.addToast('Failed to mark inquiry as resolved', 'error')
  }
}

// Delete Inquiry
async function deleteInquiry(id) {
  if (!confirm('Are you sure you want to delete this customer inquiry?')) return
  try {
    await apiClient.delete(`/contact/${id}`)
    messages.value = messages.value.filter(m => m.id !== id)
    adminStore.addToast('Inquiry removed successfully', 'info')
    if (selectedInquiry.value?.id === id) {
      closeInquiryModal()
    }
  } catch (err) {
    adminStore.addToast('Failed to delete inquiry', 'error')
  }
}

// Seed Demo Inquiries
async function seedDemoInquiries() {
  isSeeding.value = true
  try {
    const res = await apiClient.post('/contact/seed-demo')
    if (res.data?.status === 'success') {
      adminStore.addToast('Sample concierge inquiries seeded successfully', 'success')
      await load()
    }
  } catch (err) {
    adminStore.addToast('Failed to seed demo inquiries', 'error')
  } finally {
    isSeeding.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return 'Recent'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch {
    return dateStr
  }
}
</script>

<template>
  <div class="support-inquiries-page">
    <!-- Top Header Banner -->
    <div class="page-top-header">
      <div>
        <div class="breadcrumb-pill">
          <MessageSquare :size="13" class="text-crimson" />
          <span>Atelier Client Care</span>
        </div>
        <h1 class="page-main-title">Customer Inquiries &amp; Concierge</h1>
        <p class="page-main-sub">
          Review, respond to, and resolve client inquiries received through the storefront contact form.
        </p>
      </div>

      <div class="header-action-buttons">
        <button
          v-if="messages.length <= 1"
          class="btn-seed"
          :disabled="isSeeding"
          @click="seedDemoInquiries"
        >
          <Sparkles :size="15" />
          <span>{{ isSeeding ? 'Seeding...' : 'Load Demo Inquiries' }}</span>
        </button>

        <button class="btn-refresh" :disabled="loading" @click="load">
          <RefreshCw :size="15" :class="{ 'animate-spin': loading }" />
          <span>Refresh</span>
        </button>
      </div>
    </div>

    <!-- 4 Pastel KPI Cards -->
    <div class="kpi-grid">
      <!-- 1. Total Inquiries -->
      <div class="kpi-card">
        <div class="kpi-icon-wrap rose-soft">
          <MessageSquare :size="20" class="text-crimson" />
        </div>
        <div class="kpi-info">
          <div class="kpi-top">
            <span class="kpi-num">{{ countAll }}</span>
            <span class="kpi-badge positive">All Time</span>
          </div>
          <div class="kpi-sub">
            <span class="kpi-label">Total Inquiries</span>
            <span class="kpi-compare">Client submissions</span>
          </div>
        </div>
      </div>

      <!-- 2. Pending Review -->
      <div class="kpi-card">
        <div class="kpi-icon-wrap rose-soft">
          <Clock :size="20" class="text-crimson" />
        </div>
        <div class="kpi-info">
          <div class="kpi-top">
            <span class="kpi-num">{{ countPending }}</span>
            <span class="kpi-badge" :class="countPending > 0 ? 'negative' : 'positive'">
              {{ countPending > 0 ? 'Needs Reply' : 'All Clear' }}
            </span>
          </div>
          <div class="kpi-sub">
            <span class="kpi-label">Pending Inquiries</span>
            <span class="kpi-compare">Awaiting concierge</span>
          </div>
        </div>
      </div>

      <!-- 3. Replied -->
      <div class="kpi-card">
        <div class="kpi-icon-wrap rose-soft">
          <CheckCircle2 :size="20" class="text-crimson" />
        </div>
        <div class="kpi-info">
          <div class="kpi-top">
            <span class="kpi-num">{{ countReplied }}</span>
            <span class="kpi-badge positive">In Progress</span>
          </div>
          <div class="kpi-sub">
            <span class="kpi-label">Replied Messages</span>
            <span class="kpi-compare">Follow-ups sent</span>
          </div>
        </div>
      </div>

      <!-- 4. Resolved -->
      <div class="kpi-card">
        <div class="kpi-icon-wrap rose-soft">
          <ShieldCheck :size="20" class="text-crimson" />
        </div>
        <div class="kpi-info">
          <div class="kpi-top">
            <span class="kpi-num">{{ countResolved }}</span>
            <span class="kpi-badge positive">Settled</span>
          </div>
          <div class="kpi-sub">
            <span class="kpi-label">Resolved Cases</span>
            <span class="kpi-compare">Client satisfied</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Card -->
    <div class="content-table-card">
      <!-- Toolbar: Search + Filter Tabs -->
      <div class="table-toolbar">
        <div class="search-input-wrap">
          <Search :size="15" class="search-icon" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search inquiries by client name, email, subject, or reference..."
            class="search-input"
          />
        </div>

        <div class="filter-tabs-pills">
          <button
            class="tab-pill"
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
          >
            All ({{ countAll }})
          </button>
          <button
            class="tab-pill"
            :class="{ active: activeTab === 'pending' }"
            @click="activeTab = 'pending'"
          >
            Pending ({{ countPending }})
          </button>
          <button
            class="tab-pill"
            :class="{ active: activeTab === 'replied' }"
            @click="activeTab = 'replied'"
          >
            Replied ({{ countReplied }})
          </button>
          <button
            class="tab-pill"
            :class="{ active: activeTab === 'resolved' }"
            @click="activeTab = 'resolved'"
          >
            Resolved ({{ countResolved }})
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="inquiry-alert-box error" role="alert">
        <AlertCircle :size="18" />
        <span>{{ error }}</span>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="inquiry-loading-state">
        <div class="spinner"></div>
        <span>Loading customer inquiries...</span>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredMessages.length === 0" class="inquiry-empty-state">
        <MessageSquare :size="48" class="empty-icon text-taupe" />
        <h3 class="empty-title">No customer inquiries found</h3>
        <p class="empty-sub">
          {{ searchQuery || activeTab !== 'all' ? 'Try adjusting your search query or filter pills.' : 'Client messages submitted via the storefront contact page will appear here.' }}
        </p>
        <div class="empty-actions">
          <button
            v-if="searchQuery || activeTab !== 'all'"
            class="btn-outline-sm"
            @click="searchQuery = ''; activeTab = 'all'"
          >
            Reset Filters
          </button>
          <button class="btn-primary-sm" :disabled="isSeeding" @click="seedDemoInquiries">
            <Sparkles :size="13" />
            <span>Load Demo Inquiries</span>
          </button>
        </div>
      </div>

      <!-- Table View -->
      <div v-else class="table-responsive-wrap">
        <table class="atelier-data-table">
          <thead>
            <tr>
              <th class="th-ref">Reference</th>
              <th class="th-client">Client Details</th>
              <th class="th-subject">Subject &amp; Message</th>
              <th class="th-date">Submitted Date</th>
              <th class="th-status">Status</th>
              <th class="th-actions">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredMessages" :key="item.id" class="table-row">
              <!-- Reference -->
              <td class="td-ref">
                <span class="ref-badge">{{ item.reference }}</span>
              </td>

              <!-- Client Details -->
              <td class="td-client">
                <div class="client-cell">
                  <div class="client-avatar">
                    <User :size="15" />
                  </div>
                  <div class="client-meta">
                    <strong class="client-name">{{ item.name }}</strong>
                    <a :href="`mailto:${item.email}`" class="client-email">{{ item.email }}</a>
                  </div>
                </div>
              </td>

              <!-- Subject & Message Preview -->
              <td class="td-subject">
                <div class="subject-cell">
                  <strong class="subject-title">{{ item.subject }}</strong>
                  <p class="message-preview">{{ item.message }}</p>
                  <div v-if="item.admin_reply" class="reply-indicator">
                    <span class="reply-dot"></span>
                    <span class="reply-preview-text">Atelier reply recorded</span>
                  </div>
                </div>
              </td>

              <!-- Submitted Date -->
              <td class="td-date">
                <div class="date-cell">
                  <Calendar :size="13" class="text-taupe" />
                  <span>{{ formatDate(item.created_at) }}</span>
                </div>
              </td>

              <!-- Status -->
              <td class="td-status">
                <span
                  class="status-pill"
                  :class="{
                    'status-pending': normalizeStatus(item.status) === 'pending',
                    'status-replied': normalizeStatus(item.status) === 'replied',
                    'status-resolved': normalizeStatus(item.status) === 'resolved'
                  }"
                >
                  <span class="dot"></span>
                  <span>{{ normalizeStatus(item.status) === 'pending' ? 'Pending' : (normalizeStatus(item.status) === 'replied' ? 'Replied' : 'Resolved') }}</span>
                </span>
              </td>

              <!-- Actions -->
              <td class="td-actions">
                <div class="actions-group">
                  <button
                    class="btn-action-primary"
                    @click="openInquiryModal(item)"
                    aria-label="View and reply to inquiry"
                  >
                    <span>View &amp; Reply</span>
                  </button>
                  <button
                    v-if="normalizeStatus(item.status) !== 'resolved'"
                    class="btn-action-resolve"
                    title="Quick mark as resolved"
                    @click="quickResolve(item)"
                  >
                    <CheckCircle2 :size="15" />
                  </button>
                  <button
                    class="btn-action-delete"
                    title="Delete inquiry"
                    @click="deleteInquiry(item.id)"
                  >
                    <Trash2 :size="14" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Inquiry Details & Concierge Reply Modal -->
    <div v-if="selectedInquiry" class="modal-backdrop" @click="closeInquiryModal">
      <div class="inquiry-modal-card" @click.stop>
        <!-- Modal Header -->
        <div class="modal-header">
          <div class="modal-header-left">
            <div class="ref-pill">{{ selectedInquiry.reference }}</div>
            <h3 class="modal-title">{{ selectedInquiry.subject }}</h3>
          </div>
          <button class="btn-close-modal" @click="closeInquiryModal" aria-label="Close dialog">
            <X :size="18" />
          </button>
        </div>

        <!-- Modal Body (Scrollable) -->
        <div class="modal-body">
          <!-- Client Card -->
          <div class="client-detail-card">
            <div class="client-row">
              <div class="client-avatar-lg">
                <User :size="20" />
              </div>
              <div class="client-info-lg">
                <h4 class="name-lg">{{ selectedInquiry.name }}</h4>
                <div class="contact-links">
                  <a :href="`mailto:${selectedInquiry.email}`" class="contact-link">
                    <Mail :size="13" />
                    <span>{{ selectedInquiry.email }}</span>
                  </a>
                  <span class="time-stamp">
                    <Calendar :size="13" />
                    <span>{{ formatDate(selectedInquiry.created_at) }}</span>
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Client Message Box -->
          <div class="message-section">
            <label class="section-label">Client Message</label>
            <div class="client-message-quote">
              <p>{{ selectedInquiry.message }}</p>
            </div>
          </div>

          <!-- Quick Templates Bar -->
          <div class="templates-section">
            <span class="templates-label">Quick Response Presets:</span>
            <div class="templates-buttons">
              <button type="button" class="btn-preset" @click="applyTemplate('delivery')">
                Courier Tracking
              </button>
              <button type="button" class="btn-preset" @click="applyTemplate('skincare')">
                Routine Consultation
              </button>
              <button type="button" class="btn-preset" @click="applyTemplate('stock')">
                Stock Replenished
              </button>
            </div>
          </div>

          <!-- Atelier Reply Form -->
          <div class="reply-section">
            <label class="section-label" for="reply-textarea">
              Atelier Concierge Response
            </label>
            <textarea
              id="reply-textarea"
              v-model="replyText"
              rows="5"
              placeholder="Compose your personalized atelier reply to the client..."
              class="reply-textarea"
            ></textarea>
          </div>

          <!-- Status Selector -->
          <div class="status-choice-section">
            <label class="section-label">Update Inquiry Status</label>
            <div class="status-radio-group">
              <label class="radio-card" :class="{ selected: replyStatus === 'pending' }">
                <input type="radio" v-model="replyStatus" value="pending" class="radio-input" />
                <span class="radio-label">Pending</span>
              </label>
              <label class="radio-card" :class="{ selected: replyStatus === 'replied' }">
                <input type="radio" v-model="replyStatus" value="replied" class="radio-input" />
                <span class="radio-label">Replied</span>
              </label>
              <label class="radio-card" :class="{ selected: replyStatus === 'resolved' }">
                <input type="radio" v-model="replyStatus" value="resolved" class="radio-input" />
                <span class="radio-label">Resolved</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeInquiryModal">Cancel</button>
          <button
            class="btn-send-reply"
            :disabled="isSubmittingReply || !replyText.trim()"
            @click="submitReply"
          >
            <Send :size="15" />
            <span>{{ isSubmittingReply ? 'Saving...' : 'Save &amp; Record Reply' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.support-inquiries-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Header */
.page-top-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 16px;
  padding: 24px 28px;
}

.breadcrumb-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #84261B;
  background: #FAF5F2;
  border: 1px solid #EAE0D8;
  padding: 4px 10px;
  border-radius: 9999px;
  margin-bottom: 8px;
}

.page-main-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 24px;
  font-weight: 700;
  color: #2D2621;
  margin: 0 0 6px 0;
}

.page-main-sub {
  font-size: 13px;
  color: #8C847E;
  margin: 0;
}

.header-action-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-seed {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #FAF7F4;
  color: #84261B;
  border: 1px solid #E8D7D2;
  font-size: 13px;
  font-weight: 600;
  padding: 9px 16px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-seed:hover {
  background: #FAF0EC;
  border-color: #84261B;
}

.btn-refresh {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #FFFFFF;
  color: #2D2621;
  border: 1px solid #E5DFD9;
  font-size: 13px;
  font-weight: 600;
  padding: 9px 16px;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-refresh:hover {
  background: #FAF7F4;
}

/* 4 KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.kpi-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.kpi-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rose-soft {
  background: #FAF2EF;
}

.kpi-info {
  flex: 1;
  min-width: 0;
}

.kpi-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.kpi-num {
  font-size: 26px;
  font-weight: 700;
  color: #2D2621;
  line-height: 1;
}

.kpi-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 9999px;
}

.kpi-badge.positive {
  background: #E8F5E9;
  color: #2E7D32;
}

.kpi-badge.negative {
  background: #FEE2E2;
  color: #DC2626;
}

.kpi-sub {
  display: flex;
  flex-direction: column;
}

.kpi-label {
  font-size: 13px;
  font-weight: 600;
  color: #5C554F;
}

.kpi-compare {
  font-size: 11px;
  color: #A39B94;
}

/* Table Card */
.content-table-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.table-toolbar {
  padding: 18px 24px;
  border-bottom: 1px solid #EFE7E0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input-wrap {
  position: relative;
  flex: 1;
  min-width: 260px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #8C847E;
}

.search-input {
  width: 100%;
  height: 40px;
  padding: 0 14px 0 38px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 10px;
  font-size: 13px;
  color: #2D2621;
  outline: none;
  transition: all 0.2s ease;
}
.search-input:focus {
  background: #FFFFFF;
  border-color: #84261B;
  box-shadow: 0 0 0 3px rgba(132, 38, 27, 0.08);
}

.filter-tabs-pills {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #FAF7F4;
  padding: 4px;
  border-radius: 10px;
  border: 1px solid #EFE7E0;
}

.tab-pill {
  border: none;
  background: transparent;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #786F68;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.tab-pill.active {
  background: #84261B;
  color: #FFFFFF;
}

/* Table */
.table-responsive-wrap {
  overflow-x: auto;
}

.atelier-data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.atelier-data-table th {
  background: #FAF7F4;
  color: #786F68;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 14px 20px;
  border-bottom: 1px solid #EFE7E0;
}

.atelier-data-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #F3EDE7;
  vertical-align: middle;
}

.table-row:hover td {
  background: #FAF7F4;
}

/* Cell content */
.ref-badge {
  display: inline-block;
  font-family: monospace;
  font-size: 12px;
  font-weight: 700;
  color: #84261B;
  background: #FAF2EE;
  border: 1px solid #EAE0D8;
  padding: 3px 8px;
  border-radius: 6px;
}

.client-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.client-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #FAF0EB;
  color: #84261B;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.client-meta {
  display: flex;
  flex-direction: column;
}

.client-name {
  font-size: 13px;
  color: #2D2621;
}

.client-email {
  font-size: 12px;
  color: #8C847E;
  text-decoration: none;
}
.client-email:hover {
  color: #84261B;
  text-decoration: underline;
}

.subject-cell {
  max-width: 380px;
}

.subject-title {
  display: block;
  font-size: 13px;
  color: #2D2621;
  margin-bottom: 4px;
}

.message-preview {
  font-size: 12px;
  color: #786F68;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 360px;
}

.reply-indicator {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #059669;
  font-weight: 600;
  margin-top: 4px;
}

.reply-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #059669;
}

.date-cell {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #786F68;
  white-space: nowrap;
}

/* Status Pill */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 9999px;
  white-space: nowrap;
}

.status-pill .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-pending {
  background: #FEF3C7;
  color: #92400E;
}
.status-pending .dot {
  background: #D97706;
}

.status-replied {
  background: #EDE9FE;
  color: #6D28D9;
}
.status-replied .dot {
  background: #8B5CF6;
}

.status-resolved {
  background: #D1FAE5;
  color: #065F46;
}
.status-resolved .dot {
  background: #059669;
}

/* Action buttons */
.actions-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-action-primary {
  background: #84261B;
  color: #FFFFFF;
  border: none;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.btn-action-primary:hover {
  background: #73382E;
}

.btn-action-resolve {
  background: #F0FDF4;
  color: #16A34A;
  border: 1px solid #DCFCE7;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}
.btn-action-resolve:hover {
  background: #DCFCE7;
}

.btn-action-delete {
  background: #FEF2F2;
  color: #DC2626;
  border: 1px solid #FEE2E2;
  padding: 6px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}
.btn-action-delete:hover {
  background: #FEE2E2;
}

/* Empty & Loading */
.inquiry-empty-state, .inquiry-loading-state {
  padding: 60px 24px;
  text-align: center;
}

.empty-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 20px;
  color: #2D2621;
  margin: 14px 0 6px 0;
}

.empty-sub {
  font-size: 13px;
  color: #8C847E;
  margin-bottom: 20px;
}

.empty-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-primary-sm {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 9999px;
  cursor: pointer;
}

.btn-outline-sm {
  background: #FFFFFF;
  color: #5C554F;
  border: 1px solid #D6CEC7;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 9999px;
  cursor: pointer;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  backdrop-filter: blur(2px);
}

.inquiry-modal-card {
  background: #FFFFFF;
  border-radius: 16px;
  width: 100%;
  max-width: 640px;
  max-height: 88vh;
  max-height: 88dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #EFE7E0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-shrink: 0;
}

.ref-pill {
  display: inline-block;
  font-family: monospace;
  font-size: 11px;
  font-weight: 700;
  color: #84261B;
  background: #FAF2EE;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 6px;
}

.modal-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 18px;
  color: #2D2621;
  margin: 0;
}

.btn-close-modal {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
}
.btn-close-modal:hover {
  color: #84261B;
  background: #FAF7F4;
}

.modal-body {
  padding: 22px 24px;
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.client-detail-card {
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 14px 18px;
}

.client-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.client-avatar-lg {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FAF0EC;
  color: #84261B;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.name-lg {
  font-size: 15px;
  color: #2D2621;
  margin: 0 0 4px 0;
}

.contact-links {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: #786F68;
}

.contact-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #84261B;
  text-decoration: none;
}
.contact-link:hover {
  text-decoration: underline;
}

.time-stamp {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.section-label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #5C554F;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}

.client-message-quote {
  background: #FFFFFF;
  border-left: 3px solid #84261B;
  border-top: 1px solid #EFE7E0;
  border-right: 1px solid #EFE7E0;
  border-bottom: 1px solid #EFE7E0;
  border-radius: 0 8px 8px 0;
  padding: 14px 18px;
  font-size: 13.5px;
  line-height: 1.6;
  color: #2D2621;
}

.templates-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.templates-label {
  font-size: 11px;
  font-weight: 600;
  color: #8C847E;
}

.templates-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-preset {
  background: #FAF7F4;
  border: 1px solid #E5DFD9;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: #5C554F;
  padding: 4px 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-preset:hover {
  background: #FAF0EC;
  border-color: #84261B;
  color: #84261B;
}

.reply-textarea {
  width: 100%;
  border: 1px solid #E5DFD9;
  border-radius: 10px;
  padding: 12px 14px;
  font-size: 13px;
  font-family: inherit;
  color: #2D2621;
  outline: none;
  resize: vertical;
}
.reply-textarea:focus {
  border-color: #84261B;
  box-shadow: 0 0 0 3px rgba(132, 38, 27, 0.08);
}

.status-radio-group {
  display: flex;
  gap: 10px;
}

.radio-card {
  flex: 1;
  border: 1px solid #E5DFD9;
  background: #FAF7F4;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}
.radio-card.selected {
  border-color: #84261B;
  background: #FAF2EE;
}

.radio-input {
  accent-color: #84261B;
}

.radio-label {
  font-size: 13px;
  font-weight: 600;
  color: #2D2621;
}

.modal-footer {
  padding: 14px 24px;
  border-top: 1px solid #EFE7E0;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  flex-shrink: 0;
  background: #FAF7F4;
}

.btn-cancel {
  background: #FFFFFF;
  border: 1px solid #D6CEC7;
  color: #5C554F;
  padding: 8px 16px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-send-reply {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 8px 20px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-send-reply:hover {
  background: #73382E;
}
.btn-send-reply:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  .table-toolbar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
