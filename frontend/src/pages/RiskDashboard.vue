<template>
  <div class="risk-page">

    <!-- Header -->
    <div class="monitoring-header">
      <div class="header-content">
        <h1>
          <i class="pi pi-shield" style="margin-right: 0.5rem;"></i>
          Risk Dashboard
        </h1>
        <p class="welcome-text">Asset risk overview — ICS risk scores based on Purdue model, criticality, and vulnerability</p>
      </div>
      <div class="header-actions">
        <span class="last-updated" v-if="lastUpdated">Last updated: {{ lastUpdated }}</span>
        <Button
          label="Refresh"
          icon="pi pi-refresh"
          :loading="loading"
          @click="fetchAll"
          class="p-button-outlined p-button-sm"
          style="margin-left: 1rem;"
        />
      </div>
    </div>

    <!-- Error banner -->
    <div v-if="fetchError" class="error-banner">
      <i class="pi pi-exclamation-triangle"></i>
      Could not load risk data. Check that the backend is running.
    </div>

    <!-- KPI tiles -->
    <div class="metrics-grid" v-if="overview">

      <div class="metric-card">
        <div class="metric-icon" style="background: #dbeafe;">
          <i class="pi pi-server" style="color: #2563eb;"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">Total Assets</div>
          <div class="metric-value" style="font-size: 2rem; font-weight: 700;">{{ overview.total_assets ?? '—' }}</div>
          <div class="metric-detail">All tracked assets</div>
        </div>
      </div>

      <div class="metric-card component-danger">
        <div class="metric-icon" style="background: #fee2e2;">
          <i class="pi pi-exclamation-triangle" style="color: #dc2626;"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">High Risk</div>
          <div class="metric-value" style="font-size: 2rem; font-weight: 700; color: #dc2626;">{{ overview.high_risk ?? '—' }}</div>
          <div class="metric-detail">Score ≥ 70</div>
        </div>
      </div>

      <div class="metric-card component-warning">
        <div class="metric-icon" style="background: #fef9c3;">
          <i class="pi pi-exclamation-circle" style="color: #d97706;"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">Medium Risk</div>
          <div class="metric-value" style="font-size: 2rem; font-weight: 700; color: #d97706;">{{ overview.medium_risk ?? '—' }}</div>
          <div class="metric-detail">Score 40 – 69</div>
        </div>
      </div>

      <div class="metric-card component-ok">
        <div class="metric-icon" style="background: #dcfce7;">
          <i class="pi pi-check-circle" style="color: #16a34a;"></i>
        </div>
        <div class="metric-content">
          <div class="metric-label">Low Risk</div>
          <div class="metric-value" style="font-size: 2rem; font-weight: 700; color: #16a34a;">{{ overview.low_risk ?? '—' }}</div>
          <div class="metric-detail">Score &lt; 40</div>
        </div>
      </div>

    </div>

    <!-- Loading placeholder for KPIs -->
    <div class="metrics-grid" v-else-if="loading && !fetchError">
      <div class="metric-card" v-for="n in 4" :key="n">
        <div class="metric-icon" style="background: #f1f5f9;"></div>
        <div class="metric-content">
          <div class="metric-label" style="background: #f1f5f9; height: 12px; width: 80px; border-radius: 4px;"></div>
          <div class="metric-value" style="background: #f1f5f9; height: 32px; width: 60px; border-radius: 4px; margin-top: 4px;"></div>
        </div>
      </div>
    </div>

    <!-- Risk Score Distribution -->
    <div class="section-card" v-if="overview">
      <h3><i class="pi pi-chart-bar" style="margin-right: 0.5rem;"></i>Risk Score Distribution</h3>
      <div class="distribution-grid">

        <div class="dist-row">
          <span class="dist-label">High Risk (≥ 70)</span>
          <ProgressBar
            :value="distributionPercent('high')"
            :class="'progress-danger'"
            style="flex: 1; height: 16px; margin: 0 0.75rem;"
          />
          <span class="dist-count danger-text">{{ overview.high_risk ?? 0 }} assets</span>
        </div>

        <div class="dist-row">
          <span class="dist-label">Medium Risk (40–69)</span>
          <ProgressBar
            :value="distributionPercent('medium')"
            :class="'progress-warning'"
            style="flex: 1; height: 16px; margin: 0 0.75rem;"
          />
          <span class="dist-count warning-text">{{ overview.medium_risk ?? 0 }} assets</span>
        </div>

        <div class="dist-row">
          <span class="dist-label">Low Risk (&lt; 40)</span>
          <ProgressBar
            :value="distributionPercent('low')"
            :class="'progress-ok'"
            style="flex: 1; height: 16px; margin: 0 0.75rem;"
          />
          <span class="dist-count ok-text">{{ overview.low_risk ?? 0 }} assets</span>
        </div>

      </div>
    </div>

    <!-- Top Risky Assets table -->
    <div class="section-card" v-if="riskyAssets.length > 0">
      <h3><i class="pi pi-list" style="margin-right: 0.5rem;"></i>Highest-Risk Assets</h3>
      <DataTable
        :value="riskyAssets"
        class="p-datatable-sm"
        :striped-rows="true"
        :rows="10"
        responsiveLayout="scroll"
      >
        <Column field="name" header="Asset Name">
          <template #body="{ data }">
            <router-link :to="`/assets/${data.id}`" class="asset-link">{{ data.name }}</router-link>
          </template>
        </Column>
        <Column field="asset_type_name" header="Type" />
        <Column field="site_name" header="Site" />
        <Column field="purdue_level" header="Purdue Level">
          <template #body="{ data }">
            <Tag
              :value="`Level ${data.purdue_level ?? '?'}`"
              severity="info"
            />
          </template>
        </Column>
        <Column field="risk_score" header="Risk Score" :sortable="true">
          <template #body="{ data }">
            <Tag
              :value="String(data.risk_score ?? 'N/A')"
              :severity="riskSeverity(data.risk_score)"
            />
          </template>
        </Column>
        <Column header="Action">
          <template #body="{ data }">
            <router-link :to="`/assets/${data.id}`">
              <Button icon="pi pi-eye" class="p-button-text p-button-sm" />
            </router-link>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Risk Register Summary -->
    <div class="section-card">
      <h3><i class="pi pi-book" style="margin-right: 0.5rem;"></i>Project Risk Register — Status Summary</h3>
      <p class="section-subtitle">Project-level risks tracked in <code>docs/risk-management.md</code>. Asset-level risks are computed automatically by the risk scoring engine.</p>
      <DataTable :value="riskRegister" class="p-datatable-sm" :striped-rows="true" responsiveLayout="scroll">
        <Column field="id" header="ID" style="width: 60px;" />
        <Column field="title" header="Risk" />
        <Column field="category" header="Category" />
        <Column field="severity" header="Severity">
          <template #body="{ data }">
            <Tag :value="data.severity" :severity="riskSeverity(data.severity)" />
          </template>
        </Column>
        <Column field="owner" header="Owner" />
        <Column field="status" header="Status">
          <template #body="{ data }">
            <Tag
              :value="data.status"
              :severity="data.status === 'mitigated' ? 'success' : data.status === 'closed' ? 'secondary' : 'warning'"
            />
          </template>
        </Column>
        <Column field="mitigation" header="Mitigation" />
      </DataTable>
    </div>

    <!-- Risk Trend note -->
    <div class="info-card">
      <i class="pi pi-info-circle"></i>
      <strong>Risk Trend</strong> — Historical risk score time-series is a planned enhancement.
      Currently the risk score is recalculated each time an asset is updated.
      To see the risk trend for an individual asset, view its change history on the Asset Detail page.
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import api from '../api/api'

