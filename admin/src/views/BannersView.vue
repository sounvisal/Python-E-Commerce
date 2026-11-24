<script setup>
import { computed, ref, onMounted, reactive } from 'vue'
import apiClient from '@/api/client'
import { useAdminStore } from '@/stores/admin'
import { getStorefrontUrl } from '@/utils/storefront'
import {
  ExternalLink,
  Edit2,
  Plus,
  GripVertical,
  CheckCircle2,
  AlertCircle,
  Upload,
  Trash2,
  Eye,
  RefreshCw,
  Sparkles,
  Save,
  Layers,
  ShoppingBag,
  BookOpen,
  Image as ImageIcon,
  X
} from 'lucide-vue-next'

const adminStore = useAdminStore()
const hostedDeployment = import.meta.env.VITE_HOSTED_DEPLOYMENT === 'true'
const canUploadMedia = computed(() => !hostedDeployment && adminStore.uploadStatus?.enabled === true)

// State
const banners = ref([])
const loading = ref(false)
const loadError = ref('')
const showEditModal = ref(false)
const isSubmitting = ref(false)

// Homepage Settings State
const pageTitle = ref('Luméa - Beauty Lives Here')
const metaDescription = ref('Discover authentic beauty products, expert advice, and personalized skincare solutions at Luméa.')
const metaImage = ref('/images/admin-hero-bottles.jpg')
const lastPublished = ref('')

// Homepage Sections matching Luméa Homepage Management Dashboard.png
const sections = ref([])

// Banner Edit Form
const bannerForm = reactive({
  id: null,
  title: '',
  subtitle: '',
  badge: '',
  image_url: '',
  cta_text: '',
  link: '',
  is_active: true
})

onMounted(async () => {
  await fetchBanners()
})

async function fetchBanners() {
  loading.value = true
  loadError.value = ''
  try {
    const res = await apiClient.get('/banners?active_only=false')
    if (res.data?.status === 'success' && Array.isArray(res.data.data)) {
      banners.value = res.data.data
      sections.value = banners.value.map(b => ({ id: b.id, order: b.display_order, title: b.title, type: b.page,
        type_badge: 'badge-banner', description: b.subtitle, is_active: b.is_active, thumb: b.image_url, banner: b }))
      lastPublished.value = banners.value.map(b => b.updated_at || b.created_at || '').sort().at(-1) || ''
    } else {
      throw new Error('Unexpected banner response')
    }
  } catch (err) {
    loadError.value = 'Could not load banners. Try refreshing the list.'
  } finally {
    loading.value = false
  }
}

const bannerFileInput = ref(null)
const isUploadingBanner = ref(false)

function triggerBannerUpload() {
  if (!canUploadMedia.value) {
    adminStore.addToast('Hosted media upload is disabled on this server. Provide an image URL directly.', 'warning')
    return
  }
  if (bannerFileInput.value) {
    bannerFileInput.value.click()
  }
}

async function handleBannerUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  isUploadingBanner.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.data?.status === 'success' && res.data.data?.url) {
      bannerForm.image_url = res.data.data.url
      adminStore.addToast('Section banner image uploaded successfully!', 'success')
    }
  } catch (err) {
    adminStore.addToast('Failed to upload banner image.', 'error')
  } finally {
    isUploadingBanner.value = false
    if (e.target) e.target.value = ''
  }
}

function openEditSection(sec) {
  bannerForm.id = sec.id
  bannerForm.title = sec.banner.title
  bannerForm.subtitle = sec.description
  bannerForm.badge = sec.banner.badge_text || ''
  bannerForm.image_url = sec.thumb
  bannerForm.cta_text = sec.banner.cta_text || ''
  bannerForm.link = sec.banner.cta_link || ''
  bannerForm.is_active = sec.is_active
  showEditModal.value = true
}

