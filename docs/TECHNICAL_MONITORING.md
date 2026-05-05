# Technical Monitoring Plan
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Version:** 1.0  
**Owner:** Mohanad Aref Ali Sultan (Backend Developer, 2309115898) + Hamdi Alnaqeeb (DevOps, 2309116178)

---

## 1. Overview

Technical monitoring is the continuous observation of the system's runtime behavior to detect failures, degradation, and anomalies before they affect users. This document defines what Industry Maintenance Platform monitors, how it monitors it, and how alerts are handled.

**Monitoring Principles Applied:**
- **Observe, don't guess** — metrics over intuition
- **Alert on symptoms, not causes** — user-visible impact first
- **Low noise** — only page on actionable conditions
- **Immutable logs** — audit trail is append-only

---

## 2. Health Check Endpoints

### 2.1 Basic Health Check (Implemented)
**Endpoint:** `GET /health`  
**Auth:** None required  
**Purpose:** Load-balancer liveness probe

```json
{
  "status": "healthy",
  "timestamp": "2026-04-20T14:32:01.123456",
  "version": "1.0.0",
  "environment": "production"
}
```

### 2.2 Detailed Health Check (Implemented)
**Endpoint:** `GET /health/detailed`  
**Auth:** None required (monitoring systems need unauthenticated access)  
**Purpose:** Full system status for the Technical Monitoring Dashboard

```json
{
  "status": "healthy",
  "timestamp": "2026-04-20T14:32:01.123456",
  "version": "1.0.0",
  "environment": "production",
  "uptime_seconds": 86400,
  "components": {
    "database": {
      "status": "healthy",
      "response_time_ms": 3.2,
      "pool_size": 5,
      "pool_checked_out": 1
    },
    "cache": {
      "status": "healthy",
      "type": "in-memory"
    },
    "api": {
      "status": "healthy",
      "active_requests": 2
    }
  },
  "system": {
    "cpu_percent": 12.4,
    "memory_percent": 38.7,
    "memory_used_mb": 312,
    "memory_total_mb": 8192,
    "disk_percent": 24.1
  }
}
```

**Status Values:**
| Value | Meaning |
|-------|---------|
| `healthy` | All components operating normally |
| `degraded` | One non-critical component has issues |
| `unhealthy` | One or more critical components failed |

---

## 3. Performance Metrics

### 3.1 API Response Time Targets

| Endpoint Category | P50 Target | P95 Target | P99 Target |
|------------------|-----------|-----------|-----------|
| Dashboard (cached) | < 50ms | < 150ms | < 300ms |
| Asset list (paginated) | < 200ms | < 500ms | < 1s |
| Asset detail | < 100ms | < 300ms | < 500ms |
| Search | < 200ms | < 500ms | < 1s |
| Risk scoring | < 500ms | < 1s | < 2s |
| File upload | < 2s | < 5s | < 10s |
| Login/Auth | < 300ms | < 600ms | < 1s |

### 3.2 Current Performance Baseline (Sprint 4 measurements)

| Endpoint | Method | P50 | P95 | Notes |
|----------|--------|-----|-----|-------|
| `GET /api/v1/assets/` | Backend | 45ms | 180ms | Redis cache active |
| `GET /api/v1/dashboards/` | Backend | 32ms | 95ms | Fully cached |
| `POST /login` | Backend | 210ms | 480ms | bcrypt is intentionally slow |
| `GET /api/v1/search/` | Backend | 90ms | 310ms | PostgreSQL full-text |
| `GET /health/detailed` | Backend | 15ms | 40ms | DB ping included |

### 3.3 Throughput Targets

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Concurrent users | ≥ 50 | < 30 |
| Requests/minute | ≥ 1,000 | < 500 |
| Database connections | ≤ 20 active | > 18 active |

---

## 4. Error Rate Monitoring

### 4.1 HTTP Error Categories

| HTTP Status | Category | Alert Condition |
|-------------|----------|-----------------|
| 4xx (client) | Client errors | No alert (normal) |
| 400 Bad Request | Validation failure | Alert if rate > 50/min |
| 401 Unauthorized | Auth failure | Alert if rate > 20/min (potential brute force) |
| 403 Forbidden | RBAC denial | Alert if rate > 20/min |
| 404 Not Found | Missing resource | No alert |
| 422 Unprocessable | Validation error | No alert |
| 500 Internal Error | Server failure | Alert immediately |
| 503 Service Unavailable | Overload | Alert immediately |

### 4.2 Error Rate Calculation

