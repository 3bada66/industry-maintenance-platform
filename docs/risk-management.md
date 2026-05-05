# Risk Management
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.1
**Owner:** Abdulaziz Alyahya (Risk Manager, 2309116441)
**Reviewed by:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)

---

## 1. Risk Identification

### 1.1 Context

Industry Maintenance Platform is an industrial monitoring platform that manages assets mapped against the Purdue Model, tracks risk scores for industrial control system (ICS) components, and provides technical and management monitoring dashboards. Its risk profile is therefore shaped by two distinct concerns:

1. **Platform risks** — technical, security, and operational risks that affect the running system and its users (plant managers, maintenance technicians, IT security officers, compliance auditors).
2. **Project risks** — schedule, team, cost, and quality risks that affect the course project's ability to deliver a working, documented system by Week 16.

Both categories are managed in this document.

### 1.2 Risk Categories

| Code | Category | Description |
|------|----------|-------------|
| **TECH** | Technical Risk | Failures in infrastructure, code, integrations, or monitoring coverage |
| **SCHED** | Schedule Risk | Delays that threaten milestones or the final submission deadline |
| **COST** | Cost Risk | Unexpected resource expenditure that was not planned |
| **SEC** | Security Risk | Unauthorized access, privilege misuse, or data exposure |
| **DATA** | Data Risk | Corruption, inaccuracy, or loss of asset or operational data |
| **DEPLOY** | Deployment Risk | Failures in CI/CD pipeline, container builds, or production deployment |
| **ADOPT** | User Adoption Risk | Users failing to engage with or trust the platform correctly |
| **TEAM** | Team Availability Risk | Loss of contributor capacity affecting delivery |
| **DEBT** | Technical Debt Risk | Accumulated shortcuts that degrade maintainability or monitoring fidelity |

### 1.3 Scoring Scale

| Score | Probability | Impact |
|-------|------------|--------|
| 1 | Very Low (< 10 %) | Negligible — no visible effect |
| 2 | Low (10–25 %) | Minor — small rework or delay |
| 3 | Medium (25–50 %) | Moderate — sprint impacted |
| 4 | High (50–75 %) | Major — milestone at risk |
| 5 | Very High (> 75 %) | Critical — project or system failure |

**Risk Score = Probability × Impact**

| Score | Level | Response |
|-------|-------|---------|
| 1–4 | 🟢 Low | Monitor |
| 5–9 | 🟡 Medium | Mitigate |
| 10–16 | 🔴 High | Immediate action required |
| 17–25 | 🔴 Critical | Escalate immediately |

---

## 2. Risk Assessment

Full risk register for the Industry Maintenance Platform industrial monitoring platform.

| ID | Risk | Category | Probability | Impact | Score | Level | Owner |
|----|------|----------|------------|--------|-------|-------|-------|
| R-01 | Database connection failure | TECH | 2 | 5 | 10 | 🔴 High | Mohanad Aref Ali Sultan |
| R-02 | Incorrect asset data | DATA | 3 | 4 | 12 | 🔴 High | Mohanad Aref Ali Sultan |
| R-03 | Unauthorized access | SEC | 2 | 5 | 10 | 🔴 High | Mohanad Aref Ali Sultan |
| R-04 | Delayed implementation | SCHED | 3 | 3 | 9 | 🟡 Medium | Obada Abdulhakim Kharaz |
| R-05 | Cost overrun | COST | 1 | 2 | 2 | 🟢 Low | Obada Abdulhakim Kharaz |
| R-06 | Weak monitoring coverage | DEBT | 3 | 3 | 9 | 🟡 Medium | Hamdi Alnaqeeb |
| R-07 | Broken deployment pipeline | DEPLOY | 2 | 4 | 8 | 🟡 Medium | Hamdi Alnaqeeb |
| R-08 | Poor user adoption | ADOPT | 3 | 3 | 9 | 🟡 Medium | Fares Stouhi |
| R-09 | Accumulated technical debt | DEBT | 4 | 3 | 12 | 🔴 High | Mohanad Aref Ali Sultan |
| R-10 | Team member unavailability | TEAM | 3 | 3 | 9 | 🟡 Medium | Obada Abdulhakim Kharaz |
| R-11 | System downtime | TECH | 2 | 4 | 8 | 🟡 Medium | Hamdi Alnaqeeb |
| R-12 | Incomplete test coverage | TECH | 3 | 3 | 9 | 🟡 Medium | Praise-God Tobby |
| R-13 | Misconfigured user roles | SEC | 2 | 4 | 8 | 🟡 Medium | Mohanad Aref Ali Sultan |
| R-14 | Poor stakeholder communication | SCHED | 2 | 3 | 6 | 🟡 Medium | Obada Abdulhakim Kharaz |

