import { useAuthStore } from '@/stores/auth'
import CategoriesView from '@/views/CategoriesView.vue'
import CustomersView from '@/views/CustomersView.vue'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import OrdersView from '@/views/OrdersView.vue'
import ProductsView from '@/views/ProductsView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ReturnsView from '@/views/ReturnsView.vue'
import ArticlesView from '@/views/ArticlesView.vue'
import BannersView from '@/views/BannersView.vue'
import AnalyticsView from '@/views/AnalyticsView.vue'
import BrandsView from '@/views/BrandsView.vue'
import PromotionsView from '@/views/PromotionsView.vue'
import ReviewsView from '@/views/ReviewsView.vue'
import SkinQuizView from '@/views/SkinQuizView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true, title: 'Admin Login' },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true, title: 'Executive Overview' },
  },
  {
    path: '/products',
    name: 'products',
    component: ProductsView,
    meta: { requiresAuth: true, title: 'Product Atelier' },
  },
  {
    path: '/brands',
    name: 'brands',
    component: BrandsView,
    meta: { requiresAuth: true, title: 'Brands Management' },
  },
  {
    path: '/orders',
    name: 'orders',
    component: OrdersView,
    meta: { requiresAuth: true, title: 'Order Fulfillment' },
  },
  {
    path: '/returns',
    name: 'returns',
    component: ReturnsView,
    meta: { requiresAuth: true, title: 'Returns & Refunds' },
  },
  {
    path: '/articles',
    name: 'articles',
    component: ArticlesView,
    meta: { requiresAuth: true, title: 'Editorial Articles' },
  },
  {
    path: '/banners',
    name: 'banners',
    component: BannersView,
    meta: { requiresAuth: true, title: 'Banners CMS' },
  },
  {
    path: '/homepage',
    name: 'homepage',
    component: BannersView,
    meta: { requiresAuth: true, title: 'Homepage Management' },
  },
  {
    path: '/promotions',
    name: 'promotions',
    component: PromotionsView,
    meta: { requiresAuth: true, title: 'Promotions Management' },
  },
  {
    path: '/reviews',
    name: 'reviews',
    component: ReviewsView,
    meta: { requiresAuth: true, title: 'Reviews Management' },
  },
  {
    path: '/quiz',
    name: 'quiz',
    component: SkinQuizView,
    meta: { requiresAuth: true, title: 'Skin Quiz Diagnostic Atelier' },
  },
  {
    path: '/categories',
    name: 'categories',
    component: CategoriesView,
    meta: { requiresAuth: true, title: 'Collections' },
  },
  {
    path: '/customers',
    name: 'customers',
    component: CustomersView,
    meta: { requiresAuth: true, title: 'Clientele' },
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
    meta: { requiresAuth: true, title: 'Console Settings' },
  },
  {
    path: '/analytics',
    name: 'analytics',
    component: AnalyticsView,
    meta: { requiresAuth: true, title: 'Skincare Analytics' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.title) {
    document.title = `${to.meta.title} — LUMEA Atelier Admin`
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
