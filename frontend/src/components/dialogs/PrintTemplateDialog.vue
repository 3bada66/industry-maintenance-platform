<template>
  <Dialog 
    :visible="visible" 
    :header="isEditing ? $t('setup.printTemplates.editTemplate') : $t('setup.printTemplates.createTemplate')"
    modal 
    class="template-dialog"
    :style="{ width: '700px' }"
    @update:visible="$emit('update:visible', $event)"
    @hide="onHide"
  >
    <form @submit.prevent="saveTemplate" class="template-form">
      <div class="form-section">
        <h3>{{ $t('setup.strings.printTemplates.basicInfo') }}</h3>
        
        <div class="form-row">
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.templateKey') }} *</label>
            <InputText 
              v-model="form.key" 
              :placeholder="$t('setup.strings.printTemplates.keyPlaceholder')"
              :disabled="isEditing"
              :class="{ 'p-invalid': errors.key }"
            />
            <small class="p-error" v-if="errors.key">{{ errors.key }}</small>
          </div>
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.icon') }}</label>
            <Dropdown 
              v-model="form.icon" 
              :options="iconOptions"
              optionLabel="label"
              optionValue="value"
              :placeholder="$t('setup.strings.printTemplates.selectIcon')"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.templateName') }} ({{ $t('common.italian') }}) *</label>
            <InputText 
              v-model="form.name_translations.it" 
              :placeholder="$t('setup.strings.printTemplates.namePlaceholder')"
              :class="{ 'p-invalid': errors.name }"
            />
            <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
          </div>
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.templateName') }} ({{ $t('common.english') }}) *</label>
            <InputText 
              v-model="form.name_translations.en" 
              :placeholder="$t('setup.strings.printTemplates.namePlaceholder')"
              :class="{ 'p-invalid': errors.name }"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.templateDescription') }} ({{ $t('common.strings.italian') }})</label>
            <Textarea 
              v-model="form.description_translations.it" 
              :placeholder="$t('setup.strings.printTemplates.descriptionPlaceholder')"
              rows="3"
            />
          </div>
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.templateDescription') }} ({{ $t('common.strings.english') }})</label>
            <Textarea 
              v-model="form.description_translations.en" 
              :placeholder="$t('setup.printTemplates.descriptionPlaceholder')"
              rows="3"
            />
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3>{{ $t('setup.strings.printTemplates.printOptions') }}</h3>
        
        <div class="form-row">
          <div class="form-field">
            <label>{{ $t('setup.strings.printTemplates.component') }}</label>
            <Dropdown 
              v-model="form.component" 
              :options="componentOptions"
              optionLabel="label"
              optionValue="value"
              :placeholder="$t('setup.strings.printTemplates.selectComponent')"
            />
          </div>
        </div>

        <div class="options-grid">
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includePhoto" :binary="true" />
              {{ $t('setup.strings.printTemplates.includePhoto') }}
            </label>
          </div>
          
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includeQR" :binary="true" />
              {{ $t('setup.strings.printTemplates.includeQR') }}
            </label>
          </div>
          
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includeConnections" :binary="true" />
              {{ $t('setup.strings.printTemplates.includeConnections') }}
            </label>
          </div>
          
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includeRiskMatrix" :binary="true" />
              {{ $t('setup.strings.printTemplates.includeRiskMatrix') }}
            </label>
          </div>
          
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includeCustomFields" :binary="true" />
              {{ $t('setup.strings.printTemplates.includeCustomFields') }}
            </label>
          </div>
          
          <div class="option-item">
            <label class="checkbox-label">
              <Checkbox v-model="form.options.includeAuditLog" :binary="true" />
              {{ $t('setup.strings.printTemplates.includeAuditLog') }}
            </label>
          </div>
        </div>
      </div>

      <!-- Nuova sezione per la configurazione avanzata dei campi -->
      <div class="form-section">
        <h3>{{ $t('setup.strings.printTemplates.advancedFields') }}</h3>
        <p class="section-description">{{ $t('setup.strings.printTemplates.advancedFieldsDescription') }}</p>
        
        <div class="fields-configuration">
          <div class="fields-header">
            <Button 
              type="button"
              :label="$t('setup.strings.printTemplates.addField')" 
              icon="pi pi-plus" 
              size="small"
              @click="addField"
            />
            <Button 
              type="button"
              :label="$t('setup.strings.printTemplates.resetToDefault')" 
              icon="pi pi-refresh" 
              size="small"
              severity="secondary"
              @click="resetToDefaultFields"
            />
          </div>
          
          <div class="fields-list">
            <div 
              v-for="(field, index) in form.options.fields || []" 
              :key="index"
              class="field-item"
            >
              <div class="field-controls">
                <Button 
                  icon="pi pi-bars" 
                  text 
                  class="drag-handle"
                  @mousedown="startDrag(index)"
                />
                <Button 
                  icon="pi pi-trash" 
                  text 
                  severity="danger"
                  @click="removeField(index)"
                />
              </div>
              
              <div class="field-config">
                <div class="field-row">
                  <div class="field-field">
                    <label>{{ $t('setup.strings.printTemplates.fieldName') }}</label>
                    <Dropdown 
                      v-model="field.name" 
                      :options="availableFields"
                      optionLabel="label"
                      optionValue="value"
                      :placeholder="$t('setup.strings.printTemplates.selectField')"
                    />
                  </div>
                  <div class="field-field">
                    <label>{{ $t('setup.strings.printTemplates.fieldLabel') }}</label>
                    <InputText 
                      v-model="field.label" 
                      :placeholder="$t('setup.strings.printTemplates.fieldLabelPlaceholder')"
                    />
                  </div>
                  <div class="field-field">
                    <label>{{ $t('setup.strings.printTemplates.fieldSection') }}</label>
                    <Dropdown 
                      v-model="field.section" 
                      :options="sectionOptions"
                      optionLabel="label"
                      optionValue="value"
                      :placeholder="$t('setup.strings.printTemplates.selectSection')"
                    />
                  </div>
                </div>
                
                <div class="field-row">
                  <div class="field-field">
                    <label class="checkbox-label">
                      <Checkbox v-model="field.visible" :binary="true" />
                      {{ $t('setup.strings.printTemplates.fieldVisible') }}
                    </label>
                  </div>
                  <div class="field-field">
                    <label>{{ $t('setup.strings.printTemplates.fieldWidth') }}</label>
                    <Dropdown 
                      v-model="field.width" 
                      :options="widthOptions"
                      optionLabel="label"
                      optionValue="value"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <Button 
          type="button"
          :label="$t('common.actions.cancel')" 
          text 
          @click="onHide"
        />
        <Button 
          type="submit"
          :label="$t('common.actions.save')" 
          icon="pi pi-save" 
          :loading="saving"
        />
      </div>
    </form>
  </Dialog>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import api from '../../api/api'

