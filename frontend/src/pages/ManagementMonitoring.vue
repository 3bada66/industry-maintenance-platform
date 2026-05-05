<template>
  <div class="mgmt-page">

    <!-- Header -->
    <div class="mgmt-header">
      <div class="header-content">
        <h1><i class="pi pi-chart-line" style="margin-right:0.5rem;"></i>Management Monitoring</h1>
        <p class="sub-text">Project progress, team workload, milestones, cost, and risk summary</p>
      </div>
      <div class="header-actions">
        <span class="last-updated" v-if="lastUpdated">Last updated: {{ lastUpdated }}</span>
        <Button label="Refresh" icon="pi pi-refresh" :loading="loading" @click="fetchStatus"
          class="p-button-outlined p-button-sm" style="margin-left:1rem;" />
      </div>
    </div>

    <!-- Error -->
    <div v-if="fetchError" class="error-banner">
      <i class="pi pi-exclamation-triangle"></i>
      Could not load management data. Check that the backend is running.
    </div>

    <div v-if="data">

      <!-- ── Row 1: KPI tiles ───────────────────────────────────── -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-icon"><i class="pi pi-check-circle"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">{{ data.tasks.completed }} / {{ data.tasks.total }}</div>
            <div class="kpi-label">Tasks Completed</div>
            <ProgressBar :value="data.tasks.progress_percent" style="height:8px;margin-top:0.4rem;" />
            <div class="kpi-sub">{{ data.tasks.progress_percent }}% done</div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon"><i class="pi pi-clock"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">{{ data.tasks.actual_hours }} h</div>
            <div class="kpi-label">Hours Logged</div>
            <div class="kpi-sub">Est. {{ data.tasks.estimated_hours }} h</div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon"><i class="pi pi-euro"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">€{{ data.cost.actual_eur }}</div>
            <div class="kpi-label">Actual Cost</div>
            <div class="kpi-sub">{{ data.cost.note }}</div>
          </div>
        </div>

        <div class="kpi-card" :class="spiClass">
          <div class="kpi-icon"><i class="pi pi-arrows-h"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">{{ data.schedule.spi }}</div>
            <div class="kpi-label">SPI (Schedule)</div>
            <div class="kpi-sub">
              <Tag :value="data.schedule.status.replace('_',' ').toUpperCase()"
                :severity="spiSeverity" />
            </div>
          </div>
        </div>

        <div class="kpi-card">
          <div class="kpi-icon"><i class="pi pi-server"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">{{ data.project.assets_managed }}</div>
            <div class="kpi-label">Assets Managed (live)</div>
            <div class="kpi-sub">In current tenant database</div>
          </div>
        </div>

        <div class="kpi-card risk-kpi">
          <div class="kpi-icon"><i class="pi pi-exclamation-circle"></i></div>
          <div class="kpi-body">
            <div class="kpi-value">{{ data.risks.by_status.active }}</div>
            <div class="kpi-label">Open Risks</div>
            <div class="kpi-sub">
              <Tag value="HIGH" severity="danger" style="margin-right:0.3rem;" />{{ data.risks.by_severity.high }}
              &nbsp;
              <Tag value="MED" severity="warning" style="margin-right:0.3rem;" />{{ data.risks.by_severity.medium }}
            </div>
          </div>
        </div>
      </div>

      <!-- ── Row 2: Sprint velocity + Schedule ─────────────────── -->
      <div class="two-col">

        <div class="panel">
          <h3><i class="pi pi-chart-bar"></i> Sprint Velocity</h3>
          <div class="velocity-bars">
            <div v-for="(sp, i) in data.schedule.sprint_velocities" :key="i" class="velocity-row">
              <div class="vel-label">Sprint {{ i + 1 }}</div>
              <div class="vel-bar-wrap">
                <div class="vel-bar" :style="{ width: velWidth(sp) }"></div>
              </div>
              <div class="vel-sp">{{ sp }} SP</div>
            </div>
          </div>
          <div class="schedule-meta">
            <span>Planned: <strong>{{ data.schedule.planned_value_sp }} SP</strong></span>
            <span>Earned: <strong>{{ data.schedule.earned_value_sp }} SP</strong></span>
            <span>Variance: <strong :class="data.schedule.variance_sp < 0 ? 'neg' : 'pos'">
              {{ data.schedule.variance_sp }} SP
            </strong></span>
          </div>
        </div>

        <div class="panel">
          <h3><i class="pi pi-flag"></i> Milestone Timeline</h3>
          <DataTable :value="data.milestones" size="small" class="milestone-table">
            <Column field="id" header="ID" style="width:4rem;" />
            <Column field="name" header="Milestone" />
            <Column header="Week" style="width:5rem;">
              <template #body="{ data: row }">W{{ row.due_week }}</template>
            </Column>
            <Column header="Status" style="width:8rem;">
              <template #body="{ data: row }">
                <Tag :value="row.status.replace('_',' ')" :severity="milestoneSeverity(row.status)" />
              </template>
            </Column>
          </DataTable>
        </div>

      </div>

      <!-- ── Row 3: Team workload ───────────────────────────────── -->
      <div class="panel full-width">
        <h3><i class="pi pi-users"></i> Team Workload Distribution</h3>
        <DataTable :value="data.team_workload" size="small">
          <Column field="name" header="Name" />
          <Column field="student_id" header="Student ID" style="width:9rem;" />
          <Column field="role" header="Role" />
          <Column field="assigned_sp" header="Assigned SP" style="width:8rem;" />
          <Column field="completed_sp" header="Completed SP" style="width:9rem;" />
          <Column header="Load" style="width:12rem;">
            <template #body="{ data: row }">
              <ProgressBar :value="row.load_percent"
                :class="row.load_percent > 95 ? 'bar-warn' : 'bar-ok'"
                style="height:10px;" />
              <span style="font-size:0.8rem;">{{ row.load_percent }}%</span>
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- ── Row 4: Cost + Risk ─────────────────────────────────── -->
      <div class="two-col">

        <div class="panel">
          <h3><i class="pi pi-wallet"></i> Cost Tracking</h3>
          <table class="simple-table">
            <tr><td>Estimated cost</td><td><strong>€{{ data.cost.estimated_eur }}</strong></td></tr>
            <tr><td>Actual cost</td><td><strong>€{{ data.cost.actual_eur }}</strong></td></tr>
            <tr><td>Variance</td><td><strong>€{{ data.cost.variance_eur }}</strong></td></tr>
            <tr><td>CPI</td><td><strong>{{ data.cost.cpi }}</strong></td></tr>
          </table>
          <p class="cost-note">{{ data.cost.note }}</p>
        </div>

        <div class="panel">
          <h3><i class="pi pi-shield"></i> Risk Summary</h3>
          <div class="risk-counts">
            <div class="risk-badge danger"><span>{{ data.risks.by_severity.high }}</span>High</div>
            <div class="risk-badge warning"><span>{{ data.risks.by_severity.medium }}</span>Medium</div>
            <div class="risk-badge success"><span>{{ data.risks.by_severity.low }}</span>Low</div>
          </div>
          <p style="margin:0.75rem 0 0.4rem; font-size:0.85rem; font-weight:600;">Top open risks:</p>
          <ul class="risk-list">
            <li v-for="r in data.risks.top_open" :key="r.id">
              <Tag :value="r.id" severity="danger" style="margin-right:0.4rem;font-size:0.75rem;" />
              {{ r.name }}
              <span class="risk-score">Score {{ r.score }}</span>
            </li>
          </ul>
        </div>

      </div>

    </div><!-- /data -->

    <!-- Loading skeleton -->
    <div v-else-if="loading" class="loading-state">
      <i class="pi pi-spin pi-spinner" style="font-size:2rem;"></i>
      <p>Loading management data…</p>
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

