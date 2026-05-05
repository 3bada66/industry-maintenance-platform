# Monitoring Strategy
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.0
**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)
**Supporting:** Hamdi Alnaqeeb (DevOps/Operations, 2309116178) · Mohanad Aref Ali Sultan (Backend Developer, 2309115898)

---

## 1. Purpose

This document defines the complete monitoring strategy for Industry Maintenance Platform. It combines two monitoring layers — **management monitoring** and **technical monitoring** — into a single framework, explaining what is measured, why it is measured, where the data comes from, and when an alert is triggered.

The strategy is guided by four principles:

- **Metrics show what is happening** — quantitative indicators of system and project state
- **Logs explain why it happened** — timestamped records of every event and action
- **Health checks show whether the system is usable** — binary pass/fail tests that answer "is this component working right now"
- **Alerts notify the team when action is required** — triggered only when a threshold is crossed, not on every poll

---

## 2. Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Management Layer (project KPIs)                            │
│  Source: GET /api/v1/management/status                      │
│  Consumer: ManagementMonitoring.vue (60 s refresh)          │
│  Data: static project plan + live asset count from DB       │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│  Technical Layer (system health)                            │
│  Source: GET /health · GET /health/detailed                 │
│  Consumer: TechnicalMonitoring.vue (30 s refresh)           │
│  Also consumed by: Docker healthcheck, external monitors    │
│  Data: live DB ping, psutil system stats, log file scan     │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│  Observability Base Layer                                   │
│  logs/app.log          — all HTTP requests, INFO+           │
│  logs/error.log        — ERROR and CRITICAL events only     │
│  logs/security.log     — all auth events in JSON format     │
│  audit_logs table      — every CREATE/UPDATE/DELETE entity  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Management Monitoring

Management monitoring answers the project manager's question: **"Is the project on track and is the team healthy?"**

### 3.1 Progress KPIs

| KPI | Source | Meaning |
|-----|--------|---------|
| Tasks completed | `tasks.completed / tasks.total` | Percentage of all sprint tasks done |
| Story points earned | `schedule.earned_value_sp` | EVM earned value in story points |
| Sprint progress (%) | `tasks.progress_percent` | Overall task completion rate |
| Assets managed (live) | `project.assets_managed` — live DB query | Confirms the system holds real data |

These KPIs appear as the top-row tiles on the Management Monitoring Dashboard at `/management`.

### 3.2 Schedule KPIs (Earned Value Management)

| KPI | Formula | Interpretation |
|-----|---------|---------------|
| **SPI** (Schedule Performance Index) | `earned_value_sp / planned_value_sp` | = 1.0: on schedule; < 1.0: behind; > 1.0: ahead |
| **Schedule Variance** | `earned_value_sp − planned_value_sp` | Negative = behind plan in story points |
| **Sprint velocity** | Story points completed per sprint | Trend reveals team capacity; sharp drop signals a problem |

The SPI is the primary schedule health signal. An SPI below 0.85 triggers the schedule risk escalation path defined in `docs/risk-management.md`.

### 3.3 Cost KPIs

All infrastructure costs in this project are €0 (Docker, PostgreSQL, GitHub Actions are free). Cost tracking uses person-hours as the proxy for cost:

| KPI | Source | Meaning |
|-----|--------|---------|
| Estimated hours | `cost.estimated_eur` (h) | Planned effort for the sprint |
| Actual hours | `cost.actual_eur` (h) | Reported effort spent |
| CPI | `cost.cpi` | = 1.0: effort on budget; < 1.0: overspent |
| Effort variance | `cost.variance_eur` | Difference between planned and actual hours |

### 3.4 Workload KPIs

| KPI | Source | Alert Condition |
|-----|--------|----------------|
| Team member load (%) | `team_workload[*].load_percent` | > 95 %: member is overloaded |
| Story points assigned | `team_workload[*].assigned_sp` | > 20 per sprint: review task distribution |
| Story points completed | `team_workload[*].completed_sp` | < 50 % at sprint midpoint: follow up |

The workload table on the Management Dashboard uses a `<ProgressBar>` coloured green (< 80 %), amber (80–95 %), or red (> 95 %) to make overload immediately visible.

### 3.5 Milestone Tracking

Seven milestones are tracked from project kickoff to final submission:

