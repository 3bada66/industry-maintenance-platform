# Technical Monitoring Metrics Reference
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Owner:** Mohanad Aref Ali Sultan (Backend Developer, 2309115898)
**Supporting:** Hamdi Alnaqeeb (DevOps, 2309116178)

---

## Overview

This document defines the ten technical monitoring metrics tracked by the Industry Maintenance Platform platform. Each metric lists where it is collected, how it is exposed, and what thresholds trigger action. All monitoring is implemented using local logging, health check endpoints, and PostgreSQL audit tables — no paid monitoring services are required.

---

## Health Endpoint Quick Reference

```
GET /health
```
```json
{
  "status": "ok",
  "database": "connected",
  "uptime": "running",
  "timestamp": "2026-04-20T12:00:00Z"
}
```

```
GET /health/detailed
```
```json
{
  "status": "healthy",
  "timestamp": "2026-04-20T12:00:00Z",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 86400,
  "components": {
    "database": { "status": "healthy", "response_time_ms": 3.2, "pool_size": 5, "pool_checked_out": 1 },
    "cache":    { "status": "healthy", "type": "in-memory" },
    "api":      { "status": "healthy" }
  },
  "system": {
    "cpu_percent": 12.4,
    "memory_percent": 38.7,
    "memory_used_mb": 312,
    "memory_total_mb": 8192,
    "disk_percent": 24.1,
    "python_version": "3.10.12"
  }
}
```

Both endpoints require no authentication. They are accessible to Docker health checks, CI smoke tests, and the Technical Monitoring Dashboard at `/monitoring`.

---

## Metric 1 — API Response Time

**What it measures:** End-to-end latency from HTTP request receipt to response sent, in milliseconds.

**Where collected:** Uvicorn access logs (stdout); manually benchmarked per sprint.

**How to read it:**
```bash
# View live access log from running container
docker logs industry-maintenance-platform_backend 2>&1 | grep "GET /api"
```

**Targets:**

| Endpoint Category | P50 | P95 |
|------------------|-----|-----|
| Dashboard (cached) | < 50 ms | < 150 ms |
| Asset list | < 200 ms | < 500 ms |
| Search | < 200 ms | < 500 ms |
| Risk scoring | < 500 ms | < 1 s |
| Login (bcrypt) | < 300 ms | < 600 ms |
| `/health` | < 20 ms | < 50 ms |

**Alert:** If any P95 exceeds its target for more than one sprint, add an index or cache entry.

---

## Metric 2 — Error Rate

**What it measures:** Percentage of HTTP responses with 5xx status codes over a rolling window.

**Where collected:** Uvicorn access logs; application-level `logger.error()` calls in routers.

**Formula:**
```
Error Rate (%) = (5xx responses / Total responses) × 100
```

**Thresholds:**
- Warning: > 1 % over a 5-minute window
- Critical: > 5 % over a 1-minute window

**How to inspect:**
```bash
docker logs industry-maintenance-platform_backend 2>&1 | grep " 5[0-9][0-9] " | wc -l
```

**Log location:** `logs/industry-maintenance-platform.log` (rotating, 10 MB max, 5 backups)

---

## Metric 3 — Failed Request Count

**What it measures:** Absolute count of requests that returned an error (4xx or 5xx), broken down by type.

**Where collected:** Application logger at `WARNING` (4xx client errors) and `ERROR` (5xx server errors) level.

**Categories tracked:**

| HTTP Status | Meaning | Expected Volume |
|-------------|---------|-----------------|
| 401 | Auth failure (bad/expired token) | Low; spike → brute force |
| 403 | RBAC denial | Occasional |
| 422 | Validation error | Occasional (bad input) |
| 500 | Internal server error | Zero in steady state |
| 503 | Service unavailable | Zero in steady state |

**How to inspect:**
```bash
grep "ERROR" logs/industry-maintenance-platform.log | tail -50
grep "status_code.*500" logs/industry-maintenance-platform.log | wc -l
```

---

## Metric 4 — Database Status

