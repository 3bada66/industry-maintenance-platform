<template>
  <div class="contact-detail" v-if="contact">
    <div class="page-header">
      <Button icon="pi pi-arrow-left" :label="t('common.actions.back')" class="p-button-text" @click="router.go(-1)" />
      <h1>{{ contact.fullName }}</h1>
    </div>
    <Card>
      <template #title>{{ t('contacts.strings.info') }}</template>
      <template #content>
        <div class="grid">
          <div class="col-12 md:col-6">
            <p><strong>{{ t('contacts.fields.firstName') }}:</strong> {{ contact.first_name }}</p>
            <p><strong>{{ t('contacts.fields.lastName') }}:</strong> {{ contact.last_name }}</p>
            <p><strong>{{ t('common.fields.email') }}:</strong> {{ contact.email || t('common.strings.na') }}</p>
            <p><strong>{{ t('contacts.fields.phone1') }}:</strong> {{ contact.phone1 || t('common.strings.na') }}</p>
            <p><strong>{{ t('contacts.fields.phone2') }}:</strong> {{ contact.phone2 || t('common.strings.na') }}</p>
            <p><strong>{{ t('contacts.fields.type') }}:</strong> {{ contact.type || t('common.strings.na') }}</p>
            <p><strong>{{ t('contacts.fields.notes') }}:</strong> {{ contact.notes || t('common.strings.na') }}</p>
          </div>
        </div>
      </template>
    </Card>
    <div class="mt-5">
      <h3 class="text-lg font-semibold mb-2">{{ t('common.strings.linkedAssets') }}</h3>
      <ul>
        <li v-for="asset in assets" :key="asset.id">
          <RouterLink :to="`/assets/${asset.id}`">{{ asset.name || asset.id }}</RouterLink>
        </li>
        <li v-if="assets.length === 0">{{ t('common.strings.na') }}</li>
      </ul>
      <h3 class="text-lg font-semibold mt-4 mb-2">{{ t('common.strings.linkedSites') }}</h3>
      <ul>
        <li v-for="site in sites" :key="site.id">
          <RouterLink :to="`/sites/${site.id}`">{{ site.name || site.id }}</RouterLink>
        </li>
        <li v-if="sites.length === 0">{{ t('common.strings.na') }}</li>
      </ul>
      <h3 class="text-lg font-semibold mt-4 mb-2">{{ t('common.strings.linkedLocations') }}</h3>
      <ul>
        <li v-for="location in locations" :key="location.id">
          <RouterLink :to="`/locations/${location.id}`">{{ location.name || location.id }}</RouterLink>
        </li>
        <li v-if="locations.length === 0">{{ t('common.strings.na') }}</li>
      </ul>
      <h3 class="text-lg font-semibold mt-4 mb-2">{{ t('common.strings.linkedSuppliers') }}</h3>
      <ul>
        <li v-for="supplier in suppliers" :key="supplier.id">
          <RouterLink :to="`/suppliers/${supplier.id}`">{{ supplier.name || supplier.id }}</RouterLink>
        </li>
        <li v-if="suppliers.length === 0">{{ t('common.strings.na') }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '../api/api'
import Card from 'primevue/card'
import Button from 'primevue/button'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const contact = ref(null)
const assets = ref([])
const sites = ref([])
const locations = ref([])
const suppliers = ref([])

function mapContact(c) {
  return { ...c, fullName: `${c.first_name} ${c.last_name}` }
}

onMounted(async () => {
  const response = await api.getContact(route.params.id)
  contact.value = mapContact(response.data)
  // fetch linked entities if present as IDs
  if (response.data.assets && response.data.assets.length) {
    assets.value = await Promise.all(response.data.assets.map(async id => {
      try {
        const res = await api.getAsset(id)
        return res.data
      } catch { return { id } }
    }))
  }
  if (response.data.sites && response.data.sites.length) {
    sites.value = await Promise.all(response.data.sites.map(async id => {
      try {
        const res = await api.getSite(id)
        return res.data
      } catch { return { id } }
    }))
  }
  if (response.data.locations && response.data.locations.length) {
    locations.value = await Promise.all(response.data.locations.map(async id => {
      try {
        const res = await api.getLocation(id)
        return res.data
      } catch { return { id } }
    }))
  }
  if (response.data.suppliers && response.data.suppliers.length) {
    suppliers.value = await Promise.all(response.data.suppliers.map(async id => {
      try {
        const res = await api.getSupplier(id)
        return res.data
      } catch { return { id } }
    }))
  }
})
</script>

<style scoped>
.contact-detail {
  padding: 1rem;
}
.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
</style> 