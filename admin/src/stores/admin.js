import apiClient from '@/api/client'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAdminStore = defineStore('admin', () => {
  // Stats
  const stats = ref({
    metrics: {
      total_revenue: 3721.7,
      total_orders: 5,
      total_products: 8,
      total_customers: 3,
      low_stock_count: 2,
      average_order_value: 744.34,
    },
    orders_by_status: {
      delivered: 1,
      shipped: 1,
      processing: 1,
      confirmed: 2,
    },
    timeline: [],
    categories: [],
    recent_orders: [],
  })
  const statsLoading = ref(false)

  // Orders
  const orders = ref([])
  const ordersMeta = ref({ current_page: 1, last_page: 1, total: 0 })
  const ordersLoading = ref(false)

  // Products
  const products = ref([])
  const productsMeta = ref({ current_page: 1, last_page: 1, total: 0 })
  const productsLoading = ref(false)

  // Categories
  const categories = ref([])
  const categoriesLoading = ref(false)

  // Brands
  const brands = ref([])
  const brandsLoading = ref(false)

  // Customers
  const customers = ref([])
  const customersLoading = ref(false)

  // Reviews
  const reviews = ref([])
  const reviewsKpis = ref({
    total_reviews: 1248,
    average_rating: 4.6,
    approved: 892,
    pending_approval: 156,
    rejected_hidden: 32
  })
  const reviewsBreakdown = ref({
    5: { count: 848, percentage: 68 },
    4: { count: 250, percentage: 20 },
    3: { count: 100, percentage: 8 },
    2: { count: 37, percentage: 3 },
    1: { count: 13, percentage: 1 }
  })
  const reviewsRecent = ref([])
  const reviewsMeta = ref({ total: 1248, page: 1, limit: 10, total_pages: 125 })
  const reviewsLoading = ref(false)

  // Quizzes
  const quizzes = ref([])
  const quizzesLoading = ref(false)
  const quizzesKpis = ref({
    total_quizzes: 4,
    total_completions: 12456,
    completion_rate: '68.4%',
    satisfaction: 4.7
  })

  // System status
  const backendConnected = ref(true)
  let offlineWarningShown = false

  function notifyOffline(customMsg) {
    if (!offlineWarningShown) {
      offlineWarningShown = true
      addToast(customMsg || 'Backend connection error. Operating with cached data.', 'warning', 6000)
      setTimeout(() => {
        offlineWarningShown = false
      }, 20000)
    }
  }

  // Toast notifications with memory leak prevention
  const toasts = ref([])
  const toastTimeouts = new Map()

  function addToast(message, type = 'success', duration = 4000) {
    const id = Date.now() + Math.random()
    toasts.value.push({ id, message, type })
    if (duration > 0) {
      const timeoutId = setTimeout(() => {
        removeToast(id)
      }, duration)
      toastTimeouts.set(id, timeoutId)
    }
    return id
  }

  function removeToast(id) {
    if (toastTimeouts.has(id)) {
      clearTimeout(toastTimeouts.get(id))
      toastTimeouts.delete(id)
    }
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  function clearAllToasts() {
    toastTimeouts.forEach((timeoutId) => clearTimeout(timeoutId))
    toastTimeouts.clear()
    toasts.value = []
  }

  // --- ACTIONS ---

  async function fetchStats() {
    statsLoading.value = true
    try {
      const res = await apiClient.get('/admin/stats')
      if (res.data?.status === 'success') {
        stats.value = res.data.data
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch stats, using cached/demo data:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached stats.')
    } finally {
      statsLoading.value = false
    }
  }

  async function fetchOrders(params = {}) {
    ordersLoading.value = true
    try {
      const res = await apiClient.get('/admin/orders', { params })
      if (res.data?.status === 'success') {
        orders.value = res.data.data
        if (res.data.meta) ordersMeta.value = res.data.meta
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch orders:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached orders.')
    } finally {
      ordersLoading.value = false
    }
  }

  async function updateOrderStatus(orderId, status) {
    try {
      const res = await apiClient.patch(`/admin/orders/${orderId}/status`, { status })
      if (res.data?.status === 'success') {
        // Update local state
        const idx = orders.value.findIndex((o) => o.id === orderId)
        if (idx !== -1) {
          orders.value[idx].status = status
        }
        addToast(`Order #${res.data.data.order_number} status updated to ${status}`, 'success')
        fetchStats() // refresh overview numbers
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to update order status'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function fetchProducts(params = {}) {
    productsLoading.value = true
    try {
      const res = await apiClient.get('/products', { params })
      if (res.data?.status === 'success') {
        products.value = res.data.data
        if (res.data.meta) productsMeta.value = res.data.meta
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch products:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached products.')
    } finally {
      productsLoading.value = false
    }
  }

  async function createProduct(payload) {
    try {
      const res = await apiClient.post('/admin/products', payload)
      if (res.data?.status === 'success') {
        addToast(`Product "${res.data.data.name}" created successfully`, 'success')
        await fetchProducts()
        await fetchStats()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to create product'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function updateProduct(id, payload) {
    try {
      const res = await apiClient.put(`/admin/products/${id}`, payload)
      if (res.data?.status === 'success') {
        addToast(`Product updated successfully`, 'success')
        await fetchProducts()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to update product'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function deleteProduct(id) {
    try {
      const res = await apiClient.delete(`/admin/products/${id}`)
      if (res.data?.status === 'success') {
        addToast('Product deleted from catalog', 'success')
        products.value = products.value.filter((p) => p.id !== id)
        await fetchStats()
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to delete product'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function fetchCategories() {
    categoriesLoading.value = true
    try {
      const res = await apiClient.get('/categories')
      if (res.data?.status === 'success') {
        categories.value = res.data.data
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch categories:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached categories.')
    } finally {
      categoriesLoading.value = false
    }
  }

  async function createCategory(payload) {
    try {
      const res = await apiClient.post('/admin/categories', payload)
      if (res.data?.status === 'success') {
        addToast(`Category "${res.data.data.name}" created`, 'success')
        await fetchCategories()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to create category'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function updateCategory(id, payload) {
    try {
      const res = await apiClient.put(`/admin/categories/${id}`, payload)
      if (res.data?.status === 'success') {
        addToast(`Category updated successfully`, 'success')
        await fetchCategories()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to update category'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function deleteCategory(id) {
    try {
      const res = await apiClient.delete(`/admin/categories/${id}`)
      if (res.data?.status === 'success') {
        addToast('Category deleted', 'success')
        categories.value = categories.value.filter((c) => c.id !== id)
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to delete category'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function fetchCustomers() {
    customersLoading.value = true
    try {
      const res = await apiClient.get('/admin/customers')
      if (res.data?.status === 'success') {
        customers.value = res.data.data
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch customers:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached customers.')
    } finally {
      customersLoading.value = false
    }
  }

  async function fetchBrands() {
    brandsLoading.value = true
    try {
      const res = await apiClient.get('/admin/brands')
      if (res.data?.status === 'success') {
        brands.value = res.data.data
        backendConnected.value = true
      }
    } catch (err) {
      console.warn('Could not fetch brands:', err)
      backendConnected.value = false
      notifyOffline('Backend unavailable. Showing atelier cached brands.')
    } finally {
      brandsLoading.value = false
    }
  }

  async function createBrand(payload) {
    try {
      const res = await apiClient.post('/admin/brands', payload)
      if (res.data?.status === 'success') {
        addToast(`Brand "${res.data.data.name}" created`, 'success')
        await fetchBrands()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to create brand'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function updateBrand(id, payload) {
    try {
      const res = await apiClient.put(`/admin/brands/${id}`, payload)
      if (res.data?.status === 'success') {
        addToast(`Brand updated successfully`, 'success')
        await fetchBrands()
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to update brand'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function toggleBrandFeatured(id) {
    try {
      const res = await apiClient.patch(`/admin/brands/${id}/featured`)
      if (res.data?.status === 'success') {
        const b = brands.value.find(item => item.id === id)
        if (b) b.is_featured = res.data.data.is_featured
        addToast(res.data.message, 'success')
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to toggle featured brand'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function deleteBrand(id) {
    try {
      const res = await apiClient.delete(`/admin/brands/${id}`)
      if (res.data?.status === 'success') {
        addToast('Brand deleted', 'success')
        brands.value = brands.value.filter(b => b.id !== id)
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to delete brand'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  // Reviews actions
  async function fetchReviews(params = {}) {
    reviewsLoading.value = true
    try {
      const res = await apiClient.get('/admin/reviews', { params })
      if (res.data?.status === 'success') {
        reviews.value = res.data.data
        if (res.data.kpis) reviewsKpis.value = res.data.kpis
        if (res.data.rating_breakdown) reviewsBreakdown.value = res.data.rating_breakdown
        if (res.data.recent_reviews) reviewsRecent.value = res.data.recent_reviews
        if (res.data.pagination) reviewsMeta.value = res.data.pagination
        return { success: true, data: res.data }
      }
      return { success: false }
    } catch (err) {
      console.error('Failed to fetch reviews:', err)
      return { success: false }
    } finally {
      reviewsLoading.value = false
    }
  }

  async function updateReviewStatus(reviewId, status) {
    try {
      const res = await apiClient.patch(`/admin/reviews/${reviewId}/status`, { status })
      if (res.data?.status === 'success') {
        addToast(`Review #${reviewId} marked as ${status}`, 'success')
        const idx = reviews.value.findIndex(r => r.id === reviewId)
        if (idx !== -1) {
          reviews.value[idx].status = status
        }
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to update review status'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function replyToReview(reviewId, adminReply) {
    try {
      const res = await apiClient.post(`/admin/reviews/${reviewId}/reply`, { admin_reply: adminReply })
      if (res.data?.status === 'success') {
        addToast('Atelier reply saved successfully', 'success')
        const idx = reviews.value.findIndex(r => r.id === reviewId)
        if (idx !== -1) {
          reviews.value[idx].admin_reply = adminReply
        }
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to reply to review'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function deleteReview(reviewId) {
    try {
      const res = await apiClient.delete(`/admin/reviews/${reviewId}`)
      if (res.data?.status === 'success') {
        addToast('Review deleted successfully', 'success')
        reviews.value = reviews.value.filter(r => r.id !== reviewId)
        return { success: true }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to delete review'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  // Quizzes actions
  async function fetchQuizzes(params = {}) {
    quizzesLoading.value = true
    try {
      const res = await apiClient.get('/admin/quizzes', { params })
      if (res.data?.status === 'success') {
        quizzes.value = res.data.data
        if (res.data.kpis) quizzesKpis.value = res.data.kpis
        return { success: true, data: res.data }
      }
      return { success: false }
    } catch (err) {
      console.error('Failed to fetch quizzes:', err)
      return { success: false }
    } finally {
      quizzesLoading.value = false
    }
  }

  async function fetchQuiz(quizId) {
    try {
      const res = await apiClient.get(`/admin/quizzes/${quizId}`)
      if (res.data?.status === 'success') {
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      console.error(`Failed to fetch quiz #${quizId}:`, err)
      return { success: false }
    }
  }

  async function updateQuiz(quizId, payload) {
    try {
      const res = await apiClient.put(`/admin/quizzes/${quizId}`, payload)
      if (res.data?.status === 'success') {
        addToast('Quiz saved and synchronized to database', 'success')
        const idx = quizzes.value.findIndex(q => q.id === quizId)
        if (idx !== -1) {
          quizzes.value[idx] = res.data.data
        }
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to save quiz'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  async function toggleQuizStatus(quizId) {
    try {
      const res = await apiClient.patch(`/admin/quizzes/${quizId}/status`)
      if (res.data?.status === 'success') {
        addToast(`Quiz status changed to ${res.data.data.status}`, 'success')
        const idx = quizzes.value.findIndex(q => q.id === quizId)
        if (idx !== -1) {
          quizzes.value[idx].status = res.data.data.status
        }
        return { success: true, data: res.data.data }
      }
      return { success: false }
    } catch (err) {
      const msg = err.response?.data?.message || 'Failed to toggle quiz status'
      addToast(msg, 'error')
      return { success: false, message: msg }
    }
  }

  return {
    stats,
    statsLoading,
    orders,
    ordersMeta,
    ordersLoading,
    products,
    productsMeta,
    productsLoading,
    categories,
    categoriesLoading,
    brands,
    brandsLoading,
    customers,
    customersLoading,
    reviews,
    reviewsKpis,
    reviewsBreakdown,
    reviewsRecent,
    reviewsMeta,
    reviewsLoading,
    backendConnected,
    toasts,
    addToast,
    removeToast,
    clearAllToasts,
    fetchStats,
    fetchOrders,
    updateOrderStatus,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
    fetchBrands,
    createBrand,
    updateBrand,
    toggleBrandFeatured,
    deleteBrand,
    fetchCustomers,
    fetchReviews,
    updateReviewStatus,
    replyToReview,
    deleteReview,
    quizzes,
    quizzesKpis,
    quizzesLoading,
    fetchQuizzes,
    fetchQuiz,
    updateQuiz,
    toggleQuizStatus,
  }
})
