<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import {
  Star,
  ThumbsUp,
  MessageSquare,
  Clock,
  Ban,
  Search,
  ChevronDown,
  Calendar,
  ExternalLink,
  Eye,
  Edit2,
  MoreHorizontal,
  CheckCircle2,
  XCircle,
  Trash2,
  CornerDownRight,
  Send,
  Lightbulb,
  ArrowRight,
  Filter,
  Check,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const searchQuery = ref('')
const selectedProduct = ref('all')
const selectedRating = ref('all')
const selectedStatus = ref('all')
const selectedDateRange = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)
const selectedReviews = ref([])
const activeDropdown = ref(null)

// Modals
const inspectingReview = ref(null)
const replyingReview = ref(null)
const replyText = ref('')

// Load data
onMounted(async () => {
  await adminStore.fetchProducts()
  await loadReviews()
})

async function loadReviews() {
  await adminStore.fetchReviews({
    search: searchQuery.value || undefined,
    product_id: selectedProduct.value !== 'all' ? selectedProduct.value : undefined,
    rating: selectedRating.value !== 'all' ? selectedRating.value : undefined,
    status: selectedStatus.value !== 'all' ? selectedStatus.value : undefined,
    page: currentPage.value,
    limit: pageSize.value
  })
}

// Watch filters
function handleFilterChange() {
  currentPage.value = 1
  loadReviews()
}

// Checkbox multi-select
const allSelected = computed(() => {
  return adminStore.reviews.length > 0 && selectedReviews.value.length === adminStore.reviews.length
})

function toggleSelectAll() {
  if (allSelected.value) {
    selectedReviews.value = []
  } else {
    selectedReviews.value = adminStore.reviews.map(r => r.id)
  }
}

function toggleSelectReview(id) {
  const idx = selectedReviews.value.indexOf(id)
  if (idx > -1) {
    selectedReviews.value.splice(idx, 1)
  } else {
    selectedReviews.value.push(id)
  }
}

// Status Updates
async function updateStatus(review, newStatus) {
  activeDropdown.value = null
  const res = await adminStore.updateReviewStatus(review.id, newStatus)
  if (res.success && inspectingReview.value?.id === review.id) {
    inspectingReview.value.status = newStatus
  }
}

// Reply
function openReplyModal(review) {
  replyingReview.value = review
  replyText.value = review.admin_reply || ''
  activeDropdown.value = null
}

async function submitReply() {
  if (!replyingReview.value || !replyText.value.trim()) return
  const res = await adminStore.replyToReview(replyingReview.value.id, replyText.value.trim())
  if (res.success) {
    if (inspectingReview.value?.id === replyingReview.value.id) {
      inspectingReview.value.admin_reply = replyText.value.trim()
    }
    replyingReview.value = null
    replyText.value = ''
  }
}

// Delete
async function deleteReview(review) {
  if (!confirm(`Are you sure you want to permanently delete review #${review.id}?`)) return
  activeDropdown.value = null
  const res = await adminStore.deleteReview(review.id)
  if (res.success && inspectingReview.value?.id === review.id) {
    inspectingReview.value = null
  }
}

