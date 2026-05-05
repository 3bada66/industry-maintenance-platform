<template>
  <div>
    <div class="section-title">{{ t('assets.strings.technicalInfo') }}</div>
    <div class="info-list">
      <div><span class="label">{{ t('assets.fields.firmwareVersion') }}:</span> <span class="value">{{ asset.firmware_version || t('common.strings.na') }}</span></div>
      <div><span class="label">{{ t('assets.fields.installationDate') }}:</span> <span class="value">{{ formatDate(asset.installation_date) }}</span></div>
      <div><span class="label">{{ t('assets.fields.lastMaintenanceDate') }}:</span> <span class="value">{{ formatDate(asset.last_update_date) }}</span></div>
      <div><span class="label">{{ t('assets.fields.remoteAccess') }}:</span> <span class="value">{{ asset.remote_access ? t('common.strings.yes') : t('common.strings.no') }}</span></div>
      <div><span class="label">{{ t('assets.fields.remoteAccessType') }}:</span> <span class="value">{{ asset.remote_access_type ? getRemoteAccessTypeLabel(asset.remote_access_type) : t('common.strings.na') }}</span></div>
      <div><span class="label">{{ t('assets.fields.physicalAccessEase') }}:</span> <span class="value">{{ asset.physical_access_ease ? getPhysicalAccessLabel(asset.physical_access_ease) : t('common.strings.na') }}</span></div>
      <div><span class="label">{{ t('assets.fields.businessCriticality') }}:</span> <span class="value"><CriticalityBadge :value="asset.business_criticality" /></span></div>
      <div v-if="asset.protocols && asset.protocols.length">
        <span class="label">{{ t('assets.fields.protocols') }}:</span>
        <span class="value">
          <span v-for="(protocol, idx) in asset.protocols" :key="protocol + idx" class="protocol-badge">
            {{ protocol }}<span v-if="idx < asset.protocols.length - 1">, </span>
          </span>
        </span>
      </div>
    </div>
    <div class="section-title">{{ t('assets.strings.positionInfo') }}</div>
    <div class="info-list">
      <div><span class="label">{{ t('assets.fields.site') }}:</span> <span class="value">{{ asset.site?.name || t('common.strings.na') }}</span></div>
      <div><span class="label">{{ t('assets.fields.area') }}:</span> <span class="value">{{ asset.area_name || t('common.strings.na') }}</span></div>
      <div><span class="label">{{ t('assets.fields.location') }}:</span> <span class="value">{{ asset.location?.name || t('common.strings.na') }}</span></div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useDateFormatter } from '../../../composables/useDateFormatter'
import CriticalityBadge from '../../common/CriticalityBadge.vue'

const props = defineProps({
  asset: { type: Object, required: true },
  getRemoteAccessTypeLabel: { type: Function, required: true },
  getPhysicalAccessLabel: { type: Function, required: true }
})
const { t } = useI18n()
const { formatDate } = useDateFormatter()
</script>

<style scoped>
.section-title { font-weight: bold; margin-top: 1.5rem; margin-bottom: 0.5rem; }
.info-list { margin-bottom: 1rem; }
.label { font-weight: 500; color: #555; }
.value { color: #222; }
.protocol-badge { background: #f0f0f0; border-radius: 4px; padding: 0 0.3em; margin-right: 0.2em; }
</style> 