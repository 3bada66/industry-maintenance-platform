<template>
  <div class="monitoring-page">

    <!-- Header -->
    <div class="monitoring-header">
      <div class="header-content">
        <h1>
          <i class="pi pi-heart-fill" style="margin-right: 0.5rem;"></i>
          Technical Monitoring
        </h1>
        <p class="welcome-text">Real-time system health — auto-refreshes every 30 seconds</p>
      </div>
      <div class="header-actions">
        <span class="last-updated" v-if="lastUpdated">
          Last updated: {{ lastUpdated }}
        </span>
        <Button
          label="Refresh Now"
          icon="pi pi-refresh"
          :loading="loading"
          @click="fetchHealth"
          class="p-button-outlined p-button-sm"
          style="margin-left: 1rem;"
        />
      </div>
    </div>

    <!-- Error banner -->
    <div v-if="fetchError" class="error-banner">
      <i class="pi pi-exclamation-triangle"></i>
      Could not reach the health endpoint. The system may be starting up or unreachable.
    </div>

    <!-- Overall status card -->
    <div class="status-banner" :class="statusClass" v-if="health">
      <i :class="statusIcon" style="font-size: 1.5rem; margin-right: 0.75rem;"></i>
      <div>
        <div class="status-label">Overall System Status</div>
        <div class="status-value">{{ health.status?.toUpperCase() }}</div>
      </div>
      <div class="status-meta">
        <span>Version {{ health.version }}</span>
        <span style="margin-left: 1rem;">Uptime {{ formatUptime(health.uptime_seconds) }}</span>
        <span style="margin-left: 1rem;">Environment: {{ health.environment }}</span>
      </div>
    </div>

    <!-- Component cards -->
    <div class="metrics-grid" v-if="health">

      <!-- Database -->
      <div class="metric-card" :class="componentClass(health.components?.database?.status)">
        <div class="metric-icon">
          <i class="pi pi-database"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">Database (PostgreSQL)</div>
          <div class="metric-value component-status">
            <Tag
              :value="health.components?.database?.status || 'unknown'"
              :severity="tagSeverity(health.components?.database?.status)"
            />
          </div>
          <div class="metric-detail" v-if="health.components?.database?.response_time_ms !== undefined">
            Response: {{ health.components.database.response_time_ms }} ms
          </div>
          <div class="metric-detail" v-if="health.components?.database?.pool_size">
            Pool: {{ health.components.database.pool_checked_out }} /
            {{ health.components.database.pool_size }} connections
          </div>
        </div>
      </div>

      <!-- Cache -->
      <div class="metric-card" :class="componentClass(health.components?.cache?.status)">
        <div class="metric-icon">
          <i class="pi pi-bolt"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">Cache Layer</div>
          <div class="metric-value component-status">
            <Tag
              :value="health.components?.cache?.status || 'unknown'"
              :severity="tagSeverity(health.components?.cache?.status)"
            />
          </div>
          <div class="metric-detail">
            Type: {{ health.components?.cache?.type || 'N/A' }}
          </div>
        </div>
      </div>

      <!-- API -->
      <div class="metric-card" :class="componentClass(health.components?.api?.status)">
        <div class="metric-icon">
          <i class="pi pi-server"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">API Server (FastAPI)</div>
          <div class="metric-value component-status">
            <Tag
              :value="health.components?.api?.status || 'unknown'"
              :severity="tagSeverity(health.components?.api?.status)"
            />
          </div>
          <div class="metric-detail">
            Python {{ health.system?.python_version || 'N/A' }}
          </div>
        </div>
      </div>

    </div>

    <!-- System resources -->
    <div class="resources-section" v-if="health?.system && hasSystemMetrics">
      <h3>System Resources</h3>
      <div class="resources-grid">

        <div class="resource-card" v-if="health.system.cpu_percent !== null">
          <div class="resource-label">
            <i class="pi pi-microchip"></i> CPU Usage
          </div>
          <ProgressBar
            :value="health.system.cpu_percent"
            :class="progressClass(health.system.cpu_percent)"
            style="height: 12px; margin-top: 0.5rem;"
          />
          <div class="resource-value">{{ health.system.cpu_percent }}%</div>
        </div>

        <div class="resource-card" v-if="health.system.memory_percent !== null">
          <div class="resource-label">
            <i class="pi pi-bookmark"></i> Memory Usage
          </div>
          <ProgressBar
            :value="health.system.memory_percent"
            :class="progressClass(health.system.memory_percent)"
            style="height: 12px; margin-top: 0.5rem;"
          />
          <div class="resource-value">
            {{ health.system.memory_used_mb }} MB / {{ health.system.memory_total_mb }} MB
            ({{ health.system.memory_percent }}%)
          </div>
        </div>

        <div class="resource-card" v-if="health.system.disk_percent !== null">
          <div class="resource-label">
            <i class="pi pi-hdd"></i> Disk Usage
          </div>
          <ProgressBar
            :value="health.system.disk_percent"
            :class="progressClass(health.system.disk_percent)"
            style="height: 12px; margin-top: 0.5rem;"
          />
          <div class="resource-value">{{ health.system.disk_percent }}%</div>
        </div>

      </div>
    </div>

    <!-- No psutil info message -->
    <div class="info-card" v-if="health && !hasSystemMetrics">
      <i class="pi pi-info-circle"></i>
      System resource metrics (CPU, memory, disk) are not available because the
      <code>psutil</code> package is not installed. Install it with
      <code>pip install psutil==5.9.8</code> and restart the backend.
    </div>

    <!-- Alert thresholds reference -->
    <div class="thresholds-section" v-if="health">
      <h3>Alert Thresholds</h3>
      <DataTable :value="alertThresholds" class="p-datatable-sm" :striped-rows="true">
        <Column field="metric" header="Metric" />
        <Column field="warning" header="Warning" />
        <Column field="critical" header="Critical" />
        <Column field="severity" header="Severity">
          <template #body="{ data }">
            <Tag :value="data.severity" :severity="data.severity === 'P1-Critical' ? 'danger' : data.severity === 'P2-High' ? 'warning' : 'info'" />
          </template>
        </Column>
      </DataTable>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import api from '../api/api'

