<template>
  <Dialog 
    :visible="isVisible" 
    @update:visible="val => $emit('update:isVisible', val)"
    :header="t('users.resetPassword')" 
    :modal="true" 
    :style="{ width: '500px' }"
    :closable="true"
    :closeOnEscape="true"
    :autoZIndex="true"
    :baseZIndex="1000"
    @hide="handleHide"
  >
    <div class="password-reset-content">
      <div class="mb-4">
        <i class="pi pi-check-circle text-green-500 text-2xl mb-3"></i>
        <h3 class="text-lg font-semibold mb-2">{{ t('users.resetPasswordSuccess') }}</h3>
        <p class="text-gray-600 mb-4">{{ t('users.temporaryPasswordInfo') }}</p>
      </div>
      
      <div class="password-display mb-4">
        <label class="block text-sm font-medium mb-2">{{ t('users.temporaryPassword') }}</label>
        <div class="flex gap-2">
          <InputText 
            :value="displayPassword" 
            readonly 
            class="flex-1 font-mono text-lg"
            :class="{ 'p-invalid': showCopyError }"
            ref="passwordInput"
            :autofocus="false"
          />
          <Button 
            icon="pi pi-copy" 
            @click="copyPassword"
            :label="t('common.copy')"
            severity="secondary"
          />
        </div>
        <small v-if="showCopyError" class="p-error">{{ t('users.copyError') }}</small>
      </div>
      
      <div class="user-info mb-4 p-3 bg-gray-50 rounded">
        <div class="text-sm text-gray-600">
          <strong>{{ t('users.userEmail') }}:</strong> {{ userEmail }}
        </div>
      </div>
      
      <div class="warning-box p-3 bg-yellow-50 border border-yellow-200 rounded">
        <div class="flex items-start gap-2">
          <i class="pi pi-exclamation-triangle text-yellow-600 mt-1"></i>
          <div class="text-sm text-yellow-800">
            <strong>{{ t('users.warning') }}:</strong> {{ t('users.passwordSecurityWarning') }}
          </div>
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="flex justify-content-end gap-2">
        <Button 
          :label="t('common.ok')" 
          @click="handleOk"
          severity="success"
        />
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, computed, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

const { t } = useI18n()

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  temporaryPassword: {
    type: String,
    default: ''
  },
  userEmail: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:isVisible', 'ok'])

const showCopyError = ref(false)
const passwordInput = ref(null)

// Computed property per assicurarci che la password sia sempre visibile
const displayPassword = computed(() => {
  return props.temporaryPassword || ''
})

function handleHide() {
  emit('update:isVisible', false)
}

function handleOk() {
  emit('ok')
  emit('update:isVisible', false)
}

async function copyPassword() {
  try {
    await navigator.clipboard.writeText(displayPassword.value)
    showCopyError.value = false
  } catch (error) {
    showCopyError.value = true
    setTimeout(() => {
      showCopyError.value = false
    }, 3000)
  }
}

// Reset error when dialog opens and ensure password is visible
watch(() => props.isVisible, async (newVal) => {
  if (newVal) {
    showCopyError.value = false
    // Assicurati che la password sia visibile dopo che il dialog è stato renderizzato
    await nextTick()
    // Focus sul campo password solo se c'è una password da mostrare
    if (passwordInput.value && displayPassword.value) {
      passwordInput.value.$el.focus()
    }
  }
})
</script>

<style scoped>
.password-reset-content {
  padding: 1rem 0;
}

.password-display {
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  padding: 1rem;
}

.warning-box {
  border-left: 4px solid #fbbf24;
}
</style> 