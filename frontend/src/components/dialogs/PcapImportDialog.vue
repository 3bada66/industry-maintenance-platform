<template>
  <Dialog v-model:visible="visible" :modal="true" :closable="true" :header="t('assetCommunications.importPcap')" :style="{ width: '400px' }">
    <div class="pcap-import-dialog">
      <p>{{ t('assetCommunications.importPcapDesc') }}</p>
      <!-- Placeholder per upload file -->
      <input type="file" accept=".pcap" />
      <div class="mt-3">
        <Button :label="t('common.actions.cancel')" class="p-button-secondary p-button-sm" @click="$emit('update:visible', false)" />
        <Button :label="t('assetCommunications.import')" class="p-button-sm ml-2" />
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
const props = defineProps({
  modelValue: Boolean,
  visible: Boolean
})
const { t } = useI18n()
</script>

<style scoped>
.pcap-import-dialog {
  padding: 1em 0;
}
.mt-3 { margin-top: 1em; }
.ml-2 { margin-left: 0.7em; }
</style> 