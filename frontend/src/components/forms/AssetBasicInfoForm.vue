<template>
  <Card class="mb-4">
    <template #title>
      <div class="flex align-items-center">
        <i class="pi pi-info-circle mr-2"></i>
        {{ t('assets.strings.mainInfo') }}
      </div>
    </template>
    <template #content>
      <div class="grid">
        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="name">{{ t('common.fields.name') }} <span class="required">*</span></label>
            <InputText 
              id="name" 
              v-model="form.name" 
              :class="{ 'p-invalid': errors.name }"
              required 
              class="w-full"
              maxlength="100"
            />
            <small v-if="errors.name" class="p-error">{{ errors.name }}</small>
          </div>
        </div>
        
        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="asset_type_id">{{ t('common.fields.type') }} <span class="required">*</span></label>
            <Dropdown 
              id="asset_type_id" 
              v-model="form.asset_type_id" 
              :options="assetTypes" 
              optionLabel="name" 
              optionValue="id" 
              :class="{ 'p-invalid': errors.asset_type_id }"
              class="w-full"
              required 
            />
            <small v-if="errors.asset_type_id" class="p-error">{{ errors.asset_type_id }}</small>
          </div>
        </div>

        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="manufacturer_id">{{ t('manufacturers.strings.manufacturer') }} <span class="required">*</span></label>
            <Dropdown 
              id="manufacturer_id" 
              v-model="form.manufacturer_id" 
              :options="manufacturers" 
              optionLabel="name" 
              optionValue="id" 
              :class="{ 'p-invalid': errors.manufacturer_id }"
              class="w-full"
              required 
            />
            <small v-if="errors.manufacturer_id" class="p-error">{{ errors.manufacturer_id }}</small>
          </div>
        </div>

        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="status_id">{{ t('common.fields.status') }} <span class="required">*</span></label>
            <Dropdown 
              id="status_id" 
              v-model="form.status_id" 
              :options="assetStatusOptions" 
              optionLabel="name" 
              optionValue="id" 
              :itemTemplate="statusItemTemplate"
              :placeholder="t('common.selectStatus')"
              :class="{ 'p-invalid': errors.status_id }"
              class="w-full"
              required 
            />
            <small v-if="errors.status_id" class="p-error">{{ errors.status_id }}</small>
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'

const props = defineProps({
  form: { type: Object, required: true },
  errors: { type: Object, default: () => ({}) },
  assetTypes: { type: Array, required: true },
  manufacturers: { type: Array, required: true },
  assetStatusOptions: { type: Array, required: true }
})

const { t } = useI18n()

function statusItemTemplate(option) {
  return option ? (
    `<span style="background:${option.color};color:#fff;padding:0.2rem 0.5rem;border-radius:4px;">${option.name}</span>`
  ) : ''
}
</script>

<style scoped>
.required {
  color: #dc3545;
  font-weight: bold;
}

.p-field {
  margin-bottom: 1rem;
}

.p-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.p-invalid {
  border-color: #dc3545 !important;
}

.p-error {
  color: #dc3545;
  font-size: 0.875rem;
}
</style> 