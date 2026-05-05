<template>
  <div>
    <div v-if="loading" class="p-4 text-center">
      <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      <p>{{ t('riskBreakdown.loadingRiskData') }}</p>
    </div>
    <RiskBreakdown v-else-if="riskBreakdown" :breakdown="riskBreakdown" />
    <div v-else class="p-4 text-center text-muted">{{ t('riskBreakdown.noRiskData') }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import RiskBreakdown from '../components/RiskBreakdown.vue'
import api from '@/api/api'
import { useCriticality } from '@/composables/useCriticality'

const props = defineProps({
  assetId: { type: [String, Number], required: true }
})
const { t } = useI18n()
const { criticalityColors } = useCriticality()

const riskBreakdown = ref(null)
const loading = ref(false)

function riskLevelLabel(score) {
  if (score === null || score === undefined) return t('riskBreakdown.riskLevelUndefined')
  if (score >= 7) return t('riskBreakdown.riskLevelHigh')
  if (score >= 4) return t('riskBreakdown.riskLevelMedium')
  return t('riskBreakdown.riskLevelLow')
}

function riskLevelSeverity(score) {
  if (score === null || score === undefined) return 'info'
  if (score >= 7) return 'danger'
  if (score >= 4) return 'warning'
  return 'success'
}

async function fetchRiskBreakdown() {
  if (!props.assetId) return
  loading.value = true
  try {
    const res = await api.calculateAssetRisk(props.assetId)
    riskBreakdown.value = res.data.breakdown
  } catch (e) {
    riskBreakdown.value = null
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchRiskBreakdown()
})

watch(() => props.assetId, async (newId, oldId) => {
  if (newId !== oldId) {
    await fetchRiskBreakdown()
  }
})

// Esponi le funzioni e dati per l'header
defineExpose({
  riskBreakdown,
  riskLevelLabel,
  riskLevelSeverity,
  criticalityColors
})
</script> 