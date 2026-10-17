<template>
  <div class="lumea-quiz-questions-view">
    <div class="container quiz-layout-container">
      <!-- ============================================================= -->
      <!-- 1. LEFT EDITORIAL COLUMN (Sticky)                             -->
      <!-- ============================================================= -->
      <aside class="quiz-left-editorial">
        <div class="editorial-card">
          <div class="editorial-eyebrow">LUMÉA SKIN QUIZ</div>
          <h2 class="editorial-title">
            Small Questions.<br>
            A Brighter <span class="text-terracotta">You.</span>
          </h2>
          <div class="editorial-divider"></div>
          <p class="editorial-desc">
            Because your skin is unique, your routine should be too.
          </p>
          <div class="editorial-image-box">
            <img
              src="/images/deals-showcase-bottles.jpg"
              alt="Luméa Pure Skincare Formula"
              class="editorial-img"
            />
          </div>
        </div>
      </aside>

      <!-- ============================================================= -->
      <!-- 2. MAIN QUESTIONNAIRE STAGE                                    -->
      <!-- ============================================================= -->
      <main class="quiz-main-stage">
        <!-- Top Nav & Progress -->
        <div class="stage-top-bar">
          <button class="btn-text-nav" @click="prevStep" :disabled="currentStep === 1">
            <ArrowLeft :size="16" />
            <span>Back</span>
          </button>

          <div class="top-progress-indicator">
            <div class="progress-bar-track">
              <div
                class="progress-bar-fill"
                :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
              ></div>
            </div>
            <span class="step-label">Question {{ currentStep }} of {{ totalSteps }}</span>
          </div>

          <button class="btn-text-nav skip-btn" @click="nextStep">
            <span>Skip Question</span>
          </button>
        </div>

        <!-- Dynamic Question Card -->
        <div class="question-surface-card animate-fade-in">
          <!-- Step 1: Goals -->
          <div v-if="currentStep === 1" class="question-step-content">
            <div class="question-category-tag">YOUR GOALS</div>
            <h1 class="question-main-title">What are your primary skincare goals?</h1>
            <p class="question-subtitle">Select up to 3 goals that matter most to you right now.</p>

            <div class="options-grid-chips">
              <button
                v-for="goal in goalOptions"
                :key="goal.id"
                class="option-chip-card"
                :class="{ 'is-selected': isGoalSelected(goal.label) }"
                @click="toggleGoal(goal.label)"
              >
                <div class="chip-icon-box">
                  <component :is="goal.icon" :size="20" />
                </div>
                <div class="chip-info">
                  <div class="chip-title">{{ goal.label }}</div>
                  <div class="chip-desc">{{ goal.desc }}</div>
                </div>
                <div class="chip-check" v-if="isGoalSelected(goal.label)">
                  <Check :size="14" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 2: Skin Type (Visual Texture Grid) -->
          <div v-else-if="currentStep === 2" class="question-step-content">
            <div class="question-category-tag">YOUR SKIN</div>
            <h1 class="question-main-title">What is your skin type?</h1>
            <p class="question-subtitle">Choose the option that best describes your skin.</p>

            <div class="skin-types-grid">
              <div
                v-for="type in skinTypeOptions"
                :key="type.id"
                class="skin-type-card"
                :class="{ 'is-selected': selectedSkinType === type.id }"
                @click="selectSkinType(type.id)"
              >
                <div class="type-texture-wrapper">
                  <img :src="type.image" :alt="type.name" class="type-texture-img" />
                  <div class="type-selected-badge" v-if="selectedSkinType === type.id">
                    <Check :size="16" />
                  </div>
                </div>
                <div class="type-card-body">
                  <div class="type-name">{{ type.name }}</div>
                  <div class="type-desc">{{ type.desc }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Concerns -->
          <div v-else-if="currentStep === 3" class="question-step-content">
            <div class="question-category-tag">SKIN CONCERNS</div>
            <h1 class="question-main-title">What concerns would you like to target?</h1>
            <p class="question-subtitle">Select any areas you want your routine to focus on.</p>

            <div class="options-grid-chips">
              <button
                v-for="concern in concernOptions"
                :key="concern.id"
                class="option-chip-card"
                :class="{ 'is-selected': isConcernSelected(concern.label) }"
                @click="toggleConcern(concern.label)"
              >
                <div class="chip-icon-box">
                  <component :is="concern.icon" :size="20" />
                </div>
                <div class="chip-info">
                  <div class="chip-title">{{ concern.label }}</div>
                  <div class="chip-desc">{{ concern.desc }}</div>
                </div>
                <div class="chip-check" v-if="isConcernSelected(concern.label)">
                  <Check :size="14" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 4: Lifestyle -->
          <div v-else-if="currentStep === 4" class="question-step-content">
            <div class="question-category-tag">LIFESTYLE & HABITS</div>
            <h1 class="question-main-title">Tell us about your daily lifestyle</h1>
            <p class="question-subtitle">Sun exposure, stress, and schedule affect barrier health.</p>

            <div class="options-list-rows">
              <button
                v-for="item in lifestyleOptions"
                :key="item.id"
                class="option-row-card"
                :class="{ 'is-selected': isLifestyleSelected(item.label) }"
                @click="toggleLifestyle(item.label)"
              >
                <div class="row-icon-box">
                  <component :is="item.icon" :size="20" />
                </div>
                <div class="row-info">
                  <div class="row-title">{{ item.label }}</div>
                  <div class="row-desc">{{ item.desc }}</div>
                </div>
                <div class="row-check" v-if="isLifestyleSelected(item.label)">
                  <Check :size="16" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 5: Environment -->
          <div v-else-if="currentStep === 5" class="question-step-content">
            <div class="question-category-tag">ENVIRONMENT</div>
            <h1 class="question-main-title">Where do you spend most of your time?</h1>
            <p class="question-subtitle">Your local climate directly shapes your hydration needs.</p>

            <div class="options-list-rows">
              <button
                v-for="env in environmentOptions"
                :key="env.id"
                class="option-row-card"
                :class="{ 'is-selected': isEnvSelected(env.label) }"
                @click="toggleEnv(env.label)"
              >
                <div class="row-icon-box">
                  <component :is="env.icon" :size="20" />
                </div>
                <div class="row-info">
                  <div class="row-title">{{ env.label }}</div>
                  <div class="row-desc">{{ env.desc }}</div>
                </div>
                <div class="row-check" v-if="isEnvSelected(env.label)">
                  <Check :size="16" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 6: Preferences -->
          <div v-else-if="currentStep === 6" class="question-step-content">
            <div class="question-category-tag">PREFERENCES</div>
            <h1 class="question-main-title">Any ingredient or formulation preferences?</h1>
            <p class="question-subtitle">We'll tailor suggestions to match your values.</p>

            <div class="options-grid-chips">
              <button
                v-for="pref in preferenceOptions"
                :key="pref.id"
                class="option-chip-card"
                :class="{ 'is-selected': isPrefSelected(pref.label) }"
                @click="togglePref(pref.label)"
              >
                <div class="chip-icon-box">
                  <component :is="pref.icon" :size="20" />
                </div>
                <div class="chip-info">
                  <div class="chip-title">{{ pref.label }}</div>
                  <div class="chip-desc">{{ pref.desc }}</div>
                </div>
                <div class="chip-check" v-if="isPrefSelected(pref.label)">
                  <Check :size="14" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 7: Current Routine -->
          <div v-else-if="currentStep === 7" class="question-step-content">
            <div class="question-category-tag">ROUTINE HABITS</div>
            <h1 class="question-main-title">How many steps do you prefer in your routine?</h1>
            <p class="question-subtitle">Choose the routine depth that fits your day-to-day rhythm.</p>

            <div class="options-list-rows">
              <button
                v-for="routine in routineDepthOptions"
                :key="routine.id"
                class="option-row-card"
                :class="{ 'is-selected': selectedRoutineDepth === routine.label }"
                @click="selectedRoutineDepth = routine.label"
              >
                <div class="row-icon-box">
                  <component :is="routine.icon" :size="20" />
                </div>
                <div class="row-info">
                  <div class="row-title">{{ routine.label }}</div>
                  <div class="row-desc">{{ routine.desc }}</div>
                </div>
                <div class="row-check" v-if="selectedRoutineDepth === routine.label">
                  <Check :size="16" />
                </div>
              </button>
            </div>
          </div>

          <!-- Step 8: Generating Analysis Animation -->
          <div v-else-if="currentStep === 8" class="analyzing-step-content">
            <div class="analyzing-loader-box">
              <div class="pulsing-emblem-ring">
                <Sparkles :size="38" class="pulsing-sparkle" />
              </div>
            </div>
            <h2 class="analyzing-title">Analyzing Your Skin Profile...</h2>
            <p class="analyzing-subtitle">Formulating your bespoke skincare regimen and ingredient synergy.</p>

            <div class="analyzing-checklist">
              <div class="check-item is-done">
                <CheckCircle2 :size="18" class="check-icon-done" />
                <span>Evaluating skin type & moisture balance</span>
              </div>
              <div class="check-item is-done">
                <CheckCircle2 :size="18" class="check-icon-done" />
                <span>Screening active ingredients for your concerns</span>
              </div>
              <div class="check-item is-done">
                <CheckCircle2 :size="18" class="check-icon-done" />
                <span>Sequencing 5-step morning & evening ritual</span>
              </div>
            </div>

            <button class="btn-view-results" @click="finalizeAndNavigate">
              <span>View My Results</span>
              <ArrowRight :size="18" />
            </button>
          </div>

          <!-- Footer Actions -->
          <div class="card-footer-actions" v-if="currentStep < 8">
            <button
              class="btn-outline-prev"
              @click="prevStep"
              :disabled="currentStep === 1"
            >
              Previous
            </button>

            <button
              class="btn-terracotta-next"
              @click="nextStep"
            >
              <span>{{ currentStep === 7 ? 'Generate Results' : 'Next Question' }}</span>
              <ArrowRight :size="16" />
            </button>
          </div>
        </div>
      </main>

      <!-- ============================================================= -->
      <!-- 3. RIGHT PROGRESS & WHY WE ASK COLUMN (Sticky)                -->
      <!-- ============================================================= -->
      <aside class="quiz-right-sidebar">
        <!-- Progress Checklist Card -->
        <div class="sidebar-progress-card">
          <div class="progress-card-header">
            <span class="progress-title">Your Progress</span>
            <span class="progress-counter">{{ currentStep }} / {{ totalSteps }}</span>
          </div>

          <div class="progress-mini-bar">
            <div
              class="mini-bar-fill"
              :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
            ></div>
          </div>

          <ul class="step-checklist">
            <li
              v-for="(stepName, idx) in stepNames"
              :key="idx"
              class="step-check-item"
              :class="{
                'is-active': currentStep === idx + 1,
                'is-completed': currentStep > idx + 1
              }"
            >
              <div class="step-bullet">
                <Check v-if="currentStep > idx + 1" :size="12" />
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <span class="step-name">{{ stepName }}</span>
            </li>
          </ul>
        </div>

        <!-- Why We Ask Card -->
        <div class="sidebar-why-card">
          <div class="why-icon-box">
            <Sprout :size="24" class="why-icon" />
          </div>
          <h4 class="why-title">Why We Ask?</h4>
          <p class="why-text">
            {{ currentWhyText }}
          </p>
          <div class="why-footer-quote">
            <em>Better Answers. Brighter Results.</em>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { useQuizStore } from '@/stores/quiz'
