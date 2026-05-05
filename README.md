# Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

> **University Term Project** | Course: Software Project Management & Technical Monitoring
>
> | Member | ID | Role |
> |--------|-----|------|
> | Obada Abdulhakim Kharaz | 2309115277 | Project Manager |
> | Mohanad Aref Ali Sultan | 2309115898 | Backend Developer |
> | Zekeriya Dulli | 2309115377 | Frontend Developer |
> | Praise-God Tobby | 2309116418 | QA/Test Engineer |
> | Fares Stouhi | 2309115179 | UX/UI Designer |
> | Hamdi Alnaqeeb | 2309116178 | DevOps/Operations Engineer |
> | Abdulaziz Alyahya | 2309116441 | Risk Manager |

---

[![University](https://img.shields.io/badge/Istinye%20University-SPM%20Course-blue.svg)](https://istinye.edu.tr)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-green.svg)](https://vuejs.org/)

---

## Project Purpose

**Industry Maintenance Platform** is a comprehensive Industrial Asset Management System designed for managing and monitoring industrial equipment, networks, and infrastructure. Built with FastAPI backend and Vue.js frontend, it provides a modern, scalable solution for industrial environments.

Most asset management tools are designed for IT environments. They do not understand Purdue Model levels, ICS risk scoring, or OT compliance requirements. This platform was built to close that gap — making industrial asset state observable, continuous, and auditable at zero infrastructure cost.

---

## Academic Adaptation

This repository has been adapted for a **Software Project Management & Technical Monitoring** course project. The adaptation adds management monitoring, technical monitoring, risk management, stakeholder analysis, value creation, CI/CD documentation, continuous testing, and presentation/report deliverables on top of the original open-source Industry Maintenance Platform v1.1.0 codebase.

### What Was Added

| Area | What Was Added |
|------|---------------|
| Management Monitoring | `GET /api/v1/management/status` endpoint · Management Dashboard at `/management` |
| Technical Monitoring | `GET /health/detailed` endpoint · Technical Monitoring Dashboard at `/monitoring` |
| Risk Dashboard | New Vue.js page at `/risk` with asset-level and project-level risk register |
| CI/CD | GitHub Actions workflows for backend (pytest) and frontend (Vitest) |
| Frontend Tests | `useStatus.spec.js` — 29 Vitest assertions against the status composable |
| Documentation | 10 course-specific documents in `docs/` covering every course requirement |

### No Paid Services Required

| Service | Tool Used | Cost |
|---------|-----------|------|
| Backend CI | GitHub Actions (free tier) | €0 |
| Frontend CI | GitHub Actions (free tier) | €0 |
| Database (CI) | PostgreSQL 15 service container | €0 |
| Deployment | Docker Compose | €0 |
| Hosting | localhost (self-hosted) | €0 |
| Infrastructure | All open-source components | €0 |

**Total infrastructure cost: €0**

---

## Main Features

- **Asset Management**: Complete lifecycle management of industrial assets with soft delete and audit trail
- **Network Mapping**: Visual representation of asset connections and communications
- **Risk Assessment**: Built-in ICS risk scoring and vulnerability assessment via `risk_scoring.py`
- **Multi-tenant Architecture**: Support for multiple organisations with data isolation
- **Role-based Access Control**: Granular permissions (Admin, Editor, Viewer)
- **Change Management**: Asset timeline with before/after change comparisons
- **Global Search**: Spotlight-style search (Ctrl+K) across all entities with instant results
- **Document Management**: Asset documentation and photo management
- **Audit Trail**: Immutable append-only activity log with user, IP, and timestamp
- **API-First Design**: 31 RESTful routers with auto-generated OpenAPI/Swagger documentation
- **Modern UI**: Responsive Vue.js 3 frontend with PrimeVue components
- **Import/Export**: Excel/CSV import with preview and validation
- **Print System**: PDF report generation with QR codes
- **Floor Plan Integration**: Visual asset placement on floor plans

### Management Monitoring Features

- **`GET /api/v1/management/status`** — returns 14 management KPIs in a single JSON response
- **Management Dashboard** (`/management`) — auto-refreshes every 60 seconds
- **SPI (Schedule Performance Index)** — real-time schedule health; threshold ±10 %
- **Sprint velocity tracking** — story points per sprint across all sprints
- **Team workload table** — per-member load with colour-coded progress bars (red at > 95 %)
- **Milestone tracker** — 7 milestones from project kickoff to final submission
- **CPI (Cost Performance Index)** — estimated vs. actual effort ratio
- **Budget overview** — actual vs. allocated hours with variance

### Technical Monitoring Features

- **`GET /health`** — unauthenticated; returns `{"status":"ok","database":"connected","uptime":"running","timestamp":"...Z"}`; used by Docker healthcheck
- **`GET /health/detailed`** — unauthenticated; returns database response time, connection pool, CPU %, memory %, disk %, Python version, uptime seconds
- **Technical Monitoring Dashboard** (`/monitoring`) — auto-refreshes every 30 seconds; full-width status banner (green/amber/red)
- **Three-level downtime prevention:**
  - Level 1: Docker `healthcheck` restarts container after 3 failures (≤ 90 s, no human action)
  - Level 2: Dashboard polls every 30 s; degraded status shows red banner before users notice errors
  - Level 3: `logs/security.log` in JSON format — 401 spikes signal brute-force attempts
- **System resources** via `psutil 5.9.8` — CPU, memory, disk tracked live

### Risk Management Features

- **Risk Dashboard** (`/risk`) — combines asset-level and project-level risks in one view
- **ICS Risk Scoring** — `risk_scoring.py` computes 0–100 score from Purdue level, criticality, network access, and known vulnerabilities
- **Risk Register** — 14 project risks across 9 categories, each with owner, mitigation, contingency, and monitoring method
- **Risk Distribution** — visual breakdown by high / medium / low severity bands
- **Continuous monitoring** — risk scores update on every asset change, not annually

---

## Local Setup Instructions

### Prerequisites

- Docker and Docker Compose
- 4 GB RAM minimum (8 GB recommended)
- 20 GB disk space minimum
- Port 80 and 443 available

### Quick Start (< 5 minutes)

See [run_me.md](run_me.md) for the full Windows step-by-step guide.

```powershell
# Generate SSL certificates (once)
New-Item -ItemType Directory -Force -Path nginx\ssl
openssl genrsa -out nginx\ssl\key.pem 2048
openssl req -new -key nginx\ssl\key.pem -out nginx\ssl\cert.csr -subj "/C=TR/ST=Istanbul/L=Istanbul/O=IndustryMaintenancePlatform/CN=localhost"
openssl x509 -req -days 365 -in nginx\ssl\cert.csr -signkey nginx\ssl\key.pem -out nginx\ssl\cert.pem

# Start the full stack
docker compose -f docker-compose.prod.yml up -d

# Run migrations and load demo data
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
docker compose -f docker-compose.prod.yml exec backend python -m app.init_demo_data

# Access the application
# Open https://localhost in your browser
```

### Default Credentials

| Field | Value |
|-------|-------|
| URL | https://localhost |
| Email | admin@example.com |
| Password | admin123 |

Demo data is automatically loaded by `make prod`. It includes 8 assets, 3 sites, full network topology, contacts, and suppliers.

### Available Make Commands

```bash
make prod        # Start full stack (Nginx + self-signed certs + auto-init DB)
make demo        # Load demo data into an existing running system
make clean       # Remove all containers and volumes
make test        # Run backend tests
make logs        # Stream container logs
make stop        # Stop all services
make build       # Build all containers
make rebuild     # Force rebuild all containers
make status      # Show service health
make shell       # Open a shell in the backend container
make migrate     # Run Alembic database migrations
make reset-db    # Drop and recreate the database (destructive)
make restart     # Restart all services
make info        # Show system information
make config      # Show configuration options
make help        # List all commands
```

---

## Test Instructions

### Backend Tests (pytest)

```bash
# From the repo root — requires Docker running
cd backend
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

Or via the CI pipeline on every push to GitHub:

```bash
# GitHub Actions runs this automatically
# See .github/workflows/backend.yml
```

The test suite covers:
- `tests/test_health.py` — health endpoint responses and unauthenticated access
- `tests/test_auth.py` — login, JWT, invalid credentials
- `tests/test_users.py` — health and API docs smoke checks
- `tests/test_comprehensive.py` — user CRUD, asset creation, and RBAC enforcement

### Frontend Tests (Vitest)

```bash
cd frontend
npm ci
npm run test:unit
```

The test suite covers:
- `src/composables/__tests__/useStatus.spec.js` — 29 assertions against `getContrastColor`, `getStatusSeverity`, `getStatusColor`, `getStatusLabel`

### Smoke Tests (post-deployment)

Run these after every `make prod` to confirm the system is alive:

```bash
curl -k https://localhost/health
curl -k https://localhost/health/detailed
curl -k -X POST https://localhost/api/login \
  -d "username=admin@example.com&password=admin123"
curl -k -H "Authorization: Bearer <token>" https://localhost/api/assets/
```

---

## Architecture

- **Backend**: FastAPI 0.104.1 with SQLAlchemy ORM — 31 routers, 24 models, 26 Pydantic schemas
- **Database**: PostgreSQL 15 — multi-tenant isolation, soft delete, Alembic migrations
- **Frontend**: Vue.js 3 with Vite — 25+ pages, Composition API, PrimeVue components
- **Authentication**: JWT-based with role-based access control (Admin / Editor / Viewer)
- **Containerisation**: Docker and Docker Compose — 4 services: `db`, `backend`, `frontend`, `nginx`
- **CI/CD**: GitHub Actions (free tier) — backend and frontend pipelines
- **API Documentation**: Auto-generated with OpenAPI/Swagger at `/docs`

---

## Documentation Index

### Course Adaptation Documents

| Document | Purpose |
|----------|---------|
| [docs/project-report.md](docs/project-report.md) | Complete academic report — all 12 course requirements |
| [docs/monitoring-strategy.md](docs/monitoring-strategy.md) | Management and technical monitoring strategy with 22-metric table |
| [docs/risk-management.md](docs/risk-management.md) | Risk register and mitigation plan |
| [docs/stakeholder-management.md](docs/stakeholder-management.md) | Stakeholder expectations and communication plan |
| [docs/value-creation.md](docs/value-creation.md) | Business and operational value — €0 cost, €110k Year 1 benefit |
| [docs/software-design-analysis.md](docs/software-design-analysis.md) | Architecture, maintainability, scalability, and design quality |
| [docs/ui-dashboard-design.md](docs/ui-dashboard-design.md) | Three dashboard designs: Management, Technical Monitoring, Risk |
| [docs/ci-cd-testing.md](docs/ci-cd-testing.md) | CI/CD pipelines and continuous testing approach |
| [docs/presentation-outline.md](docs/presentation-outline.md) | 7-minute presentation plan with speaker scripts |
| [docs/video-submission-instructions.md](docs/video-submission-instructions.md) | Video recording and submission guide |

### Additional Course Documents

| Document | Purpose |
|----------|---------|
| [docs/TEAM.md](docs/TEAM.md) | Team member roles and responsibilities |
| [docs/team-work-plan.md](docs/team-work-plan.md) | Sprint plan and task breakdown |
| [docs/PROJECT_MANAGEMENT_PLAN.md](docs/PROJECT_MANAGEMENT_PLAN.md) | Full project management plan |
| [docs/management-under-uncertainty.md](docs/management-under-uncertainty.md) | 8 uncertainty scenarios with detection signals and responses |
| [docs/monitoring-metrics.md](docs/monitoring-metrics.md) | Monitoring metrics reference table |

### Technical Documentation

| Document | Purpose |
|----------|---------|
| [docs/QUICK_START.md](docs/QUICK_START.md) | Get running in 5 minutes |
| [docs/installation.md](docs/installation.md) | Detailed installation instructions |
| [docs/api-documentation.md](docs/api-documentation.md) | Complete API reference |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Common issues and solutions |
| [docs/custom-certificates.md](docs/custom-certificates.md) | Deploy with internal CA certificates |
| [docs/UPGRADE.md](docs/UPGRADE.md) | Upgrade guide from previous versions |

---

## Demo Data

The system comes pre-populated when using `make prod` or `make demo`:

- **3 Sites**: Main Production Plant, Research & Development Center, Distribution Warehouse
- **12 Areas**: Assembly Lines, Quality Control Lab, Control Room, Maintenance Bay, etc.
- **19 Locations**: Control Panels, Quality Stations, Maintenance Bays, etc.
- **8 Assets**: PLCs, HMIs, Robots, Switches, Sensors, Servers with realistic specifications
- **10 Interfaces**: Network interfaces with IP addresses, MAC addresses, and protocols
- **5 Connections**: Network topology showing asset communications
- **4 Manufacturers**: Siemens, Rockwell Automation, Schneider Electric, ABB
- **4 Suppliers** and **6 Contacts**: Complete supply chain information

---

## Contact

- **Project Manager**: Obada Abdulhakim Kharaz
- **University**: Istinye University
- **Course**: Software Project Management & Technical Monitoring
- **Contact**: obadahakeem74@gmail.com