// PrimeVue Components
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'

const { t } = useI18n()
const toast = useToast()

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  template: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'saved'])

// State
const saving = ref(false)
const errors = reactive({})

// Form data
const form = reactive({
  key: '',
  name_translations: {
    it: '',
    en: ''
  },
  description_translations: {
    it: '',
    en: ''
  },
  icon: '',
  component: '',
  options: {
    includePhoto: true,
    includeQR: true,
    includeConnections: false,
    includeRiskMatrix: true,
    includeCustomFields: true,
    includeAuditLog: false,
    fields: [] // Aggiunto per la configurazione avanzata
  }
})

// Computed
const isEditing = computed(() => !!props.template)

// Options
const iconOptions = [
  { label: 'Server', value: 'pi pi-server' },
  { label: 'File', value: 'pi pi-file' },
  { label: 'Print', value: 'pi pi-print' },
  { label: 'Desktop', value: 'pi pi-desktop' },
  { label: 'Laptop', value: 'pi pi-laptop' },
  { label: 'Mobile', value: 'pi pi-mobile' },
  { label: 'Tablet', value: 'pi pi-tablet' },
  { label: 'Network', value: 'pi pi-wifi' },
  { label: 'Database', value: 'pi pi-database' },
  { label: 'Cloud', value: 'pi pi-cloud' },
  { label: 'Shield', value: 'pi pi-shield' },
  { label: 'Cog', value: 'pi pi-cog' }
]

