#!/usr/bin/env node

/**
 * Script per generare statistiche delle traduzioni
 * Mostra lo stato delle traduzioni e identifica problemi
 */

const fs = require('fs')
const path = require('path')

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
 * Ottieni tutti i file di traduzione per una lingua
 */
function getTranslationFiles(lang) {
  const langDir = path.join(LOCALES_DIR, lang)
  if (!fs.existsSync(langDir)) {
    return []
  }
  
  return fs.readdirSync(langDir)
    .filter(file => file.endsWith('.json'))
    .map(file => file.replace('.json', ''))
}

/**
 * Analizza le statistiche per una lingua
 */
function analyzeLanguageStats(lang) {
  const files = getTranslationFiles(lang)
  const stats = {
    language: lang,
    totalFiles: files.length,
    totalKeys: 0,
    files: {},
    categories: {},
    duplicates: [],
    emptyValues: [],
    longKeys: [],
    shortKeys: []
  }
  
  for (const filename of files) {
    const data = loadTranslationFile(lang, filename)
    const keys = Object.keys(data)
    
    stats.files[filename] = {
      keyCount: keys.length,
      keys: keys,
      hasEmptyValues: false,
      hasLongKeys: false,
      hasShortKeys: false
    }
    
    stats.totalKeys += keys.length
    
    // Analizza le chiavi
    for (const [key, value] of Object.entries(data)) {
      // Categoria (prima parte della chiave)
      const category = key.split('.')[0]
      if (!stats.categories[category]) {
        stats.categories[category] = 0
      }
      stats.categories[category]++
      
      // Valori vuoti
      if (!value || (typeof value === 'string' && value.trim() === '')) {
        stats.emptyValues.push({ file: filename, key, value })
        stats.files[filename].hasEmptyValues = true
      }
      
      // Chiavi lunghe
      if (key.length > 50) {
        stats.longKeys.push({ file: filename, key, length: key.length })
        stats.files[filename].hasLongKeys = true
      }
      
      // Chiavi corte
      if (key.length < 3) {
        stats.shortKeys.push({ file: filename, key, length: key.length })
        stats.files[filename].hasShortKeys = true
      }
    }
  }
  
  return stats
}

/**
 * Confronta le statistiche tra lingue
 */
function compareLanguageStats(stats1, stats2) {
  const comparison = {
    missingInFirst: [],
    missingInSecond: [],
    differentValues: [],
    coverage: 0
  }
  
  const keys1 = new Set()
  const keys2 = new Set()
  
  // Raccogli tutte le chiavi
  for (const [filename, fileStats] of Object.entries(stats1.files)) {
    for (const key of fileStats.keys) {
      keys1.add(`${filename}.${key}`)
    }
  }
  
  for (const [filename, fileStats] of Object.entries(stats2.files)) {
    for (const key of fileStats.keys) {
      keys2.add(`${filename}.${key}`)
    }
  }
  
  // Trova chiavi mancanti
  for (const key of keys1) {
    if (!keys2.has(key)) {
      comparison.missingInSecond.push(key)
    }
  }
  
  for (const key of keys2) {
    if (!keys1.has(key)) {
      comparison.missingInFirst.push(key)
    }
  }
  
  // Calcola coverage
  const totalKeys = Math.max(keys1.size, keys2.size)
  const commonKeys = Math.min(keys1.size, keys2.size)
  comparison.coverage = totalKeys > 0 ? (commonKeys / totalKeys) * 100 : 100
  
  return comparison
}

/**
 * Genera un report dettagliato
 */
function generateDetailedReport() {
  console.log('📊 Report Dettagliato Traduzioni\n')
  
  const allStats = {}
  for (const lang of LANGUAGES) {
    allStats[lang] = analyzeLanguageStats(lang)
  }
  
  // Statistiche per lingua
  for (const [lang, stats] of Object.entries(allStats)) {
    console.log(`🌐 Lingua: ${lang.toUpperCase()}`)
    console.log(`   📁 File totali: ${stats.totalFiles}`)
    console.log(`   🔑 Chiavi totali: ${stats.totalKeys}`)
    console.log(`   📂 Categorie: ${Object.keys(stats.categories).length}`)
    
    // Top 5 categorie
    const topCategories = Object.entries(stats.categories)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
    
    console.log(`   🏆 Top categorie:`)
    topCategories.forEach(([category, count]) => {
      console.log(`      - ${category}: ${count} chiavi`)
    })
    
    // Problemi
    if (stats.emptyValues.length > 0) {
      console.log(`   ⚠️  Valori vuoti: ${stats.emptyValues.length}`)
    }
    
    if (stats.longKeys.length > 0) {
      console.log(`   ⚠️  Chiavi lunghe (>50 char): ${stats.longKeys.length}`)
    }
    
    if (stats.shortKeys.length > 0) {
      console.log(`   ⚠️  Chiavi corte (<3 char): ${stats.shortKeys.length}`)
    }
    
    console.log('')
  }
  
  // Confronto tra lingue
  if (LANGUAGES.length >= 2) {
    const comparison = compareLanguageStats(allStats[LANGUAGES[0]], allStats[LANGUAGES[1]])
    
    console.log('🔄 Confronto tra lingue:')
    console.log(`   📈 Coverage: ${comparison.coverage.toFixed(1)}%`)
    console.log(`   ❌ Mancanti in ${LANGUAGES[0]}: ${comparison.missingInFirst.length}`)
    console.log(`   ❌ Mancanti in ${LANGUAGES[1]}: ${comparison.missingInSecond.length}`)
    
    if (comparison.missingInFirst.length > 0) {
      console.log(`   📝 Prime 10 chiavi mancanti in ${LANGUAGES[0]}:`)
      comparison.missingInFirst.slice(0, 10).forEach(key => {
        console.log(`      - ${key}`)
      })
    }
    
    if (comparison.missingInSecond.length > 0) {
      console.log(`   📝 Prime 10 chiavi mancanti in ${LANGUAGES[1]}:`)
      comparison.missingInSecond.slice(0, 10).forEach(key => {
        console.log(`      - ${key}`)
      })
    }
    
    console.log('')
  }
}

