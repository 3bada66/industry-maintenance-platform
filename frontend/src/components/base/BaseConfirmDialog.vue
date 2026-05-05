
<template>
  <ConfirmDialog />
  
  <Dialog 
    :visible="showConfirmDialog" 
    @update:visible="val => $emit('update:showConfirmDialog', val)"
    :header="confirmData?.title || t('common.actions.confirm')" 
    :modal="true" 
    :style="{ width: '400px' }"
    :closable="true"
    :closeOnEscape="true"
  >
    <div class="confirm-content">
      <div class="confirm-icon mb-3">
        <i :class="iconClass" :style="{ color: iconColor }"></i>
      </div>
      
      <div class="confirm-message">
        <p>{{ confirmData?.message || t('common.actions.confirmAction') }}</p>
        
        <!-- Dettagli aggiuntivi per azioni bulk -->
        <div v-if="confirmData?.type === 'bulk' && confirmData?.items" class="bulk-details mt-2">
          <p class="text-sm text-500">
            {{ t('common.actions.selectedItems', { count: confirmData.items.length }) }}
          </p>
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="flex justify-content-end gap-2">
        <Button 
          :label="t('common.actions.cancel')" 
          class="p-button-text" 
          @click="closeConfirmDialog"
        />
        <Button 
          :label="confirmButtonLabel" 
          :severity="confirmButtonSeverity"
          @click="executeConfirmedAction"
          :loading="isExecuting"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import ConfirmDialog from 'primevue/confirmdialog'

const { t } = useI18n()

// Props
const props = defineProps({
  showConfirmDialog: {
    type: Boolean,
    default: false
  },
  confirmData: {
    type: Object,
    default: null
  },
  isExecuting: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['confirm', 'cancel', 'update:visible', 'execute', 'close', 'update:showConfirmDialog'])

// Computed
const iconClass = computed(() => {
  if (!props.confirmData) return 'pi pi-question-circle'
  
  switch (props.confirmData.type) {
    case 'delete':
      return 'pi pi-exclamation-triangle'
    case 'bulk':
      return 'pi pi-exclamation-triangle'
    case 'emptyTrash':
      return 'pi pi-trash'
    default:
      return 'pi pi-question-circle'
  }
})

const iconColor = computed(() => {
  if (!props.confirmData) return 'var(--orange-500)'
  
  switch (props.confirmData.type) {
    case 'delete':
    case 'bulk':
    case 'emptyTrash':
      return 'var(--red-500)'
    default:
      return 'var(--orange-500)'
  }
})

const confirmButtonLabel = computed(() => {
  if (!props.confirmData) return t('common.actions.confirm')
  
  switch (props.confirmData.type) {
    case 'delete':
      return props.confirmData.hardDelete ? t('common.actions.deletePermanently') : t('common.actions.delete')
    case 'bulk':
      return t(`common.actions.${props.confirmData.action.charAt(0).toUpperCase() + props.confirmData.action.slice(1)}`)
    case 'emptyTrash':
      return t('common.actions.emptyTrash')
    default:
      return t('common.actions.confirm')
  }
})

const confirmButtonSeverity = computed(() => {
  if (!props.confirmData) return 'warning'
  
  switch (props.confirmData.type) {
    case 'delete':
    case 'bulk':
    case 'emptyTrash':
      return 'danger'
    default:
      return 'warning'
  }
})

// Methods
const executeConfirmedAction = () => {
  emit('execute')
}

const closeConfirmDialog = () => {
  emit('close')
}
</script>

<style scoped>
.confirm-content {
  text-align: center;
  padding: 1rem 0;
}

.confirm-icon {
  font-size: 3rem;
}

.confirm-message {
  font-size: 1rem;
  line-height: 1.5;
}

.bulk-details {
  background: var(--surface-100);
  padding: 0.75rem;
  border-radius: 6px;
  border-left: 4px solid var(--primary-color);
}

:deep(.p-dialog-header) {
  border-bottom: 1px solid var(--surface-border);
  padding: 1.5rem 1.5rem 1rem;
}

:deep(.p-dialog-content) {
  padding: 1rem 1.5rem;
}

:deep(.p-dialog-footer) {
  border-top: 1px solid var(--surface-border);
  padding: 1rem 1.5rem 1.5rem;
}
</style> 