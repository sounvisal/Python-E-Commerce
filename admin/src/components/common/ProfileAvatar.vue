<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  name: { type: String, default: '' },
  src: { type: String, default: '' },
})

const failedImage = ref('')
const initials = computed(() =>
  props.name?.trim().split(/\s+/).slice(0, 2).map(part => Array.from(part)[0]).join('').toUpperCase() || '?'
)
</script>

<template>
  <span class="profile-avatar" aria-hidden="true">
    <img
      v-if="src && src !== failedImage && src !== '/images/avatars/avatar-default.png'"
      :src="src"
      alt=""
      @error="failedImage = src"
    />
    <span v-else>{{ initials }}</span>
  </span>
</template>

<style scoped>
.profile-avatar {
  display: inline-grid;
  place-items: center;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 50%;
  color: var(--crimson);
  background: #f5e7df;
  font-size: 0.8rem;
  font-weight: 700;
  line-height: 1;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