---

## 3. Risk Mitigation

Each risk entry below follows the full structure:

> **Risk | Category | Impact | Probability | Mitigation | Owner | Monitoring Method**

---

### R-01 — Database Connection Failure

| Field | Detail |
|-------|--------|
| **Category** | Technical Risk |
| **Impact** | 5 — Critical. All API endpoints that read or write assets, audit logs, and risk scores become unavailable. The monitoring dashboards show `"database": "disconnected"`. |
| **Probability** | 2 — Low. PostgreSQL 15 is stable; Docker health checks restart the container automatically on failure. |
| **Risk Score** | 10 — High |
| **Mitigation** | PostgreSQL container has a Docker `healthcheck` (`pg_isready` every 10 s, 5 retries). The connection pool is limited to 20 connections to prevent pool exhaustion. `GET /health` performs a live `SELECT 1` and returns `"database": "disconnected"` immediately if the DB is unreachable, so the monitoring dashboard detects the failure before users do. Alembic migrations are tested on a dev DB before production applies. DB backup scripts are in `scripts/backup.py`. |
| **Contingency** | Stop all containers (`make stop`), restore from last backup (`scripts/restore.py`), restart with `make prod`, verify with `curl /health`. |
| **Owner** | Mohanad Aref Ali Sultan (Backend Developer) |
| **Monitoring Method** | `GET /health` endpoint → `"database"` field; `GET /health/detailed` → `components.database.status` and `response_time_ms`; Docker container health status in `docker ps`; daily backup verification. |

---

### R-02 — Incorrect Asset Data

| Field | Detail |
|-------|--------|
| **Category** | Data Risk |
| **Impact** | 4 — High. Inaccurate asset records (wrong Purdue level, incorrect IP, stale firmware version) produce misleading risk scores. A plant manager making maintenance decisions based on wrong data could prioritise the wrong assets. |
| **Probability** | 3 — Medium. Data is entered manually by technicians; human error is expected. |
| **Risk Score** | 12 — High |
| **Mitigation** | All asset write operations are validated by Pydantic schemas before reaching the database — mandatory fields (name, asset type, site) cannot be omitted. Every CREATE, UPDATE, and DELETE is recorded in the immutable `audit_logs` table with a before/after diff, making incorrect entries detectable and reversible. The Risk Scoring engine (`services/risk_scoring.py`) validates Purdue level against a controlled enum — invalid values are rejected with HTTP 422. CSV import templates (`public/template_import_asset.csv`) include field descriptions to reduce entry errors. |
| **Contingency** | Auditor uses `GET /api/v1/audit-logs/` to identify incorrect entries by timestamp and user ID. An admin corrects the record; the correction itself is logged. |
| **Owner** | Mohanad Aref Ali Sultan (Backend Developer) |
| **Monitoring Method** | Audit trail review at each sprint; 422 error rate in application logs; manual data quality spot-check by QA (Praise-God Tobby) at sprint end. |

---

### R-03 — Unauthorized Access