const componentOptions = [
  { label: 'Asset Card Print', value: 'AssetCardPrint' },
  { label: 'Asset Summary Print', value: 'AssetSummaryPrint' },
  { label: 'Asset Compact Print', value: 'AssetCompactPrint' },
  { label: 'Asset Detailed Print', value: 'AssetDetailedPrint' }
]

// Nuove opzioni per la configurazione avanzata
const availableFields = [
  { label: 'ID Asset', value: 'asset_id' },
  { label: 'Nome Asset', value: 'asset_name' },
  { label: 'Tag', value: 'asset_tag' },
  { label: 'Tipo Asset', value: 'asset_type' },
  { label: 'Stato Asset', value: 'asset_status' },
  { label: 'Posizione', value: 'asset_location' },
  { label: 'Sito', value: 'asset_site' },
  { label: 'Produttore', value: 'asset_manufacturer' },
  { label: 'Modello', value: 'asset_model' },
  { label: 'Numero di Serie', value: 'asset_serial' },
  { label: 'Indirizzo IP', value: 'asset_ip' },
  { label: 'Firmware', value: 'asset_firmware' },
  { label: 'Descrizione', value: 'asset_description' },
  { label: 'Data Acquisto', value: 'asset_purchase_date' },
  { label: 'Garanzia', value: 'asset_warranty' },
  { label: 'Valore', value: 'asset_value' },
  { label: 'Note', value: 'asset_notes' },
  { label: 'Risk Score', value: 'asset_risk_score' },
  { label: 'Criticità Business', value: 'asset_business_criticality' },
  { label: 'Data Installazione', value: 'asset_installation_date' },
  { label: 'Ultima Manutenzione', value: 'asset_last_maintenance' }
]

const sectionOptions = [
  { label: 'Header', value: 'header' },
  { label: 'Body', value: 'body' },
  { label: 'Footer', value: 'footer' }
]

const widthOptions = [
  { label: '10%', value: '10%' },
  { label: '20%', value: '20%' },
  { label: '30%', value: '30%' },
  { label: '40%', value: '40%' },
  { label: '50%', value: '50%' },
  { label: '60%', value: '60%' },
  { label: '70%', value: '70%' },
  { label: '80%', value: '80%' },
  { label: '90%', value: '90%' },
  { label: '100%', value: '100%' }
]

// Methods
const validateForm = () => {
  errors.key = ''
  errors.name = ''
  
  if (!form.key.trim()) {
    errors.key = t('setup.strings.printTemplates.keyRequired')
  } else if (!/^[a-z0-9-]+$/.test(form.key)) {
    errors.key = t('setup.strings.printTemplates.keyFormat')
  }
  
  if (!form.name_translations.it.trim() || !form.name_translations.en.trim()) {
    errors.name = t('setup.strings.printTemplates.nameRequired')
  }
  
  return !errors.key && !errors.name
}

const saveTemplate = async () => {
  if (!validateForm()) return
  
  try {
    saving.value = true
    
    const templateData = {
      key: form.key,
      name: form.name_translations.it, // Per retrocompatibilità
      name_translations: form.name_translations,
      description: form.description_translations.it, // Per retrocompatibilità
      description_translations: form.description_translations,
      icon: form.icon,
      component: form.component,
      options: form.options
    }
    
    if (isEditing.value) {
      await api.updatePrintTemplate(props.template.id, templateData)
      toast.add({
        severity: 'success',
        summary: t('common.messages.success'),
        detail: t('setup.strings.printTemplates.templateUpdated'),
        life: 3000
      })
    } else {
      await api.createPrintTemplate(templateData)
      toast.add({
        severity: 'success',
        summary: t('common.messages.success'),
        detail: t('setup.strings.printTemplates.templateCreated'),
        life: 3000
      })
    }
    
    emit('saved')
    onHide()
    
  } catch (error) {
          console.error('Error saving template:', error)
    toast.add({
      severity: 'error',
      summary: t('common.messages.error'),
      detail: t('setup.strings.printTemplates.saveError'),
      life: 3000
    })
  } finally {
    saving.value = false
  }
}

const onHide = () => {
  emit('update:visible', false)
}

