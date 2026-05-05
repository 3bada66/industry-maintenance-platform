# Software Design and Analysis
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.0
**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)
**Supporting:** Mohanad Aref Ali Sultan (Backend Developer, 2309115898) · Zekeriya Dulli (Frontend Developer, 2309115377)

---

## 1. Architecture Overview

Industry Maintenance Platform follows a **three-tier architecture**: a Vue.js 3 single-page application in the browser, a FastAPI REST backend, and a PostgreSQL 15 database. The three tiers are decoupled and communicate only through defined interfaces — HTTP/JSON for the browser-to-backend boundary, and SQLAlchemy sessions for the backend-to-database boundary.

```
┌─────────────────────────────────────────────────────────────────┐
│  Browser (Vue.js 3 SPA)                                         │
│  ┌─────────┐ ┌────────────┐ ┌──────────────┐ ┌─────────────┐  │
│  │  Pages  │ │ Components │ │ Composables  │ │  api.js     │  │
│  └────┬────┘ └─────┬──────┘ └──────┬───────┘ └──────┬──────┘  │
│       └────────────┴───────────────┴────────────────▼          │
│                                               axios / fetch     │
└───────────────────────────────────────────────────┬─────────────┘
                                                    │ HTTPS / JSON
┌───────────────────────────────────────────────────▼─────────────┐
│  FastAPI Backend (Python 3.8+)                                  │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Routers  │→ │  Schemas   │→ │  CRUD    │→ │  Models      │  │
│  │ (31)     │  │ (Pydantic) │  │  (22)    │  │ (SQLAlchemy) │  │
│  └──────────┘  └────────────┘  └──────────┘  └──────┬───────┘  │
│  ┌──────────┐  ┌────────────┐                        │          │
│  │ Services │  │ JWT / RBAC │                        │          │
│  └──────────┘  └────────────┘                        │          │
└──────────────────────────────────────────────────────┬──────────┘
                                                       │ SQLAlchemy
┌──────────────────────────────────────────────────────▼──────────┐
│  PostgreSQL 15                                                   │
│  24 tables · multi-tenant (tenant_id FK) · Alembic migrations   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Backend Structure

### 2.1 Entry Point — `backend/app/main.py`

`main.py` is the FastAPI application factory. It performs four functions:

1. Creates the `FastAPI` app instance with title, version, and description
2. Registers CORS middleware from `settings.CORS_ORIGINS`
3. Registers all 31 `APIRouter` instances
4. Defines inline the three system-level endpoints (`/health`, `/health/detailed`, `/login`, `/refresh`, `/logout`) that do not fit within a domain router
5. Runs the Alembic auto-migration on startup via `@app.on_event("startup")`

The startup event also seeds demo data when `ENVIRONMENT=development` and the database is empty.

### 2.2 Routing Layer — `backend/app/routers/`

Each file in `routers/` is a self-contained `APIRouter` instance. There are 31 routers covering every domain:

| Group | Routers |
|-------|---------|
| **Asset domain** | `assets`, `asset_types`, `asset_statuses`, `asset_interfaces`, `asset_connections`, `asset_documents`, `asset_photos`, `asset_communications`, `global_connections` |
| **Location domain** | `sites`, `areas`, `locations`, `locations_floormap` |
| **Supply chain** | `suppliers`, `manufacturers`, `contacts` |
| **Access control** | `users`, `roles`, `tenants`, `api_keys` |
| **Platform** | `audit_logs`, `dashboards`, `search`, `setup`, `smtp_config` |
| **Specialised** | `pcap`, `print`, `external_api`, `performance_test` |
| **Monitoring** | `management_monitoring` |

All routers follow the same dependency injection pattern:

```python
@router.get("/{id}")
def get_entity(
    id: int,
    current_user: User = Depends(get_current_user),   # auth + RBAC
    db: Session = Depends(get_db),                    # DB session
):
```

### 2.3 Schema Layer — `backend/app/schemas/`

26 Pydantic schema files. Each domain entity has at least three schema classes:

- `*Base` — shared fields
- `*Create` — fields required for POST
- `*Update` — fields accepted for PUT/PATCH (all optional)
- `*Response` — fields returned in the JSON response (including computed fields like `risk_score`)

Pydantic validates all input before it reaches the CRUD layer and serialises all output before it leaves the router.

### 2.4 CRUD Layer — `backend/app/crud/`

22 files, one per domain entity. Each file contains pure database functions that accept a `Session` and typed arguments. Routers never call SQLAlchemy directly — they call CRUD functions. This separation means the same CRUD functions can be called from the API, from init scripts, and from tests.

### 2.5 Model Layer — `backend/app/models/`

24 SQLAlchemy ORM model files. Key design properties:

- **Multi-tenancy:** Every entity that belongs to an organisation has a `tenant_id` column with a foreign key to the `Tenant` model. All queries filter by `tenant_id` extracted from the authenticated user's JWT.
- **Soft delete:** Assets, areas, locations, and sites use a `deleted_at` timestamp column. Deleted records are excluded from queries but retained in the database for audit purposes.
- **Audit trail:** Every write operation is wrapped by an audit decorator that inserts a row into the `audit_logs` table with the user ID, tenant ID, IP address, timestamp, entity type, operation, and before/after diff.

### 2.6 Services Layer — `backend/app/services/`

Business logic that does not belong in a single CRUD file:

| Service | Purpose |
|---------|---------|
| `risk_scoring.py` | Computes ICS risk score from Purdue level, criticality, access type, vulnerability score |
| `auth_service.py` | Password hashing, JWT creation and validation |
| `audit_service.py` | Audit log writing decorator / context manager |
| `email_service.py` | SMTP and third-party email dispatch (SendGrid, Gmail, SES) |

### 2.7 Configuration — `backend/app/config.py`

A single Pydantic `Settings` class reads all configuration from environment variables. The application imports `settings` as a module-level singleton. Production validation is built into the Settings class: it raises at startup if `SECRET_KEY` is still the default, `DEBUG=True`, or `SECURE_COOKIES=False`.

### 2.8 Error Handling — `backend/app/errors/`

A custom exception system with:

- `ErrorCodeException`: raised with a code string (e.g., `ASSET_NOT_FOUND`)
- `error_codes.py`: maps codes to HTTP status codes
- `translations.py`: maps codes to localised messages in EN and IT
- Global exception handlers in `main.py` catch `ErrorCodeException`, `RequestValidationError`, and `Exception` and convert them to consistent JSON error responses

---

## 3. Frontend Structure

### 3.1 Pages — `frontend/src/pages/`

25+ Vue 3 single-file components (SFCs), one per application screen. Each page is responsible for:

1. Fetching its data from `api.js`
2. Composing the layout from base and feature components
3. Handling user actions (create, edit, delete, search, paginate)

Pages use the Composition API (`<script setup>`) throughout. State is local (`ref`, `reactive`) except authentication, which is in the Pinia `auth` store.

### 3.2 Components — `frontend/src/components/`

Organised into four layers:

| Layer | Location | Purpose |
|-------|----------|---------|
| **Base** | `components/base/` | `BaseDataTable`, `BaseDialog`, `BaseForm`, `BaseConfirmDialog` — generic wrappers around PrimeVue primitives |
| **Common** | `components/common/` | `SidebarMenu`, `BaseFooter`, `CriticalityBadge`, `GlobalSearchSpotlight` |
| **Feature** | `components/features/assets/` | 30+ asset-specific display and edit components |
| **Dialog** | `components/dialogs/` | Import wizards (Asset, Contact, Manufacturer, Supplier), Password Reset, PCAP import |

### 3.3 API Layer — `frontend/src/api/api.js`

A single Axios instance configured with:

- `baseURL: '/api'` — relative path so the SPA works behind any reverse proxy
- `withCredentials: true` — sends the `access_token` HTTP-only cookie automatically
- A response interceptor that calls `auth.logout()` on any 401, sending the user to `/login`

All API calls in the application go through the methods exported from this file. Pages never call `axios` directly.

### 3.4 Routing — `frontend/src/router.js`

Vue Router 4 with 28 routes. All routes except `/login` have `meta: { requiresAuth: true }`. The `beforeEach` guard calls `GET /users/me` to verify the cookie is valid before allowing navigation. If the call fails, the user is redirected to `/login`.

### 3.5 Composables — `frontend/src/composables/`

13 composables encapsulate reusable logic that crosses multiple pages:

| Composable | Responsibility |
|-----------|---------------|
| `useApi` | Generic error handling wrapper for API calls |
| `useStatus` | Maps backend status strings to PrimeVue severity levels |
| `usePermissions` | Checks whether the current user's role allows an action |
| `useFilters` | Shared filter state for table views |
| `useGlobalSearch` | Spotlight search state and keyboard shortcut handler |
| `usePrint` | Print dialog state and PDF trigger |
| `useDuplicate` | Asset duplication workflow |
| `useDateFormatter` | Locale-aware date formatting |
| `useCriticality` | Maps criticality integer to label and colour |

### 3.6 Localisation — `frontend/src/locales/`

40 JSON files split into `en/` and `it/` directories. Every user-visible string is a translation key looked up via `vue-i18n`'s `t()` function. The sidebar menu keys (`menu.navigation.*`, `menu.section.*`) are critical — a missing key causes the sidebar to render `undefined` as a label rather than throwing an error.

---

## 4. Database Structure

### 4.1 Connection and Sessions

`database.py` creates a single SQLAlchemy `engine` from `DATABASE_URL` and a `SessionLocal` factory. Each request gets its own session via `Depends(get_db)`, which yields a session and guarantees `db.close()` in the finally block regardless of whether the request succeeds or raises.

### 4.2 Entity Model

24 tables across five domains:

| Domain | Tables |
|--------|--------|
| **Assets** | `assets`, `asset_types`, `asset_statuses`, `asset_interfaces`, `asset_connections`, `asset_communications`, `asset_documents`, `asset_photos` |
| **Location** | `sites`, `areas`, `locations` |
| **Supply chain** | `suppliers`, `manufacturers`, `contacts` |
| **Access control** | `users`, `roles`, `tenants`, `api_keys` |
| **Platform** | `audit_logs`, `print_templates`, `print_history`, `tenant_smtp_config` |

### 4.3 Multi-Tenancy

Every entity that belongs to an organisation carries a `tenant_id` foreign key. The `get_current_user` dependency extracts `tenant_id` from the JWT and passes it into every CRUD call. There is no cross-tenant data leakage path at the ORM layer.

### 4.4 Migrations

Alembic manages the schema lifecycle. Migration scripts live in `alembic/versions/`. The startup event in `main.py` runs `alembic upgrade head` automatically, so the schema is always current when the container starts. The `/health/detailed` endpoint reports `alembic current` as the `deployment_status` field.

---

## 5. API Structure

### 5.1 URL Convention

All domain endpoints follow the pattern:

```
/api/v1/{resource}           GET (list), POST (create)
/api/v1/{resource}/{id}      GET (detail), PUT (update), DELETE (delete)
/api/v1/{resource}/trash     GET (soft-deleted items)
/api/v1/{resource}/{id}/restore  POST (restore from trash)
```

System endpoints live at the root without the `/api/v1` prefix:

```
/health            GET — basic health (no auth)
/health/detailed   GET — full system metrics (no auth)
/login             POST — form-based login
/refresh           POST — token refresh
/logout            POST — logout
/docs              GET — Swagger UI (OpenAPI)
/redoc             GET — ReDoc UI
```

### 5.2 Authentication Flow

1. Client POSTs credentials to `/login`
2. Backend verifies password hash via `passlib`/`bcrypt`
3. Backend returns a short-lived JWT (`ACCESS_TOKEN_EXPIRE_MINUTES`, default 30) in an HTTP-only `SameSite=Lax` cookie
4. All subsequent requests include the cookie automatically (Axios `withCredentials: true`)
5. `GET /refresh` issues a new access token using a longer-lived refresh token
6. `POST /logout` deletes both cookies server-side and writes an audit log entry

### 5.3 RBAC

Roles are stored in the `roles` table with a JSON `permissions` column. The `get_current_user` dependency loads the user's role and attaches it to the `current_user` object. Permission checks are done inside router handlers using `usePermissions` (frontend) and direct role lookups (backend).

### 5.4 API Keys

For machine-to-machine integration, the `api_keys` router manages API keys with the prefix `ind_`. Keys are stored as bcrypt hashes. The backend accepts keys via the `X-API-Key` header as an alternative to the cookie-based JWT flow.

### 5.5 Rate Limiting

`slowapi` 0.1.9 is configured with a default rate limit of `100/hour` per IP. The `RATE_LIMIT_ENABLED` setting can disable limiting in development.

### 5.6 OpenAPI Documentation

FastAPI auto-generates OpenAPI 3.0 documentation. The Swagger UI is available at `/docs` and ReDoc at `/redoc`. Every endpoint has typed request and response models derived from the Pydantic schemas, so the documentation is always in sync with the implementation.

---

## 6. Authentication and Security

| Control | Implementation |
|--------|---------------|
| **Password storage** | bcrypt via `passlib` — no plaintext or reversible hashing |
| **JWT** | HS256 signed with `SECRET_KEY`; claims include `sub` (user ID), `tenant_id`, `role`, `iss`, `aud`, `exp` |
| **Token delivery** | HTTP-only `SameSite=Lax` cookie — not accessible to JavaScript, not sent cross-origin |
| **Token refresh** | Separate refresh token with longer expiry; `/refresh` endpoint rotates both tokens |
| **CORS** | `CORSMiddleware` whitelists `CORS_ORIGINS` from settings; credentials mode requires explicit origin, not wildcard |
| **Rate limiting** | `slowapi` 100/hour per IP on login and all API endpoints |
| **Role-based access** | Role permissions checked server-side on every mutating request; the frontend only hides UI elements |
| **Input validation** | All request bodies parsed through Pydantic schemas before reaching business logic; Pydantic raises 422 on any type or constraint violation |
| **Audit logging** | Every CREATE, UPDATE, DELETE records user ID, tenant ID, IP address, timestamp, and before/after diff in `audit_logs` |
| **Soft delete** | Records are flagged `deleted_at` rather than removed; hard delete is an explicit separate operation |
| **Production checks** | `config.py` raises at startup if `SECRET_KEY` is default, `DEBUG=True`, or `SECURE_COOKIES=False` |

---

## 7. Main Modules and Data Flow

### 7.1 Asset Creation Flow

```
Browser → POST /api/v1/assets (JSON body)
  → FastAPI: validate cookie → get_current_user (loads user + role + tenant_id)
  → Router: parse body through AssetCreate Pydantic schema
  → CRUD: assets.create_asset(db, asset_in, tenant_id=current_user.tenant_id)
    → risk_scoring.compute_risk_score(asset) → sets asset.risk_score
    → db.add(asset) → db.commit()
    → audit_service: writes audit_log row (operation=CREATE, entity=Asset, diff=new_values)
  → Router: return AssetResponse schema → FastAPI serialises to JSON
