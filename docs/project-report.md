# Project Report
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Submission:** Week 16
**Branch:** `course-adaptation-monitoring`
**Repository:** `SPM_git_vs` (adapted from Industry Maintenance Platform v1.1.0)

---

## Cover Page

### Project Title

**Industry Maintenance Platform: Industrial Asset, Risk, Management and Technical Monitoring Platform**
An adaptation of the open-source Industry Maintenance Platform v1.1.0 system as a fully documented, monitored, and course-aligned industrial monitoring platform.

### Team

| Student Name | Student ID | Role | Exact Responsibilities |
|-------------|------------|------|----------------------|
| Obada Abdulhakim Kharaz | 2309115277 | Project Manager | Defines and enforces project scope; maintains the sprint plan and 7-milestone schedule; runs weekly stand-ups and sprint reviews; owns the project management plan, team work plan, value creation document, and stakeholder communication plan; validates that every course deliverable is mapped to a working feature or document before final submission |
| Mohanad Aref Ali Sultan | 2309115898 | Backend Developer | Implements and documents the `GET /health` and `GET /health/detailed` endpoints; writes the management monitoring router (`routers/management_monitoring.py`); maintains the FastAPI application factory (`main.py`); owns the backend test suite (`backend/tests/`); documents the API structure, database schema, and backend contribution to technical monitoring |
| Zekeriya Dulli | 2309115377 | Frontend Developer | Implements `TechnicalMonitoring.vue` and `ManagementMonitoring.vue` dashboard pages; creates `RiskDashboard.vue`; adds all three routes to `router.js`; adds monitoring nav items to `SidebarMenu.vue`; maintains the Vue Router, Axios API client (`api.js`), and i18n translation keys |
| Praise-God Tobby | 2309116418 | QA/Test Engineer | Owns the continuous testing strategy; writes and maintains `backend/tests/test_health.py` (15 assertions) and the frontend unit test `useStatus.spec.js` (29 assertions); configures Vitest in `vite.config.js`; runs the smoke test sequence after every deployment; documents the testing pyramid, regression checklist, and missing-tests roadmap |
| Fares Stouhi | 2309115179 | UX/UI Designer | Designs the layout, colour coding, and interaction flows for all three monitoring dashboards; produces wireframe layouts with panel-by-panel descriptions; documents the visual hierarchy, typography scale, colour palette, responsive breakpoints, and accessibility requirements in `docs/ui-dashboard-design.md` |
| Hamdi Alnaqeeb | 2309116178 | DevOps/Operations Engineer | Maintains `.github/workflows/backend.yml` and `frontend.yml`; owns the Docker Compose deployment configuration; writes the deployment runbook and rollback procedure; documents the local CD pipeline, no-paid-services guarantee, and CI quality gate definitions in `docs/ci-cd-testing.md` |
| Abdulaziz Alyahya | 2309116441 | Risk Manager | Identifies and scores 14 project risks across 9 categories; maintains the risk register in `docs/risk-management.md`; writes the management-under-uncertainty document (`docs/management-under-uncertainty.md`); defines backup role assignments; owns the risk monitoring schedule and escalation path |

---

## 1. Project Overview

### 1.1 Problem Definition

Industrial facilities — manufacturing plants, energy infrastructure, water treatment, and critical infrastructure — manage hundreds to thousands of physical assets: PLCs (Programmable Logic Controllers), HMIs (Human-Machine Interfaces), RTUs, switches, sensors, historians, and servers. These assets are interconnected across Operational Technology (OT) networks structured by the **Purdue Model** — a hierarchical reference model with five levels from field devices (Level 0) to enterprise systems (Level 4).

The core problem is not a lack of data. It is that data is **scattered and incompatible**:

- Asset inventories live in Excel spreadsheets updated manually and always out of date
- Risk assessments are performed by external consultants every 12–18 months — not continuously
- Network topology diagrams are drawn in Visio and diverge from actual cable runs within weeks of creation
- Audit trails of who changed what configuration exist only in email threads and paper logs
- When a security incident occurs, there is no authoritative record of the asset's last known-good state

The result is **management under uncertainty**: plant managers make maintenance and security decisions without reliable, current information. Mean Time To Recovery (MTTR) is extended because the affected asset's configuration history is unavailable. Compliance audits consume weeks because evidence must be manually assembled.

Most commercial tools (Claroty, Dragos, Armis) address this problem at a licensing cost of €50,000–€200,000 per year — inaccessible to small and medium industrial operators.

### 1.2 Proposed Solution

**Industry Maintenance Platform** is an open-source Industrial Asset Management System adapted and documented as a course project. It provides:

- A **centralised, validated asset registry** backed by a PostgreSQL 15 database with 24 entity models covering assets, interfaces, connections, sites, areas, locations, manufacturers, suppliers, contacts, and documents
- An **ICS-specific risk scoring engine** (`services/risk_scoring.py`) that computes a continuous risk score (0–100) for every asset based on Purdue level, business criticality, physical access ease, remote access type, and known vulnerability score
- An **immutable audit trail** — every CREATE, UPDATE, and DELETE on any entity is recorded in the `audit_logs` table with user ID, tenant ID, IP address, UTC timestamp, and a before/after diff
- **Three monitoring dashboards** — Technical Monitoring (`/monitoring`), Management Monitoring (`/management`), and Risk Dashboard (`/risk`) — providing real-time visibility into system health, project progress, and asset risk

The system is deployed using Docker Compose and a `Makefile`. The complete stack starts in under 5 minutes with `make prod`.

### 1.3 Target Users

| User | Role | How They Use Industry Maintenance Platform |
|------|------|------------------------|
| Plant / Facility Manager | Operational decision maker | Reviews asset inventory, risk scores, and recent changes from the main dashboard |
| IT/OT Security Officer | Compliance and security | Exports audit logs for compliance reviews; monitors risk scores for vulnerability management |
| Maintenance Technician | On-site operations | Searches assets by serial number, location, or IP address; uploads photos and maintenance notes from mobile |
| Procurement / Supply Chain | Purchasing and contracts | Links manufacturer, supplier, purchase date, and warranty expiry in a single asset record |
| Compliance Auditor | External or internal audit | Queries `GET /api/v1/audit-logs/` for complete, filterable, append-only change history |
| DevOps Engineer | System operations | Monitors system health via `GET /health/detailed` and the Technical Monitoring Dashboard |
| Course Instructor/Examiner | Academic evaluator | Evaluates a running system demonstrating all course concepts with full documentation |

### 1.4 Why the System Is Needed

Three converging trends make a tool like Industry Maintenance Platform necessary:

