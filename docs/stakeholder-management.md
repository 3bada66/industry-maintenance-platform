# Stakeholder Management
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.1
**Owner:** Abdulaziz Alyahya (Risk Manager, 2309116441)
**Communication Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)

---

## 1. Overview

Stakeholder management ensures that everyone affected by or influencing the Industry Maintenance Platform platform has clearly defined expectations, a reliable communication channel, and a known process for raising concerns. This document covers both internal stakeholders (the project team) and external stakeholders (users, clients, and evaluators).

### 1.1 Stakeholder Map

```
                    LOW INTEREST            HIGH INTEREST
                 ┌──────────────────────┬───────────────────────────┐
HIGH INFLUENCE   │  KEEP SATISFIED       │  MANAGE CLOSELY           │
                 │  • IT Administrator   │  • Course Instructor      │
                 │  • System Owner       │  • Project Manager        │
                 │                       │  • Backend Developer      │
                 │                       │  • Facility Manager       │
                 ├──────────────────────┼───────────────────────────┤
LOW INFLUENCE    │  MONITOR              │  KEEP INFORMED            │
                 │  • Open-source users  │  • End Users              │
                 │                       │  • Maintenance Team       │
                 │                       │  • QA / UX / DevOps / RM  │
                 │                       │  • Frontend Developer     │
                 └──────────────────────┴───────────────────────────┘
```

---

## 2. Internal Stakeholders

### 2.1 Summary Table

| ID | Name | Role | Student ID | Interest | Influence |
|----|------|------|-----------|---------|-----------|
| IS-1 | Obada Abdulhakim Kharaz | Project Manager | 2309115277 | Project success, schedule, quality | High |
| IS-2 | Mohanad Aref Ali Sultan | Backend Developer | 2309115898 | Backend quality, API correctness, monitoring endpoints | High |
| IS-3 | Zekeriya Dulli | Frontend Developer | 2309115377 | UX quality, dashboard implementation, routing | Medium |
| IS-4 | Praise-God Tobby | QA/Test Engineer | 2309116418 | System reliability, test coverage, regression prevention | Medium |
| IS-5 | Fares Stouhi | UX/UI Designer | 2309115179 | Dashboard clarity, visual design, user flows | Medium |
| IS-6 | Hamdi Alnaqeeb | DevOps/Operations Engineer | 2309116178 | Deployment stability, CI/CD pipeline, container health | Medium |
| IS-7 | Abdulaziz Alyahya | Risk Manager | 2309116441 | Risk visibility, stakeholder concerns, documentation | Medium |

---

### IS-1 — Project Manager

**Obada Abdulhakim Kharaz (2309115277)**

| Field | Detail |
|-------|--------|
| **Expectations** | All 7 team members deliver their assignments on time. Sprint velocity stays above 0.90 SPI. Documentation is written incrementally, not at the last minute. Final submission is complete and submitted by Week 16. |
| **Concerns** | Scope creep consuming buffer weeks. Team members becoming unavailable. Misalignment between implementation and course requirements. |
| **Communication method** | Chairs weekly Monday stand-up (20 min). Sends formal milestone update emails to the course instructor. Manages GitHub issues for blockers. |
| **Communication frequency** | Weekly stand-up + ad-hoc for blockers |
| **Conflict handling** | Level 4 decision-maker for scope, schedule, and resource disputes. Facilitates Level 2 discussions when technical disagreements arise. Escalates to course instructor only if a team member drops out or a fundamental scope misunderstanding is found. |

---

### IS-2 — Backend Developer

**Mohanad Aref Ali Sultan (2309115898)**

| Field | Detail |
|-------|--------|
| **Expectations** | Backend API is stable, tested (≥ 70 % coverage), and accurately documented. Health endpoints return correct data. Risk scoring logic is validated. Security controls (JWT, RBAC) are fully implemented and tested. |
| **Concerns** | Schema migrations breaking existing data. Third-party library CVEs. Performance degradation under multi-user load. Undocumented API contracts causing frontend–backend mismatches. |
| **Communication method** | GitHub Pull Requests for all code changes; technical decisions posted as PR comments or GitHub issues. Attends architecture review sessions (Weeks 2, 8, 13). |
| **Communication frequency** | Per PR + weekly stand-up |
| **Conflict handling** | Level 3 decision-maker for technical architecture and technology choices. Makes the final call after hearing all sides; decision is documented in the Architecture Design document. |

---

### IS-3 — Frontend Developer

**Zekeriya Dulli (2309115377)**