import {
  Activity,
  ArrowLeft,
  ArrowRight,
  Building,
  Check,
  CheckCircle2,
  Clock,
  CloudSun,
  Droplets,
  Flame,
  Heart,
  Leaf,
  Moon,
  ShieldAlert,
  ShieldCheck,
  Smile,
  Sparkles,
  Sprout,
  Sun,
  Zap
} from 'lucide-vue-next'
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const quizStore = useQuizStore()

onMounted(() => {
  quizStore.fetchActiveQuiz()
})

const currentStep = ref(3) // Default to step 3 as shown in format mockup
const totalSteps = 8

const stepNames = [
  'Your Goals',
  'Your Skin Type',
  'Your Skin Concerns',
  'Your Lifestyle',
  'Your Environment',
  'Your Preferences',
  'Your Routine',
  'Your Results'
]

// ================= QUESTION 1: GOALS =================
const goalOptions = [
  { id: 'clearer', label: 'Clearer Skin', desc: 'Prevent breakouts & minimize visible pores', icon: Sparkles },
  { id: 'hydration', label: 'Hydration', desc: 'Replenish moisture barrier & banish tightness', icon: Droplets },
  { id: 'brightening', label: 'Brighter Tone', desc: 'Fade dark spots & reveal vibrant glow', icon: Sun },
  { id: 'aging', label: 'Firming & Anti-Aging', desc: 'Boost collagen, smooth fine lines & restore elasticity', icon: Activity },
  { id: 'texture', label: 'Smoother Texture', desc: 'Gentle exfoliation for baby-soft softness', icon: Zap },
  { id: 'calm', label: 'Calm & Soothe', desc: 'Reduce redness, reactivity & irritation', icon: Heart }
]

