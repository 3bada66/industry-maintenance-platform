import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '@/api/api'
import { useToast } from 'primevue/usetoast'

export function usePrint() {
  const { t, locale } = useI18n()
  const toast = useToast()
  
  const templates = ref([])
  const loading = ref(false)
  const isPrinting = ref(false)
  const selectedTemplate = ref(null)

  // Computed per ottenere il nome tradotto del template
  const getTemplateName = (template) => {
    if (template.name_translations && template.name_translations[locale.value]) {
      return template.name_translations[locale.value]
    }
    return template.name || template.key
  }

  // Computed per ottenere la descrizione tradotta del template
  const getTemplateDescription = (template) => {
    if (template.description_translations && template.description_translations[locale.value]) {
      return template.description_translations[locale.value]
    }
    return template.description || ''
  }

  // Computed per ottenere i template disponibili
  const availableTemplates = computed(() => {
    return templates.value.map(template => template.key)
  })

  // Funzione per ottenere un template specifico
  const getTemplate = (key) => {
    return templates.value.find(template => template.key === key)
  }

  // Carica i template disponibili
  const loadTemplates = async () => {
    try {
      loading.value = true
      const response = await api.getPrintTemplates()
      templates.value = response.data
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: t('common.messages.error'),
        detail: t('print.templates.loadError'),
        life: 3000
      })
    } finally {
      loading.value = false
    }
  }

  // Genera una stampa
  const generatePrint = async (assetId, templateId, options = {}) => {
    try {
      const response = await api.generatePrint(assetId, templateId, options)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Scarica una stampa generata
  const downloadPrint = async (printId) => {
    try {
      const response = await api.downloadPrint(printId)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Stampa un asset (funzione principale per il PrintDialog)
  const print = async (templateKey, data, options = {}) => {
    try {
      isPrinting.value = true
      
      // Trova il template selezionato
      const template = getTemplate(templateKey)
      if (!template) {
        throw new Error(t('print.templates.notFound'))
      }

      // Opzioni di default del template
      const templateOptions = template.options || {}
      const finalOptions = { ...templateOptions, ...options }

      // Prova prima la generazione lato backend
      try {
        const response = await generatePrint(data.id, template.id, finalOptions)
        
        if (response.print_id) {
          // Download del file generato
          const blob = await downloadPrint(response.print_id)
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = `asset-${data.name}-${new Date().toISOString().split('T')[0]}.pdf`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        }
        
        toast.add({
          severity: 'success',
          summary: t('common.messages.success'),
          detail: t('print.generation.success'),
          life: 3000
        })
        
      } catch (backendError) {
        // Fallback alla generazione frontend
        await generatePrintFrontend(templateKey, data, finalOptions)
      }
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: t('common.messages.error'),
        detail: t('print.generation.error'),
        life: 3000
      })
      throw error
    } finally {
      isPrinting.value = false
    }
  }

  // Stampa un asset (funzione legacy per compatibilità)
  const printAsset = async (data, templateKey = null, options = {}) => {
    try {
      // Trova il template selezionato
      let template = selectedTemplate.value
      if (templateKey && !template) {
        template = templates.value.find(t => t.key === templateKey)
      }
      
      if (!template) {
        throw new Error(t('print.templates.notFound'))
      }

      // Opzioni di default del template
      const templateOptions = template.options || {}
      const finalOptions = { ...templateOptions, ...options }

      // Prova prima la generazione lato backend
      try {
        const response = await generatePrint(data.id, template.id, finalOptions)
        
        if (response.print_id) {
          // Download del file generato
          const blob = await downloadPrint(response.print_id)
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = `asset-${data.name}-${new Date().toISOString().split('T')[0]}.pdf`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        }
        
        toast.add({
          severity: 'success',
          summary: t('common.messages.success'),
          detail: t('print.generation.success'),
          life: 3000
        })
        
      } catch (backendError) {
        // Fallback alla generazione frontend
        await generatePrintFrontend(templateKey, data, finalOptions)
      }
    } catch (error) {
      toast.add({
        severity: 'error',
        summary: t('common.messages.error'),
        detail: t('print.generation.error'),
        life: 3000
      })
    }
  }

  // Generazione frontend (fallback)
  const generatePrintFrontend = async (templateKey, data, options) => {
    // Implementazione fallback per generazione PDF lato frontend
    // Qui potresti implementare jsPDF o altre librerie
  }

  return {
    templates,
    loading,
    isPrinting,
    selectedTemplate,
    availableTemplates,
    getTemplate,
    getTemplateName,
    getTemplateDescription,
    loadTemplates,
    generatePrint,
    downloadPrint,
    print,
    printAsset
  }
} 