<template>
  <div v-if="trashMode && canDelete('assets')" class="mt-4 flex justify-content-end">
    <Button 
      icon="pi pi-times" 
      :label="t('common.actions.clearTrash')" 
      severity="danger"
      @click="$emit('emptyTrash')"
    />
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { usePermissions } from '../../../composables/usePermissions'
import Button from 'primevue/button'

const props = defineProps({
  trashMode: { type: Boolean, default: false }
})

const emit = defineEmits(['emptyTrash'])

const { t } = useI18n()
const { canDelete } = usePermissions()
</script> 