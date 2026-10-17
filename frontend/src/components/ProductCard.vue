<template>
  <div
    class="product-card"
    :class="{ 'list-layout': viewMode === 'list' }"
  >
    <!-- Image Stage -->
    <div class="image-wrapper">
      <router-link :to="`/product/${product.slug}`" class="image-link">
        <img :src="product.image_url" :alt="product.name" class="product-img" loading="lazy" />
      </router-link>

      <!-- Wishlist Heart -->
      <button
        class="card-heart-btn"
        :class="{ 'is-active': isWishlisted }"
        @click.stop="toggleWishlist"
        :title="isWishlisted ? 'Remove from Wishlist' : 'Add to Wishlist'"
      >
        <Heart :size="16" :stroke-width="1.6" :fill="isWishlisted ? '#9E5D4E' : 'none'" />
      </button>

      <!-- Badges -->
      <div class="badge-stack">
        <span v-if="product.badge" class="badge" :class="badgeClass">
          {{ product.badge }}
        </span>
        <span v-else-if="hasDiscount" class="badge badge-sale">
          {{ discountPercent }}% OFF
        </span>
      </div>
    </div>

    <!-- Product Info Block -->
    <div class="product-info">
      <div class="brand-row">
        <span class="brand-name">{{ product.brand || product.category_name || 'Luméa' }}</span>
        <span v-if="viewMode === 'list' && product.subcategory" class="subcat-tag">
          {{ product.subcategory }}
        </span>
      </div>

      <h3 class="product-title">
        <router-link :to="`/product/${product.slug}`">
          {{ product.name }}
        </router-link>
      </h3>

      <p v-if="viewMode === 'list' && product.desc" class="list-desc">
        {{ product.desc }}
      </p>

      <div class="product-rating-row" v-if="product.rating">
        <span class="stars-wrap">
          <Star
            v-for="i in 5"
            :key="i"
            :size="11"
            class="star-icon"
            :class="{ filled: i <= Math.round(product.rating) }"
          />
        </span>
        <span class="score">{{ Number(product.rating).toFixed(1) }}</span>
        <span class="reviews-count" v-if="product.reviews">
          ({{ formatReviews(product.reviews) }})
        </span>
      </div>

      <div class="price-action-group">
        <div class="price-row">
          <span class="current-price">${{ Number(product.price).toFixed(2) }}</span>
          <span v-if="product.compare_at_price" class="compare-price">
            ${{ Number(product.compare_at_price).toFixed(2) }}
          </span>
        </div>

        <!-- Add to Cart Button -->
        <button
          class="btn-card-add"
          :class="{ 'btn-added': isAdded }"
          @click.stop="handleAddToCart"
          :disabled="product.stock <= 0"
        >
          <ShoppingCart :size="14" :stroke-width="1.8" />
          <span>{{ buttonText }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useWishlistStore } from '@/stores/wishlist'
import { useNotificationStore } from '@/stores/notification'
import { Heart, ShoppingCart, Star } from 'lucide-vue-next'

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
  viewMode: {
    type: String,
    default: 'grid', // 'grid' | 'list'
  },
})

const cartStore = useCartStore()
const wishlistStore = useWishlistStore()
const notificationStore = useNotificationStore()
const isAdded = ref(false)

const hasDiscount = computed(() => {
  return props.product.compare_at_price && props.product.compare_at_price > props.product.price
})

const discountPercent = computed(() => {
  if (!hasDiscount.value) return 0
  const diff = props.product.compare_at_price - props.product.price
  return Math.round((diff / props.product.compare_at_price) * 100)
})

const badgeClass = computed(() => {
  const b = (props.product.badge || '').toLowerCase()
  if (b.includes('seller')) return 'badge-bestseller'
  if (b.includes('new')) return 'badge-new'
  if (b.includes('%') || b.includes('off') || b.includes('sale')) return 'badge-sale'
  if (b.includes('value') || b.includes('set')) return 'badge-value'
  return 'badge-default'
})

const buttonText = computed(() => {
  if (props.product.stock <= 0) return 'Sold Out'
  if (isAdded.value) return 'Added!'
  return 'Add to Cart'
})

const formatReviews = (num) => {
  if (!num) return '0'
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const isWishlisted = computed(() => wishlistStore.isInWishlist(props.product.id))

const toggleWishlist = () => {
  wishlistStore.toggleItem(props.product)
}

const handleAddToCart = () => {
  cartStore.addItem(props.product, 1)
  isAdded.value = true
  notificationStore.addToast(`Added "${props.product.name}" to your bag`, 'success')
  setTimeout(() => {
    isAdded.value = false
  }, 1600)
}
</script>

<style scoped>
.product-card {
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.07);
  border-radius: 14px;
  padding: 0.95rem 0.95rem 1.05rem;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.32s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.28s ease;
  animation: cardEntrance 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px -6px rgba(36, 39, 33, 0.12), 0 4px 14px rgba(28, 25, 23, 0.04);
  border-color: rgba(142, 74, 62, 0.22);
}

