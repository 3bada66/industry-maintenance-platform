export function useStatus() {
  // Mappa colori comuni a severity PrimeVue
  const colorToSeverityMap = {
    // Verdi - Success
    '#28a745': 'success',
    '#22c55e': 'success',
    '#16a34a': 'success',
    '#15803d': 'success',
    'green': 'success',
    
    // Rossi - Danger
    '#dc3545': 'danger',
    '#ef4444': 'danger',
    '#f87171': 'danger',
    '#dc2626': 'danger',
    'red': 'danger',
    
    // Arancioni - Warning
    '#fd7e14': 'warning',
    '#f97316': 'warning',
    '#fb923c': 'warning',
    '#ea580c': 'warning',
    'orange': 'warning',
    
    // Grigi - Secondary
    '#6c757d': 'secondary',
    '#64748b': 'secondary',
    '#94a3b8': 'secondary',
    '#475569': 'secondary',
    'gray': 'secondary',
    'grey': 'secondary',
    
    // Blu - Info
    '#0d6efd': 'info',
    '#3b82f6': 'info',
    '#60a5fa': 'info',
    '#2563eb': 'info',
    'blue': 'info'
  }

  function getStatusSeverity(status) {
    if (!status) return 'info'
    
    // Se lo status ha un colore definito, usalo per determinare la severity
    if (status.color) {
      const color = status.color.toLowerCase()
      
      // Cerca corrispondenza esatta
      if (colorToSeverityMap[color]) {
        return colorToSeverityMap[color]
      }
      
      // Cerca corrispondenza parziale
      for (const [colorKey, severity] of Object.entries(colorToSeverityMap)) {
        if (color.includes(colorKey) || colorKey.includes(color)) {
          return severity
        }
      }
    }
    
    // Fallback basato sul nome se non c'è colore o non è stato trovato
    const statusName = status.name?.toLowerCase() || ''
    
    // Mappa nomi comuni a severity - corrispondenza esatta
    const nameToSeverityMap = {
      'active': 'success',
      'attivo': 'success',
      'operational': 'success',
      'operativo': 'success',
      'running': 'success',
      'inactive': 'secondary',
      'inattivo': 'secondary',
      'stopped': 'secondary',
      'maintenance': 'warning',
      'manutenzione': 'warning',
      'repair': 'warning',
      'riparazione': 'warning',
      'fault': 'danger',
      'guasto': 'danger',
      'faulty': 'danger',
      'error': 'danger',
      'errore': 'danger',
      'disposed': 'secondary',
      'smaltito': 'secondary',
      'stock': 'info',
      'magazzino': 'info',
      'in stock': 'info',
      'in magazzino': 'info'
    }
    
    // Prima cerca corrispondenza esatta
    if (nameToSeverityMap[statusName]) {
      return nameToSeverityMap[statusName]
    }
    
    // Poi cerca corrispondenze parziali
    for (const [nameKey, severity] of Object.entries(nameToSeverityMap)) {
      if (statusName.includes(nameKey)) {
        return severity
      }
    }
    
    return 'info'
  }

  function getStatusColor(status) {
    if (!status) return '#64748b'
    return status.color || '#64748b'
  }

  function getStatusLabel(status) {
    if (!status) return '-'
    return status.name || '-'
  }

  function getStatusStyle(status) {
    if (!status) return {}
    
    const color = getStatusColor(status)
    return {
      background: color,
      color: getContrastColor(color),
      padding: '0.2rem 0.5rem',
      borderRadius: '4px',
      fontSize: '0.875rem',
      fontWeight: '500'
    }
  }

  // Funzione per determinare il colore del testo basato sul colore di sfondo
  function getContrastColor(hexColor) {
    // Rimuovi il # se presente
    const hex = hexColor.replace('#', '')
    
    // Converti in RGB
    const r = parseInt(hex.substr(0, 2), 16)
    const g = parseInt(hex.substr(2, 2), 16)
    const b = parseInt(hex.substr(4, 2), 16)
    
    // Calcola la luminosità
    const brightness = (r * 299 + g * 587 + b * 114) / 1000
    
    // Ritorna bianco o nero basato sulla luminosità
    return brightness > 128 ? '#000000' : '#ffffff'
  }

  return {
    getStatusSeverity,
    getStatusColor,
    getStatusLabel,
    getStatusStyle,
    getContrastColor,
    colorToSeverityMap
  }
} 