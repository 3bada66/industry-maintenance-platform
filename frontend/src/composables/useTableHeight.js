import { ref, computed, onMounted, onUnmounted } from 'vue'

export function useTableHeight(options = {}) {
  const {
    offsetTop = 0,      // Offset dall'alto (header, filtri, etc.)
    offsetBottom = 0,   // Offset dal basso (footer, paginazione, etc.)
    minHeight = '400px', // Altezza minima
    maxHeight = '80vh',  // Altezza massima
    container = null     // Container di riferimento (default: window)
  } = options

  const containerHeight = ref(0)
  const tableHeight = ref('75vh')

  // Calcola l'altezza disponibile
  const calculateHeight = () => {
    const targetContainer = container || window
    const height = targetContainer === window 
      ? window.innerHeight 
      : targetContainer.offsetHeight

    containerHeight.value = height

    // Calcola l'altezza disponibile per la tabella
    const availableHeight = height - offsetTop - offsetBottom
    
    // Se l'altezza disponibile è molto grande, non limitare
    if (availableHeight > 800) {
      tableHeight.value = 'auto'
      return
    }
    
    // Converti in viewport height
    const vhHeight = (availableHeight / window.innerHeight) * 100
    
    // Applica i limiti
    const finalVh = Math.max(50, Math.min(80, vhHeight))
    
    tableHeight.value = `${finalVh}vh`
  }

  // Computed per l'altezza CSS
  const tableHeightStyle = computed(() => ({
    height: tableHeight.value,
    minHeight,
    maxHeight
  }))

  // Gestione resize
  const handleResize = () => {
    calculateHeight()
  }

  onMounted(() => {
    calculateHeight()
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })

  return {
    tableHeight,
    tableHeightStyle,
    containerHeight,
    calculateHeight
  }
} 