| Field | Detail |
|-------|--------|
| **Expectations** | All dashboard pages are functional, route correctly, and match the UX designs produced by IS-5. The Technical Monitoring and Management Monitoring dashboards auto-refresh and display live data. Frontend CI passes on every push. |
| **Concerns** | Breaking changes to API response shapes without notice. PrimeVue component version conflicts. Translation key gaps causing runtime `t(undefined)` errors in Italian or English. |
| **Communication method** | GitHub PRs; direct coordination with IS-5 (UX) on design delta acceptance; weekly stand-up. |
| **Communication frequency** | Per PR + weekly stand-up |
| **Conflict handling** | UI/design deviations from mockup are resolved with IS-5 (UX) and IS-1 (PM). Agreed deltas are documented in the sprint review notes. |

---

### IS-4 — QA / Test Engineer

**Praise-God Tobby (2309116418)**

| Field | Detail |
|-------|--------|
| **Expectations** | Test coverage meets targets (≥ 70 % backend, ≥ 60 % frontend) before code freeze. All CI tests pass. Health endpoint tests (`test_health.py`) accurately reflect the implemented response shapes. No P1 quality regressions ship after Sprint 3. |
| **Concerns** | Developers pushing untested code directly to `main`. Coverage targets being dropped under time pressure. Integration tests that rely on mocked databases masking real schema issues. |
| **Communication method** | GitHub CI status on every PR; coverage report reviewed in Sprint Retrospective; QA veto raised in stand-up. |
| **Communication frequency** | Per CI run (automated) + sprint retrospective |
| **Conflict handling** | IS-4 holds a veto on P1 quality gates: no deployment proceeds if a P1 defect is open. Disputes about what constitutes a P1 are resolved by IS-2 (Backend Lead). |

---

### IS-5 — UX/UI Designer

**Fares Stouhi (2309115179)**

| Field | Detail |
|-------|--------|
| **Expectations** | Dashboard wireframes (documented in `docs/ui-dashboard-design.md`) are implemented with acceptable fidelity by IS-3. Users can navigate the platform intuitively without training. Mobile-responsive layout is maintained. |
| **Concerns** | Developers implementing UI without reviewing the wireframes. Accessibility not being considered. Colour choices for status indicators (green/amber/red) clashing in high-contrast environments. |
| **Communication method** | Wireframes shared in `docs/ui-dashboard-design.md`; design feedback given on frontend PRs; attends Sprint Review demos. |
| **Communication frequency** | Per UI PR + sprint review |
| **Conflict handling** | Design deviations agreed with IS-3 (Frontend Dev) and IS-1 (PM). Acceptable delta is documented in sprint review notes. |

---

### IS-6 — DevOps / Operations Engineer

**Hamdi Alnaqeeb (2309116178)**

| Field | Detail |
|-------|--------|
| **Expectations** | CI/CD pipelines (`backend.yml`, `frontend.yml`) are green on every merge to main. `make prod` deployment succeeds on a clean machine. Docker image versions are pinned. Monitoring endpoints (`/health`, `/health/detailed`) are reachable post-deployment. |
| **Concerns** | Unpinned Docker image tags breaking builds. Node.js or Python version drift between local dev and CI. CI minutes being exhausted on a free GitHub tier. Missing environment variables causing silent runtime failures. |
| **Communication method** | GitHub Actions status badges in README; CI failure notifications via GitHub email; DevOps issues posted to GitHub. |
| **Communication frequency** | Per push (automated) + weekly stand-up |
| **Conflict handling** | Deployment blockers are treated as P2 and escalated to IS-1 immediately. CI bypass (`--no-verify`) is never used without explicit PM approval. |

---

### IS-7 — Risk Manager

**Abdulaziz Alyahya (2309116441)**

| Field | Detail |
|-------|--------|
| **Expectations** | Risk register (`docs/risk-management.md`) is kept current. All 14 identified risks have active owners and monitoring methods. Stakeholder feedback is logged and actioned. Documentation package is accurate at the time of submission. |
| **Concerns** | Risk register becoming stale after Sprint 2. Risks being closed prematurely before mitigations are verified. Poor stakeholder communication causing scope misalignment with the course instructor. |
| **Communication method** | Weekly risk review during Monday stand-up; maintains the Stakeholder Feedback Log; flags unmitigated risks to IS-1. |
| **Communication frequency** | Weekly + per milestone |
| **Conflict handling** | Raises risk-related concerns to IS-1 (PM). If a mitigation is contested, IS-2 (Backend Lead) provides technical opinion; IS-1 makes the final call. |