async function saveSection() {
  if (isSubmitting.value) return
  const title = bannerForm.title.trim()
  const link = bannerForm.link.trim()
  if (!title || (link && !/^\/(?![\/\\])[^\\\s]*$/.test(link))) {
    adminStore.addToast('Enter a title and a storefront path such as /shop.', 'warning')
    return
  }
  isSubmitting.value = true
  try {
    await apiClient.put(`/banners/${bannerForm.id}`, { title, subtitle: bannerForm.subtitle,
      badge_text: bannerForm.badge, image_url: bannerForm.image_url, cta_text: bannerForm.cta_text.trim(),
      cta_link: link, is_active: bannerForm.is_active })
    await fetchBanners()
    showEditModal.value = false
    adminStore.addToast('Banner saved to the storefront.', 'success')
  } catch (error) { adminStore.addToast(error.response?.data?.detail || 'Banner was not saved. Please retry.', 'error') }
  finally { isSubmitting.value = false }
}
async function toggleSection(sec) {
  try {
    await apiClient.put(`/banners/${sec.id}`, { is_active: !sec.is_active })
    await fetchBanners()
    adminStore.addToast('Banner visibility saved.', 'success')
  } catch { adminStore.addToast('Could not save visibility.', 'error') }
}
async function updateHomepage() { await fetchBanners() }

function openLiveSite() {
  window.open(getStorefrontUrl(), '_blank')
}

const metaImageFileInput = ref(null)
function triggerMetaImageUpload() {
  if (metaImageFileInput.value) metaImageFileInput.value.click()
}
async function handleMetaImageUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    const url = res.data?.data?.url || res.data?.url
    if (url) {
      metaImage.value = url
      adminStore.addToast('Social share meta image updated!', 'success')
    }
  } catch (err) {
    adminStore.addToast('Failed to upload social image.', 'error')
  } finally {
    if (e.target) e.target.value = ''
  }
}

function applyTemplate(name) {
  adminStore.addToast(`Applied ${name} template layout presets.`, 'success')
}
</script>

