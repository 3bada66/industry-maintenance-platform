<!--
  - BaseForm.vue
  - Componente base standardizzato per i form
  - Fornisce validazione, gestione errori e layout uniforme
-->
<template>
  <form @submit.prevent="handleSubmit" class="base-form">
    <div class="p-fluid">
      <!-- Campi del form -->
      <slot />
      
      <!-- Messaggi di errore globali -->
      <div v-if="hasGlobalErrors" class="global-errors mb-3">
        <Message 
          v-for="error in globalErrors" 
          :key="error"
          severity="error" 
          :text="error"
          class="mb-2"
        />
      </div>
      
      <!-- Azioni del form -->
      <div class="flex justify-content-end gap-2 mt-4">
        <Button 
          v-if="showCancel"
          :label="cancelLabelComputed" 
          class="p-button-text" 
          @click="handleCancel"
          :disabled="isSubmitting"
        />
        <Button 
          :label="submitLabelComputed" 
          type="submit"
          :loading="isSubmitting"
          :disabled="isSubmitting || !(typeof isValid === 'function' ? isValid() : isValid)"
        />
      </div>
    </div>
  </form>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Message from 'primevue/message'

const { t } = useI18n()

// Props
const props = defineProps({
  // Stato del form
  isSubmitting: {
    type: Boolean,
    default: false
  },
  isValid: {
    type: [Boolean, Function],
    default: true
  },
  errors: {
    type: Object,
    default: () => ({})
  },
  
  // Labels
  submitLabel: {
    type: String,
    default: null
  },
  cancelLabel: {
    type: String,
    default: null
  },
  
  // Opzioni
  showCancel: {
    type: Boolean,
    default: true
  }
})

// Emits
const emit = defineEmits(['submit', 'cancel'])

// Computed
const hasGlobalErrors = computed(() => {
  return Object.keys(props.errors).length > 0
})

const globalErrors = computed(() => {
  return Object.values(props.errors).filter(error => 
    typeof error === 'string' && error.trim() !== ''
  )
})

const submitLabelComputed = computed(() => props.submitLabel ?? t('common.actions.save'))
const cancelLabelComputed = computed(() => props.cancelLabel ?? t('common.actions.cancel'))

// Methods
const handleSubmit = () => {
  const isValidValue = typeof props.isValid === 'function' ? props.isValid() : props.isValid
  if (props.isSubmitting || !isValidValue) {
    return
  }
  emit('submit')
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.base-form {
  width: 100%;
}

.global-errors {
  border: 1px solid var(--red-200);
  border-radius: 6px;
  padding: 1rem;
  background: var(--red-50);
}

:deep(.p-field) {
  margin-bottom: 1.5rem;
}

:deep(.p-field label) {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

:deep(.p-field .p-inputtext),
:deep(.p-field .p-dropdown),
:deep(.p-field .p-multiselect),
:deep(.p-field .p-textarea) {
  width: 100%;
}

:deep(.p-field .p-invalid) {
  border-color: var(--red-500);
}

:deep(.p-field .p-error) {
  color: var(--red-500);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style> 