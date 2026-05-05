# Value Creation
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.1
**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)
**Supporting:** Abdulaziz Alyahya (Risk Manager, 2309116441)

---

## 1. Problem Statement

Industrial facilities — manufacturing plants, energy infrastructure, water treatment, and critical infrastructure — manage hundreds to thousands of physical assets: PLCs, HMIs, switches, sensors, historians, and servers. These assets are interconnected across operational technology (OT) networks structured by the Purdue Model.

The problem is not that organisations lack data about their assets — it is that the data is scattered:

- Asset inventories live in spreadsheets that are updated manually and are always out of date
- Risk assessments are performed by consultants every 12–18 months, not continuously
- Network topology diagrams are drawn in Visio and do not reflect current cable runs
- Audit trails of who changed what configuration exist only in email threads
- When a security incident occurs, there is no authoritative record of the asset's last known-good state

The result is **management under uncertainty**: plant managers make maintenance and security decisions without reliable, current information. This increases operational risk, extends mean time to recovery (MTTR) after incidents, and makes compliance audits expensive and slow.

---

## 2. Who Benefits

| Beneficiary | Before Industry Maintenance Platform | After Industry Maintenance Platform |
|------------|-------------------|-----------------|
| **Plant / Facility Manager** | Manually assembles asset status from emails, spreadsheets, and site visits | Single dashboard shows all assets, risk scores, and system health — refreshed automatically |
| **IT / OT Security Officer** | Audit evidence collected manually before each compliance review | Immutable audit trail in PostgreSQL; exportable via API; every change logged with user, timestamp, and diff |
| **Maintenance Technician** | Looks up asset info in shared spreadsheets; takes paper notes on-site | Searches by serial number, location, or IP in < 200 ms; uploads photos and maintenance notes from any device |
| **Procurement / Supply Chain** | Tracks supplier and warranty data separately from asset data | Asset detail page links manufacturer, supplier, purchase date, and warranty expiry in one view |
| **Compliance Auditor** | Manually requests log data from multiple systems | `GET /api/v1/audit-logs/` returns a complete, filterable, append-only audit trail |
| **Course Instructor / Examiner** | Evaluates project documentation alone | Evaluates a running system demonstrating all course concepts: CI/CD, monitoring, risk management, value creation |

---

## 3. What Problems the System Solves

### 3.1 Scattered and Stale Asset Data → Centralised, Validated Registry

Industry Maintenance Platform provides a structured PostgreSQL database of 21 data models covering assets, interfaces, connections, sites, areas, locations, manufacturers, suppliers, contacts, and documents. All data is validated by Pydantic schemas before writing. CSV bulk import templates reduce manual entry effort for initial data migration.

**Value delivered:** One authoritative source of truth instead of 5–10 disconnected spreadsheets.

### 3.2 No Continuous Risk Assessment → Automated ICS Risk Scoring

The `services/risk_scoring.py` engine computes a risk score for every asset based on:
- Purdue Model level (OT assets at lower levels = higher risk)
- Business criticality
- Physical access ease
- Remote access type
- Known vulnerability score

Scores update automatically when asset attributes change. The Risk Dashboard (`/`) shows the top high-risk assets without any manual consultant input.

**Value delivered:** Continuous risk awareness instead of a point-in-time assessment every 18 months.

### 3.3 No Audit Trail → Immutable Change Log

Every CREATE, UPDATE, and DELETE on any entity is recorded in the `audit_logs` PostgreSQL table with the user ID, tenant ID, IP address, timestamp, and a before/after diff. Audit logs are never deleted or modified by the application. They are accessible via a filterable UI page and a REST API endpoint.

**Value delivered:** Compliance-ready audit evidence without manual log collection.

### 3.4 No Operational Monitoring → Live Technical Monitoring Dashboard

`GET /health` and `GET /health/detailed` expose database connectivity, uptime, CPU, memory, disk, and connection pool status. The Technical Monitoring Dashboard at `/monitoring` polls these endpoints every 30 seconds and displays the data with colour-coded status indicators and alert threshold tables.

**Value delivered:** System failures are detected before users notice them, reducing MTTR.

### 3.5 No Project Visibility → Management Monitoring Dashboard

`GET /api/v1/management/status` exposes sprint progress, SPI, team workload, milestone status, and the live asset count from the database. The Management Monitoring Dashboard at `/management` renders this as KPI tiles, sprint velocity bars, a milestone timeline, and a team workload table.

**Value delivered:** The project manager can see schedule health and team capacity without querying each team member individually.

---

