<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import {
  FileText,
  Users,
  BarChart2,
  Star,
  Search,
  RotateCcw,
  Download,
  Edit,
  Eye,
  MoreHorizontal,
  Plus,
  Save,
  Send,
  GripVertical,
  Trash2,
  Image as ImageIcon,
  Check,
  ChevronDown,
  ArrowRight,
  Lightbulb,
  ExternalLink,
  Shield,
  Tag,
  Grid,
  Award,
  ChevronRight,
  X,
  Sparkles
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// View toggle: 'list' | 'editor'
const currentView = ref('list')
const activeTab = ref('Builder') // Builder, Appearance, Results, Settings

// List Filters
const searchQuery = ref('')
const selectedStatus = ref('all')
const selectedAudience = ref('all')
const selectedDateRange = ref('all')
const activeDropdown = ref(null)

// Current editing quiz
const editingQuiz = ref(null)
const selectedQuestionIndex = ref(0)
const showPreviewModal = ref(false)
const previewCurrentStep = ref(0)
const previewAnswers = ref({})

onMounted(async () => {
  await adminStore.fetchQuizzes()
})

const filteredQuizzes = computed(() => {
  let list = adminStore.quizzes || []
  if (selectedStatus.value !== 'all') {
    list = list.filter(q => q.status === selectedStatus.value)
  }
  if (selectedAudience.value !== 'all') {
    list = list.filter(q => (q.target_audience || '').toLowerCase().includes(selectedAudience.value.toLowerCase()))
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(item =>
      item.title.toLowerCase().includes(q) ||
      (item.description || '').toLowerCase().includes(q)
    )
  }
  return list
})

// Current selected question in editor
const currentQuestion = computed(() => {
  if (!editingQuiz.value || !editingQuiz.value.questions_data) return null
  return editingQuiz.value.questions_data[selectedQuestionIndex.value] || null
})

// Navigation & Actions
function openCreateQuiz() {
  editingQuiz.value = {
    id: Date.now(),
    title: 'New Diagnostic Skin Quiz',
    slug: `quiz-${Date.now()}`,
    description: 'Diagnose skin characteristics and map to curated atelier formulations.',
    status: 'draft',
    target_audience: 'Beginners',
    badge: 'Skin Type',
    level: 'Beginner',
    cover_image: '/images/quiz-model.jpg',
    questions_count: 1,
    completions: 0,
    completion_rate: '0%',
    questions_data: [
      {
        id: 1,
        step: 1,
        question: 'What is your primary skincare concern?',
        description: 'Choose the concern you would like your regimen to focus on.',
        type: 'Single Choice',
        required: true,
        image: '/images/quiz-model.jpg',
        help_text: 'Helps curate effective botanical actives.',
        options: [
          { id: 'hydration', title: 'Dryness & Dehydration', desc: 'Tight, flaky skin', image: '/images/texture-dry.jpg', maps_to: 'Dry' },
          { id: 'blemishes', title: 'Excess Oil & Blemishes', desc: 'Shiny T-zone and breakouts', image: '/images/texture-oily.jpg', maps_to: 'Oily' },
          { id: 'sensitivity', title: 'Redness & Irritation', desc: 'Easily reactive skin barrier', image: '/images/texture-sensitive.jpg', maps_to: 'Sensitive' }
        ]
      }
    ]
  }
  selectedQuestionIndex.value = 0
  currentView.value = 'editor'
}

function openEditQuiz(quiz) {
  // Deep clone to allow editing
  editingQuiz.value = JSON.parse(JSON.stringify(quiz))
  selectedQuestionIndex.value = 0
  currentView.value = 'editor'
  activeDropdown.value = null
}

function returnToList() {
  currentView.value = 'list'
}

async function handleToggleStatus(quiz) {
  activeDropdown.value = null
  await adminStore.toggleQuizStatus(quiz.id)
}

// Question Editor Methods
function addQuestion() {
  if (!editingQuiz.value) return
  const newStep = editingQuiz.value.questions_data.length + 1
  const newQ = {
    id: Date.now(),
    step: newStep,
    question: 'New Question Title',
    description: 'Provide helpful context or instructions.',
    type: 'Single Choice',
    required: true,
    image: '/images/quiz-model.jpg',
    help_text: 'This helps personalize your routine.',
    options: [
      { id: 'opt_1', title: 'Option 1', desc: 'Description of option 1', image: '/images/texture-normal.jpg', maps_to: 'Normal' },
      { id: 'opt_2', title: 'Option 2', desc: 'Description of option 2', image: '/images/texture-dry.jpg', maps_to: 'Dry' }
    ]
  }
  editingQuiz.value.questions_data.push(newQ)
  selectedQuestionIndex.value = editingQuiz.value.questions_data.length - 1
}

function removeQuestion(index) {
  if (!editingQuiz.value || editingQuiz.value.questions_data.length <= 1) {
    adminStore.addToast('Quiz must have at least one question', 'error')
    return
  }
  editingQuiz.value.questions_data.splice(index, 1)
  if (selectedQuestionIndex.value >= editingQuiz.value.questions_data.length) {
    selectedQuestionIndex.value = editingQuiz.value.questions_data.length - 1
  }
}

function addOption() {
  if (!currentQuestion.value) return
  const count = (currentQuestion.value.options || []).length + 1
  if (!currentQuestion.value.options) currentQuestion.value.options = []
  currentQuestion.value.options.push({
    id: `opt_${Date.now()}`,
    title: `Option ${count}`,
    desc: 'Describe characteristics',
    image: '/images/texture-normal.jpg',
    maps_to: 'Normal'
  })
}

function removeOption(optIndex) {
  if (!currentQuestion.value || currentQuestion.value.options.length <= 2) {
    adminStore.addToast('Question must have at least 2 options', 'error')
    return
  }
  currentQuestion.value.options.splice(optIndex, 1)
}

// Save Quiz
async function saveQuiz(publish = false) {
  if (!editingQuiz.value) return
  if (publish) {
    editingQuiz.value.status = 'active'
  }
  editingQuiz.value.questions_count = editingQuiz.value.questions_data.length
  
  const res = await adminStore.updateQuiz(editingQuiz.value.id, editingQuiz.value)
  if (res.success) {
    adminStore.addToast(publish ? 'Quiz published successfully!' : 'Quiz draft saved successfully!', 'success')
  }
}

// Reset filters
function resetFilters() {
  searchQuery.value = ''
  selectedStatus.value = 'all'
  selectedAudience.value = 'all'
  selectedDateRange.value = 'all'
  adminStore.fetchQuizzes()
}

// Preview Modal Logic
function startPreview(quiz) {
  editingQuiz.value = quiz || editingQuiz.value
  previewCurrentStep.value = 0
  previewAnswers.value = {}
  showPreviewModal.value = true
}

function selectPreviewAnswer(questionId, option) {
  previewAnswers.value[questionId] = option
  if (previewCurrentStep.value < (editingQuiz.value.questions_data.length - 1)) {
    previewCurrentStep.value++
  } else {
    previewCurrentStep.value = editingQuiz.value.questions_data.length // Results stage
  }
}

function exportQuizzesCSV() {
  const items = adminStore.quizzes
  if (!items || items.length === 0) return
  const headers = ['ID', 'Title', 'Status', 'Questions', 'Completions', 'Completion Rate']
  const rows = items.map(q => [
    q.id,
    `"${q.title}"`,
    q.status,
    q.questions_count,
    q.completions,
    `"${q.completion_rate}"`
  ])
  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `lumea_quizzes_${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  adminStore.addToast('Quizzes exported (CSV)', 'success')
}
</script>

<template>
  <div class="skin-quiz-page-wrapper">
    <!-- ========================================== -->
    <!-- VIEW 1: QUIZZES MANAGEMENT LIST VIEW       -->
    <!-- ========================================== -->
    <div v-if="currentView === 'list'" class="quiz-management-view">
      <!-- BREADCRUMB -->
      <div class="breadcrumb-bar">
        <span class="crumb-parent">Skin Quiz</span>
        <span class="crumb-sep">></span>
        <span class="crumb-current">Management</span>
      </div>

      <!-- HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">Skin Quiz Management</h1>
          <p class="hero-subtitle">Create and manage skin quizzes to personalize product recommendations.</p>
        </div>

        <div class="hero-art-side">
          <img src="/images/admin-hero-bottles.jpg" alt="Luméa Quiz Atelier" class="hero-art-img" />
          <div class="hero-quote">
            <span class="quote-line-1">Better questions.</span>
            <span class="quote-line-2">Healthier skin.</span>
          </div>
          <button class="btn-create-top" @click="openCreateQuiz">
            <Plus class="w-4 h-4 mr-1" />
            <span>Create Quiz</span>
          </button>
        </div>
      </div>

      <!-- 4 KPI METRICS CARDS -->
      <div class="kpi-grid">
        <!-- 1. Total Quizzes -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <FileText class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.quizzesKpis.total_quizzes }}</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Total Quizzes</span>
            </div>
          </div>
        </div>

        <!-- 2. Total Completions -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Users class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.quizzesKpis.total_completions?.toLocaleString() }}</span>
              <span class="kpi-badge positive">↗ +28%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Total Completions</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 3. Completion Rate -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <BarChart2 class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.quizzesKpis.completion_rate }}</span>
              <span class="kpi-badge positive">↗ +5%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Completion Rate</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>

        <!-- 4. Satisfaction -->
        <div class="kpi-card">
          <div class="kpi-icon-wrap rose-soft">
            <Star class="w-5 h-5 text-crimson" />
          </div>
          <div class="kpi-info">
            <div class="kpi-top">
              <span class="kpi-num">{{ adminStore.quizzesKpis.satisfaction }}</span>
              <span class="kpi-badge positive">↗ +12%</span>
            </div>
            <div class="kpi-sub">
              <span class="kpi-label">Avg. Recommendation Satisfaction</span>
              <span class="kpi-compare">vs last month</span>
            </div>
          </div>
        </div>
      </div>

      <!-- FILTER TOOLBAR -->
      <div class="filter-toolbar">
        <div class="search-input-wrap">
          <Search class="search-icon w-4 h-4" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search quizzes, questions, or results..."
            class="search-input"
          />
        </div>

        <!-- Status Filter -->
        <div class="filter-field">
          <label class="filter-label">Status</label>
          <select v-model="selectedStatus" class="filter-select">
            <option value="all">All Statuses</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
          </select>
        </div>

        <!-- Target Audience -->
        <div class="filter-field">
          <label class="filter-label">Target Audience</label>
          <select v-model="selectedAudience" class="filter-select">
            <option value="all">All Audiences</option>
            <option value="beginners">Beginners</option>
            <option value="sensitive">Sensitive Skin</option>
            <option value="enthusiasts">Skincare Enthusiasts</option>
          </select>
        </div>

        <!-- Date Range -->
        <div class="filter-field">
          <label class="filter-label">Date Range</label>
          <select v-model="selectedDateRange" class="filter-select">
            <option value="all">All Time</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>

        <!-- Action buttons -->
        <div class="filter-actions">
          <button class="btn-filter-action" @click="resetFilters">
            <RotateCcw class="w-3.5 h-3.5 mr-1" />
            <span>Reset</span>
          </button>
          <button class="btn-filter-action" @click="exportQuizzesCSV">
            <Download class="w-3.5 h-3.5 mr-1" />
            <span>Export</span>
          </button>
        </div>
      </div>

      <!-- QUIZZES TABLE -->
      <div class="table-card">
        <table class="quizzes-table">
          <thead>
            <tr>
              <th class="th-num">#</th>
              <th class="th-info">Quiz Information</th>
              <th class="th-center">Questions</th>
              <th class="th-center">Completions</th>
              <th class="th-rate">Completion Rate</th>
              <th class="th-date">Last Updated</th>
              <th class="th-status">Status</th>
              <th class="th-actions">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(quiz, index) in filteredQuizzes" :key="quiz.id">
              <!-- Index -->
              <td class="td-num">{{ index + 1 }}</td>

              <!-- Quiz Info with thumbnail card -->
              <td class="td-info">
                <div class="quiz-info-block">
                  <div class="quiz-visual-thumb">
                    <img :src="quiz.cover_image || '/images/quiz-model.jpg'" :alt="quiz.title" class="thumb-img" />
                    <div class="thumb-overlay">
                      <span class="thumb-label">{{ quiz.title }}</span>
                      <ArrowRight class="w-3 h-3 text-white mt-1" />
                    </div>
                  </div>

                  <div class="quiz-text-body">
                    <h3 class="quiz-name">{{ quiz.title }}</h3>
                    <p class="quiz-desc">{{ quiz.description }}</p>
                    <div class="quiz-tag-row">
                      <span class="badge-tag pink">{{ quiz.badge || 'Skin Type' }}</span>
                      <span class="badge-tag gray">{{ quiz.level || 'Beginner' }}</span>
                    </div>
                  </div>
                </div>
              </td>

              <!-- Questions Count -->
              <td class="td-center font-medium">{{ quiz.questions_count }}</td>

              <!-- Completions -->
              <td class="td-center font-medium">{{ quiz.completions?.toLocaleString() }}</td>

              <!-- Completion Rate Progress -->
              <td class="td-rate">
                <div class="rate-cell">
                  <span class="rate-pct">{{ quiz.completion_rate }}</span>
                  <div class="progress-bar-wrap">
                    <div
                      class="progress-bar-fill"
                      :style="{ width: quiz.completion_rate }"
                    ></div>
                  </div>
                </div>
              </td>

              <!-- Last Updated -->
              <td class="td-date">{{ quiz.updated_at }}</td>

              <!-- Status -->
              <td class="td-status">
                <span class="badge-status" :class="quiz.status === 'active' ? 'status-active' : 'status-draft'">
                  {{ quiz.status === 'active' ? 'Active' : 'Draft' }}
                </span>
              </td>

              <!-- Actions -->
              <td class="td-actions">
                <div class="action-buttons-wrap">
                  <button class="btn-action-outline" @click="openEditQuiz(quiz)">
                    <Edit class="w-3.5 h-3.5 mr-1" />
                    <span>Edit</span>
                  </button>
                  <button class="btn-action-outline" @click="startPreview(quiz)">
                    <Eye class="w-3.5 h-3.5 mr-1" />
                    <span>Preview</span>
                  </button>

                  <div class="dropdown-wrap">
                    <button class="btn-action-dots" @click="activeDropdown = activeDropdown === quiz.id ? null : quiz.id">
                      <MoreHorizontal class="w-4 h-4" />
                    </button>

                    <div v-if="activeDropdown === quiz.id" class="dropdown-menu">
                      <button class="dropdown-item" @click="handleToggleStatus(quiz)">
                        <Check class="w-4 h-4 mr-2" />
                        <span>Toggle Status ({{ quiz.status === 'active' ? 'Draft' : 'Active' }})</span>
                      </button>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- TABLE FOOTER -->
        <div class="table-footer">
          <span class="footer-count">Showing 1 to {{ filteredQuizzes.length }} of {{ filteredQuizzes.length }} quizzes</span>
          <div class="pagination-bar">
            <button class="btn-page-nav" disabled>&lt;</button>
            <button class="btn-page-num active">1</button>
            <button class="btn-page-nav" disabled>&gt;</button>
            <span class="page-size-label">10 / page ⌄</span>
          </div>
        </div>
      </div>

      <!-- BOTTOM BANNER -->
      <div class="bottom-card">
        <div class="bottom-left">
          <Lightbulb class="w-5 h-5 text-crimson mr-3 flex-shrink-0" />
          <div>
            <h4 class="bottom-title">Need inspiration?</h4>
            <p class="bottom-subtitle">Create engaging questions and personalized results to improve customer experience and boost sales.</p>
          </div>
        </div>
        <a href="javascript:void(0)" class="btn-bottom-outline">
          <span>View Best Practices</span>
          <ExternalLink class="w-3.5 h-3.5 ml-1" />
        </a>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- VIEW 2: QUIZ EDITOR DASHBOARD VIEW         -->
    <!-- ========================================== -->
    <div v-else-if="currentView === 'editor'" class="quiz-editor-view">
      <!-- BREADCRUMB -->
      <div class="breadcrumb-bar">
        <span class="crumb-parent clickable" @click="returnToList">Skin Quiz</span>
        <span class="crumb-sep">></span>
        <span class="crumb-current">Edit Quiz</span>
      </div>

      <!-- EDITOR HERO BANNER -->
      <div class="hero-banner">
        <div class="hero-content">
          <div class="title-with-status">
            <h1 class="hero-title">Edit Quiz: {{ editingQuiz.title }}</h1>
            <span class="badge-status status-active ml-2">Active</span>
          </div>
          <p class="hero-subtitle">{{ editingQuiz.description }}</p>
        </div>

        <div class="hero-art-side">
          <img src="/images/admin-hero-bottles.jpg" alt="Luméa Quiz Atelier" class="hero-art-img" />
          <div class="hero-quote">
            <span class="quote-line-1">Personalized</span>
            <span class="quote-line-2">skincare for a brighter you.</span>
          </div>
          <div class="editor-header-actions">
            <button class="btn-header-outline" @click="startPreview(editingQuiz)">
              <Eye class="w-4 h-4 mr-1" />
              <span>Preview</span>
            </button>
            <button class="btn-header-outline" @click="saveQuiz(false)">
              <Save class="w-4 h-4 mr-1" />
              <span>Save Draft</span>
            </button>
            <button class="btn-header-primary" @click="saveQuiz(true)">
              <Send class="w-4 h-4 mr-1" />
              <span>Publish</span>
            </button>
          </div>
        </div>
      </div>

      <!-- TABS HEADER -->
      <div class="editor-tabs-bar">
        <button
          v-for="t in ['Builder', 'Appearance', 'Results & Recommendations', 'Settings']"
          :key="t"
          class="editor-tab-btn"
          :class="{ active: activeTab === t }"
          @click="activeTab = t"
        >
          {{ t }}
        </button>
      </div>

      <!-- TAB 1: BUILDER 3-COLUMN STUDIO LAYOUT -->
      <div v-if="activeTab === 'Builder'" class="builder-three-columns">
        <!-- 1. LEFT COLUMN: QUIZ STRUCTURE -->
        <div class="col-structure">
          <div class="col-header-row">
            <h3 class="col-heading">Quiz Structure</h3>
            <button class="btn-add-step" @click="addQuestion">
              <Plus class="w-3.5 h-3.5 mr-1" />
              <span>Add Question</span>
            </button>
          </div>

          <div class="step-list">
            <div
              v-for="(q, idx) in editingQuiz.questions_data"
              :key="q.id"
              class="step-card"
              :class="{ active: selectedQuestionIndex === idx }"
              @click="selectedQuestionIndex = idx"
            >
              <GripVertical class="w-4 h-4 text-taupe mr-1 drag-handle" />
              <span class="step-num">{{ idx + 1 }}</span>
              <div class="step-icon-box">
                <Shield v-if="idx === 0" class="w-3.5 h-3.5 text-crimson" />
                <Tag v-else-if="idx % 2 === 1" class="w-3.5 h-3.5 text-taupe" />
                <Grid v-else class="w-3.5 h-3.5 text-taupe" />
              </div>
              <div class="step-info">
                <span class="step-title">{{ q.question }}</span>
                <span class="step-type">{{ q.type }}</span>
              </div>
            </div>

            <!-- Results Step -->
            <div class="step-card step-results" @click="activeTab = 'Results & Recommendations'">
              <GripVertical class="w-4 h-4 text-taupe mr-1 drag-handle" />
              <span class="step-num">{{ editingQuiz.questions_data.length + 1 }}</span>
              <div class="step-icon-box">
                <Award class="w-3.5 h-3.5 text-crimson" />
              </div>
              <div class="step-info">
                <span class="step-title">Results</span>
                <span class="step-type">Show Result & Recommendations</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. MIDDLE COLUMN: QUESTION EDITOR -->
        <div class="col-editor" v-if="currentQuestion">
          <div class="col-header-row">
            <h3 class="col-heading">Question Editor</h3>
            <div class="type-picker">
              <span class="type-label">Question Type</span>
              <select v-model="currentQuestion.type" class="type-select">
                <option value="Single Choice">Single Choice</option>
                <option value="Multiple Choice">Multiple Choice</option>
                <option value="Dropdown">Dropdown</option>
              </select>
            </div>
          </div>

          <!-- Question Input -->
          <div class="form-group">
            <div class="label-row">
              <label class="form-label">Question</label>
              <span class="char-counter">{{ (currentQuestion.question || '').length }}/200</span>
            </div>
            <input
              v-model="currentQuestion.question"
              type="text"
              class="form-input"
              maxlength="200"
            />
          </div>

          <!-- Description Input -->
          <div class="form-group">
            <div class="label-row">
              <label class="form-label">Description (Optional)</label>
              <span class="char-counter">{{ (currentQuestion.description || '').length }}/200</span>
            </div>
            <textarea
              v-model="currentQuestion.description"
              class="form-textarea"
              rows="2"
              maxlength="200"
            ></textarea>
          </div>

          <!-- Options List -->
          <div class="options-section">
            <label class="form-label mb-2 block">Options</label>
            <div class="options-list">
              <div
                v-for="(opt, optIdx) in currentQuestion.options"
                :key="opt.id || optIdx"
                class="option-row"
              >
                <GripVertical class="w-4 h-4 text-taupe mr-1 drag-handle" />
                <img :src="opt.image || '/images/texture-normal.jpg'" :alt="opt.title" class="opt-thumb" />
                <div class="opt-inputs">
                  <input v-model="opt.title" type="text" class="opt-title-input" placeholder="Option title" />
                  <input v-model="opt.desc" type="text" class="opt-desc-input" placeholder="Option description" />
                </div>
                <button class="btn-opt-trash" @click="removeOption(optIdx)" title="Remove Option">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Add Option Button -->
            <button class="btn-add-option" @click="addOption">
              <Plus class="w-3.5 h-3.5 mr-1" />
              <span>Add Option</span>
            </button>
          </div>

          <!-- Required Toggle Switch -->
          <div class="toggle-card">
            <label class="switch-wrap">
              <input type="checkbox" v-model="currentQuestion.required" class="switch-checkbox" />
              <span class="switch-slider"></span>
            </label>
            <div class="toggle-text">
              <span class="toggle-title">Make this question required</span>
              <span class="toggle-sub">Users must answer this question to continue.</span>
            </div>
          </div>
        </div>

        <!-- 3. RIGHT COLUMN: QUESTION SETTINGS & RECOMMENDATION RULES -->
        <div class="col-settings" v-if="currentQuestion">
          <!-- Question Settings Card -->
          <div class="settings-box">
            <h4 class="box-title">Question Settings</h4>

            <div class="form-group mt-3">
              <label class="form-label">Question Image (Optional)</label>
              <div class="img-preview-row">
                <img :src="currentQuestion.image || '/images/quiz-model.jpg'" alt="Question Header" class="q-img-preview" />
                <div class="q-img-actions">
                  <button class="btn-change-img" @click="alert('Upload / select new question image...')">
                    <ImageIcon class="w-3.5 h-3.5 mr-1" />
                    <span>Change Image</span>
                  </button>
                  <button class="btn-del-img" @click="currentQuestion.image = null">
                    <Trash2 class="w-3.5 h-3.5 text-taupe" />
                  </button>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Help Text (Optional)</label>
              <input
                v-model="currentQuestion.help_text"
                type="text"
                placeholder="This helps us recommend the right products for your skin."
                class="form-input"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Display Order</label>
              <select v-model="currentQuestion.step" class="form-select">
                <option v-for="n in editingQuiz.questions_data.length" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
          </div>

          <!-- Recommendation Rules Card -->
          <div class="settings-box mt-4">
            <h4 class="box-title">Recommendation Rules</h4>
            <p class="box-subtitle">Set which skin type(s) this answer maps to for personalized product recommendations.</p>

            <table class="rules-table">
              <thead>
                <tr>
                  <th>Option</th>
                  <th>Maps to Skin Type</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="opt in currentQuestion.options" :key="opt.id">
                  <td class="font-medium text-charcoal">{{ opt.title }}</td>
                  <td>
                    <select v-model="opt.maps_to" class="rule-select" :class="`pill-${(opt.maps_to || 'Normal').toLowerCase()}`">
                      <option value="Oily">Oily</option>
                      <option value="Dry">Dry</option>
                      <option value="Combination">Combination</option>
                      <option value="Normal">Normal</option>
                      <option value="Sensitive">Sensitive</option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Tip Card -->
          <div class="tip-card mt-4">
            <Lightbulb class="w-5 h-5 text-crimson mr-2 flex-shrink-0" />
            <div>
              <h5 class="tip-heading">Tip</h5>
              <p class="tip-text">Map each answer to one or more skin types to show the most relevant product recommendations.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: APPEARANCE -->
      <div v-else-if="activeTab === 'Appearance'" class="appearance-pane">
        <div class="settings-box">
          <h3 class="box-title">Quiz Visual Styling</h3>
          <p class="box-subtitle">Configure color theme, typography, and card transitions.</p>
          <div class="color-options mt-4 flex gap-4">
            <div class="color-chip active" style="background: #FBF8F5; border: 2px solid #84261B; padding: 1rem; border-radius: 8px;">
              <span class="text-sm font-semibold text-charcoal">Warm Bisque Atelier (Default)</span>
            </div>
            <div class="color-chip" style="background: #FAF6F2; border: 1px solid #EBE1D7; padding: 1rem; border-radius: 8px;">
              <span class="text-sm font-semibold text-charcoal">Pure Minimalist Ivory</span>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: RESULTS & RECOMMENDATIONS -->
      <div v-else-if="activeTab === 'Results & Recommendations'" class="results-pane">
        <div class="settings-box">
          <h3 class="box-title">Results Logic & Regimen Generator</h3>
          <p class="box-subtitle">Configure skin diagnostic profiles and bundle routines.</p>
          <div class="routine-preview-card mt-4 p-4 border border-sand rounded-lg bg-warm-white">
            <h4 class="font-serif text-lg text-crimson font-medium">Curated Morning & Evening Regimen</h4>
            <p class="text-sm text-taupe mt-1">Automatically binds high-compatibility products from the Luméa catalog.</p>
          </div>
        </div>
      </div>

      <!-- TAB 4: SETTINGS -->
      <div v-else class="quiz-settings-pane">
        <div class="settings-box">
          <h3 class="box-title">General Quiz Configuration</h3>
          <div class="form-group mt-4">
            <label class="form-label">Quiz URL Slug</label>
            <input v-model="editingQuiz.slug" type="text" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Target Audience Badge</label>
            <input v-model="editingQuiz.target_audience" type="text" class="form-input" />
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- INTERACTIVE QUIZ PREVIEW MODAL             -->
    <!-- ========================================== -->
    <div v-if="showPreviewModal && editingQuiz" class="modal-backdrop" @click.self="showPreviewModal = false">
      <div class="modal-preview-card">
        <div class="preview-header">
          <div>
            <span class="preview-tag">Quiz Simulator</span>
            <h2 class="preview-title">{{ editingQuiz.title }}</h2>
          </div>
          <button class="btn-close-modal" @click="showPreviewModal = false">×</button>
        </div>

        <div class="preview-body">
          <!-- Step Questions -->
          <div v-if="previewCurrentStep < editingQuiz.questions_data.length" class="quiz-step-pane">
            <div class="preview-step-counter">
              Step {{ previewCurrentStep + 1 }} of {{ editingQuiz.questions_data.length }}
            </div>
            <h3 class="preview-q-title">{{ editingQuiz.questions_data[previewCurrentStep].question }}</h3>
            <p class="preview-q-desc">{{ editingQuiz.questions_data[previewCurrentStep].description }}</p>

            <div class="preview-options-grid">
              <div
                v-for="opt in editingQuiz.questions_data[previewCurrentStep].options"
                :key="opt.id"
                class="preview-opt-card"
                :class="{ selected: previewAnswers[editingQuiz.questions_data[previewCurrentStep].id]?.id === opt.id }"
                @click="selectPreviewAnswer(editingQuiz.questions_data[previewCurrentStep].id, opt)"
              >
                <img :src="opt.image || '/images/texture-normal.jpg'" :alt="opt.title" class="preview-opt-img" />
                <div class="preview-opt-text">
                  <span class="preview-opt-title">{{ opt.title }}</span>
                  <span class="preview-opt-desc">{{ opt.desc }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Results stage -->
          <div v-else class="preview-results-pane text-center py-6">
            <Sparkles class="w-12 h-12 text-crimson mx-auto mb-3" />
            <h3 class="font-serif text-2xl text-charcoal">Your Skin Profile Diagnosis</h3>
            <p class="text-sm text-taupe mt-1 mb-6">Based on your diagnostic answers, your primary skin profile is <strong>Combination & Dehydrated</strong>.</p>
            <button class="btn-primary" @click="previewCurrentStep = 0; previewAnswers = {}">Restart Simulation</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Page Layout */
.quiz-management-view, .quiz-editor-view {
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

.crumb-parent.clickable {
  cursor: pointer;
  text-decoration: underline;
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

.title-with-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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

.btn-create-top {
  display: inline-flex;
  align-items: center;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(132, 38, 27, 0.2);
}

.editor-header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-header-outline {
  display: inline-flex;
  align-items: center;
  background: #FFFFFF;
  color: #2D2422;
  border: 1px solid #EBE1D7;
  padding: 0.55rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  cursor: pointer;
}

.btn-header-primary {
  display: inline-flex;
  align-items: center;
  background: #84261B;
  color: #FFFFFF;
  border: none;
  padding: 0.55rem 1.25rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  cursor: pointer;
}

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

.text-crimson { color: #84261B; }

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
}

.kpi-badge.positive {
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.15rem 0.4rem;
  border-radius: 12px;
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
  min-width: 220px;
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

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.filter-label {
  font-size: 0.6875rem;
  color: #8C827A;
  text-transform: uppercase;
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
}

.filter-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
}

.btn-filter-action {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.45rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  color: #6E635E;
  cursor: pointer;
}

/* Table Card */
.table-card {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  overflow: hidden;
}

.quizzes-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
}

.quizzes-table th {
  background: #FAF6F2;
  padding: 0.75rem 0.875rem;
  font-weight: 600;
  color: #6E635E;
  text-align: left;
  border-bottom: 1px solid #EBE1D7;
  font-size: 0.75rem;
}

.th-center, .td-center {
  text-align: center;
}

.quizzes-table td {
  padding: 1rem 0.875rem;
  border-bottom: 1px solid #F5ECE6;
  vertical-align: middle;
}

.quiz-info-block {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.quiz-visual-thumb {
  width: 110px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  flex-shrink: 0;
  border: 1px solid #EBE1D7;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-overlay {
  position: absolute;
  inset: 0;
  background: rgba(45, 36, 34, 0.4);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0.4rem;
}

.thumb-label {
  color: #FFFFFF;
  font-size: 0.6875rem;
  font-weight: 600;
  line-height: 1.1;
}

.quiz-text-body {
  display: flex;
  flex-direction: column;
}

.quiz-name {
  font-family: var(--font-sans, sans-serif);
  font-size: 0.875rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.quiz-desc {
  font-size: 0.75rem;
  color: #8C827A;
  margin: 0.2rem 0 0.4rem 0;
}

.quiz-tag-row {
  display: flex;
  gap: 0.35rem;
}

.badge-tag {
  font-size: 0.625rem;
  padding: 0.15rem 0.45rem;
  border-radius: 10px;
  font-weight: 500;
}

.badge-tag.pink {
  background: #FCECE9;
  color: #84261B;
}

.badge-tag.gray {
  background: #F0E8E1;
  color: #6E635E;
}

.rate-cell {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: 90px;
}

.rate-pct {
  font-weight: 600;
  color: #2D2422;
  font-size: 0.75rem;
}

.progress-bar-wrap {
  width: 100%;
  height: 6px;
  background: #F0E8E1;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: #84261B;
  border-radius: 3px;
}

.badge-status {
  padding: 0.2rem 0.65rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #EAF5EE;
  color: #2D8A4E;
}

.status-draft {
  background: #F0E8E1;
  color: #6E635E;
}

.action-buttons-wrap {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.btn-action-outline {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  color: #2D2422;
  cursor: pointer;
}

.btn-action-dots {
  width: 28px;
  height: 28px;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6E635E;
}

.table-footer {
  padding: 0.875rem 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #EBE1D7;
  background: #FAF6F2;
}

.footer-count {
  font-size: 0.75rem;
  color: #6E635E;
}

.pagination-bar {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.btn-page-nav, .btn-page-num {
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

.btn-page-num.active {
  background: #84261B;
  color: #FFFFFF;
  border-color: #84261B;
}

/* Bottom Card */
.bottom-card {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bottom-left {
  display: flex;
  align-items: center;
}

.bottom-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.bottom-subtitle {
  font-size: 0.75rem;
  color: #6E635E;
  margin: 0.15rem 0 0 0;
}

.btn-bottom-outline {
  display: inline-flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid #E4D8CE;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #2D2422;
  text-decoration: none;
}

/* ==================================== */
/* EDITOR STYLES                        */
/* ==================================== */
.editor-tabs-bar {
  display: flex;
  border-bottom: 1px solid #EBE1D7;
  gap: 1.5rem;
}

.editor-tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 0;
  font-size: 0.875rem;
  font-weight: 500;
  color: #8C827A;
  cursor: pointer;
  position: relative;
}

.editor-tab-btn.active {
  color: #84261B;
  font-weight: 600;
}

.editor-tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #84261B;
}

/* 3-Column Studio */
.builder-three-columns {
  display: grid;
  grid-template-columns: 280px 1fr 340px;
  gap: 1.25rem;
  align-items: flex-start;
}

.col-structure, .col-editor, .col-settings {
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  border-radius: 10px;
  padding: 1.25rem;
}

.col-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #F5ECE6;
}

.col-heading {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.btn-add-step {
  background: none;
  border: none;
  color: #84261B;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

/* Step list */
.step-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.step-card {
  display: flex;
  align-items: center;
  padding: 0.65rem 0.75rem;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  background: #FAF6F2;
  cursor: pointer;
  transition: all 0.15s ease;
}

.step-card:hover {
  background: #F8EFE9;
}

.step-card.active {
  background: #FDF4F0;
  border-color: #84261B;
}

.step-num {
  font-size: 0.75rem;
  font-weight: 700;
  color: #2D2422;
  width: 20px;
}

.step-icon-box {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: #FFFFFF;
  border: 1px solid #EBE1D7;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
}

.step-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.step-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.step-type {
  font-size: 0.6875rem;
  color: #8C827A;
}

/* Middle Col: Form Inputs */
.type-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.type-label {
  font-size: 0.75rem;
  color: #8C827A;
}

.type-select {
  padding: 0.35rem 0.65rem;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  font-size: 0.75rem;
  background: #FAF6F2;
}

.form-group {
  margin-bottom: 1rem;
}

.label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.form-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

.char-counter {
  font-size: 0.6875rem;
  color: #B5ABA4;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0.55rem 0.75rem;
  font-size: 0.8125rem;
  background: #FFFFFF;
  color: #2D2422;
  outline: none;
}

.form-input:focus, .form-textarea:focus {
  border-color: #84261B;
}

/* Options Editor */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-row {
  display: flex;
  align-items: center;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  background: #FAF6F2;
  gap: 0.5rem;
}

.opt-thumb {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #EBE1D7;
}

.opt-inputs {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.opt-title-input {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2D2422;
  border: none;
  background: transparent;
  outline: none;
}

.opt-desc-input {
  font-size: 0.6875rem;
  color: #8C827A;
  border: none;
  background: transparent;
  outline: none;
}

.btn-opt-trash {
  background: none;
  border: none;
  color: #C0392B;
  cursor: pointer;
  opacity: 0.7;
}

.btn-opt-trash:hover {
  opacity: 1;
}

.btn-add-option {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #FDF2EE;
  border: 1px dashed #E5B2A9;
  color: #84261B;
  padding: 0.55rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: 0.75rem;
  cursor: pointer;
}

/* Switch Toggle */
.toggle-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-top: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid #F5ECE6;
}

.switch-wrap {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 22px;
}

.switch-checkbox {
  opacity: 0;
  width: 0;
  height: 0;
}

.switch-slider {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background-color: #D6CBC2;
  transition: .3s;
  border-radius: 22px;
}

.switch-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}

.switch-checkbox:checked + .switch-slider {
  background-color: #84261B;
}

.switch-checkbox:checked + .switch-slider:before {
  transform: translateX(16px);
}

.toggle-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2D2422;
  display: block;
}

.toggle-sub {
  font-size: 0.6875rem;
  color: #8C827A;
}

/* Col 3 Settings */
.settings-box {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 1rem;
}

.box-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0;
}

.box-subtitle {
  font-size: 0.6875rem;
  color: #8C827A;
  margin: 0.25rem 0 0.75rem 0;
  line-height: 1.35;
}

.img-preview-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.q-img-preview {
  width: 90px;
  height: 55px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #EBE1D7;
}

.q-img-actions {
  display: flex;
  gap: 0.35rem;
  align-items: center;
}

.btn-change-img {
  display: inline-flex;
  align-items: center;
  border: 1px solid #E4D8CE;
  background: #FFFFFF;
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.6875rem;
  cursor: pointer;
}

.btn-del-img {
  background: none;
  border: 1px solid #E4D8CE;
  border-radius: 6px;
  padding: 0.35rem;
  cursor: pointer;
}

/* Recommendation Rules Table */
.rules-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.75rem;
}

.rules-table th {
  text-align: left;
  padding: 0.45rem 0;
  font-weight: 600;
  color: #8C827A;
  border-bottom: 1px solid #EBE1D7;
}

.rules-table td {
  padding: 0.5rem 0;
  border-bottom: 1px solid #F5ECE6;
}

.rule-select {
  border: none;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.6875rem;
  font-weight: 600;
  cursor: pointer;
}

.pill-oily { background: #FDECEB; color: #C0392B; }
.pill-dry { background: #EBF4FE; color: #2980B9; }
.pill-combination { background: #FEF5E7; color: #D35400; }
.pill-normal { background: #EAF5EE; color: #27AE60; }
.pill-sensitive { background: #F3EBFA; color: #8E44AD; }

/* Tip card */
.tip-card {
  background: #FAF6F2;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  padding: 0.875rem;
  display: flex;
  align-items: flex-start;
}

.tip-heading {
  font-size: 0.75rem;
  font-weight: 600;
  color: #84261B;
  margin: 0;
}

.tip-text {
  font-size: 0.6875rem;
  color: #6E635E;
  margin: 0.2rem 0 0 0;
  line-height: 1.35;
}

/* Simulator Modal */
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

.modal-preview-card {
  background: #FFFFFF;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid #EBE1D7;
}

.preview-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #F5ECE6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF6F2;
}

.preview-tag {
  font-size: 0.6875rem;
  color: #84261B;
  text-transform: uppercase;
  font-weight: 600;
}

.preview-title {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.25rem;
  font-weight: 600;
  color: #2D2422;
  margin: 0.15rem 0 0 0;
}

.btn-close-modal {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #8C827A;
  cursor: pointer;
}

.preview-body {
  padding: 1.5rem;
}

.preview-step-counter {
  font-size: 0.75rem;
  color: #84261B;
  font-weight: 600;
  text-transform: uppercase;
}

.preview-q-title {
  font-family: var(--font-serif, Georgia, serif);
  font-size: 1.35rem;
  color: #2D2422;
  margin: 0.35rem 0 0.2rem 0;
}

.preview-q-desc {
  font-size: 0.8125rem;
  color: #8C827A;
  margin-bottom: 1.25rem;
}

.preview-options-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.preview-opt-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid #EBE1D7;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.preview-opt-card:hover {
  border-color: #84261B;
  background: #FDF4F0;
}

.preview-opt-img {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  object-fit: cover;
}

.preview-opt-text {
  display: flex;
  flex-direction: column;
}

.preview-opt-title {
  font-weight: 600;
  font-size: 0.875rem;
  color: #2D2422;
}

.preview-opt-desc {
  font-size: 0.75rem;
  color: #8C827A;
}

@media (max-width: 1200px) {
  .builder-three-columns {
    grid-template-columns: 1fr;
  }
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
