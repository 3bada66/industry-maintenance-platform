<template>
  <Dialog :visible="visible" @update:visible="$emit('close')" :header="t('manufacturers.manufacturerImport.title')" :modal="true" :style="{ width: '60vw' }">
    <div class="mb-3">
      <a :href="templateUrl" download class="p-button p-button-sm p-button-outlined">
        <i class="pi pi-download mr-2" />{{ t('manufacturers.manufacturerImport.downloadTemplate') }}
      </a>
    </div>
    
    <!-- Informazioni utili -->
    <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
      <h4 class="text-blue-800 mb-2">{{ t('manufacturers.manufacturerImport.importantInfo') }}</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
        <div>
          <h5 class="font-semibold text-blue-700 mb-1">{{ t('manufacturers.manufacturerImport.requiredFields') }}</h5>
          <ul class="text-blue-600">
            <li>• {{ t('manufacturers.manufacturerImport.nameRequired') }}</li>
          </ul>
        </div>
        <div>
          <h5 class="font-semibold text-blue-700 mb-1">{{ t('manufacturers.manufacturerImport.validFormats') }}</h5>
          <ul class="text-blue-600">
            <li>• {{ t('manufacturers.manufacturerImport.emailFormat') }}</li>
            <li>• {{ t('manufacturers.manufacturerImport.websiteFormat') }}</li>
            <li>• {{ t('manufacturers.manufacturerImport.phoneFormat') }}</li>
          </ul>
        </div>
      </div>
      <div class="mt-3 text-blue-600 text-sm">
        <p><strong>{{ t('manufacturers.manufacturerImport.tip') }}:</strong> {{ t('manufacturers.manufacturerImport.tipText') }}</p>
      </div>
    </div>
    
    <div class="mb-3">
      <input type="file" accept=".csv,.xlsx" @change="onFileChange" />
    </div>
    <div v-if="loading" class="mb-3">
      <ProgressSpinner style="width:40px;height:40px" />
    </div>
    <div v-if="error" class="mb-3 text-red-600">
      <pre>{{ error }}</pre>
    </div>
    <div v-if="previewResult">
      <div v-if="previewResult.to_create && previewResult.to_create.length">
        <h4 class="mb-1">{{ t('manufacturers.manufacturerImport.toCreate') }}</h4>
        <DataTable :value="previewResult.to_create" scrollable :scrollHeight="'20vh'">
          <Column v-for="col in columns" :key="col.field" :field="col.field" :header="t(col.header)" />
        </DataTable>
      </div>
      <div v-if="previewResult.to_update && previewResult.to_update.length">
        <h4 class="mt-3 mb-1">{{ t('manufacturers.manufacturerImport.toUpdate') }}</h4>
        <DataTable :value="previewResult.to_update" scrollable :scrollHeight="'20vh'">
          <Column field="name" :header="t('manufacturers.manufacturerForm.name')" />
          <Column field="diff" :header="t('manufacturers.manufacturerImport.differences')">
            <template #body="{ data }">
              <ul>
                <li v-for="(change, field) in data.diff" :key="field">
                  <b>{{ field }}</b>: <span style="color: #888">{{ change.old }}</span> → <span style="color: #059669">{{ change.new }}</span>
                </li>
              </ul>
            </template>
          </Column>
        </DataTable>
      </div>
      <div v-if="previewResult.errors && previewResult.errors.length">
        <h4 class="mt-3 mb-1 text-red-600">{{ t('manufacturers.manufacturerImport.errors') }}</h4>
        <ul>
          <li v-for="err in previewResult.errors" :key="err.row">{{ t('manufacturers.manufacturerImport.row') }} {{ err.row }}: {{ err.error }}</li>
        </ul>
      </div>
    </div>
    <template #footer>
      <Button :label="t('common.cancel')" class="p-button-text" @click="$emit('close')" />
      <Button :label="t('manufacturers.manufacturerImport.confirm')" :disabled="isConfirmDisabled" @click="confirmImport" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'
import api from '../../api/api'

const { t } = useI18n()
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['close', 'imported'])

const templateUrl = '/template_import_manufacturer.csv'
const file = ref(null)
const columns = ref([
  { field: 'name', header: 'manufacturers.manufacturerForm.name' },
  { field: 'description', header: 'manufacturers.manufacturerForm.description' },
  { field: 'website', header: 'manufacturers.manufacturerForm.website' },
  { field: 'email', header: 'manufacturers.manufacturerForm.email' },
  { field: 'phone', header: 'manufacturers.manufacturerForm.phone' },
])
const loading = ref(false)
const error = ref('')
const previewResult = ref(null)

// Computed property per determinare se il pulsante deve essere disabilitato
const isConfirmDisabled = computed(() => {
  return !file.value || loading.value || (error.value && error.value.length > 0) || (previewResult.value && previewResult.value.errors && previewResult.value.errors.length > 0)
})

async function onFileChange(e) {
  error.value = ''
  previewResult.value = null
  const f = e.target.files[0]
  if (!f) return
  file.value = f
  loading.value = true
  try {
    const { data } = await api.previewManufacturerImportXlsx(f)
    previewResult.value = data
    
    // Gestisci errori di parsing del file
    if (data.error) {
      error.value = data.error
    } else if (data.errors && data.errors.length) {
      error.value = data.errors.map(e => `${t('manufacturers.manufacturerImport.row')} ${e.row}: ${e.error}`).join('\n')
    } else {
      error.value = ''
    }
  } catch (e) {
    error.value = t('manufacturers.manufacturerImport.readError')
  }
  loading.value = false
}

async function confirmImport() {
  if (!file.value) return
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.confirmManufacturerImportXlsx(file.value)
    emit('imported', data)
  } catch (e) {
    error.value = t('manufacturerImport.readError')
  }
  loading.value = false
}
</script>

<style scoped>
.text-red-600 {
  color: #dc2626;
}
</style> 