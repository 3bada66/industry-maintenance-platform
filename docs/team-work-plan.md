# Team Work Plan
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring

---

## 1. Team Role Overview

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

## 2. Phase 1: Repository Audit and Scope Definition

**Main goal:**
Understand the existing Industry Maintenance Platform repository and define how it will be adapted to the course requirements for an Industrial Asset, Risk, Management, and Technical Monitoring Platform.

**Responsibilities:**

- **Project Manager (Obada):**
  - Coordinates all audit tasks across the team
  - Defines the final project scope and ensures alignment with course requirements
  - Confirms that the adapted system addresses asset management, risk assessment, technical monitoring, project progress monitoring, cost/schedule monitoring, stakeholder visibility, auditability, accountability, CI/CD, continuous testing, and observability

- **Backend Developer (Mohanad):**
  - Audits the FastAPI application: existing routes, health endpoints, database models (21 models), migration structure, authentication, audit logging, and risk scoring service
  - Identifies where monitoring-related endpoints exist and where they are missing
  - Documents the `/health` endpoint and notes that `/health/detailed` needs to be added

- **Frontend Developer (Zekeriya):**
  - Audits the Vue.js 3 frontend structure: router configuration, Pinia store, existing dashboard page, asset management pages, and component library (PrimeVue)
  - Identifies which pages already exist (Dashboard, Assets, NetworkMap, AuditLogs) and where monitoring dashboard views can be added without breaking the current UI

- **QA/Test Engineer (Praise-God):**
  - Audits existing test infrastructure: pytest suite in `backend/tests/`, Vitest configuration in `frontend/`, Cypress setup
  - Runs `make test` or `pytest` to check current test status
  - Documents which tests pass, which fail, and what test coverage exists

- **UX/UI Designer (Fares):**
  - Audits the existing interface: current dashboard layout, chart components (Chart.js), data table components, and navigation structure
  - Identifies visual extension points for the three new monitoring dashboards

- **DevOps/Operations Engineer (Hamdi):**
  - Audits Docker Compose files (dev, prod, prod-cloud), Makefile targets, GitHub Actions workflows (`backend.yml`, `frontend.yml`), Nginx configuration, and environment variable setup
  - Confirms local deployment works with `make prod`

- **Risk Manager (Abdulaziz):**
  - Identifies initial project risks: adaptation complexity, scope uncertainty, timeline risk, testing gaps, documentation completeness
  - Notes technical risks: broken CI pipeline, Docker incompatibility, missing health endpoints, incomplete frontend dashboard

**Deliverables:**
- Repository audit summary (contributed to `docs/PROJECT_REPORT.md` §1)
- Initial adaptation plan (contributed to `docs/PROJECT_MANAGEMENT_PLAN.md`)

---

## 3. Phase 2: Design and Planning

**Main goal:**
Plan the adapted system before implementation. Define what will be implemented, what will be prototyped, and what will be documented only.

**Responsibilities:**

- **Project Manager (Obada):**
  - Creates the milestone plan with 8 milestones across 16 weeks
  - Defines management monitoring KPIs: progress (story points), schedule (SPI), effort (CPI), milestone status, team workload
  - Coordinates the final report structure ensuring all 10 assignment requirements are covered

- **Backend Developer (Mohanad):**
  - Designs the `/health/detailed` endpoint: response schema, database ping, system resource reporting, component status
  - Plans the monitoring API response format for the frontend's Technical Monitoring Dashboard
  - Reviews the existing `dashboard_cache.py` and `risk_scoring.py` services

- **Frontend Developer (Zekeriya):**
  - Plans the dashboard extension: which Vue components to add, where to insert routing, how to fetch from `/health/detailed`
  - Defines prototype structure for the Technical Monitoring Dashboard page

- **QA/Test Engineer (Praise-God):**
  - Defines the full testing strategy covering unit, API, integration, UI, regression, and smoke tests
  - Creates the verification checklist for confirming the adapted system still runs correctly

- **UX/UI Designer (Fares):**
  - Designs layout wireframes for: Management Dashboard, Technical Monitoring Dashboard, Risk Dashboard
  - Documents user interaction flow, visual hierarchy, color coding (green/yellow/red health states), and data refresh behavior
  - Output: `docs/ui-dashboard-design.md`

- **DevOps/Operations Engineer (Hamdi):**
  - Defines the local deployment process: `make prod` → container health → health endpoint validation
  - Plans CI workflow: what triggers it, what it tests, what it must pass before merge
  - Plans local CD: step-by-step deployment runbook for the evaluator
  - Output: `docs/ci-cd-testing.md`

