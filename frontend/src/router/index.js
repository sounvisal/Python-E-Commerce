import { createRouter, createWebHistory } from 'vue-router'
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

import AboutView from '@/views/about/AboutView.vue'
import AuthenticityView from '@/views/authenticity/AuthenticityView.vue'
import ContactView from '@/views/contact/ContactView.vue'
import FaqView from '@/views/faq/FaqView.vue'
import ShippingView from '@/views/shipping/ShippingView.vue'
import ReturnsView from '@/views/returns/ReturnsView.vue'

import SkinQuizIntroView from '@/views/quiz/SkinQuizIntroView.vue'
import SkinQuizQuestionsView from '@/views/quiz/SkinQuizQuestionsView.vue'
import QuizResultsView from '@/views/quiz/QuizResultsView.vue'
import RecommendedRoutineView from '@/views/quiz/RecommendedRoutineView.vue'
import SkinProfileView from '@/views/account/SkinProfileView.vue'
import SkincareJournalView from '@/views/account/SkincareJournalView.vue'
import LoginRegisterView from '@/views/auth/LoginRegisterView.vue'
import MyAccountView from '@/views/account/MyAccountView.vue'
import MyOrdersView from '@/views/account/MyOrdersView.vue'
import OrderDetailsView from '@/views/account/OrderDetailsView.vue'
import PrivacyPolicyView from '@/views/legal/PrivacyPolicyView.vue'
import TermsOfServiceView from '@/views/legal/TermsOfServiceView.vue'
import NotFoundView from '@/views/error/NotFoundView.vue'
import ArticlesView from '@/views/articles/ArticlesView.vue'
import ArticleDetailView from '@/views/articles/ArticleDetailView.vue'
import SustainabilityView from '@/views/sustainability/SustainabilityView.vue'
import ReturnRequestView from '@/views/returns/ReturnRequestView.vue'
import ReturnStatusView from '@/views/returns/ReturnStatusView.vue'

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
    component: ReturnRequestView,
  },
  {
    path: '/returns/status/:requestId',
    name: 'return-status',
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
    component: QuizResultsView,
  },
  {
    path: '/routine',
    name: 'recommended-routine',
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
  },
  {
    path: '/journal',
    redirect: '/account/journal',
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
  },
  {
    path: '/account/overview',
    redirect: '/account',
  },
  {
    path: '/account/orders',
    name: 'my-orders',
    component: MyOrdersView,
  },
  {
    path: '/account/orders/:orderNumber',
    name: 'order-details',
    component: OrderDetailsView,
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

export default router
