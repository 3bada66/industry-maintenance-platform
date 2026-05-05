# Final Project Report
## Industry Maintenance Platform
### Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Institution:** Istinye University
**Submission Date:** May 2026

---

## Team Members & Roles

| Name | Student ID | Role | Responsibilities |
|------|-----------|------|-----------------|
| Obada Abdulhakim Kharaz | 2309115277 | Project Manager | Sprint planning, milestone tracking, stakeholder communication, risk escalation, schedule performance index (SPI) monitoring, final documentation oversight |
| Mohanad Aref Ali Sultan | 2309115898 | Backend Developer | FastAPI REST API design and implementation, PostgreSQL database models, JWT authentication, Alembic migrations, health endpoints, management status endpoint |
| Zekeriya Dulli | 2309115377 | Frontend Developer | Vue.js 3 SPA implementation, Management Monitoring Dashboard, Technical Monitoring Dashboard, Risk Dashboard, component architecture, routing |
| Praise-God Tobby | 2309116418 | QA / Test Engineer | Backend pytest test suite, frontend Vitest unit tests, CI/CD pipeline quality gates, test coverage reporting, regression prevention |
| Fares Stouhi | 2309115179 | UX / UI Designer | Dashboard layout and visual design, login page UX, sidebar navigation, PrimeVue theme selection, user flow design, About Us page |
| Hamdi Alnaqeeb | 2309116178 | DevOps / Operations Engineer | Docker Compose orchestration, nginx reverse proxy and SSL configuration, GitHub Actions CI/CD pipelines, healthcheck configuration, log management |
| Abdulaziz Alyahya | 2309116441 | Risk Manager | Risk identification and register, risk scoring, stakeholder mapping, mitigation and contingency planning, monitoring of project-level risks |

---

## Table of Contents

1. Executive Summary
2. Project Scope and Objectives
3. Software Design and Analysis
4. User Interface Design
5. Management Monitoring
6. Technical Monitoring
7. Value Creation
8. Stakeholder Management
9. Risk Management
10. CI/CD and Continuous Testing
11. Conclusion

---

## 1. Executive Summary

Industry Maintenance Platform is a full-stack industrial asset management system built specifically for operational technology (OT) environments. It was designed, implemented, tested, and deployed by a seven-member team as a comprehensive demonstration of all Software Project Management course concepts.

The system provides three live monitoring dashboards — Management Monitoring, Technical Monitoring, and Risk — served over HTTPS through a four-container Docker Compose stack. The backend is a FastAPI application with 28 API endpoints secured by JWT authentication and role-based access control. The frontend is a Vue.js 3 single-page application with 31 pages. The entire infrastructure runs at zero cost using open-source tools only.

The project was managed using Earned Value Management, with weekly sprint reviews, a 14-risk register, and three-level downtime prevention. All code is under version control on GitHub with automated CI/CD pipelines running on every push.

---

## 2. Project Scope and Objectives

### 2.1 Problem Statement

Industrial facilities manage hundreds of physical assets — PLCs, HMIs, industrial switches, sensors, and servers — across operational technology networks. The core problem is not a lack of data: it is that the data is scattered.

- Asset inventories live in spreadsheets that are updated manually and are always out of date
- Risk assessments are performed by consultants every 12–18 months, not continuously
- Network topology diagrams do not reflect current configurations
- Audit trails of who changed what exist only in email threads
- When a security incident occurs, there is no authoritative record of the asset's last known-good state

The result is management under uncertainty: decisions are made without reliable, current information. This increases operational risk, extends mean time to recovery after incidents, and makes compliance audits expensive.

### 2.2 Objectives