/**
 * Genera un report per file
 */
function generateFileReport() {
  console.log('📁 Report per File\n')
  
  for (const lang of LANGUAGES) {
    console.log(`🌐 Lingua: ${lang.toUpperCase()}`)
    
    const files = getTranslationFiles(lang)
    const fileStats = files.map(filename => {
      const data = loadTranslationFile(lang, filename)
      const keys = Object.keys(data)
      const emptyValues = Object.entries(data).filter(([, value]) => !value || (typeof value === 'string' && value.trim() === '')).length
      
      return {
        filename,
        keyCount: keys.length,
        emptyValues,
        size: JSON.stringify(data).length
      }
    }).sort((a, b) => b.keyCount - a.keyCount)
    
    fileStats.forEach(file => {
      const status = file.emptyValues > 0 ? '⚠️' : '✅'
      console.log(`   ${status} ${file.filename}: ${file.keyCount} chiavi, ${file.emptyValues} vuote, ${file.size} bytes`)
    })
    
    console.log('')
  }
}

/**
 * Genera un report di qualità
 */
function generateQualityReport() {
  console.log('🎯 Report Qualità Traduzioni\n')
  
  const qualityIssues = []
  
  for (const lang of LANGUAGES) {
    const stats = analyzeLanguageStats(lang)
    
    // Problemi di qualità
    if (stats.emptyValues.length > 0) {
      qualityIssues.push({
        type: 'empty_values',
        language: lang,
        count: stats.emptyValues.length,
        severity: 'high'
      })
    }
    
    if (stats.longKeys.length > 0) {
      qualityIssues.push({
        type: 'long_keys',
        language: lang,
        count: stats.longKeys.length,
        severity: 'medium'
      })
    }
    
    if (stats.shortKeys.length > 0) {
      qualityIssues.push({
        type: 'short_keys',
        language: lang,
        count: stats.shortKeys.length,
        severity: 'low'
      })
    }
  }
  
  if (qualityIssues.length === 0) {
    console.log('✅ Nessun problema di qualità rilevato!')
    return
  }
  
  // Raggruppa per severità
  const bySeverity = {
    high: qualityIssues.filter(issue => issue.severity === 'high'),
    medium: qualityIssues.filter(issue => issue.severity === 'medium'),
    low: qualityIssues.filter(issue => issue.severity === 'low')
  }
  
  for (const [severity, issues] of Object.entries(bySeverity)) {
    if (issues.length === 0) continue
    
    const icon = severity === 'high' ? '🔴' : severity === 'medium' ? '🟡' : '🟢'
    console.log(`${icon} ${severity.toUpperCase()}: ${issues.length} problemi`)
    
    issues.forEach(issue => {
      console.log(`   - ${issue.language}: ${issue.count} ${issue.type}`)
    })
  }
  
  console.log('')
}

/**
 * Genera un file JSON con tutte le statistiche
 */
function generateJsonReport() {
  const allStats = {}
  for (const lang of LANGUAGES) {
    allStats[lang] = analyzeLanguageStats(lang)
  }
  
  const report = {
    generatedAt: new Date().toISOString(),
    languages: LANGUAGES,
    stats: allStats,
    comparison: LANGUAGES.length >= 2 ? compareLanguageStats(allStats[LANGUAGES[0]], allStats[LANGUAGES[1]]) : null
  }
  
  const reportPath = path.join(__dirname, '../translation-stats.json')
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8')
  console.log(`💾 Report JSON salvato: ${reportPath}`)
}

/**
 * Funzione principale
 */
function main() {
  console.log('🚀 Generazione statistiche traduzioni...')
  console.log(`📂 Directory: ${LOCALES_DIR}\n`)
  
  // Verifica che la directory esista
  if (!fs.existsSync(LOCALES_DIR)) {
    console.error('❌ Directory delle traduzioni non trovata!')
    process.exit(1)
  }
  
  // Genera i report
  generateDetailedReport()
  generateFileReport()
  generateQualityReport()
  generateJsonReport()
  
  console.log('✅ Statistiche generate con successo!')
  console.log('\n📝 Prossimi passi:')
  console.log('   1. Rivedi i problemi di qualità identificati')
  console.log('   2. Completa le traduzioni mancanti')
  console.log('   3. Ottimizza le chiavi troppo lunghe o corte')
  console.log('   4. Usa npm run i18n:consolidate per consolidare i file')
}

// Esegui se chiamato direttamente
if (require.main === module) {
  main()
}

module.exports = {
  analyzeLanguageStats,
  compareLanguageStats,
  generateDetailedReport,
  generateFileReport,
  generateQualityReport
}
