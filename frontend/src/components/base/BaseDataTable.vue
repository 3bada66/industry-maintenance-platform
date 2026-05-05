<!--
  - BaseDataTable.vue
  - Componente base standardizzato per le tabelle dati
  - Fornisce funzionalità comuni: filtri, ordinamento, paginazione, esportazione
-->
<template>
  <div class="base-data-table" :class="{ 
    'auto-height': autoHeight,
    'needs-scroll': needsScroll 
  }">
    <DataTable 
      :value="dataWithOriginal" 
      :loading="loading"
      :filters="{}"
      :globalFilterFields="[]"
      :sortField="sortField"
      :sortOrder="sortOrder"
      paginator 
      :rows="rows"
      :rowsPerPageOptions="rowsPerPageOptions"
      :resizableColumns="resizableColumns"
      :columnResizeMode="columnResizeMode"
      :showGridlines="showGridlines"
      :scrollable="needsScroll"
      :scrollHeight="finalScrollHeight"
      :exportFilename="exportFilename"
      ref="tableRef"
      v-model:selection="selection"
      :selectionMode="selectionMode"
      @sort="onSort"
    >
      <template #header>
        <div class="flex justify-content-between align-items-center gap-2">
          <div class="flex align-items-center gap-2">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText 
                id="global_search"
                v-model="safeFilters.global.value" 
                :placeholder="t('common.actions.search')" 
                class="w-12rem"
              />
            </span>
            
            <!-- Filtri specifici -->
            <slot name="filters" />
          </div>
          
          <div class="flex gap-2">
            <!-- Azioni standard -->
            <Button 
              v-if="showExport"
              icon="pi pi-file-excel" 
              :label="t('common.actions.exportCsv')" 
              class="p-button-sm" 
              @click="exportCsv" 
            />
            
            <Button 
              v-if="showColumnSelector"
              icon="pi pi-sliders-h" 
              class="p-button-sm" 
              @click="toggleColumnPanel" 
              v-tooltip="t('common.actions.chooseColumns')" 
            />
            
            <!-- Azioni personalizzate -->
            <slot name="actions" />
          </div>
        </div>
      </template>
      
      <!-- Colonna di selezione -->
      <Column 
        v-if="selectionMode" 
        selectionMode="multiple" 
        headerStyle="width: 3rem"
      />
      
      <!-- Colonne dinamiche -->
      <template v-for="col in visibleColumns" :key="col.field">
        <Column 
          :field="col.field" 
          :header="col.header" 
          :sortable="col.sortable !== false"
          :style="col.style"
          :class="col.class"
          :frozen="col.frozen"
          :alignFrozen="col.alignFrozen"
        >
          <template #body="slotProps" v-if="col.field === 'actions'">
            <slot name="body-actions" :data="slotProps.data.__original || slotProps.data" />
          </template>
          <template #body="slotProps" v-else-if="col.field === 'status.name'">
            <slot name="body-status.name" :data="slotProps.data.__original || slotProps.data" />
          </template>
          <template #body="slotProps" v-else-if="col.field === 'risk_score'">
            <slot name="body-risk_score" :data="slotProps.data.__original || slotProps.data" />
          </template>
          <template #body="slotProps" v-else-if="col.field === 'business_criticality'">
            <slot name="body-business_criticality" :data="slotProps.data.__original || slotProps.data" />
          </template>
          <template #body="slotProps" v-else-if="col.field === 'name'">
            <slot name="body-name" :data="slotProps.data.__original || slotProps.data" v-if="$slots['body-name']" />
            <span v-else>{{ slotProps.data.name }}</span>
          </template>
          <template #body="slotProps" v-else-if="col.field === 'is_active'">
            <slot name="body-is_active" :data="slotProps.data.__original || slotProps.data" />
          </template>
          <template #body="slotProps" v-else-if="col.bodyTemplate">
            <component 
              :is="col.bodyTemplate" 
              :data="slotProps.data.__original || slotProps.data" 
              :field="col.field"
              v-bind="col.templateProps || {}"
            />
          </template>
        </Column>
      </template>
      
      <!-- Slot per contenuto personalizzato -->
      <slot />
    </DataTable>

    <!-- Panel per selezione colonne -->
    <OverlayPanel ref="columnPanel" v-if="showColumnSelector">
      <div style="min-width: 250px">
        <h4 class="mb-3">{{ t('common.actions.chooseColumns') }}</h4>
        <MultiSelect 
          v-model="selectedColumns" 
          :options="allColumns" 
          optionLabel="header" 
          :placeholder="t('common.actions.chooseColumns')" 
          display="chip" 
          class="w-full" 
        />
      </div>
    </OverlayPanel>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import OverlayPanel from 'primevue/overlaypanel'
import { useTableHeight } from '@/composables/useTableHeight'

const { t } = useI18n()

// Props
const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  columns: {
    type: Array,
    required: true
  },
  filters: {
    type: Object,
    default: () => ({ global: { value: null, matchMode: 'contains' } })
  },
  globalFilterFields: {
    type: Array,
    default: () => []
  },
  sortField: {
    type: String,
    default: ''
  },
  sortOrder: {
    type: Number,
    default: 1
  },
  rows: {
    type: Number,
    default: 15
  },
  rowsPerPageOptions: {
    type: Array,
    default: () => [10, 15, 25, 50]
  },
  resizableColumns: {
    type: Boolean,
    default: true
  },
  columnResizeMode: {
    type: String,
    default: 'fit'
  },
  showGridlines: {
    type: Boolean,
    default: true
  },
  scrollable: {
    type: Boolean,
    default: false
  },
  scrollHeight: {
    type: String,
    default: '80vh'
  },
  exportFilename: {
    type: String,
    default: 'export'
  },
  showExport: {
    type: Boolean,
    default: true
  },
  showColumnSelector: {
    type: Boolean,
    default: true
  },
  selectionMode: {
    type: String,
    default: null
  },
  storageKey: {
    type: String,
    default: null
  },
  autoHeight: {
    type: Boolean,
    default: false
  },
  heightOffsetTop: {
    type: Number,
    default: 200
  },
  heightOffsetBottom: {
    type: Number,
    default: 100
  },
  forceScroll: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['sort', 'selection-change'])