<template>
  <div class="homepage-management-page">
    <!-- Hero Banner matching Luméa Homepage Management Dashboard.png -->
    <div class="homepage-hero-card">
      <div class="hero-left">
        <div class="editor-breadcrumb">
          <span>CONTENT</span>
          <span class="crumb-sep">></span>
          <span class="crumb-current">HOMEPAGE</span>
        </div>
        <h1 class="hero-heading">Homepage Management</h1>
        <p class="hero-subtext">Customize your homepage content, banners, and sections to create the best shopping experience.</p>
      </div>

      <div class="hero-right">
        <div class="hero-visual-callout">
          <img
            src="/images/admin-hero-bottles.jpg"
            alt="Luméa Homepage Preview"
            class="hero-bottles"
            @error="$event.target.src = '/images/ai-banner-atelier.jpg'"
          />
          <div class="hero-motto">
            <span class="motto-line">Beautiful</span>
            <span class="motto-line highlight">skin. Brighter</span>
            <span class="motto-line highlight">tomorrows.</span>
          </div>
        </div>

        <button class="btn-view-live" @click="openLiveSite">
          <span>View Live Site</span>
          <ExternalLink :size="14" />
        </button>
      </div>
    </div>

    <!-- 2-Column Main Layout matching mockup -->
    <div class="homepage-grid-layout">
      <!-- Left Column: Homepage Sections -->
      <div class="sections-column">
        <div class="card sections-panel-card">
          <div class="card-header-row">
            <div>
              <h3 class="panel-card-title">Homepage Sections</h3>
              <p class="panel-sub">Choose the Home banner to edit the first storefront slide.</p>
            </div>
            <button disabled title="Custom sections are not available yet" class="btn-add-section opacity-60 cursor-not-allowed">
              <Plus :size="14" />
              <span>Add Section</span>
            </button>
          </div>

          <!-- Section List Rows -->
          <div class="sections-list">
            <p v-if="loading" role="status">Loading banners…</p>
            <div v-else-if="loadError" role="alert">
              <p>{{ loadError }}</p>
              <button type="button" class="btn-sec-edit" @click="fetchBanners">Retry</button>
            </div>
            <p v-else-if="!sections.length">No saved banners.</p>
            <div
              v-for="sec in sections"
              :key="sec.id"
              class="section-item-row"
            >
              <div class="drag-handle-wrap">
                <GripVertical :size="16" class="drag-icon" />
                <span class="sec-order-badge">{{ sec.order }}</span>
              </div>

              <div class="sec-thumb-frame">
                <img
                  :src="sec.thumb"
                  :alt="sec.title"
                  class="sec-thumb-img"
                  @error="$event.target.src = '/images/admin-hero-bottles.jpg'"
                />
              </div>

              <div class="sec-meta-content">
                <div class="sec-title-badge-row">
                  <strong class="sec-title-txt">{{ sec.title }}</strong>
                  <span class="sec-type-pill" :class="sec.type_badge">{{ sec.type }}</span>
                </div>
                <p class="sec-desc-txt">{{ sec.description }}</p>
              </div>

              <div class="sec-actions-row">
                <span
                  class="status-pill"
                  :class="sec.is_active ? 'badge-active' : 'badge-inactive'"
                >
                  {{ sec.is_active ? 'Active' : 'Inactive' }}
                </span>

                <button
                  type="button"
                  class="atelier-toggle-switch"
                  :class="{ active: sec.is_active }"
                  @click="toggleSection(sec)"
                >
                  <span class="toggle-slider"></span>
                </button>

                <button class="btn-sec-edit" @click="openEditSection(sec)">
                  <Edit2 :size="13" />
                  <span>Edit</span>
                </button>

              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Settings, Publish, Templates -->
      <div class="sidebar-column">
        <!-- 1. Homepage Settings -->
        <div v-if="false" class="card panel-sidebar-card">
          <h3 class="panel-card-title">Page metadata (not available yet)</h3>

          <div class="form-group-clean">
            <label class="form-lbl">Page Title</label>
            <input
              v-model="pageTitle"
              type="text"
              class="atelier-input"
            />
          </div>

          <div class="form-group-clean">
            <label class="form-lbl">Meta Description</label>
            <textarea
              v-model="metaDescription"
              rows="3"
              class="atelier-textarea"
            ></textarea>
          </div>

          <div class="form-group-clean">
            <label class="form-lbl">Meta Image</label>
            <div class="meta-image-row">
              <div class="meta-img-box">
                <img :src="metaImage" class="meta-thumb" />
              </div>
              <div class="meta-btns">
                <input
                  ref="metaImageFileInput"
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="handleMetaImageUpload"
                />
                <button class="btn-meta-action" @click="triggerMetaImageUpload">
                  <Upload :size="13" />
                  <span>Change</span>
                </button>
                <button class="btn-meta-action text-danger" @click="metaImage = '/images/admin-hero-bottles.jpg'">
                  <Trash2 :size="13" />
                  <span>Remove</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Publish Section -->
        <div class="card panel-sidebar-card">
          <div class="card-header-row">
            <h3 class="panel-card-title">Storefront banners</h3>
          </div>

          <div class="publish-meta">
            <span class="pub-lbl">Last saved</span>
            <strong class="pub-time">{{ lastPublished ? new Date(lastPublished).toLocaleString() : '—' }}</strong>
          </div>

          <div class="publish-buttons-row">
            <button class="btn-preview-store" @click="openLiveSite">
              <Eye :size="14" />
              <span>Preview</span>
            </button>
            <button class="btn-update-homepage" @click="updateHomepage">
              <span>Refresh saved banners</span>
            </button>
          </div>
        </div>

        <!-- 3. Templates -->
        <div v-if="false" class="card panel-sidebar-card">
          <div class="card-header-row">
            <h3 class="panel-card-title">Templates</h3>
            <span class="view-all-link">View All</span>
          </div>
          <p class="panel-sub">Use a pre-designed template to quickly set up your homepage.</p>

          <div class="templates-grid">
            <div class="template-item active">
              <div class="tmpl-thumb-box">
                <img src="/images/admin-hero-bottles.jpg" class="tmpl-thumb" />
              </div>
              <span class="tmpl-name">Default (Current)</span>
            </div>
            <div class="template-item" @click="applyTemplate('Summer Sale')">
              <div class="tmpl-thumb-box">
                <img src="/images/ai-banner-atelier.jpg" class="tmpl-thumb" />
              </div>
              <span class="tmpl-name">Summer Sale</span>
            </div>
            <div class="template-item" @click="applyTemplate('New Arrivals')">
              <div class="tmpl-thumb-box">
                <img src="/images/banner-new-arrivals.jpg" class="tmpl-thumb" />
              </div>
              <span class="tmpl-name">New Arrivals</span>
            </div>
            <div class="template-item" @click="applyTemplate('Minimal')">
              <div class="tmpl-thumb-box">
                <img src="/images/prod-sk2.jpg" class="tmpl-thumb" />
              </div>
              <span class="tmpl-name">Minimal</span>
            </div>
          </div>
        </div>

        <!-- 4. Tip Card -->
        <div class="card tip-banner-card">
          <div class="tip-top">
            <Sparkles :size="16" class="tip-icon" />
            <strong>Tip</strong>
          </div>
          <p class="tip-text">
            Use high-quality images and clear messaging to create a compelling homepage experience for atelier clientele.
          </p>
        </div>
      </div>
    </div>

    <!-- Edit Section Modal -->
    <div v-if="showEditModal" class="modal-backdrop" @click="showEditModal = false">
      <div class="section-modal-dialog" @click.stop>
        <div class="modal-header-clean">
          <div>
            <h3 class="modal-title">Edit banner</h3>
            <p class="modal-sub">Update section headline, layout description, and visual asset.</p>
          </div>
          <button class="btn-close-modal" @click="showEditModal = false">
            <X :size="18" />
          </button>
        </div>

        <div class="modal-form-body">
          <div class="form-group-clean">
            <label class="form-lbl" for="banner-title">Section Title</label>
            <input id="banner-title" v-model="bannerForm.title" type="text" class="atelier-input" />
          </div>

          <div class="form-group-clean">
            <label class="form-lbl">Subtitle / Description</label>
            <textarea v-model="bannerForm.subtitle" rows="3" class="atelier-textarea"></textarea>
          </div>
          <div class="form-group-clean">
            <label class="form-lbl" for="banner-cta-text">Button label</label>
            <input id="banner-cta-text" v-model="bannerForm.cta_text" type="text" class="atelier-input" />
          </div>
          <div class="form-group-clean">
            <label class="form-lbl" for="banner-cta-link">Button destination</label>
            <input id="banner-cta-link" v-model="bannerForm.link" type="text" class="atelier-input" placeholder="/shop" />
          </div>

          <div class="form-group-clean">
            <label class="form-lbl">Image URL or Asset Path</label>
            <div v-if="!canUploadMedia" class="media-disabled-notice mb-2">
              <AlertCircle :size="13" class="text-taupe" />
              <span>Hosted media upload is disabled on this server. Provide an image URL directly.</span>
            </div>
            <div class="input-with-upload-action">
              <input v-model="bannerForm.image_url" type="text" class="atelier-input" placeholder="/images/... or https://..." />
              <input
                v-if="canUploadMedia"
                type="file"
                ref="bannerFileInput"
                @change="handleBannerUpload"
                accept="image/*"
                style="display: none"
              />
              <button
                v-if="canUploadMedia"
                type="button"
                class="btn-upload-trigger"
                @click="triggerBannerUpload"
                :disabled="isUploadingBanner"
              >
                <Upload :size="14" />
                <span>{{ isUploadingBanner ? '...' : 'Upload Image' }}</span>
              </button>
            </div>
          </div>

          <div class="featured-toggle-row">
            <button
              type="button"
              class="atelier-toggle-switch"
              :class="{ active: bannerForm.is_active }"
              @click="bannerForm.is_active = !bannerForm.is_active"
            >
              <span class="toggle-slider"></span>
            </button>
            <div class="toggle-texts">
              <strong>Section Visibility</strong>
              <span>Show this section on the storefront homepage.</span>
            </div>
          </div>
        </div>

        <div class="modal-footer-clean">
          <button class="btn-cancel" @click="showEditModal = false">Cancel</button>
          <button class="btn-save-modal" :disabled="isSubmitting || isUploadingBanner" @click="saveSection">
            <Save :size="15" />
            <span>Save Section</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.homepage-management-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Hero Banner */
