<template>
  <div class="map-picker-card" :class="{ 'compact-mode': compact }">
    <!-- Header (only shown if not in compact mode) -->
    <div v-if="!compact" class="map-picker-header">
      <div class="header-left">
        <span class="map-title">
          <MapPin :size="15" class="map-title-icon" />
          <span>Pinpoint Exact Delivery Location</span>
        </span>
        <span class="map-subtitle">Click map, search landmark, or paste Google Maps link to auto-fill your delivery address</span>
      </div>
    </div>

    <!-- Search & Google Maps Paste Toolbar (only shown if not in compact mode) -->
    <div v-if="!compact" class="map-toolbar">
      <!-- Live Place Search -->
      <div class="search-box-wrapper">
        <div class="input-with-icon">
          <Search :size="14" class="input-icon-svg" />
          <input
            type="text"
            v-model="searchQuery"
            class="map-search-input"
            placeholder="Search landmark, Borey, mall, or street in Cambodia (e.g. Aeon 2, Toul Kork)..."
            @input="handleSearchInput"
            @keydown.enter.prevent="triggerSearch"
          />
          <button v-if="searchQuery" type="button" class="btn-clear-search" @click="clearSearch">&times;</button>
        </div>
        <!-- Search Results Dropdown -->
        <ul v-if="searchResults.length > 0" class="search-results-dropdown">
          <li
            v-for="(res, idx) in searchResults"
            :key="idx"
            class="search-result-item"
            @click="selectSearchResult(res)"
          >
            <MapPin :size="13" class="res-pin-icon" />
            <span class="res-name">{{ res.display_name }}</span>
          </li>
        </ul>
      </div>

      <!-- Paste Google Maps Link or GPS -->
      <div class="gmaps-paste-wrapper">
        <div class="input-with-icon">
          <Compass :size="14" class="input-icon-svg" />
          <input
            type="text"
            v-model="pasteGmapsInput"
            class="gmaps-paste-input"
            placeholder="Paste Google Maps link or GPS (e.g. 11.5564, 104.9282)"
            @keydown.enter.prevent="applyPastedGmaps"
          />
          <button type="button" class="btn-apply-paste" @click="applyPastedGmaps">Pin</button>
        </div>
      </div>
    </div>

    <!-- Quick Location Presets (only shown if not in compact mode) -->
    <div v-if="!compact" class="preset-pills-row">
      <span class="preset-label">Quick Jump:</span>
      <div class="preset-pills-scroll">
        <button
          v-for="p in presets"
          :key="p.name"
          type="button"
          class="preset-pill"
          :class="{ active: currentPreset === p.name }"
          @click="jumpToPreset(p)"
        >
          {{ p.name }}
        </button>
      </div>
    </div>

    <!-- Map Canvas Container with Floating Locate Me Button -->
    <div class="map-viewport-wrapper">
      <div ref="mapContainer" class="leaflet-map-canvas"></div>

      <!-- Floating Locate Me Button on the map matching mockup -->
      <button
        type="button"
        class="locate-btn-on-map"
        :disabled="isLocating"
        @click="locateUser"
        title="Detect your current location via device GPS"
      >
        <span v-if="isLocating" class="locate-spinner"></span>
        <span v-else class="locate-btn-content">
          <Navigation :size="12" class="locate-icon-svg" />
          <span>Locate Me</span>
        </span>
      </button>

      <div v-if="!compact" class="map-coords-badge">
        <span class="coords-label">GPS:</span>
        <span class="coords-val">{{ formattedCoords }}</span>
      </div>
    </div>

    <!-- Auto-Filled Address Confirmation Banner (only shown if not in compact mode) -->
    <div v-if="!compact && reverseGeoAddress" class="geocoded-address-banner">
      <div class="geo-banner-left">
        <Sparkles :size="15" class="geo-icon-svg" />
        <div class="geo-text">
          <span class="geo-label">Auto-detected Address from Pin:</span>
          <strong class="geo-value">{{ reverseGeoAddress }}</strong>
          <span v-if="reverseGeoCity" class="geo-city"> · {{ reverseGeoCity }}</span>
        </div>
      </div>
      <button
        type="button"
        class="btn-apply-to-form"
        @click="forceApplyToForm"
        title="Fill this address into the checkout form"
      >
        <Check v-if="appliedToForm" :size="13" class="applied-check-icon" />
        <span>{{ appliedToForm ? 'Auto-Filled to Form' : 'Apply to Address Form' }}</span>
      </button>
    </div>

    <!-- Landmark Notes & Google Maps Verification Link (only when not compact) -->
    <div v-if="!compact" class="landmark-section">
      <div class="landmark-label-row">
        <label class="landmark-label" for="driverNotes">
          Delivery Landmark & Driver Instructions (Optional)
        </label>
        <div class="gmaps-external-links">
          <a
            :href="googleMapsUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="gmaps-preview-link"
          >
            <Compass :size="13" class="gmaps-icon-svg" />
            <span>Open Google Maps in New Tab</span>
            <ExternalLink :size="12" class="ext-arrow-svg" />
          </a>
        </div>
      </div>
      <input
        id="driverNotes"
        type="text"
        v-model="landmarkNotes"
        placeholder="E.g., Near Wat Phnom, opposite Chip Mong Mall, blue metal gate, call on arrival"
        class="landmark-input"
        @input="emitChanges"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useNotificationStore } from '@/stores/notification'
