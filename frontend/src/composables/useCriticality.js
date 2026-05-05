import { useI18n } from 'vue-i18n'

export function useCriticality() {
  const { t } = useI18n()

  const criticalityColors = {
    low: '#28a745',      // verde
    medium: '#fd7e14',   // arancio
    high: '#dc3545',     // rosso
    critical: '#b30000'  // rosso scuro
  }

  function getCriticalityColor(value) {
    return criticalityColors[value?.toLowerCase()] || '#6c757d'
  }

  function getCriticalityLabel(value) {
    return t('assets.criticality.' + (value?.toLowerCase() || '')) || value || '-'
  }

  return {
    criticalityColors,
    getCriticalityColor,
    getCriticalityLabel
  }
} 