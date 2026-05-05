<template>
  <div class="filters">
    <Dropdown 
      id="filter_status"
      v-model="filters.status_id.value" 
      :options="assetStatusOptions" 
      optionLabel="name" 
      optionValue="id" 
      :placeholder="t('assets.strings.filterbyStatus')" 
      showClear 
      style="min-width: 150px" 
    />
    <Dropdown 
      id="filter_site"
      v-model="filters.site_id.value" 
      :options="sites" 
      optionLabel="name" 
      optionValue="id" 
      :placeholder="t('assets.strings.filterbySite')" 
      showClear 
      style="min-width: 150px" 
    />
    <Dropdown 
      id="filter_area"
      v-model="filters.area_id.value" 
      :options="areas" 
      optionLabel="name" 
      optionValue="id" 
      :placeholder="t('assets.strings.filterbyArea')" 
      showClear 
      style="min-width: 150px" 
    />
    <Button 
      icon="pi pi-filter" 
      :label="t('assets.strings.advancedFilters') || 'Filtri avanzati'"
      severity="help"
      @click="$emit('showAdvancedFilters')"
    />
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

const props = defineProps({
  filters: { type: Object, required: true },
  assetStatusOptions: { type: Array, default: () => [] },
  sites: { type: Array, default: () => [] },
  areas: { type: Array, default: () => [] }
})

const emit = defineEmits(['showAdvancedFilters'])

const { t } = useI18n()
</script>

<style scoped>
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
</style> 