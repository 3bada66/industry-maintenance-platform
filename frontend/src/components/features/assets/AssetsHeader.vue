<template>
  <div class="page-header">
    <h1>{{ t('assets.title') }}</h1>
    <div class="flex gap-2">
      <!-- Azioni principali -->
              <Button 
          v-if="!trashMode && canWrite('assets')"
          :label="t('common.actions.create')" 
          icon="pi pi-plus" 
          severity="success"
          @click="$emit('create')" 
        />
        <Button 
          v-if="!trashMode && canWrite('assets')"
          :label="t('common.actions.import')" 
          icon="pi pi-upload" 
          severity="info"
          @click="$emit('import')" 
        />
        
        <!-- Separatore visivo -->
        <div v-if="canWrite('assets') || canDelete('assets')" class="w-px h-8 bg-gray-300 mx-2"></div>
        
        <!-- Gestione cestino -->
        <Button 
          v-if="canDelete('assets')"
          icon="pi pi-trash" 
          :label="trashMode ? t('common.actions.showActive') : t('common.actions.showTrash')" 
          severity="secondary"
          @click="$emit('toggleTrash')"
        />
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { usePermissions } from '../../../composables/usePermissions'
import Button from 'primevue/button'

const props = defineProps({
  trashMode: { type: Boolean, default: false }
})

const emit = defineEmits(['create', 'import', 'toggleTrash'])

const { t } = useI18n()
const { canWrite, canDelete } = usePermissions()
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
</style> 