| Field | Detail |
|-------|--------|
| **Category** | Security Risk |
| **Impact** | 5 — Critical. Unauthorized access to an industrial asset inventory exposes network topology, IP addresses, firmware versions, and physical locations — intelligence that could enable targeted ICS attacks. |
| **Probability** | 2 — Low. JWT + RBAC is enforced on all API endpoints except `/health` and `/login`. |
| **Risk Score** | 10 — High |
| **Mitigation** | JWT HS256 tokens with configurable expiry; refresh token rotation. Three roles (Admin / Editor / Viewer) enforced via `services/rbac.py` dependency injection. Multi-tenant data isolation: every DB query filters by `tenant_id` derived from the authenticated token — a tenant cannot read another tenant's assets even with a valid JWT. Rate limiting via `slowapi`: 100 req/hour global, 10/min on auth endpoints to block brute force. HTML input sanitisation with `bleach`. HTTPS/TLS in production via Nginx with self-signed or Let's Encrypt certificates. All auth events (login, logout, token refresh, failed auth) are written to `logs/security.log` in JSON format. |
| **Contingency** | Revoke compromised JWT secret (`SECRET_KEY` rotation in `.env`), force all users to re-login, review `security.log` for scope of breach, notify affected tenant administrators. |
| **Owner** | Mohanad Aref Ali Sultan (Backend Developer) |
| **Monitoring Method** | `logs/security.log` (all auth events); 401 rate in application logs — alert if > 20/min (possible brute force); OWASP checklist completed at code freeze (Week 13); GitHub Dependabot for CVE alerts on `PyJWT`, `FastAPI`, `python-jose`. |

---

### R-04 — Delayed Implementation

| Field | Detail |
|-------|--------|
| **Category** | Schedule Risk |
| **Impact** | 3 — Moderate. Missing a sprint milestone delays downstream deliverables. Delayed Week 16 submission = no grade. |
| **Probability** | 3 — Medium. 7-person student team with concurrent academic obligations. |
| **Risk Score** | 9 — Medium |
| **Mitigation** | 4 sprints × 3 weeks, each with defined story points and a milestone acceptance gate. A 2-week buffer (Weeks 14–15) exists explicitly for documentation and fixing slippage. Weekly Monday stand-ups track blockers. Sprint velocity is measured each sprint and compared to plan (target SPI ≥ 0.90). Code freeze enforced from Week 11 to protect documentation time. RACI matrix ensures every task has a named owner and backup. |
| **Contingency** | If SPI drops below 0.85, PM (Obada) calls an emergency scope review. Low-priority features are moved to `backlog` status and documented as "planned (future)" — they do not block submission. |
| **Owner** | Obada Abdulhakim Kharaz (Project Manager) |
| **Monitoring Method** | Weekly stand-up blocker list; sprint burndown (story points remaining vs planned); SPI tracked in Management Monitoring dashboard (`GET /api/v1/management/status`); milestone acceptance checklist reviewed by PM and Backend Lead at each milestone gate. |

---

### R-05 — Cost Overrun

| Field | Detail |
|-------|--------|
| **Category** | Cost Risk |
| **Impact** | 2 — Minor. The entire infrastructure stack is free and open-source (€0). The only real cost is team time. |
| **Probability** | 1 — Very Low. No paid services are used. All tools (GitHub Actions, Docker, PostgreSQL, pytest, Vitest, Cypress, Nginx) are free. |
| **Risk Score** | 2 — Low |
| **Mitigation** | Deliberately chosen free-only technology stack. GitHub Actions free tier (2,000 min/month for private repos) is sufficient for CI. If a paid tool is proposed, PM must approve it explicitly and document the business case. |
| **Contingency** | Replace with a free alternative if a formerly free tool introduces pricing. |
| **Owner** | Obada Abdulhakim Kharaz (Project Manager) |
| **Monitoring Method** | PM reviews tool list at each sprint start; cost tracking table in Management Monitoring dashboard shows €0 actual cost and flags any deviation. |

---

### R-06 — Weak Monitoring Coverage

