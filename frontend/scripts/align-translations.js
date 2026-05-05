#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔄 Avvio allineamento traduzioni...');

const localesDir = path.join(__dirname, '../src/locales');
const languages = ['en', 'it'];

// Carica tutte le traduzioni
const translations = {};
languages.forEach(lang => {
  translations[lang] = {};
  const langDir = path.join(localesDir, lang);
  const files = fs.readdirSync(langDir).filter(f => f.endsWith('.json'));
  
  files.forEach(file => {
    const filePath = path.join(langDir, file);
    const content = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    translations[lang][file] = content;
  });
});

// Trova chiavi mancanti
const allKeys = new Set();
Object.values(translations).forEach(langTranslations => {
  Object.values(langTranslations).forEach(fileTranslations => {
    Object.keys(fileTranslations).forEach(key => allKeys.add(key));
  });
});

console.log(`📊 Chiavi totali trovate: ${allKeys.size}`);

// Allinea traduzioni
languages.forEach(lang => {
  const missingKeys = [];
  
  Object.keys(translations[lang]).forEach(file => {
    const fileTranslations = translations[lang][file];
    
    allKeys.forEach(key => {
      if (!fileTranslations.hasOwnProperty(key)) {
        missingKeys.push({ file, key });
      }
    });
  });
  
  console.log(`🌐 ${lang.toUpperCase()}: ${missingKeys.length} chiavi mancanti`);
  
  if (missingKeys.length > 0) {
    console.log(`📝 Prime 10 chiavi mancanti in ${lang}:`);
    missingKeys.slice(0, 10).forEach(({ file, key }) => {
      console.log(`   - ${file}: ${key}`);
    });
  }
});

console.log('✅ Analisi completata!');
console.log('💡 Per allineare:');
console.log('   1. Copia chiavi mancanti da una lingua all\'altra');
console.log('   2. Traduci manualmente per qualità');
console.log('   3. Usa servizi di traduzione automatica se necessario');