1. **Regulatory pressure:** IEC 62443, NIST Cybersecurity Framework, and the NIS2 Directive require operators of critical infrastructure to maintain accurate, current asset inventories and demonstrate change control. Spreadsheet-based systems cannot satisfy these requirements at audit scale.

2. **Attack surface expansion:** The convergence of IT and OT networks means that a compromised PLC at Purdue Level 1 can have physical consequences — process disruption, equipment damage, safety incidents. Risk assessment that runs annually rather than continuously cannot track this exposure.

3. **The gap in open-source tools:** Mature open-source IT asset management tools (i-doit, Snipe-IT, NetBox) exist but are not designed for OT environments. They lack Purdue model awareness, ICS-specific risk parameters, and OT protocol entity types. Industry Maintenance Platform addresses this gap at zero licensing cost.

---

## 2. Software Design and Analysis

### 2.1 Architecture

Industry Maintenance Platform follows a **three-tier architecture** with a hard boundary between each tier:

```
┌─────────────────────────────────────┐
│  Vue.js 3 SPA (Nginx)               │  Presentation layer
│  25+ pages · 13 composables         │  Port 80/443
└───────────────┬─────────────────────┘
                │ HTTPS / JSON
┌───────────────▼─────────────────────┐
│  FastAPI 0.104.1 (Uvicorn)          │  Business logic layer
│  31 routers · 24 models             │  Port 8000 (internal)
│  26 schemas · 22 CRUD modules       │
│  JWT auth · RBAC · rate limiting    │
└───────────────┬─────────────────────┘
                │ SQLAlchemy / psycopg2
┌───────────────▼─────────────────────┐
│  PostgreSQL 15                      │  Data layer
│  24 tables · multi-tenant           │  Port 5432 (internal)
│  Alembic migrations                 │
└─────────────────────────────────────┘
```

Each tier communicates only through its defined interface: the frontend uses the REST API; the backend uses SQLAlchemy ORM sessions. Neither the frontend nor the database contains business logic.

### 2.2 Main Components

**Backend (`backend/app/`):**

| Layer | Files | Responsibility |
|-------|-------|---------------|
| Routers (31) | `routers/*.py` | HTTP routing, request parsing, auth dependency injection |
| Schemas (26) | `schemas/*.py` | Pydantic request/response validation and serialisation |
| CRUD (22) | `crud/*.py` | Database operations — no HTTP concerns |
| Models (24) | `models/*.py` | SQLAlchemy ORM table definitions |
| Services | `services/risk_scoring.py`, `auth.py`, `audit_service.py` | Business logic that spans multiple models |
| Config | `config.py` | Pydantic Settings class; reads all configuration from environment variables |
| Error system | `errors/` | Custom `ErrorCodeException` with bilingual EN/IT messages |

**Frontend (`frontend/src/`):**

| Layer | Files | Responsibility |
|-------|-------|---------------|
| Pages (25+) | `pages/*.vue` | Screen-level components; orchestrate data fetching and layout |
| Components | `components/base/`, `common/`, `features/`, `dialogs/` | Reusable UI building blocks |
| Composables (13) | `composables/*.js` | Shared logic: permissions, filters, status mapping, search, print |
| API layer | `api/api.js` | Single Axios instance with auth cookie and 401-auto-logout interceptor |
| Router | `router.js` | 28 routes with `beforeEach` auth guard |
| i18n | `locales/en/`, `locales/it/` | 40 JSON files; all user-visible strings translated |

**Deployment:**

| Service | Image | Role |
|---------|-------|------|
| `db` | `postgres:15` | Persistent data store with named volume |
| `backend` | Built from `backend/Dockerfile` | FastAPI on port 8000 |
| `frontend` | Built from `frontend/Dockerfile` | Vite production build served by Nginx |
| `nginx`/`traefik` | `nginx:alpine` / `traefik:v2.10` | TLS termination, reverse proxy |

### 2.3 Technologies Used and Justification

| Technology | Version | Justification |
|-----------|---------|--------------|
| **FastAPI** | 0.104.1 | Automatic OpenAPI documentation; Pydantic validation built-in; ASGI for async endpoints; largest Python API framework by GitHub stars in 2024 |
| **SQLAlchemy** | 2.0.27 | Mature ORM with multi-database support; Alembic migration integration; native async support for future scaling |
| **PostgreSQL 15** | 15 | ACID compliance required for audit trail integrity; row-level security for multi-tenancy; proven at industrial scale |
| **Vue.js 3** | 3.3.0 | Composition API enables clean composable architecture; PrimeVue component library reduces UI development time; smaller bundle than React for same functionality |
| **PrimeVue** | 3.x | 90+ production-ready components; consistent design language; no separate CSS framework needed |
| **Docker Compose** | v2 | Reproducible environments; eliminates "works on my machine" deployment failures; `make prod` achieves full deployment in under 5 minutes |
| **GitHub Actions** | free tier | CI/CD with zero infrastructure cost; PostgreSQL service containers for integration testing |
| **Alembic** | 1.13.1 | Schema migration with rollback capability; `alembic upgrade head` runs on every container start |
| **JWT + bcrypt** | python-jose 3.3.0 / passlib 1.7.4 | Industry-standard authentication; bcrypt prevents dictionary attacks; HTTP-only cookies prevent XSS token theft |
| **psutil** | 5.9.8 | Cross-platform CPU/memory/disk metrics; used by `/health/detailed` for system resource monitoring |

### 2.4 Maintainability

**Modular structure:** 31 routers, 22 CRUD files, and 24 model files each address exactly one domain entity. Changing the Asset model does not require reading Supplier or User code.

**Separation of concerns:** Router → Schema → CRUD → Model is a strict layering. Routers never call SQLAlchemy directly; models never contain HTTP logic.

**Reusable components:** 13 frontend composables (`usePermissions`, `useStatus`, `useFilters`, `useGlobalSearch`, etc.) centralise cross-cutting logic. New pages do not rewrite permission checks or error handling from scratch.

**Consistent naming:** All routers follow `{entity}.router`; all CRUD files follow `{entity}.py`. A new developer reading one file understands the pattern for all 31.

**No hardcoded secrets:** All configuration comes from environment variables via `config.py`. Production startup refuses to start with default `SECRET_KEY` or `DEBUG=True`.

### 2.5 Scalability

**Horizontal API scaling:** FastAPI with Uvicorn is stateless. Multiple backend containers can run behind the Nginx/Traefik load balancer; all session state is in the PostgreSQL database (JWT-based, no sticky sessions required).

**Database scaling:** PostgreSQL 15 supports streaming replication for read replicas. The SQLAlchemy engine can be pointed at a primary/replica cluster without changing business logic. New indexes are added via Alembic migrations with zero downtime.

**Frontend scaling:** The Vue.js SPA is a static Vite build served by Nginx. It can be deployed to a CDN without backend changes. The backend and frontend scale independently.