| Objective | How It Is Met |
|-----------|--------------|
| Centralise asset data | PostgreSQL with 24 tables, validated by Pydantic schemas |
| Provide continuous risk visibility | Automated ICS risk scoring engine updating on every asset change |
| Enable management monitoring | 14 KPIs via `GET /management/status`, displayed on auto-refreshing dashboard |
| Enable technical monitoring | Live CPU, memory, disk, and database health via `GET /health/detailed` |
| Support multi-tenant operation | Every table carries `tenant_id` foreign key; data is fully isolated |
| Provide role-based access control | Admin / Editor / Viewer roles with per-resource permission tables |
| Prove zero-cost deployment | Docker Compose + GitHub Actions free tier + self-signed SSL |

### 2.3 Deliverables

- Running system accessible at `https://localhost`
- Three monitoring dashboards: `/monitoring`, `/management`, `/risk`
- Backend pytest test suite covering auth, health, and integration scenarios
- Frontend Vitest test suite with 29 assertions
- GitHub Actions CI/CD pipelines for backend and frontend
- Complete project documentation in `docs/`
- This final report

---

## 3. Software Design and Analysis

### 3.1 Architecture

Industry Maintenance Platform follows a **three-tier architecture**. The three tiers are decoupled and communicate only through defined interfaces.

```
┌───────────────────────────────────────────────────────┐
│  Browser — Vue.js 3 SPA                               │
│  Pages · Components · Composables · api.js (axios)   │
└───────────────────────────────┬───────────────────────┘
                                │ HTTPS / JSON
┌───────────────────────────────▼───────────────────────┐
│  FastAPI Backend (Python 3.11)                        │
│  Routers (28) · Pydantic Schemas · CRUD · Services   │
│  JWT Auth · RBAC · Alembic Migrations                │
└───────────────────────────────┬───────────────────────┘
                                │ SQLAlchemy ORM
┌───────────────────────────────▼───────────────────────┐
│  PostgreSQL 15                                        │
│  24 tables · multi-tenant · soft delete · indexes    │
└───────────────────────────────────────────────────────┘
```

An nginx reverse proxy sits in front of both the backend and frontend, handles SSL termination, enforces security headers, and rate-limits the login endpoint.

### 3.2 Maintainability

**Separation of concerns** is enforced at every layer:

- Each domain (assets, users, sites, suppliers, manufacturers, etc.) has its own router file, CRUD file, schema file, and model file. No domain logic leaks across boundaries.
- Services (`auth.py`, `rbac.py`, `risk_scoring.py`, `audit_log.py`) contain reusable business logic that routers call without duplicating.
- The frontend uses the Composition API (`script setup`) in every component, keeping template logic minimal and testable.
- A single `api.js` file manages all HTTP calls. No component makes direct HTTP requests.

**Soft delete** is implemented on all major entities. Deleted records carry a `deleted_at` timestamp and are excluded from queries with a filter rather than being removed from the database. This preserves data integrity and supports audit requirements.

**Alembic migrations** version every schema change. The database can be reproduced from zero to the current schema by running `alembic upgrade head`.

### 3.3 Scalability

| Concern | Design Decision |
|---------|----------------|
| Horizontal backend scaling | FastAPI is stateless; multiple backend containers can sit behind nginx with zero code changes |
| Multi-tenant isolation | `tenant_id` on every row means additional tenants add no structural changes |
| Database performance | Composite indexes on `(tenant_id, deleted_at)` on the most-queried tables |
| Frontend bundle size | Vite code-splits by route; only the page being viewed is loaded |
| API versioning | External API uses `/external/v1/` prefix; internal API can version independently |

### 3.4 Cohesion and Coupling

**High cohesion:** Each router file handles exactly one domain. `routers/assets.py` handles only assets. `routers/tenants.py` handles only tenants. No router exceeds its responsibility.

**Low coupling:** Routers depend on CRUD functions, not directly on models. CRUD functions depend on SQLAlchemy sessions, not on request or response objects. This means any layer can be replaced without touching the others.

**Dependency injection:** FastAPI's `Depends()` system provides `get_db` (database session) and `get_current_user` (authenticated user) to every endpoint that needs them. No global state is used.

### 3.5 Security Design

