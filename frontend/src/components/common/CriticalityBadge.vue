<template>
  <span v-if="value" class="criticality-badge" :class="{ 'icon-only': iconOnly }" :title="tooltipText">
    <i v-if="showIcon" :class="criticalityIcon"></i>
    <span v-if="!iconOnly" class="criticality-text">{{ criticalityLabel }}</span>
  </span>
  <span v-else>-</span>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  value: {
    type: [String, null],
    default: null
  },
  showIcon: {
    type: Boolean,
    default: true
  },
  showText: {
    type: Boolean,
    default: true
  },
  iconOnly: {
    type: Boolean,
    default: false
  }
})

const criticalityLabel = computed(() => {
  switch ((props.value || '').toLowerCase()) {
    case 'low': return t('assets.strings.businessCriticalityLow')
    case 'medium': return t('assets.strings.businessCriticalityMedium')
    case 'high': return t('assets.strings.businessCriticalityHigh')
    case 'critical': return t('assets.strings.businessCriticalityCritical')
    default: return t('common.strings.na')
  }
})

const criticalityIcon = computed(() => {
  if (!props.showIcon) return ''
  
  switch ((props.value || '').toLowerCase()) {
    case 'low': return 'pi pi-circle-fill'
    case 'medium': return 'pi pi-exclamation-circle'
    case 'high': return 'pi pi-exclamation-triangle'
    case 'critical': return 'pi pi-times-circle'
    default: return 'pi pi-question-circle'
  }
})

const criticalityColor = computed(() => {
  switch ((props.value || '').toLowerCase()) {
    case 'low': return '#28a745'      // Verde
    case 'medium': return '#ffc107'   // Giallo
    case 'high': return '#fd7e14'     // Arancione
    case 'critical': return '#dc3545' // Rosso
    default: return '#6c757d'         // Grigio
  }
})

const tooltipText = computed(() => {
  if (props.iconOnly) {
    return `${t('common.fields.businessCriticality')}: ${criticalityLabel.value}`
  }
  return criticalityLabel.value
})
</script>

<style scoped>
.criticality-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  background: v-bind(criticalityColor);
}

.criticality-badge i {
  font-size: 0.875rem;
}

.criticality-text {
  font-weight: 500;
}

.criticality-badge.icon-only {
  gap: 0;
  padding: 0.2rem;
}

.criticality-badge.icon-only i {
  font-size: 1rem;
}
</style> 