**What it measures:** Whether the PostgreSQL database is reachable and responding normally.

**Where collected:** `GET /health` and `GET /health/detailed` endpoints (live DB ping on every call).

**Values:**

| Value | Meaning |
|-------|---------|
| `"connected"` / `"healthy"` | `SELECT 1` succeeded within normal latency |
| `"disconnected"` / `"unhealthy"` | DB unreachable or query threw an exception |

**Additional signals from `/health/detailed`:**
- `response_time_ms` — DB ping round-trip; alert if > 100 ms sustained
- `pool_size` / `pool_checked_out` — alert if `pool_checked_out >= pool_size` (pool exhaustion)

**Docker health check (automatic):**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U industry-maintenance-platform_user -d industry-maintenance-platform"]
  interval: 10s
  retries: 5
```

---

## Metric 5 — Application Health

**What it measures:** Combined status of all application components (API, database, cache).

**Where collected:** `GET /health/detailed` — `"status"` field in response.

**Values:**

| Status | Meaning |
|--------|---------|
| `ok` / `healthy` | All components operating normally |
| `degraded` | One non-critical component has issues |
| `unhealthy` | One or more critical components failed |

**Frontend display:** The Technical Monitoring Dashboard at `/monitoring` shows this as a full-width colour banner — green, amber, or red — and auto-refreshes every 30 seconds.

**Docker container health check:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Metric 6 — Uptime

**What it measures:** Continuous time the backend process has been running without a restart.

**Where collected:** `app.state.startup_time` is set by a FastAPI startup event handler. `/health` returns `"uptime": "running"` or `"starting"`. `/health/detailed` returns `"uptime_seconds"` as an integer.

**How uptime is recorded (backend/app/main.py):**
```python
@app.on_event("startup")
async def _record_startup_time():
    import time
    app.state.startup_time = time.time()
```

**Targets:**

| Service | Target | Window |
|---------|--------|--------|
| Backend API | 99.5 % | Per sprint (3 weeks) |
| Frontend/Nginx | 99.9 % | Per sprint |
| Database | 99.9 % | Per sprint |

Planned maintenance (migrations, restarts) is excluded from uptime calculations.

---

## Metric 7 — Crash / Failure Count

**What it measures:** Number of times the application process exited unexpectedly or raised an unhandled exception.

**Where collected:**
- Docker restart events: `docker inspect --format='{{.RestartCount}}' industry-maintenance-platform_backend`
- Unhandled exceptions: logged to `logs/error.log` at `CRITICAL` level by the global exception handler in `main.py`

**How to check restart count:**
```bash
docker inspect --format='{{.RestartCount}}' industry-maintenance-platform_backend
# Expected: 0 in steady state
```

**How to check for unhandled exceptions:**
```bash
grep "CRITICAL" logs/error.log
grep "Unhandled" logs/error.log
```

**Thresholds:**

| Condition | Severity |
|-----------|---------|
| 0 restarts per day | Healthy |
| 1 restart per day | Warning — investigate root cause |
| > 1 restart per day | Critical — block new deployments until fixed |

---

## Metric 8 — Last Deployment Status

**What it measures:** Whether the most recent deployment completed successfully, including database migration.

**Where collected:** Git tags, Alembic migration state, Docker Compose exit codes.

**How to check:**
```bash
# 1. Last deployment tag
git log --tags --simplify-by-decoration --pretty="format:%d %s" | head -5

# 2. Current Alembic revision (must match latest migration)
docker exec industry-maintenance-platform_backend alembic current

# 3. Container health after deployment
docker ps --format "table {{.Names}}\t{{.Status}}"
# Expected: all containers show "(healthy)"