Browser ← 201 JSON response
```

### 7.2 Dashboard Load Flow

```
Browser → GET /api/v1/dashboards/summary
  → FastAPI: get_current_user
  → Router: calls multiple CRUD count queries (assets, sites, areas, high-risk count)
  → Returns aggregated summary object
Browser ← JSON summary → Dashboard.vue renders KPI tiles
```

### 7.3 Health Check Flow (Technical Monitoring)

```
TechnicalMonitoring.vue: setInterval(30s) → axios.get('/health/detailed')
  → No auth required
  → main.py: run db.execute("SELECT 1"), measure response_time_ms
  → Import psutil → cpu_percent, memory_percent, disk_percent
  → Return structured JSON
TechnicalMonitoring.vue: update ref(data) → Vue reactivity re-renders dashboard
```

### 7.4 Management Monitoring Flow

```
ManagementMonitoring.vue: setInterval(60s) → api.getManagementStatus()
  → auth cookie sent → get_current_user verifies JWT
  → management_monitoring.py: query db for live asset count (func.count)
  → Merge static project data with live count → return JSON
ManagementMonitoring.vue: update ref(data) → render KPI tiles, tables, progress bars
```

---

## 8. Deployment Structure

### 8.1 Docker Compose

The project ships with multiple Compose configurations:

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Production with Traefik + Let's Encrypt (cloud) |
| `docker-compose.prod.yml` | Production with Nginx + self-signed certificates (local) |
| `docker-compose.dev.yml` | Development with hot reload |

All configurations define the same four services:

| Service | Image | Exposed Port | Notes |
|---------|-------|-------------|-------|
| `db` | `postgres:15` | 5432 (internal) | Named volume `industry-maintenance-platform_postgres_data` |
| `backend` | Built from `backend/Dockerfile` | 8000 (internal) | Mounts `uploads/` and `logs/` volumes |
| `frontend` | Built from `frontend/Dockerfile` | 80/443 (external) | Nginx serves the Vite build |
| `traefik` / `nginx` | `traefik:v2.10` / `nginx:alpine` | 80, 443 | TLS termination; proxies `/api/` to backend |

### 8.2 Container Health Checks

```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-START", "pg_isready", "-U", "industry-maintenance-platform_user"]
  interval: 10s
  timeout: 5s
  retries: 5