- **Risk Manager (Abdulaziz):**
  - Creates the risk categories (Technical, Management, External, Quality, Security)
  - Builds the probability/impact scoring model
  - Defines mitigation plans for each High risk
  - Defines risk monitoring frequency and escalation criteria
  - Output: `docs/RISK_MANAGEMENT.md`

**Deliverables:**
- `docs/ARCHITECTURE_DESIGN.md` — software design and analysis
- `docs/ui-dashboard-design.md` — dashboard layout and UX design
- `docs/RISK_MANAGEMENT.md` — risk register and management plan
- `docs/TECHNICAL_MONITORING.md` — monitoring strategy

---

## 4. Phase 3: Implementation and Repository Adaptation

**Main goal:**
Make small, safe, and meaningful changes to the repository that demonstrate the course concepts through working code rather than documentation alone.

**Responsibilities:**

- **Backend Developer (Mohanad):**
  - Implements `/health/detailed` endpoint in `backend/app/main.py` — returns database status, component health, system resources, and uptime
  - Verifies database connectivity check works (PostgreSQL ping via SQLAlchemy)
  - Documents all monitoring-related API behavior in `docs/TECHNICAL_MONITORING.md`
  - Does NOT modify existing working endpoints; adds only new ones

- **Frontend Developer (Zekeriya):**
  - Adds a Technical Monitoring Dashboard page to the Vue.js frontend that fetches from `/health/detailed` and displays health status panels
  - Uses existing PrimeVue components and Chart.js — no new dependencies
  - Adds route entry in `router.js` for the new page
  - Verifies the existing dashboard, assets, and all current pages still work after changes

- **QA/Test Engineer (Praise-God):**
  - Runs `make test` (or `pytest` directly) and records results
  - Runs `npm run test:unit` for frontend and records results
  - Adds simple pytest test for the `/health/detailed` endpoint if safe (< 10 lines)
  - Documents any failed tests with exact error output and proposed resolution

- **DevOps/Operations Engineer (Hamdi):**
  - Verifies that GitHub Actions `backend.yml` and `frontend.yml` pass after all changes
  - Adds or improves CI workflow if missing
  - Verifies `make prod` still produces a fully working system
  - Documents the complete local CD process in `docs/ci-cd-testing.md`

- **UX/UI Designer (Fares):**
  - Reviews the implemented Technical Monitoring Dashboard against the wireframes
  - Ensures information hierarchy, color coding, and panel labels match the design
  - Finalizes `docs/ui-dashboard-design.md` with actual screenshots or updated wireframes

- **Risk Manager (Abdulaziz):**
  - Verifies that the risk register correctly reflects the implemented/planned system (not the original open-source project)
  - Updates any risk status changes after implementation (e.g., T3 Build Failures → Resolved after CI verification)

- **Project Manager (Obada):**
  - Tracks progress against milestones
  - Resolves any scope conflicts (e.g., if a feature is too risky to implement, labels it as "planned" with clear justification)
  - Ensures all implemented changes remain consistent with course framing

**Deliverables:**
- `/health/detailed` endpoint (backend — implemented)
- Technical Monitoring Dashboard page (frontend — implemented or prototype)
- `.github/workflows/` CI files (verified or updated)
- Updated `README.md` with course project context

---

## 5. Phase 4: Documentation Completion

**Main goal:**
Create the full academic documentation package that maps every course requirement to a specific system feature or design decision.

**Document ownership:**

| Document | Main Owner | Supporting Roles |
|----------|------------|------------------|
| `docs/PROJECT_REPORT.md` | Project Manager (Obada) | All members |
| `docs/team-work-plan.md` | Project Manager (Obada) | All members |
| `docs/TECHNICAL_MONITORING.md` | Backend Developer (Mohanad) | DevOps/Operations Engineer (Hamdi), Project Manager (Obada) |
| `docs/RISK_MANAGEMENT.md` | Risk Manager (Abdulaziz) | Project Manager (Obada) |
| `docs/STAKEHOLDER_MANAGEMENT.md` | Risk Manager (Abdulaziz) | Project Manager (Obada) |
| `docs/VALUE_CREATION.md` | Project Manager (Obada) | Risk Manager (Abdulaziz) |
| `docs/ARCHITECTURE_DESIGN.md` | Backend Developer (Mohanad) | Frontend Developer (Zekeriya), DevOps/Operations Engineer (Hamdi) |
| `docs/ui-dashboard-design.md` | UX/UI Designer (Fares) | Frontend Developer (Zekeriya) |
| `docs/ci-cd-testing.md` | DevOps/Operations Engineer (Hamdi) | QA/Test Engineer (Praise-God) |
| `docs/PRESENTATION_OUTLINE.md` | Project Manager (Obada) | UX/UI Designer (Fares) |
| `docs/video-submission-instructions.md` | Project Manager (Obada) | QA/Test Engineer (Praise-God) |

