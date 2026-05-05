<template>
  <div v-if="checking" class="setup-detector">
    <div class="loading-container">
      <div class="spinner"></div>
      <p>{{ t('setup.checking') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '@/api/api'

const router = useRouter()
const { t } = useI18n()
const checking = ref(true)

const checkSetupStatus = async () => {
  try {
    const response = await api.getSetupStatus()
    const status = response.data
    
    // Se il sistema non è configurato, reindirizza al wizard
    if (!status.is_configured) {
      router.push('/setup-wizard')
      return
    }
    
    // Se il sistema è configurato, continua normalmente
    checking.value = false
  } catch (error) {
    console.error('Error checking setup status:', error)
    // In caso di errore, continua normalmente
    checking.value = false
  }
}

onMounted(() => {
  checkSetupStatus()
})
</script>

<style scoped>
.setup-detector {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-container {
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  color: #6c757d;
  font-size: 1.1rem;
}
</style> 