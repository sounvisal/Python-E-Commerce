import { defineStore } from 'pinia'
import { useNotificationStore } from './notification'

const initialMockItems = [
  {
    id: 101,
    brand: 'SK-II',
    name: 'Facial Treatment Essence',
    volume: '230 ml',
    price: 99.00,
    compare_at_price: 142.00,
    rating: 4.8,
    reviews: '1.2K',
    stockStatus: 'In Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/prod-sk2.jpg',
    slug: 'sk-ii-facial-treatment-essence'
  },
  {
    id: 102,
    brand: 'The Ordinary',
    name: 'Niacinamide 10% + Zinc 1%',
    volume: '30 ml',
    price: 8.90,
    compare_at_price: 11.00,
    rating: 4.7,
    reviews: '9.8K',
    stockStatus: 'In Stock',
    isPriceDrop: true,
    isRecent: false,
    image_url: '/images/prod-ordinary.jpg',
    slug: 'the-ordinary-niacinamide-10-zinc-1'
  },
  {
    id: 103,
    brand: 'Laneige',
    name: 'Lip Sleeping Mask',
    volume: '20 g',
    price: 24.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '4.1K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: true,
    image_url: '/images/prod-laneige.jpg',
    slug: 'laneige-lip-sleeping-mask'
  },
  {
    id: 104,
    brand: 'CeraVe',
    name: 'Hydrating Facial Cleanser',
    volume: '236 ml',
    price: 16.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '6.2K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-cerave-cleanser.jpg',
    slug: 'cerave-hydrating-cleanser'
  },
  {
    id: 105,
    brand: 'Estée Lauder',
    name: 'Advanced Night Repair',
    volume: '50 ml',
    price: 78.00,
    compare_at_price: 104.00,
    rating: 4.7,
    reviews: '9.9K',
    stockStatus: 'Low Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/bottle-cerave.jpg',
    slug: 'estee-lauder-advanced-night-repair'
  },
  {
    id: 106,
    brand: 'Beauty of Joseon',
    name: 'Relief Sun: Rice + Probiotics SPF50+ PA++++',
    volume: '50 ml',
    price: 17.00,
    compare_at_price: 22.00,
    rating: 4.8,
    reviews: '5.4K',
    stockStatus: 'Back in Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-boj.jpg',
    slug: 'beauty-of-joseon-relief-sun'
  },
  {
    id: 501,
    brand: 'COSRX',
    name: 'Advanced Snail 96 Mucin Power Essence',
    volume: '100 ml',
    price: 25.00,
    compare_at_price: null,
    rating: 4.8,
    reviews: '3.9K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: true,
    image_url: '/images/prod-cosrx-snail.jpg',
    slug: 'cosrx-snail-96-essence'
  },
  {
    id: 502,
    brand: 'innisfree',
    name: 'Green Tea Seed Hyaluronic Serum',
    volume: '80 ml',
    price: 28.00,
    compare_at_price: 34.00,
    rating: 4.6,
    reviews: '2.1K',
    stockStatus: 'In Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/prod-innisfree-cleanser.jpg',
    slug: 'innisfree-green-tea-seed-serum'
  },
  {
    id: 503,
    brand: 'La Roche-Posay',
    name: 'Cicaplast Baume B5+ Ultra-Repairing Balm',
    volume: '40 ml',
    price: 18.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '3.2K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-laroche-effaclar.jpg',
    slug: 'la-roche-posay-cicaplast-baume'
  },
  {
    id: 504,
    brand: 'TIRTIR',
    name: 'Milk Skin Hydrating Glow Toner',
    volume: '150 ml',
    price: 24.00,
    compare_at_price: 29.00,
    rating: 4.7,
    reviews: '1.9K',
    stockStatus: 'Back in Stock',
    isPriceDrop: true,
    isRecent: true,
    image_url: '/images/prod-anua-toner.jpg',
    slug: 'tirtir-milk-skin-toner'
  },
  {
    id: 505,
    brand: 'Medicube',
    name: 'Collagen Jelly Cream',
    volume: '50 ml',
    price: 28.00,
    compare_at_price: null,
    rating: 4.6,
    reviews: '1.8K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: false,
    image_url: '/images/prod-laneige.jpg',
    slug: 'medicube-collagen-jelly-cream'
  },
  {
    id: 506,
    brand: 'Anua',
    name: 'Heartleaf 77% Soothing Toner',
    volume: '250 ml',
    price: 26.00,
    compare_at_price: null,
    rating: 4.7,
    reviews: '3.6K',
    stockStatus: 'In Stock',
    isPriceDrop: false,
    isRecent: true,
    image_url: '/images/prod-anua-cleanser.jpg',
    slug: 'anua-heartleaf-77-toner'
  }
]

export const useWishlistStore = defineStore('wishlist', {
  state: () => {
    const stored = localStorage.getItem('lumea_wishlist')
    return {
      items: stored ? JSON.parse(stored) : [...initialMockItems],
    }
  },

  getters: {
    totalItems: (state) => state.items.length,
    isInWishlist: (state) => (productId) => state.items.some((item) => item.id === productId),
    recentlyViewed: (state) => state.items.filter((item) => item.isRecent),
    priceDrops: (state) => state.items.filter((item) => item.isPriceDrop || (item.compare_at_price && item.compare_at_price > item.price)),
    backInStock: (state) => state.items.filter((item) => item.stockStatus === 'Back in Stock' || item.stockStatus === 'Low Stock'),
  },

  actions: {
    saveToStorage() {
      localStorage.setItem('lumea_wishlist', JSON.stringify(this.items))
    },

    toggleItem(product) {
      const notificationStore = useNotificationStore()
      const index = this.items.findIndex((item) => item.id === product.id)
      if (index > -1) {
        this.items.splice(index, 1)
        this.saveToStorage()
        notificationStore.addToast(`Removed "${product.name}" from wishlist`, 'info')
        return false
      } else {
        this.items.unshift({
          id: product.id,
          name: product.name,
          brand: product.brand,
          volume: product.volume || '50 ml',
          price: Number(product.price),
          compare_at_price: product.compare_at_price ? Number(product.compare_at_price) : null,
          rating: product.rating || 4.8,
          reviews: product.reviews || '500',
          stockStatus: product.stockStatus || 'In Stock',
          isPriceDrop: Boolean(product.compare_at_price && product.compare_at_price > product.price),
          isRecent: true,
          image_url: product.image_url,
          slug: product.slug,
          addedAt: new Date().toISOString(),
        })
        this.saveToStorage()
        notificationStore.addToast(`Saved "${product.name}" to wishlist`, 'success')
        return true
      }
    },

    addItem(product) {
      if (!this.isInWishlist(product.id)) {
        this.toggleItem(product)
      }
    },

    removeItem(productId) {
      const item = this.items.find((i) => i.id === productId)
      this.items = this.items.filter((i) => i.id !== productId)
      this.saveToStorage()
      if (item) {
        const notificationStore = useNotificationStore()
        notificationStore.addToast(`Removed "${item.name}" from wishlist`, 'info')
      }
    },

    removeMultiple(ids) {
      this.items = this.items.filter((i) => !ids.includes(i.id))
      this.saveToStorage()
      const notificationStore = useNotificationStore()
      notificationStore.addToast(`Removed ${ids.length} items from wishlist`, 'info')
    },

    resetToDefault() {
      this.items = [...initialMockItems]
      this.saveToStorage()
    },

    clearAll() {
      this.items = []
      this.saveToStorage()
    },
  },
})
