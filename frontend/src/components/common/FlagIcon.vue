<template>
  <span class="flag-icon-container" :class="`flag-${locale}`">
    <!-- United Kingdom Flag -->
    <svg v-if="locale === 'en' || locale === 'gb'" class="flag-svg" viewBox="0 0 60 40" width="18" height="12" aria-label="English">
      <clipPath :id="`gb-clip-${uid}`"><rect width="60" height="40" rx="2"/></clipPath>
      <g :clip-path="`url(#gb-clip-${uid})`">
        <rect width="60" height="40" fill="#012169"/>
        <path d="M0 0 L60 40 M60 0 L0 40" stroke="#FFF" stroke-width="8"/>
        <path d="M0 0 L60 40 M60 0 L0 40" stroke="#C8102E" stroke-width="4"/>
        <path d="M30 0 v40 M0 20 h60" stroke="#FFF" stroke-width="12"/>
        <path d="M30 0 v40 M0 20 h60" stroke="#C8102E" stroke-width="8"/>
      </g>
    </svg>

    <!-- Cambodia Flag -->
    <svg v-else-if="locale === 'km' || locale === 'kh'" class="flag-svg" viewBox="0 0 60 40" width="18" height="12" aria-label="Khmer">
      <clipPath :id="`kh-clip-${uid}`"><rect width="60" height="40" rx="2"/></clipPath>
      <g :clip-path="`url(#kh-clip-${uid})`">
        <rect width="60" height="10" fill="#032ea1"/>
        <rect y="10" width="60" height="20" fill="#e00025"/>
        <rect y="30" width="60" height="10" fill="#032ea1"/>
        <!-- Clean Angkor Wat Silhouette -->
        <path d="M20 26 h20 v-3 h-2 v-3 h-3 v3 h-3 v-6 h-2 v-2 h-2 v2 h-2 v6 h-3 v-3 h-3 v3 h-2 z" fill="#FFF"/>
      </g>
    </svg>

    <!-- China Flag -->
    <svg v-else-if="locale === 'zh' || locale === 'cn'" class="flag-svg" viewBox="0 0 60 40" width="18" height="12" aria-label="Chinese">
      <clipPath :id="`cn-clip-${uid}`"><rect width="60" height="40" rx="2"/></clipPath>
      <g :clip-path="`url(#cn-clip-${uid})`">
        <rect width="60" height="40" fill="#de2910"/>
        <!-- Main Star -->
        <polygon points="10,6 12,12 7,8 13,8 8,12" fill="#ffde00"/>
        <!-- Small Stars -->
        <polygon points="17,3 18,6 15,4 19,4 16,6" fill="#ffde00"/>
        <polygon points="20,7 21,10 18,8 22,8 19,10" fill="#ffde00"/>
        <polygon points="20,12 21,15 18,13 22,13 19,15" fill="#ffde00"/>
        <polygon points="17,16 18,19 15,17 19,17 16,19" fill="#ffde00"/>
      </g>
    </svg>
  </span>
</template>

<script setup>
const props = defineProps({
  locale: {
    type: String,
    default: 'en'
  }
})

const uid = Math.random().toString(36).substring(2, 7)
</script>

<style scoped>
.flag-icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  vertical-align: middle;
  line-height: 1;
}

.flag-svg {
  display: block;
  border-radius: 2px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}
</style>
