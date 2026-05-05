<template>
  <div>
    <h2>{{ t('assets.connections.title') }}</h2>
    <Button :label="t('assets.connections.addConnection')" icon="pi pi-plus" class="mb-3" @click="showAddConnectionDialog = true" />
    <AssetConnectionsTable :connections="mappedConnections" @edit-connection="onEditConnection" @delete-connection="onDeleteConnection" />
    <AssetConnectionGraph :connections="mappedConnections" />
    
    <!-- Dialog per aggiungere connessione -->
    <Dialog v-model:visible="showAddConnectionDialog" :header="t('assets.connections.addConnection')" modal style="width: 400px" :closable="true" :dismissableMask="true" @hide="resetAddConnectionForm">
      <div class="p-fluid">
        <div class="field">
          <label>{{ t('assets.connections.localInterface') }}</label>
          <Dropdown v-model="selectedLocalInterface" :options="localInterfaces" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" />
        </div>
        <div class="field">
          <label>{{ t('assets.connections.remoteAsset') }}</label>
          <Dropdown v-model="selectedRemoteAsset" :options="remoteAssets" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" />
        </div>
        <div class="field">
          <label>{{ t('assets.connections.remoteInterface') }}</label>
          <Dropdown v-model="selectedRemoteInterface" :options="remoteInterfaces" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" :disabled="!selectedRemoteAsset" />
        </div>
        <Button :label="t('common.actions.save')" icon="pi pi-check" class="mt-3" @click="addConnection" :disabled="!selectedLocalInterface || !selectedRemoteAsset || !selectedRemoteInterface" />
      </div>
    </Dialog>

    <!-- Dialog per modificare connessione -->
    <Dialog v-model:visible="showEditConnectionDialog" :header="t('assets.connections.editConnection')" modal style="width: 400px" :closable="true" :dismissableMask="true">
      <div class="p-fluid">
        <div class="field">
          <label>{{ t('assets.connections.localInterface') }}</label>
          <Dropdown v-model="editConnectionData.interfaceA.id" :options="localInterfaces" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" />
        </div>
        <div class="field">
          <label>{{ t('assets.connections.remoteAsset') }}</label>
          <Dropdown v-model="editConnectionData.assetB.id" :options="remoteAssets" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" />
        </div>
        <div class="field">
          <label>{{ t('assets.connections.remoteInterface') }}</label>
          <Dropdown v-model="editConnectionData.interfaceB.id" :options="editRemoteInterfaces" optionLabel="name" optionValue="id" :placeholder="t('common.strings.select')" :disabled="!editConnectionData.assetB.id" />
        </div>
        <Button :label="t('common.actions.save')" icon="pi pi-check" class="mt-3" @click="saveEditConnection" :disabled="!editConnectionData.interfaceA.id || !editConnectionData.assetB.id || !editConnectionData.interfaceB.id" />
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import AssetConnectionsTable from '@/components/tables/AssetConnectionsTable.vue'
import AssetConnectionGraph from '../components/AssetConnectionGraph.vue'
import api from '@/api/api'

const props = defineProps({
  assetId: { type: [String, Number], required: true },
  assetInterfaces: { type: Array, default: () => [] }
})

const { t } = useI18n()
const toast = useToast()
const confirm = useConfirm()

// Stato
const connections = ref([])
const connectionsNodes = ref([])
const connectionsEdges = ref([])
const showAddConnectionDialog = ref(false)
const showEditConnectionDialog = ref(false)
const selectedLocalInterface = ref(null)
const selectedRemoteAsset = ref(null)
const selectedRemoteInterface = ref(null)
const remoteAssets = ref([])
const editConnectionData = ref({
  interfaceA: { id: null },
  assetB: { id: null },
  interfaceB: { id: null },
  id: null
})

// Computed
const localInterfaces = computed(() => props.assetInterfaces || [])

const remoteInterfaces = computed(() => {
  if (!selectedRemoteAsset.value) return []
  const assetObj = remoteAssets.value.find(a => a.id === selectedRemoteAsset.value)
  if (!assetObj) return []
  if (!selectedLocalInterface.value) return assetObj.interfaces
  const localType = localInterfaces.value.find(i => i.id === selectedLocalInterface.value)?.type
  return assetObj.interfaces.filter(i => i.type === localType)
})

const editRemoteInterfaces = computed(() => {
  if (!editConnectionData.value?.assetB?.id) return []
  const assetObj = remoteAssets.value.find(a => a.id === editConnectionData.value.assetB.id)
  if (!assetObj) return []
  if (!editConnectionData.value.interfaceA?.id) return assetObj.interfaces
  const localType = localInterfaces.value.find(i => i.id === editConnectionData.value.interfaceA.id)?.type
  return assetObj.interfaces.filter(i => i.type === localType)
})

