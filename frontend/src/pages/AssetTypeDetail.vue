<template>
  <div class="p-4">
    <h2 class="text-xl mb-4">{{ t('assettypes.title') }}</h2>
    <div class="mb-4">
      <h3 class="text-lg font-semibold">{{ t('common.strings.info') }}</h3>
      <p><strong>{{ t('common.fields.name') }}:</strong> {{ assettype.name }}</p>
      <p><strong>{{ t('common.fields.description') }}:</strong> {{ assettype.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/api'

import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const route = useRoute()
const assettypeId = route.params.id

const assettype = ref({})

async function fetchAssetType() {
  const res = await api.getAssetType(`${assettypeId}`)
  assettype.value = res.data
}

onMounted(async () => {
  await fetchAssetType()
})
</script>
