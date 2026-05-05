<!--
  - AssetConnections.vue
  - Componente per la gestione delle connessioni degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <Card>
    <template #title>
      {{ t('assetConnections.title') }}
      <Button icon="pi pi-plus" class="p-button-text p-ml-2" @click="showAddDialog = true" />
    </template>
    <template #content>
      <div v-if="connections.length > 0">
        <div v-for="conn in connections" :key="conn.id" class="connection-item">
          <strong>{{ conn.connection_type }}:</strong> {{ getConnectedAssetName(conn) }}
          <span v-if="conn.port_parent || conn.port_child">
            ({{ t('assetConnections.ports') }}: {{ conn.port_parent }} → {{ conn.port_child }})
          </span>
          <Button :label="t('assetConnections.delete')" icon="pi pi-trash" class="p-button-danger p-button-sm"
            @click="deleteConnection(conn.id)" />
        </div>
      </div>
      <div v-else>{{ t('assetConnections.noConnections') }}</div>
    </template>
  </Card>

  <Dialog :header="t('assetConnections.addConnection')" v-model:visible="showAddDialog" modal>
    <div class="p-fluid">
      <div class="p-field">
        <label>{{ t('assetConnections.localInterface') }}</label>
        <Dropdown :options="localInterfaces" optionLabel="name" optionValue="id" v-model="newConnection.local_interface_id" />
      </div>
      <div class="p-field">
        <label>{{ t('assetConnections.remoteAsset') }}</label>
        <InputText id="remote_asset_search" v-model="remoteAssetSearch" :placeholder="t('assetConnections.searchAssetByName')" class="p-mb-2" />
        <Dropdown :options="filteredAssetOptions" optionLabel="name" optionValue="id" v-model="newConnection.remote_asset_id" />
      </div>
      <div class="p-field">
        <label>{{ t('assetConnections.remoteInterface') }}</label>
        <Dropdown :options="remoteInterfaces" optionLabel="name" optionValue="id" v-model="newConnection.remote_interface_id" :disabled="!newConnection.remote_asset_id" />
      </div>
      <div class="p-d-flex p-jc-end p-mt-3">
        <Button :label="t('assetConnections.cancel')" class="p-button-text" @click="showAddDialog = false" />
        <Button :label="t('assetConnections.add')" @click="addConnection" :disabled="!canAddConnection" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'

import api from '@/api/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  assetId: { type: [String, Number], required: true }
})

const toast = useToast()

const connections = ref([])
const allAssets = ref([])
const showAddDialog = ref(false)

const newConnection = ref({
  local_interface_id: null,
  remote_asset_id: null,
  remote_interface_id: null
})

const localInterfaces = computed(() => {
  const asset = allAssets.value.find(a => a.id === props.assetId)
  return asset ? asset.interfaces : []
})
const remoteInterfaces = computed(() => {
  const asset = allAssets.value.find(a => a.id === newConnection.value.remote_asset_id)
  return asset ? asset.interfaces : []
})

const assetOptions = computed(() =>
  allAssets.value.filter(a => a.id !== props.assetId)
)

const remoteAssetSearch = ref("")

const filteredAssetOptions = computed(() => {
  const search = remoteAssetSearch.value.trim().toLowerCase()
  if (!search) return assetOptions.value
  return assetOptions.value.filter(a => a.name && a.name.toLowerCase().includes(search))
})

const canAddConnection = computed(() =>
  newConnection.value.local_interface_id && newConnection.value.remote_asset_id && newConnection.value.remote_interface_id
)

function resetForm() {
  newConnection.value = {
    local_interface_id: null,
    remote_asset_id: null,
    remote_interface_id: null
  }
}

async function fetchConnections() {
  try {
    const response = await api.getAssetConnections(props.assetId)
    connections.value = response.data
  } catch {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetConnections.fetchError') })
  }
}

async function fetchAssets() {
  try {
    const response = await api.getAssets({ include_interfaces: true })
    allAssets.value = response.data
  } catch {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetConnections.fetchAssetsError') })
  }
}

async function addConnection() {
  try {
    await api.createAssetConnection(props.assetId, {
      local_interface_id: newConnection.value.local_interface_id,
      remote_interface_id: newConnection.value.remote_interface_id
    })
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assetConnections.addConnectionSuccess') })
    showAddDialog.value = false
    resetForm()
    await fetchConnections()
  } catch {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assetConnections.addConnectionError') })
  }
}

async function deleteConnection(id) {
  try {
    await api.deleteAssetConnection(props.assetId, id)
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assetConnections.deleteConnectionSuccess'), life: 3000 })
    fetchConnections()
  } catch {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assetConnections.deleteConnectionError'), life: 3000 })
  }
}

function getConnectedAssetName(conn) {
  return conn.parent_asset_id === props.assetId
    ? conn.child_asset?.name || 'Unknown'
    : conn.parent_asset?.name || 'Unknown'
}

onMounted(async () => {
  await fetchAssets()
  await fetchConnections()
})
</script>

<style scoped>
.connection-item {
  margin-bottom: 0.5rem;
}
</style>