---

## 3. External Stakeholders

### 3.1 Summary Table

| ID | Role | Type | Interest | Influence |
|----|------|------|---------|-----------|
| ES-1 | Course Instructor / Examiner | Real | Academic quality, course alignment, working system | High |
| ES-2 | Industrial Facility Manager (Simulated) | Simulated | Asset visibility, uptime, risk overview | High |
| ES-3 | IT Administrator (Simulated) | Simulated | Security, access control, audit trails | High |
| ES-4 | End Users — Maintenance Technicians (Simulated) | Simulated | Fast asset lookup, photo upload, mobile access | Medium |
| ES-5 | System Owner / Client (Simulated) | Simulated | Business value, compliance, total cost | High |
| ES-6 | Maintenance Team (Simulated) | Simulated | Accurate asset records, maintenance history, location data | Medium |

*ES-2 through ES-6 are simulated stakeholder personas used for requirements elicitation and feature prioritisation. ES-1 is the only real external evaluating stakeholder.*

---

### ES-1 — Course Instructor / Examiner

| Field | Detail |
|-------|--------|
| **Expectations** | All 10 course requirements are demonstrably met. The system runs locally with a single command (`make prod`). Documentation is accurate, version-controlled, and complete. Technical monitoring, management monitoring, and risk management are each clearly evidenced in both code and documentation. |
| **Concerns** | Documentation claims not matched by actual running code. Monitoring being superficial (a single status badge rather than a real monitoring layer). Risk management being generic rather than platform-specific. |
| **Communication method** | Formal email from IS-1 at each milestone. Submitted document package at Week 16. In-person or recorded video presentation at Week 16. |
| **Communication frequency** | Per milestone (Weeks 3, 8, 14, 16) |
| **Conflict handling** | If a requirement is misunderstood, IS-1 (PM) sends a clarification email immediately. Scope adjustments made within buffer weeks. No unilateral interpretation of requirements — always confirmed in writing. |

---

### ES-2 — Industrial Facility Manager (Simulated)

| Field | Detail |
|-------|--------|
| **Expectations** | Single dashboard showing all assets across all sites with risk scores. Ability to drill down from a risk overview to a specific asset's detail page. Uptime and maintenance history visible without requiring technical knowledge. |
| **Concerns** | Dashboard being too technical for a non-IT manager. Risk scores not being actionable (no "what to do next" guidance). System being unavailable during a shift when a decision needs to be made. |
| **User story** | "As a facility manager, I want to see all assets and their risk scores on one screen so I can prioritise maintenance without opening multiple tools." |
| **Communication method** | Simulated user stories in sprint planning; UX review by IS-5 against this persona. |
| **Communication frequency** | Sprint 1 requirements elicitation; Sprint Review demos |
| **Conflict handling** | Conflicting requirements between ES-2 (visibility) and ES-3 (security) are resolved by defaulting to least-privilege: hide sensitive technical details from the management view unless the user has Editor/Admin role. |

---

### ES-3 — IT Administrator (Simulated)

| Field | Detail |
|-------|--------|
| **Expectations** | Every user action is logged in an immutable audit trail. Role-based access control prevents privilege escalation. No plaintext credentials are stored or logged. HTTPS is enforced. Failed login attempts are rate-limited and recorded. |
| **Concerns** | Default admin credentials not being changed after first deployment. JWT secret key being committed to the repository. API Swagger UI being enabled in production and exposing the internal API surface. |
| **User story** | "As an IT administrator, I want to see who changed what and when on every asset so I can satisfy compliance audits without manual log searching." |
| **Communication method** | Security feature status table reviewed at each milestone; OWASP checklist completed at code freeze. |
| **Communication frequency** | Per milestone security review |
| **Conflict handling** | Security requirements take precedence over convenience features. Any feature that weakens the security posture requires IS-2 approval and documentation of the accepted risk. |

---

### ES-4 — End Users — Maintenance Technicians (Simulated)

| Field | Detail |
|-------|--------|
| **Expectations** | Find any asset by serial number, location, or IP address in under 3 seconds. Upload photos and maintenance notes from a mobile device. See the full maintenance history of an asset on one page without scrolling through multiple tabs. |
| **Concerns** | Search being too slow for on-floor use. Photo upload failing on poor WiFi. Interface requiring a desktop browser — technicians often use tablets. |
| **User story** | "As a maintenance technician, I want to search for an asset by its location tag and immediately see its photos, last maintenance date, and network interfaces." |
| **Communication method** | Simulated via UX review by IS-5; Global spotlight search performance verified by IS-4 (QA). |
| **Communication frequency** | Sprint 2 and Sprint 4 UX review |
| **Conflict handling** | Performance requirements (< 200 ms search) are non-negotiable for this persona. If they conflict with feature richness, performance wins. |

