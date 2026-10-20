<template>
  <div class="skeleton-loader">
    <div v-for="i in rows" :key="i" class="skeleton-row">
      <div v-for="j in columns" :key="j" class="skeleton-cell"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  rows: { type: Number, default: 6 },
  columns: { type: Number, default: 5 }
})
</script>

<style scoped>
.skeleton-loader {
  width: 100%;
  padding: 1.25rem;
}

.skeleton-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.875rem;
  align-items: center;
}

.skeleton-cell {
  flex: 1;
  height: 38px;
  background: linear-gradient(
    90deg,
    #F5ECE6 0%,
    #EFE7E0 50%,
    #F5ECE6 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