**Current baseline:** 50 concurrent users, 10,000 assets, 100 GB data — achievable on a single 4-core server with 16 GB RAM using the current Docker Compose deployment.

### 2.6 Cohesion

Each module group has a single, well-defined responsibility with no overlap:

| Group | Responsibility | Key Files |
|-------|---------------|-----------|
| Asset features | Full lifecycle: creation, interfaces, connections, photos, risk scoring | `routers/assets.py`, `services/risk_scoring.py`, `pages/AssetDetail.vue` |
| Risk features | Risk score computation and risk dashboard | `services/risk_scoring.py`, `pages/RiskDashboard.vue` |
| Auth/user features | Login, token lifecycle, RBAC, API keys | `main.py` (auth endpoints), `routers/users.py`, `routers/roles.py` |
| Technical monitoring | System health exposure and dashboard | `main.py` (`/health`, `/health/detailed`), `pages/TechnicalMonitoring.vue` |
| Management monitoring | Project KPIs, EVM, milestones, team workload | `routers/management_monitoring.py`, `pages/ManagementMonitoring.vue` |

---

## 3. Management Monitoring

### 3.1 Overview

The Management Monitoring layer answers: **"Is the project on track and is the team healthy?"**

**Backend endpoint:** `GET /api/v1/management/status`
**Frontend dashboard:** `/management` (`ManagementMonitoring.vue`)
**Refresh interval:** 60 seconds auto-refresh
**Authentication:** Required (JWT cookie)

The endpoint returns a structured JSON response combining static sprint plan data with a live asset count queried from the PostgreSQL database, demonstrating that the management layer connects to real system state.

### 3.2 Progress Monitoring

| KPI | Endpoint Field | Current Value | Meaning |
|-----|---------------|---------------|---------|
| Sprint number | `project.current_sprint` | 4 of 4 | Final sprint |
| Task completion | `tasks.progress_percent` | 87.5 % | 28 of 32 tasks complete |
| Overdue tasks | `tasks.overdue` | 0 | No blocked work |
| Live assets | `project.assets_managed` | Live DB query | Confirms system holds real data |

### 3.3 Schedule Monitoring — Earned Value Management

Industry Maintenance Platform uses Earned Value Management to quantify schedule health in objective, comparable terms:

| EVM Metric | Formula | Current Value | Interpretation |
|-----------|---------|---------------|---------------|
| **Planned Value (PV)** | Planned story points at week N | 151 SP | What should be done |
| **Earned Value (EV)** | Story points accepted by PO | 145 SP | What is actually done |
| **SPI** | EV / PV | **0.96** | 96 % of schedule achieved — on track |
| **Schedule Variance** | EV − PV | −6 SP | Slightly behind; within acceptable range |

An SPI of 0.96 means the team is 4 % behind the ideal schedule — well within the ±10 % threshold for "on track." No scope reduction was triggered.

**Sprint velocity history:**

| Sprint | Story Points Completed | Notes |
|--------|----------------------|-------|
| Sprint 1 (W1–W4) | 45 | Foundation: auth, CRUD, DB schema, CI |
| Sprint 2 (W5–W7) | 52 | Risk scoring, audit trail, main dashboard |
| Sprint 3 (W8–W10) | 54 | Network map, floor plan, technical monitoring |
| Sprint 4 (W11–W13) | 48 | Management monitoring, dashboards, docs, tests |

### 3.4 Cost Monitoring

All infrastructure costs are €0 (Docker, PostgreSQL, GitHub Actions, Nginx are free and open source). Cost tracking uses person-hours as the effort proxy.

| Cost Area | Estimated Hours | Actual Hours | Variance |
|-----------|----------------|-------------|---------|
| Development effort | 302 h | 289 h | −13 h (under budget) |
| Testing effort | 60 h | 62 h | +2 h |
| Documentation effort | 80 h | 83 h | +3 h |
| Training / onboarding | 5 h | 5 h | 0 |
| **Total** | **447 h** | **439 h** | **−8 h (−1.8 %)** |

**CPI (Cost Performance Index):** 447 / 439 = **1.02** — slightly under budget. Effort variance is within the ±5 % target.

### 3.5 KPIs on the Management Dashboard

The Management Dashboard at `/management` displays six KPI tiles as the top row:

| Tile | Value | Source |
|------|-------|--------|
| Current Sprint | 4 / 4 | `project.current_sprint` |
| SPI | 0.96 | `schedule.spi` |
| Task Completion | 87.5 % | `tasks.progress_percent` |
| Assets Managed | Live count | `project.assets_managed` (DB query) |
| Team Load | 7 members | `team_workload` array |
| Open Risks | 7 active | `risks.by_status.active` |

### 3.6 Milestones

| ID | Milestone | Due Week | Status | Key Deliverables |
|----|-----------|----------|--------|-----------------|
| M1 | Project Kickoff | W1 | Completed | Team formed, repo forked, branching model agreed, roles assigned |
| M2 | Sprint 1 Complete | W4 | Completed | JWT auth, RBAC, asset CRUD, DB schema, CI pipelines running |
| M3 | Sprint 2 Complete | W7 | Completed | Risk scoring engine, audit trail, main dashboard charts |
| M4 | Sprint 3 Complete | W10 | Completed | Network map, floor plan, `/health/detailed`, TechnicalMonitoring.vue |
| M5 | Sprint 4 Complete | W13 | Completed | Management monitoring, RiskDashboard.vue, all docs, tests |
| M6 | Documentation Freeze | W14 | Completed | All 30+ docs reviewed and finalised |
| M7 | Final Submission | W16 | In progress | Repository tagged, video recorded, report submitted |

---

## 4. Technical Monitoring

### 4.1 Overview

The Technical Monitoring layer answers: **"Is the system healthy and responsive right now?"**

Two unauthenticated health endpoints are exposed at the application root (not behind `/api/v1` — monitoring systems must access them without credentials):

| Endpoint | Purpose | Consumer |
|----------|---------|---------|
| `GET /health` | Basic liveness probe | Docker healthcheck, uptime monitors |
| `GET /health/detailed` | Full system metrics | TechnicalMonitoring.vue (30 s), debugging |

### 4.2 Health Endpoint Responses

**`GET /health`** — Basic check:
```json
{
  "status": "ok",
  "database": "connected",
  "uptime": "running",
  "timestamp": "2026-04-20T12:00:00Z"
}
```
`database` becomes `"disconnected"` if `SELECT 1` raises an exception. `timestamp` is always UTC with `Z` suffix (`datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`).