| Field | Detail |
|-------|--------|
| **Category** | Technical Debt Risk |
| **Impact** | 3 — Moderate. An industrial platform with gaps in monitoring cannot satisfy the course requirement for "technical monitoring" and may miss real operational failures in deployment. |
| **Probability** | 3 — Medium. Monitoring dashboards were added late (Sprint 3); gaps could exist. |
| **Risk Score** | 9 — Medium |
| **Mitigation** | Two monitoring endpoints: `GET /health` (basic liveness probe with DB check) and `GET /health/detailed` (CPU, memory, disk, DB pool, uptime). Technical Monitoring Dashboard auto-refreshes every 30 s and displays all 10 defined metrics (see `docs/monitoring-metrics.md`). Management Monitoring Dashboard (`/management`) covers project-level metrics. Docker container health checks act as a second monitoring layer independent of the application. CI pipeline failure is treated as a monitoring event (P2-High). Alert thresholds table is displayed on the Technical Monitoring Dashboard. |
| **Contingency** | If a metric is found missing from the dashboards, add it to the relevant endpoint and update `docs/monitoring-metrics.md` before the final submission. |
| **Owner** | Hamdi Alnaqeeb (DevOps/Operations Engineer) |
| **Monitoring Method** | Manual review of `docs/monitoring-metrics.md` against the running dashboard at each sprint end; Praise-God verifies all 10 metrics are accessible and accurate before code freeze. |

---

### R-07 — Broken Deployment Pipeline

| Field | Detail |
|-------|--------|
| **Category** | Deployment Risk |
| **Impact** | 4 — High. A broken pipeline blocks all future deployments and makes it impossible to demo the live system to the course examiner. |
| **Probability** | 2 — Low. Pinned Docker image versions and `npm ci` (not `npm install`) make the pipeline deterministic. |
| **Risk Score** | 8 — Medium |
| **Mitigation** | Docker images use pinned version tags (`postgres:15`, `python:3.10-slim`, `node:18-alpine`) — never `:latest`. `backend.yml` and `frontend.yml` GitHub Actions workflows run on every push; both must pass before a PR can merge. `npm ci` uses exact versions from `package-lock.json`. `make prod` is tested end-to-end before each sprint milestone. Rollback procedure is documented in `docs/ci-cd-testing.md §3.3`. |
| **Contingency** | `git checkout <last-good-tag>` and `make prod` to restore previous known-good deployment. CI pipeline failure is treated as P2 and must be resolved before the next sprint ends. |
| **Owner** | Hamdi Alnaqeeb (DevOps/Operations Engineer) |
| **Monitoring Method** | GitHub Actions status badges in README; CI status checked at every PR; smoke tests (`curl /health`) run after every `make prod`; `docker ps` container health verified post-deployment. |

---

### R-08 — Poor User Adoption

| Field | Detail |
|-------|--------|
| **Category** | User Adoption Risk |
| **Impact** | 3 — Moderate. If simulated stakeholder personas (plant manager, maintenance technician, procurement) would not realistically use the platform, the course examiner may question the value creation argument. |
| **Probability** | 3 — Medium. Industrial asset management tools often have steep learning curves. |
| **Risk Score** | 9 — Medium |
| **Mitigation** | UX/UI Designer (Fares Stouhi) designed dashboards around the three primary user stories identified in stakeholder analysis. Global spotlight search (Cmd+K) allows technicians to find assets by serial number or location in < 200 ms. Mobile-responsive layout documented in `docs/ui-dashboard-design.md`. Default demo data (`make demo`) seeds 8 realistic assets, 3 sites, 4 manufacturers, and network topology so evaluators can explore a populated system immediately. Sidebar navigation is collapsed-capable for dense information environments. |
| **Contingency** | If UX feedback suggests a workflow is unclear, add a tooltip or inline help text — small changes that don't require architectural rework. |
| **Owner** | Fares Stouhi (UX/UI Designer) |
| **Monitoring Method** | Simulated usability review against the 3 user stories at Sprint 2 and Sprint 4 review; examiner walkthrough in presentation covers the primary user journeys end-to-end. |

---

### R-09 — Accumulated Technical Debt