// Refs
const tableRef = ref()
const columnPanel = ref()
const selection = ref([])
const selectedColumns = ref([])

// Calcolo altezza automatica
const { tableHeight: autoTableHeight } = useTableHeight({
  offsetTop: props.heightOffsetTop,
  offsetBottom: props.heightOffsetBottom
})

// Computed
const allColumns = computed(() => props.columns)

const visibleColumns = computed(() => {
  if (selectedColumns.value.length === 0) {
    return props.columns
  }
  return props.columns.filter(col => 
    selectedColumns.value.some(selected => selected.field === col.field)
  )
})

// Determina se lo scroll è necessario
const needsScroll = computed(() => {
  // Se forceScroll è abilitato, forza lo scroll
  if (props.forceScroll) return true
  
  // Se autoHeight è abilitato, calcoliamo dinamicamente
  if (props.autoHeight) {
    const availableHeight = window.innerHeight - props.heightOffsetTop - props.heightOffsetBottom
    
    // Calcolo più realistico basato su righe visibili
    const visibleRows = Math.floor(availableHeight / 50) // ~50px per riga
    const currentRows = props.rows || 15
    
    // Se le righe correnti sono più delle righe visibili, serve scroll
    if (currentRows > visibleRows) {
      return true
    }
    
    // Altrimenti, calcola se i dati attuali necessitano scroll
    const headerHeight = 60 // Altezza header tabella
    const paginatorHeight = 60 // Altezza paginatore
    const estimatedTableHeight = props.data.length * 50 + headerHeight + paginatorHeight
    
    // Se la tabella ha molte colonne, aumenta l'altezza stimata
    const columnMultiplier = props.columns.length > 10 ? 1.3 : 1.0
    const adjustedHeight = estimatedTableHeight * columnMultiplier
    
    return adjustedHeight > availableHeight
  }
  
  // Se scrollable è esplicitamente impostato, rispettiamo il valore
  return props.scrollable
})

// Altezza finale della tabella
const finalScrollHeight = computed(() => {
  if (!needsScroll.value) return null
  return props.autoHeight ? autoTableHeight.value : props.scrollHeight
})

// Gestione sicura dei filtri
const safeFilters = computed(() => {
  if (!props.filters || Object.keys(props.filters).length === 0) {
    return { global: { value: null, matchMode: 'contains' } }
  }
  return props.filters
})

// Data with original for body templates
const dataWithOriginal = computed(() => {
  // Per ogni riga, crea una shallow copy e aggiungi __original che punta all'oggetto asset originale
  return props.data.map(row => ({ ...row, __original: row }))
})

// Methods
const exportCsv = () => {
  if (tableRef.value) {
    tableRef.value.exportCSV()
  }
}

const toggleColumnPanel = (event) => {
  if (columnPanel.value) {
    columnPanel.value.toggle(event)
  }
}

const onSort = (event) => {
  emit('sort', event)
}

// Load saved columns
const loadSavedColumns = () => {
  if (!props.storageKey) {
    // Se non c’è storageKey, seleziona tutte
    selectedColumns.value = [...props.columns];
    return;
  }
  try {
    const saved = localStorage.getItem(`${props.storageKey}_columns`)
    if (saved) {
      selectedColumns.value = JSON.parse(saved)
    } else {
      // Se non c’è nulla salvato, seleziona tutte
      selectedColumns.value = [...props.columns];
    }
  } catch (error) {
    console.warn('Error loading saved columns:', error)
    selectedColumns.value = [...props.columns];
  }
}

// Save columns when changed
watch(selectedColumns, (newColumns) => {
  if (props.storageKey) {
    try {
      localStorage.setItem(`${props.storageKey}_columns`, JSON.stringify(newColumns))
    } catch (error) {
      console.warn('Error saving columns:', error)
    }
  }
}, { deep: true })

// Watch selection changes
watch(selection, (newSelection) => {
  emit('selection-change', newSelection)
}, { deep: true })



// Lifecycle
onMounted(() => {
  loadSavedColumns()
  // If no columns are selected (first opening), select all
  if (!selectedColumns.value.length && Array.isArray(props.columns)) {
    selectedColumns.value = [...props.columns];
  }
})

// Expose methods
defineExpose({
  exportCsv,
  getTableRef: () => tableRef.value
})
</script>

<style scoped>
.base-data-table {
  width: 100%;
}

:deep(.p-datatable) {
  font-size: 0.875rem;
}

/* Rimuove la limitazione di altezza di PrimeVue quando autoHeight è abilitato */
.auto-height :deep(.p-datatable-wrapper) {
  max-height: none !important;
}

/* Quando autoHeight è abilitato e non serve scroll, rimuovi overflow */
.auto-height:not(.needs-scroll) :deep(.p-datatable-wrapper) {
  overflow: visible !important;
}

:deep(.p-datatable .p-datatable-header) {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-bottom: none;
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: var(--surface-section);
  border: 1px solid var(--surface-border);
  font-weight: 600;
  padding: 0.75rem;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  border: 1px solid var(--surface-border);
  padding: 0.75rem;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: var(--surface-hover);
}
</style> 