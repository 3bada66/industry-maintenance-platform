<template>
  <Card class="mb-4">
    <template #title>
      <div class="flex align-items-center">
        <i class="pi pi-calendar mr-2"></i>
        {{ t('assets.strings.datesInfo') }}
      </div>
    </template>
    <template #content>
      <div class="grid">
        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="installation_date">{{ t('assets.fields.installationDate') }}</label>
            <Calendar id="installation_date" v-model="form.installation_date" dateFormat="dd/mm/yy" showIcon class="w-full" />
          </div>
        </div>

        <div class="col-12 md:col-6">
          <div class="p-field">
            <label for="last_update_date">{{ t('assets.fields.lastMaintenanceDate') }}</label>
            <Calendar id="last_update_date" v-model="form.last_update_date" dateFormat="dd/mm/yy" showIcon class="w-full" />
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import Card from 'primevue/card'
import Calendar from 'primevue/calendar'

const props = defineProps({
  form: { type: Object, required: true }
})

const { t } = useI18n()
</script>

<style scoped>
.p-field {
  margin-bottom: 1rem;
}

.p-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
</style> 