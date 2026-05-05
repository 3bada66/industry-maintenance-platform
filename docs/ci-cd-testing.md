# CI/CD Pipeline and Continuous Testing
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 2.0
**Owner:** Hamdi Alnaqeeb (DevOps/Operations Engineer, 2309116178)
**Supporting:** Praise-God Tobby (QA/Test Engineer, 2309116418)

---

## 1. Overview

This document describes the complete Continuous Integration, Continuous Delivery, and testing infrastructure for Industry Maintenance Platform. All pipelines and tools run on GitHub's free tier or locally — **no paid services are used**.

The CI/CD system serves two purposes:
1. **Quality gate** — prevents regressions from reaching the main branch
2. **Monitoring signal** — a failing pipeline is a technical event that must be investigated before the sprint ends

### 1.1 What Exists vs. What Is Planned

| Component | Status | File |
|-----------|--------|------|
| Backend CI (pytest + syntax check) | **Implemented** | `.github/workflows/backend.yml` |
| Frontend CI (Vitest + Vite build) | **Implemented** | `.github/workflows/frontend.yml` |
| Backend unit + integration tests | **Implemented** | `backend/tests/` (4 files) |
| Frontend unit tests (Vitest) | **Implemented** | `frontend/src/composables/__tests__/useStatus.spec.js` |
| Vitest environment config | **Implemented** | `frontend/vite.config.js` — `test` block |
| Local Docker CD | **Implemented** | `Makefile` + Docker Compose |
| End-to-end tests (Cypress) | **Planned** | Package installed; no test files yet |
| ESLint / code style check | **Planned** | Not yet configured |

---

## 2. Continuous Integration

### 2.1 Backend CI Pipeline

**File:** `.github/workflows/backend.yml`
**Owner:** Hamdi Alnaqeeb
**Trigger:** Push or pull request to any branch

**Steps:**

| Step | Command | What it validates |
|------|---------|------------------|
| Install dependencies | `pip install -r requirements.txt` | All Python packages resolve without conflict |
| Syntax & import check | `python -m py_compile app/main.py` + `python -c "from app.main import app"` | No syntax errors; application imports successfully |
| Run tests with coverage | `pytest tests/ -v --cov=app --cov-report=term-missing` | All tests pass; coverage report printed to CI log |

**PostgreSQL service:** The workflow starts a real PostgreSQL 15 container via GitHub Actions `services:`. The backend tests connect to this container — no mocking of database calls. This is intentional: mocked database tests allowed a schema migration to break production undetected in a prior project; real DB tests catch this class of error.

**Environment variables in CI:**

| Variable | CI Value | Purpose |
|----------|----------|---------|
| `DATABASE_URL` | `postgresql://test:test@localhost:5432/testdb` | Connect to the CI PostgreSQL service |
| `SECRET_KEY` | `test-secret-key-for-ci-only` | JWT signing; never the production key |
| `ENVIRONMENT` | `test` | Disables demo data seeding, relaxes cert checks |
| `PYTHONPATH` | `${{ github.workspace }}/backend` | Allows `from app.X import Y` without install |

**Full workflow YAML:**

```yaml
name: Backend CI
on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
          cache: "pip"
          cache-dependency-path: backend/requirements.txt
      - name: Install dependencies
        run: cd backend && pip install -r requirements.txt
      - name: Syntax and import check
        env:
          PYTHONPATH: ${{ github.workspace }}/backend
        run: |
          cd backend
          python -m py_compile app/main.py
          python -m py_compile app/database.py
          python -m py_compile app/config.py
          python -c "from app.main import app; print('app import OK')"
      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          SECRET_KEY: test-secret-key-for-ci-only
          ENVIRONMENT: test
          PYTHONPATH: ${{ github.workspace }}/backend
        run: cd backend && pytest tests/ -v --cov=app --cov-report=term-missing --tb=short
```

### 2.2 Frontend CI Pipeline

**File:** `.github/workflows/frontend.yml`
**Owner:** Hamdi Alnaqeeb
**Trigger:** Push or pull request to any branch

**Steps:**

| Step | Command | What it validates |
|------|---------|------------------|
| Install dependencies | `npm ci` | Exact versions from `package-lock.json`; clean install |
| Run unit tests | `npm run test:unit` | All Vitest tests pass |
| Build production bundle | `npm run build` | No broken imports, missing assets, or Vite build errors |

**Full workflow YAML:**