```
Error Rate (%) = (5xx responses / Total responses) × 100
Alert threshold: Error Rate > 1% over 5-minute window
Critical threshold: Error Rate > 5% over 1-minute window
```

### 4.3 Error Tracking in Logs

All errors are captured with:
- Timestamp (ISO 8601)
- HTTP status code
- Request path and method
- User ID (if authenticated)
- Tenant ID
- IP address
- Stack trace (500 errors only, development mode)
- Correlation ID for request tracing

---

## 5. System Stability Indicators

### 5.1 Application Stability

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|---------|
| Unhandled exceptions / hour | 0 | 1–5 | > 5 |
| Crash restarts / day | 0 | 1 | > 1 |
| Memory growth / hour | < 5 MB | 5–20 MB | > 20 MB |
| CPU sustained > 80% | 0 min | < 5 min | > 5 min |
| Failed DB connections | 0 | 1–2 | > 2 |

### 5.2 Container Health (Docker)

Docker Compose health checks are configured for all services:

```yaml
# backend service health check
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s

# postgres service health check
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U industry-maintenance-platform_user -d industry-maintenance-platform"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### 5.3 Uptime Target

| Service | Uptime Target | Measurement Window |
|---------|--------------|-------------------|
| Backend API | 99.5% | Per sprint (3 weeks) |
| Frontend | 99.9% | Per sprint (3 weeks) |
| Database | 99.9% | Per sprint (3 weeks) |

*Planned maintenance (migrations, restarts) is excluded from uptime calculation.*

---

## 6. Database Health Status

### 6.1 PostgreSQL Monitoring

| Metric | Query | Alert Threshold |
|--------|-------|-----------------|
| Connection count | `SELECT count(*) FROM pg_stat_activity` | > 18/20 pool |
| Long-running queries | `SELECT ... WHERE duration > interval '30s'` | Any query > 30s |
| Table bloat | `pg_stat_user_tables` | Bloat ratio > 30% |
| Index hit rate | `pg_statio_user_tables` | Hit rate < 95% |
| DB size growth | `pg_database_size()` | > 1 GB/week |
| Replication lag | N/A (single node) | — |

### 6.2 Database Performance Index

The dashboard shows these PostgreSQL health signals:
- **Index hit rate** (should be > 99%)
- **Cache hit rate** (should be > 95%)
- **Active connections** vs pool maximum
- **Query execution times** (P50/P95 from application logs)
- **Table sizes** (top 10 largest tables)

### 6.3 Alembic Migration Safety

Before every deployment:
1. Run `alembic current` to verify current revision
2. Run `alembic check` to detect pending migrations
3. Test migration on dev DB first
4. Backup production DB before applying
5. Apply with `alembic upgrade head`
6. Verify with `alembic current` post-deploy

---

## 7. Logs and Alerts

### 7.1 Log Architecture

```
Application Code
      │
      ▼ (Python logging module)
  logging_config.py
      │
      ├─► logs/app.log          (rotating, 10MB max, 5 backups)
      ├─► stdout/stderr         (captured by Docker)
      └─► Docker log driver     ──► docker logs industry-maintenance-platform_backend