function isGoalSelected(label) {
  return quizStore.answers.goals?.includes(label)
}

function toggleGoal(label) {
  quizStore.toggleMultiSelect('goals', label)
}

// ================= QUESTION 2: SKIN TYPE =================
const skinTypeOptions = [
  {
    id: 'Normal',
    name: 'Normal',
    desc: 'Balanced, not too oily and not too dry.',
    image: '/images/texture-normal.jpg'
  },
  {
    id: 'Oily',
    name: 'Oily',
    desc: 'Shiny, especially in the T-zone, prone to breakouts.',
    image: '/images/texture-oily.jpg'
  },
  {
    id: 'Dry',
    name: 'Dry',
    desc: 'Feels tight, may be flaky or rough.',
    image: '/images/texture-dry.jpg'
  },
  {
    id: 'Combination',
    name: 'Combination',
    desc: 'Oily in some areas (like T-zone), dry in others.',
    image: '/images/texture-combination.jpg'
  },
  {
    id: 'Sensitive',
    name: 'Sensitive',
    desc: 'Easily irritated, prone to redness or reactions.',
    image: '/images/texture-sensitive.jpg'
  }
]

const selectedSkinType = computed(() => quizStore.answers.skinType || 'Combination')

function selectSkinType(id) {
  quizStore.setAnswer('skinType', id)
}

