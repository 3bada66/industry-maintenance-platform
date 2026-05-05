<!--
  - AssetTypeForm.vue
  - Componente per il form di creazione/modifica di un tipo di asset
  - Utilizza i componenti PrimeVue per la gestione del form
-->
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
        <label for="purdue_level">{{ t('assettypes.fields.purdueLevel') }}</label>
        <Dropdown id="purdue_level" v-model="form.purdue_level" :options="purdueLevels" optionLabel="label" optionValue="value" :placeholder="t('assettypes.strings.selectPurdueLevel')" />
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
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  assettype: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref({
  name: '',
  description: '',
  purdue_level: null
})

const purdueLevels = [
  { value: 0, label: t('assettypes.level0') },
  { value: 1, label: t('assettypes.level1') },
  { value: 1.5, label: t('assettypes.level1_5') },
  { value: 2, label: t('assettypes.level2') },
  { value: 3, label: t('assettypes.level3') },
  { value: 4, label: t('assettypes.level4') }
]

watch(() => props.assettype, (newVal) => {
  if (newVal) {
    form.value = {
      name: newVal.name || '',
      description: newVal.description || '',
      purdue_level: newVal.purdue_level ?? null
    }
  } else {
    form.value = {
      name: '',
      description: '',
      purdue_level: null
    }
  }
}, { immediate: true })

function handleSubmit() {
  emit('submit', { ...form.value })
}

</script>
