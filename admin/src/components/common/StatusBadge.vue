<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
  },
  type: {
    type: String,
    default: 'order', // 'order' or 'stock'
  },
})

const badgeConfig = computed(() => {
  const s = (props.status || '').toLowerCase()
  if (props.type === 'stock') {
    const qty = Number(props.status)
    if (qty <= 0) return { class: 'badge-rose', label: 'Out of Stock' }
    if (qty <= 5) return { class: 'badge-amber', label: `Low Stock (${qty})` }
    return { class: 'badge-emerald', label: `In Stock (${qty})` }
  }

  switch (s) {
    case 'delivered':
      return { class: 'badge-emerald', label: 'Delivered' }
    case 'shipped':
      return { class: 'badge-blue', label: 'Shipped' }
    case 'processing':
      return { class: 'badge-amber', label: 'Processing' }
    case 'confirmed':
      return { class: 'badge-gold', label: 'Confirmed' }
    case 'pending':
      return { class: 'badge-neutral', label: 'Pending' }
    case 'cancelled':
      return { class: 'badge-rose', label: 'Cancelled' }
    case 'pending approval':
      return { class: 'badge-amber', label: 'Pending Approval' }
    case 'approved':
      return { class: 'badge-emerald', label: 'Approved' }
    case 'in transit':
      return { class: 'badge-blue', label: 'In Transit' }
    case 'items inspected':
      return { class: 'badge-gold', label: 'Items Inspected' }
    case 'refund processed':
      return { class: 'badge-emerald', label: 'Refund Processed' }
    case 'completed':
      return { class: 'badge-emerald', label: 'Completed' }
    case 'rejected':
      return { class: 'badge-rose', label: 'Rejected' }
    default:
      return { class: 'badge-neutral', label: props.status }
  }
})
</script>

<template>
  <span class="badge" :class="badgeConfig.class">
    <span class="badge-dot"></span>
    {{ badgeConfig.label }}
  </span>
</template>
