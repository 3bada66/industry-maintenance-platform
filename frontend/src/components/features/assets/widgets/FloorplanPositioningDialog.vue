<template>
  <Dialog 
    :visible="visible" 
    @update:visible="$emit('update:visible', $event)"
    :header="t('locations.floorplan.title')"
    modal 
    :style="{ width: '95vw', height: '90vh', maxWidth: 'none' }"
    :closable="true"
    :dismissableMask="false"
    class="floorplan-positioning-dialog"
  >
    <div class="floorplan-positioning-container">
      <!-- Toolbar superiore -->
      <div class="positioning-toolbar">
        <div class="toolbar-left">
          <Button 
            icon="pi pi-plus" 
            class="p-button-sm p-button-text"
            @click="zoomIn"
            :title="t('locations.floorplan.zoomIn')"
          />
          <Button 
            icon="pi pi-minus" 
            class="p-button-sm p-button-text"
            @click="zoomOut"
            :title="t('locations.floorplan.zoomOut')"
          />
          <Button 
            icon="pi pi-refresh" 
            class="p-button-sm p-button-text"
            @click="resetView"
            :title="t('locations.floorplan.resetView')"
          />
          <Button 
            icon="pi pi-expand" 
            class="p-button-sm p-button-text"
            @click="fitToView"
            :title="t('locations.floorplan.fitToView')"
          />
          <span class="zoom-level">{{ Math.round(zoom * 100) }}%</span>
        </div>
        
        <div class="toolbar-center">
          <span class="asset-name">{{ asset?.name || '' }}</span>
          <Tag 
            v-if="asset?.status?.name"
            :value="asset.status.name" 
            :severity="getStatusSeverity(asset.status)"
          />
        </div>
        
        <div class="toolbar-right">
          <Button 
            v-if="isPositioned(marker)"
            icon="pi pi-save" 
            class="p-button-sm p-button-success"
            @click="savePosition"
            :title="t('locations.floorplan.savePosition')"
          />
          <Button 
            icon="pi pi-times" 
            class="p-button-sm p-button-secondary"
            @click="close"
            :title="t('locations.floorplan.close')"
          />
        </div>
      </div>

      <!-- Container principale per la planimetria -->
      <div 
        class="floorplan-canvas-container"
        ref="canvasContainer"
        @wheel="handleWheel"
        @click="handleCanvasClick"
      >
        <div 
          class="floorplan-canvas"
          :style="canvasStyle"
          ref="canvas"
        >
          <!-- Immagine della planimetria -->
          <img
            v-if="floorplanUrl && hasFloorplan"
            :src="floorplanUrl"
            alt="Floorplan"
            ref="floorplanImage"
            @load="onImageLoad"
            class="floorplan-image"
            draggable="false"
            @contextmenu.prevent
          />
          
          <!-- Messaggio se non c'è planimetria -->
          <div v-else-if="!hasFloorplan" class="no-floorplan-message">
            <i class="pi pi-image" style="font-size: 3rem; color: var(--text-color-secondary);"></i>
            <p>{{ t('locations.floorplan.noFloorplan') }}</p>
          </div>
          
          <!-- Grid overlay -->
          <div 
            v-if="showGrid"
            class="grid-overlay"
            :style="gridStyle"
          ></div>
          
          <!-- Marker dell'asset corrente -->
          <div 
            v-if="isPositioned(marker)"
            class="asset-marker current-asset"
            :style="getMarkerStyle(marker)"
            @mousedown="startMarkerDrag"
            @click.stop="selectMarker(marker)"
            draggable="false"
          >
            <div class="marker-icon">
              <i class="pi pi-map-marker"></i>
            </div>
            <div class="marker-label">{{ marker.name }}</div>
          </div>
          
          <!-- Marker temporaneo per il drag -->
          <div 
            v-if="isDraggingMarker"
            class="asset-marker current-asset dragging"
            :style="getMarkerStyle(dragMarker)"
          >
            <div class="marker-icon">
              <i class="pi pi-map-marker"></i>
            </div>
            <div class="marker-label">{{ marker.name }}</div>
          </div>
          
          <!-- Altri marker (placeholder per future implementazioni) -->
          <div 
            v-for="otherMarker in otherMarkers" 
            :key="otherMarker.id"
            class="asset-marker other-asset"
            :style="getMarkerStyle(otherMarker)"
            @click.stop="selectMarker(otherMarker)"
          >
            <div class="marker-icon">
              <i class="pi pi-circle"></i>
            </div>
            <div class="marker-label">{{ otherMarker.name }}</div>
          </div>
          
          <!-- Guida di posizionamento -->
          <div 
            v-if="showPositioningGuide && !isPositioned(marker)"
            class="positioning-guide"
            :style="positioningGuideStyle"
          >
            <div class="guide-circle"></div>
            <div class="guide-text">{{ t('locations.floorplan.clickToPosition') }}</div>
          </div>
        </div>
      </div>

      <!-- Pannello informazioni -->
      <div class="info-panel">
        <div class="info-section">
          <h4>{{ t('locations.floorplan.instructions') }}</h4>
          <ul>
            <li>{{ t('locations.floorplan.instruction1') }}</li>
            <li>{{ t('locations.floorplan.instruction2') }}</li>
            <li>{{ t('locations.floorplan.instruction3') }}</li>
            <li v-if="isPositioned(marker)">{{ t('locations.floorplan.instruction4') }}</li>
          </ul>
        </div>
        
        <div class="info-section">
          <h4>{{ t('locations.floorplan.status') }}</h4>
          <div class="status-display">
            <span v-if="hasChanges" class="status-changed">
              <i class="pi pi-exclamation-triangle"></i>
              {{ t('locations.floorplan.changesPending') }}
            </span>
            <span v-else-if="isPositioned(marker)" class="status-saved">
              <i class="pi pi-check-circle"></i>
              {{ t('locations.floorplan.positionSaved') }}
            </span>
            <span v-else class="status-not-positioned">
              <i class="pi pi-map-marker"></i>
              {{ t('locations.floorplan.notPositioned') }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import api from '@/api/api'
import { useStatus } from '@/composables/useStatus'

const { t } = useI18n()
const toast = useToast()
const { getStatusSeverity } = useStatus()

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  assetId: {
    type: [String, Number],
    required: true
  },
  locationId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:visible', 'position-saved'])

// Template refs
const canvasContainer = ref(null)
const canvas = ref(null)
const floorplanImage = ref(null)

// Stato principale
const asset = ref(null)
const loading = ref(false)
const error = ref(null)

// Stato del marker
const marker = reactive({
  id: null,
  x: 0,
  y: 0,
  name: '',
  originalX: 0,
  originalY: 0
})

// Stato del canvas
const zoom = ref(1)
const pan = reactive({ x: 0, y: 0 })
const imageSize = reactive({ width: 0, height: 0 })
const containerSize = reactive({ width: 0, height: 0 })

// Stato dell'interazione
const isDragging = ref(false)
const isPanning = ref(false)
const isDraggingMarker = ref(false)
const lastPanPoint = reactive({ x: 0, y: 0 })
const dragMarker = reactive({ x: 0, y: 0 })
const showGrid = ref(true)
const showPositioningGuide = ref(false)

// Computed properties
const floorplanUrl = computed(() => {
  if (!asset.value?.location?.floorplan?.id || !asset.value?.location?.id) return ''
  const baseUrl = '/api'
  return `${baseUrl}/locations/${asset.value.location.id}/floorplan/${asset.value.location.floorplan.id}`
})

const hasFloorplan = computed(() => !!asset.value?.location?.floorplan?.id)

const canvasStyle = computed(() => ({
  transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom.value})`,
  transformOrigin: '0 0'
}))

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

const hasChanges = computed(() => {
  const tolerance = 0.001
  return (
    Math.abs(marker.x - marker.originalX) > tolerance ||
    Math.abs(marker.y - marker.originalY) > tolerance
  )
})

const otherMarkers = computed(() => [])

// Methods
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

function isPositioned(marker) {
  return marker.x !== 0 || marker.y !== 0
}

function getMarkerStyle(marker) {
  return {
    position: 'absolute',
    left: `${marker.x}px`,
    top: `${marker.y}px`,
    transform: 'translate(-50%, -50%)',
    zIndex: 10
  }
}



// Zoom e pan
function zoomIn() {
  zoom.value = Math.min(zoom.value * 1.2, 5)
}

function zoomOut() {
  zoom.value = Math.max(zoom.value / 1.2, 0.1)
}

function resetView() {
  zoom.value = 1
  pan.x = 0
  pan.y = 0
}

function fitToView() {
  if (!imageSize.width || !imageSize.height || !containerSize.width || !containerSize.height) return
  
  const scaleX = containerSize.width / imageSize.width
  const scaleY = containerSize.height / imageSize.height
  const scale = Math.min(scaleX, scaleY, 1) * 0.9 // 90% per un po' di margine
  
  zoom.value = scale
  pan.x = (containerSize.width - imageSize.width * scale) / 2
  pan.y = (containerSize.height - imageSize.height * scale) / 2
}

// Event handlers per il drag del marker
function startMarkerDrag(event) {
  if (!isPositioned(marker)) return
  
  event.preventDefault()
  event.stopPropagation()
  
  isDraggingMarker.value = true
  dragMarker.x = marker.x
  dragMarker.y = marker.y
  
  // Nascondi il marker originale durante il drag
  document.addEventListener('mousemove', handleMarkerDrag)
  document.addEventListener('mouseup', stopMarkerDrag)
}

function handleMarkerDrag(event) {
  if (!isDraggingMarker.value) return
  
  const rect = canvasContainer.value.getBoundingClientRect()
  const clickX = (event.clientX - rect.left - pan.x) / zoom.value
  const clickY = (event.clientY - rect.top - pan.y) / zoom.value
  
  // Verifica che il drag sia dentro l'immagine
  if (clickX >= 0 && clickX <= imageSize.width && 
      clickY >= 0 && clickY <= imageSize.height) {
    dragMarker.x = clickX
    dragMarker.y = clickY
  }
}

function stopMarkerDrag() {
  if (isDraggingMarker.value) {
    // Aggiorna la posizione del marker
    marker.x = dragMarker.x
    marker.y = dragMarker.y
    
    isDraggingMarker.value = false
    
    // Rimuovi gli event listeners
    document.removeEventListener('mousemove', handleMarkerDrag)
    document.removeEventListener('mouseup', stopMarkerDrag)
  }
}

function handleWheel(event) {
  event.preventDefault()
  
  const delta = event.deltaY > 0 ? 0.9 : 1.1
  const newZoom = Math.max(0.1, Math.min(5, zoom.value * delta))
  
  // Zoom towards mouse position
  const rect = canvasContainer.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top
  
  const scaleChange = newZoom / zoom.value
  
  pan.x = mouseX - (mouseX - pan.x) * scaleChange
  pan.y = mouseY - (mouseY - pan.y) * scaleChange
  
  zoom.value = newZoom
}

function handleCanvasClick(event) {
  if (isPanning.value) return
  
  const rect = canvasContainer.value.getBoundingClientRect()
  const clickX = (event.clientX - rect.left - pan.x) / zoom.value
  const clickY = (event.clientY - rect.top - pan.y) / zoom.value
  
  // Verifica che il click sia dentro l'immagine
  if (clickX >= 0 && clickX <= imageSize.width && 
      clickY >= 0 && clickY <= imageSize.height) {
    marker.x = clickX
    marker.y = clickY
  }
}

function selectMarker(marker) {
  // Focus sul marker selezionato
  const markerElement = event.target.closest('.asset-marker')
  if (markerElement) {
    markerElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

async function savePosition() {
  if (!hasChanges.value) return
  
  try {
    await api.updatePosition(marker.id, { map_x: marker.x, map_y: marker.y })
    marker.originalX = marker.x
    marker.originalY = marker.y
    
    toast.add({ 
      severity: 'success', 
      summary: t('common.messages.success'), 
      detail: t('locations.floorplan.positionSaved'), 
      life: 3000 
    })
    
    emit('position-saved', { id: marker.id, map_x: marker.x, map_y: marker.y })
  } catch (err) {
    toast.add({ 
      severity: 'error', 
      summary: t('common.messages.error'), 
      detail: t('locations.floorplan.saveError'), 
      life: 3000 
    })
  }
}

function close() {
  if (hasChanges.value) {
    // Chiedi conferma se ci sono modifiche non salvate
    if (confirm(t('locations.floorplan.confirmClose'))) {
      emit('update:visible', false)
    }
  } else {
    emit('update:visible', false)
  }
}

// Lifecycle
function updateImageSize() {
  if (floorplanImage.value) {
    imageSize.width = floorplanImage.value.naturalWidth
    imageSize.height = floorplanImage.value.naturalHeight
  }
}

function updateContainerSize() {
  if (canvasContainer.value) {
    containerSize.width = canvasContainer.value.clientWidth
    containerSize.height = canvasContainer.value.clientHeight
  }
}

function onImageLoad() {
  if (!floorplanImage.value) return
  
  updateImageSize()
  updateContainerSize()
  
  nextTick(() => {
    fitToView()
    
    if (!isPositioned(marker)) {
      showPositioningGuide.value = true
    }
  })
}

// Watchers
watch(() => props.visible, (newVisible) => {
  if (newVisible) {
    loadAsset()
  }
})

watch(() => props.assetId, () => {
  if (props.visible) {
    loadAsset()
  }
})

// Keyboard shortcuts
function handleKeydown(event) {
  if (!props.visible) return
  
  switch (event.key) {
    case '+':
    case '=':
      event.preventDefault()
      zoomIn()
      break
    case '-':
      event.preventDefault()
      zoomOut()
      break
    case '0':
      event.preventDefault()
      resetView()
      break
    case 'f':
      event.preventDefault()
      fitToView()
      break
    case 'Escape':
      close()
      break
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('mousemove', handleMarkerDrag)
  document.removeEventListener('mouseup', stopMarkerDrag)
})
</script>

<style scoped>
.floorplan-positioning-dialog {
  --toolbar-height: 60px;
  --info-panel-width: 300px;
}

.floorplan-positioning-container {
  display: flex;
  flex-direction: column;
  height: calc(90vh - 120px);
  gap: 0;
  position: relative;
}

.positioning-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: var(--surface-card);
  border-bottom: 1px solid var(--surface-border);
  height: var(--toolbar-height);
  flex-shrink: 0;
  z-index: 30;
  position: relative;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.toolbar-center {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.asset-name {
  font-weight: 600;
  color: var(--text-color);
}

.zoom-level {
  font-family: monospace;
  font-weight: 600;
  color: var(--text-color-secondary);
  min-width: 50px;
  text-align: center;
}

.floorplan-canvas-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: var(--surface-ground);
  cursor: default;
}

.floorplan-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.floorplan-image {
  max-width: none;
  display: block;
}

.no-floorplan-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-color-secondary);
  text-align: center;
}

.no-floorplan-message p {
  margin-top: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.grid-overlay {
  pointer-events: none;
}

.asset-marker {
  position: absolute;
  cursor: grab;
  transition: all 0.2s ease;
  z-index: 20;
}

.asset-marker:hover {
  transform: translate(-50%, -50%) scale(1.1);
}

.asset-marker:active {
  cursor: grabbing;
}

.current-asset {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  padding: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid var(--primary-color);
}

.current-asset .marker-icon {
  color: var(--primary-color);
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.current-asset.dragging .marker-icon {
  color: var(--primary-color);
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  opacity: 0.8;
}

.other-asset .marker-icon {
  color: var(--text-color-secondary);
  font-size: 1.2rem;
}

.marker-label {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface-card);
  color: var(--text-color);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.asset-marker:hover .marker-label {
  opacity: 1;
}

.positioning-guide {
  pointer-events: none;
}

.guide-circle {
  width: 60px;
  height: 60px;
  border: 3px dashed var(--primary-color);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.guide-text {
  margin-top: 0.5rem;
  text-align: center;
  color: var(--primary-color);
  font-weight: 600;
  font-size: 0.875rem;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

.info-panel {
  position: absolute;
  top: calc(var(--toolbar-height) + 50px);
  right: 0;
  width: var(--info-panel-width);
  height: calc(100% - var(--toolbar-height) - 50px);
  background: var(--surface-card);
  border-left: 1px solid var(--surface-border);
  padding: 1rem;
  overflow-y: auto;
  z-index: 10;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
}

.info-section {
  margin-bottom: 1rem;
}

.info-section h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text-color);
  font-size: 0.875rem;
  font-weight: 600;
}

.info-section ul {
  margin: 0;
  padding-left: 1rem;
  font-size: 0.8rem;
  color: var(--text-color-secondary);
}

.info-section li {
  margin-bottom: 0.25rem;
}



.status-display {
  font-size: 0.875rem;
}

.status-display span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.status-changed {
  color: var(--orange-600);
  background: var(--orange-50);
}

.status-saved {
  color: var(--green-600);
  background: var(--green-50);
}

.status-not-positioned {
  color: var(--blue-600);
  background: var(--blue-50);
}

/* Responsive */
@media (max-width: 1200px) {
  .info-panel {
    position: relative;
    width: 100%;
    height: auto;
    border-left: none;
    border-top: 1px solid var(--surface-border);
    padding-top: 1rem;
  }
  
  .floorplan-positioning-container {
    height: auto;
  }
  
  .floorplan-canvas-container {
    height: 60vh;
  }
}
</style> 