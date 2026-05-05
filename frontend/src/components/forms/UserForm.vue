<template>
  <form @submit.prevent="handleSubmit">
    <div class="p-fluid">
      <div class="p-field">
        <label for="name">{{ t('common.fields.name') }}</label>
        <InputText id="name" v-model="form.name" required maxlength="100" />
      </div>
      
      <div class="p-field">
        <label for="email">{{ t('common.fields.email') }}</label>
        <InputText id="email" v-model="form.email" type="email" required maxlength="254" />
      </div>
      
      <div class="p-field">
        <label for="role">{{ t('users.fields.role') }}</label>
        <Dropdown 
          id="role" 
          v-model="form.role_id" 
          :options="props.roles" 
          optionLabel="name" 
          optionValue="id" 
          required 
        />
      </div>
      
      <div class="p-field" v-if="!props.user">
        <label for="user_password_input">{{ t('users.fields.password') }}</label>
        <Password id="password" v-model="form.password" :feedback="false" :required="!props.user" toggleMask maxlength="100" inputId="user_password_input" />
      </div>
      
      <div class="p-field" v-else-if="canResetPassword">
        <Button :label="t('users.fields.resetPassword')" icon="pi pi-refresh" class="p-button-warning" @click.prevent="handleResetPassword" />
      </div>
      
      <div class="flex justify-content-end gap-2 mt-4">
        <Button :label="t('common.actions.cancel')" class="p-button-text" @click="handleCancel" />
        <Button :label="t('common.actions.save')" type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import Password from 'primevue/password'
import Button from 'primevue/button'

const props = defineProps({
  user: { type: Object, default: null },
  roles: { type: Array, default: () => [] },
  canResetPassword: { type: Boolean, default: false }
})

const { t } = useI18n()

const emit = defineEmits(['submit', 'cancel', 'reset-password'])

const form = ref({
  name: '',
  email: '',
  role_id: '',
  password: ''
})

watch(
  () => props.user,
  (user) => {
    if (user) {
      form.value = {
        name: user.name || '',
        email: user.email || '',
        role_id: user.role_id || '',
        password: ''
      }
    } else {
      form.value = {
        name: '',
        email: '',
        role_id: '',
        password: ''
      }
    }
  },
  { immediate: true }
)

// Set a default value for role_id if there is no user and there are roles available
watch(
  () => props.roles,
  (roles) => {
    if (!props.user && roles.length > 0 && !form.value.role_id) {
      form.value.role_id = roles[0].id
    }
  },
  { immediate: true }
)

function handleSubmit() {
  if (!form.value.role_id || !form.value.name || !form.value.email || (!props.user && !form.value.password)) {
    return;
  }
  emit('submit', { ...form.value, id: props.user ? props.user.id : undefined })
}

function handleCancel() {
  emit('cancel')
}

function handleResetPassword() {
  emit('reset-password', props.user)
}
</script>

<style scoped>
.p-field {
  margin-bottom: 1.5rem;
}
</style> 