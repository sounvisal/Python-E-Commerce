<template>
  <div class="map-picker-card">
    <div class="map-picker-header">
      <div class="header-left">
        <span class="map-title">📍 Pinpoint Exact Delivery Location</span>
        <span class="map-subtitle">Click map or drag the pin so our delivery courier finds your door accurately</span>
      </div>
      <button
        type="button"
        class="locate-btn"
        :disabled="isLocating"
        @click="locateUser"
        title="Detect your current location via device GPS"
      >
        <span v-if="isLocating" class="locate-spinner"></span>
        <span v-else>📍 Locate Me</span>
      </button>
    </div>

    <!-- Quick Location Presets -->
    <div class="preset-pills-row">
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

    <!-- Map Canvas Container -->
    <div class="map-viewport-wrapper">
      <div ref="mapContainer" class="leaflet-map-canvas"></div>
      <div class="map-coords-badge">
        <span class="coords-label">GPS:</span>
        <span class="coords-val">{{ formattedCoords }}</span>
      </div>
    </div>

    <!-- Landmark Notes & Google Maps Link -->
    <div class="landmark-section">
      <label class="landmark-label" for="driverNotes">
        <span>Delivery Landmark & Driver Instructions (Optional)</span>
        <a
          v-if="selectedLat && selectedLng"
          :href="googleMapsUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="gmaps-preview-link"
        >
          🗺️ Verify in Google Maps ↗
        </a>
      </label>
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
  }
})

const emit = defineEmits(['update:location'])

const mapContainer = ref(null)
let mapInstance = null
let markerInstance = null

const selectedLat = ref(props.initialLat || 11.5564)
const selectedLng = ref(props.initialLng || 104.9282)
const landmarkNotes = ref(props.initialNotes || '')
const isLocating = ref(false)
const currentPreset = ref('BKK1 / Chamkarmon')

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

function emitChanges() {
  emit('update:location', {
    lat: selectedLat.value,
    lng: selectedLng.value,
    notes: landmarkNotes.value,
    map_url: googleMapsUrl.value
  })
}

function updatePin(lat, lng) {
  selectedLat.value = lat
  selectedLng.value = lng
  if (markerInstance) {
    markerInstance.setLatLng([lat, lng])
  }
  emitChanges()
}

function jumpToPreset(preset) {
  currentPreset.value = preset.name
  if (mapInstance) {
    mapInstance.setView([preset.lat, preset.lng], preset.zoom)
    updatePin(preset.lat, preset.lng)
  }
}

function locateUser() {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.')
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
        updatePin(lat, lng)
      }
    },
    (err) => {
      isLocating.value = false
      console.warn('Geolocation error:', err.message)
      alert('Unable to detect location. Please click on the map to set your pin.')
    },
    { enableHighAccuracy: true, timeout: 8000 }
  )
}

onMounted(async () => {
  await nextTick()
  if (!mapContainer.value) return

  // Custom luxury pin marker HTML
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
    updatePin(latlng.lat, latlng.lng)
    currentPreset.value = 'Custom Pin'
  })

  mapInstance.on('click', (e) => {
    updatePin(e.latlng.lat, e.latlng.lng)
    currentPreset.value = 'Custom Pin'
  })

  emitChanges()
})

onBeforeUnmount(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
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
  margin-top: 1.25rem;
  padding: 1.15rem;
  background: #FCFAF8;
  border: 1.5px solid #EAE5DF;
  border-radius: 14px;
}

.map-picker-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.map-title {
  display: block;
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 0.98rem;
  font-weight: 700;
  color: #1C1917;
}

.map-subtitle {
  display: block;
  font-size: 0.78rem;
  color: #78716C;
  margin-top: 0.15rem;
}

.locate-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.85rem;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #1C1917;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.locate-btn:hover:not(:disabled) {
  background: #FAF6F3;
  border-color: #7A2E22;
  color: #7A2E22;
}

.locate-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #E5E0D8;
  border-top-color: #7A2E22;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.preset-pills-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  overflow: hidden;
}

.preset-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #8C827A;
  white-space: nowrap;
}

.preset-pills-scroll {
  display: flex;
  gap: 0.4rem;
  overflow-x: auto;
  padding-bottom: 2px;
  scrollbar-width: thin;
}

.preset-pill {
  padding: 0.25rem 0.65rem;
  background: #FFFFFF;
  border: 1px solid #E5E0D8;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  color: #57534E;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.18s ease;
}

.preset-pill:hover {
  border-color: #CBB4A0;
  color: #1C1917;
}

.preset-pill.active {
  background: #7A2E22;
  border-color: #7A2E22;
  color: #FFFFFF;
}

.map-viewport-wrapper {
  position: relative;
  width: 100%;
  height: 220px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #E2DCD5;
}

.leaflet-map-canvas {
  width: 100%;
  height: 100%;
  z-index: 1;
}

.map-coords-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  z-index: 999;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(4px);
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  font-size: 0.7rem;
  font-family: monospace;
  color: #44403C;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.coords-label {
  font-weight: 700;
  color: #7A2E22;
  margin-right: 0.25rem;
}

.landmark-section {
  margin-top: 0.85rem;
}

.landmark-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #44403C;
  margin-bottom: 0.35rem;
}

.gmaps-preview-link {
  font-size: 0.72rem;
  font-weight: 700;
  color: #7A2E22;
  text-decoration: underline;
  cursor: pointer;
}

.landmark-input {
  width: 100%;
  padding: 0.6rem 0.85rem;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.landmark-input:focus {
  border-color: #7A2E22;
  box-shadow: 0 0 0 3px rgba(122, 46, 34, 0.08);
}
</style>