**`GET /health/detailed`** — Full metrics:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 86400,
  "components": {
    "database": {
      "status": "healthy",
      "response_time_ms": 2,
      "pool_size": 5,
      "pool_checked_out": 1
    },
    "cache": { "status": "available", "type": "memory" },
    "api":   { "status": "running" }
  },
  "system": {
    "cpu_percent": 12.4,
    "memory_percent": 48.2,
    "memory_used_mb": 1964,
    "memory_total_mb": 8192,
    "disk_percent": 34.1,
    "python_version": "3.11.6"
  }
}
```
`system` block requires `psutil 5.9.8`. If not installed, the system fields are omitted and the endpoint returns 200 with a note.

### 4.3 Performance Monitoring

| Metric | Source | Normal Range | Alert Threshold |
|--------|--------|-------------|----------------|
| DB query response time | `components.database.response_time_ms` | 1–10 ms | > 500 ms |
| API uptime | `uptime_seconds` | Increasing | Resets to 0 (container restart) |
| Connection pool usage | `pool_checked_out / pool_size` | < 50 % | > 90 % |

### 4.4 Error Rate Monitoring

HTTP 5xx responses are logged to `logs/error.log`. The alert thresholds defined on the Technical Monitoring Dashboard are:

| Error Signal | Warning | Critical |
|-------------|---------|---------|
| 5xx rate | > 1 % over 5 min | > 5 % over 1 min |
| Login failures from one IP | > 10 / min | > 20 / min (brute force) |
| DB connection failures | Any | Treat as P1 immediately |

Login failure events are written to `logs/security.log` in JSON format for structured monitoring.

### 4.5 Stability Monitoring

Three-level stability confirmation:

| Level | Mechanism | Frequency |
|-------|-----------|-----------|
| **Container** | `pg_isready` healthcheck + `curl /health` healthcheck | Every 10–30 s |
| **Application** | `TechnicalMonitoring.vue` polls `/health/detailed` | Every 30 s |
| **System** | `psutil` CPU/memory/disk via `/health/detailed` | Every 30 s |

Docker's `restart: unless-stopped` policy restarts the backend container automatically if the health check fails three consecutive times. Recovery time is typically 60–90 seconds without human intervention.

### 4.6 Health Checks

**Docker health check configuration** (from `docker-compose.prod.yml`):
```yaml
backend:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

The `start_period: 40s` allows Alembic migrations to complete before health checks begin.

### 4.7 Logs

| Log File | Content | Format | Retention |
|----------|---------|--------|-----------|
| `logs/app.log` | All HTTP requests, INFO+ events | Plain text | 30 days |
| `logs/error.log` | ERROR and CRITICAL events only | Plain text | 90 days |
| `logs/security.log` | All auth events: login success, failure, logout, token refresh | JSON (one object per line) | 365 days |

### 4.8 Alerts

The Technical Monitoring Dashboard displays colour-coded alert indicators without requiring an external alerting tool:

| Signal | Colour | Trigger |
|--------|--------|---------|
| Database disconnected | Red banner (full width) | `components.database.status != "healthy"` |
| CPU > 70 % | Amber progress bar | `system.cpu_percent > 70` |
| Memory > 80 % | Amber progress bar | `system.memory_percent > 80` |
| Disk > 85 % | Red progress bar | `system.disk_percent > 85` |
| Overall degraded | Amber status banner | `status == "degraded"` |
| Overall unhealthy | Red status banner | `status == "unhealthy"` |

### 4.9 Database Status

Monitored at three levels: Docker `pg_isready` container healthcheck (every 10 s); live `SELECT 1` ping in `/health/detailed` (on request); connection pool statistics (`pool_size`, `pool_checked_out`) visible in the Technical Monitoring Dashboard.

### 4.10 Uptime

`uptime_seconds` is calculated from `app.state.startup_time` set in the FastAPI `@app.on_event("startup")` handler. A container restart resets this counter to 0, making unexpected restarts immediately visible on the dashboard.

---

## 5. UI Design

### 5.1 Design Principles

All three monitoring dashboards follow five principles:
1. **Status at a glance** — green/amber/red coding communicates state within 2 seconds of page load
2. **Information density without clutter** — most actionable data first; details reachable in one click
3. **Industrial context** — terminology and icons reflect OT/ICS environments
4. **Consistency** — all dashboards use PrimeVue components, the same card pattern, and the same CSS variable palette
5. **Non-breaking** — all dashboards are additions to the existing route structure; no existing pages were modified

**Shared colour palette:**

| State | Colour | Hex |
|-------|--------|-----|
| Healthy / Low risk | Green | `#10B981` |
| Warning / Medium risk | Amber | `#F59E0B` |
| Danger / High risk | Red | `#EF4444` |
| Unknown / Inactive | Gray | `#6B7280` |
| Primary action | Blue | `#3B82F6` |

### 5.2 Management Dashboard (`/management`)

**Purpose:** Project health for the PM; course concept demonstration for the examiner.
**Users:** Project Manager, Course Instructor
**Refresh:** 60-second auto-refresh

**Panels:**

| Panel | Component | What Is Shown |
|-------|-----------|--------------|
| KPI tiles (top row) | `<div class="metric-card">` × 6 | Sprint number, SPI, task %, live asset count, team size, open risk count |
| Sprint velocity | Custom CSS bar chart | Story points completed per sprint (4 bars) |
| Milestones | `<DataTable>` + `<Tag>` | 7 milestones: due week, status, deliverables |
| Team workload | `<DataTable>` + `<ProgressBar>` | Assigned SP, completed SP, load % — bar turns red at > 95 % |
| Cost/effort | HTML `<table>` | Estimated vs. actual hours, CPI |
| Risk summary | Badge grid + list | Severity counts; top 4 open risks with owner and mitigation status |

**Key interaction:** If the SPI KPI tile turns red (< 0.85), the PM opens the Management Dashboard and uses the Milestones table and Team Workload table to identify the source of the delay before the next stand-up.

### 5.3 Technical Monitoring Dashboard (`/monitoring`)

**Purpose:** Real-time system health visibility without SSH access.
**Users:** DevOps Engineer, IT/OT Administrator, Backend Developer
**Refresh:** 30-second auto-refresh; data source: `GET /health/detailed`

**Panels:**

| Panel | Component | What Is Shown |
|-------|-----------|--------------|
| Status banner (full-width) | `<div class="status-banner">` coloured by status | Overall status, version, uptime, environment |
| Component cards | `<div class="metric-card">` × 3 | Database (status + response time + pool), Cache (status + type), API (status + Python version) |
| System resources | `<ProgressBar>` × 3 | CPU %, Memory %, Disk % with amber/red thresholds |
| Alert thresholds | `<DataTable>` | Reference table: metric, warning threshold, critical threshold, severity |