---

### ES-5 — System Owner / Client (Simulated)

| Field | Detail |
|-------|--------|
| **Expectations** | The platform can be deployed on existing on-premise infrastructure without additional licensing costs. Total cost of ownership is predictable. The system is maintainable by an internal team without specialist knowledge. Compliance audit requirements are met out of the box. |
| **Concerns** | Hidden costs from cloud services or commercial monitoring tools being introduced later. Vendor lock-in from technology choices. Documentation being insufficient for a handover to an internal IT team. |
| **User story** | "As the system owner, I want a fully documented, open-source platform that my team can deploy and maintain without external consultants." |
| **Communication method** | Value creation document (`docs/value-creation.md`); architecture document (`docs/ARCHITECTURE_DESIGN.md`); deployment runbook (`docs/ci-cd-testing.md §3.2`). |
| **Communication frequency** | Document review at Week 14 submission |
| **Conflict handling** | Any introduction of a paid or proprietary dependency requires explicit system owner approval and must be justified against the free-infrastructure guarantee. |

---

### ES-6 — Maintenance Team (Simulated)

| Field | Detail |
|-------|--------|
| **Expectations** | Asset records are accurate and up to date. Physical location (site → area → location) is correctly mapped. Manufacturer, supplier, and warranty data are linked to each asset. The platform supports bulk import of asset data via CSV templates. |
| **Concerns** | Data entry errors creating incorrect risk scores for ICS components. Bulk import overwriting existing records without warning. No way to see what changed between two versions of an asset record. |
| **User story** | "As a member of the maintenance team, I want to bulk-import assets from our existing spreadsheet and see their risk scores immediately, without re-entering data manually." |
| **Communication method** | Simulated via data import testing by IS-4 (QA); CSV templates available in `frontend/public/`. |
| **Communication frequency** | Sprint 1 requirements + Sprint 3 data quality review |
| **Conflict handling** | Data integrity requirements (audit trail, no silent overwrite) take precedence over import convenience. Bulk import always shows a preview before committing. |

---

## 4. Communication Plan

### 4.1 Communication Matrix

| Audience | Message Type | Channel | Frequency | Owner |
|----------|-------------|---------|-----------|-------|
| IS-1 to IS-7 (Team) | Sprint planning, task assignments | Monday stand-up + GitHub issues | Weekly | Obada (IS-1) |
| IS-1 to IS-7 (Team) | Code reviews, technical decisions | GitHub Pull Requests | Per PR | Mohanad (IS-2) |
| IS-1 to IS-7 (Team) | Risk and issue escalation | Stand-up + direct message | As needed | Obada (IS-1) |
| IS-1 to IS-7 (Team) | Sprint retrospective | Meeting | Every 3 weeks | Obada (IS-1) |
| ES-1 (Instructor) | Progress update, milestone delivery | Formal email + submitted docs | Per milestone | Obada (IS-1) |
| ES-1 (Instructor) | Final submission | Course platform + document package | Week 16 | Obada (IS-1) |
| ES-1 (Instructor) | Presentation | In-person or recorded video | Week 16 | All team |
| Simulated stakeholders (ES-2–ES-6) | Requirements, user stories | Written personas, sprint planning | Sprint 1 | Abdulaziz (IS-7) |

### 4.2 Meeting Schedule

| Meeting | Participants | Duration | Frequency | Output |
|---------|-------------|----------|-----------|--------|
| Weekly Stand-up | All team (IS-1..7) | 20 min | Weekly (Monday) | Blocker list, task updates |
| Sprint Planning | All team | 1 hour | Every 3 weeks | Sprint backlog, assignments |
| Sprint Review | All team | 45 min | Every 3 weeks | Demo, acceptance review |
| Sprint Retrospective | All team | 30 min | Every 3 weeks | Process improvements, tech debt triage |
| Architecture Review | IS-2, IS-3, IS-6 | 1 hour | Weeks 2, 8, 13 | Architecture sign-off |
| Milestone Review | IS-1, IS-2 | 30 min | Per milestone | Milestone acceptance |
| Risk Review | IS-1, IS-7 | 15 min | Weekly (within stand-up) | Risk register update |

