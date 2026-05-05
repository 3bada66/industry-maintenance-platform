const fs = require('fs');
const path = require('path');

// Funzione per ottenere tutte le chiavi da un oggetto (ricorsiva)
function getAllKeys(obj, prefix = '') {
  const keys = [];
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const fullKey = prefix ? `${prefix}.${key}` : key;
      if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
        keys.push(...getAllKeys(obj[key], fullKey));
      } else {
        keys.push(fullKey);
      }
    }
  }
  return keys;
}

// Funzione per ottenere il valore da un percorso chiave annidato
function getNestedValue(obj, keyPath) {
  const keys = keyPath.split('.');
  let value = obj;
  for (const key of keys) {
    if (value && typeof value === 'object' && key in value) {
      value = value[key];
    } else {
      return undefined;
    }
  }
  return value;
}

// Funzione per impostare un valore in un percorso chiave annidato
function setNestedValue(obj, keyPath, value) {
  const keys = keyPath.split('.');
  let current = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i];
    if (!(key in current) || typeof current[key] !== 'object' || current[key] === null) {
      current[key] = {};
    }
    current = current[key];
  }
  current[keys[keys.length - 1]] = value;
}

// Funzione per tradurre una stringa (placeholder - dovrebbe usare un servizio di traduzione)
function translateString(itString) {
  // Per ora, restituiamo un placeholder che indica che va tradotto
  // In un caso reale, useresti un servizio di traduzione o un dizionario
  if (itString.startsWith('[IT]')) {
    return itString.replace('[IT]', '[EN]');
  }
  // Se contiene già una traduzione placeholder, la manteniamo
  return `[TO_TRANSLATE] ${itString}`;
}

// Funzione principale per sincronizzare le traduzioni
function syncTranslations(itFile, enFile) {
  const itContent = JSON.parse(fs.readFileSync(itFile, 'utf8'));
  const enContent = fs.existsSync(enFile) ? JSON.parse(fs.readFileSync(enFile, 'utf8')) : {};
  
  const itKeys = getAllKeys(itContent);
  const enKeys = getAllKeys(enContent);
  
  const missingKeys = itKeys.filter(key => !enKeys.includes(key));
  
  if (missingKeys.length === 0) {
    console.log(`✓ ${path.basename(enFile)}: All keys present`);
    return false;
  }
  
  console.log(`\n${path.basename(enFile)}: Adding ${missingKeys.length} missing keys:`);
  
  // Aggiungi le chiavi mancanti
  for (const key of missingKeys) {
    const itValue = getNestedValue(itContent, key);
    // Se il valore italiano inizia con [IT], lo traduciamo
    // Altrimenti, manteniamo il valore esistente se presente, o aggiungiamo un placeholder
    const enValue = typeof itValue === 'string' && itValue.startsWith('[IT]') 
      ? translateString(itValue)
      : (getNestedValue(enContent, key) || itValue);
    
    setNestedValue(enContent, key, enValue);
    console.log(`  + ${key}: ${enValue}`);
  }
  
  // Scrivi il file aggiornato
  fs.writeFileSync(enFile, JSON.stringify(enContent, null, 2) + '\n', 'utf8');
  return true;
}

// Directory delle traduzioni
const localesDir = path.join(__dirname, '../src/locales');
const itDir = path.join(localesDir, 'it');
const enDir = path.join(localesDir, 'en');

// Ottieni tutti i file JSON italiani
const itFiles = fs.readdirSync(itDir).filter(file => file.endsWith('.json'));

console.log('Synchronizing translation files...\n');

let updatedCount = 0;
for (const itFile of itFiles) {
  const itPath = path.join(itDir, itFile);
  const enPath = path.join(enDir, itFile);
  
  if (syncTranslations(itPath, enPath)) {
    updatedCount++;
  }
}

console.log(`\n✓ Synchronization complete! ${updatedCount} files updated.`);
console.log('\n⚠️  Note: Keys marked with [TO_TRANSLATE] need manual translation.');