**Key interaction:** A red status banner is visible across the room without reading text. The operator checks the component cards to identify which service degraded. If it is the database card, they check `logs/error.log` and the connection pool count.

### 5.4 Risk Dashboard (`/risk`)

**Purpose:** Surfaces which assets are at highest risk and what the mitigation status is.
**Users:** Risk Manager, Safety Manager, IT/OT Security Officer
**Data sources:** `GET /assets/risk-overview` + `GET /dashboard/risky-assets?limit=15`

**Panels:**

| Panel | Component | What Is Shown |
|-------|-----------|--------------|
| KPI tiles | `<div class="metric-card">` × 4 | Total assets, high risk count (≥70), medium risk count (40–69), low risk count (<40) |
| Risk distribution | `<ProgressBar>` × 3 | % of assets in each band with absolute count |
| Highest-risk assets | `<DataTable>` | Asset name (clickable → detail), type, site, Purdue level, risk score badge |
| Project risk register | `<DataTable>` | 10 project risks: ID, title, category, severity, owner, mitigation status |
| Risk trend note | Info card | Explains that time-series is planned; redirects to Asset Detail for per-asset history |

**Key interaction:** A maintenance technician sees PLC-01 at risk score 82 (red badge). They click the asset name, navigate to Asset Detail, and see the last configuration change that drove the score up — enabling a targeted maintenance action.

### 5.5 Navigation

All three dashboards are accessible from the **Monitoring** section of the sidebar:

```
Monitoring
  ├── Technical Monitoring    → /monitoring
  ├── Management Monitoring   → /management
  └── Risk Dashboard          → /risk
```

Translation keys in `locales/en/menu.json` and `locales/it/menu.json` ensure the sidebar renders correctly in both languages without `undefined` labels.

---

## 6. Value Creation

### 6.1 Problem Statement Recap

Industrial facilities operate with asset data scattered across spreadsheets, paper records, and disconnected systems. The result: management under uncertainty, high MTTR, expensive compliance audits, and reactive — rather than preventive — maintenance.

### 6.2 Business Value

**Centralised asset registry** — one PostgreSQL database replaces 5–10 disconnected spreadsheets. Assets are validated by Pydantic schemas before writing; stale records are eliminated by the enforced update workflow.

**Continuous risk assessment** — `risk_scoring.py` computes a risk score for every asset on every attribute change. A security officer can identify the top 5 highest-risk assets in 3 seconds rather than scheduling a consultant visit.

**Immutable audit trail** — every CREATE, UPDATE, and DELETE is recorded with user, timestamp, and diff in the `audit_logs` table. A compliance audit that previously required manual log collection over 3 weeks can now be served by a single `GET /api/v1/audit-logs/` API call.

**Technical monitoring** — `GET /health/detailed` and the Technical Monitoring Dashboard reduce mean detection time for silent failures from "the next user to notice" to ≤ 30 seconds.

### 6.3 Operational Value

| Manual Task (Before) | Automated Alternative (After) | Time Saved |
|---------------------|------------------------------|-----------|
| Monthly asset spreadsheet update | Real-time web UI or CSV bulk import | ~4 h/month per site |
| Quarterly risk assessment (consultant) | Continuous automated scoring in `risk_scoring.py` | ~1–2 days/assessment cycle |
| Manual audit log collection | `GET /api/v1/audit-logs/` with date filter | ~1 day/review |
| Network topology update in Visio | Interactive network map (`/network-map`) | ~2 h/change |
| Manual health checks by pinging servers | `GET /health/detailed` auto-polled every 30 s | Eliminates reactive checks |
| Asset lookup across spreadsheets | Global spotlight search (Cmd+K) → < 200 ms | Minutes to seconds |

### 6.4 Cost vs. Benefit

| Cost Area | Estimated | Actual |
|-----------|-----------|--------|
| Development effort | 302 h | 289 h |
| Testing effort | 60 h | 62 h |
| Documentation effort | 80 h | 83 h |
| Infrastructure | €0 | €0 |
| Licensing | €0 | €0 |
| **Total project cost** | **~447 h** | **~434 h** |

**Infrastructure cost is €0.** Docker, PostgreSQL, Nginx, and GitHub Actions are all open-source or free-tier. Commercial equivalents (Claroty, Dragos) cost €50,000–€200,000/year in licensing alone.

**Year 1 operational benefit estimate (medium industrial plant):**

| Benefit | Annual Value |
|---------|-------------|
| Reduced technician search time (15 min → 30 sec per lookup × 3,000 lookups/year) | €15,000 |
| Faster compliance audits (3 weeks → 2 days × 2 audits/year) | €40,000 |
| Preventive maintenance from risk scoring (2 avoided incidents/year × €20,000 each) | €40,000 |
| Reduced consultant risk assessment cost (annual assessment → continuous) | €15,000 |
| **Total Year 1 benefit** | **€110,000** |

ROI estimate: €110,000 benefit / €0 infrastructure cost = **unlimited on operational budget**. Against the development effort at €25/hour academic rate (€10,850), ROI is 914 % in Year 1.

### 6.5 Beneficiaries

| Beneficiary | Primary Benefit |
|-------------|----------------|
| Plant Manager | Single dashboard replaces manual status collection |
| IT/OT Security Officer | Audit evidence available via API; continuous risk scores |
| Maintenance Technician | Asset lookup in < 200 ms from any device |
| Compliance Auditor | `GET /api/v1/audit-logs/` returns complete filterable trail |
| Procurement | Manufacturer, supplier, warranty in one asset record |
| Course Examiner | Running system demonstrating every course concept |

---

## 7. Stakeholder Management

### 7.1 Internal Stakeholders

| Stakeholder | Expectations | Communication | Conflict Handling |
|------------|-------------|--------------|------------------|
| **Obada (PM)** | Project meets all 10 course deliverables on schedule | Daily Slack; weekly stand-up | Scope disputes escalated through change control process |
| **Mohanad (Backend)** | Clear API specifications before implementation; no moving goalposts mid-sprint | Sprint planning + async GitHub | Technical disagreements resolved by PM with 24-hour decision rule |
| **Zekeriya (Frontend)** | Stable backend endpoints to connect to; UX direction from Fares | Async GitHub; daily Slack | Breaking API changes require 48-hour advance notice to Frontend |
| **Praise-God (QA)** | Access to test environment; clear acceptance criteria per feature | Sprint review; async | Missing acceptance criteria treated as incomplete story — not QA's fault |
| **Fares (UX)** | Early involvement in feature decisions; feedback on designs before implementation | Sprint planning; Figma reviews | Design disagreements resolved by PM after one round of async comment |
| **Hamdi (DevOps)** | Infrastructure requirements stable after Sprint 1; no last-minute deployment surprises | Weekly sync; CI alerts | Deployment changes require PM approval and 48-hour notice |
| **Abdulaziz (Risk)** | Risk register reviewed in every sprint; risk inputs acted on | Sprint retro; async | Risk concerns escalated to PM; PM decides within 24 hours |