| Field | Detail |
|-------|--------|
| **Category** | Technical Debt Risk |
| **Impact** | 3 — Moderate. Unaddressed technical debt makes the codebase harder to document accurately, slows Sprint 4 QA, and creates a gap between documentation claims and actual code behaviour. |
| **Probability** | 4 — High. 4-sprint project with 7 contributors and a wide feature set creates inevitable shortcuts. |
| **Risk Score** | 12 — High |
| **Mitigation** | Code freeze from Week 11 stops new feature additions and forces quality focus. Sprint 4 is explicitly allocated to QA, refactoring, and coverage improvement (target: ≥ 70 % backend, ≥ 60 % frontend). All PRs require at least one review from a second team member before merge. Known shortcuts are documented as GitHub issues labelled `tech-debt` and triaged in Sprint Retrospective. `TODO` and `FIXME` comments are tracked in the sprint backlog, not left as permanent dead weight. |
| **Contingency** | If tech debt prevents accurate documentation, document the deviation explicitly rather than misrepresenting the system state. |
| **Owner** | Mohanad Aref Ali Sultan (Backend Developer) |
| **Monitoring Method** | `pytest-cov` coverage report in every CI run; Sprint Retrospective tech debt triage; PR review gate (no self-merge); code complexity review at architecture review sessions (Weeks 2, 8, 13). |

---

### R-10 — Team Member Unavailability

| Field | Detail |
|-------|--------|
| **Category** | Team Availability Risk |
| **Impact** | 3 — Moderate. A team member missing for ≥ 1 week creates a gap in the sprint's story point delivery and may stall their assigned documentation sections. |
| **Probability** | 3 — Medium. A 7-person student team over 16 weeks will encounter illness, exam periods, and personal commitments. |
| **Risk Score** | 9 — Medium |
| **Mitigation** | RACI matrix ensures every critical task has a named backup. No "single-point-of-knowledge" silos: all code is reviewed by at least one other team member (GitHub PR process). Documentation is written incrementally each sprint, not at the end — so if a member is unavailable in Week 15, their sections are already 80 % complete. 2-week schedule buffer (Weeks 14–15) absorbs up to 1 week of team capacity loss. Weekly stand-ups surface capacity issues early. |
| **Contingency** | PM (Obada) redistributes the blocked tasks to available team members from the backup column of the RACI matrix. If more than 2 members are unavailable simultaneously, escalate to course supervisor per the Stakeholder Management Plan. |
| **Owner** | Obada Abdulhakim Kharaz (Project Manager) |
| **Monitoring Method** | Weekly stand-up attendance and blockers; sprint burndown rate (drop in velocity signals capacity issue); PM tracks task assignment status in sprint board. |

---

### R-11 — System Downtime

| Field | Detail |
|-------|--------|
| **Category** | Technical Risk |
| **Impact** | 4 — High. An industrial monitoring platform that is itself unavailable during a demo or evaluation is a direct failure of its purpose. Downtime also means assets are unmonitored. |
| **Probability** | 2 — Low. Docker Compose with `restart: unless-stopped` and health checks provides automatic recovery from transient failures. |
| **Risk Score** | 8 — Medium |
| **Mitigation** | All services (backend, frontend/Nginx, PostgreSQL) have Docker health checks. `restart: unless-stopped` policy restarts crashed containers automatically. Uptime target: 99.5 % for the backend per sprint. `GET /health/detailed` exposes `uptime_seconds` for tracking. Nginx serves the frontend independently of the backend — even if the API is down, users can reach the login page. Rate limiting prevents traffic spikes from causing self-inflicted downtime. |
| **Contingency** | `docker logs industry-maintenance-platform_backend` to diagnose; `make stop && make prod` to perform a clean restart. If data corruption is suspected, restore from backup before restarting. |
| **Owner** | Hamdi Alnaqeeb (DevOps/Operations Engineer) |
| **Monitoring Method** | Docker container health in `docker ps`; `GET /health` liveness probe every 30 s from the Technical Monitoring Dashboard; `uptime_seconds` field in `/health/detailed`; alert if `/health` returns non-200 for 2 consecutive minutes (P1-Critical per alert rules). |

---

### R-12 — Incomplete Test Coverage

