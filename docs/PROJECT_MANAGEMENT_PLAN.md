# Project Management Plan
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Version:** 1.0  
**Date:** 2026-04-20  
**Project Manager:** Obada Abdulhakim Kharaz (2309115277)

---

## 1. Project Overview

### 1.1 Objectives
Develop and document a production-ready industrial asset management and technical monitoring platform that:
- Manages industrial assets across sites, areas, and locations
- Provides real-time risk scoring and vulnerability assessment
- Delivers management and technical monitoring dashboards
- Runs locally on Docker with full CI/CD automation

### 1.2 Scope
**In Scope:**
- FastAPI backend with PostgreSQL (all 21 data models)
- Vue.js 3 frontend with 3 monitoring dashboards
- Docker-based deployment (dev and production profiles)
- GitHub Actions CI/CD pipeline
- Technical monitoring endpoint `/health/detailed`
- Full project documentation set

**Out of Scope:**
- Cloud hosting or SaaS deployment
- Mobile native applications
- Paid third-party monitoring services (e.g., Datadog, New Relic)
- Integration with real industrial hardware

### 1.3 Constraints
| Constraint | Details |
|-----------|---------|
| Budget | Zero monetary cost — open-source tools only |
| Team | 7 students, maximum 80 hours each |
| Duration | 16 weeks (one semester) |
| Infrastructure | Local Docker on developer machines |
| License | AGPL-3.0 inherited from upstream Industry Maintenance Platform |

---

## 2. Work Breakdown Structure (WBS)

```
Industry Maintenance Platform Project
├── 1. Project Management
│   ├── 1.1 Project Plan
│   ├── 1.2 Sprint Planning & Retrospectives (×4)
│   ├── 1.3 Risk Management
│   └── 1.4 Stakeholder Communication
│
├── 2. Requirements & Analysis
│   ├── 2.1 Functional Requirements
│   ├── 2.2 Non-Functional Requirements
│   └── 2.3 Architecture Design
│
├── 3. Backend Development (FastAPI + PostgreSQL)
│   ├── 3.1 Database Models & Migrations (21 models)
│   ├── 3.2 Core API Endpoints (assets, sites, areas, etc.)
│   ├── 3.3 Authentication & RBAC
│   ├── 3.4 Risk Scoring Engine
│   ├── 3.5 Audit Trail & Logging
│   └── 3.6 Technical Monitoring Endpoint
│
├── 4. Frontend Development (Vue.js 3)
│   ├── 4.1 Asset Management Pages
│   ├── 4.2 Management Dashboard
│   ├── 4.3 Technical Monitoring Dashboard
│   ├── 4.4 Risk Dashboard
│   └── 4.5 Audit Log & Search Pages
│
├── 5. Infrastructure & CI/CD
│   ├── 5.1 Docker Compose Configurations
│   ├── 5.2 GitHub Actions Backend Pipeline
│   ├── 5.3 GitHub Actions Frontend Pipeline
│   ├── 5.4 Nginx Configuration
│   └── 5.5 Make Automation Targets
│
├── 6. Testing & Quality Assurance
│   ├── 6.1 Backend Unit Tests (pytest)
│   ├── 6.2 Frontend Unit Tests (Vitest)
│   ├── 6.3 End-to-End Tests (Cypress)
│   └── 6.4 Performance Testing
│
└── 7. Documentation & Presentation
    ├── 7.1 Team Document
    ├── 7.2 Architecture & Design Document
    ├── 7.3 Technical Monitoring Document
    ├── 7.4 Risk Management Document
    ├── 7.5 Stakeholder Management Document
    ├── 7.6 Value Creation Document
    ├── 7.7 Final Project Report
    └── 7.8 Presentation (slides + video backup)
```

---

## 3. Project Schedule

### 3.1 Phase Overview

| Phase | Weeks | Focus |
|-------|-------|-------|
| Initiation & Planning | 1–2 | Requirements, architecture design, WBS, team setup |
| Sprint 1 | 3–5 | Backend core: models, migrations, API endpoints, auth |
| Sprint 2 | 6–8 | Frontend core: asset pages, management dashboard |
| Sprint 3 | 9–11 | Monitoring features, risk dashboard, CI/CD, testing |
| Sprint 4 | 12–13 | QA, performance tuning, bug fixes, code freeze |
| Documentation & Presentation | 14–16 | Final report, presentation, video backup |

### 3.2 Gantt Chart (16-Week Overview)

```
Week:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
       ↑                                               ↑
     Start                                           End

Planning      [██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Requirements  [████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Architecture  [░░████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Sprint 1      [░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░] (Wk 3-5)
Sprint 2      [░░░░░░░░░░████████░░░░░░░░░░░░░░░░░░░] (Wk 6-8)
Sprint 3      [░░░░░░░░░░░░░░░░████████░░░░░░░░░░░░░] (Wk 9-11)
Sprint 4      [░░░░░░░░░░░░░░░░░░░░░░████████░░░░░░░] (Wk 12-13)
Testing       [░░░░░░░░░░░░░░░░░░░░████████████░░░░░] (Wk 10-13)
Docs/Report   [░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████] (Wk 14-16)
Presentation  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████] (Wk 15-16)

Legend:  ██ Active   ░░ Inactive
```

