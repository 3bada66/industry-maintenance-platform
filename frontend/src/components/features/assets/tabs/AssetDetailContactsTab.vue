<template>
  <div class="contacts-section">
    <div class="contacts-header">
      <h4>{{ t('assets.contacts.title') }}</h4>
      <div class="contacts-actions" v-if="canWrite">
        <MultiSelect 
          v-model="selectedContactIds" 
          :options="allContactsWithFullName" 
          optionLabel="fullName" 
          optionValue="id" 
          :placeholder="t('assets.contacts.addContacts')" 
          display="chip" 
          class="mr-2" 
          style="min-width:250px" 
        />
        <Button 
          :label="t('common.actions.save')" 
          icon="pi pi-check" 
          size="small"
          @click="updateAssetContacts" 
        />
        <Button 
          :label="t('common.actions.create')" 
          icon="pi pi-plus" 
          size="small"
          class="ml-2"
          @click="showContactDialog = true"
        />
      </div>
    </div>
    <div class="contacts-list mt-3">
      <DataTable 
        :value="contactsWithFullName" 
        :emptyMessage="t('assets.contacts.noContacts')"
        class="p-datatable-sm"
      >
        <Column field="fullName" :header="t('contacts.fields.fullName')" />
        <Column field="email" :header="t('common.fields.email')" />
        <Column field="phone1" :header="t('common.fields.phone')" />
        <Column field="type" :header="t('common.fields.type')" />
        <Column v-if="canWrite" :header="t('common.strings.actions')">
          <template #body="{ data }">
            <Button 
              icon="pi pi-trash" 
              class="p-button-rounded p-button-text p-button-danger" 
              @click="removeContact(data.id)" 
              :title="t('assets.contacts.removeContact')" 
            />
          </template>
        </Column>
      </DataTable>
    </div>
    <Dialog v-model:visible="showContactDialog" :header="t('assets.contacts.newContact')" modal :closable="true" :dismissableMask="true">
      <div class="p-fluid">
        <div class="field">
          <label>{{ t('contacts.fields.firstName') }}</label>
          <input v-model="newContact.first_name" type="text" class="p-inputtext" />
        </div>
        <div class="field">
          <label>{{ t('contacts.fields.lastName') }}</label>
          <input v-model="newContact.last_name" type="text" class="p-inputtext" />
        </div>
        <div class="field">
          <label>{{ t('common.fields.email') }}</label>
          <input v-model="newContact.email" type="email" class="p-inputtext" />
        </div>
        <div class="field">
          <label>{{ t('common.fields.phone') }}</label>
          <input v-model="newContact.phone1" type="text" class="p-inputtext" />
        </div>
        <div class="field">
          <label>{{ t('common.fields.type') }}</label>
          <input v-model="newContact.type" type="text" class="p-inputtext" />
        </div>
        <div class="flex justify-content-end gap-2 mt-3">
          <Button :label="t('common.actions.save')" icon="pi pi-check" class="p-button-sm" @click="createContact" />
          <Button :label="t('common.actions.cancel')" icon="pi pi-times" class="p-button-secondary p-button-sm" @click="showContactDialog = false" />
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MultiSelect from 'primevue/multiselect'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import api from '@/api/api'

const props = defineProps({
  assetId: { type: [String, Number], required: true },
  canWrite: { type: Boolean, default: false }
})
const emit = defineEmits(['updated'])
const { t } = useI18n()

const contacts = ref([])
const allContacts = ref([])
const selectedContactIds = ref([])
const loading = ref(false)
const showContactDialog = ref(false)
const newContact = ref({ first_name: '', last_name: '', email: '', phone1: '', type: '' })

function mapContact(contact) {
  return { ...contact, fullName: `${contact.first_name || ''} ${contact.last_name || ''}`.trim() }
}

const contactsWithFullName = computed(() =>
  (contacts.value || []).map(mapContact)
)
const allContactsWithFullName = computed(() =>
  (allContacts.value || []).map(mapContact)
)

async function fetchContacts() {
  loading.value = true
  try {
    const res = await api.getAssetContacts(props.assetId)
    contacts.value = res.data
    selectedContactIds.value = res.data.map(c => c.id)
  } finally {
    loading.value = false
  }
}

async function fetchAllContacts() {
  const res = await api.getContacts()
  allContacts.value = res.data
}

async function updateAssetContacts() {
  await api.updateAssetContacts(props.assetId, selectedContactIds.value)
  await fetchContacts()
  emit('updated')
}

async function removeContact(contactId) {
  await api.deleteAssetContact(props.assetId, contactId)
  await fetchContacts()
  selectedContactIds.value = contacts.value.map(c => c.id)
  emit('updated')
}

async function createContact() {
  await api.createContact(newContact.value)
  showContactDialog.value = false
  await fetchAllContacts()
  await fetchContacts()
  emit('updated')
}

onMounted(async () => {
  await fetchContacts()
  await fetchAllContacts()
})

watch(() => props.assetId, async (newId, oldId) => {
  if (newId !== oldId) {
    await fetchContacts()
    await fetchAllContacts()
  }
})
</script>

<style scoped>
.contacts-section { padding: 1rem 0; }
.contacts-header { display: flex; align-items: center; justify-content: space-between; }
.contacts-actions { display: flex; align-items: center; gap: 0.5rem; }
.contacts-list ul { list-style: none; padding: 0; margin: 0; }
.contacts-list li { margin-bottom: 0.3em; }
.text-muted { color: #888; }
</style> 