- All passwords are hashed with `bcrypt` via `passlib`
- JWT tokens are signed with a configurable secret key and expire in 30 minutes
- Roles and permissions are stored in the database and checked via `require_permission()` on protected endpoints
- All write endpoints require authentication; admin operations require the Admin role
- nginx adds HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Content-Security-Policy headers on every response
- Login endpoint is rate-limited to 5 requests per minute per IP address
- An immutable audit log records every CREATE, UPDATE, and DELETE with user ID, IP address, and timestamp

---

## 4. User Interface Design

### 4.1 Design Principles

The interface was designed around three principles:

1. **Clarity over density** — Each dashboard shows the most important metric as a large tile at the top, with detail further down. Users can read the system state at a glance from across the room.
2. **Live data without interaction** — All three monitoring dashboards auto-refresh automatically (Technical: 30 seconds, Management: 60 seconds, Risk: on load). No manual refresh button is needed.
3. **Consistent navigation** — A persistent sidebar provides one-click access to every section. The sidebar collapses to icons on smaller screens. A logout link is always visible at the bottom.

### 4.2 Technology

- **Framework:** Vue.js 3 with Composition API
- **Component Library:** PrimeVue 3 (lara-light-blue theme)
- **Layout:** Flexbox sidebar + scrollable main content area
- **Color mode:** Light mode with blue accent for primary actions
- **Animations:** CSS transitions on login page (slide-in, fade-in, button pulse)

### 4.3 The Three Monitoring Dashboards

#### Technical Monitoring Dashboard (`/monitoring`)

The top of the page shows a full-width status banner that is green (HEALTHY), amber (DEGRADED), or red (OFFLINE) based on the `/health/detailed` response. Below the banner:

- System resource bars: CPU %, Memory %, Disk %
- Database status: connection state and response time
- Uptime counter in seconds
- Python version and environment information

The dashboard refreshes every 30 seconds without any user action.

#### Management Monitoring Dashboard (`/management`)

Four KPI tiles at the top show: SPI (Schedule Performance Index), Sprint Velocity, Task Completion %, and Assets Managed (live from the database). Below the tiles:

- Sprint velocity bar chart across all sprints
- Team workload table with colour-coded progress bars (red when load > 95%)
- Milestone tracker showing 7 milestones from project kickoff to final submission
- Budget overview showing actual vs. allocated person-hours

The dashboard refreshes every 60 seconds.

#### Risk Dashboard (`/risk`)

Three risk KPI tiles: total risks identified, high-severity count, and open mitigations. Below the tiles:

- Risk distribution panel showing High / Medium / Low counts
- Top 5 highest-risk assets sorted by ICS risk score
- Full project risk register with 14 entries, each showing category, probability, impact, score, owner, and mitigation status

### 4.4 Additional UI Features

- **Global search** (Ctrl+K) — Spotlight-style search across all assets, sites, contacts, and suppliers with instant results
- **Floor plan integration** — Visual asset placement on site floor plans
- **XLSX import** — Bulk asset import with preview and validation before confirming
- **Print/PDF** — Asset card printing with QR codes
- **About Us page** — Lists all seven team members with names, student IDs, and roles

---

## 5. Management Monitoring

Management monitoring answers the project manager's question: **"Is the project on track and is the team healthy?"**

### 5.1 KPIs Tracked

| KPI | Formula / Source | Threshold |
|-----|-----------------|-----------|
| SPI (Schedule Performance Index) | Earned Value SP ÷ Planned Value SP | Warning below 0.90, Critical below 0.85 |
| Sprint velocity | Story points completed per sprint | Drop > 20% triggers capacity review |
| Task completion | Tasks done ÷ Tasks total | Tracked weekly per sprint |
| CPI (Cost Performance Index) | Allocated hours ÷ Actual hours | Warning below 0.90 |
| Team workload | Person-hours per member | Alert when any member exceeds 95% |
| Assets managed | Live DB count | Confirms system holds real data |

### 5.2 Sprint Plan

