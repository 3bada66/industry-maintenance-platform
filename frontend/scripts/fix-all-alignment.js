#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔧 Correzione allineamento tutti i file...');

const localesDir = path.join(__dirname, '../src/locales');
const files = ['core.json', 'assets.json', 'entities.json', 'features.json', 'ui.json', 'examples.json'];

files.forEach(file => {
  console.log(`\n📁 Processando ${file}...`);
  
  const enPath = path.join(localesDir, 'en', file);
  const itPath = path.join(localesDir, 'it', file);
  
  if (!fs.existsSync(enPath) || !fs.existsSync(itPath)) {
    console.log(`⚠️  File ${file} non trovato, salto...`);
    return;
  }
  
  const enData = JSON.parse(fs.readFileSync(enPath, 'utf8'));
  const itData = JSON.parse(fs.readFileSync(itPath, 'utf8'));
  
  console.log(`📊 EN: ${Object.keys(enData).length} chiavi`);
  console.log(`📊 IT: ${Object.keys(itData).length} chiavi`);
  
  // Trova chiavi che esistono in IT ma non in EN
  const enKeys = new Set(Object.keys(enData));
  const itKeys = Object.keys(itData);
  const keysToRemove = itKeys.filter(key => !enKeys.has(key));
  
  if (keysToRemove.length > 0) {
    console.log(`❌ Chiavi da rimuovere da IT: ${keysToRemove.length}`);
    
    // Rimuovi chiavi non presenti in EN
    keysToRemove.forEach(key => {
      delete itData[key];
    });
    
    // Salva file corretto
    fs.writeFileSync(itPath, JSON.stringify(itData, null, 2) + '\n');
    
    console.log(`✅ Rimosse ${keysToRemove.length} chiavi da IT`);
    console.log(`📊 IT aggiornato: ${Object.keys(itData).length} chiavi`);
  } else {
    console.log('✅ Nessuna chiave da rimuovere');
  }
});

console.log('\n🎉 Correzione completata per tutti i file!');