# 4. Smoke test
curl -s http://localhost:8000/health | python3 -m json.tool
# Expected: {"status": "ok", "database": "connected", ...}
```

**Deployment is considered successful when:**
- All containers report `(healthy)` in `docker ps`
- `GET /health` returns `{"status": "ok", "database": "connected"}`
- `alembic current` matches the latest migration revision

---

## Metric 9 — Recent Logs

**What it measures:** Application log output since the last restart, used for anomaly detection and debugging.

**Where collected:** Python `logging` module → `logs/industry-maintenance-platform.log` (all levels) and `logs/error.log` (ERROR+).

**Log file locations:**

| File | Content | Rotation |
|------|---------|---------|
| `logs/industry-maintenance-platform.log` | All INFO+ events | 10 MB, 5 backups |
| `logs/error.log` | ERROR and CRITICAL only | 10 MB, 5 backups |
| `logs/security.log` | Auth events (JSON format) | 10 MB, 10 backups |

**How to read recent logs:**
```bash
# Last 100 lines from running container
docker logs --tail 100 industry-maintenance-platform_backend

# Last 50 error-level entries
grep "ERROR\|CRITICAL" logs/industry-maintenance-platform.log | tail -50

# Security events (login, logout, failed auth)
tail -20 logs/security.log

# Slow queries (WARNING level)
grep "WARNING" logs/industry-maintenance-platform.log | grep -i "slow\|timeout"
```

**Log entry format (application):**
```
2026-04-20 12:00:00 - app.routers.assets - INFO - Asset created: uuid-123
```

**Log entry format (security.log — JSON):**
```json
{"timestamp": "2026-04-20 12:00:00", "level": "INFO", "logger": "app.services.auth", "message": "Security event: {...}"}
```

---

## Metric 10 — Audit Activity

**What it measures:** Count and content of all CREATE, UPDATE, DELETE, LOGIN, and LOGOUT events recorded in the immutable audit trail.

**Where collected:** `audit_logs` table in PostgreSQL — written by `services/audit_log.py` via the `@audit_action` decorator on every mutating endpoint.

**Schema:**
```sql
audit_logs (
  id          UUID PRIMARY KEY,
  user_id     UUID,
  tenant_id   UUID,
  action      VARCHAR,   -- CREATE, UPDATE, DELETE, LOGIN, LOGOUT
  entity_type VARCHAR,   -- asset, user, site, ...
  entity_id   UUID,
  ip_address  VARCHAR,
  timestamp   TIMESTAMPTZ,
  details     JSONB      -- before/after diff for updates
)
```

**How to query:**
```bash
# Via API (admin token required)
curl -H "Authorization: Bearer <token>" \
  https://localhost/api/v1/audit-logs/?limit=20

# Direct PostgreSQL query
docker exec industry-maintenance-platform_postgres psql -U industry-maintenance-platform_user -d industry-maintenance-platform \
  -c "SELECT action, entity_type, ip_address, timestamp FROM audit_logs ORDER BY timestamp DESC LIMIT 20;"
```

**Alert:** If the audit log insert fails (write error to `audit_logs`), treat as P1 — the system must maintain a compliance trail at all times.

**Immutability guarantee:** Audit log rows are never updated or deleted by the application. No DELETE or UPDATE SQL is issued on `audit_logs` by any router or service.

---

## Summary Table

| # | Metric | Source | Alert Threshold |
|---|--------|--------|-----------------|
| 1 | API Response Time | Uvicorn logs | P95 > target for 1 sprint |
| 2 | Error Rate | App logs + access logs | > 1 % / 5 min; > 5 % / 1 min |
| 3 | Failed Request Count | App logs (ERROR level) | Any 500 in production |
| 4 | Database Status | `GET /health` DB ping | `disconnected` or ping > 100 ms |
| 5 | Application Health | `GET /health/detailed` | Status `degraded` or `unhealthy` |
| 6 | Uptime | `app.state.startup_time` | Container restart detected |
| 7 | Crash / Failure Count | Docker restart count + error.log | > 0 restarts per day |
| 8 | Last Deployment Status | Git tag + alembic + docker ps | Any container not `(healthy)` |
| 9 | Recent Logs | `logs/` directory | Any CRITICAL in error.log |
| 10 | Audit Activity | `audit_logs` PostgreSQL table | Audit insert failure → P1 |

All tools used are free and open-source. No paid monitoring services are required.