// ================= QUESTION 3: CONCERNS =================
const concernOptions = [
  { id: 'pores', label: 'Enlarged Pores', desc: 'Visible congestion around nose & cheeks', icon: Sparkles },
  { id: 'breakouts', label: 'Occasional Breakouts', desc: 'Hormonal, stress or mask-related blemishes', icon: Flame },
  { id: 'tone', label: 'Uneven Skin Tone', desc: 'Post-acne marks & mild sun spots', icon: Sun },
  { id: 'dryness', label: 'Dryness & Flaking', desc: 'Rough patches or seasonal tightness', icon: Droplets },
  { id: 'redness', label: 'Redness & Sensitivity', desc: 'Flushing from weather or active ingredients', icon: ShieldAlert },
  { id: 'dullness', label: 'Dullness & Fatigue', desc: 'Tired-looking complexion needing a boost', icon: Zap }
]

function isConcernSelected(label) {
  return quizStore.answers.concerns?.includes(label)
}

function toggleConcern(label) {
  quizStore.toggleMultiSelect('concerns', label)
}

// ================= QUESTION 4: LIFESTYLE =================
const lifestyleOptions = [
  { id: 'indoors', label: 'Mostly Indoors', desc: 'Air conditioning or dry indoor heating', icon: Building },
  { id: 'sun', label: 'Moderate Sun Exposure', desc: 'Commuting, weekend outdoor activities', icon: CloudSun },
  { id: 'busy', label: 'Busy Schedule / High Stress', desc: 'Short nights and on-the-go lifestyle', icon: Clock },
  { id: 'balanced', label: 'Consistent Sleep & Wellness', desc: '7+ hours of sleep, regular hydration', icon: Moon }
]

function isLifestyleSelected(label) {
  return quizStore.answers.lifestyle?.includes(label)
}

function toggleLifestyle(label) {
  quizStore.toggleMultiSelect('lifestyle', label)
}

// ================= QUESTION 5: ENVIRONMENT =================
const environmentOptions = [
  { id: 'urban', label: 'Urban Area', desc: 'City smog, particulate dust and traffic', icon: Building },
  { id: 'humid', label: 'Warm & Humid Climate', desc: 'Tropical or sub-tropical ambient air', icon: Droplets },
  { id: 'dry', label: 'Cold & Dry Climate', desc: 'Winter chills and low indoor humidity', icon: CloudSun },
  { id: 'pollution', label: 'Some Pollution Exposure', desc: 'Frequent outdoor city commutes', icon: ShieldCheck }
]

function isEnvSelected(label) {
  return quizStore.answers.environment?.includes(label)
}

function toggleEnv(label) {
  quizStore.toggleMultiSelect('environment', label)
}

