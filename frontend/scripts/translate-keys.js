const fs = require('fs');
const path = require('path');

// Dizionario di traduzioni comuni
const translations = {
  'Dettagli Tecnici': 'Technical Details',
  'Protocolli': 'Protocols',
  'Accesso Remoto': 'Remote Access',
  'Tipo di Accesso Remoto': 'Remote Access Type',
  'Facilità di Accesso Fisico': 'Physical Access Ease',
  'Interno': 'Internal',
  'Esterno': 'External',
  'Connessione di Rete': 'Network Connection',
  'Interfacce di Rete': 'Network Interfaces',
  'Informazioni di Rete': 'Network Information',
  'Etichetta Presa Fisica': 'Physical Plug Label',
  'Connessioni Fisiche': 'Physical Connections',
  'Aggiungi protocollo': 'Add Protocol',
  'Seleziona i protocolli industriali supportati da questa interfaccia': 'Select the industrial protocols supported by this interface',
  'Inserisci dettagli in formato JSON': 'Enter details in JSON format',
  'Seleziona protocolli supportati': 'Select supported protocols',
  'Interfacce di Rete': 'Network Interfaces',
  'Informazioni Principali': 'Main Information',
  'Informazioni Tecniche': 'Technical Information',
  'Informazioni di Sicurezza': 'Security Information',
  'Informazioni Posizione': 'Position Information',
  'Accesso Remoto Atteso': 'Attended Remote Access',
  'Accesso Remoto Non Atteso': 'Unattended Remote Access',
  'Nessun Accesso Remoto': 'No Remote Access',
  'Carica Connessione': 'Upload Connection',
  'Seleziona Connessione': 'Select Connection',
  'Connessione caricata con successo': 'Connection uploaded successfully',
  'Connessione eliminata con successo': 'Connection deleted successfully',
  'Errore nel caricamento della connessione': 'Error uploading connection',
  'Errore nell\'eliminazione della connessione': 'Error deleting connection',
  'Aggiungi Connessione': 'Add Connection',
  'Modifica Connessione': 'Edit Connection',
  'Elimina Connessione': 'Delete Connection',
  'Tipo di Connessione': 'Connection Type',
  'Dettagli Connessione': 'Connection Details',
  'Connessione aggiunta con successo': 'Connection added successfully',
  'Errore nell\'aggiunta della connessione': 'Error adding connection',
  'Connessione modificata con successo': 'Connection modified successfully',
  'Errore nella modifica della connessione': 'Error modifying connection',
  'Errore nel caricamento delle interfacce': 'Error loading interfaces',
  'Sei sicuro di voler eliminare questa connessione?': 'Are you sure you want to delete this connection?',
  'Etichetta Presa A': 'Plug Label A',
  'Etichetta Presa B': 'Plug Label B',
  'Facilità di accesso': 'Access Ease',
  'Informazioni Importanti': 'Important Information',
  'Seleziona Sito': 'Select Site',
  'Seleziona un sito prima di caricare i file': 'Please select a site before uploading files',
  'Seleziona File PCAP': 'Select PCAP Files',
  'File caricati con successo': 'Files uploaded successfully',
  'Errore nel caricamento dei siti': 'Error loading sites',
  'Errore durante il caricamento: ': 'Upload error: ',
  'Import completato con successo': 'Import completed successfully',
  'Operazione completata con successo': 'Operation completed successfully',
  'Errore': 'Error',
  'Errore nella lettura del file': 'Error reading file',
  'importati con successo': 'imported successfully',
  'Errore nel caricamento del dispositivo': 'Error loading device',
  'Errore nella creazione del dispositivo': 'Error creating device',
  'Errore nell\'aggiornamento del dispositivo': 'Error updating device',
  'Errore nell\'eliminazione del dispositivo': 'Error deleting device',
  'Aggiungi Interfaccia': 'Add Interface',
  'Aggiungi Multiple': 'Add Multiple',
  'Modifica Interfaccia': 'Edit Interface',
  'Dettagli': 'Details',
  'Aggiungi Protocollo': 'Add Protocol',
  'Caricamento Foto': 'Photo Upload',
  'Carica Foto': 'Upload Photo',
  'Seleziona Foto': 'Select Photo',
  'Foto caricata con successo': 'Photo uploaded successfully',
  'Foto eliminata con successo': 'Photo deleted successfully',
  'Errore nel caricamento della foto': 'Error uploading photo',
  'Errore nell\'eliminazione della foto': 'Error deleting photo',
  'Errore nel caricamento delle foto': 'Error loading photos',
  'Carica': 'Upload',
  'Foto caricate con successo': 'Photos uploaded successfully',
  'Carica Documento': 'Upload Document',
  'Seleziona Documento': 'Select Document',
  'Documento caricato con successo': 'Document uploaded successfully',
  'Documento eliminato con successo': 'Document deleted successfully',
  'Errore nel caricamento del documento': 'Error uploading document',
  'Errore nell\'eliminazione del documento': 'Error deleting document',
  'Errore nel caricamento dei documenti': 'Error loading documents',
  'Documenti caricati con successo': 'Documents uploaded successfully',
  'Carica Documenti': 'Upload Documents',
  'Errore nel caricamento delle connessioni': 'Error loading connections',
  'Interfaccia Locale': 'Local Interface',
  'Interfaccia Remota': 'Remote Interface',
  'Errore nel caricamento degli asset': 'Error loading assets',
  'Interfaccia A': 'Interface A',
  'Interfaccia B': 'Interface B',
  'Elimina': 'Delete',
  'Aggiungi Campo': 'Add Field',
  'Errore nel salvataggio dei campi personalizzati': 'Error saving custom fields',
  'Nessun campo personalizzato': 'No custom fields',
  'Nessun dato disponibile per la tabella': 'No data available for table',
  'Nessun dato disponibile per il grafico': 'No data available for chart',
  'Aggiungi Comunicazione': 'Add Communication',
  'Seleziona Comunicazione': 'Select Communication',
  'Comunicazione caricata con successo': 'Communication uploaded successfully',
  'Comunicazione eliminata con successo': 'Communication deleted successfully',
  'Errore nel caricamento della comunicazione': 'Error uploading communication',
  'Errore nell\'eliminazione della comunicazione': 'Error deleting communication',
  'Errore nel caricamento delle comunicazioni': 'Error loading communications',
  'Aggiungi Evento': 'Add Event',
  'Seleziona Evento': 'Select Event',
  'Evento caricato con successo': 'Event uploaded successfully',
  'Evento eliminato con successo': 'Event deleted successfully',
  'Errore nel caricamento dell\'evento': 'Error uploading event',
  'Errore nell\'eliminazione dell\'evento': 'Error deleting event',
  'Errore nel caricamento degli eventi': 'Error loading events',
  'Errore nel caricamento degli utenti': 'Error loading users',
  'Seleziona azione': 'Select action',
  'Seleziona utente': 'Select user',
  'Seleziona intervallo date': 'Select date range',
  'Nessuna modifica trovata per questo asset': 'No changes found for this asset',
  'Modifica': 'Update',
  'Nessuna modifica rilevata': 'No changes detected',
  'Aggiungi contatti': 'Add contacts',
  'Nessun contatto associato': 'No contacts associated',
  'Aggiungi nota': 'Add note',
  'Nessuna nota associata': 'No notes associated',
  'Modifica nota': 'Edit note',
  'Errore nel caricamento dei ruoli': 'Error loading roles',
  'Errore nella creazione dell\'utente': 'Error creating user',
  'Errore nell\'aggiornamento dell\'utente': 'Error updating user',
  'Errore nell\'eliminazione dell\'utente': 'Error deleting user',
  'Errore nell\'aggiornamento di massa degli utenti': 'Error in bulk update of users',
  'Attivo': 'Active',
  'Inattivo': 'Inactive',
  'Seleziona ruolo padre': 'Select parent role',
  'Errore nell\'eliminazione del ruolo': 'Error deleting role',
  'Errore nell\'aggiornamento del ruolo': 'Error updating role',
  'Errore nella creazione del ruolo': 'Error creating role',
  'Errore nel test dei permessi': 'Error testing permissions',
  'Permessi aggiornati con successo': 'Permissions updated successfully',
  'Errore nell\'aggiornamento dei permessi': 'Error updating permissions',
  'Informazioni Base': 'Basic Information',
  'Nessuno': 'None',
  'Eliminazione': 'Deletion',
  'Ruolo aggiornato con successo': 'Role updated successfully',
  'Ruolo creato con successo': 'Role created successfully',
  'Errore durante il salvataggio del ruolo': 'Error saving role',
  'Nessun accesso alle risorse': 'No access to resources',
  'Ultimo Accesso': 'Last Login',
  'Informazioni Utente': 'User Information',
  'Password aggiornata con successo': 'Password updated successfully',
  'Errore durante il reset della password': 'Error resetting password',
  'Errore nel caricamento del profilo utente': 'Error loading user profile',
  'Attenzione': 'Warning',
  'Carica nuova planimetria': 'Upload new floorplan',
  'Nessun file selezionato': 'No file selected',
  'Errore durante il caricamento': 'Error during upload',
  'Nessun file planimetria': 'No floorplan file',
  'Contatti importati con successo': 'Contacts imported successfully',
  'Produttori importati con successo': 'Manufacturers imported successfully',
  'Test Permessi': 'Test Permissions',
  'Aggiorna Permessi': 'Refresh Permissions',
  'Permessi': 'Permissions',
  'Ruolo Padre': 'Parent Role',
  'Contatti': 'Contacts',
  'Produttori': 'Manufacturers',
  'Reset Password Utenti': 'Reset User Password',
  'Può resettare la password di altri utenti': 'Can reset passwords of other users',
  'Ruolo': 'Role',
  'Inserisci la password attuale e la nuova password per aggiornare le tue credenziali di accesso.': 'Enter your current password and new password to update your login credentials.',
  'Password Attuale': 'Current Password',
  'Nuova Password': 'New Password',
  'Conferma Password': 'Confirm Password',
  // Aggiungi altre traduzioni comuni qui
};