const overview = ref(null)
const riskyAssets = ref([])
const loading = ref(false)
const fetchError = ref(false)
const lastUpdated = ref('')

async function fetchAll() {
  loading.value = true
  fetchError.value = false
  try {
    const [overviewRes, assetsRes] = await Promise.all([
      api.getRiskOverview(),
      api.getRiskyAssets(15),
    ])
    overview.value = overviewRes.data
    riskyAssets.value = Array.isArray(assetsRes.data) ? assetsRes.data
      : Array.isArray(assetsRes.data?.items) ? assetsRes.data.items
      : []
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch {
    fetchError.value = true
  } finally {
    loading.value = false
  }
}

function distributionPercent(band) {
  const total = overview.value?.total_assets
  if (!total) return 0
  const count = band === 'high' ? overview.value.high_risk
    : band === 'medium' ? overview.value.medium_risk
    : overview.value.low_risk
  return Math.round(((count ?? 0) / total) * 100)
}

function riskSeverity(value) {
  if (typeof value === 'number') {
    if (value >= 70) return 'danger'
    if (value >= 40) return 'warning'
    return 'success'
  }
  if (typeof value === 'string') {
    if (value.toLowerCase() === 'high') return 'danger'
    if (value.toLowerCase() === 'medium') return 'warning'
    if (value.toLowerCase() === 'low') return 'success'
  }
  return 'info'
}

// Top open risks from the project risk register (docs/risk-management.md)
const riskRegister = [
  { id: 'R-01', title: 'Scope creep from feature requests', category: 'Scope', severity: 'high', owner: 'Obada (PM)', status: 'active', mitigation: 'Change control board; document all additions' },
  { id: 'R-02', title: 'Key team member unavailability', category: 'Resource', severity: 'high', owner: 'Obada (PM)', status: 'active', mitigation: 'Cross-train team; document all features' },
  { id: 'R-03', title: 'CI/CD pipeline failure blocking merges', category: 'Technical', severity: 'high', owner: 'Hamdi (DevOps)', status: 'mitigated', mitigation: 'Local pre-commit checks; rollback plan documented' },
  { id: 'R-04', title: 'Database migration breaking existing data', category: 'Technical', severity: 'high', owner: 'Mohanad (Backend)', status: 'active', mitigation: 'Backup before migration; canary deploy' },
  { id: 'R-05', title: 'Integration gap between frontend and backend', category: 'Technical', severity: 'medium', owner: 'Zekeriya (Frontend)', status: 'mitigated', mitigation: 'Shared Pydantic schemas; API contract testing' },
  { id: 'R-06', title: 'Insufficient test coverage', category: 'Quality', severity: 'medium', owner: 'Praise-God (QA)', status: 'active', mitigation: 'pytest-cov gate at 70 %; peer review required' },
  { id: 'R-07', title: 'Schedule delay from external dependency', category: 'Schedule', severity: 'medium', owner: 'Obada (PM)', status: 'active', mitigation: 'Docker isolates all dependencies; no cloud services required' },
  { id: 'R-08', title: 'Security misconfiguration in production', category: 'Security', severity: 'medium', owner: 'Hamdi (DevOps)', status: 'mitigated', mitigation: 'Production startup validation in config.py; security checklist' },
  { id: 'R-09', title: 'Data loss from database failure', category: 'Infrastructure', severity: 'medium', owner: 'Hamdi (DevOps)', status: 'active', mitigation: 'PostgreSQL ACID; Docker volume; backup script' },
  { id: 'R-10', title: 'Unclear requirements from stakeholders', category: 'Stakeholder', severity: 'low', owner: 'Obada (PM)', status: 'mitigated', mitigation: 'Sprint demos; documented acceptance criteria' },
]

onMounted(fetchAll)
</script>

<style scoped>
.risk-page {
  padding: 1.5rem;
  max-width: 1400px;
}

/* Reuse same header style as TechnicalMonitoring */
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

/* KPI grid — same as monitoring page */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
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

.metric-card.component-danger { border-color: #fca5a5; background: #fff5f5; }
.metric-card.component-warning { border-color: #fcd34d; background: #fffbeb; }
.metric-card.component-ok { border-color: #86efac; background: #f0fdf4; }

.metric-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon i { font-size: 1.3rem; }
.metric-label { font-size: 0.8rem; color: var(--text-color-secondary, #64748b); margin-bottom: 0.2rem; }
.metric-detail { font-size: 0.78rem; color: var(--text-color-secondary, #64748b); margin-top: 0.2rem; }

/* Sections */
.section-card {
  background: var(--surface-card, #ffffff);
  border: 1px solid var(--surface-border, #e2e8f0);
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.section-card h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: var(--text-color, #1e293b);
  display: flex;
  align-items: center;
}

.section-subtitle {
  font-size: 0.85rem;
  color: var(--text-color-secondary, #64748b);
  margin: -0.5rem 0 1rem 0;
}

.section-subtitle code {
  background: #f1f5f9;
  padding: 0.1rem 0.3rem;
  border-radius: 4px;
  font-family: monospace;
}

/* Distribution */
.distribution-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.dist-row {
  display: flex;
  align-items: center;
}

.dist-label {
  width: 200px;
  flex-shrink: 0;
  font-size: 0.88rem;
  color: var(--text-color, #1e293b);
}

.dist-count {
  width: 90px;
  text-align: right;
  font-size: 0.85rem;
  font-weight: 600;
}

.danger-text  { color: #dc2626; }
.warning-text { color: #d97706; }
.ok-text      { color: #16a34a; }

/* Asset link */
.asset-link {
  color: var(--primary-600, #2563eb);
  text-decoration: none;
  font-weight: 500;
}
.asset-link:hover { text-decoration: underline; }

/* Info card */
.info-card {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #1d4ed8;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
}
</style>