// ================= QUESTION 6: PREFERENCES =================
const preferenceOptions = [
  { id: 'fragrance_free', label: 'Fragrance-Free', desc: 'No synthetic or essential oil aromas', icon: Droplets },
  { id: 'cruelty_free', label: 'Cruelty-Free & Vegan', desc: 'Ethically verified botanical formulas', icon: Sprout },
  { id: 'clean', label: 'Clean Formulations', desc: 'Free from parabens, sulfates & drying alcohols', icon: Leaf },
  { id: 'dermatologist', label: 'Dermatologist Tested', desc: 'Hypoallergenic & clinically evaluated', icon: ShieldCheck }
]

function isPrefSelected(label) {
  return quizStore.answers.preferences?.includes(label)
}

function togglePref(label) {
  quizStore.toggleMultiSelect('preferences', label)
}

// ================= QUESTION 7: ROUTINE DEPTH =================
const routineDepthOptions = [
  { id: 'minimal', label: 'Minimal (2 Steps)', desc: 'Cleanser and moisturizer only', icon: Droplets },
  { id: 'standard', label: 'Essential (3-4 Steps)', desc: 'Cleanser, toner, serum, and moisturizer', icon: Sparkles },
  { id: 'advanced', label: 'Complete (5 Steps)', desc: 'Cleanse, tone, treat, moisturize & protect', icon: Zap }
]

const selectedRoutineDepth = computed({
  get: () => quizStore.answers.routineLevel || 'Essential (3-4 Steps)',
  set: (val) => quizStore.setAnswer('routineLevel', val)
})

// ================= WHY WE ASK TEXT =================
const currentWhyText = computed(() => {
  if (currentStep.value === 1) return 'Understanding your primary goals helps prioritize active ingredients like Niacinamide or Hyaluronic Acid.'
  if (currentStep.value === 2) return 'Your skin type helps us recommend products and ingredients that work best for your unique barrier balance.'
  if (currentStep.value === 3) return 'Specifying concerns allows our algorithm to choose proven targeted treatments that don\'t cause irritation.'
  if (currentStep.value === 4) return 'Daily stress, screen time and sun habits impact barrier recovery and antioxidant needs.'
  if (currentStep.value === 5) return 'Humidity and urban pollution alter how quickly your skin loses moisture throughout the day.'
  if (currentStep.value === 6) return 'We honor your clean beauty and sensitivity preferences so you love every texture.'
  if (currentStep.value === 7) return 'The best routine is the one you actually stick to every morning and evening.'
  return 'Synthesizing your responses to build your custom ritual.'
})

// ================= NAVIGATION =================
function nextStep() {
  if (currentStep.value < totalSteps) {
    currentStep.value++
    window.scrollTo({ top: 120, behavior: 'smooth' })
  } else {
    finalizeAndNavigate()
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 120, behavior: 'smooth' })
  } else {
    router.push('/quiz')
  }
}

function finalizeAndNavigate() {
  quizStore.completeQuiz()
  router.push('/quiz/results')
}
</script>

<style scoped>
.lumea-quiz-questions-view {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding: 40px 0 80px;
  color: #242721;
}

.container {
  max-width: 1240px;
  margin: 0 auto;
  padding: 0 24px;
}

.quiz-layout-container {
  display: grid;
  grid-template-columns: 280px 1fr 280px;
  gap: 32px;
  align-items: start;
}

/* ================= 1. LEFT EDITORIAL ================= */
.quiz-left-editorial {
  position: sticky;
  top: 100px;
}

.editorial-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 28px 24px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.editorial-eyebrow {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #8C7B70;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.editorial-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 600;
  line-height: 1.25;
  color: #1A1D1A;
  margin-bottom: 16px;
}

.text-terracotta {
  color: #9E3332;
  font-style: italic;
}

.editorial-divider {
  width: 32px;
  height: 2px;
  background-color: #9E3332;
  margin-bottom: 16px;
}

.editorial-desc {
  font-size: 13.5px;
  line-height: 1.55;
  color: #6C665D;
  margin-bottom: 24px;
}

.editorial-image-box {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #EAE1D7;
}

.editorial-img {
  width: 100%;
  height: 260px;
  object-fit: cover;
  display: block;
}

/* ================= 2. MAIN QUESTIONNAIRE STAGE ================= */
.quiz-main-stage {
  min-width: 0;
}

.stage-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.btn-text-nav {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: none;
  font-size: 13.5px;
  font-weight: 600;
  color: #5C5852;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-text-nav:hover:not(:disabled) {
  color: #1A1D1A;
  background-color: #EFE8E1;
}

