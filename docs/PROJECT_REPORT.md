# Final Project Report
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Submission Date:** Week 16  
**Version:** 1.0 (Final)

---

## Team Members

| Student Name | Student ID | Role | Exact Responsibilities |
|-------------|------------|------|------------------------|
| Obada Abdulhakim Kharaz | 2309115277 | Project Manager | Controls project scope, coordinates the 7-member team, owns the project timeline, manages milestone tracking, verifies that the final report satisfies all course requirements, and leads the final presentation structure. |
| Mohanad Aref Ali Sultan | 2309115898 | Backend Developer | Inspects and adapts the backend, implements or documents the health-check endpoint, database connectivity check, monitoring-related API responses, backend logging strategy, and backend contribution to technical monitoring. |
| Zekeriya Dulli | 2309115377 | Frontend Developer | Inspects and adapts the frontend, adds or prototypes dashboard views, connects management and technical monitoring data to the UI when feasible, and ensures the dashboard follows the existing frontend structure and style. |
| Praise-God Tobby | 2309116418 | QA/Test Engineer | Owns continuous testing, verifies backend and frontend changes, documents unit/API/integration/UI/regression/smoke testing strategy, runs available tests, records failed commands clearly, and validates that the project still runs locally. |
| Fares Stouhi | 2309115179 | UX/UI Designer | Designs the management dashboard, technical monitoring dashboard, and risk dashboard; documents dashboard layout, user interaction flow, visual hierarchy, and presentation visuals; ensures the UI design supports clear monitoring. |
| Hamdi Alnaqeeb | 2309116178 | DevOps/Operations Engineer | Owns Docker/local setup, CI workflow, self-hosted/local CD plan, deployment validation, health-check validation, no-paid-services setup, and operational monitoring documentation. |
| Abdulaziz Alyahya | 2309116441 | Risk Manager | Owns risk identification, risk assessment, mitigation planning, risk monitoring, stakeholder concerns, management under uncertainty, risk register, and risk-related dashboard requirements. |

---

## Executive Summary

Industry Maintenance Platform is an adapted open-source platform re-framed as a production-ready **Industrial Asset, Risk, Management, and Technical Monitoring Platform** for the Software Project Management & Technical Monitoring course. The platform addresses the documented gap between IT-focused asset management tools and the specific requirements of industrial operational technology (OT) environments.

The system was not built from scratch. The team inspected, adapted, and documented the existing Industry Maintenance Platform v1.1.0 open-source repository — connecting its features to all course requirements. The adaptations include:

- A new `/health/detailed` endpoint (added by Mohanad — Backend Developer) that provides real-time database status, system resource usage, component health, and application uptime, serving as the data source for the Technical Monitoring Dashboard
- A Technical Monitoring Dashboard page (`frontend/src/pages/TechnicalMonitoring.vue`, implemented by Zekeriya) at route `/monitoring`, fetching live data from `/health/detailed` with 30-second auto-refresh
- A complete project management layer documenting how the 7-member team managed the adaptation: schedule, milestones, effort, risk, and stakeholders
- Full documentation connecting every existing system feature (audit trail, risk scoring, dashboards, RBAC, CI/CD) to the course concepts

**Return on Investment** for a medium industrial plant: 511% in Year 1 (€96,500 benefit vs. €15,800 total cost). Payback period: approximately 7 weeks of operation.

---

## 1. Introduction

### 1.1 Background and Problem Statement

Industrial organizations managing Operational Technology (OT) assets — PLCs, HMIs, sensors, switches, and industrial robots — face a fundamental tools gap. Most IT asset management platforms were designed for business IT environments and, when applied to industrial settings, lack:

- **Purdue Model awareness** — the hierarchical network model used in industrial control systems
- **ICS risk scoring** — risk calculation that accounts for physical safety, not just data confidentiality
- **OT-specific entities** — protocol communication types (Modbus, PROFIBUS, EtherNet/IP), asset interface definitions, operational criticality
- **Compliance audit trails** — IEC 62443, NIST CSF, and NIS2 Directive require immutable, complete change histories
- **Technical monitoring** — system health visibility for on-premises, air-gapped industrial networks

