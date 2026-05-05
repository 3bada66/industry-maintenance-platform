<template>
  <div>
    <AssetPhotoUpload :assetId="assetId" :readOnly="readOnly" />
    <AssetDocumentUpload :assetId="assetId" :readOnly="readOnly" />
  </div>
</template>

<script setup>
import AssetPhotoUpload from '../components/AssetPhotoUpload.vue'
import AssetDocumentUpload from '../components/AssetDocumentUpload.vue'
const props = defineProps({
  assetId: { type: [String, Number], required: true },
  readOnly: { type: Boolean, default: false }
})
</script> 