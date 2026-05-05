<template>
  <div class="area-form">
    <BaseForm 
      :is-submitting="isSubmitting"
      :is-valid="isValid"
      :errors="errors"
      @submit="handleSubmit"
      @cancel="$emit('cancel')"
    >
      <!-- Informazioni Base -->
      <Card class="mb-4">
        <template #title>
          <div class="flex align-items-center">
            <i class="pi pi-info-circle mr-2"></i>
            {{ t('common.strings.info') }}
          </div>
        </template>
        <template #content>
          <div class="grid">
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="name" class="required">{{ t('common.fields.name') }}</label>
                <InputText
                  id="name"
                  v-model="form.name"
                  :class="{ 'p-invalid': errors.name }"
                  class="w-full"
                />
                <small v-if="errors.name" class="p-error">{{ errors.name }}</small>
              </div>
            </div>
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="code" class="required">{{ t('common.fields.code') }}</label>
                <InputText
                  id="code"
                  v-model="form.code"
                  :class="{ 'p-invalid': errors.code }"
                  class="w-full"
                />
                <small v-if="errors.code" class="p-error">{{ errors.code }}</small>
              </div>
            </div>
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="typology">{{ t('areas.fields.typology') }}</label>
                <InputText
                  id="typology"
                  v-model="form.typology"
                  class="w-full"
                />
              </div>
            </div>
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="site_id" class="required">{{ t('common.fields.site') }}</label>
                <Dropdown
                  id="site_id"
                  v-model="form.site_id"
                  :options="sites"
                  optionLabel="name"
                  optionValue="id"
                  :placeholder="t('common.strings.select')"
                  :class="{ 'p-invalid': errors.site_id }"
                  class="w-full"
                />
                <small v-if="errors.site_id" class="p-error">{{ errors.site_id }}</small>
              </div>
            </div>
            <div class="col-12">
              <div class="field">
                <label for="notes">{{ t('common.fields.notes') }}</label>
                <Textarea
                  id="notes"
                  v-model="form.notes"
                  rows="3"
                  class="w-full"
                />
              </div>
            </div>
          </div>
        </template>
      </Card>
    </BaseForm>
  </div>
</template>

<script setup>
import { watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useForm } from '../../composables/useForm'
import BaseForm from '../base/BaseForm.vue'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'

const { t } = useI18n()

const props = defineProps({
  area: {
    type: Object,
    default: null
  },
  sites: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['submit', 'cancel'])

// Use the useForm composable
const {
  form,
  errors,
  isSubmitting,
  isValid,
  submit,
  setForm
} = useForm({
  name: '',
  code: '',
  typology: '',
  site_id: null,
  notes: ''
})

// Watch for area changes (edit mode)
watch(() => props.area, (newArea) => {
  if (newArea) {
    const formData = {
      name: newArea.name || '',
      code: newArea.code || '',
      typology: newArea.typology || '',
      site_id: newArea.site_id || null,
      notes: newArea.notes || ''
    }
    setForm(formData)
  }
}, { immediate: true })

async function handleSubmit() {
  // Custom validation
  const validationErrors = validateAreaData(form.value)
  if (validationErrors.length > 0) {
    // Set errors manually
    Object.keys(validationErrors).forEach(key => {
      errors.value[key] = validationErrors[key]
    })
    return
  }

  await submit(async (formData) => {
    emit('submit', formData)
  }, {
    successMessage: null, // Disabilitiamo i toast qui, li gestisce il parent
    errorContext: t('common.messages.error')
  })
}

// Function to validate area data
function validateAreaData(areaData) {
  const errors = {}
  
  // Required fields
  if (!areaData.name || areaData.name.trim() === '') {
    errors.name = t('common.fields.nameRequired')
  } 
  
  return errors
}
</script>

<style scoped>
.area-form {
  width: 100%;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.required::after {
  content: ' *';
  color: #dc3545;
  font-weight: bold;
}

.p-invalid {
  border-color: #dc3545 !important;
}

.p-error {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Responsive adjustments */
@media screen and (max-width: 768px) {
  .field {
    margin-bottom: 1.5rem;
  }
  
  .grid > .col-12 {
    padding: 0.5rem;
  }
}
</style> 