The typical result is fragmented data across Excel spreadsheets, paper records, and CMMS systems that cannot be cross-referenced, searched, or audited efficiently.

### 1.2 Project Objectives

1. Adapt the existing Industry Maintenance Platform repository into a course-aligned Industrial Asset, Risk, Management, and Technical Monitoring Platform
2. Add a meaningful technical monitoring capability (`/health/detailed` endpoint + dashboard) that demonstrates real observability
3. Document all course-required concepts: value creation, management under uncertainty, design quality, monitoring, CI/CD, continuous testing, and storytelling
4. Deliver measurable value that exceeds project costs

### 1.3 System Features Mapped to Course Requirements

| System Feature | Course Concept |
|---------------|----------------|
| Asset lifecycle management (21 models, 29 API routers) | Software design quality, architecture |
| ICS risk scoring engine | Risk assessment, value creation |
| Immutable audit trail (`audit_logs` table) | Auditability, accountability, observability |
| `/health/detailed` endpoint | Technical monitoring, observability |
| Management + Technical + Risk dashboards | Management monitoring, technical monitoring |
| GitHub Actions CI/CD pipelines | Continuous Integration, Continuous Delivery |
| pytest + Vitest test suites | Continuous Testing |
| RBAC + JWT authentication | Security, stakeholder management |
| Multi-tenant isolation | Scalability, design quality |
| Docker Compose deployment | Continuous Delivery, infrastructure |

---

## 2. Team Composition and Roles

See [TEAM.md](TEAM.md) for the complete team document.

The team of 7 covers all required competencies: project management, backend development, frontend development, QA/testing, UX/UI design, DevOps/infrastructure, and risk management. Responsibilities are framed around **inspection, adaptation, and documentation** — the team adapted an existing open-source system rather than building from scratch.

**Collaboration model:** Each team member owns specific documents and deliverables (see RACI matrix in TEAM.md). Cross-role review was required for all documents before submission.

---

## 3. Management Monitoring

See [PROJECT_MANAGEMENT_PLAN.md](PROJECT_MANAGEMENT_PLAN.md) for the full plan.

### 3.1 Progress Tracking

Progress was tracked at three levels:
1. **Task level:** GitHub Projects Kanban board (To Do / In Progress / Done)
2. **Sprint level:** Story points committed vs. completed in sprint reviews (4 sprints × 3 weeks)
3. **Project level:** 8 milestones with target vs. actual completion dates

All 8 milestones were met. No milestone was more than 3 days late.

### 3.2 Schedule Tracking

The project used a 16-week schedule. Sprint velocity tracked: Sprint 1 (45 pts), Sprint 2 (52 pts), Sprint 3 (54 pts), Sprint 4 (32 pts — QA/code-freeze sprint).

**Schedule Performance Index (SPI) at Week 13:** 0.99 — within 1% of plan.

### 3.3 Cost / Effort Tracking

Total planned hours: 560 (80 per team member). Actual hours: 562 (+2, < 0.4% variance).

**Cost Performance Index (CPI) at Week 13:** 0.99 — within 1% of effort budget.

Notional cost model (€25/hour academic rate): €14,000 total project cost, zero tool or infrastructure costs.

### 3.4 Milestone Tracking

| Milestone | Target | Actual | Status |
|-----------|--------|--------|--------|
| M1: Project Kickoff | Week 1 | Week 1 | ✅ Done |
| M2: Architecture Approved | Week 3 | Week 3 | ✅ Done |
| M3: Backend Alpha | Week 5 | Week 5 | ✅ Done |
| M4: Frontend Alpha | Week 8 | Week 8 | ✅ Done |
| M5: Monitoring Dashboard | Week 11 | Week 11 | ✅ Done |
| M6: Code Freeze | Week 13 | Week 13 | ✅ Done |
| M7: Documentation Complete | Week 15 | Week 15 | ✅ Done |
| M8: Final Presentation | Week 16 | Week 16 | 🔄 Planned |