| Milestone | Due Week | Deliverables |
|-----------|----------|-------------|
| Project Kickoff | W1 | Team formed, repository created, branching model agreed |
| Sprint 1 Complete | W4 | Auth, CRUD, DB schema, CI pipeline |
| Sprint 2 Complete | W7 | Risk scoring, audit trail, dashboard |
| Sprint 3 Complete | W10 | Network map, floor plan, technical monitoring |
| Sprint 4 Complete | W13 | Management monitoring, stakeholder docs, value creation |
| Documentation Freeze | W14 | All docs finalised and reviewed |
| Final Submission | W16 | Repository tagged, video recorded, report submitted |

Status values: `completed`, `in_progress`, `at_risk`, `not_started`. The milestone timeline on the dashboard uses coloured tags to show current state at a glance.

### 3.6 Risk Status Tracking

The management endpoint exposes a risk summary pulled from the risk register in `docs/risk-management.md`:

| Signal | Value | Meaning |
|--------|-------|---------|
| Total risks | 14 | Full register count |
| High severity | 4 | Require immediate owner attention |
| Medium severity | 6 | Monitor weekly |
| Low severity | 4 | Review monthly |
| Active risks | 7 | Mitigations in progress |
| Mitigated risks | 3 | Contingency applied, monitoring continues |
| Closed risks | 4 | No longer relevant |

The four top open risks are listed individually with their ID, title, severity, owner, and mitigation status so the PM can act without opening the full register.

---

## 4. Technical Monitoring

Technical monitoring answers the operations question: **"Is the system healthy and responsive right now?"**

### 4.1 Health Checks

Two health endpoints are exposed by `main.py`. Neither requires authentication — they are designed to be polled by monitoring systems and Docker's own health check.

#### `GET /health` — Basic check

```json
{
  "status": "ok",
  "database": "connected",
  "uptime": "running",
  "timestamp": "2026-04-20T12:00:00Z"
}
```

Used by: Docker healthcheck (`curl -f /health`), basic uptime monitors.

`database` becomes `"disconnected"` if `SELECT 1` raises an exception.
`uptime` is `"starting"` for the first few seconds after container start.

#### `GET /health/detailed` — Full metrics

