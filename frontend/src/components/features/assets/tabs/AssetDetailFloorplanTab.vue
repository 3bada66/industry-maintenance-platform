<!--
  - FloorplanWithMarkers.vue
-->
<template>
  <div class="floorplan-editor">
    <div class="floorplan-controls">
      <div class="control-group">
        <Button 
          icon="pi pi-plus" 
          class="p-button-sm p-button-text"
          @click="zoomIn"
          :title="t('floorplanWithMarkers.zoomIn')"
        />
        <Button 
          icon="pi pi-minus" 
          class="p-button-sm p-button-text"
          @click="zoomOut"
          :title="t('floorplanWithMarkers.zoomOut')"
        />
        <Button 
          icon="pi pi-refresh" 
          class="p-button-sm p-button-text"
          @click="resetView"
          :title="t('floorplanWithMarkers.resetView')"
        />
        <Button 
          icon="pi pi-expand" 
          class="p-button-sm p-button-text"
          @click="fitToView"
          :title="t('floorplanWithMarkers.fitToView')"
        />
        <Button 
          v-if="!readOnly && !isPositioned(marker)"
          icon="pi pi-crosshairs" 
          class="p-button-sm p-button-text"
          @click="zoomToAsset"
          :title="t('floorplanWithMarkers.zoomToAsset')"
        />
        <Button 
          v-if="!readOnly"
          :icon="showGrid ? 'pi pi-th-large' : 'pi pi-th-large'"
          class="p-button-sm p-button-text"
          :class="{ 'p-button-outlined': !showGrid }"
          @click="showGrid = !showGrid"
          :title="showGrid ? t('floorplanWithMarkers.hideGrid') : t('floorplanWithMarkers.showGrid')"
        />
      </div>
      
      <div class="control-group" v-if="!readOnly">
        <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
        <Button 
          icon="pi pi-save" 
          class="p-button-sm p-button-success"
          @click="savePosition"
          :disabled="!hasChanges"
          :title="t('floorplanWithMarkers.savePosition')"
        />
        <span class="position-info" v-if="hasChanges">
          <i class="pi pi-info-circle"></i>
          {{ t('floorplanWithMarkers.positionChanged') }}
        </span>
        <span class="position-info" v-else-if="!isPositioned(marker)">
          <i class="pi pi-map-marker"></i>
          {{ t('floorplanWithMarkers.clickToPosition') }}
        </span>
      </div>
      <div class="control-group" v-else>
        <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
        <span class="position-info">
          <i class="pi pi-eye"></i>
          {{ t('floorplanWithMarkers.viewMode') }}
        </span>
      </div>
    </div>

    <div 
      class="floorplan-container" 
      :class="{ 'read-only': readOnly }"
      ref="container"
      @mousedown="handleMouseDown"
      @wheel="handleWheel"
      @mouseleave="handleMouseLeave"
      @click="handleContainerClick"
      @mousemove="onPan"
      @mouseup="handleMouseUp"
    >
      <div 
        class="floorplan-wrapper"
        :style="wrapperStyle"
        ref="wrapper"
      >
        <img
          v-if="floorplanUrl"
          :src="floorplanUrl"
          alt="Floorplan"
          ref="image"
          @load="onImageLoad"
          class="floorplan-image"
          draggable="false"
          @contextmenu.prevent
        />
        <div v-else-if="loading" class="floorplan-loading">
          <div class="spinner"></div>
          <p>{{ t('common.loading') }}</p>
        </div>
        <div v-else-if="error" class="floorplan-error">
          <p>{{ error }}</p>
        </div>
        <div v-else-if="!hasFloorplan" class="floorplan-no-floorplan">
          <p>{{ t('assetDetail.noFloorplan') }}</p>
        </div>

        <!-- Grid overlay per aiutare il posizionamento -->
        <div 
          v-if="!readOnly && showGrid" 
          class="grid-overlay"
          :style="gridStyle"
        ></div>

        <!-- Indicatore di posizionamento per asset non posizionati -->
        <div
          v-if="!readOnly && !isPositioned(marker) && showPositioningGuide"
          class="positioning-guide"
          :style="positioningGuideStyle"
        >
          <div class="guide-circle"></div>
          <div class="guide-text">{{ t('floorplanWithMarkers.clickHereToPosition') }}</div>
        </div>

        <div
          v-for="marker in otherMarkers"
          :key="marker.id"
          class="marker other-marker"
          :class="{ 'positioned': isPositioned(marker) }"
          :style="getMarkerStyle(marker)"
          @mouseenter="showTooltip(marker, $event)"
          @mouseleave="hideTooltip"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" fill="currentColor" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" fill="white"/>
          </svg>
        </div>

        <div
          v-if="marker.id"
          class="marker editable-marker"
          :class="{ 
            'positioned': isPositioned(marker),
            'unsaved-changes': hasChanges,
            'read-only': readOnly,
            'highlighted': !isPositioned(marker),
            'dragging': isDragging
          }"
          :style="getMarkerStyle(marker)"
          @mousedown.prevent="!readOnly && startDrag($event)"
          @mouseenter="showTooltip(marker, $event)"
          @mouseleave="hideTooltip"
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" fill="currentColor" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="4" fill="white"/>
            <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <!-- Area di drag invisibile più grande -->
          <div class="drag-area"></div>
          <div v-if="hasChanges" class="unsaved-indicator">
            <i class="pi pi-exclamation-triangle"></i>
          </div>
          <div v-if="!isPositioned(marker)" class="positioning-indicator">
            <i class="pi pi-map-marker"></i>
          </div>
        </div>
      </div>
    </div>

    <div 
      v-if="tooltip.visible"
      class="marker-tooltip"
      :style="tooltipStyle"
    >
      <div class="tooltip-header">
        <i class="pi pi-map-marker"></i>
        <span class="tooltip-title">{{ tooltip.data?.name || 'Asset' }}</span>
      </div>
      <div class="tooltip-content">
        <div class="tooltip-row">
          <span class="tooltip-label">{{ t('floorplanWithMarkers.coordinates') }}:</span>
          <span class="tooltip-value">{{ formatCoordinates(tooltip.data) }}</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">{{ t('floorplanWithMarkers.status') }}:</span>
          <span class="tooltip-value" :class="getStatusClass(tooltip.data)">
            {{ getStatusText(tooltip.data) }}
          </span>
        </div>
        <div v-if="tooltip.data?.id === marker.id && hasChanges" class="tooltip-row">
          <span class="tooltip-label">{{ t('floorplanWithMarkers.saveStatus') }}:</span>
          <span class="tooltip-value status-unsaved">
            {{ t('floorplanWithMarkers.unsavedChanges') }}
          </span>
        </div>
      </div>
    </div>

    <div class="floorplan-legend">
      <div class="legend-item">
        <div class="legend-marker editable-marker">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" fill="currentColor" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" fill="white"/>
          </svg>
        </div>
        <span>{{ t('floorplanWithMarkers.currentAsset') }}</span>
      </div>
      <div class="legend-item">
        <div class="legend-marker other-marker">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" fill="currentColor" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="3" fill="white"/>
          </svg>
        </div>
        <span>{{ t('floorplanWithMarkers.otherAssets') }}</span>
      </div>
      <div class="legend-item">
        <div class="legend-marker unpositioned">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="8" fill="currentColor" stroke="white" stroke-width="2" stroke-dasharray="4"/>
            <circle cx="12" cy="12" r="3" fill="white"/>
          </svg>
        </div>
        <span>{{ t('floorplanWithMarkers.unpositioned') }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import api from '@/api/api'

const { t } = useI18n()
const toast = useToast()

const props = defineProps({
  assetId: {
    type: [String, Number],
    required: true
  },
  readOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['position-saved'])

// Stato asset e floorplan
const asset = ref(null)
const loading = ref(false)
const error = ref(null)

        // Current marker (selected asset)
const marker = reactive({
  id: null,
  x: 0,
  y: 0,
  name: '',
  originalX: 0,
  originalY: 0
})

// Computed per floorplan
const floorplanUrl = computed(() => {
  if (!asset.value?.location?.floorplan?.id || !asset.value?.location?.id) return ''
  const baseUrl = '/api'
  return `${baseUrl}/locations/${asset.value.location.id}/floorplan/${asset.value.location.floorplan.id}`
})

const hasFloorplan = computed(() => !!asset.value?.location?.floorplan?.id)

// Marker degli altri asset (placeholder, da implementare se serve)
const otherMarkers = computed(() => [])

const hasChanges = computed(() => {
  const tolerance = 0.001
  return (
    Math.abs(marker.x - marker.originalX) > tolerance ||
    Math.abs(marker.y - marker.originalY) > tolerance
  )
})

// Computed properties
const zoom = ref(1)
const pan = reactive({ x: 0, y: 0 })
const imageSize = reactive({ width: 0, height: 0 })
const isDragging = ref(false)
const isPanning = ref(false)
const lastPanPoint = reactive({ x: 0, y: 0 })

// Nuove variabili per le funzionalità migliorate
const showGrid = ref(false)
const showPositioningGuide = ref(false)
const containerSize = reactive({ width: 0, height: 0 })

// Variabili per long press
const longPressTimer = ref(null)
const longPressDelay = 500 // 500ms per long press
const isLongPressing = ref(false)

// Template refs
const container = ref(null)
const image = ref(null)
const wrapper = ref(null)

const tooltip = reactive({
  visible: false,
  data: null,
  x: 0,
  y: 0
})

const wrapperStyle = computed(() => ({
  transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom.value})`,
  transformOrigin: '0 0'
}))

const tooltipStyle = computed(() => ({
  left: `${tooltip.x}px`,
  top: `${tooltip.y}px`
}))

// Computed per il grid overlay
const gridStyle = computed(() => ({
  position: 'absolute',
  top: 0,
  left: 0,
  width: `${imageSize.width}px`,
  height: `${imageSize.height}px`,
  backgroundImage: `
    linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px)
  `,
  backgroundSize: '50px 50px',
  pointerEvents: 'none',
  zIndex: 5
}))

// Computed per la guida di posizionamento
const positioningGuideStyle = computed(() => {
  if (!imageSize.width || !imageSize.height) return {}
  
  const centerX = imageSize.width * 0.5
  const centerY = imageSize.height * 0.5
  
  return {
    position: 'absolute',
    left: `${centerX}px`,
    top: `${centerY}px`,
    transform: 'translate(-50%, -50%)',
    zIndex: 15
  }
})

// Fetch asset
async function loadAsset() {
  loading.value = true
  error.value = null
  try {
    const response = await api.getAsset(props.assetId)
    asset.value = response.data
    // Inizializza marker
    marker.id = asset.value.id
    marker.x = asset.value.map_x || 0
    marker.y = asset.value.map_y || 0
    marker.name = asset.value.name
    marker.originalX = marker.x
    marker.originalY = marker.y
  } catch (err) {
            error.value = err.response?.data?.message || 'Error loading asset'
  } finally {
    loading.value = false
  }
}

onMounted(loadAsset)
watch(() => props.assetId, loadAsset)

// Salva posizione
async function savePosition() {
  if (!hasChanges.value) return
  try {
    await api.updatePosition(marker.id, { map_x: marker.x, map_y: marker.y })
    marker.originalX = marker.x
    marker.originalY = marker.y
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assetDetail.positionSaved') })
    emit('position-saved', { id: marker.id, map_x: marker.x, map_y: marker.y })
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assetDetail.positionSaveError') })
  }
}

const updateImageSize = () => {
  if (image.value) {
    imageSize.width = image.value.naturalWidth
    imageSize.height = image.value.naturalHeight
  }
}

const updateContainerSize = () => {
  if (container.value) {
    containerSize.width = container.value.clientWidth
    containerSize.height = container.value.clientHeight
  }
}

const onImageLoad = () => {
  updateImageSize()
  updateContainerSize()
  
  // Auto-fit immediato per tutte le mappe
  nextTick(() => {
    fitToView()
    
    // Mostra la guida di posizionamento solo per asset non posizionati
    if (!isPositioned(marker)) {
      showPositioningGuide.value = true
    } else {
      // Per asset già posizionati, zoom alla posizione dopo un breve delay
      setTimeout(() => {
        zoomToAsset()
      }, 500)
    }
  })
}

const zoomIn = () => {
  zoom.value = Math.min(zoom.value * 1.2, 5)
}

const zoomOut = () => {
  zoom.value = Math.max(zoom.value / 1.2, 0.1)
}

const resetView = () => {
  zoom.value = 1
  pan.x = 0
  pan.y = 0
}

const handleWheel = (event) => {
  event.preventDefault()
  const delta = event.deltaY > 0 ? 0.9 : 1.1
  zoom.value = Math.max(0.1, Math.min(5, zoom.value * delta))
}

const startPan = (event) => {
  if (event.target === container.value) {
    isPanning.value = true
    lastPanPoint.x = event.clientX
    lastPanPoint.y = event.clientY
    // Cancella long press se inizia il pan
    cancelLongPress()
  }
}

// Nuovi metodi combinati per gestire gli eventi del mouse
const handleMouseDown = (event) => {
  if (event.target === container.value) {
    // Inizia il long press timer
    startLongPress(event)
    
    // Inizia il pan solo se non è un long press
    const panTimer = setTimeout(() => {
      if (!isLongPressing.value) {
        startPan(event)
      }
    }, 100) // Piccolo delay per distinguere tra click e pan
    
    // Salva il timer per cancellarlo se necessario
    event.panTimer = panTimer
  }
}

const handleMouseUp = (event) => {
  // Cancella il timer del pan se esiste
  if (event.panTimer) {
    clearTimeout(event.panTimer)
  }
  
  stopPan()
  cancelLongPress()
}

const handleMouseLeave = (event) => {
  // Cancella il timer del pan se esiste
  if (event.panTimer) {
    clearTimeout(event.panTimer)
  }
  
  stopPan()
  cancelLongPress()
}

const onPan = (event) => {
  if (!isPanning.value) return
  
  // Se inizia il pan, cancella il long press
  if (!isLongPressing.value) {
    cancelLongPress()
  }
  
  const deltaX = event.clientX - lastPanPoint.x
  const deltaY = event.clientY - lastPanPoint.y
  
  pan.x += deltaX
  pan.y += deltaY
  
  lastPanPoint.x = event.clientX
  lastPanPoint.y = event.clientY
}

const stopPan = () => {
  isPanning.value = false
  // Cancella long press quando si rilascia il mouse
  cancelLongPress()
}

const handleContainerClick = (event) => {
  if (isDragging.value || isPanning.value || isLongPressing.value) return
  if (readOnly.value) return

  // Calcolo corretto delle coordinate considerando zoom e pan
  const rect = container.value.getBoundingClientRect()
  const x = (event.clientX - rect.left - pan.x) / zoom.value
  const y = (event.clientY - rect.top - pan.y) / zoom.value

  // Converti in coordinate relative (0-1)
  const relativeX = Math.min(Math.max(x / imageSize.width, 0), 1)
  const relativeY = Math.min(Math.max(y / imageSize.height, 0), 1)

  marker.x = relativeX
  marker.y = relativeY
}

// Nuovo metodo per long press
const startLongPress = (event) => {
  if (readOnly.value) return
  
  // Aggiungi classe CSS per feedback visivo
  if (container.value) {
    container.value.classList.add('long-pressing')
  }
  
  longPressTimer.value = setTimeout(() => {
    isLongPressing.value = true
    handleLongPress(event)
    
    // Rimuovi classe CSS
    if (container.value) {
      container.value.classList.remove('long-pressing')
    }
  }, longPressDelay)
}

const handleLongPress = (event) => {
  if (readOnly.value) return

  // Calcolo corretto delle coordinate per long press
  const rect = container.value.getBoundingClientRect()
  const x = (event.clientX - rect.left - pan.x) / zoom.value
  const y = (event.clientY - rect.top - pan.y) / zoom.value

  // Converti in coordinate relative (0-1)
  const relativeX = Math.min(Math.max(x / imageSize.width, 0), 1)
  const relativeY = Math.min(Math.max(y / imageSize.height, 0), 1)

  marker.x = relativeX
  marker.y = relativeY
  
  // Feedback visivo
  toast.add({ 
    severity: 'success', 
    summary: t('floorplanWithMarkers.positioned'), 
    detail: t('floorplanWithMarkers.longPressPositioned'),
    life: 2000
  })
}

const cancelLongPress = () => {
  if (longPressTimer.value) {
    clearTimeout(longPressTimer.value)
    longPressTimer.value = null
  }
  isLongPressing.value = false
  
  // Rimuovi classe CSS
  if (container.value) {
    container.value.classList.remove('long-pressing')
  }
}

const fitToView = () => {
  if (!imageSize.width || !imageSize.height || !container.value) return
  
  const containerRect = container.value.getBoundingClientRect()
  
  // Calcolo del fattore di scala per adattare l'immagine al container
  const scaleX = containerRect.width / imageSize.width
  const scaleY = containerRect.height / imageSize.height
  
  // Usa il fattore più piccolo per mantenere le proporzioni
  const newZoom = Math.min(scaleX, scaleY) * 0.9 // 90% per un po' di margine
  
  zoom.value = newZoom
  
  // Centra l'immagine
  pan.x = (containerRect.width - imageSize.width * newZoom) / 2
  pan.y = (containerRect.height - imageSize.height * newZoom) / 2
}

const zoomToAsset = () => {
  if (!isPositioned(marker) || !container.value) {
    toast.add({ severity: 'info', summary: t('floorplanWithMarkers.info'), detail: t('floorplanWithMarkers.assetNotPositioned') })
    return
  }
  
  const containerRect = container.value.getBoundingClientRect()
  
  // Zoom per mostrare l'asset con un po' di contesto
  const newZoom = Math.min(2, Math.max(0.5, zoom.value))
  zoom.value = newZoom
  
  // Posiziona l'asset al centro
  const assetX = marker.x * imageSize.width * newZoom
  const assetY = marker.y * imageSize.height * newZoom
  
  pan.x = containerRect.width / 2 - assetX
  pan.y = containerRect.height / 2 - assetY
}

const getMarkerStyle = (marker) => {
  if (!imageSize.width || !imageSize.height) return {}

  const isUnpositioned = !isPositioned(marker)
  const posX = isUnpositioned ? 0.5 : marker.x
  const posY = isUnpositioned ? 0.5 : marker.y

  return {
    position: 'absolute',
    left: `${posX * imageSize.width}px`,
    top: `${posY * imageSize.height}px`,
    userSelect: 'none',
    transform: 'translate(-50%, -50%)'
  }
}

const isPositioned = (marker) => {
  return marker.x !== null && marker.y !== null && 
         !(marker.x === 0 && marker.y === 0)
}

const startDrag = (event) => {
  if (isPanning.value) return
  
  isDragging.value = true
  window.addEventListener('mousemove', onDrag)
  window.addEventListener('mouseup', stopDrag)
}

const onDrag = (event) => {
  if (!isDragging.value || !image.value) return

  // Calcolo corretto delle coordinate considerando zoom e pan
  const rect = image.value.getBoundingClientRect()
  const x = (event.clientX - rect.left - pan.x) / zoom.value
  const y = (event.clientY - rect.top - pan.y) / zoom.value

  // Converti in coordinate relative (0-1)
  const relativeX = Math.min(Math.max(x / imageSize.width, 0), 1)
  const relativeY = Math.min(Math.max(y / imageSize.height, 0), 1)

  marker.x = relativeX
  marker.y = relativeY
}

const stopDrag = () => {
  isDragging.value = false
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', stopDrag)
}

const showTooltip = (marker, event) => {
  tooltip.data = marker
  tooltip.x = event.clientX + 10
  tooltip.y = event.clientY - 10
  tooltip.visible = true
}

const hideTooltip = () => {
  tooltip.visible = false
}

const formatCoordinates = (marker) => {
  if (!isPositioned(marker)) return t('floorplanWithMarkers.notPositioned')
  return `X: ${Math.round(marker.x * 100)}%, Y: ${Math.round(marker.y * 100)}%`
}

const getStatusText = (marker) => {
  return isPositioned(marker) 
    ? t('floorplanWithMarkers.positioned') 
    : t('floorplanWithMarkers.notPositioned')
}

const getStatusClass = (marker) => {
  return isPositioned(marker) ? 'status-positioned' : 'status-unpositioned'
}
</script>

<style scoped>
.floorplan-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.floorplan-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e9ecef;
  gap: 16px;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.zoom-level {
  font-size: 14px;
  font-weight: 500;
  color: #495057;
  min-width: 50px;
  text-align: center;
}

.position-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #dc3545;
  font-weight: 500;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.floorplan-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #f8f9fa;
  cursor: grab;
  user-select: none;
}

.floorplan-container:active {
  cursor: grabbing;
}

.floorplan-container:not(.read-only) {
  cursor: crosshair;
}

.floorplan-container.read-only {
  cursor: default;
}

.floorplan-container.read-only .floorplan-image {
  cursor: default;
}

.floorplan-container.long-pressing {
  cursor: wait;
}

.floorplan-container.long-pressing::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 123, 255, 0.1);
  pointer-events: none;
  z-index: 100;
  animation: longPressPulse 0.5s ease-in-out;
}

@keyframes longPressPulse {
  0% { opacity: 0; }
  50% { opacity: 0.3; }
  100% { opacity: 0; }
}

.floorplan-wrapper {
  position: relative;
  display: inline-block;
  transition: transform 0.1s ease-out;
}

.floorplan-image {
  display: block;
  max-width: none;
  user-select: none;
  pointer-events: none;
  cursor: default;
}

.marker {
  position: absolute;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
}

.marker:hover {
  transform: translate(-50%, -50%) scale(1.2);
  z-index: 20;
}

.marker svg {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.other-marker {
  color: #6c757d;
}

.other-marker:hover {
  color: #495057;
}

.editable-marker {
  color: #007bff;
}

.editable-marker:hover {
  color: #0056b3;
}

.editable-marker.positioned {
  color: #28a745;
}

.editable-marker.unsaved-changes {
  color: #ffc107;
  animation: pulse 2s infinite;
}

.editable-marker.read-only {
  color: #6c757d;
  cursor: default;
}

.editable-marker.read-only:hover {
  transform: none;
  color: #6c757d;
}

.editable-marker.highlighted {
  animation: pulse-highlight 2s infinite;
  color: #dc3545;
}

.editable-marker.dragging {
  cursor: grabbing !important;
  transform: translate(-50%, -50%) scale(1.3);
  z-index: 30;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
}

.drag-area {
  position: absolute;
  top: -20px;
  left: -20px;
  width: 68px;
  height: 68px;
  background: transparent;
  cursor: grab;
  z-index: 5;
}

.drag-area:hover {
  background: rgba(0, 123, 255, 0.1);
  border-radius: 50%;
}

@keyframes pulse-highlight {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.3); }
  100% { transform: translate(-50%, -50%) scale(1); }
}

.positioning-indicator {
  position: absolute;
  top: -12px;
  right: -12px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  animation: pulse 1s infinite;
}

.positioning-guide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  pointer-events: none;
}

.guide-circle {
  width: 60px;
  height: 60px;
  border: 3px dashed #dc3545;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.guide-text {
  background: rgba(220, 53, 69, 0.9);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.other-marker.positioned {
  color: #17a2b8;
}

.unpositioned {
  color: #dc3545;
  opacity: 0.7;
}

.unsaved-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #dc3545;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 8px;
  animation: pulse 1s infinite;
}

/* Tooltip */
.marker-tooltip {
  position: fixed;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 12px;
  font-size: 14px;
  z-index: 1000;
  max-width: 250px;
  pointer-events: none;
}

.tooltip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #495057;
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tooltip-label {
  color: #6c757d;
  font-size: 12px;
}

.tooltip-value {
  font-weight: 500;
  color: #495057;
}

.status-positioned {
  color: #28a745;
}

.status-unpositioned {
  color: #dc3545;
}

.status-unsaved {
  color: #ffc107;
  font-weight: 600;
}

/* Legenda */
.floorplan-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e9ecef;
  font-size: 12px;
  color: #6c757d;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-marker {
  display: flex;
  align-items: center;
  justify-content: center;
}

.legend-marker.other-marker {
  color: #6c757d;
}

.legend-marker.editable-marker {
  color: #007bff;
}

.legend-marker.unpositioned {
  color: #dc3545;
}

/* Responsive */
@media (max-width: 768px) {
  .floorplan-controls {
    flex-direction: column;
    gap: 12px;
  }
  
  .floorplan-legend {
    flex-wrap: wrap;
    gap: 16px;
  }
}
</style>