import {
  MapPin,
  Search,
  Compass,
  Navigation,
  Sparkles,
  Check,
  ExternalLink
} from 'lucide-vue-next'

const props = defineProps({
  initialLat: {
    type: Number,
    default: 11.5564
  },
  initialLng: {
    type: Number,
    default: 104.9282
  },
  initialNotes: {
    type: String,
    default: ''
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:location'])
const notificationStore = useNotificationStore()

const mapContainer = ref(null)
let mapInstance = null
let markerInstance = null

const selectedLat = ref(props.initialLat || 11.5564)
const selectedLng = ref(props.initialLng || 104.9282)
const landmarkNotes = ref(props.initialNotes || '')
const isLocating = ref(false)
const currentPreset = ref('BKK1 / Chamkarmon')

// Reverse geocode states
const reverseGeoAddress = ref('')
const reverseGeoCity = ref('')
const appliedToForm = ref(false)
let reverseGeoTimeout = null

// Search states
const searchQuery = ref('')
const searchResults = ref([])
let searchDebounceTimeout = null
let searchAbortController = null
let reverseGeoAbortController = null
let currentSearchId = 0

// Paste Google Maps input
const pasteGmapsInput = ref('')

const presets = [
  { name: 'BKK1 / Chamkarmon', lat: 11.5524, lng: 104.9282, zoom: 15 },
  { name: 'Daun Penh / Wat Phnom', lat: 11.5714, lng: 104.9282, zoom: 15 },
  { name: 'Toul Kork', lat: 11.5732, lng: 104.8967, zoom: 15 },
  { name: 'Sen Sok / Aeon 2', lat: 11.5850, lng: 104.8710, zoom: 15 },
  { name: 'Chroy Changvar', lat: 11.5950, lng: 104.9450, zoom: 15 },
  { name: 'Pur Senchey / Chaom Chau', lat: 11.5350, lng: 104.8350, zoom: 14 },
  { name: 'Siem Reap City', lat: 13.3633, lng: 103.8564, zoom: 14 },
  { name: 'Battambang City', lat: 13.0957, lng: 103.2022, zoom: 14 },
  { name: 'Sihanoukville Port', lat: 10.6275, lng: 103.5221, zoom: 14 }
]

const formattedCoords = computed(() => {
  return `${selectedLat.value.toFixed(5)}, ${selectedLng.value.toFixed(5)}`
})

const googleMapsUrl = computed(() => {
  return `https://www.google.com/maps?q=${selectedLat.value.toFixed(6)},${selectedLng.value.toFixed(6)}`
})

function emitChanges(autoAddress = null, autoCity = null) {
  emit('update:location', {
    lat: selectedLat.value,
    lng: selectedLng.value,
    notes: landmarkNotes.value,
    map_url: googleMapsUrl.value,
    auto_address: autoAddress || reverseGeoAddress.value,
    auto_city: autoCity || reverseGeoCity.value
  })
}

function updatePin(lat, lng, shouldReverseGeocode = true) {
  selectedLat.value = lat
  selectedLng.value = lng
  if (markerInstance) {
    markerInstance.setLatLng([lat, lng])
  }
  emitChanges()
  if (shouldReverseGeocode) {
    triggerReverseGeocode(lat, lng)
  }
}

function triggerReverseGeocode(lat, lng) {
  if (reverseGeoTimeout) clearTimeout(reverseGeoTimeout)
  if (reverseGeoAbortController) reverseGeoAbortController.abort()
  reverseGeoAbortController = new AbortController()

  reverseGeoTimeout = setTimeout(async () => {
    try {
      const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}&accept-language=en`
      const res = await fetch(url, {
        signal: reverseGeoAbortController.signal,
        headers: { 'Accept': 'application/json', 'User-Agent': 'Lumea-Atelier-Delivery/1.0' }
      })
      if (!res.ok) return
      const data = await res.json()
      if (data && data.address) {
        const a = data.address
        const parts = []
        if (a.amenity || a.building) parts.push(a.amenity || a.building)
        if (a.road) parts.push(a.road)
        if (a.suburb || a.neighbourhood || a.quarter) parts.push(a.suburb || a.neighbourhood || a.quarter)
        if (a.city_district || a.county) parts.push(a.city_district || a.county)
        
        const cleanAddress = parts.filter(Boolean).join(', ') || data.display_name.split(',').slice(0, 3).join(', ')
        let detectedCity = 'Phnom Penh'
        if (a.state && a.state.toLowerCase().includes('phnom penh')) {
          detectedCity = 'Phnom Penh'
        } else if (a.province) {
          detectedCity = a.province
        } else if (a.state) {
          detectedCity = a.state
        } else if (a.city) {
          detectedCity = a.city
        } else if (a.town && !a.town.toLowerCase().startsWith('khan')) {
          detectedCity = a.town
        }

        reverseGeoAddress.value = cleanAddress
        reverseGeoCity.value = detectedCity
        appliedToForm.value = true
        emitChanges(cleanAddress, detectedCity)
        setTimeout(() => { appliedToForm.value = false }, 3500)
      }
    } catch (e) {
      console.warn('Reverse geocode failed:', e)
    }
  }, 400)
}

function forceApplyToForm() {
  if (reverseGeoAddress.value) {
    appliedToForm.value = true
    emitChanges(reverseGeoAddress.value, reverseGeoCity.value)
    setTimeout(() => { appliedToForm.value = false }, 2500)
  }
}

function jumpToPreset(preset) {
  currentPreset.value = preset.name
  if (mapInstance) {
    mapInstance.setView([preset.lat, preset.lng], preset.zoom)
    updatePin(preset.lat, preset.lng, true)
  }
}

function locateUser() {
  if (!navigator.geolocation) {
    notificationStore.addToast('Geolocation is not supported by your browser.', 'warning')
    return
  }
  isLocating.value = true
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      isLocating.value = false
      const lat = pos.coords.latitude
      const lng = pos.coords.longitude
      currentPreset.value = 'GPS Detected'
      if (mapInstance) {
        mapInstance.setView([lat, lng], 16)
        updatePin(lat, lng, true)
      }
    },
    (err) => {
      isLocating.value = false
      console.warn('Geolocation error:', err.message)
      notificationStore.addToast('Unable to detect location. Please click on the map to set your pin.', 'warning')
    },
    { enableHighAccuracy: true, timeout: 8000 }
  )
}

// Live Place Search
function handleSearchInput() {
  if (searchDebounceTimeout) clearTimeout(searchDebounceTimeout)
  if (searchAbortController) {
    searchAbortController.abort()
    searchAbortController = null
  }
  currentSearchId++
  const activeId = currentSearchId

  if (!searchQuery.value || searchQuery.value.trim().length < 2) {
    searchResults.value = []
    return
  }
  searchDebounceTimeout = setTimeout(() => {
    triggerSearch(activeId)
  }, 350)
}

async function triggerSearch(reqId) {
  const q = searchQuery.value.trim()
  if (!q || q.length < 2) {
    searchResults.value = []
    return
  }
  if (searchAbortController) searchAbortController.abort()
  searchAbortController = new AbortController()
  try {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(q)}&countrycodes=kh&format=json&limit=5&accept-language=en`
    const res = await fetch(url, {
      signal: searchAbortController.signal,
      headers: { 'Accept': 'application/json', 'User-Agent': 'Lumea-Atelier-Delivery/1.0' }
    })
    // Invalidate if input was cleared or changed while request was in-flight
    if (reqId !== currentSearchId || !searchQuery.value || searchQuery.value.trim() !== q) {
      return
    }
    if (res.ok) {
      const data = await res.json()
      if (reqId === currentSearchId && searchQuery.value.trim() === q) {
        searchResults.value = data || []
      }
    }
  } catch (e) {
    if (e.name !== 'AbortError') {
      console.warn('Place search error:', e)
    }
  }
}

function selectSearchResult(res) {
  const lat = parseFloat(res.lat)
  const lng = parseFloat(res.lon)
  searchQuery.value = res.display_name.split(',')[0]
  searchResults.value = []
  currentPreset.value = res.display_name.split(',')[0]
  if (mapInstance) {
    mapInstance.setView([lat, lng], 16)
    updatePin(lat, lng, true)
  }
}

function clearSearch() {
  if (searchDebounceTimeout) clearTimeout(searchDebounceTimeout)
  if (searchAbortController) {
    searchAbortController.abort()
    searchAbortController = null
  }
  currentSearchId++
  searchQuery.value = ''
  searchResults.value = []
}

// Parse Pasted Google Maps URL or GPS coordinates
function applyPastedGmaps() {
  const raw = pasteGmapsInput.value.trim()
  if (!raw) return

  const coordRegex = /(-?\d+\.\d+)[,\s]+(-?\d+\.\d+)/
  const gmapsAtRegex = /@(-?\d+\.\d+),(-?\d+\.\d+)/
  const gmapsQRegex = /[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)/

  let match = raw.match(gmapsAtRegex) || raw.match(gmapsQRegex) || raw.match(coordRegex)
  if (match) {
    const lat = parseFloat(match[1])
    const lng = parseFloat(match[2])
    if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
      currentPreset.value = 'Pasted Location'
      pasteGmapsInput.value = ''
      if (mapInstance) {
        mapInstance.setView([lat, lng], 16)
        updatePin(lat, lng, true)
      }
      return
    }
  }
  notificationStore.addToast('Could not parse valid coordinates from the input. Please enter GPS (e.g. 11.5564, 104.9282) or paste a Google Maps link.', 'warning')
}

onMounted(async () => {
  await nextTick()
  if (!mapContainer.value) return

  // Custom luxury pin marker HTML matching Luméa theme
  const customIcon = L.divIcon({
    className: 'lumea-map-marker',
    html: `
      <div class="marker-pin-bubble">
        <span class="marker-dot"></span>
      </div>
      <div class="marker-shadow"></div>
    `,
    iconSize: [36, 44],
    iconAnchor: [18, 42]
  })

  mapInstance = L.map(mapContainer.value, {
    center: [selectedLat.value, selectedLng.value],
    zoom: 14,
    zoomControl: true,
    attributionControl: true,
    scrollWheelZoom: false
  })

  // OpenStreetMap clean tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(mapInstance)

  markerInstance = L.marker([selectedLat.value, selectedLng.value], {
    icon: customIcon,
    draggable: true
  }).addTo(mapInstance)

  markerInstance.on('dragend', (e) => {
    const latlng = e.target.getLatLng()
    updatePin(latlng.lat, latlng.lng, true)
    currentPreset.value = 'Custom Pin'
  })

  mapInstance.on('click', (e) => {
    updatePin(e.latlng.lat, e.latlng.lng, true)
    currentPreset.value = 'Custom Pin'
  })

  // Initial reverse-geocoding
  triggerReverseGeocode(selectedLat.value, selectedLng.value)
  emitChanges()
})

onBeforeUnmount(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
  if (reverseGeoTimeout) clearTimeout(reverseGeoTimeout)
  if (searchDebounceTimeout) clearTimeout(searchDebounceTimeout)
})
</script>

<style>
/* Global Leaflet Marker Styling */
.lumea-map-marker {
  position: relative;
  text-align: center;
}

.marker-pin-bubble {
  width: 32px;
  height: 32px;
  border-radius: 50% 50% 50% 0;
  background: #7A2E22;
  position: absolute;
  transform: rotate(-45deg);
  left: 2px;
  top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(122, 46, 34, 0.4);
  border: 2px solid #FFFFFF;
}

.marker-dot {
  width: 10px;
  height: 10px;
  background: #FFFFFF;
  border-radius: 50%;
  transform: rotate(45deg);
}

.marker-shadow {
  position: absolute;
  bottom: 0;
  left: 6px;
  width: 24px;
  height: 6px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  filter: blur(1px);
}
</style>

<style scoped>
.map-picker-card {
  margin-top: 10px;
  padding: 14px;
  background: #FCFAF8;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
}

.map-picker-card.compact-mode {
  margin-top: 6px;
  padding: 0;
  background: transparent;
  border: none;
}

.map-picker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.map-title {
  display: block;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
}

.map-subtitle {
  display: block;
  font-size: 0.75rem;
  color: #78716C;
  margin-top: 2px;
}

/* Map Toolbar (Search + Paste Gmaps) */
.map-toolbar {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 8px;
  margin-bottom: 0.65rem;
}

@media (max-width: 768px) {
  .map-toolbar {
    grid-template-columns: 1fr;
  }
}

.search-box-wrapper, .gmaps-paste-wrapper {
  position: relative;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 10px;
  font-size: 0.85rem;
  pointer-events: none;
  opacity: 0.75;
}

.map-search-input, .gmaps-paste-input {
  width: 100%;
  padding: 8px 30px 8px 32px;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 0.76rem;
  color: #1C1917;
  transition: border-color 0.2s;
}

.map-search-input:focus, .gmaps-paste-input:focus {
  outline: none;
  border-color: #7A2E22;
  box-shadow: 0 0 0 2px rgba(122, 46, 34, 0.08);
}

.btn-clear-search {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  font-size: 1.1rem;
  color: #A8A29E;
  cursor: pointer;
  line-height: 1;
}

.btn-apply-paste {
  position: absolute;
  right: 4px;
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  padding: 4px 10px;
  border-radius: 5px;
  font-size: 0.7rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-apply-paste:hover {
  opacity: 0.9;
}

/* Search Dropdown */
.search-results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: #FFFFFF;
  border: 1px solid #E7E5E4;
  border-radius: 8px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  max-height: 220px;
  overflow-y: auto;
  list-style: none;
  padding: 4px 0;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: 0.75rem;
  color: #1F2937;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid #F3F4F6;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: #F5EFEB;
  color: #7A2E22;
}

.res-pin {
  font-size: 0.85rem;
  flex-shrink: 0;
}

.res-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Preset Pills */
.preset-pills-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 0.65rem;
  overflow: hidden;
}

.preset-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: #78716C;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.preset-pills-scroll {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 2px;
  scrollbar-width: thin;
}