## 4. How the System Reduces Manual Work

| Manual Task (Before) | Automated or Structured Alternative (After) | Time Saved (Estimate) |
|---------------------|--------------------------------------------|-----------------------|
| Monthly asset spreadsheet update | Assets updated in real time via web UI or CSV import | ~4 h/month per site |
| Quarterly risk assessment with external consultant | Continuous automated risk scoring in `risk_scoring.py` | ~1–2 days per assessment cycle |
| Manual audit log collection before compliance review | `GET /api/v1/audit-logs/` returns complete filterable export | ~1 day per review |
| Network topology diagram update in Visio | Interactive network map (`/network-map`) updated when connections change | ~2 h per topology change |
| Manual health checks by pinging servers | `GET /health/detailed` checked automatically every 30 s | Eliminates reactive manual checks |
| Searching multiple spreadsheets for one asset | Global spotlight search (Cmd+K) returns results in < 200 ms | Minutes to seconds per lookup |

*All estimates are illustrative. Actual savings depend on facility size and current process maturity.*

---

## 5. How It Improves Visibility

**Technical visibility:** The `/monitoring` dashboard surfaces 10 defined metrics — database status, response time, CPU, memory, disk, uptime, error rate, audit activity, deployment status, and crash count — in a single view. System operators know the state of the platform without SSH access to the server.

**Asset visibility:** Every asset is linked to its site, area, location, interfaces, connections, photos, documents, contacts, risk score, and change history. A plant manager can answer "what assets do I have at Site B, what is their risk score, and what changed last week" in three clicks.

**Risk visibility:** The Risk Dashboard shows the distribution of risk scores across all assets, highlights the top high-risk items, and links directly to their detail pages. Risk trends over time are visible via the time-series chart (Sprint 3 deliverable).

**Project visibility:** The Management Monitoring Dashboard shows the current sprint's SPI, story points earned vs planned, team workload per member, and the milestone timeline — all on one page.

---

## 6. How It Reduces Operational and Technical Risk

| Risk Reduced | Mechanism |
|-------------|-----------|
| Undetected misconfigured ICS assets | Purdue-level risk scoring flags assets at vulnerable levels |
| Privilege escalation by internal users | RBAC enforced server-side; role changes are audit-logged |
| Stale asset records leading to wrong maintenance | Pydantic validation prevents incomplete records; audit trail shows last change |
| Data loss from DB failure | PostgreSQL ACID transactions; backup scripts in `scripts/backup.py`; Docker health check restarts container |
| Compliance audit failure | Immutable `audit_logs` table with user, timestamp, and diff for every action |
| Undetected software vulnerabilities | GitHub Dependabot alerts on CVEs; `pip-audit` and `npm audit` at each sprint start |
| Deployment breaking production | Pinned Docker image versions; CI quality gate on every PR; rollback documented in `docs/ci-cd-testing.md §3.3` |

---

## 7. How Technical Monitoring Prevents Downtime

The Technical Monitoring layer provides **early warning** at three levels:

**Level 1 — Container health (Docker)**
Docker `healthcheck` pings `/health` every 30 seconds. If the backend fails to respond 3 times consecutively, Docker marks the container `unhealthy` and `restart: unless-stopped` restarts it automatically — typically within 60–90 seconds, without human intervention.

**Level 2 — Endpoint monitoring (Dashboard)**
The Technical Monitoring Dashboard polls `/health/detailed` every 30 seconds. A `degraded` or `unhealthy` status triggers a red banner visible to any logged-in user before they encounter API errors. Response time trends reveal performance degradation before it becomes a user-visible problem.

**Level 3 — Log-based anomaly detection**
`logs/error.log` captures all ERROR and CRITICAL events. `logs/security.log` captures all auth events in JSON format. A spike in 401 responses (> 20/min) signals a potential brute-force attack — detectable without a paid SIEM tool by watching the log.

**Combined MTTR impact:** Without monitoring, the average detection time for a silent database failure is the time until the next user reports an error. With the three-level monitoring stack, detection time is ≤ 30 seconds and automated recovery is possible without any human action.

---

## 8. How Management Monitoring Improves Decision-Making

The Management Monitoring Dashboard exposes four decision-support signals:

| Signal | Decision It Supports |
|--------|---------------------|
| **SPI (Schedule Performance Index)** | Is the sprint on track? Should scope be reduced to protect the deadline? |
| **Team workload per member** | Is any team member overloaded (> 95 % load)? Should tasks be redistributed? |
| **Milestone status** | Which milestones are complete, in progress, or at risk? |
| **Live asset count** | Is the system being populated with real data, or is the database empty? |

