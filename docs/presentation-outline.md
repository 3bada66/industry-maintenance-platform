# Presentation Outline
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Format:** 7 slides · 7 minutes maximum
**Story arc:** Problem → Solution → Monitoring → Risk/Value → Delivery → Conclusion

**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)
**Design:** Fares Stouhi (UX/UI Designer, 2309115179)

---

## Speaker and Timing Plan

| Slide | Title | Speaker | Time |
|-------|-------|---------|------|
| 1 | Problem and Project Idea | Obada | 1:00 |
| 2 | System Overview and Architecture | Mohanad | 1:00 |
| 3 | Management Monitoring | Obada | 1:00 |
| 4 | Technical Monitoring | Mohanad + Hamdi | 1:30 |
| 5 | Risk, Stakeholders, and Value | Abdulaziz | 1:00 |
| 6 | CI/CD, Testing, and Course Concepts | Hamdi + Praise-God | 0:30 |
| 7 | Conclusion | Obada | 1:00 |
| **Total** | | | **7:00** |

*Zekeriya (Frontend) operates the live dashboard during Slides 3–4 if a live demo is used.*
*Fares (UX) reviews all slide visuals for consistency with the dashboard design document.*

---

## Slide 1 — Problem and Project Idea

**Speaker:** Obada Abdulhakim Kharaz
**Time:** 1:00 (0:00 – 1:00)

### Key Points

- Industrial plants manage hundreds of PLCs, HMIs, sensors, and switches — with asset data scattered across spreadsheets, paper logs, and Visio diagrams that are always out of date
- Risk assessments happen once a year with an external consultant — not continuously
- When a security incident occurs, there is no authoritative record of the asset's last known-good state
- **The gap:** most asset management tools were built for IT environments; they do not understand Purdue Model levels, ICS risk scoring, or OT audit requirements
- **The project:** we adapted Industry Maintenance Platform — an open-source industrial CMDB — into a complete industrial asset, risk, management, and technical monitoring platform, at zero infrastructure cost

### Visual Suggestion

Split screen: left side shows a messy Excel spreadsheet with 400 rows of asset data; right side shows the Industry Maintenance Platform dashboard with risk scores, charts, and a clean search bar.

### Speaker Notes

> "Every morning, a maintenance supervisor opens a 400-row spreadsheet to find which PLC needs servicing. She doesn't know its current risk score. She doesn't know who changed its configuration last week. When the compliance auditor arrives, she spends three weeks reconstructing change history from emails.
>
> This is a real, documented problem in industrial operations. Most tools were designed for IT — they don't speak the Purdue Model, they don't score ICS risk, and they don't survive an OT compliance audit.
>
> We adapted an existing open-source platform into a system that solves exactly this. Let me show you how."

---

## Slide 2 — System Overview and Architecture

**Speaker:** Mohanad Aref Ali Sultan
**Time:** 1:00 (1:00 – 2:00)

### Key Points

- **Stack:** FastAPI 0.104.1 (backend) · Vue.js 3 (frontend) · PostgreSQL 15 (database) · Docker Compose (deployment)
- **Scale:** 31 REST API routers · 24 database models · 26 Pydantic schemas · 25+ frontend pages
- **Three-tier architecture:** Vue SPA → FastAPI → PostgreSQL — strict layer boundaries, no business logic in the database
- **Key features already in the open-source base:** asset CRUD, risk scoring engine (`risk_scoring.py`), immutable audit trail, RBAC, network map, multi-tenancy
- **What we added:** `/health/detailed` monitoring endpoint · Technical Monitoring Dashboard · Management Monitoring Dashboard · Risk Dashboard · 29 frontend unit tests · CI syntax check step

### Visual Suggestion

Three-tier architecture diagram with service names and port numbers. Feature matrix table: Feature | Existed in v1.1.0 | Added by Team.

### Speaker Notes

