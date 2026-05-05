import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/store/auth'
import api from '@/api/api'

export function useGlobalSearch() {
  const router = useRouter()
  const toast = useToast()
  const auth = useAuthStore()
  
  const searchQuery = ref('')
  const searchResults = ref([])
  const isLoading = ref(false)
  const isVisible = ref(false)
  
  const hasResults = computed(() => searchResults.value.length > 0)
  
  const search = async (query) => {
    const trimmedQuery = query ? query.trim() : ''
    if (!trimmedQuery || trimmedQuery.length < 2) {
      searchResults.value = []
      return
    }
    
    // Verifica che l'utente sia autenticato
    if (!auth.isAuthenticated) {
      toast.add({
        severity: 'warn',
        summary: 'Attenzione',
        detail: 'Devi essere autenticato per utilizzare la ricerca',
        life: 3000
      })
      return
    }
    
    isLoading.value = true
    
    try {
      const response = await api.globalSearch(trimmedQuery, 5)
      // La risposta API ha struttura { results: [...] }
      searchResults.value = response.data?.results || []
      console.log('Search results:', searchResults.value)
    } catch (error) {
      console.error('Errore durante la ricerca:', error)
      console.error('Error response:', error.response?.data)
      toast.add({
        severity: 'error',
        summary: 'Errore',
        detail: error.response?.data?.detail || 'Errore durante la ricerca',
        life: 3000
      })
      searchResults.value = []
    } finally {
      isLoading.value = false
    }
  }
  
  const handleSearch = async () => {
    const query = searchQuery.value?.trim() || ''
    if (query.length >= 2) {
      await search(query)
    } else {
      searchResults.value = []
    }
  }
  
  const handleResultClick = (result) => {
    router.push(result.url)
    isVisible.value = false
    searchQuery.value = ''
    searchResults.value = []
  }
  
  const handleKeydown = (event) => {
    if (event.key === 'Enter' && searchQuery.value.trim()) {
      handleSearch()
    } else if (event.key === 'Escape') {
      isVisible.value = false
      searchQuery.value = ''
      searchResults.value = []
    }
  }
  
  const openSearch = () => {
    isVisible.value = true
    // Focus sull'input dopo che il dialog è aperto
    setTimeout(() => {
      const input = document.querySelector('.global-search-input')
      if (input) {
        input.focus()
      }
    }, 100)
  }
  
  const closeSearch = () => {
    isVisible.value = false
    searchQuery.value = ''
    searchResults.value = []
  }
  
  return {
    searchQuery,
    searchResults,
    isLoading,
    isVisible,
    hasResults,
    search,
    handleSearch,
    handleResultClick,
    handleKeydown,
    openSearch,
    closeSearch
  }
} 