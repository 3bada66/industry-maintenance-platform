<template>
  <transition name="fade">
    <div v-if="isVisible" class="spotlight-overlay" @mousedown.self="closeSearch">
      <div class="spotlight-modal" ref="modal">
        <div class="spotlight-input-wrapper">
          <i class="pi pi-search search-icon" />
          <input
            ref="input"
            v-model="searchQuery"
            :placeholder="t('globalsearch.strings.placeholder')"
            class="spotlight-input global-search-input"
            @keydown.down.prevent="moveSelection(1)"
            @keydown.up.prevent="moveSelection(-1)"
            @keydown.enter.prevent="selectCurrent"
            @keydown.esc.prevent="closeSearch"
            @input="handleSearch"
            autocomplete="off"
            spellcheck="false"
          />
          <div v-if="isLoading" class="loading-spinner">
            <i class="pi pi-spin pi-spinner" />
          </div>
        </div>
        <div class="spotlight-results">
          <template v-if="searchResults.length">
            <template v-for="(group, idx) in groupedResults" :key="group.type">
              <div class="spotlight-group-label">{{ t('globalsearch.types.' + group.type) }}</div>
              <div v-for="(item, i) in group.items" :key="item.id"
                :class="['spotlight-result', { selected: isSelected(idx, i) }]"
                @mousedown.prevent="select(idx, i)"
              >
                <i :class="['result-icon', iconForType(group.type)]" />
                <span class="result-title" v-html="highlight(item.title)"></span>
                <span class="result-desc" v-if="item.desc" v-html="highlight(item.desc)"></span>
              </div>
            </template>
          </template>
          <div v-else-if="searchQuery && !isLoading" class="spotlight-no-results">
            <i class="pi pi-info-circle" />
            {{ t('globalsearch.strings.noResults') }}
          </div>
          <div v-else-if="!searchQuery && !auth.isAuthenticated" class="spotlight-no-results">
            <i class="pi pi-lock" />
            {{ t('globalsearch.strings.loginRequired') }}
          </div>
          <div v-else-if="!searchQuery" class="spotlight-no-results">
            <i class="pi pi-search" />
            {{ t('globalsearch.strings.startTyping') }}
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'
import { useGlobalSearch } from '@/composables/useGlobalSearch'
import DOMPurify from 'dompurify'

const { t } = useI18n()
const auth = useAuthStore()

// Usa il composable per la ricerca globale
const {
  searchQuery,
  searchResults,
  isLoading,
  isVisible,
  search,
  handleSearch: performSearch,
  handleResultClick,
  openSearch,
  closeSearch
} = useGlobalSearch()

const input = ref(null)
const modal = ref(null)

// Raggruppamento per tipo
const groupedResults = computed(() => {
  const groups = {}
  searchResults.value.forEach(r => {
    if (!groups[r.type]) groups[r.type] = []
    groups[r.type].push(r)
  })
  return Object.entries(groups).map(([type, items]) => ({ type, items }))
})

// Navigazione tastiera
const selection = ref({ group: 0, item: 0 })
const isSelected = (g, i) => selection.value.group === g && selection.value.item === i

function moveSelection(dir) {
  if (!searchResults.value.length) return
  const groups = groupedResults.value
  let g = selection.value.group
  let i = selection.value.item
  if (dir > 0) {
    if (i < groups[g].items.length - 1) {
      i++
    } else if (g < groups.length - 1) {
      g++
      i = 0
    }
  } else {
    if (i > 0) {
      i--
    } else if (g > 0) {
      g--
      i = groups[g].items.length - 1
    }
  }
  selection.value = { group: g, item: i }
}

function selectCurrent() {
  const groups = groupedResults.value
  if (!groups.length) return
  const { group, item } = selection.value
  const result = groups[group]?.items[item]
  if (result) {
    handleResultClick(result)
  }
}

function select(g, i) {
  selection.value = { group: g, item: i }
  selectCurrent()
}

