<!--
  - ManufacturerDetail.vue
  - Componente per la visualizzazione dei dettagli di un fornitore
  - Utilizza i componenti PrimeVue per la gestione del form
-->
<template>
  <div class="p-4">
    <Button icon="pi pi-arrow-left" :label="t('common.actions.back')" class="mb-3" @click="goBack" />
    <h2 class="text-xl mb-4">{{ t('manufacturers.title') }}</h2>

    <div class="mb-4">
      <h3 class="text-lg font-semibold">{{ t('common.strings.info') }}</h3>
      <p><strong>{{ t('common.fields.name') }}:</strong> {{ manufacturer.name }}</p>
      <p><strong>{{ t('common.fields.description') }}:</strong> {{ manufacturer.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/api'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const manufacturerId = route.params.id

const manufacturer = ref({})

function goBack() {
  router.push({ name: 'Manufacturers' })
}

async function fetchManufacturer() {
  const res = await api.getManufacturer(`${manufacturerId}`)
  manufacturer.value = res.data
}

onMounted(async () => {
  await fetchManufacturer()
})
</script>