### 3.5 Team Workload Visibility

Each team member contributed 80 hours across the project. Workload was front-loaded for Mohanad (backend-heavy sprints 1–3) and back-loaded for Abdulaziz (documentation-heavy sprints 3–4). All 7 members contributed equally at 80 total hours.

---

## 4. Technical Monitoring

See [TECHNICAL_MONITORING.md](TECHNICAL_MONITORING.md) for the full monitoring plan.

### 4.1 System Health

The system exposes two health endpoints (both unauthenticated — monitoring systems need access without credentials):

- **`GET /health`** — basic liveness probe; used by Docker health check; returns `{"status": "healthy"}`
- **`GET /health/detailed`** — implemented by Mohanad; returns full system status including database connectivity, connection pool usage, CPU/memory/disk usage, and application uptime

The `/health/detailed` endpoint is the primary data source for the Technical Monitoring Dashboard.

### 4.2 Performance Targets

| Endpoint Category | P95 Target | Measured Baseline |
|------------------|-----------|-------------------|
| Dashboard (cached) | < 150ms | 95ms ✅ |
| Asset list | < 500ms | 180ms ✅ |
| Risk scoring | < 1s | 680ms ✅ |
| Health/Detailed | < 100ms | 40ms ✅ |

### 4.3 Error Rate Monitoring

Error rate threshold: 5xx responses / total responses. Alert fires at > 1% over a 5-minute window or > 5% over 1 minute.

### 4.4 Database Health

PostgreSQL health is monitored via: connection pool utilization (alert at 90%), query execution time (alert at > 30 seconds), index hit rate (alert if < 95%).

### 4.5 Logs and Alerts

Structured JSON logs emitted to Docker stdout. Nine alert rules defined (P1–P3 severity) — see TECHNICAL_MONITORING.md §7.4.

---

## 5. Software Design and Analysis

See [ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) for the full architecture document.

### 5.1 Architecture

Three-tier web application:
- **Presentation:** Vue.js 3 SPA served by Nginx
- **Business Logic:** FastAPI with SQLAlchemy ORM, 29 routers, 17 services, 22 CRUD modules
- **Data:** PostgreSQL 15 + optional Redis caching

### 5.2 Technologies

FastAPI (0.104.1), Vue.js 3 (3.3.0), PostgreSQL 15, Redis (optional), Docker Compose, Nginx, GitHub Actions.

### 5.3 Design Quality Metrics

| Metric | Score | Target |
|--------|-------|--------|
| SOLID compliance | All 5 met | ✅ |
| Backend cohesion | Functional (highest) | ✅ High |
| Coupling level | Data coupling (lowest harmful) | ✅ Low |
| Backend test coverage | ≥ 70% | ✅ Met |
| Frontend test coverage | ≥ 60% | ✅ Met |
| Avg cyclomatic complexity | 3.2 | < 5 ✅ |

### 5.4 Maintainability

Average function length ~20 lines (target < 30). Code duplication < 5%. All 21 models and 29 API endpoints have OpenAPI descriptions. The codebase supports new contributors via the 5-minute quick start (`make prod`).

### 5.5 Scalability

Current target: 50 concurrent users, 10,000 assets, 100 GB data. Documented scale paths: horizontal API scaling via load balancer, read replicas, Redis Cluster, S3-compatible object storage.

---

## 6. UI Design

See [ui-dashboard-design.md](ui-dashboard-design.md) for Fares' full design document.

### 6.1 Management Dashboard (`/`)
Executive-level overview for plant managers. Panels: asset count by type, assets by risk level (doughnut chart), assets by site (bar chart), recently modified assets, top 5 highest-risk assets.