```yaml
name: Frontend CI
on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json
      - run: cd frontend && npm ci
      - run: cd frontend && npm run test:unit
      - run: cd frontend && npm run build
```

**Vitest environment configuration** (`frontend/vite.config.js`):

```javascript
test: {
  globals: true,
  environment: 'jsdom',
  include: ['src/**/*.{spec,test}.{js,ts}'],
},
```

`jsdom` is installed as a dev dependency. `globals: true` makes `describe`, `it`, `expect` available without explicit imports in test files.

### 2.3 CI Quality Gates

| Gate | Condition | Action on Failure |
|------|-----------|-------------------|
| Backend syntax check | `py_compile` fails | PR blocked — fix syntax error |
| Backend import check | `from app.main import app` fails | PR blocked — fix broken import |
| Backend tests | Any pytest assertion fails | PR blocked — fix test |
| Frontend unit tests | Any Vitest assertion fails | PR blocked — fix test |
| Frontend build | `npm run build` fails | PR blocked — fix broken import or component |
| Coverage report | Coverage < 70 % | Advisory warning in CI log; does not block |

---

## 3. Continuous Delivery — Local/Self-Hosted

Industry Maintenance Platform uses a **local CD model**. Deployment is performed on the operator's machine using Docker Compose and the `Makefile`. No cloud services, no paid hosting, no external runners.

### 3.1 CD Pipeline Steps

```
Developer pushes code to branch
         │
         ▼
CI runs automatically (GitHub Actions — free tier)
  ├── Backend: syntax check + pytest + coverage
  └── Frontend: Vitest + Vite build
         │
         ▼
CI passes (all checks green)
         │
         ▼
Code review and merge to main
         │
         ▼
Deployment on local / staging machine:
  make prod
  (Docker builds images → starts containers → Alembic migrates DB)
         │
         ▼
Health check confirms deployment:
  curl -k https://localhost/health
  → {"status": "ok", "database": "connected", ...}
         │
         ▼
Smoke tests confirm functionality:
  curl -k https://localhost/health/detailed
  POST /login with admin credentials
  GET /api/v1/assets/
         │
         ▼
Technical Monitoring Dashboard at /monitoring
  confirms: Healthy status, DB connected, uptime increasing
         │
         ▼
System stable — deployment complete
```

### 3.2 Deployment Command Reference

```bash
# Full production deployment (Nginx + self-signed TLS)
make prod

# Start Traefik + Let's Encrypt (cloud / staging)
make prod-cloud

# Seed demo data (8 assets, 3 sites, full network topology)
make demo

# Confirm all containers are running and healthy
make status

# View real-time logs from all services
make logs

# Stop all services (data preserved)
make stop

# Remove all containers and volumes (destructive — deletes DB data)
make clean
```

### 3.3 Rollback Procedure

```bash
# 1. Stop the failing deployment
make stop

# 2. Revert to the previous commit (or tag)
git checkout <previous-tag-or-sha>

# 3. Rebuild and redeploy
make prod

# 4. Confirm health
curl -k https://localhost/health
```

### 3.4 Deployment Environment Variables

| Variable | Default | Production Requirement |
|----------|---------|----------------------|
| `SECRET_KEY` | — | Must be changed; startup fails if default |
| `DATABASE_URL` | `postgresql://industry-maintenance-platform_user:...@db:5432/industry-maintenance-platform` | Set in `.env` |
| `ENVIRONMENT` | `production` | Must be `production` for `SECURE_COOKIES=true` |
| `SECURE_COOKIES` | `false` | Must be `true` in production |
| `CORS_ORIGINS` | `https://localhost` | Set to actual deployment URL |
| `SEED_DEMO_DATA` | `false` | Set `true` for demo deployments only |

Secrets are loaded from `.env` — never committed to git. `.env.example` is committed and documents all variables.

---

## 4. Continuous Testing Strategy

**Owner:** Praise-God Tobby (QA/Test Engineer)

### 4.1 Testing Pyramid

```
             ┌─────────────┐
             │  E2E Tests   │  Cypress — installed, test files planned
             │  (planned)   │  Would cover login → asset → monitoring flows
            ┌┴─────────────┴┐
            │  Integration  │  pytest — assets + auth + multi-step flows
            │   Tests       │  backend/tests/test_comprehensive.py
           ┌┴───────────────┴┐
           │   Unit Tests    │  pytest (backend) + Vitest (frontend)
           │   (most)        │  backend/tests/test_health.py + useStatus.spec.js
           └─────────────────┘
```

### 4.2 Backend Tests — Current State

