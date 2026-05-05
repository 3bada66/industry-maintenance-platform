<!--
  - AssetCustomFields.vue
  - Componente per la gestione dei campi personalizzati degli asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <Card>
    <template #title>{{ t('assets.customFields.title') }}</template>
    <template #content>
      <div v-if="!isEditing">
        <table class="custom-fields-table">
          <tbody>
            <tr v-for="(field, index) in fieldsArray" :key="index" @click="readOnly ? null : startEditing" :class="{ 'clickable': !readOnly }">
              <td>{{ field.key }}</td>
              <td>{{ field.value }}</td>
            </tr>
            <tr v-if="fieldsArray.length === 0">
              <td colspan="2">{{ t('assets.customFields.noCustomFields') }}</td>
            </tr>
          </tbody>
        </table>
        <Button v-if="!readOnly" :label="t('assets.customFields.addField')" icon="pi pi-plus" class="mt-2" @click="addNewField" />
      </div>

      <div v-else>
        <div v-for="(field, index) in editableFields" :key="index" class="flex gap-2 items-center mb-2">
          <InputText :id="`custom_field_key_${index}`" v-model="field.key" placeholder="Key" class="w-4/12" @input="showSave = true" />
          <InputText :id="`custom_field_value_${index}`" v-model="field.value" placeholder="Value" class="w-6/12" @input="showSave = true" />
          <Button icon="pi pi-trash" severity="danger" @click="removeField(index)" />
        </div>
        <Button :label="t('assets.customFields.addField')" icon="pi pi-plus" class="mt-2" @click="addField" />
        <Button :label="t('assets.customFields.saveFields')" icon="pi pi-save" class="mt-2" @click="saveFields" v-if="showSave" />
        <Button :label="t('common.actions.cancel')" icon="pi pi-times" class="mt-2 p-button-text" @click="cancelEditing" />
      </div>
    </template>
  </Card>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import api from '../../api/api'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  assetId: { type: [String, Number], required: true },
  customFields: { type: Object, default: () => ({}) },  // Cambiato da Array a Object
  readOnly: { type: Boolean, default: false }
})

const emit = defineEmits(['saved'])

const toast = useToast()

const isEditing = ref(false)
const editableFields = ref([])
const showSave = ref(false)

// computed per convertire l'oggetto in array di {key,value}
const fieldsArray = computed(() => {
  return Object.entries(props.customFields).map(([key, value]) => ({ key, value }))
})

watch(() => props.customFields, (newVal) => {
  if (!isEditing.value) {
    // In fase di editing uso l'array di oggetti
    editableFields.value = Object.entries(newVal).map(([key, value]) => ({ key, value }))
  }
}, { immediate: true })

function startEditing() {
  isEditing.value = true
  editableFields.value = Object.entries(props.customFields).map(([key, value]) => ({ key, value }))
  showSave.value = false
}

function addNewField() {
  if (!isEditing.value) {
    startEditing()
  }
  addField()
  showSave.value = true
}

function addField() {
  editableFields.value.push({ key: '', value: '' })
}

function removeField(index) {
  editableFields.value.splice(index, 1)
  showSave.value = true
}

function cancelEditing() {
  isEditing.value = false
  showSave.value = false
  editableFields.value = Object.entries(props.customFields).map(([key, value]) => ({ key, value }))
}

async function saveFields() {
  // Validazione base
  const keys = editableFields.value.map(f => f.key.trim())
  if (keys.some(k => !k)) {
    toast.add({ severity: 'warn', summary: t('common.messages.error'), detail: t('assets.customFields.allKeysMustBeFilled') })
    return
  }
  if (new Set(keys).size !== keys.length) {
    toast.add({ severity: 'warn', summary: t('common.messages.error'), detail: t('assets.customFields.allKeysMustBeUnique') })
    return
  }

  const payload = {}
  editableFields.value.forEach(({ key, value }) => {
    payload[key] = value
  })

  try {
    await api.updateAssetCustomFields(props.assetId, { custom_fields: payload })
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('assets.customFields.fieldsUpdated') })
    isEditing.value = false
    showSave.value = false
    emit('saved', editableFields.value)
  } catch (error) {
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('assets.customFields.saveError') })
  }
}
</script>

<style scoped>
.custom-fields-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--card-bg);
  color: var(--text-color);
}

.custom-fields-table td {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
}

.flex {
  display: flex;
  align-items: center;
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  background-color: var(--surface-hover);
}
</style>