| Field | Detail |
|-------|--------|
| **Category** | Technical Risk |
| **Impact** | 3 — Moderate. Undetected regressions ship to the demo environment and undermine the claim that the CI/CD pipeline is a quality gate. The course examiner expects evidence of continuous testing. |
| **Probability** | 3 — Medium. Monitoring endpoints, risk scoring, and auth flows are complex; coverage gaps are likely in early sprints. |
| **Risk Score** | 9 — Medium |
| **Mitigation** | Coverage targets enforced in CI: ≥ 70 % backend (`pytest-cov`), ≥ 60 % frontend (Vitest). Four backend test suites: `test_auth.py`, `test_users.py`, `test_comprehensive.py`, `test_health.py` (16 tests covering both health endpoints). CI runs `pytest --cov=app tests/ -v` on every push against a real PostgreSQL 15 instance — no mocked DB. Sprint 4 is dedicated to closing coverage gaps. Coverage report is advisory (does not block merge) but is reviewed in every sprint retrospective. |
| **Contingency** | If coverage drops below target before code freeze, QA (Praise-God) calls a test sprint — no new features until coverage is restored. |
| **Owner** | Praise-God Tobby (QA/Test Engineer) |
| **Monitoring Method** | `pytest-cov` XML report in every CI run; coverage percentage visible in GitHub Actions log; Praise-God reviews the coverage delta at each sprint end; coverage badge in README. |

---

### R-13 — Misconfigured User Roles

| Field | Detail |
|-------|--------|
| **Category** | Security Risk |
| **Impact** | 4 — High. In an industrial asset inventory, a Viewer-level technician granted Editor or Admin privileges could accidentally delete assets, corrupt the audit trail, or expose data to unauthorised parties. |
| **Probability** | 2 — Low. Roles are seeded with correct permissions by `init_roles.py` on first startup; the role schema is versioned in Alembic migrations. |
| **Risk Score** | 8 — Medium |
| **Mitigation** | RBAC is enforced server-side via `services/rbac.py` dependency injection on every protected endpoint — the frontend role display is cosmetic only and cannot bypass server enforcement. Role definitions (Admin / Editor / Viewer) and their permission sets are documented in `docs/ARCHITECTURE_DESIGN.md`. The `update_roles_permissions.py` migration script updates permissions deterministically on deployment. Auth tests (`test_auth.py`) include `test_viewer_cannot_delete_asset()` to prevent privilege escalation regressions. |
| **Contingency** | Admin uses `GET /api/v1/roles/` to audit role assignments. Role permissions can be corrected via `PUT /api/v1/roles/{id}` (Admin only) without downtime. |
| **Owner** | Mohanad Aref Ali Sultan (Backend Developer) |
| **Monitoring Method** | Auth test suite (`test_auth.py`) in every CI run; audit logs capture all role changes; 403 rate in application logs — spike may indicate misconfiguration; manual role audit by IT Security persona (ES-3) at each milestone. |

---

### R-14 — Poor Stakeholder Communication

| Field | Detail |
|-------|--------|
| **Category** | Schedule Risk |
| **Impact** | 3 — Moderate. If the course examiner's expectations diverge from the team's implementation, the project may satisfy requirements that were misunderstood while failing requirements that were not communicated clearly. |
| **Probability** | 2 — Low. Communication plan is documented; the examiner is the single real external stakeholder. |
| **Risk Score** | 6 — Medium |
| **Mitigation** | Communication plan in `docs/STAKEHOLDER_MANAGEMENT.md §3` defines message type, channel, frequency, and owner for each audience. Formal email + submitted docs to the examiner at each milestone (Weeks 3, 8, 14, 16). All project documents are version-controlled in `docs/` and submitted as a package at Week 16. Feedback is logged in the Stakeholder Feedback Log (section 6 of the stakeholder doc) and actioned in the following sprint. |
| **Contingency** | If a misunderstanding is discovered late (Week 13+), Obada sends an urgent clarification email and adjusts scope within the buffer weeks. |
| **Owner** | Obada Abdulhakim Kharaz (Project Manager) |
| **Monitoring Method** | Milestone delivery checklist reviewed against examiner requirements; feedback log updated after each stakeholder interaction; Abdulaziz (Risk Manager) flags communication gaps during weekly stand-up risk review. |

---

## 4. Risk Monitoring

### 4.1 Monitoring Schedule

