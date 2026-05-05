# UI and Dashboard Design
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 2.0
**Owner:** Fares Stouhi (UX/UI Designer, 2309115179)
**Supporting:** Zekeriya Dulli (Frontend Developer, 2309115377) · Obada Abdulhakim Kharaz (Project Manager, 2309115277)

---

## 1. Design Principles

All dashboards follow five principles:

1. **Information density without clutter** — most actionable data first; details reachable in one click
2. **Status at a glance** — green/amber/red colour coding communicates state within 2 seconds of page load
3. **Industrial context** — terminology and icons reflect OT/ICS environments, not generic IT dashboards
4. **Consistency** — all dashboards use the same PrimeVue component library, CSS variables, and card patterns
5. **Non-breaking** — all dashboard pages are additions to the existing route structure, never replacements

### 1.1 Shared Colour Palette

| Purpose | Colour | Usage |
|---------|--------|-------|
| Primary action | `#3B82F6` (blue) | Buttons, links, selected state |
| Healthy / Low risk | `#10B981` (green) | Healthy status, low risk score |
| Warning / Medium risk | `#F59E0B` (amber) | Degraded status, medium risk score |
| Danger / High risk | `#EF4444` (red) | Unhealthy status, high risk score |
| Unknown / Inactive | `#6B7280` (gray) | Unknown state, closed risks |
| Card background | `var(--surface-card)` | All metric cards |
| Page background | `var(--surface-ground)` | Page canvas |

### 1.2 Shared Component Patterns

All three dashboards share:

- **Header row:** page title + icon on left; "Last updated" timestamp + Refresh button on right
- **Error banner:** red-bordered strip shown when the API call fails; keeps last known data visible
- **Metric cards:** rounded card with a coloured icon square, large number, and small label
- **Section cards:** white card with a `<h3>` heading, containing a `<DataTable>` or progress bar grid
- **PrimeVue components used:** `<Button>`, `<Tag>`, `<ProgressBar>`, `<DataTable>`, `<Column>`

---

## 2. Management Dashboard

**Route:** `/management`
**Vue component:** `frontend/src/pages/ManagementMonitoring.vue`
**Status:** Implemented
**Users:** Project Manager, Course Instructor/Examiner
**Refresh:** 60-second auto-refresh via `setInterval`; manual Refresh button
**Authentication required:** Yes (JWT cookie)
**Data source:** `GET /api/v1/management/status`

### 2.1 Purpose

The Management Dashboard answers the question: **"Is the project on track and is the team healthy?"** It translates sprint data, team workload, milestones, and earned value into a single-page view that the PM can read in under 30 seconds before a stand-up.

### 2.2 Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Management Monitoring     [Last updated: 14:32]  [Refresh]      │
│  Project KPIs — auto-refreshes every 60 seconds                  │
├─────────────┬──────────────┬──────────────┬──────────────────────┤
│ Sprint       │ SPI           │ Tasks Done    │ Assets Managed      │
│ 4 / 4       │ 0.96          │ 87.5 %        │ 8 (live)            │
├─────────────┴──────────────┴──────────────┴──────────────────────┤
│ Sprint Velocity (story points completed per sprint)               │
│  [Sprint 1: ████ 45]  [Sprint 2: ████████ 52]                    │
│  [Sprint 3: ████████ 54]  [Sprint 4: ██████ 48]                  │
├──────────────────────────────────────────────────────────────────┤
│ Milestones                                                        │
│  ID | Name                    | Due Week | Status   | Deliverables│
│  M1 | Project Kickoff         | W1       | ✅ done  | ...         │
│  M7 | Final Submission        | W16      | 🔄 prog  | ...         │
├──────────────────────────────────────────────────────────────────┤
│ Team Workload                                                     │
│  Member       | Role       | Assigned SP | Completed | Load %    │
│  Obada        | PM         | 12          | 12        | ████ 80%  │
│  Mohanad      | Backend    | 16          | 14        | ████ 95%  │
├──────────────────────────────────────────────────────────────────┤
│ Cost / Effort            │ Risk Summary                          │
│  Estimated: 302 h        │  Total: 14 risks                     │
│  Actual:    289 h        │  High: 4  Medium: 6  Low: 4          │
│  CPI: 1.04               │  Active: 7  Mitigated: 3  Closed: 4  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Panels

