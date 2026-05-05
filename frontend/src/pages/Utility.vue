<!--
  - Utility.vue
  - Componente per la gestione delle utility
  - Utilizza i componenti PrimeVue per la gestione del form
--> 
<template>
  <div class="utility-page">
    <Card>
      <template #title>
        <h3 class="m-0">{{ t('pcap.title') }}</h3>
      </template>
      <template #content>
        <div class="pcap-upload-section">
          <div class="site-selection mb-4">
            <label for="site-dropdown" class="block text-900 font-medium mb-2">
              {{ t('pcap.strings.selectSite') }}:
            </label>
            <Dropdown
              id="site-dropdown"
              v-model="selectedSiteId"
              :options="sites"
              optionLabel="name"
              optionValue="id"
              :placeholder="t('pcap.strings.selectSite')"
              class="w-full"
              :class="{ 'p-invalid': !selectedSiteId && showValidation }"
            />
            <small v-if="!selectedSiteId && showValidation" class="p-error">
              {{ t('pcap.strings.selectSiteBeforeUpload') }}
            </small>
          </div>

          <div class="file-upload-section">
            <div class="mb-2">
              <small class="text-gray-600">
                {{ t('pcap.strings.pcapFileLimit') }}: 50MB per file
              </small>
            </div>
            <FileUpload
              name="file"
              :customUpload="true"
              :multiple="true"
              :auto="true"
              accept=".pcap"
              :chooseLabel="t('pcap.strings.selectPcap')"
              :uploadLabel="t('pcap.strings.preview')"
              @uploader="previewFiles"
              :disabled="loading || !selectedSiteId"
              class="mb-3"
            />
          </div>

          <div v-if="loading" class="loading-indicator">
            <ProgressSpinner />
            <span>{{ t('pcap.strings.processing') }}</span>
          </div>

          <div v-if="previewResult && !loading" class="preview-section">
            <h4 class="text-xl font-semibold mb-3">{{ t('pcap.strings.previewTitle') }}</h4>
            
            <div v-if="previewResult.manufacturers_to_create.length" class="mb-4">
              <h5 class="text-lg font-medium mb-2">{{ t('pcap.strings.newManufacturers') }}</h5>
              <ul class="list-disc list-inside">
                <li v-for="m in previewResult.manufacturers_to_create" :key="m">{{ m }}</li>
              </ul>
            </div>
            
            <div v-if="previewResult.to_create.length" class="mb-4">
              <h5 class="text-lg font-medium mb-2">{{ t('pcap.strings.assetsToCreate') }}</h5>
              <DataTable :value="previewResult.to_create" class="mb-3">
                <Column field="name" :header="t('pcap.strings.name')" />
                <Column field="ip" :header="t('pcap.strings.ip')" />
                <Column field="mac" :header="t('pcap.strings.mac')" />
                <Column field="vendor" :header="t('pcap.strings.vendor')" />
                <Column field="protocols" :header="t('pcap.strings.protocols')">
                  <template #body="{ data }">
                    {{ data.protocols.join(', ') }}
                  </template>
                </Column>
              </DataTable>
            </div>
            
            <div v-if="previewResult.to_update.length" class="mb-4">
              <h5 class="text-lg font-medium mb-2">{{ t('pcap.strings.assetsToUpdate') }}</h5>
              <DataTable :value="previewResult.to_update" class="mb-3">
                <Column field="name" :header="t('pcap.strings.name')" />
                <Column field="ip" :header="t('pcap.strings.ip')" />
                <Column field="mac" :header="t('pcap.strings.mac')" />
                <Column field="vendor" :header="t('pcap.strings.vendor')" />
                <Column field="protocols" :header="t('pcap.strings.protocols')">
                  <template #body="{ data }">
                    {{ data.protocols.join(', ') }}
                  </template>
                </Column>
                <Column :header="t('pcap.strings.changes')">
                  <template #body="{ data }">
                    <div v-for="(change, field) in data.diff" :key="field" class="text-sm">
                      <b>{{ field }}</b>: <span class="text-gray-500">{{ change.old }}</span> → <span class="text-green-600">{{ change.new }}</span>
                    </div>
                  </template>
                </Column>
              </DataTable>
            </div>
            
            <div class="flex gap-2">
              <Button 
                :label="t('pcap.strings.confirmImport')" 
                @click="confirmImport" 
                :disabled="loading"
                severity="success"
              />
              <Button 
                :label="t('common.actions.cancel')" 
                @click="resetPreview" 
                :disabled="loading"
                severity="secondary"
                outlined
              />
            </div>
          </div>

          <div v-if="report && !loading && !previewResult" class="report-section">
            <Message severity="success" :closable="false">
              <template #messageicon>
                <i class="pi pi-check-circle"></i>
              </template>
              <div>
                <p class="font-semibold mb-2">{{ t('pcap.strings.filesUploaded') }}</p>
                <ul class="list-disc list-inside">
                  <li>{{ t('pcap.strings.devicesFound') }}: {{ report.total_devices_found }}</li>
                  <li>{{ t('pcap.strings.newDevicesCreated') }}: {{ report.created }}</li>
                  <li>{{ t('pcap.strings.devicesUpdated') }}: {{ report.updated }}</li>
                </ul>
              </div>
            </Message>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import FileUpload from 'primevue/fileupload'
