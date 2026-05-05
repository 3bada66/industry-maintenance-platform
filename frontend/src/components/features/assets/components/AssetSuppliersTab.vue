<template>
  <div>
    <div class="flex align-items-center mb-2">
      <span class="section-title">{{ t('suppliers.title') }}</span>
      <Button v-if="!readOnly" class="ml-2 p-button-sm" icon="pi pi-pencil" :label="t('common.actions.edit')" @click="showDialog = true" />
    </div>
    <DataTable :value="suppliers" :loading="loading" class="p-datatable-sm" v-if="suppliers.length">
      <Column field="name" :header="t('common.fields.name')" />
      <Column field="email" :header="t('common.fields.email')" />
      <Column field="phone" :header="t('common.fields.phone')" />
      <Column field="website" :header="t('common.fields.website')" />
      <Column field="notes" :header="t('common.fields.notes')" />
    </DataTable>
    <div v-else class="text-muted">{{ t('suppliers.strings.noSuppliers') }}</div>

    <Dialog v-model:visible="showDialog" :header="t('suppliers.strings.editSuppliers')" modal :closable="true" :dismissableMask="true">
      <MultiSelect
        v-model="selectedSupplierIds"
        :options="allSuppliers"
        optionLabel="name"
        optionValue="id"
        :placeholder="t('common.strings.select')"
        display="chip"
        class="w-full mb-3"
      />
      <div class="flex justify-content-end gap-2">
        <Button :label="t('common.actions.cancel')" class="p-button-secondary" @click="showDialog = false" />
        <Button :label="t('common.actions.save')" icon="pi pi-check" @click="saveSuppliers" :loading="saving" /> 
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import MultiSelect from 'primevue/multiselect'
import api from '@/api/api'

const { t } = useI18n()

const props = defineProps({
  assetId: { type: [String, Number], required: true },
  readOnly: { type: Boolean, default: false }
})

const suppliers = ref([])
const allSuppliers = ref([])
const selectedSupplierIds = ref([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const toast = useToast()

async function fetchSuppliers() {
  loading.value = true
  try {
    const res = await api.getAssetSuppliers(props.assetId)
    suppliers.value = res.data
    selectedSupplierIds.value = res.data.map(s => s.id)
  } finally {
    loading.value = false
  }
}

async function fetchAllSuppliers() {
  const res = await api.getSuppliers()
  allSuppliers.value = res.data
}

async function saveSuppliers() {
  saving.value = true
  try {
    await api.updateAssetSuppliers(props.assetId, selectedSupplierIds.value)
    toast.add({ severity: 'success', summary: t('common.saved'), detail: t('assetSuppliersTab.suppliersUpdated'), life: 2000 })
    showDialog.value = false
    await fetchSuppliers()
  } catch (e) {
    toast.add({ severity: 'error', summary: t('common.error'), detail: t('assetSuppliersTab.updateError'), life: 3000 })
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await fetchSuppliers()
  await fetchAllSuppliers()
})

watch(() => props.assetId, async () => {
  await fetchSuppliers()
  await fetchAllSuppliers()
})
</script>

<style scoped>
.section-title {
  font-weight: bold;
  font-size: 1.1rem;
}
</style> 