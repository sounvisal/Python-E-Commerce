<template>
  <div class="carrier-selector-wrapper">
    <div class="carrier-header">
      <span class="carrier-title">Select Cambodia Courier</span>
      <span class="carrier-subtitle">Direct delivery to all 25 provinces and Phnom Penh</span>
    </div>

    <div class="carrier-grid" role="radiogroup" aria-label="Cambodia Delivery Courier Options">
      <div
        v-for="carrier in carriers"
        :key="carrier.id"
        class="carrier-card"
        :class="{ 'is-selected': modelValue === carrier.id }"
        @click="selectCarrier(carrier)"
        role="radio"
        :aria-checked="modelValue === carrier.id"
        tabindex="0"
        @keydown.space.prevent="selectCarrier(carrier)"
        @keydown.enter.prevent="selectCarrier(carrier)"
      >
        <div class="carrier-card-top">
          <div class="carrier-badge-wrap">
            <span class="carrier-badge" :class="`badge-${carrier.id}`">{{ carrier.badge }}</span>
          </div>
          <div class="carrier-fee">
            <span v-if="getCarrierFee(carrier) === 0" class="fee-free">FREE</span>
            <span v-else class="fee-amount">${{ getCarrierFee(carrier).toFixed(2) }}</span>
          </div>
        </div>

        <div class="carrier-info">
          <div class="carrier-name-row">
            <span class="carrier-radio-dot" aria-hidden="true"></span>
            <h4 class="carrier-name">{{ carrier.name }}</h4>
          </div>
          <p class="carrier-desc">{{ carrier.description }}</p>
          <div class="carrier-transit-row">
            <Clock :size="13" class="transit-icon-clean" />
            <span class="transit-time">{{ carrier.transit }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Clock } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'vet_express'
  },
  subtotal: {
    type: Number,
    default: 0
  },
  freeShippingThreshold: {
    type: Number,
    default: 50.0
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const carriers = [
  {
    id: 'vet_express',
    name: 'Vireak Buntham (VET Logistics)',
    description: "Cambodia's #1 nationwide courier service. Direct door-to-door delivery across all 25 provinces.",
    fee: 1.50,
    transit: '1–2 Business Days',
    badge: 'Nationwide #1',
    freeOverThreshold: true
  },
  {
    id: 'jt_express',
    name: 'J&T Express Cambodia',
    description: 'High-speed express courier with live automated GPS van dispatch and phone coordination.',
    fee: 1.75,
    transit: 'Next-Day Delivery',
    badge: 'Fast Domestic',
    freeOverThreshold: true
  },
  {
    id: 'grab_express',
    name: 'GrabExpress On-Demand',
    description: 'Direct instant motorbike dispatch for urgent beauty rituals within Phnom Penh city limits.',
    fee: 3.50,
    transit: '60–90 Mins (Phnom Penh)',
    badge: 'Instant Express',
    freeOverThreshold: false
  },
  {
    id: 'lumea_concierge',
    name: 'Luméa Atelier Concierge',
    description: 'White-glove luxury delivery in signature silk-ribbon boxes with complimentary deluxe samples.',
    fee: 3.00,
    transit: 'White-Glove Scheduled',
    badge: 'Atelier Signature',
    freeOverThreshold: true
  }
]

function getCarrierFee(carrier) {
  if (props.subtotal >= props.freeShippingThreshold && carrier.freeOverThreshold) {
    return 0.0
  }
  return carrier.fee
}

function selectCarrier(carrier) {
  emit('update:modelValue', carrier.id)
  emit('change', {
    carrier,
    fee: getCarrierFee(carrier)
  })
}
</script>

<style scoped>
.carrier-selector-wrapper {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px dashed #E5E0D8;
}

.carrier-header {
  margin-bottom: 0.85rem;
}

.carrier-title {
  display: block;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #1C1917;
}

.carrier-subtitle {
  display: block;
  font-size: 0.8rem;
  color: #78716C;
  margin-top: 0.15rem;
}

.carrier-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.75rem;
}

.carrier-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0.9rem;
  background: #FFFFFF;
  border: 1.5px solid #EAE5DF;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.22s ease;
  user-select: none;
}

.carrier-card:hover {
  border-color: #CBB4A0;
  background: #FCFAF8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(122, 46, 34, 0.06);
}

.carrier-card.is-selected {
  border-color: #7A2E22;
  background: #FAF6F3;
  box-shadow: 0 4px 16px rgba(122, 46, 34, 0.1);
}

.carrier-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.carrier-badge {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  background: #F2EBE5;
  color: #7A2E22;
}

.badge-grab_express {
  background: #E8F5E9;
  color: #2E7D32;
}

.badge-lumea_concierge {
  background: #FDF4E3;
  color: #925E1A;
}

.badge-jt_express {
  background: #FBE9E7;
  color: #D84315;
}

.carrier-fee {
  font-size: 0.95rem;
  font-weight: 800;
}

.fee-free {
  color: #16A34A;
  background: #DCFCE7;
  padding: 0.15rem 0.45rem;
  border-radius: 6px;
  font-size: 0.78rem;
}

.fee-amount {
  color: #1C1917;
}

.carrier-name-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  margin-bottom: 0.35rem;
}

.carrier-radio-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 1.5px solid #D6D3D1;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.carrier-card.is-selected .carrier-radio-dot {
  border-color: #7A2E22;
  background: #7A2E22;
  box-shadow: inset 0 0 0 2.5px #FFFFFF;
}

.carrier-name {
  margin: 0;
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.25;
}

.carrier-desc {
  margin: 0 0 0.5rem 0;
  font-size: 0.75rem;
  color: #78716C;
  line-height: 1.35;
}

.carrier-transit-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.72rem;
  color: #57534E;
  font-weight: 600;
}

.transit-icon-clean {
  color: #8C7E72;
  flex-shrink: 0;
}
</style>
