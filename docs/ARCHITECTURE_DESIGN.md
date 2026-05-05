# Architecture & Design Quality
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Version:** 1.0  
**Owner:** Mohanad Aref Ali Sultan (Backend Developer, 2309115898)

---

## 1. System Architecture Overview

Industry Maintenance Platform follows a **three-tier web application architecture** with clear separation of concerns across the presentation, business logic, and data layers.

### 1.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                               │
│   Browser  ──►  HTTPS (443)  ──►  Nginx / Traefik               │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Reverse Proxy
        ┌───────────────────┴───────────────────┐
        │                                       │
        ▼                                       ▼
┌──────────────────┐                 ┌──────────────────────────┐
│  FRONTEND LAYER  │                 │     BACKEND LAYER         │
│  Vue.js 3        │  REST API       │  FastAPI (Python 3.10)    │
│  Vite build      │◄───────────────►│  Uvicorn ASGI server      │
│  PrimeVue 3      │  JSON / JWT     │  Port 8000                │
│  Chart.js        │                 │                           │
│  vis-network     │                 │  ┌─────────────────────┐  │
│  Pinia store     │                 │  │  Routers (29 files) │  │
│  Port 80/443     │                 │  │  CRUD (22 files)    │  │
└──────────────────┘                 │  │  Services (17 files) │  │
                                     │  │  Models (21 files)  │  │
                                     │  │  Schemas (27 files) │  │
                                     │  └─────────┬───────────┘  │
                                     └────────────┼──────────────┘
                                                  │
                              ┌───────────────────┴───────────────┐
                              │                                   │
                              ▼                                   ▼
                   ┌──────────────────┐              ┌────────────────────┐
                   │   DATA LAYER     │              │   CACHE LAYER      │
                   │  PostgreSQL 15+  │              │  Redis (optional)  │
                   │  21 tables       │              │  Dashboard cache   │
                   │  4 migrations    │              │  5-min TTL         │
                   └──────────────────┘              └────────────────────┘
```

### 1.2 Deployment Architecture (Production Local)

```
┌─────────────────────────────── Docker Network: industry-maintenance-platform-network ──────┐
│                                                                          │
│  ┌──────────────────────┐    ┌──────────────────────────────────────┐   │
│  │  nginx               │    │  backend (FastAPI)                    │   │
│  │  Port: 80, 443       │───►│  Port: 8000                          │   │
│  │  Self-signed TLS     │    │  Mounts: ./uploads, ./logs            │   │
│  │  Static Vue build    │    │  Depends: postgres                   │   │
│  └──────────────────────┘    └───────────────────┬──────────────────┘   │
│                                                   │                      │
│                               ┌───────────────────▼──────────────────┐  │
│                               │  postgres (PostgreSQL 15)             │  │
│                               │  Port: 5432 (internal only)          │  │
│                               │  Volume: industry-maintenance-platform_postgres_data     │  │
│                               └──────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technologies Used

### 2.1 Technology Selection Rationale

| Technology | Version | Role | Why Chosen |
|-----------|---------|------|-----------|
| **FastAPI** | 0.104.1 | REST API framework | Automatic OpenAPI docs; async-ready; Python type hints; high performance (Starlette/Uvicorn) |
| **SQLAlchemy** | 2.0.27 | ORM | Industry-standard Python ORM; supports PostgreSQL fully; migration support via Alembic |
| **Alembic** | 1.13.1 | DB migrations | Tight SQLAlchemy integration; version-controlled schema changes |
| **PostgreSQL** | 15 | Primary database | ACID compliance; JSON support; full-text search; proven reliability for enterprise data |
| **Redis** | 5.0.1 | Caching | In-memory speed for dashboard queries; TTL-based invalidation |
| **Vue.js 3** | 3.3.0 | Frontend framework | Composition API; reactive; component-based; large ecosystem |
| **Vite** | 4.5.0 | Build tool | Fast HMR; optimized production builds; ES module native |
| **PrimeVue** | 3.38.1 | UI component library | Rich industrial-quality components; accessible; data tables, charts |
| **Chart.js** | 4.4.0 | Data visualization | Lightweight; well-documented; works well with Vue via vue-chartjs |
| **Pinia** | 2.1.7 | State management | Vue 3 native; simpler than Vuex; TypeScript-friendly |
| **Docker** | 24+ | Containerization | Reproducible environments; isolation; simple multi-service orchestration |
| **Nginx** | 1.25 | Reverse proxy | High-performance static serving; SSL termination; load balancing capable |
| **GitHub Actions** | — | CI/CD | Free for open source; tight GitHub integration; YAML-based |

### 2.2 Architecture Style