**Location:** `backend/tests/`
**Framework:** pytest 7.4.3 + pytest-cov 4.1.0 + httpx 0.25.2
**Run command:** `pytest tests/ -v --cov=app --cov-report=term-missing`

| File | Type | What it tests |
|------|------|--------------|
| `test_health.py` | Unit + API | `GET /health` — status, database, uptime, timestamp format, no-auth; `GET /health/detailed` — all 10 required monitoring metrics |
| `test_auth.py` | API + Security | Login, token refresh, logout, invalid credentials, expired tokens |
| `test_users.py` | API + RBAC | User CRUD, role assignment, permission checks |
| `test_comprehensive.py` | Integration | Asset creation, site/area/location hierarchy, multi-step workflows with real PostgreSQL |

**All tests use a real PostgreSQL 15 instance** (via Docker in CI, local PostgreSQL in development). The `get_db` dependency is overridden to point to the test database.

### 4.3 Unit Tests — `test_health.py` (selected examples)

```python
class TestBasicHealth:
    def test_health_status_is_ok(self):
        assert client.get("/health").json()["status"] == "ok"

    def test_health_database_is_connected(self):
        assert client.get("/health").json()["database"] == "connected"

    def test_health_timestamp_is_utc(self):
        assert client.get("/health").json()["timestamp"].endswith("Z")

    def test_health_no_auth_required(self):
        assert client.get("/health").status_code == 200

class TestDetailedHealth:
    def test_detailed_health_database_is_healthy(self):
        data = client.get("/health/detailed").json()
        assert data["components"]["database"]["status"] == "healthy"

    def test_detailed_health_has_response_time(self):
        db = client.get("/health/detailed").json()["components"]["database"]
        assert isinstance(db["response_time_ms"], (int, float))
        assert db["response_time_ms"] >= 0
```

### 4.4 API Tests — `test_comprehensive.py` (selected examples)

```python
def test_create_asset_returns_201(auth_client, test_site, ...):
    response = auth_client.post("/api/v1/assets/", json={...})
    assert response.status_code == 201
    assert response.json()["name"] == "Test PLC"

def test_viewer_role_cannot_delete_asset(viewer_client, asset_id):
    response = viewer_client.delete(f"/api/v1/assets/{asset_id}")
    assert response.status_code == 403
```

### 4.5 Frontend Tests — Current State

**Location:** `frontend/src/composables/__tests__/useStatus.spec.js`
**Framework:** Vitest 0.34.0 + jsdom 22.1.0
**Run command:** `npm run test:unit`
**Configuration:** `vite.config.js` — `test: { globals: true, environment: 'jsdom' }`

The test file covers 20 assertions across four functions of the `useStatus` composable:

| Function | Tests | What is asserted |
|----------|-------|-----------------|
| `getContrastColor` | 4 | Black/white background → correct text contrast colour |
| `getStatusSeverity` (color) | 9 | `#28a745` → `success`; `#ef4444` → `danger`; named colors |
| `getStatusSeverity` (name) | 10 | `"active"` → `success`; `"fault"` → `danger`; Italian names |
| `getStatusColor` | 3 | Null → default gray; present color → returned; no color → default |
| `getStatusLabel` | 3 | Null → `"-"`; name present → returned; missing name → `"-"` |

**`vue-i18n` mock pattern:**
```javascript
vi.mock('vue-i18n', () => ({
  useI18n: () => ({ t: (key) => key }),
}))
```
This is required because `useStatus` calls `useI18n()` at the top of its factory function, even though none of the tested functions call `t()`.

### 4.6 Smoke Tests — Post-Deployment

Run these after every `make prod` before announcing the deployment complete:

```bash
# 1. Basic liveness
curl -k https://localhost/health
# Expected: {"status": "ok", "database": "connected", "uptime": "running", ...}

# 2. Full health check
curl -k https://localhost/health/detailed
# Expected: {"status": "healthy", "components": {"database": {"status": "healthy"}}}

# 3. Login
curl -k -c /tmp/ci_cookies.txt -X POST https://localhost/login \
  -F "email=admin@example.com" -F "password=admin123"
# Expected: 200 with access_token

# 4. Authenticated endpoint
curl -k -b /tmp/ci_cookies.txt https://localhost/api/v1/assets/
# Expected: {"items": [...], "total": N}

# 5. Open Technical Monitoring Dashboard
# Navigate to https://localhost/monitoring
# Expected: green "HEALTHY" banner
```

### 4.7 Regression Tests

