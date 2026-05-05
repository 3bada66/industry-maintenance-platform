
<template>
  <Dialog 
    :visible="isVisible" 
    @update:visible="val => $emit('update:isVisible', val)"
    :header="title" 
    :modal="true" 
    :style="{ width: width }"
    :closable="closable"
    :closeOnEscape="closeOnEscape"
    @hide="handleHide"
  >
    <!-- Contenuto del dialog -->
    <div class="dialog-content">
      <slot :data="data" :mode="mode" />
    </div>
    
    <!-- Footer del dialog -->
    <template #footer v-if="showFooter">
      <div class="flex justify-content-end gap-2">
        <Button 
          v-if="showCancel"
          :label="computedCancelLabel" 
          class="p-button-text" 
          @click="handleCancel"
          :disabled="isSubmitting"
        />
        <Button 
          v-if="showSubmit"
          :label="computedSubmitLabel" 
          @click="handleSubmit"
          :loading="isSubmitting"
          :disabled="isSubmitting || !isValid"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'

const { t } = useI18n()

// Props
const props = defineProps({
  // Stato del dialog
  isVisible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  mode: {
    type: String,
    default: 'create', // 'create', 'edit', 'view'
    validator: (value) => ['create', 'edit', 'view'].includes(value)
  },
  
  // Dati del form
  data: {
    type: Object,
    default: null
  },
  
  // Dimensioni e comportamento
  width: {
    type: String,
    default: '40vw'
  },
  closable: {
    type: Boolean,
    default: true
  },
  closeOnEscape: {
    type: Boolean,
    default: true
  },
  
  // Footer
  showFooter: {
    type: Boolean,
    default: true
  },
  showCancel: {
    type: Boolean,
    default: true
  },
  showSubmit: {
    type: Boolean,
    default: true
  },
  
  // Stato del form
  isSubmitting: {
    type: Boolean,
    default: false
  },
  isValid: {
    type: Boolean,
    default: true
  },
  
  // Labels
  submitLabel: {
    type: String,
    default: null
  },
  cancelLabel: {
    type: String,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:isVisible', 'submit', 'cancel', 'hide'])

// Computed
const computedSubmitLabel = computed(() => {
  if (props.submitLabel) {
    return props.submitLabel
  }
  switch (props.mode) {
    case 'create':
      return t('common.actions.create')
    case 'edit':
      return t('common.actions.update')
    case 'view':
      return t('common.actions.close')
    default:
      return t('common.actions.save')
  }
})

const computedCancelLabel = computed(() => props.cancelLabel ?? t('common.actions.cancel'))

const computedTitle = computed(() => {
  if (props.title) {
    return props.title
  }
  switch (props.mode) {
    case 'create':
      return t('common.actions.create')
    case 'edit':
      return t('common.actions.edit')
    case 'view':
      return t('common.actions.close')
    default:
      return ''
  }
})

// Methods
const handleSubmit = () => {
  if (props.isSubmitting || !props.isValid) {
    return
  }
  if (props.showFooter) {
    emit('submit')
  }
}

const handleCancel = () => {
  emit('cancel')
  closeDialog()
}

const handleHide = () => {
  emit('hide')
}

const closeDialog = () => {
  emit('update:isVisible', false)
}

// Watch per chiudere automaticamente in modalità view
watch(() => props.mode, (newMode) => {
  if (newMode === 'view') {
    props.showSubmit = false
  }
})
</script>

<style scoped>
.dialog-content {
  min-height: 200px;
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

:deep(.p-dialog-title) {
  font-size: 1.25rem;
  font-weight: 600;
}
</style> 