| Sprint | Weeks | Deliverable |
|--------|-------|-------------|
| Sprint 1 | 1–2 | Project setup, roles assigned, Docker stack running |
| Sprint 2 | 3–4 | Core asset CRUD, database schema, authentication |
| Sprint 3 | 5–6 | Management Monitoring endpoint and dashboard |
| Sprint 4 | 7–8 | Technical Monitoring endpoint and dashboard |
| Sprint 5 | 9–10 | Risk Dashboard, risk scoring engine |
| Sprint 6 | 11–12 | CI/CD pipelines, test suites |
| Sprint 7 | 13–14 | Full audit, bug fixes, documentation |
| Sprint 8 | 15–16 | Final report, presentation preparation, submission |

### 5.3 Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| Project kickoff — roles and stack defined | Week 1 | Completed |
| Database schema and auth working | Week 4 | Completed |
| Both monitoring dashboards live | Week 8 | Completed |
| CI/CD pipelines passing | Week 12 | Completed |
| Full test suite passing | Week 14 | Completed |
| Documentation complete | Week 15 | Completed |
| Final submission | Week 16 | Completed |

### 5.4 API Endpoint

`GET /management/status` returns the full management status payload in a single authenticated call. It is consumed by the Management Monitoring Dashboard, which auto-refreshes every 60 seconds.

---

## 6. Technical Monitoring

Technical monitoring answers the operations engineer's question: **"Is the system alive and healthy right now?"**

### 6.1 Three-Level Downtime Prevention

| Level | Mechanism | Response Time | Action |
|-------|-----------|--------------|--------|
| Level 1 | Docker healthcheck polls `GET /health` every 30 s | ≤ 90 s | Container restarted automatically — no human action required |
| Level 2 | Technical Monitoring Dashboard polls `GET /health/detailed` every 30 s | ≤ 30 s | Red banner appears before any user notices errors |
| Level 3 | `logs/security.log` in JSON format | Manual review | 401 spikes signal brute-force; log entries are machine-parseable |

### 6.2 Health Endpoints

#### `GET /health`
Unauthenticated. Returns:
```json
{
  "status": "ok",
  "database": "connected",
  "uptime": "running",
  "timestamp": "2026-05-05T17:47:04Z"
}
```
Used by Docker healthcheck and nginx monitoring.

#### `GET /health/detailed`
Unauthenticated. Returns:
```json
{
  "status": "healthy",
  "database": { "connected": true, "response_time_ms": 2.1 },
  "system": { "cpu_percent": 12.4, "memory_percent": 38.1, "disk_percent": 22.0 },
  "uptime_seconds": 86400,
  "python_version": "3.11.x",
  "environment": "production"
}
```
Used by the Technical Monitoring Dashboard.

### 6.3 System Resource Monitoring

`psutil 5.9.8` provides CPU, memory, and disk usage at the operating system level. These values are read on every call to `/health/detailed` — no caching — to ensure the dashboard always shows the current state.

### 6.4 Logging Architecture

| Log file | Content | Format |
|----------|---------|--------|
| `logs/app.log` | All HTTP requests at INFO level and above | Text |
| `logs/error.log` | ERROR and CRITICAL events only | Text |
| `logs/security.log` | All authentication events (login, logout, token refresh, failed attempts) | JSON (machine-parseable) |
| `audit_logs` table | Every CREATE, UPDATE, DELETE on every entity | PostgreSQL, queryable via API |

---

## 7. Value Creation

### 7.1 Problem vs. Solution

| Industrial Problem | Industry Maintenance Platform Solution |
|-------------------|----------------------------------------|
| Asset data in disconnected spreadsheets | Single PostgreSQL registry with 24 validated tables |
| Risk assessed once every 18 months | Automated ICS risk scoring on every asset change |
| No network topology visibility | Interactive network map showing all asset connections |
| Manual compliance audit preparation | Immutable audit log queryable via REST API |
| No early warning of system degradation | Technical Monitoring Dashboard with 30-second refresh |
| No project schedule visibility | Management Monitoring Dashboard with SPI and EVM |