| Activity | Frequency | Owner | Method |
|----------|-----------|-------|--------|
| Full risk register review | Weekly (Monday stand-up) | Obada | Manual review against this document |
| Database connectivity check | Every 30 seconds (automated) | Hamdi | `GET /health` → `"database"` field |
| Container health check | Every 30 seconds (automated) | Hamdi | `docker ps` health status |
| CI pipeline status | Every push (automated) | Hamdi | GitHub Actions `backend.yml` + `frontend.yml` |
| Auth anomaly detection | Continuous (automated) | Mohanad | 401 rate in `logs/security.log` |
| Test coverage review | Every sprint end | Praise-God | `pytest-cov` report in CI |
| Security dependency scan | Every sprint start | Mohanad | `pip-audit` + `npm audit` |
| DB migration check | Every deployment | Mohanad | `alembic current` matches latest revision |
| Uptime tracking | Continuous (automated) | Hamdi | `uptime_seconds` in `/health/detailed` |
| Scope creep check | Every sprint planning | Obada | Story point delta vs baseline |
| Stakeholder feedback review | Per milestone | Obada | Email + feedback log in `STAKEHOLDER_MANAGEMENT.md` |
| Technical debt triage | Every sprint retrospective | Mohanad | PR review backlog + TODO/FIXME count |

### 4.2 Risk Dashboard Integration

Three monitoring surfaces expose risk-relevant signals at runtime:

| Dashboard | URL | Relevant Risks |
|-----------|-----|---------------|
| Technical Monitoring | `/monitoring` | R-01, R-07, R-11 (DB, deployment, downtime) |
| Management Monitoring | `/management` | R-04, R-05, R-06, R-10 (schedule, cost, coverage, team) |
| Audit Logs Page | `/audit-logs` | R-02, R-03, R-13 (data quality, access, roles) |

### 4.3 Risk Status Summary

| ID | Risk | Current Score | Current Status |
|----|------|--------------|----------------|
| R-01 | Database connection failure | 10 | Active — Docker health checks in place |
| R-02 | Incorrect asset data | 12 | Active — audit trail and validation in place |
| R-03 | Unauthorized access | 10 | Mitigated — OWASP checklist completed |
| R-04 | Delayed implementation | 9 | Active — SPI 0.96 (on track) |
| R-05 | Cost overrun | 2 | Closed — €0 infrastructure confirmed |
| R-06 | Weak monitoring coverage | 9 | Active — both dashboards implemented |
| R-07 | Broken deployment pipeline | 8 | Mitigated — CI pipeline operational |
| R-08 | Poor user adoption | 9 | Active — UX review in Sprint 4 |
| R-09 | Accumulated technical debt | 12 | Active — Sprint 4 QA sprint in progress |
| R-10 | Team member unavailability | 9 | Active — buffer weeks built in |
| R-11 | System downtime | 8 | Mitigated — Docker restart + health checks |
| R-12 | Incomplete test coverage | 9 | Active — coverage target ≥ 70 % enforced in CI |
| R-13 | Misconfigured user roles | 8 | Mitigated — RBAC enforced server-side |
| R-14 | Poor stakeholder communication | 6 | Active — communication plan followed |

### 4.4 Risk Closure Criteria

A risk is marked **Closed** when at least one of the following is true:

- The triggering condition is permanently eliminated (e.g., code freeze closes scope creep)
- The sprint during which the risk was relevant has ended without it materialising
- A permanent mitigation has been implemented, verified in CI, and documented

**Residual risk acceptance:** Risks with a score ≤ 4 that have been actively mitigated are accepted without further action.

### 4.5 Escalation Path

| Condition | Action | Escalation Target |
|-----------|--------|-------------------|
| Any R-01 or R-11 event (DB down / container crash) | Immediate restart + root cause analysis | Hamdi → Obada |
| R-03 or R-13 event (security breach or role misuse) | Revoke tokens, audit logs review | Mohanad → Obada → Course Supervisor if data breach |
| SPI drops below 0.85 | Emergency scope review; defer low-priority features | Obada → Team |
| Coverage drops below target at code freeze | Test sprint; no new code until target met | Praise-God → Obada |
| Team member drops out permanently | Redistribute via RACI; notify course supervisor | Obada → Course Supervisor (ES-1) |
