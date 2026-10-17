import axios from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useQuizStore = defineStore('quiz', () => {
  // Saved state from localStorage if available
  const savedProfile = localStorage.getItem('lumea_skin_profile')
  const initialData = savedProfile ? JSON.parse(savedProfile) : null

  const activeQuiz = ref(null)
  const loading = ref(false)

  const answers = ref(initialData?.answers || {
    goals: ['Clearer Skin', 'Hydration', 'Brighter Tone'],
    skinType: 'Combination',
    concerns: ['Enlarged Pores', 'Uneven Skin Tone', 'Occasional Breakouts'],
    lifestyle: ['Mostly Indoors', 'Moderate Sun Exposure', 'Busy Schedule'],
    environment: ['Urban Area', 'Warm & Humid Climate', 'Some Pollution Exposure'],
    preferences: ['Fragrance-Free', 'Cruelty-Free'],
    routineLevel: '3-4 Products (Standard)',
    currentRoutine: 'Cleanser + Moisturizer'
  })

  const completed = ref(initialData?.completed || true)
  const lastUpdated = ref(initialData?.lastUpdated || 'Jun 19, 2025')

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
    localStorage.setItem('lumea_skin_profile', JSON.stringify({
      answers: answers.value,
      completed: completed.value,
      lastUpdated: lastUpdated.value
    }))
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
        recommended_product_ids: [204, 205, 202, 203, 208]
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

  // Recommended Products IDs for the current skin profile
  const recommendedRoutineProducts = computed(() => {
    // 1. Cleanse, 2. Tone, 3. Treat, 4. Moisturize, 5. Protect
    return [
      {
        step: 1,
        stepName: 'Cleanse',
        id: 204,
        name: 'CeraVe Foaming Facial Cleanser',
        brand: 'CeraVe',
        tagline: 'For normal to oily skin',
        price: 16.00,
        rating: 4.8,
        reviews: 1200,
        image_url: '/images/prod-cerave-cleanser.jpg',
        slug: 'cerave-foaming-facial-cleanser',
        badge: 'Step 1'
      },
      {
        step: 2,
        stepName: 'Tone',
        id: 205,
        name: 'Anua Heartleaf 77% Soothing Toner',
        brand: 'Anua',
        tagline: 'Calms and balances skin',
        price: 24.00,
        rating: 4.9,
        reviews: 892,
        image_url: '/images/prod-anua-toner.jpg',
        slug: 'anua-heartleaf-77-soothing-toner',
        badge: 'Step 2'
      },
      {
        step: 3,
        stepName: 'Treat',
        id: 202,
        name: 'Niacinamide 10% + Zinc 1%',
        brand: 'The Ordinary',
        tagline: 'Minimizes pores & controls oil',
        price: 17.80,
        rating: 4.7,
        reviews: 2400,
        image_url: '/images/prod-ordinary.jpg',
        slug: 'the-ordinary-niacinamide-10-zinc-1',
        badge: 'Step 3'
      },
      {
        step: 4,
        stepName: 'Moisturize',
        id: 203,
        name: 'Water Bank Moisture Cream',
        brand: 'Laneige',
        tagline: 'Balances hydration',
        price: 32.00,
        rating: 4.8,
        reviews: 987,
        image_url: '/images/prod-laneige.jpg',
        slug: 'laneige-water-bank-moisture-cream',
        badge: 'Step 4'
      },
      {
        step: 5,
        stepName: 'Protect',
        id: 208,
        name: 'Anthelios Ultra Light Fluid SPF 50+',
        brand: 'La Roche-Posay',
        tagline: 'Broad spectrum UV protection',
        price: 29.50,
        rating: 4.9,
        reviews: 1800,
        image_url: '/images/prod-laroche-effaclar.jpg',
        slug: 'la-roche-posay-anthelios-spf-50',
        badge: 'Step 5'
      }
    ]
  })

  const eveningRoutineProducts = computed(() => {
    // Evening skips Sunscreen, adds restorative repair treatment
    return [
      recommendedRoutineProducts.value[0], // Cleanse
      recommendedRoutineProducts.value[1], // Tone
      recommendedRoutineProducts.value[2], // Treat
      {
        step: 4,
        stepName: 'Night Repair',
        id: 206,
        name: 'Advanced Snail 92 All in One Cream',
        brand: 'COSRX',
        tagline: 'Deep barrier restoration',
        price: 25.00,
        rating: 4.8,
        reviews: 1450,
        image_url: '/images/prod-cosrx-snail.jpg',
        slug: 'cosrx-advanced-snail-92-cream',
        badge: 'Night Care'
      }
    ]
  })

  return {
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