```json
{
  "status": "healthy",
  "timestamp": "2026-04-20T12:00:00Z",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 86400,
  "components": {
    "database": {
      "status": "connected",
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

Used by: `TechnicalMonitoring.vue` (30-second interval poll), external monitoring tools, manual debugging.

The `system` block requires `psutil` to be installed. If psutil is missing, the system fields are omitted and the endpoint still returns `200 OK`.

### 4.2 Metrics

Ten metrics are tracked, collected, and displayed on the Technical Monitoring Dashboard:

| # | Metric | Source | Normal Range |
|---|--------|--------|-------------|
| 1 | **Database status** | `/health/detailed` → `components.database.status` | `connected` |
| 2 | **DB response time** | `/health/detailed` → `components.database.response_time_ms` | < 100 ms |
| 3 | **API uptime** | `/health/detailed` → `uptime_seconds` | Increasing monotonically |
| 4 | **CPU usage** | `/health/detailed` → `system.cpu_percent` (psutil) | < 70 % |
| 5 | **Memory usage** | `/health/detailed` → `system.memory_percent` (psutil) | < 80 % |
| 6 | **Disk usage** | `/health/detailed` → `system.disk_percent` (psutil) | < 85 % |
| 7 | **Error rate** | `logs/error.log` line count delta | 0 new errors/min at steady state |
| 8 | **Audit activity** | `audit_logs` table — recent row count | Increases with user activity |
| 9 | **Deployment status** | `/health/detailed` → `environment` + Alembic current | Matches expected version |
| 10 | **Crash count** | Docker `docker inspect --format='{{.RestartCount}}'` | 0 since last deploy |

### 4.3 Logs

Three log files are written by the backend:

| Log File | Content | Format | Retention |
|----------|---------|--------|-----------|
| `logs/app.log` | All HTTP requests, INFO-level events | Plain text | 30 days (rotated) |
| `logs/error.log` | ERROR and CRITICAL events only | Plain text | 90 days |
| `logs/security.log` | All authentication events (login success, login failure, logout, token refresh) | JSON (one object per line) | 365 days |

`security.log` uses structured JSON format so it can be ingested by log aggregation tools without parsing:

```json
{"timestamp": "2026-04-20T12:00:00Z", "event": "login_success", "user_id": 5, "tenant_id": 1, "ip": "192.168.1.10"}
{"timestamp": "2026-04-20T12:01:00Z", "event": "login_failure", "email": "unknown@example.com", "ip": "192.168.1.99"}
```

### 4.4 Error Tracking

Errors are captured at two points:

1. **Application-level:** The global exception handler in `main.py` catches all unhandled exceptions, logs them to `logs/error.log` with a traceback, and returns a `500` JSON response.
2. **HTTP-level:** Nginx/Traefik logs every HTTP response code. 4xx rates are visible in the access log.

No external error aggregation tool (Sentry, Rollbar) is currently integrated. *(Planned enhancement.)*

A spike in 401 responses — defined as more than 20 per minute from the same IP address — is detectable by watching `security.log` for repeated `login_failure` events. This is the primary signal for a brute-force attack.

### 4.5 Database Status

The database is monitored at three levels:

| Level | Mechanism | Frequency |
|-------|-----------|-----------|
| **Container** | `pg_isready` via Docker healthcheck | Every 10 s |
| **Connection** | `SELECT 1` via `/health/detailed` | Every 30 s (when dashboard is open) |
| **Pool** | `pool_size`, `pool_checked_out` fields | Every 30 s |

`pool_checked_out` approaching `pool_size` indicates connection pool exhaustion — a precursor to API latency spikes.

### 4.6 Uptime

`uptime_seconds` in `/health/detailed` is calculated from `app.state.startup_time` set in the FastAPI startup event. A container restart resets this counter to 0, making it easy to detect unexpected restarts.

Docker's `restart: unless-stopped` policy automatically restarts the backend container if the health check fails three consecutive times. Recovery time is typically 60–90 seconds.

---

## 5. Audit Trails

The `audit_logs` PostgreSQL table is the central accountability record for all data changes in the system.

### 5.1 What is Logged

Every CREATE, UPDATE, and DELETE operation on any entity (asset, site, user, role, contact, etc.) produces one audit log row containing:

| Field | Value |
|-------|-------|
| `id` | Auto-increment primary key |
| `user_id` | FK to the user who performed the action |
| `tenant_id` | FK to the tenant — no cross-tenant log leakage |
| `ip_address` | Client IP from the HTTP request |
| `timestamp` | UTC timestamp — immutable after write |
| `entity_type` | String name of the model (e.g., `Asset`, `Site`) |
| `entity_id` | Primary key of the changed entity |
| `operation` | `CREATE`, `UPDATE`, or `DELETE` |
| `diff` | JSON object with `before` and `after` values for every changed field |

### 5.2 Audit Log Guarantees

- **Append-only:** The application has no DELETE or UPDATE endpoint for audit logs. Rows are written and never modified.
- **Multi-tenant isolated:** `tenant_id` is set server-side from the authenticated user's JWT, not from the request body. No client can write audit logs to another tenant.
- **API accessible:** `GET /api/v1/audit-logs/` with filter parameters (`entity_type`, `user_id`, `start_date`, `end_date`) returns a filterable, paginated audit trail suitable for compliance export.

### 5.3 How Audit Trails Support Accountability

| Accountability Question | Audit Log Answer |
|------------------------|-----------------|
| Who changed this asset's IP address? | Filter by `entity_type=Asset`, `entity_id=N`, `operation=UPDATE` → `user_id` in result |
| What changed between yesterday and today? | Filter by `timestamp` range → list of diffs |
| Was this user ever granted admin rights? | Filter by `entity_type=User`, `entity_id=N` → scan diffs for `role` field changes |
| Which assets were deleted last month? | Filter by `operation=DELETE`, `entity_type=Asset`, timestamp range |

---

## 6. Observability

Observability is the ability to understand the internal state of a system from its external outputs. Industry Maintenance Platform provides observability at three levels:

| Level | Tool | Answers |
|-------|------|---------|
| **Metrics** | `/health/detailed` + Management dashboard | What is the current state? Is it normal? |
| **Logs** | `app.log`, `error.log`, `security.log` | What happened and when? Why did the system behave this way? |
| **Traces** (partial) | Request ID in log lines + audit log diff per operation | Which request caused this change? What did it do step by step? |

Full distributed tracing (OpenTelemetry, Jaeger) is not implemented. *(Planned enhancement.)* Current observability is sufficient for a single-server deployment.

---

## 7. Alerts

No automated alerting system (PagerDuty, Grafana Alertmanager, email on threshold) is configured in the current deployment. *(Planned enhancement.)*

The team relies on the dashboard dashboards as the alert surface. The monitoring pages use colour-coded indicators to draw attention to threshold violations:

| Dashboard | Signal | Colour Code |
|-----------|--------|-------------|
| Technical Monitoring | Database `disconnected` | Red banner |
| Technical Monitoring | CPU > 70 % | Amber |
| Technical Monitoring | Memory > 80 % | Amber |
| Technical Monitoring | Disk > 85 % | Red |
| Management Monitoring | SPI < 0.85 | Red badge |
| Management Monitoring | Team member load > 95 % | Red progress bar |
| Management Monitoring | Milestone status `at_risk` | Amber tag |

When a red signal appears on either dashboard, the responsible team member takes action according to the escalation path in `docs/risk-management.md §4`.

---

## 8. Complete Monitoring Metrics Table

| Monitoring Area | Metric | Purpose | Alert Condition |
|----------------|--------|---------|----------------|
| **Database** | Connection status | Confirm DB is reachable | `disconnected` |
| **Database** | Query response time (ms) | Detect DB performance degradation | > 500 ms |
| **Database** | Connection pool checked out | Detect pool exhaustion | = pool_size |
| **API** | Uptime (seconds) | Detect unexpected restarts | Resets to 0 |
| **API** | HTTP 5xx error count | Detect application errors | > 0 in 5-minute window |
| **API** | HTTP 401 login failures | Detect brute-force attempts | > 20 / minute from same IP |
| **System** | CPU usage (%) | Detect runaway processes | > 70 % |
| **System** | Memory usage (%) | Detect memory pressure | > 80 % |
| **System** | Disk usage (%) | Prevent out-of-disk failures | > 85 % |
| **Deployment** | Alembic migration version | Detect stale schema | Not matching HEAD |
| **Container** | Backend restart count | Detect crash loops | > 0 since last deploy |
| **Security** | Login failure rate | Detect brute force | > 20 failures / minute |
| **Security** | Auth events in security.log | Audit trail for access | Any `permission_denied` event |
| **Audit** | New audit_log rows per hour | Confirm audit trail is active | 0 rows during active session |
| **Project — Schedule** | SPI | Sprint schedule health | < 0.85 |
| **Project — Schedule** | Sprint velocity trend | Team capacity signal | Drop > 20 % vs prior sprint |
| **Project — Workload** | Team member load (%) | Overload detection | > 95 % |
| **Project — Tasks** | Overdue task count | Blocked work detection | > 0 |
| **Project — Milestones** | Milestone status | Delivery risk | `at_risk` or missed due date |
| **Project — Risk** | High-severity open risks | Active threat to project | > 2 unmitigated high risks |
| **Project — Cost** | CPI | Effort budget health | < 0.90 |
| **Data** | Live asset count | System is being populated | 0 assets after Week 2 |

---

## 9. Monitoring Dashboard Summary

### 9.1 Technical Monitoring Dashboard (`/monitoring`)

| Section | Refresh | Key Data |
|---------|---------|---------|
| System Status banner | 30 s | Overall `healthy` / `degraded` / `unhealthy` |
| Component Status tiles | 30 s | Database, API, Cache — green/amber/red |
| System Metrics | 30 s | CPU %, Memory %, Disk % with colour thresholds |
| DB Performance | 30 s | Response time ms, pool size, pool checked out |
| Uptime | 30 s | Seconds since last start |
| Alert Thresholds table | Static | Reference: what triggers each alert |

Source: `GET /health/detailed` (no authentication required)

### 9.2 Management Monitoring Dashboard (`/management`)

| Section | Refresh | Key Data |
|---------|---------|---------|
| KPI tiles | 60 s | Tasks %, SPI, live asset count, sprint number |
| Sprint Velocity | 60 s | Bar chart — story points per sprint (4 sprints) |
| Milestones | 60 s | DataTable with due week, status tag, deliverables |
| Team Workload | 60 s | DataTable with ProgressBar per member |
| Cost / Effort | 60 s | Estimated vs actual hours, CPI |
| Risk Summary | 60 s | Severity counts, top open risks list |

Source: `GET /api/v1/management/status` (JWT authentication required)

---

## 10. Monitoring in the Development Workflow

| Activity | Monitoring Touchpoint |
|----------|----------------------|
| Before every PR merge | `pytest --cov` CI job must pass; `/health` must return `ok` in CI container |
| After every deploy | Check `/health/detailed` for `"status": "healthy"` and `uptime_seconds > 0` |
| Sprint retrospective | Review Management Dashboard SPI, velocity trend, and workload distribution |
| Security review | Scan `logs/security.log` for `login_failure` spikes and `permission_denied` events |
| Compliance audit | Export `GET /api/v1/audit-logs/` for the review period |
| Incident response | Check `logs/error.log` for ERROR entries; check `/health/detailed` for DB and system status |
