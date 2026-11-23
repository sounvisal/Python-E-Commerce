import { createRouter, createWebHistory } from 'vue-router'
import { privateStorageKey } from '@/utils/orderAccess'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useAtelierNotificationStore } from '@/stores/atelierNotifications'
import HomeView from '@/views/home/HomeView.vue'
import ShopView from '@/views/shop/ShopView.vue'
import CategoryView from '@/views/category/CategoryView.vue'
import BrandListingView from '@/views/brands/BrandListingView.vue'
import BrandStoreView from '@/views/brands/BrandStoreView.vue'
import ProductDetailView from '@/views/product/ProductDetailView.vue'
import SearchView from '@/views/search/SearchView.vue'
import CartView from '@/views/cart/CartView.vue'
import CheckoutView from '@/views/checkout/CheckoutView.vue'
import OrderSuccessView from '@/views/checkout/OrderSuccessView.vue'

import BestSellersView from '@/views/best-sellers/BestSellersView.vue'
import NewArrivalsView from '@/views/new-arrivals/NewArrivalsView.vue'
import DealsView from '@/views/deals/DealsView.vue'
import AllDealsView from '@/views/deals/AllDealsView.vue'
import ConcernsView from '@/views/concerns/ConcernsView.vue'
import WishlistView from '@/views/wishlist/WishlistView.vue'

// Lazy-loaded secondary views
const AboutView = () => import('@/views/about/AboutView.vue')
const AuthenticityView = () => import('@/views/authenticity/AuthenticityView.vue')
const ContactView = () => import('@/views/contact/ContactView.vue')
const FaqView = () => import('@/views/faq/FaqView.vue')
const ShippingView = () => import('@/views/shipping/ShippingView.vue')
const ReturnsView = () => import('@/views/returns/ReturnsView.vue')

