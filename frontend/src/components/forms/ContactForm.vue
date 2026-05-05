<template>
  <form @submit.prevent="handleSubmit">
    <div class="p-fluid">
      <div class="p-field">
        <label for="first_name">{{ t('contacts.fields.firstName') }}</label>
        <InputText id="first_name" v-model="form.first_name" required />
      </div>
      <div class="p-field">
        <label for="last_name">{{ t('contacts.fields.lastName') }}</label>
        <InputText id="last_name" v-model="form.last_name" required />
      </div>
      <div class="p-field">
        <label for="phone1">{{ t('contacts.fields.phone1') }}</label>
        <InputText id="phone1" v-model="form.phone1" />
      </div>
      <div class="p-field">
        <label for="phone2">{{ t('contacts.fields.phone2') }}</label>
        <InputText id="phone2" v-model="form.phone2" />
      </div>
      <div class="p-field">
        <label for="email">{{ t('common.fields.email') }}</label>
        <InputText id="email" v-model="form.email" type="email" />
      </div>
      <div class="p-field">
        <label for="type">{{ t('contacts.fields.type') }}</label>
        <Dropdown id="type" v-model="form.type" :options="typeOptions" optionLabel="label" optionValue="value" />
      </div>
      <div class="p-field">
        <label for="notes">{{ t('contacts.fields.notes') }}</label>
        <Textarea id="notes" v-model="form.notes" rows="3" />
      </div>
      <div class="flex justify-content-end gap-2 mt-4">
        <Button :label="t('common.actions.cancel')" class="p-button-text" @click="handleCancel" />
        <Button :label="t('common.actions.save')" type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'

const { t } = useI18n()

const props = defineProps({
  contact: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref({
  first_name: '',
  last_name: '',
  phone1: '',
  phone2: '',
  email: '',
  type: '',
  notes: ''
})

watch(
  () => props.contact,
  (contact) => {
    if (contact) {
      form.value = {
        first_name: contact.first_name || '',
        last_name: contact.last_name || '',
        phone1: contact.phone1 || '',
        phone2: contact.phone2 || '',
        email: contact.email || '',
        type: contact.type || '',
        notes: contact.notes || ''
      }
    } else {
      form.value = {
        first_name: '',
        last_name: '',
        phone1: '',
        phone2: '',
        email: '',
        type: '',
        notes: ''
      }
    }
  },
  { immediate: true }
)

const typeOptions = ref([
  { label: t('contacts.fields.internal'), value: 'interno' },
  { label: t('contacts.fields.supplier'), value: 'fornitore' },
  { label: t('contacts.fields.other'), value: 'altro' }
])

function handleSubmit() {
  emit('submit', form.value)
}

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped>
.p-field {
  margin-bottom: 1.5rem;
}
</style> 