> "The system is a standard three-tier web application. FastAPI handles all business logic through 31 routers — each one responsible for exactly one domain entity. Vue.js renders the interface and talks to the API through a single authenticated Axios client. PostgreSQL stores everything in 24 tables with full multi-tenant isolation.
>
> The original open-source Industry Maintenance Platform already had asset management, risk scoring, and audit logging. Our team added the monitoring layer — the health endpoints, three new dashboards, and the testing infrastructure — and then documented every feature against the course requirements."

---

## Slide 3 — Management Monitoring

**Speaker:** Obada Abdulhakim Kharaz
**Time:** 1:00 (2:00 – 3:00)

### Key Points

- **Endpoint:** `GET /api/v1/management/status` — returns 14 management metrics in a single JSON response
- **Dashboard:** `/management` — auto-refreshes every 60 seconds; shows project health without asking any team member directly
- **SPI (Schedule Performance Index):** 0.96 — 4 % behind ideal schedule; within the ±10 % on-track threshold
- **Sprint velocity:** 45 → 52 → 54 → 48 story points across four sprints — consistent delivery
- **Team workload:** 7-member table with a `<ProgressBar>` that turns red if any member exceeds 95 % load
- **Milestones:** 7 milestones tracked from project kickoff to final submission; all 6 completed milestones met on time

### Visual Suggestion

Screenshot of the live Management Monitoring Dashboard at `/management` — KPI tiles row at the top, sprint velocity bars below, team workload table with progress bars.

### Speaker Notes

> "Management monitoring answers one question: is the project on track?
>
> We built a backend endpoint that returns 14 KPIs — sprint number, SPI, task completion percentage, team workload per member, milestone status, and cost variance — in a single JSON response. The Vue dashboard polls it every 60 seconds.
>
> Before this existed, the PM had to ask each team member for their status in the stand-up. With the dashboard, the PM reads the signals before the meeting and the stand-up focuses on blockers, not status reporting.
>
> SPI is 0.96 — the project is 4% behind the ideal schedule, well within our ±10% threshold."

---

## Slide 4 — Technical Monitoring

**Speaker:** Mohanad Aref Ali Sultan + Hamdi Alnaqeeb
**Time:** 1:30 (3:00 – 4:30)

### Key Points

- **Two health endpoints** — unauthenticated (monitoring systems must access them without credentials):
  - `GET /health` → `{"status":"ok","database":"connected","uptime":"running","timestamp":"...Z"}` — used by Docker healthcheck
  - `GET /health/detailed` → full JSON with database response time, connection pool, CPU %, memory %, disk %, Python version, uptime seconds
- **Dashboard:** `/monitoring` — auto-refreshes every 30 seconds; full-width status banner changes colour (green/amber/red) based on overall system status
- **Three-level downtime prevention:**
  - Level 1: Docker `healthcheck` pings `/health` every 30 s; restarts container after 3 failures (recovery ≤ 90 s, no human action needed)
  - Level 2: Dashboard polls `/health/detailed` every 30 s; degraded status shows red banner before users notice errors
  - Level 3: `logs/security.log` in JSON format — spike in 401 login failures signals brute-force attempt
- **10 metrics tracked:** database status, DB response time, API uptime, CPU %, memory %, disk %, error rate, audit activity, deployment status, container restart count
- **System resources** via `psutil 5.9.8` — CPU, memory, disk visible in the dashboard when the library is installed

### Visual Suggestion

Two-panel screenshot: left shows `GET /health/detailed` JSON response in a terminal; right shows the Technical Monitoring Dashboard with the green status banner and system resource progress bars.

### Speaker Notes

*(Mohanad speaks first — 45 seconds)*

> "Technical monitoring starts at the backend. The `/health/detailed` endpoint collects 10 metrics in a single request: database connectivity, query response time, connection pool usage, CPU, memory, disk, uptime, and Python version. No authentication required — monitoring tools need unconditional access.
>
> The endpoint live-pings PostgreSQL with SELECT 1 and measures the response time. If psutil is installed, it adds CPU and memory from the OS. The timestamp is always UTC with a Z suffix."