// Funzione per tradurre una stringa
function translateString(str) {
  // Se inizia con [IT], rimuovilo
  if (str.startsWith('[IT]')) {
    return str.replace('[IT]', '').trim();
  }
  
  // Se contiene [TO_TRANSLATE], rimuovilo
  if (str.includes('[TO_TRANSLATE]')) {
    str = str.replace('[TO_TRANSLATE]', '').trim();
  }
  
  // Cerca nel dizionario
  if (translations[str]) {
    return translations[str];
  }
  
  // Se non trovato, restituisci la stringa originale (sarà tradotta manualmente)
  return str;
}

// Funzione per tradurre un oggetto ricorsivamente
function translateObject(obj) {
  if (typeof obj === 'string') {
    return translateString(obj);
  } else if (Array.isArray(obj)) {
    return obj.map(translateObject);
  } else if (obj && typeof obj === 'object') {
    const translated = {};
    for (const key in obj) {
      translated[key] = translateObject(obj[key]);
    }
    return translated;
  }
  return obj;
}

// Directory delle traduzioni
const localesDir = path.join(__dirname, '../src/locales');
const enDir = path.join(localesDir, 'en');

// Ottieni tutti i file JSON inglesi
const enFiles = fs.readdirSync(enDir).filter(file => file.endsWith('.json'));

console.log('Translating Italian keys in English files...\n');

let translatedCount = 0;
for (const enFile of enFiles) {
  const enPath = path.join(enDir, enFile);
  const content = JSON.parse(fs.readFileSync(enPath, 'utf8'));
  const translated = translateObject(content);
  
  // Controlla se ci sono state modifiche
  const originalStr = JSON.stringify(content);
  const translatedStr = JSON.stringify(translated);
  
  if (originalStr !== translatedStr) {
    fs.writeFileSync(enPath, JSON.stringify(translated, null, 2) + '\n', 'utf8');
    console.log(`✓ Translated keys in ${enFile}`);
    translatedCount++;
  }
}

console.log(`\n✓ Translation complete! ${translatedCount} files updated.`);
console.log('\n⚠️  Note: Some keys may still need manual translation.');

