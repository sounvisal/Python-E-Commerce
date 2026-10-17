<template>
  <div class="brand-vector-logo" :class="[`brand-${actualSlug}`, sizeClass]">
    <!-- 1. SK-II -->
    <svg v-if="actualSlug === 'sk-ii'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="32" font-family="'Playfair Display', Georgia, serif" font-weight="900" font-size="32" fill="#B91C1C" letter-spacing="0.08em" text-anchor="middle">
        SK-II
      </text>
    </svg>

    <!-- 2. The Ordinary. -->
    <svg v-else-if="actualSlug === 'the-ordinary'" viewBox="0 0 180 50" class="brand-svg">
      <text x="50%" y="33" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="800" font-size="21" fill="#1C1917" letter-spacing="-0.02em" text-anchor="middle">
        The Ordinary.
      </text>
    </svg>

    <!-- 3. CeraVe -->
    <svg v-else-if="actualSlug === 'cerave'" viewBox="0 0 160 45" class="brand-svg">
      <rect x="18" y="6" width="124" height="33" rx="6" fill="#005A9C" />
      <text x="50" y="29" font-family="'Plus Jakarta Sans', sans-serif" font-weight="400" font-size="20" fill="#FFFFFF">Cera</text>
      <text x="94" y="29" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="20" fill="#FFFFFF">Ve</text>
      <rect x="131" y="14" width="3" height="3" fill="#FFFFFF" rx="0.5" />
    </svg>

    <!-- 4. LANEIGE -->
    <svg v-else-if="actualSlug === 'laneige'" viewBox="0 0 180 45" class="brand-svg">
      <text x="50%" y="30" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="600" font-size="20" fill="#1C1917" letter-spacing="0.32em" text-anchor="middle">
        LANEIGE
      </text>
    </svg>

    <!-- 5. BIODERMA -->
    <svg v-else-if="actualSlug === 'bioderma'" viewBox="0 0 190 48" class="brand-svg">
      <text x="50%" y="27" font-family="'Plus Jakarta Sans', Georgia, sans-serif" font-weight="800" font-size="21" fill="#1C1917" letter-spacing="0.12em" text-anchor="middle">
        BIODERMA
      </text>
      <text x="50%" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="6.5" fill="#78716C" letter-spacing="0.22em" text-anchor="middle">
        LABORATOIRE DERMATOLOGIQUE
      </text>
    </svg>

    <!-- 6. LA ROCHE-POSAY -->
    <svg v-else-if="actualSlug === 'la-roche-posay'" viewBox="0 0 210 48" class="brand-svg">
      <rect x="8" y="14" width="10" height="10" rx="1.5" fill="#0284C7" />
      <g transform="translate(24, 0)">
        <text x="0" y="25" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="16" fill="#1C1917" letter-spacing="0.06em">
          LA ROCHE-POSAY
        </text>
        <text x="0" y="37" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="6" fill="#78716C" letter-spacing="0.18em">
          LABORATOIRE DERMATOLOGIQUE
        </text>
      </g>
    </svg>

    <!-- 7. innisfree -->
    <svg v-else-if="actualSlug === 'innisfree'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', Arial, sans-serif" font-weight="700" font-size="23" fill="#15803D" letter-spacing="-0.03em" text-anchor="middle">
        innisfree
      </text>
    </svg>

    <!-- 8. COSRX -->
    <svg v-else-if="actualSlug === 'cosrx'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="24" fill="#1C1917" letter-spacing="0.18em" text-anchor="middle">
        COSRX
      </text>
    </svg>

    <!-- 9. Anua -->
    <svg v-else-if="actualSlug === 'anua'" viewBox="0 0 140 45" class="brand-svg">
      <text x="50%" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-weight="500" font-size="27" fill="#1C1917" letter-spacing="0.04em" text-anchor="middle">
        Anua
      </text>
    </svg>

    <!-- 10. Beauty of Joseon -->
    <svg v-else-if="actualSlug === 'beauty-of-joseon' || actualSlug === 'boj'" viewBox="0 0 190 52" class="brand-svg">
      <g transform="translate(14, 4)">
        <rect x="0" y="0" width="22" height="26" rx="3" fill="#B91C1C" />
        <text x="11" y="12" font-family="serif" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">조선</text>
        <text x="11" y="22" font-family="serif" font-weight="800" font-size="9" fill="#FFFFFF" text-anchor="middle">미녀</text>
      </g>
      <text x="44" y="22" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="13" fill="#1C1917" letter-spacing="0.04em">Beauty of Joseon</text>
      <text x="44" y="34" font-family="'Plus Jakarta Sans', sans-serif" font-weight="500" font-size="8" fill="#78716C" letter-spacing="0.12em">TRADITIONAL HANBANG</text>
    </svg>

    <!-- 11. Sulwhasoo -->
    <svg v-else-if="actualSlug === 'sulwhasoo'" viewBox="0 0 180 45" class="brand-svg">
      <text x="50%" y="30" font-family="'Playfair Display', Georgia, serif" font-weight="700" font-size="23" fill="#B45309" letter-spacing="0.05em" text-anchor="middle">
        Sulwhasoo
      </text>
    </svg>

    <!-- 12. Dr.Jart+ -->
    <svg v-else-if="actualSlug === 'dr-jart'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="24" fill="#1C1917" letter-spacing="0.05em" text-anchor="middle">
        Dr.Jart+
      </text>
    </svg>

    <!-- 13. medicube -->
    <svg v-else-if="actualSlug === 'medicube'" viewBox="0 0 160 45" class="brand-svg">
      <text x="42" y="30" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="21" fill="#1C1917" letter-spacing="0.02em">
        medicube
      </text>
      <rect x="135" y="14" width="10" height="10" rx="2" fill="#DC2626" />
      <rect x="139" y="11" width="2" height="16" fill="#FFFFFF" />
      <rect x="132" y="18" width="16" height="2" fill="#FFFFFF" />
    </svg>

    <!-- 14. ESTÉE LAUDER -->
    <svg v-else-if="actualSlug === 'estee-lauder'" viewBox="0 0 190 45" class="brand-svg">
      <text x="50%" y="30" font-family="'Playfair Display', Georgia, serif" font-weight="700" font-size="19" fill="#1E3A8A" letter-spacing="0.18em" text-anchor="middle">
        ESTÉE LAUDER
      </text>
    </svg>

    <!-- 15. CLINIQUE -->
    <svg v-else-if="actualSlug === 'clinique'" viewBox="0 0 170 45" class="brand-svg">
      <text x="50%" y="30" font-family="'Playfair Display', Georgia, serif" font-weight="600" font-size="20" fill="#1C1917" letter-spacing="0.28em" text-anchor="middle">
        CLINIQUE
      </text>
    </svg>

    <!-- 16. Kiehl's -->
    <svg v-else-if="actualSlug === 'kiehls'" viewBox="0 0 170 48" class="brand-svg">
      <text x="50%" y="27" font-family="Georgia, serif" font-style="italic" font-weight="700" font-size="22" fill="#1C1917" letter-spacing="0.04em" text-anchor="middle">
        Kiehl's
      </text>
      <text x="50%" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="7" fill="#78716C" letter-spacing="0.22em" text-anchor="middle">
        SINCE 1851
      </text>
    </svg>

    <!-- 17. SHISEIDO -->
    <svg v-else-if="actualSlug === 'shiseido'" viewBox="0 0 180 48" class="brand-svg">
      <text x="50%" y="28" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="20" fill="#DC2626" letter-spacing="0.14em" text-anchor="middle">
        SHISEIDO
      </text>
      <text x="50%" y="40" font-family="'Plus Jakarta Sans', sans-serif" font-weight="500" font-size="7" fill="#78716C" letter-spacing="0.24em" text-anchor="middle">
        GINZA TOKYO
      </text>
    </svg>

    <!-- 18. Neutrogena -->
    <svg v-else-if="actualSlug === 'neutrogena'" viewBox="0 0 170 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="21" fill="#1C1917" letter-spacing="0.02em" text-anchor="middle">
        Neutrogena®
      </text>
    </svg>

    <!-- 19. Avène -->
    <svg v-else-if="actualSlug === 'avene'" viewBox="0 0 180 48" class="brand-svg">
      <text x="50%" y="16" font-family="'Plus Jakarta Sans', sans-serif" font-weight="600" font-size="7" fill="#C2410C" letter-spacing="0.24em" text-anchor="middle">
        EAU THERMALE
      </text>
      <text x="50%" y="37" font-family="'Playfair Display', Georgia, serif" font-weight="700" font-size="23" fill="#C2410C" letter-spacing="0.06em" text-anchor="middle">
        Avène
      </text>
    </svg>

    <!-- 20. Eucerin -->
    <svg v-else-if="actualSlug === 'eucerin'" viewBox="0 0 160 48" class="brand-svg">
      <polygon points="20,14 36,14 28,26" fill="#DC2626" />
      <text x="44" y="27" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="22" fill="#1E3A8A">
        Eucerin®
      </text>
    </svg>

    <!-- 21. Cetaphil -->
    <svg v-else-if="actualSlug === 'cetaphil'" viewBox="0 0 170 48" class="brand-svg">
      <rect x="18" y="7" width="134" height="34" rx="17" fill="#00A86B" />
      <rect x="22" y="9" width="126" height="30" rx="15" fill="#005A9C" />
      <text x="50%" y="30" font-family="'Plus Jakarta Sans', sans-serif" font-weight="800" font-size="18" fill="#FFFFFF" letter-spacing="0.02em" text-anchor="middle">
        Cetaphil
      </text>
    </svg>

    <!-- 22. numbuzin -->
    <svg v-else-if="actualSlug === 'numbuzin'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="22" fill="#1C1917" letter-spacing="-0.02em" text-anchor="middle">
        numbuzin
      </text>
    </svg>

    <!-- 23. TIRTIR -->
    <svg v-else-if="actualSlug === 'tirtir'" viewBox="0 0 160 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="23" fill="#1C1917" letter-spacing="0.22em" text-anchor="middle">
        TIRTIR
      </text>
    </svg>

    <!-- 24. SOME BY MI -->
    <svg v-else-if="actualSlug === 'some-by-mi'" viewBox="0 0 180 45" class="brand-svg">
      <text x="50%" y="31" font-family="'Plus Jakarta Sans', sans-serif" font-weight="900" font-size="20" fill="#1C1917" letter-spacing="0.1em" text-anchor="middle">
        SOME BY MI
      </text>
    </svg>

    <!-- Generic Fallback -->
    <svg v-else viewBox="0 0 170 45" class="brand-svg">
      <text x="50%" y="30" font-family="'Plus Jakarta Sans', sans-serif" font-weight="700" font-size="19" fill="#1C1917" letter-spacing="0.06em" text-anchor="middle">
        {{ nameFromSlug }}
      </text>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  slug: {
    type: String,
    default: '',
  },
  brand: {
    type: String,
    default: '',
  },
  name: {
    type: String,
    default: '',
  },
  size: {
    type: [Number, String],
    default: 40,
  },
})

