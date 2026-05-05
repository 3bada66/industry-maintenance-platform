# Project Team
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring

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

## Role Summary

### Obada Abdulhakim Kharaz — Project Manager (2309115277)
Controls the overall project direction and ensures all course requirements are met. Owns the project timeline, milestone tracking, and the final project report. Coordinates between all team members, resolves scope conflicts, and leads the 7-minute presentation structure.

### Mohanad Aref Ali Sultan — Backend Developer (2309115898)
Inspects the FastAPI backend and adapts it for industrial asset and technical monitoring purposes. Implements or documents the `/health/detailed` endpoint, database connectivity check, monitoring API responses, and the backend logging strategy that supports observability.

### Zekeriya Dulli — Frontend Developer (2309115377)
Inspects the Vue.js 3 frontend and adapts or prototypes dashboard views for management monitoring, technical monitoring, and risk visualization. Works within the existing frontend structure and component library to avoid breaking current UI functionality.

### Praise-God Tobby — QA/Test Engineer (2309116418)
Owns the entire testing strategy across all layers: unit, API, integration, UI, regression, and smoke tests. Runs the available test suites, records test results and failures, and validates that the adapted platform still runs locally end-to-end after any changes.

### Fares Stouhi — UX/UI Designer (2309115179)
Designs all three monitoring dashboards: Management Dashboard, Technical Monitoring Dashboard, and Risk Dashboard. Produces layout wireframes, user interaction flow diagrams, and visual hierarchy documentation. Reviews all presentation slides for clarity and visual quality.

### Hamdi Alnaqeeb — DevOps/Operations Engineer (2309116178)
Owns all Docker and local deployment configuration, CI workflow files, and local CD plan. Validates that health-check endpoints work, that the system deploys with zero paid services, and that operational monitoring (logs, alerts, container health checks) is correctly documented.

### Abdulaziz Alyahya — Risk Manager (2309116441)
Owns the complete risk lifecycle: identification, assessment, mitigation, and monitoring. Maintains the risk register, models management under uncertainty, manages stakeholder concerns, and defines the requirements for the Risk Dashboard in collaboration with Fares.

---

## RACI Matrix

| Deliverable | Obada (PM) | Mohanad (Backend) | Zekeriya (Frontend) | Praise-God (QA) | Fares (UX/UI) | Hamdi (DevOps) | Abdulaziz (Risk) |
|-------------|------------|-------------------|---------------------|-----------------|---------------|----------------|------------------|
| Project Report | **A** | C | C | C | C | C | C |
| Team Work Plan | **A** | I | I | I | I | I | I |
| Backend / Health Endpoint | I | **A** | I | C | I | C | I |
| Frontend / Dashboards (code) | I | I | **A** | C | C | I | I |
| Dashboard UI Design | I | I | C | I | **A** | I | I |
| Test Strategy & Results | C | C | C | **A** | I | I | I |
| CI/CD Pipeline | I | C | I | C | I | **A** | I |
| Risk Register | C | I | I | I | I | I | **A** |
| Stakeholder Management | C | I | I | I | I | I | **A** |
| Value Creation | **A** | I | I | I | I | I | C |
| Monitoring Strategy | C | **A** | I | I | I | R | I |
| Software Design Analysis | C | **A** | C | I | I | C | I |
| Presentation Outline | **A** | C | C | C | R | C | C |
| Video Submission Instructions | **A** | I | I | C | I | I | I |

> **R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

---

## Notes on Responsibilities

This project adapts an existing open-source repository (Industry Maintenance Platform v1.1.0) for the Software Project Management & Technical Monitoring course. Team responsibilities are framed around **inspection, adaptation, and documentation** rather than full implementation from scratch:

- "Implements or documents" means that if a feature already exists in the repository, the team documents and maps it to course requirements; if it does not exist but is small and safe to add, it is implemented.
- "Adds or prototypes" means frontend changes are kept minimal and non-breaking; mock data is acceptable where live data is not yet wired.
- "Verifies and validates" means the QA engineer runs existing test suites and records results honestly, including failures.
- All changes preserve the existing system's ability to run locally with `make prod`.