### 7.2 External Stakeholders

| Stakeholder | Role | Expectations | Communication |
|------------|------|-------------|--------------|
| **Course Instructor / Examiner** | Primary evaluator | Documented, running system covering all course concepts | Final presentation (Week 16); submitted report |
| **Plant Manager** (simulated) | Operational decision maker | Single dashboard; no training required | Represented by user stories; validated in demo data |
| **IT/OT Security Officer** (simulated) | Compliance and security | Immutable audit trail; continuous risk scores | Represented by `GET /api/v1/audit-logs/` API requirement |
| **Maintenance Technician** (simulated) | On-site operations | Fast asset search; mobile-friendly interface | Represented by global search (Cmd+K) requirement |
| **Compliance Auditor** (simulated) | External audit | Exportable, filterable change history | Represented by audit log API requirement |
| **Industry Maintenance Platform Open-Source Community** | Upstream project owners | Adaptations documented; no breaking changes to upstream | No direct communication needed; branch `course-adaptation-monitoring` keeps changes isolated |

### 7.3 Communication Methods

| Method | Frequency | Participants | Purpose |
|--------|-----------|-------------|---------|
| Daily Slack stand-up | Daily (async) | All 7 | Blockers, progress, dependencies |
| Sprint planning | Every 3 weeks | All 7 | Commit to sprint backlog |
| Sprint review | Every 3 weeks | All 7 | Demo completed features |
| Sprint retrospective | Every 3 weeks | All 7 | Process improvement |
| Weekly PM report | Weekly | PM + team leads | Schedule variance, risk status |
| Final presentation | Week 16 | Team + instructor | Course evaluation |

### 7.4 Conflict Handling

All conflicts follow a 4-level escalation:

1. **Peer resolution** (same day) — team members resolve directly
2. **PM mediation** (within 24 hours) — PM facilitates; all parties have one input
3. **PM decision** (within 48 hours) — PM decides; decision is binding
4. **Course instructor** — invoked only for scope or grading disagreements

No escalation beyond Level 2 occurred during this project.

---

## 8. Risk Management

### 8.1 Risk Identification

Risks were identified through three methods:
1. **Kickoff risk brainstorm** — each team member contributed risks in their domain
2. **Architecture review** — backend complexity and inherited codebase risks identified in Week 2
3. **Ongoing monitoring** — new risks added to the register when identified during sprints

**14 risks identified across 9 categories:** Scope, Resource, Technical, Quality, Schedule, Security, Infrastructure, Stakeholder, Operational.

### 8.2 Risk Assessment

Each risk is scored on a 1–5 scale for Impact and Probability. Risk Score = Impact × Probability (1–25).

| Severity Band | Score | Count |
|--------------|-------|-------|
| High | ≥ 15 | 4 |
| Medium | 8–14 | 6 |
| Low | ≤ 7 | 4 |

### 8.3 Risk Register (Top 10)

| ID | Risk | Category | Impact | Prob | Score | Owner | Status |
|----|------|---------|--------|------|-------|-------|--------|
| R-01 | Scope creep from feature requests | Scope | 4 | 4 | 16 | PM | Active |
| R-02 | Key team member unavailability | Resource | 4 | 4 | 16 | PM | Active |
| R-03 | CI/CD pipeline failure blocking merges | Technical | 4 | 3 | 12 | DevOps | Mitigated |
| R-04 | Database migration breaking existing data | Technical | 5 | 3 | 15 | Backend | Active |
| R-05 | Integration gap frontend/backend | Technical | 3 | 4 | 12 | Frontend | Mitigated |
| R-06 | Insufficient test coverage | Quality | 4 | 3 | 12 | QA | Active |
| R-07 | Schedule delay from course workload overlap | Schedule | 3 | 4 | 12 | PM | Active |
| R-08 | Security misconfiguration in production | Security | 5 | 2 | 10 | DevOps | Mitigated |
| R-09 | Data loss from database failure | Infrastructure | 5 | 2 | 10 | DevOps | Active |
| R-10 | Unclear requirements from instructor | Stakeholder | 3 | 2 | 6 | PM | Mitigated |

### 8.4 Risk Mitigation

Selected mitigation strategies:

**R-01 (Scope creep):** Change control board — all scope additions require PM written approval. Scope freeze enforced from Week 13. Result: 0 uncontrolled scope additions.

**R-04 (DB migration):** Alembic migrations tested on a copy of production data before applying. `make reset-db` documented for emergency rollback. Backup script in `scripts/backup.py`.

**R-08 (Security misconfiguration):** `config.py` Pydantic Settings class raises at startup if `SECRET_KEY` is default, `DEBUG=True`, or `SECURE_COOKIES=False`. These checks cannot be bypassed.

**R-03 (CI/CD failure):** `python -m py_compile` syntax check added to `backend.yml` as a fast-fail before running the full test suite. Local pre-commit hook option documented.

### 8.5 Risk Monitoring

| Frequency | Activity |
|-----------|---------|
| Weekly | PM reviews top 5 open risks; updates status |
| Sprint start | Full register review; new risks added if identified |
| Milestone review | Closed risks retired; mitigated risks confirmed stable |
| Sprint retrospective | Risks that materialised discussed; contingency plans updated |

The **Risk Dashboard** at `/risk` surfaces the top open risks from the register alongside asset-level risk scores, making risk monitoring a continuous activity rather than a periodic report.

---

## 9. CI/CD and Continuous Testing

### 9.1 CI Pipeline

Two GitHub Actions workflows run on every push to every branch:

**`.github/workflows/backend.yml`** — owned by Hamdi (DevOps):

| Step | Command | Gate |
|------|---------|------|
| Install dependencies | `pip install -r requirements.txt` | Hard fail if packages conflict |
| Syntax check | `python -m py_compile app/main.py app/database.py app/config.py` | Hard fail if syntax error |
| Import check | `python -c "from app.main import app"` | Hard fail if circular import or missing module |
| Pytest with coverage | `pytest tests/ -v --cov=app --cov-report=term-missing` | Hard fail if any test fails |

A real PostgreSQL 15 container runs as a GitHub Actions service. No database mocking — mocked tests historically allowed schema-breaking migrations to pass CI undetected.

**`.github/workflows/frontend.yml`** — owned by Hamdi (DevOps):

| Step | Command | Gate |
|------|---------|------|
| Install dependencies | `npm ci` (exact lock file) | Hard fail if packages conflict |
| Unit tests | `npm run test:unit` (Vitest) | Hard fail if any assertion fails |
| Production build | `npm run build` (Vite) | Hard fail if broken import or missing asset |