const SkinQuizIntroView = () => import('@/views/quiz/SkinQuizIntroView.vue')
const SkinQuizQuestionsView = () => import('@/views/quiz/SkinQuizQuestionsView.vue')
const QuizResultsView = () => import('@/views/quiz/QuizResultsView.vue')
const RecommendedRoutineView = () => import('@/views/quiz/RecommendedRoutineView.vue')
const SkinProfileView = () => import('@/views/account/SkinProfileView.vue')
const SkincareJournalView = () => import('@/views/account/SkincareJournalView.vue')
const LoginRegisterView = () => import('@/views/auth/LoginRegisterView.vue')
const MyAccountView = () => import('@/views/account/MyAccountView.vue')
const MyOrdersView = () => import('@/views/account/MyOrdersView.vue')
const OrderDetailsView = () => import('@/views/account/OrderDetailsView.vue')
const PrivacyPolicyView = () => import('@/views/legal/PrivacyPolicyView.vue')
const TermsOfServiceView = () => import('@/views/legal/TermsOfServiceView.vue')
const NotFoundView = () => import('@/views/error/NotFoundView.vue')
const ArticlesView = () => import('@/views/articles/ArticlesView.vue')
const ArticleDetailView = () => import('@/views/articles/ArticleDetailView.vue')
const SustainabilityView = () => import('@/views/sustainability/SustainabilityView.vue')
const ReturnRequestView = () => import('@/views/returns/ReturnRequestView.vue')
const ReturnStatusView = () => import('@/views/returns/ReturnStatusView.vue')
const ReviewsView = () => import('@/views/reviews/ReviewsView.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/shop',
    name: 'shop',
    component: ShopView,
  },
  {
    path: '/best-sellers',
    name: 'best-sellers',
    component: BestSellersView,
  },
  {
    path: '/new-arrivals',
    name: 'new-arrivals',
    component: NewArrivalsView,
  },
  {
    path: '/deals',
    name: 'deals',
    component: DealsView,
  },
  {
    path: '/deals/all',
    name: 'all-deals',
    component: AllDealsView,
  },
  {
    path: '/all-deals',
    redirect: '/deals/all',
  },
  {
    path: '/concerns',
    name: 'concerns',
    component: ConcernsView,
  },
  {
    path: '/wishlist',
    name: 'wishlist',
    component: WishlistView,
  },
  {
    path: '/category/:slug',
    name: 'category',
    component: CategoryView,
  },
  {
    path: '/brands',
    name: 'brands',
    component: BrandListingView,
  },
  {
    path: '/brand/:slug',
    name: 'brand-store',
    component: BrandStoreView,
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView,
  },
  {
    path: '/product/:slug',
    name: 'product-detail',
    component: ProductDetailView,
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartView,
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: CheckoutView,
    meta: { requiresAuth: true },
  },
  {
    path: '/order-success/:orderNumber',
    name: 'order-success',
    component: OrderSuccessView,
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
  },
  {
    path: '/our-story',
    redirect: '/about',
  },
  {
    path: '/authenticity',
    name: 'authenticity',
    component: AuthenticityView,
  },
  {
    path: '/why-shop-with-us',
    redirect: '/authenticity',
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView,
  },
  {
    path: '/faq',
    name: 'faq',
    component: FaqView,
  },
  {
    path: '/shipping',
    name: 'shipping',
    component: ShippingView,
  },
  {
    path: '/returns',
    name: 'returns',
    component: ReturnsView,
  },
  {
    path: '/returns/request',
    name: 'return-request',
    meta: { requiresAuth: true },
    component: ReturnRequestView,
  },
  {
    path: '/returns/status/:requestId',
    name: 'return-status',
    meta: { requiresAuth: true },
    component: ReturnStatusView,
  },
  {
    path: '/account/returns/:requestId',
    redirect: to => `/returns/status/${to.params.requestId}`,
  },
  // Phase 3: Skin Quiz & Personalization Routes
  {
    path: '/quiz',
    name: 'skin-quiz-intro',
    component: SkinQuizIntroView,
  },
  {
    path: '/skin-quiz',
    redirect: '/quiz',
  },
  {
    path: '/quiz/questions',
    name: 'skin-quiz-questions',
    component: SkinQuizQuestionsView,
  },
  {
    path: '/quiz/results',
    name: 'quiz-results',
    meta: { requiresQuiz: true },
    component: QuizResultsView,
  },
  {
    path: '/routine',
    name: 'recommended-routine',
    meta: { requiresQuiz: true },
    component: RecommendedRoutineView,
  },
  {
    path: '/quiz/routine',
    redirect: '/routine',
  },
  {
    path: '/account/profile',
    name: 'skin-profile',
    component: SkinProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: '/skin-profile',
    redirect: '/account/profile',
  },
  {
    path: '/profile',
    redirect: '/account/profile',
  },
  {
    path: '/account/journal',
    name: 'skincare-journal',
    component: SkincareJournalView,
    meta: { requiresAuth: true },
  },
  {
    path: '/journal',
    redirect: '/articles',
  },
  // Phase 4: Customer Account, Auth & Orders Suite
  {
    path: '/login',
    name: 'login',
    component: LoginRegisterView,
  },
  {
    path: '/register',
    name: 'register',
    component: LoginRegisterView,
  },
  {
    path: '/auth',
    redirect: '/login',
  },
  {
    path: '/account',
    name: 'my-account',
    component: MyAccountView,
    meta: { requiresAuth: true },
  },
  {
    path: '/account/overview',
    redirect: '/account',
  },
  {
    path: '/account/orders',
    name: 'my-orders',
    component: MyOrdersView,
    meta: { requiresAuth: true },
  },
  { path: '/track/:orderNumber', name: 'guest-order-tracking', component: OrderDetailsView },
  {
    path: '/account/orders/:orderNumber',
    name: 'order-details',
    component: OrderDetailsView,
    meta: { requiresAuth: true },
  },
  {
    path: '/orders',
    redirect: '/account/orders',
  },
  {
    path: '/privacy-policy',
    name: 'privacy-policy',
    component: PrivacyPolicyView,
  },
  {
    path: '/privacy',
    redirect: '/privacy-policy',
  },
  {
    path: '/terms-of-service',
    name: 'terms-of-service',
    component: TermsOfServiceView,
  },
  {
    path: '/terms',
    redirect: '/terms-of-service',
  },
  {
    path: '/articles',
    name: 'articles',
    component: ArticlesView,
  },
  {
    path: '/articles/:slug',
    name: 'article-detail',
    component: ArticleDetailView,
  },
  {
    path: '/sustainability',
    name: 'sustainability',
    component: SustainabilityView,
  },
  {
    path: '/reviews',
    name: 'customer-reviews',
    component: ReviewsView,
  },
  {
    path: '/customer-reviews',
    redirect: '/reviews',
  },
  {
    path: '/community-reviews',
    redirect: '/reviews',
  },
  {
    path: '/404',
    name: 'not-found',
    component: NotFoundView,
  },
  {
    path: '/:pathMatch(.*)*',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresQuiz) {
    try {
      if (!JSON.parse(localStorage.getItem(privateStorageKey('skin_profile')) || 'null')?.completed) return next('/quiz')
    } catch { return next('/quiz') }
  }
  const auth = useAuthStore()
  const isAuthenticated = auth.token ? await auth.ensureSession() : false

  if (to.matched.some(record => record.meta?.requiresAuth)) {
    if (!isAuthenticated) {
      return next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
    }
  }
  next()
})

router.afterEach(() => {
  try {
    const cart = useCartStore()
    if (cart.isDrawerOpen) cart.closeDrawer()
    const notif = useAtelierNotificationStore()
    if (notif.isDrawerOpen) notif.closeDrawer()
  } catch {}
})

export default router