# Backend
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

The backend `depends_on: db: condition: service_healthy` ensures FastAPI does not start before PostgreSQL is ready.

### 8.3 Makefile Commands

```
make prod         Start production (Nginx + self-signed cert + auto-init DB)
make prod-cloud   Start production (Traefik + Let's Encrypt)
make demo         Seed demo data into running system
make clean        Remove all containers and volumes
make test         Run pytest suite
make migrate      Run alembic upgrade head
make reset-db     Drop and recreate database (destructive)
make logs         Tail all service logs
make status       Show container health
```

---

## 9. How the Design Supports Quality Attributes

### 9.1 Maintainability

**Modular structure:** 31 routers, 22 CRUD files, 26 schema files, and 24 model files each address exactly one domain entity. A change to the `Asset` model does not require reading or modifying supplier or user code.

**Separation of concerns:** The four layers (Router → Schema → CRUD → Model) have distinct responsibilities and communicate through typed interfaces. A new developer reading the code can understand what each layer does without reading any other layer.

**Reusable components:** The 13 frontend composables (`useApi`, `usePermissions`, `useFilters`, etc.) centralise cross-cutting concerns. Adding a new page does not require rewriting permission checks or error handling from scratch. The `BaseDataTable`, `BaseDialog`, and `BaseForm` components standardise interaction patterns across all 25 pages.