```

### 7.2 Log Levels and Usage

| Level | When Used | Example |
|-------|-----------|---------|
| `DEBUG` | Detailed tracing (dev only) | SQL queries, request params |
| `INFO` | Normal operations | User login, asset created |
| `WARNING` | Degraded but not broken | Slow query > 500ms, Redis miss |
| `ERROR` | Failures requiring attention | DB connection failed, 500 error |
| `CRITICAL` | System cannot continue | Startup failure, disk full |

### 7.3 Structured Log Format

All INFO+ logs emit JSON lines to stdout for easy parsing:

```json
{
  "timestamp": "2026-04-20T14:32:01.123Z",
  "level": "ERROR",
  "logger": "app.routers.assets",
  "message": "Database error on asset creation",
  "user_id": "uuid-here",
  "tenant_id": "uuid-here",
  "path": "/api/v1/assets/",
  "method": "POST",
  "status_code": 500,
  "duration_ms": 45.2
}
```

### 7.4 Alert Rules

| Alert Name | Condition | Severity | Response |
|-----------|-----------|----------|---------|
| API Down | `/health` returns non-200 for 2 min | P1-Critical | Restart container; page on-call |
| High Error Rate | 5xx rate > 5% for 1 min | P1-Critical | Investigate logs immediately |
| DB Connection Exhausted | Active connections > 18/20 | P1-Critical | Scale connection pool or restart |
| Slow Queries | Any query > 30 seconds | P2-High | Analyze query plan; add index |
| Elevated Error Rate | 5xx rate > 1% for 5 min | P2-High | Review error logs |
| High Memory | Memory > 85% for 10 min | P2-High | Investigate memory leak |
| Auth Failures | 401 rate > 20/min | P2-High | Check for brute-force attack |
| Disk Usage | Disk > 80% | P3-Medium | Clean logs; expand storage |
| Slow Dashboard | Dashboard P95 > 1s | P3-Medium | Check Redis cache; DB indexes |

### 7.5 Audit Log Monitoring

The system maintains an immutable audit trail in PostgreSQL (`audit_logs` table):
- Every CREATE, UPDATE, DELETE action is logged
- Login/logout events are recorded
- IP address is captured for all auth events
- Accessible via `GET /api/v1/audit-logs/` (admin only)

Alert: If audit logging fails (insert error), treat as P1 — the system must maintain compliance trail.

---

## 8. Technical Monitoring Dashboard (UI)

**File:** `frontend/src/pages/TechnicalMonitoring.vue`  
**Route:** `/monitoring` (requires auth)  
**Status:** [Implemented]  
**Refresh:** Auto-refresh every 30 seconds via `setInterval` (cleared on `onUnmounted`)  
**Data source:** `GET /health/detailed` via `api.getHealthDetailed()`

### 8.1 Implemented Dashboard Panels

| Panel | Metric Displayed | Visual Component |
|-------|-----------------|-----------------|
| Overall Status Banner | healthy / degraded / unhealthy with colour | Full-width coloured strip |
| Database Component Card | status badge + response time (ms) + pool usage | `<Tag>` + text |
| Cache Component Card | status badge + cache type | `<Tag>` |
| API Component Card | status badge + Python version | `<Tag>` |
| CPU Usage | percentage bar (green → amber → red) | `<ProgressBar>` |
| Memory Usage | used MB / total MB percentage bar | `<ProgressBar>` |
| Disk Usage | percentage bar | `<ProgressBar>` |
| Alert Thresholds Table | all 7 alert rules with severity tags | `<DataTable>` |

System resource panels (CPU, memory, disk) require `psutil==5.9.8` installed in the backend.
When `psutil` is not available, an info card explains how to install it — the rest of the dashboard still works.

### 8.2 Status Indicators (Implemented)

| Colour | CSS Class | Status | Meaning |
|--------|-----------|--------|---------|
| 🟢 Green gradient | `status-healthy` | `healthy` | All components operating normally |
| 🟡 Amber gradient | `status-degraded` | `degraded` | One non-critical component has issues |
| 🔴 Red gradient | `status-unhealthy` | `unhealthy` | One or more critical components failed |
| ⚪ Grey gradient | `status-unknown` | fetch error | Health endpoint unreachable |

The entire status banner background changes colour — health state is visible without reading text.

### 8.3 Error Handling

If `/health/detailed` cannot be reached:
- An error banner appears at the top of the page
- The last known health data is preserved (dashboard is not cleared)
- The auto-refresh timer continues trying every 30 seconds

---

## 9. Monitoring Under Uncertainty

Technical monitoring addresses the course concept of **management under uncertainty** by:

1. **Making unknowns visible** — the `/health/detailed` endpoint surfaces hidden internal states
2. **Early warning** — P95 response time alerts fire before users notice slowness
3. **Non-deterministic failures** — error rate thresholds catch intermittent failures
4. **Audit trail** — changes are immutably recorded so post-incident analysis is possible
5. **Container self-healing** — Docker health checks and restart policies reduce MTTR (Mean Time to Recovery)

**Key Uncertainty Mitigations:**
- Rate limiting (100 req/hour) prevents traffic spikes from overwhelming the system
- Database connection pooling prevents cascading DB failures
- JWT token expiry + refresh mechanism handles stale sessions gracefully
- All external inputs validated with Pydantic before reaching business logic

---

## 10. Continuous Integration as a Monitoring Tool

The GitHub Actions pipelines serve as the first monitoring layer — they detect quality regressions before deployment:

| Pipeline | Trigger | What it Monitors |
|----------|---------|-----------------|
| `backend.yml` | Push to any branch | pytest results, test coverage |
| `frontend.yml` | Push to any branch | Vitest unit tests, production build success |

A failing CI pipeline is a monitoring signal — it means a quality regression was introduced and must be fixed before merge.

**CI Health Dashboard** (GitHub Actions tab):
- Green checkmarks = code quality maintained
- Red ✗ = regression detected — merge blocked until fixed