### 9.2 CD Plan — Local / Self-Hosted

No cloud deployment, no paid services. The full CD pipeline runs on the operator's machine:

```
git push → GitHub Actions CI (free tier)
              ↓ passes
Code review and merge to main
              ↓
make prod       (builds Docker images, starts 4 services, runs Alembic migrations)
              ↓
make status     (confirms all containers are healthy)
              ↓
curl -k https://localhost/health  (confirms backend responds "ok")
              ↓
/monitoring dashboard  (confirms system health banner is green)
```

### 9.3 Automated Testing

**Backend test files (`backend/tests/`):**

| File | Test Type | Count | What Is Covered |
|------|-----------|-------|----------------|
| `test_health.py` | Unit + API | 15 assertions | All `/health` fields; no-auth access; detailed health components |
| `test_auth.py` | API + Security | ~20 assertions | Login, token refresh, logout, invalid credentials |
| `test_users.py` | API + RBAC | ~15 assertions | User CRUD, role permissions, viewer cannot delete |
| `test_comprehensive.py` | Integration | ~25 assertions | Asset creation, site hierarchy, multi-step workflows |

**Frontend test file (`frontend/src/composables/__tests__/useStatus.spec.js`):**
- 29 assertions covering `getContrastColor`, `getStatusSeverity` (colour and name paths), `getStatusColor`, `getStatusLabel`
- `vue-i18n` mocked so tests run without a Vue application instance
- Configured in `vite.config.js` with `environment: 'jsdom'`

### 9.4 Deployment Validation

After every `make prod`, the following smoke tests must pass before the deployment is declared stable:

```bash
# 1. Liveness
curl -k https://localhost/health
# Expected: {"status":"ok","database":"connected",...}

# 2. Full health
curl -k https://localhost/health/detailed
# Expected: {"status":"healthy","components":{"database":{"status":"healthy"}}}

# 3. Login
curl -k -c /tmp/c.txt -X POST https://localhost/login -F "email=admin@example.com" -F "password=admin123"
# Expected: 200

# 4. Authenticated API
curl -k -b /tmp/c.txt https://localhost/api/v1/assets/
# Expected: {"items":[...],"total":N}
```

### 9.5 Health-Check Validation

The `/health` endpoint is tested in CI by `test_health.py`. The assertions are:

- `status == "ok"` — not `"healthy"` (spec changed in Sprint 4; test updated accordingly)
- `database == "connected"` — live `SELECT 1` against the CI PostgreSQL service
- `uptime in ("running", "starting")` — reflects container state
- `timestamp.endswith("Z")` — UTC format enforced
- HTTP 200 with no auth cookie — endpoint is always publicly accessible

The `/health/detailed` endpoint is tested by `TestDetailedHealth` (10 assertions) covering `status`, `components.database.status`, `response_time_ms`, `uptime_seconds`, and `system.python_version`.

---

## 10. Management Under Uncertainty

### 10.1 Changing Requirements

All scope changes require written approval from the PM before implementation. The change control process:

```
Proposal received
    → PM evaluates: maps to course requirement? fits sprint? no rework?
    → Accepted: added to sprint backlog with explicit story points
    → Deferred: added to backlog for Sprint N+1
    → Rejected: documented with reason
```

**Scope freeze enforced from Week 13.** From that point, only bug fixes, test writing, and documentation completion are in scope. This prevents the "one more feature" pattern that reliably breaks final submissions.

### 10.2 Delays

Early detection via SPI on the Management Dashboard. An SPI below 0.90 triggers a recovery conversation at the next stand-up. The response is **scope adjustment, not deadline extension** — lower-priority stories move to the next sprint to protect committed deliverables.

### 10.3 Budget and Scope Control

Cost is measured in person-hours. Effort variance is reported when actual exceeds 150 % of estimate — early enough to rescope. The sprint plan holds 10–15 % of story points as unassigned buffer to absorb unexpected complexity.

### 10.4 Technical Uncertainty

When a technical unknown is discovered, the team member is given a **2-hour time-boxed investigation** to produce one of three findings:
- "I understand it now, here is the updated estimate"
- "I need help — can someone pair with me"
- "This is more complex than expected, here is a reduced-scope alternative"

Spike tasks are used for high-risk unknowns. The `docs/software-design-analysis.md` document was created specifically to map the inherited codebase before committing to adaptations.

### 10.5 Risk-Based Decision Making

Every significant decision during the project was evaluated against the risk register:
- Choosing Docker Compose over manual server setup → mitigates R-09 (data loss) and R-08 (misconfiguration)
- Retaining the existing PostgreSQL schema rather than rewriting → mitigates R-04 (migration failure)
- Scope freeze from Week 13 → mitigates R-01 (scope creep) and R-07 (schedule delay)
- Backup role assignments for all 7 roles → mitigates R-02 (member unavailability)

The risk register is not a compliance document — it is an **operational decision tool** reviewed weekly by the PM.

### 10.6 Response Matrix

| Scenario | Detection | Response |
|----------|-----------|---------|
| Changing requirements | Proposal received | Change control process; PM approval required |
| Delays | SPI < 0.90 | Rescope sprint; protect committed stories |
| Cost overrun | Effort > 150 % estimate | Re-estimate; redistribute tasks; trim scope |
| Scope addition | Proposal received | Change control; defer if sprint full |
| Technical unknown | Investigation finds complexity | Time-box spike; report finding; adjust estimate |
| Failed test | CI badge red | Assign to owner within 24 h; fix, do not skip |
| Deployment failure | `make status` unhealthy | Follow runbook; check logs; rollback if needed |
| Unavailable member | Member reports absence | Activate backup role; redistribute tasks; adjust scope |

---

## 11. Conclusion

### 11.1 Final Project Summary

The Industry Maintenance Platform adaptation project delivered a **running, documented, and monitored Industrial Asset, Risk, Management and Technical Monitoring Platform** by adapting the open-source Industry Maintenance Platform v1.1.0 repository and connecting its features to all course requirements.

**What was built:**

