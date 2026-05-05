<template>
  <div class="dashboard">
    <!-- Header con benvenuto e azioni rapide -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1>{{ t('dashboard.title') }}</h1>
        <p class="welcome-text">{{ t('dashboard.welcome') }}</p>
      </div>
      <div class="quick-actions">
        <Button 
          :label="t('dashboard.actions.viewAllAssets')" 
          icon="pi pi-list" 
          @click="$router.push('/assets')"
          class="p-button-outlined"
        />
        <Button 
          :label="t('dashboard.actions.recalculateRiskScores')" 
          icon="pi pi-refresh" 
          @click="recalculateRiskScores"
          :loading="recalculatingRiskScores"
          class="p-button-outlined p-button-secondary"
        />
      </div>
    </div>

    <!-- Metriche principali -->
    <div class="metrics-grid">
      <div class="metric-card total-assets">
        <div class="metric-icon">
          <i class="pi pi-database"></i>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ stats.total_assets || 0 }}</div>
          <div class="metric-label">{{ t('dashboard.stats.totalAssets') }}</div>
        </div>
      </div>

      <div class="metric-card critical-assets">
        <div class="metric-icon">
          <i class="pi pi-exclamation-triangle"></i>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ stats.critical_assets || 0 }}</div>
          <div class="metric-label">{{ t('dashboard.stats.criticalAssets') }}</div>
        </div>
      </div>

      <div class="metric-card risky-assets">
        <div class="metric-icon">
          <i class="pi pi-shield"></i>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ stats.assets_at_risk || 0 }}</div>
          <div class="metric-label">{{ t('dashboard.stats.assetsAtRisk') }}</div>
        </div>
      </div>

      <div class="metric-card recent-changes">
        <div class="metric-icon">
          <i class="pi pi-clock"></i>
        </div>
        <div class="metric-content">
          <div class="metric-value">{{ stats.recent_changes || 0 }}</div>
          <div class="metric-label">{{ t('dashboard.stats.recentChanges') }}</div>
        </div>
      </div>
    </div>

    <!-- Grafici e analisi -->
    <div class="charts-section">
      <div class="chart-row">
        <!-- Distribuzione per tipo -->
        <div class="simple-card">
          <div class="card-title">
            <i class="pi pi-chart-pie"></i>
            {{ t('dashboard.charts.assetsByType') }}
          </div>
          <div class="chart-container" v-if="assetTypeChartData.labels.length > 0">
            <Doughnut 
              :key="`asset-type-${chartKey}`"
              :data="assetTypeChartData" 
              :options="doughnutOptions" 
              class="chart"
            />
          </div>
          <div v-else class="no-data">
            {{ t('common.messages.noData') }}
          </div>
        </div>

        <!-- Distribuzione per stato -->
        <div class="simple-card">
          <div class="card-title">
            <i class="pi pi-chart-bar"></i>
            {{ t('dashboard.charts.assetsByStatus') }}
          </div>
          <div class="chart-container" v-if="statusChartData.labels.length > 0">
            <Bar 
              :key="`status-${chartKey}`"
              :data="statusChartData" 
              :options="barOptions" 
              class="chart"
            />
          </div>
          <div v-else class="no-data">
            {{ t('common.messages.noData') }}
          </div>
        </div>
      </div>
    </div>

    <!-- Tabelle informative -->
    <div class="tables-section">
      <div class="table-row">
        <!-- Asset più a rischio -->
        <div class="simple-card">
          <div class="card-title">
            <i class="pi pi-exclamation-triangle"></i>
            {{ t('dashboard.tables.topRiskyAssets') }}
          </div>
          <div v-if="riskyAssets.length === 0" class="no-data">
            {{ t('common.messages.noData') }}
          </div>
          <DataTable 
            v-else
            :value="riskyAssets" 
            :rows="5" 
            responsiveLayout="scroll"
            class="dashboard-table"
          >
            <Column field="name" :header="t('common.fields.name')" sortable>
              <template #body="{ data }">
                <router-link :to="`/assets/${data.id}`" class="asset-link">
                  {{ data.name }}
                </router-link>
              </template>
            </Column>
            <Column field="risk_score" :header="t('common.fields.riskScore')" sortable>
              <template #body="{ data }">
                <Tag 
                  :value="data.risk_score" 
                  :severity="getRiskSeverity(data.risk_score)"
                />
              </template>
            </Column>
            <Column field="business_criticality" :header="t('common.fields.businessCriticality')" sortable>
              <template #body="{ data }">
                <CriticalityBadge :value="data.business_criticality" />
              </template>
            </Column>
            <Column field="asset_type_name" :header="t('common.fields.type')" />
            <Column field="status_name" :header="t('common.fields.status')" />
            <Column field="site_name" :header="t('common.fields.site')" />
          </DataTable>
        </div>

        <!-- Ultimi asset -->
        <div class="simple-card">
          <div class="card-title">
            <i class="pi pi-clock"></i>
            {{ t('dashboard.tables.latestAssets') }}
          </div>
          <div v-if="recentAssets.length === 0" class="no-data">
            {{ t('common.messages.noData') }}
          </div>
          <DataTable 
            v-else
            :value="recentAssets" 
            :rows="5" 
            responsiveLayout="scroll"
            class="dashboard-table"
          >
            <Column field="name" :header="t('common.fields.name')" sortable>
              <template #body="{ data }">
                <router-link :to="`/assets/${data.id}`" class="asset-link">
                  {{ data.name }}
                </router-link>
              </template>
            </Column>
            <Column field="asset_type.name" :header="t('common.fields.type')" />
            <Column field="status.name" :header="t('common.fields.status')" />
            <Column field="site.name" :header="t('common.fields.site')" />
            <Column field="created_at" :header="t('common.fields.createdAt')" sortable>
              <template #body="{ data }">
                {{ formatDate(data.created_at) }}
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>

    <!-- Sezione avvisi e notifiche -->
    <div class="alerts-section">
      <div class="simple-card">
        <div class="card-title">
          <i class="pi pi-bell"></i>
          {{ t('dashboard.alerts') }}
        </div>
        <div class="alerts-content">
          <div v-if="stats.assets_at_risk > 0" class="alert-item warning">
            <i class="pi pi-exclamation-triangle"></i>
            <span>{{ stats.assets_at_risk }} {{ t('dashboard.stats.assetsAtRisk') }}</span>
          </div>
          <div v-if="stats.critical_assets > 0" class="alert-item critical">
            <i class="pi pi-exclamation-circle"></i>
            <span>{{ stats.critical_assets }} {{ t('dashboard.stats.criticalAssets') }}</span>
          </div>
          <div v-if="stats.assets_at_risk === 0 && stats.critical_assets === 0" class="alert-item success">
            <i class="pi pi-check-circle"></i>
            <span>{{ t('dashboard.messages.allSystemsOperational') }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue/usetoast'
import { Doughnut, Bar } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'

// Registra i componenti necessari per Chart.js
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement)
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Card from 'primevue/card'
import CriticalityBadge from '../components/common/CriticalityBadge.vue'
import api from '../api/api'

