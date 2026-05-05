import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useApi } from './useApi'

export function useDuplicate() {
  const { t } = useI18n()
  const { execute } = useApi()
  const duplicating = ref(false)

  /**
   * Duplica un oggetto creando una copia con nome "Copy of [nome originale]"
   * @param {Object} original - L'oggetto originale da duplicare
   * @param {Function} createFunction - Funzione per creare il nuovo oggetto
   * @param {string} entityName - Nome dell'entità per i messaggi (es. 'asset', 'location', 'contact')
   * @param {Function} excludeFields - Funzione per escludere campi dalla duplicazione
   * @returns {Promise<Object|null>} - Il nuovo oggetto creato o null se errore
   */
  async function duplicateItem(original, createFunction, entityName, excludeFields = null) {
    if (!original) {
      console.error('Oggetto originale non valido per la duplicazione')
      return null
    }

    // Verifica che l'oggetto abbia un nome valido (diverso per tipo di entità)
    const hasValidName = hasValidEntityName(original, entityName)
    if (!hasValidName) {
      console.error(`Oggetto ${entityName} non valido per la duplicazione: manca il nome`)
      return null
    }

    duplicating.value = true

    try {
      // Prepara i dati per la duplicazione
      const duplicateData = prepareDuplicateData(original, excludeFields, entityName)
      
      // Crea il nuovo oggetto
      const result = await execute(async () => {
        return await createFunction(duplicateData)
      }, {
        successMessage: t(`${entityName}s.duplicated`),
        errorContext: t(`${entityName}s.duplicateError`)
      })

      duplicating.value = false
      return result
    } catch (error) {
      duplicating.value = false
      console.error('Errore durante la duplicazione:', error)
      return null
    }
  }

  /**
   * Prepara i dati per la duplicazione escludendo campi non necessari
   * @param {Object} original - Oggetto originale
   * @param {Function} excludeFields - Funzione per escludere campi
   * @param {string} entityName - Tipo di entità
   * @returns {Object} - Dati preparati per la duplicazione
   */
  function prepareDuplicateData(original, excludeFields = null, entityName) {
    // Campi da escludere sempre
    const alwaysExclude = ['id', 'created_at', 'updated_at', 'tenant_id', 'deleted_at']
    
    // Campi specifici per tipo di oggetto
    const specificExclude = excludeFields ? excludeFields(original) : []
    
    // Combina tutti i campi da escludere
    const fieldsToExclude = [...alwaysExclude, ...specificExclude]
    
    // Crea una copia dell'oggetto escludendo i campi
    let duplicateData = {}
    Object.keys(original).forEach(key => {
      if (!fieldsToExclude.includes(key)) {
        duplicateData[key] = original[key]
      }
    })
    
    // Modifica il nome per indicare che è una copia
    duplicateData = updateEntityName(duplicateData, entityName)
    
    return duplicateData
  }

  /**
   * Verifica se l'oggetto ha un nome valido per il tipo di entità
   * @param {Object} original - Oggetto originale
   * @param {string} entityName - Tipo di entità
   * @returns {boolean} - True se ha un nome valido
   */
  function hasValidEntityName(original, entityName) {
    switch (entityName) {
      case 'contact':
        return original.first_name && original.last_name
      case 'asset':
      case 'location':
      case 'site':
      case 'supplier':
      case 'manufacturer':
        return original.name
      default:
        return original.name
    }
  }

  /**
   * Aggiorna il nome dell'entità per indicare che è una copia
   * @param {Object} duplicateData - Dati duplicati
   * @param {string} entityName - Tipo di entità
   * @returns {Object} - Dati con nome aggiornato
   */
  function updateEntityName(duplicateData, entityName) {
    switch (entityName) {
      case 'contact':
        if (duplicateData.first_name) {
          duplicateData.first_name = `Copy of ${duplicateData.first_name}`
        }
        break
      case 'asset':
      case 'location':
      case 'site':
      case 'supplier':
      case 'manufacturer':
        if (duplicateData.name) {
          duplicateData.name = `Copy of ${duplicateData.name}`
        }
        break
    }
    return duplicateData
  }

  /**
   * Funzioni di esclusione specifiche per tipo di oggetto
   */
  const excludeFunctions = {
    // Per gli asset, escludi anche floorplan e documenti
    asset: (original) => ['floorplan', 'documents', 'photos', 'custom_fields'],
    
    // Per le locations, escludi floorplan e code (deve essere unico)
    location: (original) => ['floorplan', 'code'],
    
    // Per i contatti, non escludere nulla di specifico
    contact: (original) => [],
    
    // Per i siti, escludi code (deve essere unico)
    site: (original) => ['code'],
    
    // Per i fornitori, escludi documenti e code (se presente)
    supplier: (original) => ['documents', 'code'],
    
    // Per i produttori, non escludere nulla di specifico
    manufacturer: (original) => []
  }

  return {
    duplicating,
    duplicateItem,
    prepareDuplicateData,
    excludeFunctions
  }
} 