const health = ref(null)
const loading = ref(false)
const fetchError = ref(false)
const lastUpdated = ref('')
let refreshTimer = null

const REFRESH_INTERVAL_MS = 30000

async function fetchHealth() {
  loading.value = true
  fetchError.value = false
  try {
    const response = await api.getHealthDetailed()
    health.value = response.data
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (err) {
    fetchError.value = true
    // Keep last known data on error — do not clear dashboard
  } finally {
    loading.value = false
  }
}

const statusClass = computed(() => {
  const s = health.value?.status
  if (s === 'healthy') return 'status-healthy'
  if (s === 'degraded') return 'status-degraded'
  if (s === 'unhealthy') return 'status-unhealthy'
  return 'status-unknown'
})

const statusIcon = computed(() => {
  const s = health.value?.status
  if (s === 'healthy') return 'pi pi-check-circle'
  if (s === 'degraded') return 'pi pi-exclamation-circle'
  if (s === 'unhealthy') return 'pi pi-times-circle'
  return 'pi pi-question-circle'
})

const hasSystemMetrics = computed(() => {
  const sys = health.value?.system
  return sys && (sys.cpu_percent !== null || sys.memory_percent !== null)
})

function componentClass(status) {
  if (status === 'healthy') return 'component-healthy'
  if (status === 'unhealthy') return 'component-unhealthy'
  return ''
}

function tagSeverity(status) {
  if (status === 'healthy') return 'success'
  if (status === 'degraded') return 'warning'
  if (status === 'unhealthy') return 'danger'
  return 'info'
}

function progressClass(value) {
  if (value >= 85) return 'progress-danger'
  if (value >= 70) return 'progress-warning'
  return 'progress-ok'
}

function formatUptime(seconds) {
  if (!seconds && seconds !== 0) return 'N/A'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  if (h > 0) return `${h}h ${m}m`
  if (m > 0) return `${m}m ${s}s`
  return `${s}s`
}

const alertThresholds = [
  { metric: 'API Liveness (/health)', warning: 'Non-200 for 1 min', critical: 'Non-200 for 2 min', severity: 'P1-Critical' },
  { metric: 'Error Rate (5xx)', warning: '> 1% over 5 min', critical: '> 5% over 1 min', severity: 'P1-Critical' },
  { metric: 'DB Connection Pool', warning: '> 80% used', critical: '> 90% used', severity: 'P1-Critical' },
  { metric: 'Memory Usage', warning: '> 70%', critical: '> 85%', severity: 'P2-High' },
  { metric: 'CPU Usage', warning: '> 70% sustained', critical: '> 85% sustained', severity: 'P2-High' },
  { metric: 'Disk Usage', warning: '> 70%', critical: '> 80%', severity: 'P3-Medium' },
  { metric: 'Slow DB Query', warning: '> 10s', critical: '> 30s', severity: 'P2-High' },
]

onMounted(() => {
  fetchHealth()
  refreshTimer = setInterval(fetchHealth, REFRESH_INTERVAL_MS)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})
</script>

<style scoped>
.monitoring-page {
  padding: 1.5rem;
  max-width: 1400px;
}

.monitoring-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.monitoring-header h1 {
  margin: 0 0 0.25rem 0;
  font-size: 1.75rem;
  color: var(--text-color, #1e293b);
}

.welcome-text {
  color: var(--text-color-secondary, #64748b);
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.last-updated {
  font-size: 0.85rem;
  color: var(--text-color-secondary, #64748b);
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #dc2626;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Status banner */
.status-banner {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  color: white;
}

.status-healthy  { background: linear-gradient(135deg, #10b981, #059669); }
.status-degraded { background: linear-gradient(135deg, #f59e0b, #d97706); }
.status-unhealthy { background: linear-gradient(135deg, #ef4444, #dc2626); }
.status-unknown  { background: linear-gradient(135deg, #6b7280, #4b5563); }

.status-label { font-size: 0.8rem; opacity: 0.85; }
.status-value { font-size: 1.4rem; font-weight: 700; }
.status-meta  { margin-left: auto; font-size: 0.85rem; opacity: 0.9; }

/* Metrics grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  background: var(--surface-card, #ffffff);
  border: 1px solid var(--surface-border, #e2e8f0);
  border-radius: 10px;
  padding: 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: box-shadow 0.2s;
}

.metric-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }

.metric-card.component-unhealthy {
  border-color: #fca5a5;
  background: #fef2f2;
}

.metric-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: var(--primary-100, #dbeafe);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon i { font-size: 1.3rem; color: var(--primary-600, #2563eb); }

.metric-label  { font-size: 0.8rem; color: var(--text-color-secondary, #64748b); margin-bottom: 0.35rem; }
.metric-value  { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem; }
.metric-detail { font-size: 0.78rem; color: var(--text-color-secondary, #64748b); }
.component-status { display: flex; align-items: center; }

/* Resources */
.resources-section, .thresholds-section {
  background: var(--surface-card, #ffffff);
  border: 1px solid var(--surface-border, #e2e8f0);
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.resources-section h3, .thresholds-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: var(--text-color, #1e293b);
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.resource-card {
  padding: 0.75rem;
  background: var(--surface-section, #f8fafc);
  border-radius: 8px;
}

.resource-label {
  font-size: 0.85rem;
  color: var(--text-color-secondary, #64748b);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.resource-value {
  font-size: 0.8rem;
  color: var(--text-color-secondary, #64748b);
  margin-top: 0.35rem;
}

.info-card {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #1d4ed8;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.info-card code {
  background: #dbeafe;
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.85rem;
}
</style>
