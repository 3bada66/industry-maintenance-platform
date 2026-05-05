import { useI18n } from 'vue-i18n'

export function useDateFormatter() {
  const { t } = useI18n()

  function formatDate(dateString) {
    if (!dateString) return t('common.strings.na')
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('it-IT')
    } catch (e) {
      return t('common.strings.na')
    }
  }

  function formatDateTime(dateString) {
    if (!dateString) return t('common.strings.na')
    try {
      const date = new Date(dateString)
      return date.toLocaleString('it-IT')
    } catch (e) {
      return t('common.strings.na')
    }
  }

  function formatDateForInput(dateString) {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toISOString().split('T')[0]
    } catch (e) {
      return ''
    }
  }

  return {
    formatDate,
    formatDateTime,
    formatDateForInput
  }
} 