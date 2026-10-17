import { defineStore } from 'pinia'

export const useBannerStore = defineStore('banners', {
  state: () => ({
    banners: {},
    isLoading: false,
    error: null,
  }),

  getters: {
    getBanner: (state) => (pageKey, fallback = {}) => {
      const banner = state.banners[pageKey]
      if (banner && banner.is_active) {
        return {
          title: banner.title || fallback.title || '',
          subtitle: banner.subtitle || fallback.subtitle || '',
          script_text: banner.script_text || fallback.script_text || '',
          badge_text: banner.badge_text || fallback.badge_text || '',
          image_url: banner.image_url || fallback.image_url || '',
          cta_text: banner.cta_text || fallback.cta_text || '',
          cta_link: banner.cta_link || fallback.cta_link || '',
        }
      }
      return fallback
    },
  },

  actions: {
    async fetchBanners() {
      // Don't re-fetch if we already have banners populated
      if (Object.keys(this.banners).length > 0) return

      this.isLoading = true
      this.error = null

      try {
        const response = await fetch('/api/banners')
        if (response.ok) {
          const resData = await response.json()
          if (resData.status === 'success' && Array.isArray(resData.data)) {
            const mapped = {}
            resData.data.forEach((b) => {
              mapped[b.page] = b
            })
            this.banners = mapped
          }
        }
      } catch (err) {
        console.warn('[BannerStore] Failed to fetch remote banners, using frontend fallbacks:', err)
        this.error = err.message
      } finally {
        this.isLoading = false
      }
    },

    async fetchBannerByPage(pageKey) {
      if (this.banners[pageKey]) return this.banners[pageKey]

      try {
        const response = await fetch(`/api/banners/${pageKey}`)
        if (response.ok) {
          const resData = await response.json()
          if (resData.status === 'success' && resData.data) {
            this.banners[pageKey] = resData.data
            return resData.data
          }
        }
      } catch (err) {
        console.warn(`[BannerStore] Failed to fetch banner for '${pageKey}':`, err)
      }
      return null
    },
  },
})