| Deliverable | Status | Evidence |
|-------------|--------|---------|
| Health monitoring endpoint (`/health`, `/health/detailed`) | Implemented | `backend/app/main.py` lines 371–474 |
| Technical Monitoring Dashboard (`/monitoring`) | Implemented | `frontend/src/pages/TechnicalMonitoring.vue` |
| Management Monitoring Dashboard (`/management`) | Implemented | `frontend/src/pages/ManagementMonitoring.vue` + `routers/management_monitoring.py` |
| Risk Dashboard (`/risk`) | Implemented | `frontend/src/pages/RiskDashboard.vue` |
| Backend CI (syntax check + pytest) | Implemented | `.github/workflows/backend.yml` |
| Frontend CI (Vitest + build) | Implemented | `.github/workflows/frontend.yml` |
| Backend tests | Implemented | `backend/tests/` — 4 files, ~75 assertions |
| Frontend unit tests | Implemented | `useStatus.spec.js` — 29 assertions |
| Risk register | Implemented | `docs/risk-management.md` — 14 risks |
| Stakeholder management | Implemented | `docs/stakeholder-management.md` — 13 stakeholders |
| Value creation analysis | Implemented | `docs/value-creation.md` + `docs/project-report.md §6` |
| Management under uncertainty | Implemented | `docs/management-under-uncertainty.md` — 8 scenarios |
| Software design analysis | Implemented | `docs/software-design-analysis.md` — 10 sections |
| Monitoring strategy | Implemented | `docs/monitoring-strategy.md` — 22-metric table |
| UI dashboard design | Implemented | `docs/ui-dashboard-design.md` — 3 dashboards |

**All 7 sprint milestones met.** SPI at sprint 4: 0.96. CPI: 1.02. Zero critical incidents.

### 11.2 Feasibility

The project is **technically feasible and operationally viable** at zero infrastructure cost:

- **Deployment:** `make prod` — full production system in under 5 minutes on any machine with Docker
- **Data migration:** CSV bulk import templates provided for initial asset migration
- **Scaling:** Horizontal scaling documented; current single-server deployment handles 50 concurrent users and 10,000 assets
- **Maintenance:** Dependency updates via Dependabot; Alembic handles schema evolution; Docker Compose makes rebuilds predictable

The main feasibility constraint is **adoption** — users must enter accurate asset data for the risk scores and audit trail to have value. The demo data (`make demo`) and 5-minute quick start (`docs/QUICK_START.md`) address the initial adoption barrier.

### 11.3 Value

Industry Maintenance Platform delivers value on three dimensions:

**Operational value:** Replaces scattered spreadsheets with a validated, searchable, auditable asset registry. Risk scores update continuously — not annually. Compliance audit evidence is a single API call.

**Economic value:** €0 infrastructure cost versus €50,000–€200,000/year for commercial equivalents. Year 1 operational benefit estimate: €110,000+ for a medium industrial facility.

**Academic value:** Every course concept is demonstrated through running software and comprehensive documentation — not claims or diagrams. A course examiner can `make prod` and reach every feature in under 10 minutes.

### 11.4 Why This Project Meets Course Goals

| Course Goal | How Industry Maintenance Platform Demonstrates It |
|-------------|-------------------------------|
| Software Project Management | 4-sprint plan, EVM, SPI, milestone tracking, change control, risk register |
| Technical Monitoring | `GET /health/detailed` with 10 metrics; 30-second auto-refresh dashboard; 3-level downtime prevention |
| Management Monitoring | `GET /api/v1/management/status` with 14 metrics; 60-second dashboard with EVM, team workload, milestones |
| Value Creation | €110,000/year operational benefit; ROI analysis; 6-beneficiary before/after table |
| Management Under Uncertainty | 8-scenario response framework; backup role assignments; risk register as decision tool |
| Design Quality | 31 routers, 22 CRUD files, 24 models — functional cohesion; SoC enforced at layer boundary |
| CI/CD and Continuous Testing | Two GitHub Actions workflows; pytest + Vitest; syntax check; local Docker CD |
| Stakeholder Management | 13 stakeholders mapped; communication matrix; conflict escalation process |
| Risk Management | 14 risks across 9 categories; probability × impact scoring; mitigation + contingency per risk |
| UI/Dashboard Design | 3 implemented dashboards with documented purpose, panels, interactions, and accessibility |

**The core insight:** Monitoring and observability are not optional extras — they are the mechanism by which a software project maintains control under uncertainty. Industry Maintenance Platform makes industrial asset state observable. Our project management made project state observable. Both apply the same principle.

---

## Appendix A — Document Index

| Document | Location | Owner |
|---------|----------|-------|
| Team | [docs/TEAM.md](TEAM.md) | PM |
| Team Work Plan | [docs/team-work-plan.md](team-work-plan.md) | PM |
| Project Management Plan | [docs/PROJECT_MANAGEMENT_PLAN.md](PROJECT_MANAGEMENT_PLAN.md) | PM |
| Architecture Design | [docs/ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) | Backend |
| Software Design Analysis | [docs/software-design-analysis.md](software-design-analysis.md) | Backend + PM |
| Technical Monitoring | [docs/TECHNICAL_MONITORING.md](TECHNICAL_MONITORING.md) | Backend |
| Monitoring Metrics | [docs/monitoring-metrics.md](monitoring-metrics.md) | DevOps |
| Monitoring Strategy | [docs/monitoring-strategy.md](monitoring-strategy.md) | DevOps + PM |
| Risk Management | [docs/RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) | Risk Manager |
| Risk Register | [docs/risk-management.md](risk-management.md) | Risk Manager |
| Stakeholder Management | [docs/stakeholder-management.md](stakeholder-management.md) | Risk Manager + PM |
| Value Creation | [docs/value-creation.md](value-creation.md) | PM |
| UI Dashboard Design | [docs/ui-dashboard-design.md](ui-dashboard-design.md) | UX/UI |
| CI/CD and Testing | [docs/ci-cd-testing.md](ci-cd-testing.md) | DevOps + QA |
| Management Under Uncertainty | [docs/management-under-uncertainty.md](management-under-uncertainty.md) | Risk Manager |
| Project Report | [docs/project-report.md](project-report.md) | PM (this document) |

## Appendix B — Course Concept Mapping

| Course Concept | Evidence Location |
|---------------|-----------------|
| Value Creation | `docs/value-creation.md`; this report §6 |
| Management Under Uncertainty | `docs/management-under-uncertainty.md`; this report §10 |
| Design Quality and Metrics | `docs/software-design-analysis.md`; this report §2 |
| Technical Monitoring | `backend/app/main.py` (`/health/detailed`); `TechnicalMonitoring.vue`; this report §4 |
| Management Monitoring | `routers/management_monitoring.py`; `ManagementMonitoring.vue`; this report §3 |
| CI/CD | `.github/workflows/backend.yml` + `frontend.yml`; this report §9 |
| Continuous Testing | `backend/tests/` (4 files); `useStatus.spec.js`; this report §9 |
| Stakeholder Management | `docs/stakeholder-management.md`; this report §7 |
| Risk Management | `docs/risk-management.md`; `RiskDashboard.vue`; this report §8 |
| UI/Dashboard Design | `docs/ui-dashboard-design.md`; 3 Vue pages; this report §5 |