### 3.3 Sprint Plan

#### Sprint 1 (Weeks 3–5): Backend Foundation
**Goal:** Runnable backend with all database models, migrations, and core API endpoints.

| Task | Owner | Story Points | Status |
|------|-------|-------------|--------|
| Define PostgreSQL schemas (21 models) | Mohanad | 8 | Implemented |
| Write Alembic migrations (4 versions) | Mohanad | 5 | Implemented |
| Implement assets CRUD endpoints | Mohanad | 8 | Implemented |
| Implement auth + JWT + RBAC | Mohanad | 8 | Implemented |
| Implement audit logging service | Mohanad | 5 | Implemented |
| Architecture review and approval | Mohanad | 3 | Implemented |
| Docker dev environment setup | Hamdi | 5 | Implemented |
| Backend CI pipeline (GitHub Actions) | Hamdi | 3 | Implemented |

**Sprint 1 Velocity:** 45 story points

#### Sprint 2 (Weeks 6–8): Frontend & Dashboards
**Goal:** Working Vue.js frontend with asset management pages and management dashboard.

| Task | Owner | Story Points | Status |
|------|-------|-------------|--------|
| Vue Router and Pinia store setup | Zekeriya | 5 | Implemented |
| Asset management pages (CRUD) | Zekeriya | 10 | Implemented |
| Sites, Areas, Locations pages | Zekeriya | 8 | Implemented |
| Main management dashboard | Zekeriya | 8 | Implemented |
| Chart.js integration for metrics | Zekeriya | 5 | Implemented |
| Network topology visualization | Zekeriya | 8 | Implemented |
| Frontend CI pipeline | Hamdi | 3 | Implemented |
| Vitest unit tests (≥ 60% coverage) | Praise-God | 5 | Implemented |

**Sprint 2 Velocity:** 52 story points

#### Sprint 3 (Weeks 9–11): Monitoring & Risk Features
**Goal:** Technical monitoring dashboard, risk scoring UI, `/health/detailed` endpoint, CI/CD complete.

| Task | Owner | Story Points | Status |
|------|-------|-------------|--------|
| `/health/detailed` monitoring endpoint | Mohanad | 5 | Implemented |
| Technical monitoring dashboard (Vue) | Zekeriya | 8 | Implemented |
| Risk dashboard with scoring visuals | Zekeriya | 8 | Implemented |
| Risk scoring engine (backend) | Mohanad | 8 | Implemented |
| Audit trail page and filters | Zekeriya | 5 | Implemented |
| Redis caching for dashboards | Mohanad | 5 | Implemented |
| PCAP analysis router | Mohanad | 5 | Implemented |
| Production Docker + Nginx config | Hamdi | 5 | Implemented |
| E2E tests (Cypress) for dashboards | Praise-God | 5 | Prototype |

**Sprint 3 Velocity:** 54 story points

#### Sprint 4 (Weeks 12–13): QA & Code Freeze
**Goal:** Bug-free, tested, optimized system ready for documentation phase.

| Task | Owner | Story Points | Status |
|------|-------|-------------|--------|
| Backend coverage ≥ 70% | Praise-God, Mohanad | 8 | Implemented |
| Performance testing (critical endpoints) | Praise-God | 5 | Implemented |
| Bug fixes from Sprints 1–3 | Mohanad, Zekeriya | 8 | Implemented |
| Database index optimization | Mohanad | 3 | Implemented |
| Code freeze and final review | Obada | 3 | Implemented |
| Security review (OWASP checklist) | Mohanad, Hamdi | 5 | Implemented |

**Sprint 4 Velocity:** 32 story points

---

## 4. Milestone Tracking

| Milestone | Target Date | Owner | Success Criteria | Status |
|-----------|-------------|-------|-----------------|--------|
| M1: Project Kickoff | Week 1 | Obada | Team formed, WBS approved, tooling set up | ✅ Done |
| M2: Architecture Approved | Week 3 | Mohanad | Architecture document signed off by team | ✅ Done |
| M3: Backend Alpha | Week 5 | Mohanad | All API endpoints return valid responses; pytest green | ✅ Done |
| M4: Frontend Alpha | Week 8 | Zekeriya | All pages render; assets CRUD works end-to-end | ✅ Done |
| M5: Monitoring Dashboard Live | Week 11 | Mohanad + Hamdi | `/health/detailed` endpoint live; dashboard shows metrics | ✅ Done |
| M6: Code Freeze | Week 13 | Obada | No new features; all bugs P1/P2 resolved; CI green | ✅ Done |
| M7: Documentation Complete | Week 15 | Obada | All docs submitted; report reviewed by PM | ✅ Done |
| M8: Final Presentation | Week 16 | Obada | 7-minute demo delivered; video backup submitted | 🔄 Planned |

---