**Primary:** Monolithic multi-layer application (appropriate for the project scale)  
**API Style:** RESTful, following HTTP conventions, with auto-generated OpenAPI/Swagger documentation  
**Authentication:** Stateless JWT tokens (Bearer + secure HttpOnly cookies)  
**Multi-tenancy:** Row-level tenant isolation (`tenant_id` column on all major tables)

---

## 3. Backend Module Organization

### 3.1 Layer Responsibilities

```
app/
├── main.py              # Application factory, middleware, global routes
├── config.py            # Settings (environment variables via pydantic-settings)
├── database.py          # SQLAlchemy engine, session factory
├── logging_config.py    # Structured logging setup
│
├── models/              # SQLAlchemy ORM models (database schema)
│   ├── asset.py         # Core entity: Industrial Asset
│   ├── user.py          # Authentication entity
│   ├── tenant.py        # Multi-tenant isolation
│   ├── audit_log.py     # Immutable change record
│   └── ... (17 more)
│
├── schemas/             # Pydantic models (request/response validation)
│   ├── asset.py         # AssetCreate, AssetRead, AssetUpdate
│   └── ... (26 more)
│
├── crud/                # Data access layer (SQL operations)
│   ├── asset.py         # get_asset, create_asset, update_asset, delete_asset
│   └── ... (21 more)
│
├── routers/             # HTTP endpoint definitions (FastAPI routers)
│   ├── assets.py        # GET/POST/PUT/DELETE /api/v1/assets/
│   ├── dashboards.py    # GET /api/v1/dashboards/
│   ├── audit_logs.py    # GET /api/v1/audit-logs/
│   └── ... (26 more)
│
└── services/            # Business logic (stateless, reusable)
    ├── risk_scoring.py  # ICS risk scoring algorithm
    ├── auth.py          # JWT creation, verification, RBAC
    ├── audit_log.py     # Audit entry creation service
    ├── dashboard_cache.py # Redis cache management
    └── ... (13 more)
```

### 3.2 Request Lifecycle

```
HTTP Request
     │
     ▼
FastAPI Router  ──► Pydantic Schema Validation ──► 422 if invalid
     │
     ▼
Auth Middleware ──► JWT Verification ──────────────► 401 if invalid
     │
     ▼
RBAC Check ─────────────────────────────────────── ► 403 if insufficient role
     │
     ▼
Route Handler
     │
     ▼
CRUD Function ──► SQLAlchemy ORM ──► PostgreSQL
     │
     ▼
Audit Log Service (async, non-blocking for performance)
     │
     ▼
Pydantic Response Schema ──► JSON Response
```

---

## 4. Design Quality Metrics

### 4.1 Cohesion Analysis

Cohesion measures how strongly related the responsibilities within a module are.

| Module | Type | Cohesion Level | Notes |
|--------|------|---------------|-------|
| `services/risk_scoring.py` | Functional | **High** | Single responsibility: compute risk score |
| `services/auth.py` | Functional | **High** | Single responsibility: authentication/authorization |
| `services/audit_log.py` | Functional | **High** | Single responsibility: create audit entries |
| `routers/assets.py` | Sequential | **High** | All endpoints operate on Asset entity |
| `routers/dashboards.py` | Communicational | **Medium-High** | Dashboard aggregation across multiple entities |
| `crud/asset.py` | Communicational | **High** | All functions access the same Asset table |
| `main.py` | Temporal | **Medium** | Application initialization — acceptable for entry point |
| `models/asset.py` | Logical | **High** | Defines a single coherent data entity |

**Overall Backend Cohesion: High** — modules have single, well-defined responsibilities.

### 4.2 Coupling Analysis

Coupling measures how much one module depends on another.

| Dependency | Type | Notes |
|-----------|------|-------|
| Router → CRUD | Data coupling | Only data passed (schemas, IDs) — **low coupling** |
| Router → Service | Stamp coupling | Service receives a DB session — acceptable |
| CRUD → Model | Data coupling | CRUD directly uses model classes — **low coupling** |
| Service → Service | Data coupling | Services call each other with simple data types |
| Main → All Routers | Control coupling | Router registration — standard FastAPI pattern |

**Coupling Rating: Low-to-Medium** — no circular dependencies; clear dependency direction (Router → Service/CRUD → Model → DB).

### 4.3 SOLID Principles Assessment

| Principle | Assessment | Evidence |
|-----------|-----------|---------|
| **S** — Single Responsibility | ✅ Met | Each service file has one purpose; each CRUD file handles one entity |
| **O** — Open/Closed | ✅ Mostly Met | New entity types can be added without modifying existing modules |
| **L** — Liskov Substitution | ✅ Met | Pydantic schemas are composable (AssetCreate ⊂ AssetRead) |
| **I** — Interface Segregation | ✅ Met | Pydantic schemas expose only needed fields per operation |
| **D** — Dependency Inversion | ✅ Met | Routes depend on abstractions (CRUD functions, services) not concrete DB queries |

