<!--
  - AssetDocumentUpload.vue
  - Componente per la gestione dei documenti degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <Card>
    <template #title>{{ t('assets.documents.title') }}</template>
    <template #content>
      <div>
        <Textarea v-if="!readOnly" v-model="doc.description" :placeholder="t('assets.documents.descriptionPlaceholder')" class="mb-2" rows="3" />
        <FileUpload v-if="!readOnly" name="file" :customUpload="true" :auto="true" :multiple="false" :chooseLabel="t('assets.documents.chooseLabel')"
          :uploadLabel="t('assets.documents.uploadLabel')" accept=".pdf,.doc,.docx,.txt" @uploader="uploadDoc" />

        <DataTable :value="documents" class="mt-4">
          <Column field="name" :header="t('assets.documents.name')" />
          <Column field="description" :header="t('assets.documents.description')" />
          <Column header="Download">
            <template #body="{ data }">
              <Button icon="pi pi-download" text @click="downloadDoc(data)" />
            </template>
          </Column>
          <Column v-if="!readOnly" :header="t('common.strings.actions')">
            <template #body="{ data }">
              <Button icon="pi pi-trash" severity="danger" size="small" @click="deleteDoc(data.id)"
                :aria-label="t('common.actions.delete')" />
            </template>
          </Column>
        </DataTable>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import FileUpload from 'primevue/fileupload'
import { useToast } from 'primevue/usetoast'
import api from '@/api/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({ 
  assetId: String,
  readOnly: { type: Boolean, default: false }
})

const toast = useToast()
const doc = ref({ description: '' })
const documents = ref([])

const fetchDocuments = async () => {
  try {
    const res = await api.getAsset(`${props.assetId}`)
    documents.value = res.data.documents || []


  } catch (err) {
    toast.add({
      severity: 'error',
      summary: t('common.strings.error'),
      detail: t('assets.documents.fetchError')
    })
  }
}

const uploadDoc = async ({ files }) => {
  try {
    const file = files[0]
    const formData = new FormData()
    formData.append('file', file)
    formData.append('description', doc.value.description || '')

    await api.uploadAssetDocument(props.assetId, formData)

    doc.value.description = ''
    await fetchDocuments()
    toast.add({
      severity: 'success',
      summary: t('assets.documents.documentUploaded')
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: t('common.strings.error'),
      detail: t('assets.documents.uploadError')
    })
  }
}

const deleteDoc = async (docId) => {
  try {
    await api.deleteAssetDocument(props.assetId, docId)
    await fetchDocuments()
    toast.add({
      severity: 'success',
      summary: t('assets.documents.documentDeleted')
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: t('common.strings.error'),
      detail: t('assets.documents.deleteError')
    })
  }
}

const downloadDoc = async (doc) => {
  try {
    const url = `/api/assets/${props.assetId}/documents/${doc.id}`

    const link = document.createElement('a')
    link.href = url
    link.download = doc.name || ''
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: t('common.strings.error'),
      detail: t('assets.documents.downloadError')
    })
  }
}

onMounted(fetchDocuments)
</script>

<style scoped>
:deep(.p-card) {
  background: var(--card-bg) !important;
  color: var(--text-color) !important;
  border: 1px solid var(--border-color) !important;
}
:deep(.p-datatable) {
  background: var(--card-bg) !important;
  color: var(--text-color) !important;
}
</style>