// Funzione highlight originale
// function highlight(text) { ... }
// Sostituisco con una versione che sanifica
function highlight(text) {
  // ...logica highlight originale...
  // Esempio: evidenziazione semplice (da adattare alla tua logica)
  if (!text) return ''
  // Supponiamo che la logica evidenzi le parti corrispondenti alla searchQuery
  const query = searchQuery.value?.trim()
  if (!query) return DOMPurify.sanitize(text)
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
  const html = text.replace(regex, '<mark>$1</mark>')
  return DOMPurify.sanitize(html)
}

function iconForType(type) {
  switch (type) {
    case 'asset': return 'pi pi-server text-blue-600'
    case 'contact': return 'pi pi-user text-green-600'
    case 'supplier': return 'pi pi-briefcase text-orange-600'
    case 'manufacturer': return 'pi pi-cog text-purple-600'
    case 'site': return 'pi pi-building text-cyan-600'
    case 'location': return 'pi pi-map-marker text-pink-600'
    default: return 'pi pi-question-circle'
  }
}

// Debounce per la ricerca
let searchTimeout = null
const handleSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  // Se la query è troppo corta, pulisci i risultati
  if (!searchQuery.value || searchQuery.value.trim().length < 2) {
    searchResults.value = []
    return
  }
  searchTimeout = setTimeout(() => {
    performSearch()
  }, 300)
}

// Shortcut globale
function onKeydown(e) {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault()
    openSearch()
  }
  if (e.key === 'Escape' && isVisible.value) {
    closeSearch()
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

watch(isVisible, (val) => {
  if (val) {
    nextTick(() => {
      input.value?.focus()
    })
  } else {
    selection.value = { group: 0, item: 0 }
    searchQuery.value = ''
    searchResults.value = []
  }
})

// Watch searchQuery per aggiornare automaticamente la ricerca
watch(searchQuery, () => {
  handleSearch()
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.spotlight-overlay {
  position: fixed;
  inset: 0;
  background: rgba(30, 32, 38, 0.55);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.spotlight-modal {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  min-width: 420px;
  max-width: 96vw;
  width: 520px;
  padding: 0 0 8px 0;
  display: flex;
  flex-direction: column;
  animation: popin 0.18s cubic-bezier(.4,1.4,.6,1) 1;
}
@keyframes popin {
  0% { transform: scale(0.98); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
}
.spotlight-input-wrapper {
  display: flex;
  align-items: center;
  padding: 18px 24px 10px 24px;
  border-bottom: 1px solid #e9ecef;
}
.spotlight-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.25rem;
  background: transparent;
  padding: 0 0 0 8px;
}
.search-icon {
  font-size: 1.2rem;
  color: #b0b3c6;
}
.loading-spinner {
  margin-left: 8px;
  color: #b0b3c6;
}
.spotlight-results {
  max-height: 340px;
  overflow-y: auto;
  padding: 8px 0 0 0;
}
.spotlight-group-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6c757d;
  padding: 8px 24px 2px 24px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.spotlight-result {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 24px;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.13s;
  font-size: 1.05rem;
}
.spotlight-result.selected {
  background: #e9f0ff;
}
.result-icon {
  font-size: 1.2rem;
  margin-top: 2px;
}
.result-title {
  font-weight: 600;
  color: #23272f;
}
.result-desc {
  font-size: 0.95rem;
  color: #6c757d;
  margin-left: 8px;
}
.spotlight-no-results {
  text-align: center;
  color: #b0b3c6;
  padding: 32px 0 24px 0;
  font-size: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
mark {
  background: #ffe066;
  color: #23272f;
  border-radius: 3px;
  padding: 0 2px;
}
@media (max-width: 600px) {
  .spotlight-modal {
    min-width: 0;
    width: 98vw;
    padding: 0;
  }
  .spotlight-input-wrapper {
    padding: 14px 10px 8px 10px;
  }
  .spotlight-group-label, .spotlight-result {
    padding-left: 10px;
    padding-right: 10px;
  }
}
</style> 