### 4.4 Maintainability Index (Estimated)

The Maintainability Index (MI) formula considers code volume, cyclomatic complexity, and Halstead volume.

| Component | Est. Lines (code) | Avg Complexity | Maintainability |
|-----------|------------------|---------------|-----------------|
| Backend services | ~1,200 | Low (1–3) | **High** |
| Backend CRUD | ~2,100 | Very Low (1–2) | **Very High** |
| Backend routers | ~3,400 | Medium (3–6) | **Good** |
| Frontend pages | ~4,200 | Medium (4–8) | **Good** |
| Frontend components | ~2,800 | Low (2–5) | **High** |

**Assessment:** The codebase is maintainable. Low average complexity and consistent patterns mean new team members can contribute quickly.

### 4.5 Scalability Analysis

| Dimension | Current State | Scale Path |
|-----------|-------------|-----------|
| **Horizontal (API)** | Single container | Add load balancer (Traefik) + multiple backend replicas |
| **Database** | Single PostgreSQL | Read replicas; connection pooling via PgBouncer |
| **Caching** | Single Redis | Redis Cluster for high-availability caching |
| **Multi-tenancy** | Row-level isolation | Schema-per-tenant for large enterprise deployments |
| **File storage** | Local `uploads/` dir | S3-compatible object storage (MinIO, AWS S3) |
| **Search** | PostgreSQL full-text | Elasticsearch/OpenSearch for large asset catalogs |

**Current scale target:** 50 concurrent users, 10,000 assets, 100 GB data — all achievable with current architecture.

### 4.6 Security Design

| Layer | Control | Implementation |
|-------|---------|----------------|
| Transport | TLS 1.2/1.3 | Nginx with self-signed (dev) or Let's Encrypt (prod) |
| Authentication | JWT HS256 | 30-min expiry; secure HttpOnly cookies |
| Authorization | RBAC | 3 roles (Admin, Editor, Viewer); enforced per endpoint |
| Input validation | Schema validation | Pydantic v2 strict typing on all API inputs |
| Output sanitization | HTML escaping | bleach library on text fields |
| Audit | Immutable log | PostgreSQL append-only `audit_logs` table |
| Rate limiting | Token bucket | slowapi: 100/hour standard, 10/minute strict endpoints |
| Secrets | Environment vars | Never in code; `.env.example` documents required vars |

---

## 5. Continuous Integration Architecture

```
Developer pushes code
         │
         ▼
  GitHub Actions triggers
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
backend.yml  frontend.yml
    │          │
    ▼          ▼
PostgreSQL   Node.js 18
service spun   npm ci
    up         │
    │          ▼
pytest with  npm run test:unit
coverage       (Vitest)
    │          │
    ▼          ▼
Coverage     npm run build
report         │
    │          │
    └────┬─────┘
         │
         ▼
    ✅ Both pass → PR may be merged
    ❌ Either fails → PR blocked
```

The CI pipeline acts as the primary **quality gate** — no code can reach `main` without passing automated tests and a successful production build.

---

## 6. Design Decisions Log

| Decision | Chosen | Alternatives Considered | Reason |
|----------|--------|------------------------|--------|
| ORM vs raw SQL | SQLAlchemy ORM | Raw psycopg2, SQLModel | Type safety; migration support; team familiarity |
| Auth strategy | JWT + cookies | Sessions, OAuth2 only | Stateless; works for API clients and browser |
| Frontend state | Pinia | Vuex 4, Zustand | Vue 3 native; simpler API; persistent state plugin |
| Build/proxy | Nginx | Node.js serve, Caddy | Mature; zero-config static serving; SSL support |
| Multi-tenancy | Row-level (tenant_id) | Schema-per-tenant | Simpler migrations; acceptable for current scale |
| Caching | Redis (optional) | Memcached, in-memory dict | Standard; persistent; easy to add without code changes |
| Monitoring | Custom `/health/detailed` | Prometheus+Grafana | No paid tools; no external dependencies; demo-friendly |

---

## 7. Technical Debt Registry

| Item | Location | Severity | Plan |
|------|----------|---------|------|
| E2E tests incomplete | `frontend/cypress/` | Medium | Sprint 4 — partial coverage; full coverage in v1.2 roadmap |
| `main.py` exceeds 600 lines | `backend/app/main.py` | Low | Refactor exception handlers to separate module in v1.2 |
| Redis optional but not auto-detected | `backend/app/services/dashboard_cache.py` | Low | Add graceful fallback detection in v1.2 |
| PCAP router uses subprocess | `backend/app/routers/pcap.py` | Medium | Replace with pure-Python implementation to avoid subprocess risk |