.preset-pill {
  background: #FFFFFF;
  border: 1px solid #E7E5E4;
  color: #44403C;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.preset-pill:hover {
  border-color: #7A2E22;
  color: #7A2E22;
}

.preset-pill.active {
  background: #7A2E22;
  color: #FFFFFF;
  border-color: #7A2E22;
}

/* Map Canvas Container */
.map-viewport-wrapper {
  position: relative;
  width: 100%;
  height: 190px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #E5E7EB;
}

.compact-mode .map-viewport-wrapper {
  height: 155px;
}

.leaflet-map-canvas {
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* Locate Me Button Floating on Map matching mockup */
.locate-btn-on-map {
  position: absolute;
  bottom: 12px;
  right: 12px;
  top: auto;
  z-index: 500;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  color: #7A2E22;
  font-size: 0.76rem;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 9999px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s ease;
}

.locate-btn-on-map:hover:not(:disabled) {
  background: #FFF8F6;
  border-color: #7A2E22;
  color: #7A2E22;
}

.locate-btn-on-map:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.map-coords-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  border: 1px solid #E7E5E4;
  padding: 2px 7px;
  border-radius: 6px;
  font-size: 0.66rem;
  z-index: 500;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 4px;
  align-items: center;
}

.coords-label {
  font-weight: 700;
  color: #78716C;
}