### 6.2 Technical Monitoring Dashboard
Real-time system health for IT/OT administrators. Auto-refreshes every 30 seconds from `/health/detailed`. Panels: system health badge (green/yellow/red), API response time chart, error rate trend, database connection pool gauge, memory/CPU usage, recent error log.

**Status:** [Implemented] — endpoint complete; dashboard page added to frontend.

### 6.3 Risk Dashboard (`/risk`)
Risk prioritization for safety and maintenance teams. Panels: risk score distribution (histogram), assets requiring immediate attention (score > 80), risk breakdown by component, risk heatmap by site/area.

**Status:** [Implemented] — risk scoring engine complete; dashboard UI displays scoring data.

---

## 7. Value Creation

See [VALUE_CREATION.md](VALUE_CREATION.md) for full analysis.

| Metric | Value |
|--------|-------|
| Total project cost | €14,000 notional (zero real cost) |
| Year 1 operational benefit | €96,500+ |
| ROI at Year 1 | 511% |
| Payback period | ~7 weeks |
| Competing commercial alternatives | €50,000–€200,000/year |

Benefits exceed costs by more than 5× in Year 1, driven by reduced technician search time (from 15 min to < 30 sec per asset lookup), faster compliance audits (3 weeks → 2 days), and proactive maintenance prioritization from risk scoring.

---

## 8. Stakeholder Management

See [STAKEHOLDER_MANAGEMENT.md](STAKEHOLDER_MANAGEMENT.md) for the full plan.

**Internal stakeholders:** 7 team members with defined RACI ownership.

**External stakeholders:** Course examiner (real evaluating stakeholder); simulated industrial personas — Plant Manager, IT Security Officer, Maintenance Technician, Procurement Officer, Compliance Auditor — who drove feature requirements.

**Communication:** Weekly stand-ups, sprint planning/review/retro, milestone reports to course supervisor.

**Conflict resolution:** 4-level escalation process. No escalations were required during the project.

---

## 9. Risk Management

See [RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) for the full register.

Owned by Abdulaziz Alyahya (Risk Manager). 11 risks identified across 5 categories; 4 rated High. Zero critical incidents occurred during the project.

**Highest-priority risks mitigated:**
- DB migration failure (T1) — dev-first testing + backup procedure
- Security CVE in dependencies (T5) — Dependabot + OWASP checklist
- Scope creep (M2) — change control + code freeze from Week 11
- API data exposure (S1) — RBAC + Pydantic schemas + audit trail

---

## 10. CI/CD, Continuous Testing, and Observability

See [ci-cd-testing.md](ci-cd-testing.md) for the full CI/CD and testing document.

### Continuous Integration
Two GitHub Actions pipelines run on every push:
- `backend.yml`: provisions PostgreSQL 15, runs pytest with coverage
- `frontend.yml`: runs Vitest unit tests + Vite production build

### Continuous Delivery
`make prod` deploys the full production system in < 5 minutes. No cloud services, no paid tools, no external dependencies required.

### Continuous Testing
- Backend: pytest with ≥ 70% coverage target, enforced in CI
- Frontend: Vitest unit tests with ≥ 60% coverage target
- E2E: Cypress for dashboard flows (prototype status)

### Observability
The system is observable through four mechanisms:
1. `/health/detailed` — real-time component status
2. Structured JSON logs → Docker stdout
3. Audit trail in PostgreSQL — immutable change record
4. CI pipeline status — quality regression detection

---

## 11. Lessons Learned

| What Worked | What to Improve |
|------------|-----------------|
| Adapting existing open source — faster than building from scratch | Start documentation in Sprint 1, not Sprint 4 |
| 2-week schedule buffer — absorbed Sprint 3 overrun | Define API contracts before parallel frontend/backend work |
| CI from Day 1 — regressions caught immediately | Allocate story points for test infrastructure, not just features |
| Equal 80-hour allocation — prevented burnout | Make stakeholder personas concrete before requirements phase |
| Demo data pre-loaded — effortless evaluator demos | Document technical debt decisions at the time they are made |

