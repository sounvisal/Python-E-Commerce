import { privateStorageKey } from '@/utils/orderAccess'
import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { useProductStore } from './products'
import { buildRoutine } from '@/utils/recommendations'

export const useQuizStore = defineStore('quiz', () => {
  // Saved state from localStorage if available
  const savedProfile = localStorage.getItem(privateStorageKey('skin_profile'))
  let initialData = null
  try { initialData = savedProfile ? JSON.parse(savedProfile) : null } catch {}

  const activeQuiz = ref(null)
  const loading = ref(false)

  const productStore = useProductStore()
  const answers = ref(initialData?.answers || { goals: [], skinType: '', concerns: [], lifestyle: [], environment: [], preferences: [], routineLevel: '', currentRoutine: '' })
  const completed = ref(initialData?.completed ?? false)
  const lastUpdated = ref(initialData?.lastUpdated || '')

  // Skin type description lookup
  const skinTypeDescriptions = {
    'Normal': 'Balanced, not too oily and not too dry.',
    'Oily': 'Shiny, especially in the T-zone, prone to breakouts.',
    'Dry': 'Feels tight, may be flaky or rough.',
    'Combination': 'Oily in the T-zone, drier in other areas.',
    'Sensitive': 'Easily irritated, prone to redness or reactions.'
  }

  const currentSkinType = computed(() => answers.value.skinType || 'Combination')
  const currentSkinDesc = computed(() => skinTypeDescriptions[currentSkinType.value] || skinTypeDescriptions['Combination'])

  // Save to localStorage
  function persist() {
    localStorage.setItem(privateStorageKey('skin_profile'), JSON.stringify({
      answers: answers.value,
      completed: completed.value,
      lastUpdated: lastUpdated.value
    }))
  }

  function loadProfile() {
    let data = null
    try { data = JSON.parse(localStorage.getItem(privateStorageKey('skin_profile')) || 'null') } catch {}
    answers.value = data?.answers || { goals: [], skinType: '', concerns: [], lifestyle: [], environment: [], preferences: [], routineLevel: '', currentRoutine: '' }
    completed.value = data?.completed ?? false
    lastUpdated.value = data?.lastUpdated || ''
  }

  async function fetchActiveQuiz() {
    loading.value = true
    try {
      const res = await axios.get('/api/quizzes/active')
      if (res.data?.status === 'success') {
        activeQuiz.value = res.data.data
      }
    } catch (err) {
      console.warn('Could not load active quiz from backend, falling back to local diagnostic steps:', err)
    } finally {
      loading.value = false
    }
  }

  function setAnswer(questionKey, value) {
    answers.value[questionKey] = value
    persist()
  }

  function toggleMultiSelect(questionKey, item) {
    if (!Array.isArray(answers.value[questionKey])) {
      answers.value[questionKey] = []
    }
    const idx = answers.value[questionKey].indexOf(item)
    if (idx > -1) {
      answers.value[questionKey].splice(idx, 1)
    } else {
      answers.value[questionKey].push(item)
    }
    persist()
  }

  async function completeQuiz() {
    completed.value = true
    const now = new Date()
    lastUpdated.value = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    persist()

    // Record completion in SQLite backend
    try {
      const quizId = activeQuiz.value?.id || 1
      await axios.post(`/api/quizzes/${quizId}/complete`, {
        answers: answers.value,
        skin_type_result: currentSkinType.value,
        recommended_product_ids: recommendedRoutineProducts.value.map(p => p.id)
      })
    } catch (err) {
      // Graceful offline fallback
    }
  }

  function resetQuiz() {
    answers.value = {
      goals: [],
      skinType: '',
      concerns: [],
      lifestyle: [],
      environment: [],
      preferences: [],
      routineLevel: '',
      currentRoutine: ''
    }
    completed.value = false
    persist()
  }

  const recommendedRoutineProducts = computed(() => buildRoutine(productStore.allCatalogProducts, answers.value, false))
  const eveningRoutineProducts = computed(() => buildRoutine(productStore.allCatalogProducts, answers.value, true))

  return {
    loadProfile,
    answers,
    completed,
    lastUpdated,
    currentSkinType,
    currentSkinDesc,
    skinTypeDescriptions,
    recommendedRoutineProducts,
    eveningRoutineProducts,
    activeQuiz,
    loading,
    fetchActiveQuiz,
    setAnswer,
    toggleMultiSelect,
    completeQuiz,
    resetQuiz
  }
})