.coords-val {
  font-family: monospace;
  color: #1C1917;
}

/* Geocoded Address Banner */
.geocoded-address-banner {
  margin-top: 0.65rem;
  padding: 0.6rem 0.8rem;
  background: #F5EFEB;
  border: 1px solid #DECFC4;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.geo-banner-left {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  flex: 1;
}

.geo-icon {
  font-size: 0.95rem;
  line-height: 1.2;
}

.geo-text {
  font-size: 0.74rem;
  color: #44403C;
}

.geo-label {
  display: block;
  font-size: 0.66rem;
  color: #78716C;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 1px;
}

.geo-value {
  color: #7A2E22;
  font-weight: 700;
}

.geo-city {
  color: #57534E;
  font-weight: 600;
}

.btn-apply-to-form {
  background: #7A2E22;
  color: #FFFFFF;
  border: none;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s;
}

.btn-apply-to-form:hover {
  opacity: 0.9;
}

/* Landmark Notes */
.landmark-section {
  margin-top: 0.75rem;
}

.landmark-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 4px;
}

.landmark-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #44403C;
}

.gmaps-preview-link {
  font-size: 0.72rem;
  font-weight: 600;
  color: #7A2E22;
  text-decoration: none;
}

.landmark-input {
  width: 100%;
  padding: 8px 12px;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 0.78rem;
  color: #1C1917;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
