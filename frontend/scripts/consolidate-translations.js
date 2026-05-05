#!/usr/bin/env node

/**
 * Script per consolidare le traduzioni esistenti
 * Raggruppa i file per categoria logica e rimuove duplicati
 */

const fs = require('fs')
const path = require('path')

// Configurazione delle categorie
const CATEGORIES = {
  'core': {
    files: ['common', 'forms', 'errors', 'menu'],
    description: 'Funzionalità core dell\'applicazione'
  },
  'assets': {
    files: ['assets', 'assetForm', 'assetDetail', 'assetConnections', 'assetCommunications', 
            'assetCustomFields', 'assetPhotoUpload', 'assetDocumentUpload', 'assetSuppliersTab', 
            'assetTimeline', 'riskBreakdown', 'assettypes', 'assetstatuses'],
    description: 'Gestione asset e dispositivi'
  },
  'entities': {
    files: ['sites', 'locations', 'areas', 'manufacturers', 'suppliers', 'contacts', 'users', 'roles'],
    description: 'Entità principali del sistema'
  },
  'features': {
    files: ['dashboard', 'networkMap', 'floorplanPositioning', 'print', 'auditLogs', 'profile', 'login'],
    description: 'Funzionalità specifiche'
  },
  'ui': {
    files: ['utility', 'permissions', 'roleForm', 'documents', 'interfaces'],
    description: 'Componenti UI e utilità'
  }
}

// Directory delle traduzioni
const LOCALES_DIR = path.join(__dirname, '../src/locales')
const LANGUAGES = ['en', 'it']

/**
 * Carica un file JSON di traduzione
 */
function loadTranslationFile(lang, filename) {
  const filePath = path.join(LOCALES_DIR, lang, `${filename}.json`)
  try {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8')
      return JSON.parse(content)
    }
  } catch (error) {
    console.warn(`⚠️  Errore nel caricamento di ${filePath}:`, error.message)
  }
  return {}
}

/**
 * Salva un file JSON di traduzione
 */
function saveTranslationFile(lang, filename, data) {
  const filePath = path.join(LOCALES_DIR, lang, `${filename}.json`)
  const dir = path.dirname(filePath)
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true })
  }
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8')
  console.log(`✅ Salvato: ${filePath}`)
}

/**
 * Consolida le traduzioni per categoria
 */
function consolidateCategory(categoryName, categoryConfig) {
  console.log(`\n📁 Consolidando categoria: ${categoryName}`)
  console.log(`   Descrizione: ${categoryConfig.description}`)
  console.log(`   File: ${categoryConfig.files.join(', ')}`)
  
  for (const lang of LANGUAGES) {
    const consolidated = {}
    const duplicates = new Set()
    const missing = new Set()
    
    // Carica tutti i file della categoria
    for (const filename of categoryConfig.files) {
      const data = loadTranslationFile(lang, filename)
      
      for (const [key, value] of Object.entries(data)) {
        if (consolidated[key]) {
          if (consolidated[key] !== value) {
            console.warn(`⚠️  Chiave duplicata con valori diversi: ${key}`)
            console.warn(`   File: ${filename}, Valore: ${value}`)
            console.warn(`   Esistente: ${consolidated[key]}`)
          }
          duplicates.add(key)
        } else {
          consolidated[key] = value
        }
      }
    }
    
    // Salva il file consolidato
    if (Object.keys(consolidated).length > 0) {
      saveTranslationFile(lang, categoryName, consolidated)
      
      console.log(`   📊 Statistiche per ${lang}:`)
      console.log(`      - Chiavi totali: ${Object.keys(consolidated).length}`)
      console.log(`      - Duplicati trovati: ${duplicates.size}`)
    }
  }
}

/**
 * Genera un report delle traduzioni mancanti
 */
function generateMissingReport() {
  console.log('\n📋 Report traduzioni mancanti:')
  
  for (const lang of LANGUAGES) {
    console.log(`\n🌐 Lingua: ${lang.toUpperCase()}`)
    
    for (const [categoryName, categoryConfig] of Object.entries(CATEGORIES)) {
      const categoryData = loadTranslationFile(lang, categoryName)
      const missingKeys = []
      
      // Controlla se ci sono chiavi mancanti confrontando con l'altra lingua
      const otherLang = lang === 'en' ? 'it' : 'en'
      const otherCategoryData = loadTranslationFile(otherLang, categoryName)
      
      for (const key of Object.keys(otherCategoryData)) {
        if (!categoryData[key]) {
          missingKeys.push(key)
        }
      }
      
      if (missingKeys.length > 0) {
        console.log(`   📁 ${categoryName}: ${missingKeys.length} chiavi mancanti`)
        missingKeys.slice(0, 5).forEach(key => {
          console.log(`      - ${key}`)
        })
        if (missingKeys.length > 5) {
          console.log(`      ... e altre ${missingKeys.length - 5} chiavi`)
        }
      }
    }
  }
}

/**
 * Genera un file di mappatura per la migrazione
 */
function generateMigrationMap() {
  console.log('\n🗺️  Generando mappa di migrazione...')
  
  const migrationMap = {}
  
  for (const [categoryName, categoryConfig] of Object.entries(CATEGORIES)) {
    migrationMap[categoryName] = {
      description: categoryConfig.description,
      oldFiles: categoryConfig.files,
      newStructure: {}
    }
    
    // Carica il file consolidato per vedere la struttura
    const consolidatedData = loadTranslationFile('en', categoryName)
    migrationMap[categoryName].newStructure = Object.keys(consolidatedData).slice(0, 10) // Prime 10 chiavi come esempio
  }
  
  const mapPath = path.join(LOCALES_DIR, 'migration-map.json')
  fs.writeFileSync(mapPath, JSON.stringify(migrationMap, null, 2) + '\n', 'utf8')
  console.log(`✅ Mappa di migrazione salvata: ${mapPath}`)
}

/**
 * Funzione principale
 */
function main() {
  console.log('🚀 Avvio consolidamento traduzioni...')
  console.log(`📂 Directory: ${LOCALES_DIR}`)
  
  // Consolida ogni categoria
  for (const [categoryName, categoryConfig] of Object.entries(CATEGORIES)) {
    consolidateCategory(categoryName, categoryConfig)
  }
  
  // Genera report
  generateMissingReport()
  
  // Genera mappa di migrazione
  generateMigrationMap()
  
  console.log('\n✅ Consolidamento completato!')
  console.log('\n📝 Prossimi passi:')
  console.log('   1. Verifica i file consolidati')
  console.log('   2. Aggiorna il loader.js per usare i nuovi file')
  console.log('   3. Testa l\'applicazione')
  console.log('   4. Rimuovi i file vecchi quando tutto funziona')
}

// Esegui se chiamato direttamente
if (require.main === module) {
  main()
}

module.exports = {
  consolidateCategory,
  generateMissingReport,
  generateMigrationMap,
  CATEGORIES
}