.btn-text-nav:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.skip-btn {
  color: #9E3332;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.top-progress-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 240px;
}

.progress-bar-track {
  width: 100%;
  height: 6px;
  background-color: #EAE1D7;
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #9E3332;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.step-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #7A7269;
}

/* Surface Card */
.question-surface-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 24px;
  padding: 36px 32px;
  box-shadow: 0 6px 24px rgba(36, 39, 33, 0.05);
}

.question-category-tag {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #8C7B70;
  margin-bottom: 10px;
  text-transform: uppercase;
}

.question-main-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 8px;
}

.question-subtitle {
  font-size: 14.5px;
  color: #6C665D;
  margin-bottom: 30px;
}

/* ================= STEP 2: SKIN TYPES (VISUAL TEXTURES) ================= */
.skin-types-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.skin-type-card {
  background: #FAF8F5;
  border: 1.5px solid #EFE6DD;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.22s ease;
}

.skin-type-card:hover {
  transform: translateY(-2px);
  border-color: #D3C4B6;
  box-shadow: 0 6px 18px rgba(36, 39, 33, 0.06);
}

.skin-type-card.is-selected {
  border-color: #9E3332;
  background-color: #FDF9F7;
  box-shadow: 0 0 0 1px #9E3332, 0 8px 24px rgba(158, 51, 50, 0.12);
}

.type-texture-wrapper {
  position: relative;
  width: 100%;
  height: 120px;
  overflow: hidden;
  background-color: #EFE8E1;
}

.type-texture-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.skin-type-card:hover .type-texture-img {
  transform: scale(1.04);
}

.type-selected-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background-color: #9E3332;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.type-card-body {
  padding: 14px 14px 16px;
}

.type-name {
  font-family: 'Playfair Display', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 4px;
}

.type-desc {
  font-size: 12px;
  line-height: 1.45;
  color: #6C665D;
}

/* ================= CHIP & ROW OPTION CARDS ================= */
.options-grid-chips {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-bottom: 36px;
}

.option-chip-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: #FAF8F5;
  border: 1.5px solid #EFE6DD;
  border-radius: 14px;
  padding: 18px 16px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.option-chip-card:hover {
  border-color: #D3C4B6;
  background: #F5EFEA;
}

.option-chip-card.is-selected {
  border-color: #9E3332;
  background: #FDF9F7;
  box-shadow: 0 0 0 1px #9E3332;
}

.chip-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #EFE5DD;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  flex-shrink: 0;
}

.option-chip-card.is-selected .chip-icon-box {
  background: #9E3332;
  color: #FFFFFF;
}

.chip-info {
  flex: 1;
}

.chip-title {
  font-size: 14.5px;
  font-weight: 600;
  color: #242721;
  margin-bottom: 4px;
}

.chip-desc {
  font-size: 12px;
  line-height: 1.4;
  color: #7A7269;
}

.chip-check {
  color: #9E3332;
  flex-shrink: 0;
}

/* Rows layout for lifestyle / environment / routine */
.options-list-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 36px;
}

.option-row-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #FAF8F5;
  border: 1.5px solid #EFE6DD;
  border-radius: 14px;
  padding: 18px 20px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-row-card:hover {
  border-color: #D3C4B6;
  background: #F5EFEA;
}

.option-row-card.is-selected {
  border-color: #9E3332;
  background: #FDF9F7;
  box-shadow: 0 0 0 1px #9E3332;
}

.row-icon-box {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #EFE5DD;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  flex-shrink: 0;
}

.option-row-card.is-selected .row-icon-box {
  background: #9E3332;
  color: #FFFFFF;
}

.row-info {
  flex: 1;
}

.row-title {
  font-size: 15px;
  font-weight: 600;
  color: #242721;
  margin-bottom: 2px;
}

.row-desc {
  font-size: 12.5px;
  color: #7A7269;
}

.row-check {
  color: #9E3332;
}

/* Step 8: Analyzing animation */
.analyzing-step-content {
  text-align: center;
  padding: 40px 20px;
}

.analyzing-loader-box {
  display: flex;
  justify-content: center;
  margin-bottom: 28px;
}

.pulsing-emblem-ring {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: #F9EFE9;
  border: 2px solid #F0DFD3;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  animation: pulseRing 2s infinite ease-in-out;
}

@keyframes pulseRing {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(158, 51, 50, 0.4); }
  70% { transform: scale(1.05); box-shadow: 0 0 0 16px rgba(158, 51, 50, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(158, 51, 50, 0); }
}