const resetForm = () => {
  Object.assign(form, {
    key: '',
    name_translations: { it: '', en: '' },
    description_translations: { it: '', en: '' },
    icon: '',
    component: '',
    options: {
      includePhoto: true,
      includeQR: true,
      includeConnections: false,
      includeRiskMatrix: true,
      includeCustomFields: true,
      includeAuditLog: false,
      fields: []
    }
  })
  Object.keys(errors).forEach(key => errors[key] = '')
}

// Nuove funzioni per la configurazione avanzata
const addField = () => {
  form.options.fields.push({
    name: '',
    label: '',
    section: 'body',
    visible: true,
    width: '10%'
  })
}

const removeField = (index) => {
  form.options.fields.splice(index, 1)
}

const startDrag = (index) => {
  const fieldItem = document.querySelector(`.field-item:nth-child(${index + 1})`)
  if (fieldItem) {
    fieldItem.classList.add('dragging')
  }
}

const endDrag = () => {
  document.querySelectorAll('.field-item.dragging').forEach(item => {
    item.classList.remove('dragging')
  })
}

const resetToDefaultFields = () => {
  form.options.fields = [
    { name: 'asset_id', label: 'ID', section: 'header', visible: true, width: '10%' },
    { name: 'asset_name', label: 'Nome', section: 'body', visible: true, width: '20%' },
    { name: 'asset_tag', label: 'Tag', section: 'body', visible: true, width: '15%' },
    { name: 'asset_type', label: 'Tipo', section: 'body', visible: true, width: '15%' },
    { name: 'asset_status', label: 'Stato', section: 'body', visible: true, width: '15%' },
    { name: 'asset_location', label: 'Posizione', section: 'body', visible: true, width: '20%' },
    { name: 'asset_site', label: 'Sito', section: 'body', visible: true, width: '15%' },
    { name: 'asset_manufacturer', label: 'Produttore', section: 'body', visible: true, width: '15%' },
    { name: 'asset_model', label: 'Modello', section: 'body', visible: true, width: '15%' },
    { name: 'asset_serial', label: 'Numero di Serie', section: 'body', visible: true, width: '15%' },
    { name: 'asset_ip', label: 'Indirizzo IP', section: 'body', visible: true, width: '15%' },
    { name: 'asset_firmware', label: 'Firmware', section: 'body', visible: true, width: '15%' },
    { name: 'asset_risk_score', label: 'Risk Score', section: 'body', visible: true, width: '10%' }
  ]
}

// Watch for template changes
watch(() => props.template, (newTemplate) => {
  if (newTemplate) {
    // Editing mode
    form.key = newTemplate.key || ''
    form.name_translations = {
      it: newTemplate.name_translations?.it || newTemplate.name || '',
      en: newTemplate.name_translations?.en || newTemplate.name || ''
    }
    form.description_translations = {
      it: newTemplate.description_translations?.it || newTemplate.description || '',
      en: newTemplate.description_translations?.en || newTemplate.description || ''
    }
    form.icon = newTemplate.icon || ''
    form.component = newTemplate.component || ''
    form.options = { ...form.options, ...newTemplate.options }
  } else {
    // Create mode
    resetForm()
  }
}, { immediate: true })
</script>

<style scoped>
.template-dialog {
  border-radius: 12px;
}

.template-form {
  padding: 1rem 0;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h3 {
  margin: 0 0 1rem 0;
  color: var(--text-color);
  font-size: 1.1rem;
  border-bottom: 1px solid var(--surface-border);
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-field label {
  font-weight: 600;
  color: var(--text-color);
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.option-item {
  padding: 0.5rem;
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  background: var(--surface-ground);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--surface-border);
}

/* Nuove regole per la configurazione avanzata */
.fields-configuration {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  background: var(--surface-ground);
}

.fields-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.fields-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  background: var(--surface-ground);
  cursor: grab;
}

.field-item.dragging {
  opacity: 0.5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.field-controls {
  display: flex;
  gap: 0.5rem;
  margin-right: 0.5rem;
}

.field-config {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr; /* Adjust as needed */
  gap: 0.5rem;
}

.field-field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.field-field label {
  font-size: 0.85rem;
  color: var(--text-color-secondary);
}

.section-description {
  font-size: 0.85rem;
  color: var(--text-color-secondary);
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }

  .field-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style> 