.homepage-hero-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #FFFFFF 0%, #FAF5F2 100%);
  border: 1px solid #EFE7E0;
  border-radius: 16px;
  padding: 24px 32px;
  box-shadow: 0 4px 18px rgba(132, 38, 27, 0.04);
}

.hero-left {
  max-width: 480px;
}

.editor-breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #84261B;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
}

.crumb-sep { color: #8C847E; }
.crumb-current { color: #84261B; }

.hero-heading {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 32px;
  line-height: 1.15;
  color: #84261B;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.hero-subtext {
  font-size: 13.5px;
  color: #7A726C;
  line-height: 1.45;
}

.hero-right {
  display: flex;
  align-items: center;
  gap: 32px;
}

.hero-visual-callout {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-bottles {
  height: 90px;
  width: auto;
  object-fit: contain;
}

.hero-motto {
  display: flex;
  flex-direction: column;
}

.motto-line {
  font-family: var(--font-serif, "Playfair Display", Georgia, serif);
  font-size: 16px;
  line-height: 1.25;
  color: #84261B;
  font-style: italic;
  font-weight: 600;
}

.btn-view-live {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #84261B;
  color: #FFFFFF;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13.5px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(132, 38, 27, 0.2);
}

.btn-view-live:hover {
  background: #6D1E15;
}

/* Grid Layout */
.homepage-grid-layout {
  display: grid;
  grid-template-columns: 1.8fr 1.2fr;
  gap: 20px;
}

.sections-column,
.sidebar-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sections-panel-card,
.panel-sidebar-card {
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 14px;
  padding: 24px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.panel-card-title {
  font-size: 16px;
  font-weight: 700;
  color: #2D2621;
}

.panel-sub {
  font-size: 12px;
  color: #8C847E;
  margin-top: 2px;
}

.btn-add-section {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #84261B;
  color: #FFFFFF;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

/* Sections List */
.sections-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-item-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px;
  background: #FAF7F4;
  border: 1px solid #EFE7E0;
  border-radius: 10px;
  transition: all 0.2s;
}

.section-item-row:hover {
  background: #FFFFFF;
  border-color: #D4A373;
}

.drag-handle-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: grab;
}

.drag-icon {
  color: #8C847E;
}

.sec-order-badge {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #2D2621;
}

.sec-thumb-frame {
  width: 72px;
  height: 48px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #EFE7E0;
  background: #FFFFFF;
}

.sec-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sec-meta-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sec-title-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sec-title-txt {
  font-size: 13.5px;
  color: #2D2621;
}

.sec-type-pill {
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.badge-banner { background: #FDF0EE; color: #D97768; }
.badge-features { background: #FEF7ED; color: #B25E00; }
.badge-catlist { background: #FAF0E8; color: #C4623C; }
.badge-slider { background: #F8E9E4; color: #84261B; }
.badge-artlist { background: #E8F5E9; color: #2E7D32; }

.sec-desc-txt {
  font-size: 12px;
  color: #7A726C;
  line-height: 1.35;
}

.sec-actions-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-pill {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 600;
}

.badge-active { background: #E8F5E9; color: #2E7D32; }
.badge-inactive { background: #F5ECE6; color: #8C847E; }

.atelier-toggle-switch {
  width: 36px;
  height: 20px;
  background: #EFE7E0;
  border-radius: 99px;
  border: none;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s;
  padding: 2px;
}

.atelier-toggle-switch.active { background: #84261B; }
.toggle-slider {
  display: block;
  width: 16px;
  height: 16px;
  background: #FFFFFF;
  border-radius: 50%;
  transition: transform 0.2s;
}
.atelier-toggle-switch.active .toggle-slider { transform: translateX(16px); }

.btn-sec-edit {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  font-size: 12px;
  color: #5C544E;
  cursor: pointer;
}

.btn-sec-edit:hover {
  border-color: #84261B;
  color: #84261B;
}

.btn-more-dots {
  background: none;
  border: none;
  color: #8C847E;
  cursor: pointer;
}

/* Sidebar Forms */
.form-group-clean {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-lbl {
  font-size: 12px;
  font-weight: 600;
  color: #3C3530;
}

.atelier-input,
.atelier-textarea {
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 12.5px;
  color: #2D2621;
  outline: none;
}

.atelier-input:focus,
.atelier-textarea:focus { border-color: #84261B; }

.meta-image-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.meta-img-box {
  width: 90px;
  height: 50px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #EFE7E0;
}

.meta-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.meta-btns {
  display: flex;
  gap: 8px;
}

.btn-meta-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 6px;
  font-size: 11.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-meta-action.text-danger:hover {
  border-color: #D32F2F;
  color: #D32F2F;
}

/* Publish Box */
.publish-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 16px;
}

.pub-lbl { font-size: 11px; color: #8C847E; }
.pub-time { font-size: 13.5px; color: #2D2621; }
.pub-author { font-size: 11.5px; color: #7A726C; }

.publish-buttons-row {
  display: flex;
  gap: 10px;
}

.btn-preview-store {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 9px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #3C3530;
  cursor: pointer;
}

.btn-update-homepage {
  flex: 1.4;
  padding: 9px;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
}

/* Templates Grid */
.templates-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-top: 10px;
}

.template-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  cursor: pointer;
}

.tmpl-thumb-box {
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #EFE7E0;
}

.template-item.active .tmpl-thumb-box {
  border: 2px solid #84261B;
}

.tmpl-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tmpl-name {
  font-size: 11px;
  color: #5C544E;
  text-align: center;
}

/* Tip */
.tip-banner-card {
  background: #FAF5F2;
  border: 1px solid #EFE7E0;
  border-radius: 12px;
  padding: 16px;
}

.tip-top {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #84261B;
  font-size: 13px;
  margin-bottom: 6px;
}

.tip-text {
  font-size: 12px;
  color: #5C544E;
  line-height: 1.45;
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
  backdrop-filter: blur(2px);
}

.section-modal-dialog {
  background: #FFFFFF;
  border-radius: 16px;
  width: 90%;
  max-width: 540px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header-clean {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 24px;
  border-bottom: 1px solid #EFE7E0;
}

.modal-title { font-size: 17px; font-weight: 700; color: #2D2621; }
.modal-sub { font-size: 12px; color: #8C847E; margin-top: 2px; }
.btn-close-modal { background: none; border: none; color: #8C847E; cursor: pointer; }

.modal-form-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.modal-footer-clean {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  background: #FAF7F4;
  border-top: 1px solid #EFE7E0;
}

.btn-cancel {
  padding: 8px 16px;
  background: #FFFFFF;
  border: 1px solid #EFE7E0;
  border-radius: 8px;
  font-size: 12.5px;
  color: #5C544E;
  cursor: pointer;
}

.btn-save-modal {
  padding: 8px 18px;
  background: #84261B;
  border: none;
  border-radius: 8px;
  color: #FFFFFF;
  font-size: 12.5px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.input-with-upload-action {
  display: flex;
  gap: 8px;
  align-items: center;
}

.input-with-upload-action .atelier-input {
  flex: 1;
}

.btn-upload-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FAF5F2;
  border: 1px solid #84261B;
  color: #84261B;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.btn-upload-trigger:hover {
  background: #84261B;
  color: #FFFFFF;
}

@media (max-width: 1100px) {
  .homepage-grid-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .templates-grid {
    grid-template-columns: 1fr;
  }
  .actions-top-bar {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
}
</style>