## 5. Cost & Effort Tracking

### 5.1 Effort Model
The project uses an **hours-based effort model** (no monetary budget — all tools are open-source).

| Category | Planned Hours | Actual Hours | Variance |
|----------|--------------|-------------|---------|
| Project Management | 60 | 58 | −2 |
| Requirements & Analysis | 30 | 32 | +2 |
| Backend Development | 120 | 125 | +5 |
| Frontend Development | 110 | 108 | −2 |
| Infrastructure & CI/CD | 60 | 63 | +3 |
| Testing & QA | 80 | 77 | −3 |
| Documentation | 80 | 81 | +1 |
| Presentation | 20 | 18 | −2 |
| **Total** | **560** | **562** | **+2** |

*Variance is within ±5% — project is on track.*

### 5.2 Notional Cost Model (Academic Reference)
For academic valuation purposes, applying a notional rate of €25/hour (junior developer rate):

| Phase | Hours | Notional Cost (€) |
|-------|-------|------------------|
| Project Management | 60 | 1,500 |
| Backend Development | 120 | 3,000 |
| Frontend Development | 110 | 2,750 |
| Infrastructure / CI/CD | 60 | 1,500 |
| Testing & QA | 80 | 2,000 |
| Documentation | 100 | 2,500 |
| **Total** | **530** | **13,250** |

*Tools cost: €0 (all open-source). Infrastructure cost: €0 (local Docker).*  
*Total project cost: €13,250 equivalent (labor only).*

### 5.3 Earned Value Metrics (Week 13 Snapshot)

| EVM Metric | Formula | Value |
|-----------|---------|-------|
| Planned Value (PV) | Budget × % scheduled | €12,600 |
| Earned Value (EV) | Budget × % complete | €12,450 |
| Actual Cost (AC) | Actual hours × rate | €12,550 |
| Schedule Variance (SV) | EV − PV | −€150 (−1.2%) |
| Cost Variance (CV) | EV − AC | −€100 (−0.8%) |
| SPI (Schedule Performance) | EV / PV | 0.99 |
| CPI (Cost Performance) | EV / AC | 0.99 |

*SPI and CPI both ≈ 1.0 — project is on schedule and within effort budget.*

---

## 6. Team Workload Visibility

### 6.1 Sprint Velocity Chart (Story Points Completed)

```
        Sprint 1   Sprint 2   Sprint 3   Sprint 4
         (Wk3-5)   (Wk6-8)   (Wk9-11)  (Wk12-13)
60 |                                    
55 |                ░░░░░░     ░░░░░░   
50 |     ░░░░░░     ████████   ████████  
45 |     ████████                        ░░░░░░  
40 |                                     ████████
35 |                                    
   +-----------+-----------+-----------+-----------
   Points:   45          52          54          32
```

*Sprint 4 points are lower by design — QA, testing, and code freeze produce fewer new features.*

### 6.2 Individual Contribution Tracking

| Member | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Docs | Total Hours |
|--------|----------|----------|----------|----------|------|-------------|
| Obada (PM) | 18h | 15h | 15h | 15h | 17h | 80h |
| Mohanad (Backend) | 22h | 22h | 20h | 12h | 4h | 80h |
| Zekeriya (Frontend) | 10h | 24h | 22h | 14h | 10h | 80h |
| Praise-God (QA) | 12h | 16h | 20h | 22h | 10h | 80h |
| Fares (UX/UI) | 14h | 18h | 16h | 12h | 20h | 80h |
| Hamdi (DevOps) | 18h | 14h | 18h | 18h | 12h | 80h |
| Abdulaziz (Risk) | 12h | 14h | 14h | 14h | 26h | 80h |

*All team members contribute equally at 80 hours across the project.*

---

## 7. Progress Tracking Mechanisms

### 7.1 Sprint Review Checklist (used each sprint)
- [ ] All committed user stories are demonstrated
- [ ] All automated tests pass (CI green)
- [ ] Code coverage targets met
- [ ] No P1 open bugs
- [ ] Documentation updated
- [ ] Next sprint backlog is prioritized

### 7.2 Definition of Done
A task is "Done" when:
1. Code is merged to `main` branch
2. Automated tests pass
3. Code reviewed by at least one other team member
4. Documentation updated if user-facing change
5. No new P1/P2 bugs introduced

### 7.3 Tools Used for Tracking
| Tool | Purpose |
|------|---------|
| GitHub Projects (Kanban board) | Sprint backlog, task tracking |
| GitHub Actions | CI/CD status, automated quality gates |
| Git commit history | Contribution traceability |
| This document | Official management baseline |
| Sprint meeting notes | Decision log |

---

## 8. Change Management

All scope changes follow this process:
1. Team member raises a change request in GitHub Issues with label `scope-change`
2. Omar (PM) assesses impact on schedule, effort, and milestones
3. Lina (Tech Lead) assesses technical feasibility
4. Change approved/rejected in next sprint planning meeting
5. Approved changes update this document (version bumped)

*No changes were approved after Week 11 (code freeze protection).*
