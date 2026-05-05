#!/usr/bin/env node

/**
 * Script per trovare stringhe hardcoded nei componenti Vue
 * Aiuta a identificare testo che dovrebbe essere tradotto
 */

const fs = require('fs')
const path = require('path')

// Directory da analizzare
const SRC_DIR = path.join(__dirname, '../src')
const COMPONENTS_DIR = path.join(SRC_DIR, 'components')
const PAGES_DIR = path.join(SRC_DIR, 'pages')

// Pattern per trovare stringhe hardcoded
const HARDCODED_PATTERNS = [
  // Stringhe tra virgolette doppie
  /"[^"]*[a-zA-ZÀ-ÿ][^"]*"/g,
  // Stringhe tra virgolette singole
  /'[^']*[a-zA-ZÀ-ÿ][^']*'/g,
  // Template literals
  /`[^`]*[a-zA-ZÀ-ÿ][^`]*`/g
]

// Pattern per escludere stringhe che non dovrebbero essere tradotte
const EXCLUDE_PATTERNS = [
  // URL, path, classi CSS
  /^(https?:\/\/|\.\/|\/|class=|id=|src=|href=|action=)/,
  // Numeri, date, codici
  /^[\d\s\-\.:]+$/,
  // Variabili, funzioni, codice
  /^[a-zA-Z_$][a-zA-Z0-9_$]*$/,
  // Stringhe molto corte
  /^.{1,2}$/,
  // Stringhe con solo caratteri speciali
  /^[^a-zA-ZÀ-ÿ]*$/,
  // Stringhe già tradotte (contengono $t o t()
  /\$t\(|t\(/,
  // Commenti
  /^\/\/|\/\*|\*\/$/
]

// Parole comuni che potrebbero essere hardcoded
const COMMON_HARDCODED_WORDS = [
  'Create', 'Edit', 'Delete', 'Save', 'Cancel', 'Close', 'Back', 'Next', 'Previous',
  'Add', 'Remove', 'Update', 'View', 'Search', 'Filter', 'Clear', 'Refresh',
  'Export', 'Import', 'Download', 'Upload', 'Print', 'Restore', 'Duplicate',
  'Active', 'Inactive', 'Online', 'Offline', 'Enabled', 'Disabled',
  'Name', 'Description', 'Email', 'Phone', 'Address', 'City', 'Country',
  'Status', 'Type', 'Category', 'Priority', 'Date', 'Time',
  'Success', 'Error', 'Warning', 'Info', 'Loading', 'Please', 'Confirm',
  'Yes', 'No', 'OK', 'Cancel', 'Apply', 'Reset', 'Submit'
]

/**
 * Controlla se una stringa dovrebbe essere esclusa
 */
function shouldExcludeString(str) {
  // Rimuovi virgolette
  const cleanStr = str.replace(/^['"`]|['"`]$/g, '')
  
  // Controlla pattern di esclusione
  for (const pattern of EXCLUDE_PATTERNS) {
    if (pattern.test(cleanStr)) {
      return true
    }
  }
  
  // Controlla se è una parola comune
  if (COMMON_HARDCODED_WORDS.includes(cleanStr)) {
    return false // Non escludere, potrebbe essere hardcoded
  }
  
  return false
}

/**
 * Analizza un file Vue per stringhe hardcoded
 */
function analyzeVueFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8')
  const issues = []
  
  // Trova tutte le stringhe
  for (const pattern of HARDCODED_PATTERNS) {
    let match
    while ((match = pattern.exec(content)) !== null) {
      const str = match[0]
      
      if (!shouldExcludeString(str)) {
        const lineNumber = content.substring(0, match.index).split('\n').length
        issues.push({
          string: str,
          line: lineNumber,
          context: getContext(content, match.index, 50)
        })
      }
    }
  }
  
  return issues
}

/**
 * Ottieni il contesto intorno a una posizione nel file
 */
function getContext(content, position, contextLength) {
  const start = Math.max(0, position - contextLength)
  const end = Math.min(content.length, position + contextLength)
  return content.substring(start, end).replace(/\n/g, '\\n')
}

/**
 * Analizza ricorsivamente una directory
 */
function analyzeDirectory(dirPath, results = []) {
  if (!fs.existsSync(dirPath)) {
    return results
  }
  
  const items = fs.readdirSync(dirPath)
  
  for (const item of items) {
    const itemPath = path.join(dirPath, item)
    const stat = fs.statSync(itemPath)
    
    if (stat.isDirectory()) {
      // Salta node_modules e altre directory non rilevanti
      if (!['node_modules', '.git', 'dist', 'build'].includes(item)) {
        analyzeDirectory(itemPath, results)
      }
    } else if (item.endsWith('.vue') || item.endsWith('.js')) {
      const issues = analyzeVueFile(itemPath)
      if (issues.length > 0) {
        results.push({
          file: path.relative(SRC_DIR, itemPath),
          issues
        })
      }
    }
  }
  
  return results
}

/**
 * Genera un report delle stringhe hardcoded
 */
function generateReport(results) {
  console.log('🔍 Report Stringhe Hardcoded\n')
  
  let totalIssues = 0
  let totalFiles = 0
  
  for (const fileResult of results) {
    totalFiles++
    totalIssues += fileResult.issues.length
    
    console.log(`📁 ${fileResult.file}`)
    console.log(`   ${fileResult.issues.length} stringhe potenzialmente hardcoded`)
    
    // Mostra le prime 5 stringhe per file
    fileResult.issues.slice(0, 5).forEach(issue => {
      console.log(`   Linea ${issue.line}: ${issue.string}`)
      console.log(`   Contesto: ...${issue.context}...`)
    })
    
    if (fileResult.issues.length > 5) {
      console.log(`   ... e altre ${fileResult.issues.length - 5} stringhe`)
    }
    
    console.log('')
  }
  
  console.log(`📊 Statistiche:`)
  console.log(`   - File analizzati: ${totalFiles}`)
  console.log(`   - Stringhe hardcoded trovate: ${totalIssues}`)
  console.log(`   - Media per file: ${(totalIssues / totalFiles).toFixed(1)}`)
}

/**
 * Genera un file JSON con i risultati
 */
function generateJsonReport(results) {
  const reportPath = path.join(__dirname, '../hardcoded-strings-report.json')
  fs.writeFileSync(reportPath, JSON.stringify(results, null, 2) + '\n', 'utf8')
  console.log(`\n💾 Report salvato: ${reportPath}`)
}

/**
 * Genera suggerimenti per le chiavi di traduzione
 */
function generateTranslationSuggestions(results) {
  console.log('\n💡 Suggerimenti per chiavi di traduzione:\n')
  
  const suggestions = new Map()
  
  for (const fileResult of results) {
    for (const issue of fileResult.issues) {
      const str = issue.string.replace(/^['"`]|['"`]$/g, '')
      const key = generateTranslationKey(str, fileResult.file)
      
      if (!suggestions.has(key)) {
        suggestions.set(key, {
          key,
          originalString: str,
          files: [],
          suggestedTranslation: str // Inizialmente uguale all'originale
        })
      }
      
      suggestions.get(key).files.push(fileResult.file)
    }
  }
  
  // Mostra i primi 20 suggerimenti
  let count = 0
  for (const [key, suggestion] of suggestions) {
    if (count >= 20) break
    
    console.log(`🔑 ${key}`)
    console.log(`   Originale: "${suggestion.originalString}"`)
    console.log(`   File: ${suggestion.files.join(', ')}`)
    console.log(`   Suggerimento: "${suggestion.suggestedTranslation}"`)
    console.log('')
    
    count++
  }
  
  if (suggestions.size > 20) {
    console.log(`... e altri ${suggestions.size - 20} suggerimenti`)
  }
}

/**
 * Genera una chiave di traduzione da una stringa
 */
function generateTranslationKey(str, filePath) {
  // Rimuovi caratteri speciali e converti in camelCase
  const cleanStr = str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9\s]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
  
  // Prendi le prime 3-4 parole
  const words = cleanStr.split(' ').slice(0, 4)
  
  // Converti in camelCase
  const key = words.map((word, index) => {
    if (index === 0) return word
    return word.charAt(0).toUpperCase() + word.slice(1)
  }).join('')
  
  // Aggiungi prefisso basato sul file
  const filePrefix = getFilePrefix(filePath)
  
  return `${filePrefix}${key}`
}

/**
 * Ottieni un prefisso basato sul file
 */
function getFilePrefix(filePath) {
  if (filePath.includes('components/forms/')) return 'forms.'
  if (filePath.includes('components/dialogs/')) return 'dialogs.'
  if (filePath.includes('components/tables/')) return 'tables.'
  if (filePath.includes('pages/')) return 'pages.'
  if (filePath.includes('components/')) return 'components.'
  return 'common.'
}

/**
 * Funzione principale
 */
function main() {
  console.log('🚀 Avvio analisi stringhe hardcoded...')
  console.log(`📂 Directory: ${SRC_DIR}\n`)
  
  // Analizza componenti e pagine
  const componentResults = analyzeDirectory(COMPONENTS_DIR)
  const pageResults = analyzeDirectory(PAGES_DIR)
  
  const allResults = [...componentResults, ...pageResults]
  
  if (allResults.length === 0) {
    console.log('✅ Nessuna stringa hardcoded trovata!')
    return
  }
  
  // Genera report
  generateReport(allResults)
  
  // Genera file JSON
  generateJsonReport(allResults)
  
  // Genera suggerimenti
  generateTranslationSuggestions(allResults)
  
  console.log('\n✅ Analisi completata!')
  console.log('\n📝 Prossimi passi:')
  console.log('   1. Rivedi le stringhe hardcoded identificate')
  console.log('   2. Sostituisci con chiavi di traduzione appropriate')
  console.log('   3. Aggiungi le traduzioni ai file JSON')
  console.log('   4. Testa l\'applicazione')
}

// Esegui se chiamato direttamente
if (require.main === module) {
  main()
}

module.exports = {
  analyzeVueFile,
  analyzeDirectory,
  generateTranslationKey,
  shouldExcludeString
}
