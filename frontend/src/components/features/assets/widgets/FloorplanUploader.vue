
<script setup>
import { ref, computed } from 'vue'
import FileUpload from 'primevue/fileupload'
import { useToast } from 'primevue/usetoast'
import api from '@/api/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  locationId: {
    type: String,
    required: true
  },
  floorplan: {
    type: [String, Object],
    default: null
  },
})
const emit = defineEmits(['uploaded'])

const uploading = ref(false)
const toast = useToast()

// Computed property to handle the image URL
const floorplanUrl = computed(() => {
  if (!props.floorplan) return null
  
  // If it's already a string (URL), use it directly
  if (typeof props.floorplan === 'string') {
    return props.floorplan
  }
  
  // If it's an object, construct the URL
  if (props.floorplan && props.floorplan.file_path) {
    const baseUrl = '/api'
    return `${baseUrl}/locations/${props.locationId}/floorplan/${props.floorplan.id}`
  }
  
  return null
})

async function uploadFloorplan({ files }) {
  const file = files[0]
  if (!file) {
    toast.add({ severity: 'warn', summary: t('common.messages.error'), detail: t('locations.floorplan.noFileSelected') })
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  uploading.value = true
  try {
    await api.uploadFloorplan(props.locationId, formData)
    toast.add({ severity: 'success', summary: t('common.messages.success'), detail: t('locations.floorplan.floorplanUploaded') })
    emit('uploaded')
  } catch (error) {
    console.error('Upload error:', error)
    toast.add({ severity: 'error', summary: t('common.messages.error'), detail: t('locations.floorplan.uploadError') })
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="mt-3">
    <h4>{{ t('locations.floorplan.title') }}</h4>

    <div v-if="floorplanUrl" class="mb-3">
      <p>{{ t('locations.floorplan.currentFloorplan') }}:</p>
      <img :src="floorplanUrl" alt="Planimetria" style="max-width: 100%; max-height: 300px;" />
    </div>

<FileUpload
  name="file"
  customUpload
  :auto="false"
  :chooseLabel="t('locations.floorplan.chooseLabel')"
  :uploadLabel="t('locations.floorplan.uploadLabel')"
  @uploader="uploadFloorplan"
  :disabled="uploading"
  accept="image/*"
/>

  </div>
</template>
