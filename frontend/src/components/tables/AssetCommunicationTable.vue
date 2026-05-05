<template>
  <div class="asset-comm-table">
    <table v-if="rows.length" class="comm-table">
      <thead>
        <tr>
          <th>{{ t('assets.communications.sourceAsset') }}</th>
          <th>{{ t('assets.communications.sourceInterface') }}</th>
          <th>{{ t('assets.communications.destinationAsset') }}</th>
          <th>{{ t('assets.communications.destinationInterface') }}</th>
          <th>{{ t('assets.communications.packets') }}</th>
          <th>{{ t('assets.communications.direction') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in rows" :key="idx">
          <td>{{ row.src_asset?.name }}</td>
          <td>
            <div v-if="row.src_interface">
              <div><b>{{ row.src_interface.name }}</b></div>
              <div v-if="row.src_interface.mac_address">MAC: {{ row.src_interface.mac_address }}</div>
              <div v-if="row.src_interface.ip_address">IP: {{ row.src_interface.ip_address }}</div>
            </div>
          </td>
          <td>{{ row.dst_asset?.name }}</td>
          <td>
            <div v-if="row.dst_interface">
              <div><b>{{ row.dst_interface.name }}</b></div>
              <div v-if="row.dst_interface.mac_address">MAC: {{ row.dst_interface.mac_address }}</div>
              <div v-if="row.dst_interface.ip_address">IP: {{ row.dst_interface.ip_address }}</div>
            </div>
          </td>
          <td>{{ row.packet_count }}</td>
          <td>{{ row.direction === 'outgoing' ? t('assets.communications.outgoing') : t('assets.communications.incoming') }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="placeholder">
      <span>{{ t('assets.communications.noTableData') }}</span>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
const props = defineProps({
  type: { type: String, default: 'physical' },
  rows: { type: Array, default: () => [] }
})
const { t } = useI18n()
</script>

<style scoped>
.asset-comm-table {
  margin-bottom: 2em;
}
.comm-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.comm-table th, .comm-table td {
  border: 1px solid #e5e7eb;
  padding: 0.5em 0.75em;
  text-align: left;
}
.comm-table th {
  background: #f3f4f6;
}
.placeholder {
  text-align: center;
  color: #888;
  padding: 2em 0;
}
</style> 