**Clear API boundaries:** The OpenAPI schema at `/docs` is the contract between the frontend and backend. Because the schema is generated from Pydantic models, it is always current. Any breaking change to a response model appears immediately in the documentation.

**Documentation:** 30 markdown files in `docs/` cover architecture, API reference, installation, development setup, security, monitoring, risk management, value creation, and stakeholder management.

### 9.2 Scalability

**Database scalability:** PostgreSQL 15 supports read replicas via streaming replication. The SQLAlchemy `create_engine` call can be swapped for a connection pool pointing at a primary/replica cluster without changing any business logic. New indexes can be added via Alembic migrations without downtime on PostgreSQL.

**API scalability:** FastAPI with Uvicorn runs as an ASGI application. Multiple backend containers can be run behind the Nginx/Traefik load balancer; all session state is in the database (no sticky sessions required). The JWT-based authentication does not require a shared session store.

**Frontend/backend separation:** The frontend is a static Vite build served by Nginx. It can be deployed to a CDN without any backend changes. The backend can scale independently.

**Docker readiness:** All services are containerised with health checks and restart policies. `docker-compose up --scale backend=3` would run three backend replicas behind the proxy. *(Horizontal auto-scaling is not configured in the current Compose files — this would be a planned enhancement for production deployments.)*