const data = ref(null)
const loading = ref(false)
const fetchError = ref(false)
const lastUpdated = ref('')
let refreshTimer = null
const REFRESH_INTERVAL_MS = 60000  // 1 minute — management data changes slowly

async function fetchStatus() {
  loading.value = true
  fetchError.value = false
  try {
    const res = await api.getManagementStatus()
    data.value = res.data
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch {
    fetchError.value = true
  } finally {
    loading.value = false
  }
}

const maxVelocity = computed(() =>
  data.value ? Math.max(...data.value.schedule.sprint_velocities) : 1
)

function velWidth(sp) {
  return `${Math.round((sp / maxVelocity.value) * 100)}%`
}

const spiClass = computed(() => {
  const spi = data.value?.schedule?.spi ?? 1
  if (spi >= 0.95) return 'kpi-card kpi-good'
  if (spi >= 0.85) return 'kpi-card kpi-warn'
  return 'kpi-card kpi-bad'
})

const spiSeverity = computed(() => {
  const spi = data.value?.schedule?.spi ?? 1
  if (spi >= 0.95) return 'success'
  if (spi >= 0.85) return 'warning'
  return 'danger'
})

function milestoneSeverity(status) {
  if (status === 'completed') return 'success'
  if (status === 'in_progress') return 'warning'
  if (status === 'delayed') return 'danger'
  return 'secondary'
}

onMounted(() => {
  fetchStatus()
  refreshTimer = setInterval(fetchStatus, REFRESH_INTERVAL_MS)
})
onUnmounted(() => { if (refreshTimer) clearInterval(refreshTimer) })
</script>

<style scoped>
.mgmt-page { padding: 0; }

.mgmt-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}
.mgmt-header h1 { margin: 0; font-size: 1.6rem; }
.sub-text { margin: 0.25rem 0 0; color: #6c757d; font-size: 0.9rem; }
.header-actions { display: flex; align-items: center; flex-shrink: 0; }
.last-updated { font-size: 0.8rem; color: #6c757d; }

.error-banner {
  background: #fee2e2; border: 1px solid #fca5a5; border-radius: 6px;
  padding: 0.75rem 1rem; margin-bottom: 1rem; color: #991b1b;
}

/* KPI tiles */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.kpi-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.1rem;
  display: flex;
  gap: 0.9rem;
  align-items: flex-start;
}
.kpi-card.kpi-good { border-color: #86efac; background: #f0fdf4; }
.kpi-card.kpi-warn { border-color: #fcd34d; background: #fffbeb; }
.kpi-card.kpi-bad  { border-color: #fca5a5; background: #fef2f2; }
.kpi-icon { font-size: 1.5rem; color: #6366f1; margin-top: 0.1rem; }
.kpi-value { font-size: 1.5rem; font-weight: 700; line-height: 1.1; }
.kpi-label { font-size: 0.78rem; color: #6c757d; margin: 0.15rem 0; }
.kpi-sub { font-size: 0.75rem; color: #9ca3af; margin-top: 0.2rem; }

/* Two-column layout */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}
@media (max-width: 900px) { .two-col { grid-template-columns: 1fr; } }

.panel {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.2rem;
  margin-bottom: 1rem;
}
.panel.full-width { grid-column: 1 / -1; }
.panel h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Velocity bars */
.velocity-bars { display: flex; flex-direction: column; gap: 0.55rem; }
.velocity-row { display: flex; align-items: center; gap: 0.75rem; }
.vel-label { width: 60px; font-size: 0.82rem; color: #6c757d; flex-shrink: 0; }
.vel-bar-wrap { flex: 1; background: #f3f4f6; border-radius: 4px; height: 14px; }
.vel-bar { height: 14px; background: #6366f1; border-radius: 4px; transition: width 0.4s; }
.vel-sp { width: 42px; font-size: 0.82rem; font-weight: 600; text-align: right; }
.schedule-meta {
  display: flex; gap: 1.5rem; margin-top: 1rem;
  padding-top: 0.75rem; border-top: 1px solid #e5e7eb;
  font-size: 0.85rem; color: #6c757d;
}
.neg { color: #ef4444; }
.pos { color: #22c55e; }

/* Milestone table */
.milestone-table { font-size: 0.85rem; }

/* Cost */
.simple-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.simple-table tr td { padding: 0.4rem 0; border-bottom: 1px solid #f3f4f6; }
.simple-table tr td:first-child { color: #6c757d; }
.simple-table tr td:last-child { text-align: right; }
.cost-note { font-size: 0.78rem; color: #6c757d; margin-top: 0.75rem; }

/* Risk */
.risk-counts { display: flex; gap: 0.75rem; margin-bottom: 0.5rem; }
.risk-badge {
  display: flex; flex-direction: column; align-items: center;
  padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.78rem; font-weight: 600;
}
.risk-badge span { font-size: 1.4rem; font-weight: 700; }
.risk-badge.danger  { background: #fee2e2; color: #991b1b; }
.risk-badge.warning { background: #fef9c3; color: #92400e; }
.risk-badge.success { background: #dcfce7; color: #166534; }
.risk-list { list-style: none; padding: 0; margin: 0; font-size: 0.85rem; }
.risk-list li { padding: 0.3rem 0; border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; }
.risk-score { margin-left: auto; font-size: 0.75rem; color: #9ca3af; }

/* Loading */
.loading-state { text-align: center; padding: 4rem; color: #6c757d; }

/* Progress bar colour variants */
:deep(.bar-warn .p-progressbar-value) { background: #f59e0b !important; }
:deep(.bar-ok .p-progressbar-value)   { background: #22c55e !important; }
</style>