| Panel | Content | Data Shown |
|-------|---------|------------|
| **Project Progress** | 4 KPI tiles in a row | Sprint number, SPI, task completion %, live asset count |
| **Sprint Velocity** | Horizontal bar per sprint | Story points completed per sprint (4 sprints) |
| **Milestone Status** | `<DataTable>` — one row per milestone | ID, name, due week, status tag (completed/in_progress/at_risk), deliverables list |
| **Task Completion** | Shown in KPI tile + cost section | Tasks completed / total; overdue count |
| **Overdue Tasks** | Highlighted in cost section | `tasks.overdue` count — red badge if > 0 |
| **Cost Variance** | Cost table | Estimated hours, actual hours, variance, CPI |
| **Schedule Variance** | SPI KPI tile + velocity bars | SPI value; story-point variance from plan |
| **Team Workload** | `<DataTable>` with `<ProgressBar>` | Assigned SP, completed SP, load % per member — bar turns red at > 95 % |
| **Risk Summary** | Two-column summary section | Total/severity counts; top 4 open risks with owner and status |

### 2.4 How Users Interact

```
User opens /management
  │
  ▼
60-second auto-refresh starts; initial data loads
  │
  ├──► SPI tile shows < 0.85 (red)
  │         → PM opens /management, confirms delay
  │         → Adjusts sprint scope before stand-up
  │
  ├──► Team member load > 95 % (red progress bar)
  │         → PM reassigns tasks from Workload table
  │
  ├──► Milestone status shows "at_risk"
  │         → PM clicks to see deliverables; follows up with owner
  │
  └──► Manual Refresh button
            → Fetches latest status mid-meeting
```

### 2.5 Components Used

| Panel | PrimeVue / HTML Component | Notes |
|-------|--------------------------|-------|
| KPI tiles | `<div class="metric-card">` | Same card pattern as Technical Monitoring |
| Sprint velocity | Custom `<div>` bar chart | No Chart.js dependency — pure CSS bars |
| Milestones | `<DataTable>` + `<Column>` + `<Tag>` | Status tag coloured by value |
| Team workload | `<DataTable>` + `<ProgressBar>` | Bar colour changes at 80 % and 95 % thresholds |
| Cost/effort | HTML `<table>` | Simple two-column layout |
| Risk summary | `<div>` badge grid + risk list | Severity counts as coloured badges |

---

## 3. Technical Monitoring Dashboard

**Route:** `/monitoring`
**Vue component:** `frontend/src/pages/TechnicalMonitoring.vue`
**Status:** Implemented
**Users:** DevOps Engineer, IT/OT Administrator, Backend Developer
**Refresh:** 30-second auto-refresh; manual Refresh button
**Authentication required:** Yes (route guard) — but the underlying API endpoint requires no auth
**Data source:** `GET /health/detailed`

### 3.1 Purpose

The Technical Monitoring Dashboard answers: **"Is the system healthy and responsive right now?"** It exposes the 10 defined monitoring metrics in a single colour-coded view. A system operator can confirm system health in under 10 seconds without SSH access.

### 3.2 Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Technical Monitoring      [Last updated: 14:33]  [Refresh Now]  │
│  Real-time system health — auto-refreshes every 30 seconds       │
├──────────────────────────────────────────────────────────────────┤
│ ██████████████  HEALTHY  v1.0.0  Uptime 24h 3m  Env: production  │
│ (status banner — full-width, coloured by overall status)         │
├──────────────┬─────────────────────┬────────────────────────────┤
│ Database     │ Cache Layer          │ API Server (FastAPI)        │
│ 🟢 connected │ 🟢 available         │ 🟢 running                  │
│ 2 ms         │ Type: memory         │ Python 3.11.6               │
│ Pool: 1/5    │                      │                             │
├──────────────┴─────────────────────┴────────────────────────────┤
│ System Resources                                                  │
│  CPU Usage     [████░░░░░░░░░░] 12 %                             │
│  Memory Usage  [████████░░░░░░] 48 %  1964 MB / 8192 MB          │
│  Disk Usage    [█████░░░░░░░░░] 34 %                             │
├──────────────────────────────────────────────────────────────────┤
│ Alert Thresholds Reference                                        │
│  Metric               | Warning        | Critical    | Severity  │
│  API Liveness (/health)| Non-200 1 min  | Non-200 2 min| P1       │
│  Error Rate (5xx)      | > 1% / 5 min   | > 5% / 1 min | P1       │
│  DB Connection Pool    | > 80% used     | > 90% used   | P1       │
│  Memory Usage          | > 70%          | > 85%        | P2       │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 Panels