### 7.2 Financial Value Estimate

| Category | Calculation | Annual Value |
|----------|-------------|-------------|
| Consultant risk assessment (replaced) | 2 assessments/year × €5,000 | €10,000 |
| Manual audit preparation time (reduced) | 40 hrs/audit × 2 audits × €75/hr | €6,000 |
| Downtime reduction (1 avoided incident) | 8 hrs × €1,500/hr production loss | €12,000 |
| Maintenance engineer time saved | 30 min/day × 250 days × €40/hr | €5,000 |
| Compliance fine avoidance (partial) | Estimated risk reduction | €77,000 |
| **Total Year 1 Benefit** | | **€110,000** |
| **Total Infrastructure Cost** | Docker, GitHub Actions, PostgreSQL — all free | **€0** |
| **Net Value — Year 1** | | **€110,000** |

### 7.3 Why Zero Cost

Every component of the stack is open source and free to operate:

| Component | Tool | Cost |
|-----------|------|------|
| Backend | FastAPI, Python, PostgreSQL | €0 |
| Frontend | Vue.js, Vite, PrimeVue | €0 |
| Containerisation | Docker, Docker Compose | €0 |
| CI/CD | GitHub Actions free tier | €0 |
| SSL | Self-signed certificates (openssl) | €0 |
| Hosting | Self-hosted on any server | €0 |

---

## 8. Stakeholder Management

### 8.1 Stakeholder Map

```
                   LOW INTEREST            HIGH INTEREST
                ┌──────────────────────┬──────────────────────────┐
HIGH INFLUENCE  │  KEEP SATISFIED       │  MANAGE CLOSELY          │
                │  • IT Administrator   │  • Course Instructor     │
                │  • System Owner       │  • Project Manager       │
                │                       │  • Backend Developer     │
                │                       │  • Facility Manager      │
                ├──────────────────────┼──────────────────────────┤
LOW INFLUENCE   │  MONITOR              │  KEEP INFORMED           │
                │  • Open-source users  │  • End Users             │
                │                       │  • Maintenance Team      │
                │                       │  • QA / UX / DevOps / RM│
                └──────────────────────┴──────────────────────────┘
```

### 8.2 Internal Stakeholders

| Name | Role | Key Expectation | Communication |
|------|------|----------------|---------------|
| Obada Abdulhakim Kharaz | Project Manager | All members deliver on time; SPI ≥ 0.90 | Weekly stand-up; milestone emails |
| Mohanad Aref Ali Sultan | Backend Developer | APIs are correct, tested, and documented | GitHub PRs; code review comments |
| Zekeriya Dulli | Frontend Developer | Dashboards render correctly and auto-refresh | Shared component library; PR review |
| Praise-God Tobby | QA / Test Engineer | All tests pass in CI; no regressions | CI pipeline status; test reports |
| Fares Stouhi | UX / UI Designer | UI is clean, consistent, and user-friendly | Design reviews; screenshot feedback |
| Hamdi Alnaqeeb | DevOps / Operations | Containers stay healthy; CI/CD is green | Docker logs; GitHub Actions status |
| Abdulaziz Alyahya | Risk Manager | Risks are tracked and mitigated on time | Risk register updates; weekly review |

### 8.3 External Stakeholders

| Stakeholder | Interest | Concern | Management Approach |
|-------------|---------|---------|---------------------|
| Course Instructor | Project meets all course requirements | Incomplete or shallow deliverables | Weekly progress; comprehensive documentation |
| Facility Manager (end user) | System is easy to use and reliable | Downtime; data loss | Three-level downtime prevention; audit trail |
| IT / OT Security Officer | Data is secure; access is controlled | Unauthorized access | JWT auth; RBAC; security audit log |
| Compliance Auditor | Audit trail is complete and exportable | Manual effort to collect evidence | Immutable audit log via REST API |
| Maintenance Technician | Asset lookup is fast | Slow or unavailable system | Sub-200ms search; health monitoring |