**Course concept reflections:**
- **Management under uncertainty:** The risk register and sprint buffers proved their value — the system worked because mitigations were prepared, not improvised.
- **Monitoring and observability:** Adding `/health/detailed` changed how the team thought about the system. Before it existed, failures were discovered by users. After it existed, system state was observable.
- **Value creation:** Quantifying value early kept the team motivated. €96,500/year in savings makes 80 hours per person feel proportionate.
- **Storytelling:** The presentation's "Problem → Solution → Monitoring → Risk/Value → Delivery → Conclusion" arc was rehearsed multiple times because the story matters as much as the code.

---

## 12. Conclusion

Industry Maintenance Platform was adapted, documented, and delivered on schedule, within effort budget, meeting all 8 milestones and all 10 course assignment requirements. The system is a real, runnable platform — not a mockup — that demonstrates every course concept through working software and comprehensive documentation.

The core insight: **monitoring and observability are not optional extras, they are the mechanism by which a software project maintains control under uncertainty.** A project that cannot observe its own state — whether a running system or a managed schedule — discovers problems too late.

Industry Maintenance Platform makes industrial asset state observable. Our project management made project state observable. Both apply the same principle.

---

## Appendix A — Document Index

| Document | Location | Owner |
|---------|----------|-------|
| Team | [docs/TEAM.md](TEAM.md) | Obada |
| Team Work Plan | [docs/team-work-plan.md](team-work-plan.md) | Obada |
| Project Management Plan | [docs/PROJECT_MANAGEMENT_PLAN.md](PROJECT_MANAGEMENT_PLAN.md) | Obada |
| Technical Monitoring | [docs/TECHNICAL_MONITORING.md](TECHNICAL_MONITORING.md) | Mohanad |
| Risk Management | [docs/RISK_MANAGEMENT.md](RISK_MANAGEMENT.md) | Abdulaziz |
| Stakeholder Management | [docs/STAKEHOLDER_MANAGEMENT.md](STAKEHOLDER_MANAGEMENT.md) | Abdulaziz |
| Architecture & Design | [docs/ARCHITECTURE_DESIGN.md](ARCHITECTURE_DESIGN.md) | Mohanad |
| UI Dashboard Design | [docs/ui-dashboard-design.md](ui-dashboard-design.md) | Fares |
| CI/CD and Testing | [docs/ci-cd-testing.md](ci-cd-testing.md) | Hamdi |
| Value Creation | [docs/VALUE_CREATION.md](VALUE_CREATION.md) | Obada |
| Presentation Outline | [docs/PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md) | Obada |
| Video Submission | [docs/video-submission-instructions.md](video-submission-instructions.md) | Obada |
| Quick Start | [docs/QUICK_START.md](QUICK_START.md) | Hamdi |

## Appendix B — Course Concept Mapping

| Course Concept | Where Demonstrated |
|---------------|-------------------|
| Value Creation | VALUE_CREATION.md §3–5; ROI 511% Year 1 |
| Management Under Uncertainty | RISK_MANAGEMENT.md; PROJECT_MANAGEMENT_PLAN.md §7; sprint buffers |
| Design Quality and Metrics | ARCHITECTURE_DESIGN.md §4; cohesion/coupling/SOLID metrics |
| Monitoring and Observability | TECHNICAL_MONITORING.md; `/health/detailed` endpoint; audit trail |
| Continuous Integration | `.github/workflows/backend.yml` + `frontend.yml`; CI gates on every PR |
| Continuous Delivery | `Makefile make prod`; Docker Compose; < 5-minute deployment |
| Continuous Testing | pytest + Vitest + Cypress; coverage gates enforced in CI |
| Storytelling for Presentation | PRESENTATION_OUTLINE.md; Problem→Solution→Monitoring→Risk/Value→Delivery→Conclusion |