---

## 5. Stakeholder Expectations and Success Criteria

| Stakeholder | Primary Expectation | Success Criterion |
|------------|--------------------|--------------------|
| ES-1 (Instructor) | All course requirements demonstrated in running code and documentation | All 10 requirements mapped to evidence; system runs from `make prod` |
| ES-2 (Facility Manager) | Single dashboard showing asset risk overview | Dashboard renders all assets with risk scores in < 2 s |
| ES-3 (IT Admin) | Audit trail + RBAC + rate limiting | Every action logged; RBAC server-enforced; OWASP checklist passed |
| ES-4 (Technician) | Fast asset search + photo upload | Search < 200 ms; photo upload < 5 s |
| ES-5 (System Owner) | €0 infrastructure, fully documented | No paid dependencies; `docs/` package complete at Week 16 |
| ES-6 (Maintenance Team) | Accurate records + bulk import | CSV import available; audit trail shows change history |
| IS-1 (PM) | On-time delivery with SPI ≥ 0.90 | Final submission Week 16; SPI tracked in management dashboard |
| IS-2 (Backend) | Stable, tested, secure API | ≥ 70 % coverage; no open P1 security issues at submission |
| IS-4 (QA) | No regressions ship | CI green on all PRs; all health endpoint tests pass |

---

## 6. Conflict Handling

### 6.1 Internal Team Conflicts

| Level | Trigger | Process | Resolver | Timeframe |
|-------|---------|---------|---------|-----------|
| 1 — Direct | Preference difference, low impact | Two parties discuss directly | Both parties | < 1 day |
| 2 — Facilitated | Persistent disagreement, medium impact | PM facilitates; both sides present evidence | Obada (IS-1) | 1–2 days |
| 3 — Technical | Architecture or technology dispute | Backend Lead hears both sides, decides | Mohanad (IS-2) | Same day |
| 4 — Scope/Schedule | Feature scope or deadline dispute | PM makes final call | Obada (IS-1) | Same day |
| 5 — Escalation | Team member drops out; academic integrity | Notify course instructor | Course Instructor (ES-1) | Immediate |

### 6.2 Common Conflict Scenarios

| Scenario | Resolution |
|---------|-----------|
| "We need to add feature X but time is short" | PM evaluates; defer to backlog if not critical to course requirements |
| "This API design is wrong" | Backend Lead facilitates design review with data; documents decision |
| "Test coverage is insufficient to ship" | QA holds veto on P1 quality gate; no deployment until resolved |
| "The UI doesn't match the wireframe" | Frontend Dev and UX Designer agree on acceptable delta; PM documents deviation |
| "A stakeholder persona requirement conflicts with another" | Default to security > data quality > usability; document trade-off |
| "The examiner's requirements seem to conflict with what we built" | PM clarifies in writing with instructor; does not assume interpretation |

### 6.3 External Conflict Handling

| Conflict | Approach |
|---------|---------|
| ES-2 (visibility) vs ES-3 (security) | Least-privilege default: hide sensitive data unless user has appropriate role |
| ES-4 (speed) vs ES-2 (completeness) | Performance target is non-negotiable; add pagination/caching before adding fields |
| ES-5 (zero cost) vs feature demand | Reject any paid dependency; document the trade-off in the architecture decision log |
| ES-1 (requirement) vs team interpretation | Always seek written clarification; do not proceed on an assumption |

---

## 7. Stakeholder Feedback Log

| Date | Stakeholder | Feedback | Action Taken | Sprint |
|------|------------|---------|-------------|--------|
| Week 3 | ES-1 (Instructor) | "Ensure technical monitoring is clearly distinguished from management monitoring" | Added separate `/health/detailed` endpoint; created `TechnicalMonitoring.vue` and `ManagementMonitoring.vue` as distinct pages | Sprint 1 |
| Week 6 | IS-4 (QA/Praise-God) | "Test coverage targets should be set explicitly, not left vague" | Added ≥ 70 % / ≥ 60 % targets to definition of done; enforced in CI | Sprint 2 |
| Week 9 | IS-3 (Zekeriya) | "Risk dashboard should show trends over time, not just current scores" | Added time-series risk chart to Sprint 3 backlog | Sprint 3 |
| Week 13 | IS-2 (Mohanad) | "Architecture document needs explicit cohesion/coupling metrics, not just diagrams" | Added metrics section to Architecture Design document | Sprint 4 |
