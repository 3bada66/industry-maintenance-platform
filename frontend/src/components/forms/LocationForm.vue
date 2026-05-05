<template>
  <form @submit.prevent="handleSubmit">
    <div class="p-fluid">
      <div class="p-field">
        <label for="name">{{ t('common.fields.name') }}</label>
        <InputText id="name" v-model="form.name" required />
      </div>
      <div class="p-field">
        <label for="code">{{ t('common.fields.code') }}</label>
        <InputText id="code" v-model="form.code" />
      </div>
      <div class="p-field">
        <label for="description">{{ t('common.fields.description') }}</label>
        <Textarea id="description" v-model="form.description" rows="3" />
      </div>
      <div class="p-field">
        <label for="site_id">{{ t('common.fields.site') }}</label>
        <Dropdown
          id="site_id"
          v-model="form.site_id"
          :options="sites"
          optionLabel="name"
          optionValue="id"
          :placeholder="t('common.strings.select')"
          class="w-full"
          :showClear="true"
        />
      </div>
      <div class="p-field">
        <label for="area_id">{{ t('locations.fields.area') }}</label>
        <Dropdown
          id="area_id"
          v-model="form.area_id"
          :options="filteredAreas"
          optionLabel="name"
          optionValue="id"
          :placeholder="t('common.strings.select')"
          class="w-full"
          :showClear="true"
          :disabled="!form.site_id || filteredAreas.length === 0"
        />
      </div>
      <div class="p-field">
        <label for="notes">{{ t('common.fields.notes') }}</label>
        <Textarea id="notes" v-model="form.notes" rows="4" />
      </div>
      
      <div class="flex justify-content-end gap-2 mt-4">
        <Button :label="t('common.actions.cancel')" class="p-button-text" @click="emit('cancel')" />
        <Button :label="t('common.actions.save')" type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'

const { t } = useI18n()

const props = defineProps({
  location: {
    type: Object,
    default: null,
  },
  sites: {
    type: Array,
    default: () => []
  },
  areas: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['submit', 'cancel', 'site-changed'])

const form = ref({
  name: '',
  code: '',
  description: '',
  area_id: null,
  notes: '',
  site_id: null
})

// Filter areas based on selected site
const filteredAreas = computed(() => {
  if (!form.value.site_id) {
    return []
  }
  return props.areas.filter(area => area.site_id === form.value.site_id)
})

watch(
  () => props.location,
  (loc) => {
    if (loc) {
      form.value = {
        name: loc.name || '',
        code: loc.code || '',
        description: loc.description || '',
        notes: loc.notes || '',
        area_id: loc.area_id || null,
        site_id: loc.site_id || null
      }
    } else {
      form.value = {
        name: '',
        code: '',
        description: '',
        notes: '',
        area_id: null,
        site_id: null
      }
    }
  },
  { immediate: true }
)

watch(
  () => form.value.site_id,
  (newSiteId, oldSiteId) => {
    // Reset area when site changes
    if (newSiteId !== oldSiteId) {
    form.value.area_id = null
      if (newSiteId) {
        emit('site-changed', newSiteId)
      }
  }
}
)

function handleSubmit() {
  emit('submit', { ...form.value })
}
</script>

<style scoped>
.p-field {
  margin-bottom: 1.5rem;
}

.p-dropdown {
  min-height: 2.5rem;
}

.p-dropdown .p-dropdown-label {
  font-size: 1rem;
  padding: 0.75rem 1rem;
}

.p-dropdown .p-dropdown-trigger {
  width: 2.5rem;
}
</style>
