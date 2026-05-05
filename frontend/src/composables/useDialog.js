import { ref } from 'vue'

/**
 * Composable standardizzato per la gestione dei dialog e modali
 * Fornisce stato, apertura, chiusura e gestione dati del dialog
 */
export function useDialog() {
  const isVisible = ref(false)
  const data = ref(null)
  const title = ref('')
  const mode = ref('create') // 'create' o 'edit'

  /**
   * Apre il dialog in modalità creazione
   * @param {string} dialogTitle - Titolo del dialog
   * @param {Object} initialData - Dati iniziali (opzionale)
   */
  const openCreate = (dialogTitle, initialData = null) => {
    title.value = dialogTitle
    mode.value = 'create'
    data.value = initialData
    isVisible.value = true
  }

  /**
   * Apre il dialog in modalità modifica
   * @param {string} dialogTitle - Titolo del dialog
   * @param {Object} editData - Dati da modificare
   */
  const openEdit = (dialogTitle, editData) => {
    title.value = dialogTitle
    mode.value = 'edit'
    data.value = { ...editData }
    isVisible.value = true
  }

  /**
   * Apre il dialog in modalità visualizzazione
   * @param {string} dialogTitle - Titolo del dialog
   * @param {Object} viewData - Dati da visualizzare
   */
  const openView = (dialogTitle, viewData) => {
    title.value = dialogTitle
    mode.value = 'view'
    data.value = { ...viewData }
    isVisible.value = true
  }

  /**
   * Chiude il dialog
   */
  const close = () => {
    isVisible.value = false
    data.value = null
    title.value = ''
    mode.value = 'create'
  }

  /**
   * Controlla se il dialog è in modalità creazione
   */
  const isCreateMode = () => {
    return mode.value === 'create'
  }

  /**
   * Controlla se il dialog è in modalità modifica
   */
  const isEditMode = () => {
    return mode.value === 'edit'
  }

  /**
   * Controlla se il dialog è in modalità visualizzazione
   */
  const isViewMode = () => {
    return mode.value === 'view'
  }

  /**
   * Aggiorna i dati del dialog
   * @param {Object} newData - Nuovi dati
   */
  const updateData = (newData) => {
    data.value = { ...newData }
  }

  return {
    isVisible,
    data,
    title,
    mode,
    openCreate,
    openEdit,
    openView,
    close,
    isCreateMode,
    isEditMode,
    isViewMode,
    updateData
  }
} 