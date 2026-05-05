<template>
  <Dialog :visible="visible" @update:visible="$emit('update:visible', $event)" :header="t('assets.strings.advancedFilters')" :modal="true" :style="{ width: '400px' }">
    <div class="p-fluid">
      <div class="p-field">
        <label for="advanced_business_criticality">{{ t('assets.fields.businessCriticality') }}</label>
        <Dropdown
          id="advanced_business_criticality"
          v-model="localFilters.business_criticality"
          :options="businessCriticalityOptions"
          optionLabel="label"
          optionValue="value"
          :placeholder="t('assets.fields.businessCriticality')"
          showClear
        />
      </div>
      <div class="p-field">
        <label for="advanced_risk_score_min">{{ t('assets.fields.riskScore') }}</label>
        <div class="flex align-items-center gap-2">
          <InputNumber id="advanced_risk_score_min" v-model="localFilters.risk_score_min" :placeholder="t('assets.strings.riskScoreMin')" :min="0" :max="10" mode="decimal" style="width: 80px" />
          <span>-</span>
          <InputNumber id="advanced_risk_score_max" v-model="localFilters.risk_score_max" :placeholder="t('assets.strings.riskScoreMax')" :min="0" :max="10" mode="decimal" style="width: 80px" />
        </div>
      </div>
      <div class="p-field flex gap-2 mt-3">
        <Button :label="t('common.actions.confirm')" icon="pi pi-check" class="p-button-success" @click="applyFilters" />
        <Button :label="t('common.actions.clear')" icon="pi pi-times" class="p-button-text" @click="clearFilters" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import InputNumber from 'primevue/inputnumber'

const props = defineProps({
  visible: { type: Boolean, default: false },
  filters: { type: Object, required: true }
})

const emit = defineEmits(['update:visible', 'apply', 'clear'])

const { t } = useI18n()

const businessCriticalityOptions = [
  { label: t('assets.strings.businessCriticalityLow'), value: 'low' },
  { label: t('assets.strings.businessCriticalityMedium'), value: 'medium' },
  { label: t('assets.strings.businessCriticalityHigh'), value: 'high' },
  { label: t('assets.strings.businessCriticalityCritical'), value: 'critical' }
]

const localFilters = ref({
  business_criticality: null,
  risk_score_min: null,
  risk_score_max: null
})

// Sincronizza i filtri locali con quelli esterni
watch(() => props.filters, (newFilters) => {
  if (newFilters) {
    localFilters.value.business_criticality = newFilters.business_criticality?.value || null
    localFilters.value.risk_score_min = newFilters.risk_score_min?.value || null
    localFilters.value.risk_score_max = newFilters.risk_score_max?.value || null
  }
}, { immediate: true })

function applyFilters() {
  emit('apply', localFilters.value)
  emit('update:visible', false)
}

function clearFilters() {
  localFilters.value = {
    business_criticality: null,
    risk_score_min: null,
    risk_score_max: null
  }
  emit('clear')
  emit('update:visible', false)
}
</script> 