const mappedConnections = computed(() =>
  connections.value
    .map(conn => {
      if (conn.parent_asset_id === props.assetId) {
        return {
          interfaceA: conn.local_interface,
          assetA: conn.parent_asset,
          interfaceB: conn.remote_interface,
          assetB: conn.child_asset,
          id: conn.id
        }
      } else {
        return {
          interfaceA: conn.remote_interface,
          assetA: conn.child_asset,
          interfaceB: conn.local_interface,
          assetB: conn.parent_asset,
          id: conn.id
        }
      }
    })
    .sort((a, b) => {
      const nameA = a.interfaceA?.name?.toLowerCase() || ''
      const nameB = b.interfaceA?.name?.toLowerCase() || ''
      return nameA.localeCompare(nameB)
    })
)

// Funzioni
async function fetchConnections() {
  if (!props.assetId) return
  try {
    const res = await api.getAssetConnections(props.assetId)
    connections.value = res.data
    // Popola nodi e archi per il grafo
    const nodesSet = new Set()
    const edgesArr = []
    res.data.forEach(conn => {
      // Aggiungi nodi
      if (conn.local_asset) nodesSet.add(JSON.stringify({ id: conn.local_asset.id, label: conn.local_asset.name }))
      if (conn.remote_asset) nodesSet.add(JSON.stringify({ id: conn.remote_asset.id, label: conn.remote_asset.name }))
      // Aggiungi edge
      if (conn.local_asset && conn.remote_asset && conn.local_interface && conn.remote_interface) {
        edgesArr.push({
          from: conn.local_asset.id,
          to: conn.remote_asset.id,
          label: `${conn.local_interface.name} ↔ ${conn.remote_interface.name}`,
          color: '#2196f3'
        })
      }
    })
    connectionsNodes.value = Array.from(nodesSet).map(s => JSON.parse(s))
    connectionsEdges.value = edgesArr
  } catch (e) {
    toast.add({ severity: 'error', summary: t('common.strings.error'), detail: t('assets.connections.fetchError') })
  }
}

async function fetchRemoteAssets() {
  try {
    const res = await api.getAssets({ include_interfaces: true })
    remoteAssets.value = res.data.filter(a => a.id !== props.assetId)
  } catch (e) {
    remoteAssets.value = []
  }
}

async function addConnection() {
  try {
    await api.createAssetConnection(props.assetId, {
      local_interface_id: selectedLocalInterface.value,
      remote_interface_id: selectedRemoteInterface.value
    })
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assets.connections.addConnectionSuccess') })
    showAddConnectionDialog.value = false
    resetAddConnectionForm()
    await fetchConnections()
  } catch (e) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assets.connections.addConnectionError') })
  }
}

function resetAddConnectionForm() {
  selectedLocalInterface.value = null
  selectedRemoteAsset.value = null
  selectedRemoteInterface.value = null
}

function resetEditConnectionForm() {
  editConnectionData.value = {
    interfaceA: { id: null },
    assetB: { id: null },
    interfaceB: { id: null },
    id: null
  }
}

function onEditConnection(row) {
  editConnectionData.value = {
    interfaceA: { id: row.interfaceA?.id || null },
    assetB: { id: row.assetB?.id || null },
    interfaceB: { id: row.interfaceB?.id || null },
    id: row.id || null
  }
  showEditConnectionDialog.value = true
}

async function onDeleteConnection(row) {
  confirm.require({
    message: t('assets.connections.confirmDelete'),
    header: t('common.strings.confirm'),
    icon: 'pi pi-exclamation-triangle',
    accept: async () => {
      try {
        await api.deleteAssetConnection(props.assetId, row.id)
        toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assets.connections.deleteSuccess') })
        await fetchConnections()
      } catch (e) {
        toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assets.connections.deleteError') })
      }
    }
  })
}

async function saveEditConnection() {
  try {
    await api.updateAssetConnection(props.assetId, editConnectionData.value.id, {
      local_interface_id: editConnectionData.value.interfaceA.id,
      remote_interface_id: editConnectionData.value.interfaceB.id
    })
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assets.connections.editSuccess') })
    showEditConnectionDialog.value = false
    resetEditConnectionForm()
    await fetchConnections()
  } catch (e) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assets.connections.editError') })
  }
}

// Lifecycle
onMounted(async () => {
  await fetchConnections()
  await fetchRemoteAssets()
})

watch(() => props.assetId, async (newId, oldId) => {
  if (newId !== oldId) {
    await fetchConnections()
    await fetchRemoteAssets()
  }
})

watch(showAddConnectionDialog, val => {
  if (val) fetchRemoteAssets()
})
</script> 