*(Hamdi takes over — 45 seconds)*

> "At the infrastructure level, Docker's healthcheck pings this endpoint every 30 seconds. Three consecutive failures trigger an automatic container restart — typically within 90 seconds, without any human action.
>
> At the application level, the Technical Monitoring Dashboard at /monitoring polls the same endpoint every 30 seconds. If the status banner turns red, the operator knows before the first user reports an error.
>
> Detection time without monitoring: however long until someone notices. Detection time with our setup: 30 seconds."

---

## Slide 5 — Risk, Stakeholders, and Value

**Speaker:** Abdulaziz Alyahya
**Time:** 1:00 (4:30 – 5:30)

### Key Points

**Risk Management:**
- 14 risks identified across 9 categories (Scope, Resource, Technical, Quality, Schedule, Security, Infrastructure, Stakeholder, Operational)
- 4 high-severity, 6 medium, 4 low — all with a named owner, mitigation, and contingency plan
- Risk Dashboard at `/risk` surfaces asset-level risk scores (computed by `risk_scoring.py`) alongside project-level risks

**Stakeholder Management:**
- 7 internal stakeholders (team members) with non-overlapping responsibilities and backup role assignments
- 6 external stakeholders: Course Instructor (real evaluator), Plant Manager, IT/OT Security Officer, Maintenance Technician, Compliance Auditor, Open-Source Community
- 4-level conflict escalation — peer resolution first; instructor involvement only for grading disputes

**Value Creation:**
- Infrastructure cost: **€0** (Docker, PostgreSQL, GitHub Actions, Nginx — all open source / free tier)
- Commercial equivalent (Claroty, Dragos): €50,000–€200,000/year in licensing
- Year 1 operational benefit estimate for a medium industrial plant: **€110,000+**
  - Reduced technician lookup time: €15,000
  - Faster compliance audits: €40,000
  - Preventive maintenance from continuous risk scoring: €40,000
  - Eliminated consultant risk assessment: €15,000

### Visual Suggestion

Three-column layout: left column = risk table (top 5 risks with severity badges); centre column = stakeholder power/interest grid; right column = value KPI tiles (€0 cost, €110k benefit).

### Speaker Notes

> "Three course concepts in 60 seconds.
>
> Risk: we identified 14 project risks, scored each by impact times probability, assigned an owner, and wrote a mitigation and contingency plan for every one. The Risk Dashboard makes asset-level risk visible continuously — not annually through a consultant.
>
> Stakeholders: we mapped 13 stakeholders — 7 internal and 6 external. Each has expectations, a communication method, and a conflict handling approach. The most important external stakeholder is the course instructor — the person evaluating this presentation.
>
> Value: the infrastructure cost of this system is exactly zero euros. Commercial equivalents cost up to €200,000 per year. Our Year 1 benefit estimate is €110,000 for a medium industrial facility — through faster lookups, faster audits, and preventive maintenance from continuous risk scores."

---

## Slide 6 — CI/CD, Testing, and Course Concepts

**Speaker:** Hamdi Alnaqeeb + Praise-God Tobby
**Time:** 0:30 (5:30 – 6:00)

### Key Points

- **Two CI pipelines** (GitHub Actions, free tier):
  - `backend.yml`: Python syntax check → app import check → pytest against real PostgreSQL 15 → coverage report
  - `frontend.yml`: `npm ci` → Vitest unit tests → Vite production build
- **Tests:** 4 backend test files (~75 pytest assertions) + `useStatus.spec.js` (29 Vitest assertions) — all passing
- **CD:** `make prod` deploys the full stack in < 5 minutes — Docker builds, migrations, health confirmed
- **Smoke tests** run after every deployment: `/health`, `/health/detailed`, login, authenticated API call
- **Total infrastructure cost: €0**
- **Course concepts demonstrated in running software:** management monitoring · technical monitoring · CI/CD · continuous testing · risk management · value creation · stakeholder management · design quality · management under uncertainty · UI/dashboard design

