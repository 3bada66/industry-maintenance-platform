<template>
  <form @submit.prevent="handleSubmit">
    <div class="p-fluid">
      <div class="p-field">
        <label for="name">{{ t('common.fields.name') }}</label>
        <InputText id="name" v-model="form.name" required />
      </div>
      <div class="p-field">
        <label for="description">{{ t('common.fields.description') }}</label>
        <Textarea id="description" v-model="form.description" autoResize />
      </div>
      <div class="p-field">
        <label for="color">{{ t('common.fields.color') }}</label>
        <InputText id="color" v-model="form.color" type="color" style="width: 3rem; height: 2rem; padding: 0;" />
      </div>
      <div class="p-field">
        <label for="order">{{ t('common.fields.order') }}</label>
        <InputNumber id="order" v-model="form.order" :min="0" />
      </div>
      <div class="p-field-checkbox">
        <Checkbox id="active" v-model="form.active" :binary="true" inputId="status_active" />
        <label for="status_active">{{ t('common.fields.active') }}</label>
      </div>
      <div class="flex justify-content-end gap-2 mt-4">
        <Button :label="t('common.actions.cancel')" class="p-button-text" @click="emit('cancel')" />
        <Button :label="t('common.actions.save')" type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  status: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref({
  name: '',
  description: '',
  color: '#64748b',
  active: true,
  order: 0
})

watch(() => props.status, (newVal) => {
  if (newVal) {
    form.value = {
      name: newVal.name || '',
      description: newVal.description || '',
      color: newVal.color || '#64748b',
      active: newVal.active !== undefined ? newVal.active : true,
      order: newVal.order || 0
    }
  } else {
    form.value = {
      name: '',
      description: '',
      color: '#64748b',
      active: true,
      order: 0
    }
  }
}, { immediate: true })

function handleSubmit() {
  emit('submit', { ...form.value })
}
</script> 