.product-card:active {
  transform: scale(0.985);
}

.image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  background: #F4EFEB;
}

.image-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.42s cubic-bezier(0.16, 1, 0.3, 1);
}

.product-card:hover .product-img {
  transform: scale(1.07);
}

.card-heart-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #8C877F;
  z-index: 5;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: color 0.2s ease, transform 0.24s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.card-heart-btn:hover {
  color: #8E4A3E;
  background: #FFFFFF;
  border-color: rgba(142, 74, 62, 0.3);
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(142, 74, 62, 0.18);
}

.card-heart-btn.is-active {
  color: #8E4A3E;
  background: #FFFFFF;
  border-color: rgba(142, 74, 62, 0.35);
  box-shadow: 0 4px 14px rgba(142, 74, 62, 0.22);
  animation: heartPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes heartPop {
  0% { transform: scale(1); }
  45% { transform: scale(1.35); }
  100% { transform: scale(1); }
}

.badge-stack {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 5;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.badge {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: #8E4A3E;
  color: #FFFFFF;
  line-height: 1.2;
}

.badge-bestseller,
.badge-sale,
.badge-new,
.badge-value,
.badge-default {
  background: #8E4A3E;
  color: #FFFFFF;
}

.product-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.brand-name {
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.01em;
  color: #1C1917;
}

.subcat-tag {
  font-size: 0.7rem;
  color: #8C877F;
  background: #F4EFEB;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.product-title {
  font-family: var(--font-sans);
  font-size: 0.74rem;
  font-weight: 400;
  line-height: 1.3;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-title a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.2s ease;
}

.product-title a:hover {
  color: #1C1917;
}

.list-desc {
  font-size: 0.8rem;
  color: #78716C;
  line-height: 1.4;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-rating-row {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.68rem;
  margin-bottom: 6px;
}

.stars-wrap {
  display: inline-flex;
  align-items: center;
  gap: 1.5px;
}

.star-icon {
  color: #D6D3D1;
  fill: transparent;
}

.star-icon.filled {
  color: #F59E0B;
  fill: #F59E0B;
}

.score {
  font-weight: 600;
  color: #1C1917;
}

.reviews-count {
  color: #78716C;
}

.price-action-group {
  margin-top: auto;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-bottom: 8px;
  margin-top: 2px;
}

.current-price {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.compare-price {
  font-size: 0.78rem;
  color: #A8A29E;
  text-decoration: line-through;
}

/* Home Page Matching Porcelain Button with Smooth Dark Hover */
.btn-card-add {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.52rem 0.65rem;
  border-radius: 6px;
  background: #F4EFEB;
  border: 1px solid rgba(28, 25, 23, 0.06);
  font-size: 0.78rem;
  font-weight: 600;
  color: #1C1917;
  cursor: pointer;
  transition: all 0.24s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-card-add:hover:not(:disabled) {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
  transform: translateY(-2px);
  box-shadow: 0 5px 14px rgba(36, 39, 33, 0.18);
}

.btn-card-add:active:not(:disabled) {
  transform: scale(0.97);
}

.btn-card-add.btn-added {
  background: #242721;
  color: #FFFFFF;
  border-color: #242721;
}

.btn-card-add:disabled {
  background: #E5DFD7;
  color: #9C958E;
  border-color: transparent;
  cursor: not-allowed;
}

/* ==========================================================================
   LIST LAYOUT (View Mode: List)
   ========================================================================== */
.product-card.list-layout {
  flex-direction: row;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 1.25rem;
}

.product-card.list-layout .image-wrapper {
  width: 130px;
  height: 130px;
  aspect-ratio: auto;
  margin-bottom: 0;
  flex-shrink: 0;
}

.product-card.list-layout .product-info {
  flex: 1;
}

.product-card.list-layout .price-action-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.product-card.list-layout .price-row {
  margin-bottom: 0;
}

.product-card.list-layout .btn-card-add {
  width: auto;
  min-width: 140px;
  padding: 0.6rem 1.2rem;
}

@media (max-width: 640px) {
  .product-card.list-layout {
    flex-direction: column;
    align-items: stretch;
  }
  .product-card.list-layout .image-wrapper {
    width: 100%;
    height: auto;
    aspect-ratio: 1 / 1;
    margin-bottom: 0.75rem;
  }
  .product-card.list-layout .price-action-group {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  .product-card.list-layout .btn-card-add {
    width: 100%;
  }
}
</style>
