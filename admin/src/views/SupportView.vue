<script setup>
import { onMounted, ref } from 'vue'
import apiClient from '@/api/client'
const messages = ref([])
const loading = ref(false)
const error = ref('')
async function load() {
  loading.value = true
  error.value = ''
  try { messages.value = (await apiClient.get('/contact')).data }
  catch { error.value = 'Unable to load inquiries. Please retry.' }
  finally { loading.value = false }
}
onMounted(load)
</script>

<template>
  <section class="support-inbox">
    <header><div><h1>Customer inquiries</h1><p>Messages received through the storefront contact form.</p></div><button class="btn btn-secondary" @click="load" :disabled="loading">Refresh</button></header>
    <p v-if="loading" role="status">Loading inquiries...</p>
    <p v-else-if="error" role="alert">{{ error }}</p>
    <p v-else-if="!messages.length">No inquiries have been received.</p>
    <article v-for="message in messages" :key="message.id" class="inquiry">
      <div class="inquiry-meta"><strong>{{ message.reference }}</strong><span>{{ new Date(message.created_at).toLocaleString() }}</span></div>
      <h2>{{ message.subject }}</h2>
      <p>{{ message.name }} · {{ message.email }}</p>
      <p class="message-body">{{ message.message }}</p>
    </article>
  </section>
</template>

<style scoped>
.support-inbox { padding: 2rem; max-width: 1050px; margin: auto; }
header, .inquiry-meta { display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
header { margin-bottom: 2rem; align-items: center; }
.inquiry { background: white; border: 1px solid #eadfd7; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; }
.inquiry-meta { color: #785c51; font-size: .85rem; }
h2 { font-size: 1.1rem; margin: 1rem 0 .5rem; }
.message-body { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.7; }
</style>
