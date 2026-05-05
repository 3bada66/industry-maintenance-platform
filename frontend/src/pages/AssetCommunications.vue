<template>
  <div class="asset-communications-page">
    <h1>{{ t('assetCommunications.title') }}</h1>
    <div class="flex gap-2 mb-3">
      <Button :label="t('assetCommunications.importPcap')" icon="pi pi-upload" @click="showImportDialog = true" />
    </div>
    <TabView v-model:activeIndex="activeTab">
      <TabPanel :header="t('assetCommunications.physicalLinks')">
        <AssetCommunicationGraph :type="'physical'" :nodes="physicalNodes" :edges="physicalEdges" />
        <AssetCommunicationTable :type="'physical'" :rows="physicalLinks" />
      </TabPanel>
      <TabPanel :header="t('assetCommunications.logicalDependencies')">
        <AssetCommunicationGraph :type="'logical'" :nodes="logicalNodes" :edges="logicalEdges" />
        <AssetCommunicationTable :type="'logical'" :rows="logicalLinks" />
      </TabPanel>
    </TabView>
    <PcapImportDialog v-model:visible="showImportDialog" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import AssetCommunicationGraph from '@/components/AssetCommunicationGraph.vue'
import AssetCommunicationTable from '@/components/AssetCommunicationTable.vue'
import PcapImportDialog from '@/components/PcapImportDialog.vue'
import api from '@/api/api'

const { t } = useI18n()
const activeTab = ref(0)
const showImportDialog = ref(false)

const physicalNodes = ref([])
const physicalEdges = ref([])
const physicalLinks = ref([])
const logicalNodes = ref([])
const logicalEdges = ref([])
const logicalLinks = ref([])

async function fetchCommunications(assetId) {
  try {
    const res = await api.getAssetCommunications(assetId)
    // Supponiamo che l'API ritorni un oggetto con physical e logical
    const { physical, logical } = res.data
    // Popola dati fisici
    physicalNodes.value = physical.nodes || []
    physicalEdges.value = physical.edges || []
    physicalLinks.value = physical.links || []
    // Popola dati logici
    logicalNodes.value = logical.nodes || []
    logicalEdges.value = logical.edges || []
    logicalLinks.value = logical.links || []
  } catch (e) {
    physicalNodes.value = []
    physicalEdges.value = []
    physicalLinks.value = []
    logicalNodes.value = []
    logicalEdges.value = []
    logicalLinks.value = []
  }
}

onMounted(() => {
  // Recupera assetId dalla route se necessario
  // Esempio: const assetId = ...
  // fetchCommunications(assetId)
})
</script>

<style scoped>
.asset-communications-page {
  padding: 1rem;
}
.mb-3 { margin-bottom: 1.5em; }
</style> 