### Visual Suggestion

Two-panel: left shows a green GitHub Actions CI check on a pull request; right shows the `make prod` terminal output with "All services healthy" confirmation.

### Speaker Notes

*(Hamdi — 15 seconds)*

> "Both pipelines run on every push with zero cost. The backend pipeline adds a syntax and import check before running tests — we learned from a prior incident that silent import errors waste sprint time. All tests pass against a real PostgreSQL container."

*(Praise-God — 15 seconds)*

> "On the testing side: 75 backend assertions cover health, auth, user management, and integration flows. 29 Vitest assertions cover the useStatus composable with a vue-i18n mock. After every deployment, four smoke-test curl commands confirm the system is alive. Every course concept has a running implementation behind it."

---

## Slide 7 — Conclusion

**Speaker:** Obada Abdulhakim Kharaz
**Time:** 1:00 (6:00 – 7:00)

### Key Points

- **What was delivered:** running industrial monitoring platform · 3 dashboards · 2 CI pipelines · ~100 tests · 30+ documentation files · 7 milestones met · SPI 0.96 · CPI 1.02
- **The system is real:** `make prod` → login in 5 minutes · pre-loaded with demo data · every feature accessible from the navigation sidebar
- **The core insight:** monitoring and observability are not optional extras — they are the mechanism by which a project maintains control under uncertainty. Industry Maintenance Platform makes industrial asset state observable. Our project management made project state observable. Both apply the same principle.
- **Course concepts:** every requirement demonstrated through working software and specific file references — not claims or diagrams
- **Closing offer:** repository is open-source (AGPL-3.0); `make demo` loads 8 assets, 3 sites, and a complete network topology in under 2 minutes

### Visual Suggestion

Final slide: full-width screenshot of the Technical Monitoring Dashboard showing a green "HEALTHY" banner, overlaid with a 4-line summary text in the bottom-right corner:

```
7 milestones — all met
SPI 0.96 · CPI 1.02
€0 infrastructure cost
make prod → running in 5 minutes
```

### Speaker Notes

> "We started with a spreadsheet problem in an industrial plant. We ended with a running platform that makes asset state observable, continuous, and auditable — at zero infrastructure cost.
>
> Every course concept — management monitoring, technical monitoring, CI/CD, testing, risk management, value creation, stakeholder management — is demonstrated by a working feature with a specific file reference in the project report. Not claims. Working code.
>
> The system is live. You can run it yourself with `make prod` in under 5 minutes. Thank you."

---

## Timing Summary

```
0:00 – 1:00  Slide 1  Problem and Project Idea          Obada
1:00 – 2:00  Slide 2  System Overview and Architecture  Mohanad
2:00 – 3:00  Slide 3  Management Monitoring             Obada
3:00 – 4:30  Slide 4  Technical Monitoring              Mohanad + Hamdi
4:30 – 5:30  Slide 5  Risk, Stakeholders, and Value     Abdulaziz
5:30 – 6:00  Slide 6  CI/CD, Testing, Course Concepts   Hamdi + Praise-God
6:00 – 7:00  Slide 7  Conclusion                        Obada
─────────────────────────────────────────────────────────────────
TOTAL                                                    7:00
```

---

## Rehearsal Checklist

Before the presentation:

- [ ] All 7 speakers have read their script at least once
- [ ] Fares has reviewed all slides for visual consistency
- [ ] Zekeriya has confirmed the live dashboard demo works (`make prod` + login)
- [ ] Total timed rehearsal completed — final time must be ≤ 7:00
- [ ] Slide transitions do not add more than 15 seconds total
- [ ] Hamdi has confirmed the recording equipment (for video backup) is working
- [ ] Each speaker knows their handoff cue to the next speaker