**Rate limiting:** `slowapi` protects the API from abuse at the application layer. In a scaled deployment, the rate limiter state would need to move to Redis (already a listed dependency in `requirements.txt`, currently used for optional caching).

### 9.3 Cohesion

Each module group has a single, well-defined responsibility:

| Module Group | Responsibility | Files |
|-------------|---------------|-------|
| Asset features | Full lifecycle: creation, editing, interfaces, connections, photos, documents, risk scoring | `routers/assets.py`, `crud/assets.py`, `services/risk_scoring.py`, `models/asset.py`, `pages/Assets.vue`, `pages/AssetDetail.vue`, `components/features/assets/` |
| Risk features | Risk score computation, risk dashboard KPIs, risk register documentation | `services/risk_scoring.py`, `routers/dashboards.py`, `docs/risk-management.md` |
| User / Auth features | Login, token lifecycle, RBAC, API keys | `main.py` (auth endpoints), `routers/users.py`, `routers/roles.py`, `routers/api_keys.py`, `services/auth_service.py` |
| Technical monitoring | System health exposure, dashboard auto-refresh | `main.py` (`/health`, `/health/detailed`), `pages/TechnicalMonitoring.vue`, `docs/monitoring-metrics.md` |
| Management monitoring | Project KPIs, EVM, team workload, milestone tracking | `routers/management_monitoring.py`, `pages/ManagementMonitoring.vue` |