| Panel | Content | Data Shown |
|-------|---------|------------|
| **System Health** | Full-width status banner | Overall status (healthy/degraded/unhealthy), version, uptime, environment |
| **API Response Time** | Database card — response_time_ms | `components.database.response_time_ms` in milliseconds |
| **Error Rate** | Alert Thresholds table | Reference thresholds for 5xx rate; live error rate requires log parsing (not live in dashboard) |
| **Uptime** | Status banner | `uptime_seconds` formatted as Xh Ym |
| **Database Status** | Database component card | Connection status, response time, pool usage |
| **Failed Requests** | Alert threshold row for DB pool | Pool exhaustion is the leading indicator for failed requests |
| **Last Deployment** | Status banner environment field | Environment name; Alembic migration status in `/health/detailed` `version` field |
| **Recent Logs / Alerts** | Alert Thresholds table | Reference table; actual log parsing is a planned enhancement |

### 3.4 Health Status Logic

```
GET /health/detailed response
  │
  ├─► status == "healthy"   → green banner + pi-check-circle
  ├─► status == "degraded"  → amber banner + pi-exclamation-circle
  ├─► status == "unhealthy" → red banner + pi-times-circle
  └─► fetch error / timeout → error banner shown; last data preserved
```

The status banner changes its full background colour so the health state is visible from across a room without reading text.

### 3.5 Auto-Refresh Behaviour

- `setInterval(fetchHealth, 30000)` starts in `onMounted()`
- Cleared with `clearInterval` in `onUnmounted()` — no memory leak on navigation
- On fetch error: error banner is shown but the last known data remains visible
- Loading spinner shown on the Refresh button during any active fetch

### 3.6 How Users Interact

```
User opens /monitoring
  │
  ├──► Banner is red (unhealthy)
  │         → User reads DB card → pool exhausted
  │         → Checks error.log, restarts connections
  │
  ├──► Memory bar is amber (> 70 %)
  │         → User reviews running processes
  │         → Considers increasing container memory limit
  │
  ├──► psutil not installed
  │         → Blue info card explains missing metrics
  │         → User runs: pip install psutil==5.9.8
  │
  └──► User navigates away → timer cleared automatically
```

### 3.7 Components Used

| Panel | PrimeVue / HTML | Notes |
|-------|-----------------|-------|
| Status banner | `<div class="status-banner">` | CSS class changes by status value |
| Component cards | `<div class="metric-card">` | Shared card style; border turns red if unhealthy |
| Status tags | `<Tag :severity="...">` | success/warning/danger mapped from status string |
| Resource bars | `<ProgressBar>` | CSS class changes at 70 % (warning) and 85 % (danger) |
| Alert thresholds | `<DataTable>` | Static data; renders as reference table |

---

## 4. Risk Dashboard

**Route:** `/risk`
**Vue component:** `frontend/src/pages/RiskDashboard.vue`
**Status:** Implemented
**Users:** Risk Manager, Safety Manager, Maintenance Supervisor, IT/OT Security Officer
**Refresh:** On page load + manual Refresh button
**Authentication required:** Yes (JWT cookie)
**Data sources:**
- `GET /assets/risk-overview` — aggregated risk counts (total, high, medium, low)
- `GET /dashboard/risky-assets?limit=15` — top risky assets list

### 4.1 Purpose