Before management monitoring existed, these questions required the PM to manually query each team member in the stand-up. With the dashboard, the PM can observe the signals before the meeting and focus the stand-up on blockers rather than status reporting.

---

## 9. How Risk Monitoring Supports Safer Industrial Operations

The Industry Maintenance Platform platform applies risk management at two levels:

**Platform-level risks (project):** 14 risks are identified, scored, owned, and monitored in `docs/risk-management.md`. Each has a mitigation, contingency, and monitoring method. The three dashboards surface the most critical risk signals (database failure, auth anomalies, schedule variance) automatically.

**Asset-level risks (runtime):** The `risk_scoring.py` service computes a risk score for every industrial asset based on ICS-specific parameters: Purdue model level, business criticality, physical access ease, and vulnerability score. Assets at Purdue Level 1 (field devices, PLCs) with remote access enabled receive the highest risk scores — because a compromise at this level can have physical consequences (process disruption, equipment damage, safety incidents).

**Why this matters for industrial operations:**
- A maintenance technician can see at a glance which assets need priority attention
- A security officer can prove to a compliance auditor that high-risk assets were reviewed and acted on
- A plant manager can schedule downtime for the riskiest asset without needing a consultant to tell them which one it is

---

## 10. Cost–Benefit Analysis

All costs below are estimates based on a 7-person student team over 16 weeks. No paid infrastructure is used.

| Cost Area | Expected Cost | Expected Benefit |
|-----------|--------------|-----------------|
| **Development effort** | ~450 person-hours (7 people × ~9 h/week × 7 weeks active development) | Fully functional industrial asset monitoring platform; all course requirements met |
| **Local infrastructure** | €0 — Docker, PostgreSQL, Nginx, GitHub Actions (all free) | No recurring operational cost; deployable on any machine with Docker |
| **Testing effort** | ~60 person-hours (QA engineer + developer test writing across 4 sprints) | CI quality gate on every PR; ≥ 70 % backend coverage; regression prevention |
| **Documentation effort** | ~80 person-hours (15+ documents, updated incrementally each sprint) | Complete academic submission package; system is self-documenting for future maintainers |
| **Training effort** | ~5 person-hours (demo data + README walkthrough; no classroom training needed) | New users can run `make demo` and explore a populated system in < 5 minutes |
| **Maintenance effort** | ~2 h/month (dependency updates, log rotation, DB backup verification) | Low ongoing cost; free toolchain with no licensing; Docker Compose makes updates predictable |
| **Total estimated effort** | ~595 person-hours | Working industrial monitoring platform, complete documentation, CI/CD, security controls, two monitoring dashboards |

### 10.1 Why Benefits Exceed Costs

The total cost is **effort only** — there is no infrastructure cost, no licensing cost, and no consultant cost. A commercial industrial asset management platform (e.g., Claroty, Dragos, or Armis) costs tens of thousands of euros per year in licensing alone. Industry Maintenance Platform achieves comparable core functionality (asset inventory, risk scoring, audit trail, user management) on a €0 infrastructure budget.

For the course project specifically: the value is demonstrated by mapping every implemented feature to a course concept (CI/CD, technical monitoring, management monitoring, risk management, value creation, stakeholder management, software design quality) — so the academic benefit of the work is directly proportional to its completeness.

### 10.2 Value Realised Per Feature Area

| Feature Area | Effort Investment | Value Delivered |
|-------------|------------------|----------------|
| Asset CRUD + 21 data models | High | Foundation for all other value; without accurate records, monitoring and risk scoring are meaningless |
| ICS Risk Scoring (`risk_scoring.py`) | Medium | Continuous automated risk assessment replaces periodic manual consultant work |
| Audit Trail (`audit_logs` table) | Low (decorator pattern) | High compliance value; append-only immutable log out of the box |
| Technical Monitoring (`/health/detailed` + dashboard) | Medium | Prevents downtime; demonstrates course concept of observability |
| Management Monitoring (`/management` endpoint + dashboard) | Medium | Demonstrates EVM, sprint tracking, and team visibility in a live dashboard |
| CI/CD Pipelines (GitHub Actions) | Low (2 YAML files) | Every commit quality-gated; demonstrates continuous testing course concept |
| RBAC + JWT + Rate Limiting | Medium | Security posture appropriate for an industrial environment |
| Global Search (Cmd+K) | Low (reuses existing API) | High usability value; technicians can find assets in < 200 ms |