// Export CSV
function exportReviewsCSV() {
  const items = adminStore.reviews
  if (!items || items.length === 0) {
    adminStore.addToast('No reviews to export', 'error')
    return
  }
  const headers = ['ID', 'Customer', 'Product', 'Rating', 'Title', 'Comment', 'Status', 'Date']
  const rows = items.map(r => [
    r.id,
    `"${r.customer_name}"`,
    `"${r.product_name}"`,
    r.rating,
    `"${(r.title || '').replace(/"/g, '""')}"`,
    `"${(r.comment || '').replace(/"/g, '""')}"`,
    r.status,
    `"${r.created_at}"`
  ])
  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `lumea_reviews_export_${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  adminStore.addToast('Reviews exported successfully (CSV)', 'success')
}
</script>

<template>
  <div class="reviews-page">
      <!-- BREADCRUMB -->
      <div class="breadcrumb-bar">
        <span class="crumb-parent">Content</span>
        <span class="crumb-sep">></span>
        <span class="crumb-current">Reviews</span>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">Reviews Management</h1>
          <p class="hero-subtitle">Moderate and manage customer reviews to build trust and showcase real experiences.</p>
        </div>

        <div class="hero-art-side">
          <img src="/images/admin-hero-bottles.jpg" alt="Luméa Atelier Skincare" class="hero-art-img" />
          <div class="hero-quote">
            <span class="quote-line-1">Real people.</span>
            <span class="quote-line-2">Real results.</span>
          </div>
          <button class="btn-export-top" @click="exportReviewsCSV">
            <ExternalLink class="w-4 h-4" />
            <span>Export Reviews</span>
          </button>
        </div>
      </div>

      <!-- 5 KPI METRICS CARDS -->
      <div class="kpi-grid">
        <!-- Total Reviews -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Star class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.reviewsKpis.total_reviews?.toLocaleString() || '1,248' }}</span>
              <span class="kpi-badge positive">↗ +18%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Total Reviews</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- Average Rating -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <ThumbsUp class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.reviewsKpis.average_rating || '4.6' }}</span>
              <span class="kpi-badge positive">↗ +0.2</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Average Rating</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- Approved -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <MessageSquare class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.reviewsKpis.approved || '892' }}</span>
              <span class="kpi-badge positive">↗ +24%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Approved</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- Pending Approval -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Clock class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.reviewsKpis.pending_approval || '156' }}</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Pending Approval</span>
            </div>
          </div>
        </div>

        <!-- Rejected / Hidden -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Ban class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.reviewsKpis.rejected_hidden || '32' }}</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Rejected / Hidden</span>
            </div>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT SPLIT: TABLE (LEFT) + SIDEBAR WIDGETS (RIGHT) -->
      <div class="reviews-split-layout">
        <!-- LEFT: FILTERS & REVIEWS TABLE -->
        <div class="reviews-main-pane">
          <!-- FILTER TOOLBAR -->
          <div class="filter-toolbar">
            <div class="search-input-wrap">
              <Search class="search-icon w-4 h-4" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search reviews..."
                class="search-input"
                @keyup.enter="handleFilterChange"
              />
            </div>

            <!-- Product Dropdown -->
            <div class="filter-field">
              <label class="filter-label">Product</label>
              <select v-model="selectedProduct" class="filter-select" @change="handleFilterChange">
                <option value="all">All Products</option>
                <option v-for="prod in adminStore.products" :key="prod.id" :value="prod.id">
                  {{ prod.name }}
                </option>
              </select>
            </div>

            <!-- Rating Dropdown -->
            <div class="filter-field">
              <label class="filter-label">Rating</label>
              <select v-model="selectedRating" class="filter-select" @change="handleFilterChange">
                <option value="all">All Ratings</option>
                <option value="5">5 Stars</option>
                <option value="4">4 Stars</option>
                <option value="3">3 Stars</option>
                <option value="2">2 Stars</option>
                <option value="1">1 Star</option>
              </select>
            </div>

            <!-- Status Dropdown -->
            <div class="filter-field">
              <label class="filter-label">Status</label>
              <select v-model="selectedStatus" class="filter-select" @change="handleFilterChange">
                <option value="all">All Statuses</option>
                <option value="approved">Approved</option>
                <option value="pending">Pending</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>

            <!-- Date Range Dropdown -->
            <div class="filter-field">
              <label class="filter-label">Date Range</label>
              <div class="date-select-wrap">
                <Calendar class="w-3.5 h-3.5 text-taupe mr-1" />
                <select v-model="selectedDateRange" class="filter-select date-select" @change="handleFilterChange">
                  <option value="all">All Time</option>
                  <option value="30d">Last 30 Days</option>
                  <option value="90d">Last 90 Days</option>
                  <option value="year">This Year</option>
                </select>
              </div>
            </div>
          </div>

          <!-- REVIEWS TABLE -->
          <div class="table-card">
            <table class="reviews-table">
              <thead>
                <tr>
                  <th class="th-check">
                    <input type="checkbox" :checked="allSelected" @change="toggleSelectAll" class="custom-checkbox" />
                  </th>
                  <th class="th-num">#</th>
                  <th class="th-review">Review</th>
                  <th class="th-product">Product</th>
                  <th class="th-customer">Customer</th>
                  <th class="th-rating">Rating</th>
                  <th class="th-status">Status</th>
                  <th class="th-date">Date</th>
                  <th class="th-actions">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="adminStore.reviewsLoading">
                  <td colspan="9" class="td-loading">
                    <div class="spinner"></div>
                    <span>Loading reviews atelier data...</span>
                  </td>
                </tr>

                <tr v-else-if="adminStore.reviews.length === 0">
                  <td colspan="9" class="td-empty">
                    <MessageSquare class="w-10 h-10 text-taupe mx-auto mb-2 opacity-50" />
                    <p class="font-serif text-lg text-charcoal">No customer reviews found</p>
                    <p class="text-xs text-taupe">Try adjusting search parameters or filter criteria.</p>
                  </td>
                </tr>

                <tr
                  v-for="(review, index) in adminStore.reviews"
                  :key="review.id"
                  :class="{ 'row-selected': selectedReviews.includes(review.id) }"
                >
                  <!-- Checkbox -->
                  <td class="td-check">
                    <input
                      type="checkbox"
                      :checked="selectedReviews.includes(review.id)"
                      @change="toggleSelectReview(review.id)"
                      class="custom-checkbox"
                    />
                  </td>

                  <!-- Number -->
                  <td class="td-num">{{ index + 1 }}</td>

                  <!-- Review Title & Excerpt -->
                  <td class="td-review">
                    <div class="review-flex">
                      <img :src="review.product_image || '/images/prod-sk2.jpg'" :alt="review.product_name" class="rev-prod-thumb" />
                      <div class="rev-text-block">
                        <span class="rev-title">{{ review.title }}</span>
                        <p class="rev-comment">{{ review.comment }}</p>
                        <div v-if="review.admin_reply" class="rev-atelier-reply-tag">
                          <CornerDownRight class="w-3 h-3 text-crimson inline mr-1" />
                          <span>Atelier Responded</span>
                        </div>
                      </div>
                    </div>
                  </td>

                  <!-- Product Name -->
                  <td class="td-product">
                    <span class="prod-name-text">{{ review.product_name }}</span>
                  </td>

                  <!-- Customer Info -->
                  <td class="td-customer">
                    <div class="customer-info-block">
                      <div class="avatar-row">
                        <img :src="review.customer_avatar || '/images/customer-1.jpg'" :alt="review.customer_name" class="cust-avatar" />
                        <span class="cust-name">{{ review.customer_name }}</span>
                      </div>
                      <span v-if="review.verified_purchase" class="badge-verified">Verified Purchase</span>
                    </div>
                  </td>

                  <!-- Star Rating -->
                  <td class="td-rating">
                    <div class="stars-row">
                      <Star
                        v-for="s in 5"
                        :key="s"
                        class="w-3.5 h-3.5"
                        :class="s <= review.rating ? 'star-filled' : 'star-empty'"
                      />
                    </div>
                  </td>

                  <!-- Status Badge -->
                  <td class="td-status">
                    <span class="badge-status" :class="`status-${review.status}`">
                      {{ review.status === 'approved' ? 'Approved' : review.status === 'pending' ? 'Pending' : 'Rejected' }}
                    </span>
                  </td>

                  <!-- Date -->
                  <td class="td-date">
                    <span class="date-text">{{ review.created_at }}</span>
                  </td>

                  <!-- Action Buttons -->
                  <td class="td-actions">
                    <div class="actions-group">
                      <button class="action-btn" title="Inspect Review" @click="inspectingReview = review">
                        <Eye class="w-4 h-4" />
                      </button>
                      <button class="action-btn" title="Reply to Review" @click="openReplyModal(review)">
                        <Edit2 class="w-4 h-4" />
                      </button>

                      <div class="dropdown-wrap">
                        <button class="action-btn" title="More options" @click="activeDropdown = activeDropdown === review.id ? null : review.id">
                          <MoreHorizontal class="w-4 h-4" />
                        </button>

                        <div v-if="activeDropdown === review.id" class="dropdown-menu">
                          <button
                            v-if="review.status !== 'approved'"
                            class="dropdown-item text-green"
                            @click="updateStatus(review, 'approved')"
                          >
                            <CheckCircle2 class="w-4 h-4 mr-2" />
                            <span>Approve Review</span>
                          </button>
                          <button
                            v-if="review.status !== 'rejected'"
                            class="dropdown-item text-red"
                            @click="updateStatus(review, 'rejected')"
                          >
                            <XCircle class="w-4 h-4 mr-2" />
                            <span>Reject / Hide</span>
                          </button>
                          <button
                            v-if="review.status !== 'pending'"
                            class="dropdown-item text-amber"
                            @click="updateStatus(review, 'pending')"
                          >
                            <Clock class="w-4 h-4 mr-2" />
                            <span>Set Pending</span>
                          </button>
                          <div class="dropdown-divider"></div>
                          <button class="dropdown-item text-danger" @click="deleteReview(review)">
                            <Trash2 class="w-4 h-4 mr-2" />
                            <span>Delete Permanently</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- TABLE FOOTER / PAGINATION -->
            <div class="table-footer">
              <div class="footer-info">
                Showing 1 to {{ adminStore.reviews.length }} of {{ adminStore.reviewsKpis.total_reviews?.toLocaleString() || '1,248' }} reviews
              </div>

              <div class="pagination-controls">
                <button class="page-nav-btn" :disabled="currentPage <= 1" @click="currentPage--; loadReviews()">
                  <ChevronLeft class="w-4 h-4" />
                </button>
                <button
                  v-for="p in [1, 2, 3, 4, 5]"
                  :key="p"
                  class="page-num-btn"
                  :class="{ active: currentPage === p }"
                  @click="currentPage = p; loadReviews()"
                >
                  {{ p }}
                </button>
                <span class="page-ellipsis">...</span>
                <button class="page-num-btn" @click="currentPage = 156; loadReviews()">156</button>
                <button class="page-nav-btn" @click="currentPage++; loadReviews()">
                  <ChevronRight class="w-4 h-4" />
                </button>

                <div class="page-size-select">
                  <select v-model="pageSize" @change="currentPage = 1; loadReviews()">
                    <option :value="10">10 / page</option>
                    <option :value="20">20 / page</option>
                    <option :value="50">50 / page</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT: SIDEBAR WIDGETS -->
        <div class="reviews-sidebar">
          <!-- 1. RATING BREAKDOWN CARD -->
          <div class="widget-card">
            <h3 class="widget-title">Rating Breakdown</h3>

            <div class="rating-header-row">
              <span class="rating-big-num">4.6</span>
              <div class="rating-stars-col">
                <div class="stars-row">
                  <Star v-for="s in 5" :key="s" class="w-4 h-4 star-filled" />
                </div>
                <span class="rating-count-label">Based on 1,248 reviews</span>
              </div>
            </div>

            <!-- Distribution Bars -->
            <div class="breakdown-list">
              <div class="breakdown-row">
                <span class="star-label">5 stars</span>
                <div class="bar-track">
                  <div class="bar-fill" style="width: 68%;"></div>
                </div>
                <span class="star-pct">68%</span>
              </div>

              <div class="breakdown-row">
                <span class="star-label">4 stars</span>
                <div class="bar-track">
                  <div class="bar-fill" style="width: 20%;"></div>
                </div>
                <span class="star-pct">20%</span>
              </div>

              <div class="breakdown-row">
                <span class="star-label">3 stars</span>
                <div class="bar-track">
                  <div class="bar-fill" style="width: 8%;"></div>
                </div>
                <span class="star-pct">8%</span>
              </div>

              <div class="breakdown-row">
                <span class="star-label">2 stars</span>
                <div class="bar-track">
                  <div class="bar-fill" style="width: 3%;"></div>
                </div>
                <span class="star-pct">3%</span>
              </div>

              <div class="breakdown-row">
                <span class="star-label">1 star</span>
                <div class="bar-track">
                  <div class="bar-fill" style="width: 1%;"></div>
                </div>
                <span class="star-pct">1%</span>
              </div>
            </div>
          </div>

          <!-- 2. RECENT REVIEWS CARD -->
          <div class="widget-card">
            <h3 class="widget-title">Recent Reviews</h3>

            <div class="recent-list">
              <div class="recent-item">
                <img src="/images/prod-sk2.jpg" alt="Serum" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Amazing results!</span>
                  <span class="recent-sub">Brightening Face Serum</span>
                  <div class="recent-meta">
                    <span class="recent-star-tag">5 <Star :size="10" class="star-fill" /></span>
                    <span class="recent-date">Aug 28, 2025</span>
                  </div>
                </div>
              </div>

              <div class="recent-item">
                <img src="/images/prod-laneige.jpg" alt="Moisturizer" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Good product</span>
                  <span class="recent-sub">Hydrating Moisturizer</span>
                  <div class="recent-meta">
                    <span class="recent-star-tag">4 <Star :size="10" class="star-fill" /></span>
                    <span class="recent-date">Aug 27, 2025</span>
                  </div>
                </div>
              </div>

              <div class="recent-item">
                <img src="/images/prod-anua-cleanser.jpg" alt="Cleanser" class="recent-thumb" />
                <div class="recent-body">
                  <span class="recent-title">Not for me</span>
                  <span class="recent-sub">Gentle Cleanser</span>
                  <div class="recent-meta">
                    <span class="recent-star-tag">2 <Star :size="10" class="star-fill" /></span>
                    <span class="recent-date">Aug 26, 2025</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="widget-footer-action">
              <button class="link-action" @click="selectedStatus = 'all'; handleFilterChange()">
                <span>View All Reviews</span>
                <ArrowRight class="w-3.5 h-3.5 ml-1" />
              </button>
            </div>
          </div>

          <!-- 3. MODERATION TIP CARD -->
          <div class="widget-card tip-card">
            <div class="tip-header">
              <Lightbulb class="w-5 h-5 text-crimson mr-2" />
              <h4 class="tip-title">Moderation Tip</h4>
            </div>
            <p class="tip-body">
              Responding to reviews shows you care about your customers and helps build trust in your brand.
            </p>
            <a href="javascript:void(0)" class="tip-link">
              <span>View Review Guidelines</span>
              <ArrowRight class="w-3.5 h-3.5 ml-1" />
            </a>
          </div>
        </div>
      </div>

      <!-- INSPECT REVIEW MODAL -->
      <div v-if="inspectingReview" class="modal-backdrop" @click.self="inspectingReview = null">
        <div class="modal-card">
          <div class="modal-header">
            <div>
              <span class="modal-label">Customer Review</span>
              <h2 class="modal-title">{{ inspectingReview.title }}</h2>
            </div>
            <button class="modal-close" @click="inspectingReview = null">×</button>
          </div>

          <div class="modal-body">
            <!-- Product & Customer row -->
            <div class="inspect-grid">
              <div class="inspect-item">
                <label class="inspect-lbl">Product</label>
                <div class="flex items-center gap-2 mt-1">
                  <img :src="inspectingReview.product_image" class="w-9 h-9 rounded object-cover" />
                  <span class="font-medium text-sm">{{ inspectingReview.product_name }}</span>
                </div>
              </div>

              <div class="inspect-item">
                <label class="inspect-lbl">Customer</label>
                <div class="flex items-center gap-2 mt-1">
                  <img :src="inspectingReview.customer_avatar" class="w-9 h-9 rounded-full object-cover" />
                  <div>
                    <span class="font-medium text-sm block">{{ inspectingReview.customer_name }}</span>
                    <span class="text-xs text-taupe">{{ inspectingReview.customer_email || 'Verified Patron' }}</span>
                  </div>
                </div>
              </div>

              <div class="inspect-item">
                <label class="inspect-lbl">Rating</label>
                <div class="stars-row mt-1">
                  <Star v-for="s in 5" :key="s" class="w-4 h-4" :class="s <= inspectingReview.rating ? 'star-filled' : 'star-empty'" />
                </div>
              </div>

              <div class="inspect-item">
                <label class="inspect-lbl">Status</label>
                <span class="badge-status mt-1 inline-block" :class="`status-${inspectingReview.status}`">
                  {{ inspectingReview.status }}
                </span>
              </div>
            </div>

            <!-- Full comment text -->
            <div class="comment-box">
              <label class="inspect-lbl">Full Review Feedback</label>
              <p class="comment-full-text">{{ inspectingReview.comment }}</p>
            </div>

            <!-- Atelier response if present -->
            <div v-if="inspectingReview.admin_reply" class="reply-box">
              <label class="inspect-lbl text-crimson">Atelier Official Response</label>
              <p class="reply-text">{{ inspectingReview.admin_reply }}</p>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="inspectingReview = null">Close</button>
            <button v-if="inspectingReview.status !== 'approved'" class="btn-approve" @click="updateStatus(inspectingReview, 'approved')">
              Approve
            </button>
            <button v-if="inspectingReview.status !== 'rejected'" class="btn-reject" @click="updateStatus(inspectingReview, 'rejected')">
              Reject
            </button>
            <button class="btn-primary" @click="openReplyModal(inspectingReview)">
              Write Reply
            </button>
          </div>
        </div>
      </div>

      <!-- REPLY MODAL -->
      <div v-if="replyingReview" class="modal-backdrop" @click.self="replyingReview = null">
        <div class="modal-card">
          <div class="modal-header">
            <div>
              <span class="modal-label">Atelier Response</span>
              <h2 class="modal-title">Reply to {{ replyingReview.customer_name }}</h2>
            </div>
            <button class="modal-close" @click="replyingReview = null">×</button>
          </div>

          <div class="modal-body">
            <div class="customer-preview-box">
              <p class="font-medium text-sm text-charcoal">"{{ replyingReview.title }}"</p>
              <p class="text-xs text-taupe mt-1">{{ replyingReview.comment }}</p>
            </div>

            <div class="form-group mt-4">
              <label class="form-label">Your Atelier Reply</label>
              <textarea
                v-model="replyText"
                rows="4"
                placeholder="Thank you for sharing your experience with Luméa Atelier! We are delighted to hear..."
                class="reply-textarea"
              ></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="replyingReview = null">Cancel</button>
            <button class="btn-primary" @click="submitReply">
              <Send class="w-3.5 h-3.5 mr-1" />
              <span>Save & Publish Reply</span>
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.reviews-page {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Breadcrumb */
.breadcrumb-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #8C827A;
}

.crumb-parent {
  color: #8C827A;
}

.crumb-sep {
  color: #B5ABA4;
}

.crumb-current {
  color: #2D2422;
  font-weight: 500;
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
  position: relative;
  overflow: hidden;
  min-height: 120px;
}

.hero-content {
  max-width: 550px;
  z-index: 2;
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
  gap: 1.75rem;
  z-index: 2;
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

.quote-line-1 {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.125rem;
  font-weight: 600;
  color: #84261B;
  font-style: italic;
}

.quote-line-2 {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.125rem;
  font-weight: 600;
  color: #84261B;
}

.btn-export-top {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(132, 38, 27, 0.2);
  transition: all 0.2s ease;
}

.btn-export-top:hover {
  background: #6E1F16;
  transform: translateY(-1px);
}

/* 5 KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}

.kpi-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.125rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.kpi-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-icon-wrap.rose-soft {
  background: #FCECE9;
}

.text-crimson {
  color: #84261B;
}

.kpi-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.kpi-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.kpi-num {
  font-size: 1.35rem;
  font-weight: 700;
  color: #2D2422;
  font-family: var(--font-sans, -apple-system, sans-serif);
}

.kpi-badge {
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.15rem 0.4rem;
  border-radius: 12px;
}

.kpi-badge.positive {
  background: #EAF5EE;
  color: #2D8A4E;
}

.kpi-sub {
  display: flex;
  flex-direction: column;
  margin-top: 0.15rem;
}

.kpi-label {
  font-size: 0.75rem;
  color: #8C827A;
  font-weight: 500;
}

.kpi-compare {
  font-size: 0.6875rem;
  color: #B5ABA4;
}

/* Split Layout */
.reviews-split-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 1.25rem;
  align-items: flex-start;
}

/* Main Pane */
.reviews-main-pane {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Filter Toolbar */
.filter-toolbar {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 0.875rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex-wrap: wrap;
}

.search-input-wrap {
  position: relative;
  flex: 1;
  min-width: 180px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #8C827A;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem 0.5rem 2.25rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.8125rem;
  background: #FAF6F2;
  color: #2D2422;
  outline: none;
}

.search-input:focus {
  border-color: #84261B;
  background: #FFFFFF;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.filter-label {
  font-size: 0.6875rem;
  color: #8C827A;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  font-weight: 600;
}

.filter-select {
  padding: 0.45rem 0.75rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.8125rem;
  background: #FFFFFF;
  color: #2D2422;
  outline: none;
  cursor: pointer;
}

.filter-select:focus {
  border-color: #84261B;
}

.date-select-wrap {
  display: flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0 0.5rem;
  background: #FFFFFF;
}

.date-select {
  border: none;
  padding: 0.45rem 0.25rem;
}

/* Table Card */
.table-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  overflow: hidden;
}

.reviews-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
}

.reviews-table th {
  background: #FAF6F2;
  padding: 0.75rem 0.875rem;
  font-weight: 600;
  color: #6E635E;
  text-align: left;
  border-bottom: 1px solid #EBE1D7;
  font-size: 0.75rem;
  letter-spacing: 0.02em;
}

.reviews-table td {
  padding: 0.875rem;
  border-bottom: 1px solid #F5ECE6;
  color: #2D2422;
  vertical-align: middle;
}

.reviews-table tr:hover {
  background: #FAF6F2;
}

.row-selected {
  background: #FDF7F5 !important;
}

.custom-checkbox {
  accent-color: #84261B;
  cursor: pointer;
  width: 15px;
  height: 15px;
}

.th-num, .td-num {
  width: 32px;
  color: #8C827A;
  font-size: 0.75rem;
}

.review-flex {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  max-width: 280px;
}

.rev-prod-thumb {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EBE1D7;
  flex-shrink: 0;
}

.rev-text-block {
  display: flex;
  flex-direction: column;
}

.rev-title {
  font-weight: 600;
  color: #2D2422;
  font-size: 0.8125rem;
}

.rev-comment {
  font-size: 0.75rem;
  color: #6E635E;
  margin: 0.15rem 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.35;
}

.rev-atelier-reply-tag {
  font-size: 0.6875rem;
  color: #84261B;
  margin-top: 0.25rem;
  font-weight: 500;
}

.prod-name-text {
  font-weight: 500;
  color: #2D2422;
  max-width: 130px;
  display: block;
}

.customer-info-block {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cust-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EBE1D7;
}

.cust-name {
  font-weight: 500;
  color: #2D2422;
  font-size: 0.8125rem;
}

.badge-verified {
  font-size: 0.625rem;
  background: #FCECE9;
  color: #84261B;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
  font-weight: 500;
  align-self: flex-start;
}

.stars-row {
  display: flex;
  align-items: center;
  gap: 0.15rem;
}

.star-filled {
  color: #E58A2B;
  fill: #E58A2B;
}

.star-empty {
  color: #D6CBC2;
}

/* Status Badges */
.badge-status {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
}

.status-approved {
  background: #EAF5EE;
  color: #2D8A4E;
}

.status-pending {
  background: #FEF6E7;
  color: #B57914;
}

.status-rejected {
  background: #FDECEB;
  color: #C0392B;
}

.date-text {
  font-size: 0.75rem;
  color: #6E635E;
}

/* Actions */
.actions-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  position: relative;
}

.action-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #EBE1D7;
  background: #FFFFFF;
  border-radius: 6px;
  color: #6E635E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.action-btn:hover {
  background: #FAF6F2;
  color: #84261B;
  border-color: #84261B;
}

/* Dropdown */
.dropdown-wrap {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(45, 36, 34, 0.12);
  z-index: 50;
  min-width: 170px;
  padding: 0.35rem 0;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.85rem;
  background: none;
  border: none;
  font-size: 0.75rem;
  cursor: pointer;
  text-align: left;
}

.dropdown-item:hover {
  background: #FAF6F2;
}

.text-green { color: #2D8A4E; }
.text-red { color: #C0392B; }
.text-amber { color: #B57914; }
.text-danger { color: #C0392B; }

.dropdown-divider {
  height: 1px;
  background: #F5ECE6;
  margin: 0.25rem 0;
}

/* Table Footer */
.table-footer {
  padding: 0.875rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #EBE1D7;
  background: #FAF6F2;
}

.footer-info {
  font-size: 0.75rem;
  color: #6E635E;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.page-nav-btn, .page-num-btn {
  min-width: 28px;
  height: 28px;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #6E635E;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.page-num-btn.active {
  background: #84261B;
  color: #FFFFFF;
  border-color: #84261B;
}

.page-ellipsis {
  color: #8C827A;
  font-size: 0.75rem;
  padding: 0 0.25rem;
}

.page-size-select select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.75rem;
  background: #FFFFFF;
  color: #6E635E;
}

/* SIDEBAR WIDGETS */
.reviews-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.widget-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.25rem;
}

.widget-title {
  font-family: var(--font-sans, sans-serif);
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0 0 1rem 0;
}

/* Rating Breakdown */
.rating-header-row {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1.125rem;
}

.rating-big-num {
  font-size: 2.25rem;
  font-weight: 700;
  color: #2D2422;
  line-height: 1;
}

.rating-stars-col {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.rating-count-label {
  font-size: 0.75rem;
  color: #8C827A;
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.breakdown-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.star-label {
  width: 48px;
  color: #6E635E;
}

.bar-track {
  flex: 1;
  height: 6px;
  background: #F0E8E1;
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #84261B;
  border-radius: 3px;
}

.star-pct {
  width: 32px;
  text-align: right;
  color: #8C827A;
  font-size: 0.6875rem;
}

/* Recent Reviews */
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.recent-item {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #FAF6F2;
}

.recent-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.recent-thumb {
  width: 38px;
  height: 38px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EBE1D7;
}

.recent-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.recent-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

.recent-sub {
  font-size: 0.6875rem;
  color: #8C827A;
}

.recent-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.25rem;
}

.recent-star-tag {
  font-size: 0.6875rem;
  color: #E58A2B;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.recent-star-tag .star-fill {
  fill: #E58A2B;
  color: #E58A2B;
}

.recent-date {
  font-size: 0.6875rem;
  color: #B5ABA4;
}

.widget-footer-action {
  margin-top: 1rem;
  border-top: 1px solid #F5ECE6;
  padding-top: 0.75rem;
  text-align: center;
}

.link-action {
  background: none;
  border: none;
  color: #84261B;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

/* Moderation Tip */
.tip-card {
  background: #FAF6F2;
  border-color: #EBE1D7;
}

.tip-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tip-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.tip-body {
  font-size: 0.75rem;
  color: #6E635E;
  line-height: 1.45;
  margin: 0 0 0.75rem 0;
}

.tip-link {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  color: #84261B;
  font-weight: 600;
  text-decoration: none;
}

/* Modals */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(30, 24, 22, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1.5rem;
}

.modal-card {
  background: #FFFFFF;
  border-radius: 12px;
  width: 100%;
  max-width: 540px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid #EBE1D7;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #F5ECE6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF6F2;
}

.modal-label {
  font-size: 0.6875rem;
  color: #84261B;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: 600;
}

.modal-title {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.25rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0.15rem 0 0 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #8C827A;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.inspect-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.inspect-lbl {
  font-size: 0.6875rem;
  color: #8C827A;
  text-transform: uppercase;
  font-weight: 600;
  display: block;
}

.comment-box, .reply-box {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
}

.comment-full-text {
  font-size: 0.8125rem;
  color: #2D2422;
  line-height: 1.5;
  margin-top: 0.35rem;
}

.reply-text {
  font-size: 0.8125rem;
  color: #84261B;
  line-height: 1.5;
  margin-top: 0.35rem;
}

.customer-preview-box {
  background: #FAF6F2;
  border-left: 3px solid #84261B;
  padding: 0.75rem 1rem;
  border-radius: 4px;
}

.reply-textarea {
  width: 100%;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0.75rem;
  font-size: 0.8125rem;
  font-family: inherit;
  color: #2D2422;
  resize: vertical;
  outline: none;
  margin-top: 0.35rem;
}

.reply-textarea:focus {
  border-color: #84261B;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #F5ECE6;
  background: #FAF6F2;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-secondary {
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  color: #6E635E;
  cursor: pointer;
}

.btn-primary {
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.btn-approve {
  background: #2D8A4E;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

.btn-reject {
  background: #C0392B;
  color: #FFFFFF;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #EBE1D7;
  border-top-color: #84261B;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 1200px) {
  .reviews-split-layout {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