The Risk Dashboard answers: **"Which assets are at highest risk right now, who is responsible, and what is the current mitigation status?"** It surfaces asset-level risk (computed automatically by `risk_scoring.py`) alongside project-level risk (from the risk register in `docs/risk-management.md`).

### 4.2 Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Risk Dashboard            [Last updated: 14:34]  [Refresh]      │
│  Asset risk overview — ICS risk scores based on Purdue model...  │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│ Total Assets │ High Risk     │ Medium Risk   │ Low Risk           │
│ 8            │ 3  🔴         │ 4  🟡         │ 1  🟢              │
│ All tracked  │ Score ≥ 70    │ Score 40–69   │ Score < 40         │
├──────────────┴──────────────┴──────────────┴────────────────────┤
│ Risk Score Distribution                                           │
│  High Risk (≥ 70)   [███████░░░░░░░░░░░░░░] 37 %   3 assets     │
│  Medium Risk (40–69)[█████████░░░░░░░░░░░░] 50 %   4 assets     │
│  Low Risk (< 40)    [█░░░░░░░░░░░░░░░░░░░░] 13 %   1 asset      │
├──────────────────────────────────────────────────────────────────┤
│ Highest-Risk Assets                                               │
│  Asset Name | Type    | Site       | Purdue | Score  | Action   │
│  PLC-01     | PLC     | Main Plant | L1     | 🔴 82  | 👁 View  │
│  HMI-Control| HMI     | Main Plant | L2     | 🔴 74  | 👁 View  │
│  RTU-Sensor | RTU     | R&D Center | L1     | 🟡 58  | 👁 View  │
├──────────────────────────────────────────────────────────────────┤
│ Project Risk Register — Status Summary                            │
│  ID  | Risk Title                   | Sev    | Owner  | Status  │
│  R-01| Scope creep                  | 🔴 high| PM     | active  │
│  R-03| CI/CD pipeline failure       | 🔴 high| DevOps | ✅ mitig│
│  R-06| Insufficient test coverage   | 🟡 med | QA     | active  │
├──────────────────────────────────────────────────────────────────┤
│ ℹ Risk Trend — planned enhancement. Current score recalculated   │
│   on asset update. See Asset Detail page for change history.     │
└──────────────────────────────────────────────────────────────────┘
```

### 4.3 Panels

| Panel | Content | Data Shown |
|-------|---------|------------|
| **High-Priority Risks** | KPI tile — red | Count of assets with risk score ≥ 70 |
| **Risk Status** | Distribution section with progress bars | % of assets in each band (high/medium/low), absolute counts |
| **Risk Owners** | Project Risk Register table — Owner column | Risk owner per project risk (PM, DevOps, QA, etc.); asset owner linkable via Asset Detail |
| **Mitigation Progress** | Project Risk Register table — Status column | Status tags: `active` (amber), `mitigated` (green), `closed` (grey) |
| **Risk Trend** | Info card | Planned enhancement; redirects user to Asset Detail → change history for per-asset trend |

### 4.4 Risk Scoring Model

The `risk_scoring.py` service computes a score (0–100) for every asset from five inputs:

| Input | Weight | Source |
|-------|--------|--------|
| Purdue Level | High | Level 0–1 (field/control) = highest risk |
| Business criticality | High | 1–10 scale set on asset record |
| Physical access ease | Medium | Attribute on asset record |
| Remote access type | Medium | `asset_interfaces` — remote protocol present? |
| Known vulnerability score | Medium | CVE/patch status field on asset |

The score updates automatically when any input attribute changes. No manual consultant input is required.

### 4.5 How Users Interact

```
User opens /risk
  │
  ├──► High Risk KPI tile shows > 0 (red)
  │         → Scrolls to "Highest-Risk Assets" table
  │         → Clicks View on the top asset
  │         → Asset Detail page shows risk score breakdown and change history
  │
  ├──► Risk Register shows R-04 (DB migration) as "active"
  │         → Risk Manager contacts DevOps owner (Hamdi)
  │         → Verifies mitigation step is in progress
  │
  ├──► Distribution bars show > 50 % high-risk
  │         → Security Officer prioritises remediation plan
  │         → Requests maintenance schedule for Level 0/1 assets
  │
  └──► Refresh button
            → Fetches latest risk overview after risk scores are recalculated
