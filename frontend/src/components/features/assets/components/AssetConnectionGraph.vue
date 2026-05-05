<template>
  <div>
    <div class="graph-controls mb-2">
      <Button icon="pi pi-plus" size="small" @click="zoomIn" title="Zoom in" />
      <Button icon="pi pi-minus" size="small" @click="zoomOut" title="Zoom out" />
      <Button icon="pi pi-refresh" size="small" @click="resetView" title="Reset view" />
      <Button icon="pi pi-arrows-alt" size="small" @click="fitToScreen" title="Fit to screen" />
    </div>
    <div ref="networkContainer" style="width: 100%; height: 500px; border: 1px solid #ccc;"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Network } from 'vis-network/standalone/esm/vis-network'
import Button from 'primevue/button'
import api from '@/api/api'

const props = defineProps({
  connections: { type: Array, required: true }
})

const networkContainer = ref(null)
let network = null

function buildGraphData() {
  const nodes = []
  const edges = []
  const nodeIds = new Set()

  props.connections.forEach(conn => {
    if (conn.assetA && !nodeIds.has(conn.assetA.id)) {
      nodes.push({ 
        id: conn.assetA.id, 
        label: conn.assetA.name, 
        shape: 'box', 
        color: '#e3eaff', 
        font: { bold: true } 
      })
      nodeIds.add(conn.assetA.id)
    }
    if (conn.assetB && !nodeIds.has(conn.assetB.id)) {
      nodes.push({ 
        id: conn.assetB.id, 
        label: conn.assetB.name, 
        shape: 'box', 
        color: '#e3eaff', 
        font: { bold: true } 
      })
      nodeIds.add(conn.assetB.id)
    }
    
    if (conn.interfaceA && !nodeIds.has(conn.interfaceA.id)) {
      nodes.push({ 
        id: conn.interfaceA.id, 
        label: conn.interfaceA.name, 
        shape: 'ellipse', 
        color: '#f5f5f5' 
      })
      nodeIds.add(conn.interfaceA.id)
    }
    if (conn.interfaceB && !nodeIds.has(conn.interfaceB.id)) {
      nodes.push({ 
        id: conn.interfaceB.id, 
        label: conn.interfaceB.name, 
        shape: 'ellipse', 
        color: '#f5f5f5' 
      })
      nodeIds.add(conn.interfaceB.id)
    }

    if (conn.assetA && conn.interfaceA) {
      edges.push({ 
        from: conn.assetA.id, 
        to: conn.interfaceA.id, 
        dashes: true, 
        color: { color: '#bbb' } 
      })
    }
    if (conn.assetB && conn.interfaceB) {
      edges.push({ 
        from: conn.assetB.id, 
        to: conn.interfaceB.id, 
        dashes: true, 
        color: { color: '#bbb' } 
      })
    }

    if (conn.interfaceA && conn.interfaceB) {
      edges.push({
        from: conn.interfaceA.id,
        to: conn.interfaceB.id,
        label: conn.connection_type || '',
        arrows: 'to',
        color: { color: '#2196f3' },
        font: { align: 'middle' }
      })
    }
  })

  return { nodes, edges }
}

function renderNetwork() {
  if (!networkContainer.value) return
  const data = buildGraphData()
  const options = {
    layout: {
      hierarchical: false
    },
    nodes: {
      shape: 'dot',
      size: 16,
      font: { size: 14 }
    },
    edges: {
      width: 2,
      color: { color: '#bbb' },
      smooth: {
        type: 'dynamic'
      }
    },
    physics: {
      enabled: true,
      barnesHut: {
        gravitationalConstant: -30000,
        springLength: 120
      }
    },
    interaction: {
      hover: true,
      tooltipDelay: 200,
      zoomView: true,
      dragView: true
    },
    manipulation: {
      enabled: false
    }
  }
  if (network) {
    network.destroy()
  }
  network = new Network(networkContainer.value, data, options)
}

function zoomIn() {
  if (network) {
    const scale = network.getScale()
    network.moveTo({ scale: scale * 1.2 })
  }
}

function zoomOut() {
  if (network) {
    const scale = network.getScale()
    network.moveTo({ scale: scale / 1.2 })
  }
}

function resetView() {
  if (network) {
    network.fit()
  }
}

function fitToScreen() {
  if (network) {
    network.fit()
  }
}

onMounted(() => {
  renderNetwork()
})

watch(() => props.connections, () => {
  renderNetwork()
}, { deep: true })

onBeforeUnmount(() => {
  if (network) network.destroy()
})
</script>

<style scoped>
.graph-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.graph-controls .p-button {
  min-width: 2rem;
  height: 2rem;
}
</style> 