### 8.4 Communication Plan

| Channel | Frequency | Participants | Purpose |
|---------|-----------|-------------|---------|
| Weekly stand-up | Every Monday | All 7 members | Sprint review, blockers, next week plan |
| GitHub Issues | Continuous | All developers | Bug tracking and feature requests |
| GitHub Pull Requests | Per feature | Developer + reviewer | Code review and integration |
| Milestone email | Per milestone | Project Manager → Instructor | Progress reporting |
| Risk register update | Weekly | Risk Manager | Risk status and mitigation progress |

---

## 9. Risk Management

### 9.1 Risk Scoring Scale

| Score | Probability | Impact |
|-------|------------|--------|
| 1 | Very Low (< 10%) | Negligible |
| 2 | Low (10–25%) | Minor |
| 3 | Medium (25–50%) | Moderate |
| 4 | High (50–75%) | Major |
| 5 | Very High (> 75%) | Critical |

**Risk Score = Probability × Impact**

| Score Range | Level | Response |
|-------------|-------|---------|
| 1–4 | Low | Monitor |
| 5–9 | Medium | Mitigate |
| 10–16 | High | Immediate action |
| 17–25 | Critical | Escalate immediately |

### 9.2 Risk Register

| ID | Risk | Category | Probability | Impact | Score | Level | Owner | Mitigation |
|----|------|----------|------------|--------|-------|-------|-------|------------|
| R-01 | Database connection failure | Technical | 2 | 5 | 10 | High | Mohanad | Docker healthcheck auto-restarts; connection pool configured |
| R-02 | Incorrect asset data | Data | 3 | 4 | 12 | High | Mohanad | Pydantic validation on all inputs; audit log on every change |
| R-03 | Unauthorized access | Security | 2 | 5 | 10 | High | Mohanad | JWT auth; RBAC; rate limiting; security audit log |
| R-04 | Delayed implementation | Schedule | 3 | 3 | 9 | Medium | Obada | Sprint buffering; weekly SPI tracking; early escalation |
| R-05 | Cost overrun | Cost | 1 | 2 | 2 | Low | Obada | Zero-cost stack; no paid services used |
| R-06 | Weak monitoring coverage | Technical Debt | 3 | 3 | 9 | Medium | Hamdi | Three monitoring layers; 30-second health polling |
| R-07 | Broken deployment pipeline | Deployment | 2 | 4 | 8 | Medium | Hamdi | GitHub Actions CI on every push; Docker image build tested |
| R-08 | Poor user adoption | Adoption | 3 | 3 | 9 | Medium | Fares | Intuitive UI; demo data pre-loaded; Ctrl+K global search |
| R-09 | Accumulated technical debt | Technical Debt | 4 | 3 | 12 | High | Mohanad | Code review on every PR; full audit performed at Week 14 |
| R-10 | Team member unavailability | Team | 3 | 3 | 9 | Medium | Obada | Shared documentation; no single point of knowledge |
| R-11 | System downtime | Technical | 2 | 4 | 8 | Medium | Hamdi | Three-level downtime prevention; auto-restart |
| R-12 | Incomplete test coverage | Technical | 3 | 3 | 9 | Medium | Praise-God | CI blocks merge if tests fail; coverage tracked |
| R-13 | Misconfigured user roles | Security | 2 | 4 | 8 | Medium | Mohanad | RBAC enforced at API level; admin endpoints verified |
| R-14 | Poor stakeholder communication | Schedule | 2 | 3 | 6 | Medium | Obada | Weekly stand-ups; milestone emails; GitHub transparency |

### 9.3 ICS Asset Risk Scoring

Beyond project risks, the platform computes an automated risk score (0–100) for every industrial asset using the `risk_scoring.py` engine. The score is calculated from:

- **Purdue Model level** — lower-level OT assets (Level 0–1) are inherently higher risk
- **Business criticality** — Critical / High / Medium / Low
- **Physical access ease** — External / Internal / Restricted
- **Remote access type** — Unattended / Attended / None
- **Known vulnerability score** — Manual input from CVE databases

Scores update automatically whenever an asset attribute changes. No annual consultant engagement is required.

### 9.4 Risk Monitoring

- The Risk Dashboard (`/risk`) displays all 14 project risks and the top high-risk assets at all times
- Risk scores are reviewed at every weekly stand-up
- Any risk reaching score ≥ 10 triggers immediate escalation to the project manager
- Mitigation progress is logged in the GitHub Issues tracker

---

## 10. CI/CD and Continuous Testing

### 10.1 Pipeline Architecture

Every push to GitHub triggers two automated pipelines running in parallel:

**Backend Pipeline (`.github/workflows/backend.yml`)**

1. Checkout code
2. Set up Python 3.10
3. Install dependencies from `requirements.txt`
4. Start a PostgreSQL 15 service container
5. Run `pytest tests/ -v --tb=short --cov=app`
6. Report coverage

**Frontend Pipeline (`.github/workflows/frontend.yml`)**

1. Checkout code
2. Set up Node.js with `package-lock.json` cache
3. Run `npm ci`
4. Run `npm run test:unit` (Vitest — 29 assertions in 1 test file)
5. Run `npm run build` (Vite production build)

Both pipelines run on GitHub Actions free tier at zero cost.

### 10.2 Test Coverage

**Backend tests (`backend/tests/`):**

| File | What it tests |
|------|--------------|
| `test_health.py` | `/health` and `/health/detailed` responses; unauthenticated access |
| `test_auth.py` | Login success and failure; JWT token creation; invalid credentials |
| `test_users.py` | API availability; documentation endpoint |
| `test_comprehensive.py` | User CRUD; asset creation; RBAC enforcement; integration flow |

**Frontend tests (`frontend/src/composables/__tests__/useStatus.spec.js`):**

29 assertions covering:
- `getContrastColor` — correct white/black contrast for light and dark backgrounds
- `getStatusSeverity` — correct PrimeVue severity mapped from color hex values and status names
- `getStatusColor` — correct color returned for status objects with and without color fields
- `getStatusLabel` — correct label returned for null, empty, and populated status objects

---

## 11. Conclusion

Industry Maintenance Platform demonstrates every concept required by the Software Project Management & Technical Monitoring course:

| Requirement | Implementation |
|-------------|---------------|
| Software Design & Analysis | Three-tier architecture; separation of concerns; maintainability via domain-scoped routers and CRUD; scalability via stateless backend and multi-tenant database |
| UI Design | Three monitoring dashboards; PrimeVue component library; auto-refreshing data; responsive sidebar navigation; Ctrl+K global search |
| Value Creation | €110,000 estimated Year 1 benefit at €0 infrastructure cost; replaces manual spreadsheets, consultant assessments, and manual audit preparation |
| Stakeholder Management | 7 internal stakeholders with defined roles; 5 external stakeholder categories; structured communication plan; stakeholder influence/interest map |
| Risk Management | 14-risk register with probability × impact scoring; ICS automated asset risk scoring; three-level technical downtime prevention |
| Management Monitoring | SPI, CPI, sprint velocity, task completion, and team workload tracked via live dashboard at `/management` |
| Technical Monitoring | CPU, memory, disk, database health, and uptime tracked via live dashboard at `/monitoring` with 30-second refresh |
| CI/CD | GitHub Actions backend and frontend pipelines on every push; pytest + Vitest; production build verification |

The system runs end-to-end on any machine with Docker Desktop in under 5 minutes, at zero cost, with no external paid services. All code, tests, documentation, and pipelines are available at:

**https://github.com/3bada66/industry-maintenance-platform-clean**

---

*Prepared by the Industry Maintenance Platform Team — Istinye University, 2026*