Regression testing is handled by running the full pytest suite on every push:

```bash
pytest tests/ -v --tb=short
```

Any feature that worked in a previous sprint and breaks now will be caught by the existing test suite. New features introduced in a sprint must include at least one test that would fail if the feature were removed.

**Regression test checklist per sprint:**

| Check | Command | Pass condition |
|-------|---------|----------------|
| Health endpoint | `pytest tests/test_health.py -v` | All 15 assertions pass |
| Authentication | `pytest tests/test_auth.py -v` | All auth scenarios pass |
| Asset CRUD | `pytest tests/test_comprehensive.py -v` | Create/read/update/delete pass |
| Frontend build | `npm run build` | No build errors |
| Frontend composables | `npm run test:unit` | All 20 Vitest assertions pass |

### 4.8 Tests That Should Be Added

The following tests are missing and should be added before the final submission. They are listed in priority order:

| Missing Test | File to Create | Why It Matters |
|-------------|---------------|----------------|
| `GET /api/v1/management/status` | `backend/tests/test_management.py` | Verifies the management monitoring endpoint returns all required fields with correct types |
| Risk scoring computation | `backend/tests/test_risk_scoring.py` | Core business logic; verifies `risk_scoring.py` produces correct scores for known inputs |
| Asset risk score updates on edit | `backend/tests/test_comprehensive.py` extension | Verifies that editing a Purdue level recalculates the risk score |
| Frontend `RiskDashboard.vue` render | `frontend/src/pages/__tests__/RiskDashboard.spec.js` | Smoke test that the page mounts without errors |
| Frontend `ManagementMonitoring.vue` render | `frontend/src/pages/__tests__/ManagementMonitoring.spec.js` | Smoke test that the page mounts without errors |

---

## 5. Continuous Testing Principles

### 5.1 Unit Tests

Test individual functions in isolation. For backend: CRUD helper functions, risk scoring computation, JWT utilities. For frontend: composable pure functions (covered by `useStatus.spec.js`).

**Rule:** A unit test must not depend on a database, an HTTP server, or a running Vue application.

### 5.2 API Tests

Test HTTP endpoints end-to-end through the FastAPI test client against a real PostgreSQL database. Verify status codes, response shapes, and RBAC enforcement.

**Rule:** API tests must connect to a real database. Mocking the database layer defeats the purpose of API tests and has historically allowed schema-breaking changes to pass CI.

### 5.3 Integration Tests

Test multi-step workflows that span more than one endpoint or more than one database table. Example: create a site → create an area in that site → create an asset in that area → verify the asset's `site_name` in the response.

**Rule:** Integration tests must be idempotent — they must clean up their data in a `teardown` or via `drop_all` so they can be run multiple times.

### 5.4 UI Tests (Planned — Cypress)

Test complete user flows in a browser: login → navigate to a page → perform an action → verify the result. Cypress 12.0.0 is installed (`devDependencies`) but no test files exist yet.

**Planned flows:**
- Login with valid credentials → dashboard renders
- Create asset → asset appears in assets list
- Navigate to `/monitoring` → health status badge is visible
- Navigate to `/risk` → risk KPI tiles render

### 5.5 Smoke Tests After Deployment

Defined in §4.6. Run manually after every deployment. The four `curl` commands confirm that the system is alive, the database is connected, authentication works, and the main API is responding.

### 5.6 Continuous Testing — Not Just Pre-Merge

Testing runs at three points in the development cycle:

| When | What runs | Who triggers |
|------|-----------|-------------|
| On every push | Full CI pipeline (syntax + tests + build) | Automatic (GitHub Actions) |
| After every `make prod` | Smoke test sequence | DevOps engineer manually |
| Every sprint retro | Coverage review; test gap analysis | QA engineer reviews CI logs |

---

## 6. No-Paid-Services Guarantee

| Tool | Cost | Version Used |
|------|------|-------------|
| GitHub Actions | Free (2,000 min/month for private repos) | — |
| Docker Desktop | Free for personal/education use | — |
| PostgreSQL 15 | Free (open source) | postgres:15 |
| pytest | Free (open source) | 7.4.3 |
| pytest-cov | Free (open source) | 4.1.0 |
| Vitest | Free (open source) | 0.34.0 |
| jsdom | Free (open source) | 22.1.0 |
| @vue/test-utils | Free (open source) | 2.3.0 |
| Cypress | Free (open source) | 12.0.0 |
| Nginx | Free (open source) | alpine |

**Total infrastructure cost: €0.**
