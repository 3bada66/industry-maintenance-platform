<template>
  <div>
    <h2>{{ t('assets.communications.title') }}</h2>
    <AssetCommunicationGraph :nodes="communicationsNodes" :edges="communicationsEdges" />
    <AssetCommunicationTable :rows="communications" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import AssetCommunicationGraph from '../components/AssetCommunicationGraph.vue'
import AssetCommunicationTable from '@/components/tables/AssetCommunicationTable.vue'
import api from '@/api/api'

const props = defineProps({
  assetId: { type: [String, Number], required: true }
})

const { t } = useI18n()
const toast = useToast()

// Stato
const communications = ref([])
const communicationsNodes = ref([])
const communicationsEdges = ref([])

// Funzioni
function buildCommunicationGraphData(communications) {
  const nodesMap = new Map()
  const edges = []
  communications.forEach(comm => {
    // Nodo sorgente
    if (comm.src_asset) {
      nodesMap.set(comm.src_asset.id, { id: comm.src_asset.id, label: comm.src_asset.name })
    }
    // Nodo destinazione
    if (comm.dst_asset) {
      nodesMap.set(comm.dst_asset.id, { id: comm.dst_asset.id, label: comm.dst_asset.name })
    }
    // Arco
    if (comm.src_asset && comm.dst_asset) {
      edges.push({
        from: comm.src_asset.id,
        to: comm.dst_asset.id,
        label: `${comm.packet_count} pkt`,
        value: comm.packet_count
      })
    }
  })
  return {
    nodes: Array.from(nodesMap.values()),
    edges
  }
}

async function fetchCommunications() {
  if (!props.assetId) return
  try {
    const response = await api.getAssetCommunications(props.assetId)
    communications.value = response.data
    const graphData = buildCommunicationGraphData(response.data)
    communicationsNodes.value = graphData.nodes
    communicationsEdges.value = graphData.edges
  } catch (e) {
    toast.add({ 
      severity: 'error', 
      summary: t('common.strings.error'), 
      detail: t('assets.communications.fetchError'), 
      life: 3000 
    })
  }
}

// Lifecycle
onMounted(async () => {
  await fetchCommunications()
})

watch(() => props.assetId, async (newId, oldId) => {
  if (newId !== oldId) {
    await fetchCommunications()
  }
})
</script>

<style scoped>
.asset-communications-section {
  margin-top: 1rem;
}
</style> 