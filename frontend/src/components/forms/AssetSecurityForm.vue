<template>
  <Card class="mb-4">
    <template #title>
      <div class="flex align-items-center">
        <i class="pi pi-shield mr-2"></i>
        {{ t('assets.strings.securityInfo') }}
      </div>
    </template>
    <template #content>
      <div class="grid">
        <div class="col-12 md:col-6">
          <div class="p-field">
            <label class="flex align-items-center">
              <InputSwitch v-model="form.remote_access" class="mr-2" />
              {{ t('assets.fields.remoteAccess') }}
            </label>
          </div>
        </div>

        <div class="col-12 md:col-6" v-if="form.remote_access">
          <div class="p-field">
            <label for="remote_access_type">{{ t('assets.fields.remoteAccessType') }}</label>
            <Dropdown 
              id="remote_access_type" 
              v-model="form.remote_access_type" 
              :options="remoteAccessTypeOptions" 
              optionLabel="label" 
              optionValue="value"
              :placeholder="t('common.strings.select')"
              class="w-full"
            />
          </div>
        </div>

        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="physical_access_ease">{{ t('assets.fields.physicalAccessEase') }}</label>
            <Dropdown 
              id="physical_access_ease" 
              v-model="form.physical_access_ease" 
              :options="physicalAccessOptions" 
              optionLabel="label" 
              optionValue="value"
              :placeholder="t('common.strings.select')"
              class="w-full"
            />
          </div>
        </div>

        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="business_criticality">{{ t('assets.fields.businessCriticality') }}</label>
            <Dropdown
              id="business_criticality"
              v-model="form.business_criticality"
              :options="businessCriticalityOptions"
              optionLabel="label"
              optionValue="value"
              :placeholder="t('common.strings.select')"
              class="w-full"
            />
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'
import Dropdown from 'primevue/dropdown'
import InputSwitch from 'primevue/inputswitch'

const props = defineProps({
  form: { type: Object, required: true }
})

const { t } = useI18n()

const remoteAccessTypeOptions = [
  { label: t('assets.strings.remoteAccessTypeNone'), value: 'none' },
  { label: t('assets.strings.remoteAccessTypeAttended'), value: 'attended' },
  { label: t('assets.strings.remoteAccessTypeUnattended'), value: 'unattended' }
]

const physicalAccessOptions = [
  { label: t('assets.strings.physicalAccessInternal'), value: 'internal' },
  { label: t('assets.strings.physicalAccessDMZ'), value: 'dmz' },
  { label: t('assets.strings.physicalAccessExternal'), value: 'external' }
]

const businessCriticalityOptions = [
  { label: t('assets.strings.businessCriticalityLow'), value: 'low' },
  { label: t('assets.strings.businessCriticalityMedium'), value: 'medium' },
  { label: t('assets.strings.businessCriticalityHigh'), value: 'high' },
  { label: t('assets.strings.businessCriticalityCritical'), value: 'critical' }
]
</script>

<style scoped>
.p-field {
  margin-bottom: 1rem;
}

.p-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
</style> 