import ProgressSpinner from "primevue/progressspinner"
import Dropdown from 'primevue/dropdown'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Message from 'primevue/message'
import api from '../api/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const sites = ref([])
const selectedSiteId = ref('')
const report = ref(null);
const toast = useToast()
const loading = ref(false);
const previewResult = ref(null)
const selectedFiles = ref([])
const showValidation = ref(false)

onMounted(async () => {
  try {
    const res = await api.getSites()
    sites.value = res.data
  } catch (e) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('pcap.strings.fetchSitesError') })
  }
})

async function uploadFiles(event) {
  const files = event.files || [];
  
  // Validazione dimensione file
  const validationErrors = validatePcapFiles(files);
  if (validationErrors.length > 0) {
    const errorMessage = validationErrors.map(err => 
      `${err.filename}: ${err.size}MB (massimo ${err.maxSize}MB)`
    ).join(', ');
    
    toast.add({ 
      severity: 'error', 
      summary: t('pcap.strings.fileTooLarge'), 
      detail: errorMessage 
    });
    return;
  }
  
  loading.value = true;
  if (!selectedSiteId.value) {
    showValidation.value = true
    toast.add({ severity: 'warn', summary: t('pcap.strings.missingSelection'), detail: t('pcap.strings.selectSiteBeforeUpload') })
    loading.value = false
    return
  }
  
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  formData.append('site_id', selectedSiteId.value )

  try {
    const res = await api.uploadPcapFile(formData);
    report.value = res.data;
  } catch (err) {
    console.error('Errore:', err.response?.data || err.message);
    toast.add({
      severity: 'error',
      summary: t('common.messages.error'),
      detail: t('pcap.strings.uploadError') + (err.response?.data?.detail || err.message),
    });
  } finally {
    loading.value = false;
  }
}

const validatePcapFiles = (files) => {
  const maxSize = 50 * 1024 * 1024; // 50MB
  const errors = [];
  
  files.forEach((file, index) => {
    if (file.size > maxSize) {
      errors.push({
        filename: file.name,
        size: (file.size / 1024 / 1024).toFixed(1),
        maxSize: 50
      });
    }
  });
  
  return errors;
};

const previewFiles = async (event) => {
  const files = event.files || [];
  
  // Validazione dimensione file
  const validationErrors = validatePcapFiles(files);
  if (validationErrors.length > 0) {
    const errorMessage = validationErrors.map(err => 
      `${err.filename}: ${err.size}MB (massimo ${err.maxSize}MB)`
    ).join(', ');
    
    toast.add({ 
      severity: 'error', 
      summary: t('pcap.strings.fileTooLarge'), 
      detail: errorMessage 
    });
    return;
  }
  
  loading.value = true
  previewResult.value = null
  report.value = null
  selectedFiles.value = files
  
  if (!selectedSiteId.value) {
    showValidation.value = true
    toast.add({ severity: 'warn', summary: t('pcap.strings.missingSelection'), detail: t('pcap.strings.selectSiteBeforeUpload') })
    loading.value = false
    return
  }
  
  showValidation.value = false
  const formData = new FormData()
  selectedFiles.value.forEach((file) => formData.append('files', file))
  formData.append('site_id', selectedSiteId.value)
  
  try {
    const res = await api.previewPcapImport(formData)
    previewResult.value = res.data
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('pcap.strings.uploadError') + (err.response?.data?.detail || err.message) })
  } finally {
    loading.value = false
  }
}

const resetPreview = () => {
  previewResult.value = null
  selectedFiles.value = []
}

const confirmImport = async () => {
  loading.value = true
  if (!selectedSiteId.value || !previewResult.value || !selectedFiles.value.length) return
  const formData = new FormData()
  selectedFiles.value.forEach((file) => formData.append('files', file))
  formData.append('site_id', selectedSiteId.value)
  try {
    const res = await api.uploadPcapFile(formData)
    report.value = res.data
    previewResult.value = null
    selectedFiles.value = []
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('pcap.strings.importSuccess') })
  } catch (err) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('pcap.strings.uploadError') + (err.response?.data?.detail || err.message) })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.utility-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.pcap-upload-section {
  padding: 1rem 0;
}

.site-selection {
  max-width: 400px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 1rem;
  font-weight: 600;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.preview-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.report-section {
  margin-top: 1rem;
}

:deep(.p-dropdown) {
  width: 100%;
}

:deep(.p-fileupload) {
  width: 100%;
}

:deep(.p-fileupload-content) {
  padding: 1rem;
  border: 2px dashed #d1d5db;
  border-radius: 6px;
  text-align: center;
}

:deep(.p-fileupload-content:hover) {
  border-color: #3b82f6;
}

:deep(.p-datatable) {
  font-size: 0.875rem;
}

:deep(.p-datatable .p-datatable-header) {
  background: #f3f4f6;
  font-weight: 600;
}

:deep(.p-message) {
  margin: 0;
}
</style>