const actualSlug = computed(() => {
  const raw = (props.slug || props.brand || props.name || '').toString()
  const s = raw
    .toLowerCase()
    .trim()
    .replace(/[éèê]/g, 'e')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

  if (s === 'sk-ii' || s === 'sk2' || s === 'sk-2') return 'sk-ii'
  if (s === 'the-ordinary' || s === 'ordinary') return 'the-ordinary'
  if (s === 'dr-jart' || s === 'dr-jart-' || s === 'drjart') return 'dr-jart'
  if (s === 'beauty-of-joseon' || s === 'boj') return 'beauty-of-joseon'
  if (s === 'la-roche-posay' || s === 'laroche-posay' || s === 'la-roche' || s === 'laroche') return 'la-roche-posay'
  if (s === 'estee-lauder' || s === 'estee-lauder-') return 'estee-lauder'
  if (s === 'eau-thermale-avene' || s === 'avene') return 'avene'
  if (s === 'some-by-mi' || s === 'somebymi' || s === 'some-by') return 'some-by-mi'
  return s
})

const sizeClass = computed(() => {
  if (props.size === 'circle') return 'size-circle'
  if (props.size === 'marquee') return 'size-marquee'
  const num = Number(props.size)
  if (!isNaN(num)) {
    if (num <= 24) return 'size-sm'
    if (num >= 50) return 'size-lg'
  }
  return 'size-md'
})

const nameFromSlug = computed(() => {
  if (props.brand) return props.brand
  if (props.name) return props.name
  return actualSlug.value
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
})
</script>

<style scoped>
.brand-vector-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 150px;
  height: auto;
}

.brand-svg {
  width: 100%;
  height: 100%;
  max-height: 38px;
  object-fit: contain;
}

.size-sm .brand-svg {
  max-height: 22px;
}

.size-md .brand-svg {
  max-height: 34px;
}

.size-lg .brand-svg {
  max-height: 48px;
}

.size-circle {
  width: 100%;
  max-width: 82%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.size-circle .brand-svg {
  width: 100%;
  max-height: 38px;
}

.size-marquee {
  max-width: 125px;
}

.size-marquee .brand-svg {
  max-height: 26px;
}
</style>