**Writing guidelines:**
- Every document must be specific to the adapted industrial asset, risk, management, and technical monitoring platform
- Avoid generic writing — connect every claim to a specific feature, endpoint, component, or file in the repository
- Where a feature is fully implemented, label it **[Implemented]**
- Where a feature is prototyped or designed but not fully connected, label it **[Prototype]**
- Where a feature is planned for future work, label it **[Planned]**
- The first page of `docs/PROJECT_REPORT.md` must include the exact team table from this document

---

## 6. Phase 5: Verification and Quality Review

**Main goal:**
Check that the adapted project is complete, consistent, and ready for submission.

**Responsibilities:**

- **Project Manager (Obada):**
  - Checks all 10 assignment requirements against the final report and documentation
  - Verifies the final report covers: team, management monitoring, technical monitoring, software design, UI design, value creation, stakeholders, risk management, presentation outline, and course concept mapping
  - Signs off on final submission package

- **Backend Developer (Mohanad):**
  - Re-runs the backend and confirms `/health` and `/health/detailed` return correct responses
  - Verifies backend changes are documented in `docs/TECHNICAL_MONITORING.md` and `docs/ARCHITECTURE_DESIGN.md`

- **Frontend Developer (Zekeriya):**
  - Confirms the Technical Monitoring Dashboard page loads and displays data
  - Confirms all existing pages still function after adaptation changes

- **QA/Test Engineer (Praise-God):**
  - Runs the full test suite one final time and records the results in `docs/ci-cd-testing.md`
  - Checks that `make prod` still runs the complete system from scratch
  - Verifies that setup instructions in `docs/QUICK_START.md` are accurate

- **UX/UI Designer (Fares):**
  - Reviews all dashboard documentation for visual clarity
  - Confirms presentation slides match the final implemented system

- **DevOps/Operations Engineer (Hamdi):**
  - Runs `make prod` on a clean environment and confirms the system starts correctly
  - Verifies CI pipeline status (both `backend.yml` and `frontend.yml` green)
  - Confirms health endpoint returns `"status": "healthy"` on a running system

- **Risk Manager (Abdulaziz):**
  - Reviews risk register for completeness (all 11 risks with current status)
  - Reviews stakeholder management document for accuracy
  - Confirms the uncertainty section of the project report is complete

**Deliverables:**
- Final verification checklist (appended to `docs/PROJECT_REPORT.md`)
- Confirmed passing CI status

---

## 7. Phase 6: Presentation Preparation

**Main goal:**
Prepare a clear, evidence-based 7-minute presentation that demonstrates all course concepts through the adapted industrial platform.

**Slide ownership:**

| Slide | Topic | Owner |
|------|-------|-------|
| 1 | Problem and Project Idea | Project Manager (Obada) |
| 2 | System Overview and Architecture | Backend Developer (Mohanad) |
| 3 | Management Monitoring | Project Manager (Obada) |
| 4 | Technical Monitoring | Backend Developer (Mohanad) + DevOps/Operations Engineer (Hamdi) |
| 5 | Risk, Stakeholders, and Value | Risk Manager (Abdulaziz) |
| 6 | CI/CD, Testing, and Course Concepts | QA/Test Engineer (Praise-God) + DevOps/Operations Engineer (Hamdi) |
| 7 | Conclusion | Project Manager (Obada) |

**Cross-role responsibilities:**
- **UX/UI Designer (Fares):** Reviews all slides for visual clarity and hierarchy; provides dashboard screenshots for Slides 3–5
- **Frontend Developer (Zekeriya):** Supports live demo of dashboard pages for Slides 3–4 if applicable

**Presentation story arc:**
```
Problem → Solution → Monitoring → Risk/Value → Delivery → Conclusion
```

**Timing:**

| Segment | Duration | Speaker |
|---------|----------|---------|
| Slide 1: Problem and Project Idea | 1:00 | Obada |
| Slide 2: System Overview and Architecture | 1:00 | Mohanad |
| Slide 3: Management Monitoring | 1:00 | Obada |
| Slide 4: Technical Monitoring | 1:30 | Mohanad + Hamdi |
| Slide 5: Risk, Stakeholders, and Value | 1:00 | Abdulaziz |
| Slide 6: CI/CD, Testing, and Concepts | 0:30 | Praise-God + Hamdi |
| Slide 7: Conclusion | 1:00 | Obada |
| **Total** | **7:00** | |

**Total time must not exceed 7 minutes.**

See `docs/PRESENTATION_OUTLINE.md` for the full slide-by-slide script.