.analyzing-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  font-weight: 600;
  color: #1A1D1A;
  margin-bottom: 10px;
}

.analyzing-subtitle {
  font-size: 15px;
  color: #6C665D;
  margin-bottom: 34px;
}

.analyzing-checklist {
  display: inline-flex;
  flex-direction: column;
  gap: 14px;
  text-align: left;
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  padding: 24px 30px;
  border-radius: 16px;
  margin-bottom: 38px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #38342F;
}

.check-icon-done {
  color: #9E3332;
}

.btn-view-results {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background-color: #9E3332;
  color: #FFFFFF;
  padding: 16px 40px;
  border-radius: 999px;
  font-size: 15.5px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(158, 51, 50, 0.28);
  transition: all 0.25s ease;
}

.btn-view-results:hover {
  background-color: #832726;
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(158, 51, 50, 0.38);
}

/* Card Footer Actions */
.card-footer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 24px;
  border-top: 1px solid #EFE8E1;
}

.btn-outline-prev {
  padding: 12px 28px;
  border-radius: 999px;
  background: transparent;
  border: 1.5px solid #D4C9BF;
  font-size: 14px;
  font-weight: 600;
  color: #4A453F;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-outline-prev:hover:not(:disabled) {
  border-color: #9E3332;
  color: #9E3332;
}

.btn-outline-prev:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-terracotta-next {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 34px;
  border-radius: 999px;
  background-color: #9E3332;
  border: none;
  color: #FFFFFF;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(158, 51, 50, 0.2);
  transition: all 0.22s ease;
}

.btn-terracotta-next:hover {
  background-color: #832726;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(158, 51, 50, 0.3);
}

/* ================= 3. RIGHT SIDEBAR ================= */
.quiz-right-sidebar {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-progress-card {
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(36, 39, 33, 0.04);
}

.progress-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.progress-title {
  font-size: 14.5px;
  font-weight: 700;
  color: #242721;
}

.progress-counter {
  font-size: 12.5px;
  font-weight: 600;
  color: #8C7B70;
}

.progress-mini-bar {
  width: 100%;
  height: 5px;
  background-color: #EAE1D7;
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 20px;
}

.mini-bar-fill {
  height: 100%;
  background-color: #9E3332;
  border-radius: 999px;
  transition: width 0.3s ease;
}

.step-checklist {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-check-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12.5px;
  font-weight: 500;
  color: #7A7269;
  transition: all 0.2s ease;
}

.step-bullet {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid #D6CBC1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10.5px;
  font-weight: 700;
  flex-shrink: 0;
  color: #7A7269;
}

.step-check-item.is-completed {
  color: #38342F;
}

.step-check-item.is-completed .step-bullet {
  background-color: #9E3332;
  border-color: #9E3332;
  color: #FFFFFF;
}

.step-check-item.is-active {
  background-color: #F8EFE9;
  color: #9E3332;
  font-weight: 700;
}

.step-check-item.is-active .step-bullet {
  background-color: #9E3332;
  border-color: #9E3332;
  color: #FFFFFF;
}

/* Why We Ask Card */
.sidebar-why-card {
  background: #FDF8F4;
  border: 1px solid #EFE0D5;
  border-radius: 20px;
  padding: 24px;
}

.why-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #F4E8DF;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9E3332;
  margin-bottom: 14px;
}

.why-title {
  font-family: 'Playfair Display', serif;
  font-size: 17px;
  font-weight: 600;
  color: #9E3332;
  margin-bottom: 8px;
}

.why-text {
  font-size: 12.5px;
  line-height: 1.55;
  color: #6C665D;
  margin-bottom: 16px;
}

.why-footer-quote {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  font-weight: 600;
  color: #9E3332;
  border-top: 1px solid #EFE0D5;
  padding-top: 12px;
}

/* Responsive */
@media (max-width: 1080px) {
  .quiz-layout-container {
    grid-template-columns: 1fr 280px;
  }
  .quiz-left-editorial {
    display: none;
  }
}

@media (max-width: 768px) {
  .quiz-layout-container {
    grid-template-columns: 1fr;
  }
  .quiz-right-sidebar {
    display: none;
  }
  .skin-types-grid {
    grid-template-columns: 1fr;
  }
  .options-grid-chips {
    grid-template-columns: 1fr;
  }
}
</style>
