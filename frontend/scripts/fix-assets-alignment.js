#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔧 Correzione allineamento assets.json...');

const localesDir = path.join(__dirname, '../src/locales');

// Carica traduzioni EN come riferimento
const enAssets = JSON.parse(fs.readFileSync(path.join(localesDir, 'en/assets.json'), 'utf8'));
const itAssets = JSON.parse(fs.readFileSync(path.join(localesDir, 'it/assets.json'), 'utf8'));

console.log(`📊 EN: ${Object.keys(enAssets).length} chiavi`);
console.log(`📊 IT: ${Object.keys(itAssets).length} chiavi`);

// Trova chiavi che esistono in IT ma non in EN
const enKeys = new Set(Object.keys(enAssets));
const itKeys = Object.keys(itAssets);
const keysToRemove = itKeys.filter(key => !enKeys.has(key));

console.log(`❌ Chiavi da rimuovere da IT: ${keysToRemove.length}`);

if (keysToRemove.length > 0) {
  console.log('📝 Prime 10 chiavi da rimuovere:');
  keysToRemove.slice(0, 10).forEach(key => {
    console.log(`   - ${key}: "${itAssets[key]}"`);
  });
  
  // Rimuovi chiavi non presenti in EN
  keysToRemove.forEach(key => {
    delete itAssets[key];
  });
  
  // Salva file corretto
  fs.writeFileSync(
    path.join(localesDir, 'it/assets.json'), 
    JSON.stringify(itAssets, null, 2) + '\n'
  );
  
  console.log(`✅ Rimosse ${keysToRemove.length} chiavi da IT`);
  console.log(`📊 IT aggiornato: ${Object.keys(itAssets).length} chiavi`);
} else {
  console.log('✅ Nessuna chiave da rimuovere');
}

console.log('🎉 Correzione completata!');