---

## 10. Design Quality and Metrics

### 10.1 Code Modularity

| Metric | Value |
|--------|-------|
| Backend routers | 31 (one per domain entity) |
| Backend CRUD files | 22 |
| Backend model files | 24 |
| Pydantic schema files | 26 |
| Frontend pages | 25+ |
| Frontend composables | 13 |
| Frontend base components | 4 |
| Lines in largest single file | `main.py` ≈ 722 lines (includes all inline system endpoints) |

`main.py` is the only file that exceeds 300 lines. All domain logic lives in the domain-specific files.

### 10.2 Test Coverage

| Area | Files Present | Coverage |
|------|--------------|---------|
| Health endpoints | `tests/test_health.py` | All 5 health assertions covered |
| Authentication | `tests/test_auth.py` | Login, token refresh, logout |
| User management | `tests/test_users.py` | CRUD, permission checks |
| Comprehensive | `tests/test_comprehensive.py` | Integration scenarios |
| Frontend unit tests | `AssetForm.spec.js`, `useStatus.spec.js` | 2 files (limited coverage) |

**Note:** The documented 70% backend coverage claim requires verification via `pytest --cov` against the current test suite. Frontend coverage is limited to 2 unit test files.

### 10.3 API Response Time

The `/health` endpoint measures database response time as part of its check. The `/health/detailed` endpoint records `response_time_ms` (time to execute `SELECT 1` against PostgreSQL). In the development environment with Docker, measured values are typically 1–5 ms.

The `performance_test.py` router (`/api/v1/performance`) provides a dedicated endpoint for load testing response times under concurrent requests.

### 10.4 Critical Errors

- **Zero known runtime errors** in the current deployed state
- All 31 router registrations verified in `main.py`
- Translation keys for all navigation items verified in `en/menu.json` and `it/menu.json`
- Health endpoint returns `{"status":"ok", "database":"connected"}` when database is reachable

### 10.5 Technical Debt

| Item | Location | Severity | Notes |
|------|----------|----------|-------|
| Redundant `menuItems` array | `frontend/src/App.vue` | Low | Left from earlier session; `SidebarMenu.vue` now builds its own sections and does not consume this array |
| Frontend test coverage gap | `frontend/src/` | Medium | Only 2 Vitest unit tests; no integration tests for pages |
| `psutil` optional import | `main.py` `/health/detailed` | Low | If psutil is not installed, system metrics are omitted without notification |
| Redis caching unused | `backend/requirements.txt` | Low | `redis 5.0.1` is listed as a dependency but optional caching is not fully wired in all dashboard endpoints |

### 10.6 Maintainability Indicators

| Indicator | Status |
|-----------|--------|
| Consistent naming convention | All routers follow `{entity}.router`, all CRUD files follow `{entity}.py` |
| No circular imports | Models import Base; CRUD imports Models; Routers import CRUD and Schemas; main.py imports Routers |
| Environment-based config | All secrets and URLs are environment variables; no hardcoded credentials in source |
| Dependency injection | All DB sessions and current users obtained via `Depends()`; not constructed inline |
| Error code system | Custom `ErrorCodeException` with bilingual messages avoids scattered string literals |

### 10.7 Deployment Health

| Check | Mechanism |
|-------|-----------|
| Database up | `pg_isready` Docker healthcheck every 10 s; `depends_on: condition: service_healthy` |
| Backend up | `curl /health` Docker healthcheck every 30 s; restarts after 3 consecutive failures |
| Schema current | Alembic `upgrade head` runs on every container start |
| Secrets valid | Pydantic `Settings` validates at startup; refuses to start with default `SECRET_KEY` in production |

### 10.8 Error Rate

No production error tracking tool (e.g., Sentry) is configured. *(Planned enhancement.)* Current error visibility comes from:

- `logs/error.log` — all ERROR and CRITICAL log entries
- `logs/security.log` — all authentication events in JSON format
- `GET /audit-logs/` — all application-level entity changes
- Nginx/Traefik access logs — HTTP 4xx/5xx counts per endpoint