```

### 4.6 Components Used

| Panel | PrimeVue / HTML | Notes |
|-------|-----------------|-------|
| KPI tiles | `<div class="metric-card">` | Border colour matches risk band |
| Distribution | `<ProgressBar>` × 3 | CSS class `progress-danger/warning/ok` per band |
| Top assets table | `<DataTable>` + `<Column>` + `<Tag>` | Risk score as Tag severity; asset name is a `<router-link>` to detail page |
| Risk register | `<DataTable>` + `<Tag>` | Status tag: success for mitigated, warning for active |
| Risk trend note | `<div class="info-card">` | Blue info box; honest about what is planned |

---

## 5. Navigation

All three dashboards are accessible from the Monitoring section of the sidebar:

```
Monitoring
  ├── Technical Monitoring    → /monitoring   (pi-heart-fill)
  ├── Management Monitoring   → /management   (pi-chart-line)
  └── Risk Dashboard          → /risk         (pi-shield)
```

Translation keys defined in `frontend/src/locales/en/menu.json` and `it/menu.json`:

| Key | English | Italian |
|-----|---------|---------|
| `menu.navigation.monitoring` | Technical Monitoring | Monitoraggio Tecnico |
| `menu.navigation.managementMonitoring` | Management Monitoring | Monitoraggio Gestionale |
| `menu.navigation.riskDashboard` | Risk Dashboard | Dashboard Rischi |
| `menu.section.monitoring` | Monitoring | Monitoraggio |

---

## 6. Visual Hierarchy and Typography

### 6.1 Type Scale

| Element | Size | Weight | Purpose |
|---------|------|--------|---------|
| Dashboard title (`h1`) | 1.75 rem | Bold | Page identification |
| Section heading (`h3`) | 1 rem | SemiBold | Panel identification |
| KPI number | 2 rem | Bold | Immediate attention |
| KPI label | 0.8 rem | Regular | KPI description |
| Table headers | 0.875 rem | SemiBold | Column identification |
| Table data | 0.875 rem | Regular | Data readability |
| Timestamps / detail | 0.78–0.85 rem | Regular | Secondary information |

### 6.2 Grid

All dashboards use CSS Grid with `repeat(auto-fill, minmax(240px, 1fr))` for the KPI row. Section cards are full-width. This produces:

- **Desktop (≥ 1280 px):** 4 KPI tiles per row
- **Tablet (768–1279 px):** 2–3 KPI tiles per row
- **Mobile (< 768 px):** 1 tile per row; tables scroll horizontally

---

## 7. Responsiveness

| Breakpoint | KPI Row | Charts / Tables |
|------------|---------|-----------------|
| Desktop ≥ 1280 px | 4 columns | Full width, horizontal layout |
| Tablet 768–1279 px | 2–3 columns | Scrollable tables, stacked progress bars |
| Mobile < 768 px | 1 column | Simplified: status banner + top table only |

All `<DataTable>` components include `responsiveLayout="scroll"` so wide tables become horizontally scrollable on narrow screens.

---

## 8. Accessibility

- Status colours always paired with text labels or icons — colour alone never carries meaning
- `<Tag>` components include their value as visible text alongside colour
- All `<router-link>` elements are keyboard-navigable
- `<Button>` elements have `label` or `aria-label` attributes
- Minimum contrast ratio: 4.5:1 (WCAG AA) for all text/background combinations using the palette above

---

## 9. Planned Enhancements

| Enhancement | Dashboard | Priority |
|-------------|-----------|---------|
| Risk score time-series chart | Risk | High |
| Live error rate from log file parsing | Technical | Medium |
| Sentry / Rollbar integration for error aggregation | Technical | Medium |
| Chart.js doughnut for risk distribution | Risk | Low |
| Export risk register to PDF/Excel | Risk | Low |
| Mobile-optimised single-metric view | All | Low |
| SPI trend chart across all sprints | Management | Low |