const { t } = useI18n()
const router = useRouter()
const toast = useToast()

// Reactive data
const stats = ref({})
const assetTypes = ref([])
const recentAssets = ref([])
const riskyAssets = ref([])
const recalculatingRiskScores = ref(false)

// Chart data
const assetTypeChartData = ref({ labels: [], datasets: [] })
const statusChartData = ref({ labels: [], datasets: [] })
const chartKey = ref(0) // Per forzare il re-render dei grafici

// Chart options
const doughnutOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { 
      display: true,
      position: 'bottom'
    }
  }
})

const barOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
})

// Computed functions
const getRiskSeverity = (score) => {
  if (score >= 8) return 'danger'
  if (score >= 6) return 'warning'
  return 'info'
}

const getCriticalitySeverity = (level) => {
  if (level >= 4) return 'danger'
  if (level >= 3) return 'warning'
  return 'info'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

// Funzione per ricalcolare i risk score
const recalculateRiskScores = async () => {
  recalculatingRiskScores.value = true
  try {
    const response = await api.recalculateAllRiskScores()
    console.log('Risk scores ricalcolati:', response.data)
    
    // Ricarica i dati della dashboard
    await loadDashboardData()
    
    // Mostra messaggio di successo
    toast.add({
      severity: 'success',
      summary: t('common.messages.success'),
      detail: response.data.message || 'Risk scores aggiornati con successo!',
      life: 3000
    })
  } catch (error) {
    console.error('Errore durante il ricalcolo dei risk score:', error)
    toast.add({
      severity: 'error',
      summary: t('common.messages.error'),
      detail: 'Errore durante il ricalcolo dei risk score',
      life: 3000
    })
  } finally {
    recalculatingRiskScores.value = false
  }
}

// Watcher per reagire ai cambiamenti dei dati
watch(() => stats.value, (newStats) => {
  if (newStats && (newStats.type_stats || newStats.status_stats)) {
    prepareChartData()
  }
}, { deep: true })

// Funzione per caricare i dati della dashboard
const loadDashboardData = async () => {
  try {
    // Carica statistiche
    const statsRes = await api.getDashboardStats()
    stats.value = statsRes.data

    // Carica asset a rischio
    const riskyRes = await api.getRiskyAssets(5)
    riskyAssets.value = Array.isArray(riskyRes.data) ? riskyRes.data : []

    // Carica ultimi asset
    const recentRes = await api.getAssets({ limit: 5 })
    recentAssets.value = Array.isArray(recentRes.data) ? recentRes.data : []

    // Prepara dati per i grafici
    prepareChartData()
  } catch (error) {
    console.error('Error loading dashboard data:', error.response?.data || error  )
  }
}

// Load data
onMounted(async () => {
  await loadDashboardData()
})

const prepareChartData = () => {
  // Incrementa la key per forzare il re-render
  chartKey.value++
  
  // Grafico asset per tipo
  if (stats.value.type_stats && Array.isArray(stats.value.type_stats) && stats.value.type_stats.length > 0) {
    // Filtra solo i tipi con asset_count > 0
    const validTypes = stats.value.type_stats.filter(t => t.asset_count > 0)
    
    if (validTypes.length > 0) {
      assetTypeChartData.value = {
        labels: validTypes.map(t => t.name),
        datasets: [{
          label: 'Asset per tipo',
          data: validTypes.map(t => t.asset_count),
          backgroundColor: [
            '#42A5F5', '#66BB6A', '#FFA726', '#AB47BC', '#FF7043', 
            '#26A69A', '#D4E157', '#FFCA28', '#8D6E63', '#789262'
          ],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      }
    } else {
      assetTypeChartData.value = { labels: [], datasets: [] }
    }
  } else {
    assetTypeChartData.value = { labels: [], datasets: [] }
  }

  // Grafico asset per stato
  if (stats.value.status_stats && Array.isArray(stats.value.status_stats) && stats.value.status_stats.length > 0) {
    statusChartData.value = {
      labels: stats.value.status_stats.map(s => s.name),
      datasets: [{
        label: t('dashboard.stats.totalAssets'),
        data: stats.value.status_stats.map(s => s.count),
        backgroundColor: stats.value.status_stats.map(s => s.color || '#42A5F5'),
        borderWidth: 1,
        borderColor: '#fff'
      }]
    }
  } else {
    statusChartData.value = { labels: [], datasets: [] }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  background: #f8f9fa;
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.header-content h1 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 700;
}

.welcome-text {
  margin: 0;
  color: #6c757d;
  font-size: 1.1rem;
}

.quick-actions {
  display: flex;
  gap: 1rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.total-assets .metric-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.critical-assets .metric-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.risky-assets .metric-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.recent-changes .metric-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.metric-label {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.charts-section {
  margin-bottom: 2rem;
}

.chart-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.simple-card {
  flex: 1;
  min-width: 0;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  overflow: hidden;
}

.card-title {
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-container {
  padding: 1rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart {
  width: 100%;
  height: 300px;
  min-height: 300px;
}



.no-data {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
  font-style: italic;
}

.tables-section {
  margin-bottom: 2rem;
}

.table-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 1.5rem;
}

.table-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.table-card :deep(.p-card-title) {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.dashboard-table {
  font-size: 0.9rem;
}

.asset-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.asset-link:hover {
  text-decoration: underline;
}

.alerts-section {
  margin-bottom: 2rem;
}

.alerts-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
}

.alert-item.warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.alert-item.critical {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-item.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-item i {
  font-size: 1.2rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .quick-actions {
    justify-content: center;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-row,
  .table-row {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 1.5rem;
  }
  
  .metric-value {
    font-size: 2rem;
  }
}
</style>
