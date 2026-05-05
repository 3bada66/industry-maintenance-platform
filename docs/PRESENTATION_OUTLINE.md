# 7-Minute Presentation Outline
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Owner:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)  
**Reviewer:** Fares Stouhi (UX/UI Designer, 2309115179)

**Presentation story arc:** Problem → Solution → Monitoring → Risk/Value → Delivery → Conclusion

---

## Slide and Speaker Assignment

| Slide | Topic | Speaker | Duration |
|------|-------|---------|----------|
| 1 | Problem and Project Idea | Obada (PM) | 1:00 |
| 2 | System Overview and Architecture | Mohanad (Backend) | 1:00 |
| 3 | Management Monitoring | Obada (PM) | 1:00 |
| 4 | Technical Monitoring | Mohanad + Hamdi | 1:30 |
| 5 | Risk, Stakeholders, and Value | Abdulaziz (Risk Manager) | 1:00 |
| 6 | CI/CD, Testing, and Course Concepts | Praise-God + Hamdi | 0:30 |
| 7 | Conclusion | Obada (PM) | 1:00 |
| **Total** | | | **7:00** |

*UX/UI Designer (Fares) reviews all slides for visual clarity and provides dashboard screenshots.*  
*Frontend Developer (Zekeriya) supports live dashboard demo for Slides 3–4 if applicable.*

---

## Slide-by-Slide Script

---

### SLIDE 1 — Problem and Project Idea (0:00–1:00)
**Speaker:** Obada Abdulhakim Kharaz  
**Title:** "The Industrial Asset Management Gap"

**Visual:** Split screen — messy Excel spreadsheet on left, clean Industry Maintenance Platform dashboard on right

**Script:**
> "Every morning, a maintenance supervisor at an industrial plant opens a 400-row spreadsheet to find which PLC needs servicing. She doesn't know its risk score. She can't see who changed its configuration last week. When the compliance auditor arrives — she spends three weeks reconstructing change history from emails.
>
> This is the real problem: most asset management tools were designed for IT environments. They don't speak the Purdue Model. They don't score ICS risk. They don't survive an OT audit.
>
> We adapted Industry Maintenance Platform — an open-source industrial asset management system — into a complete industrial asset, risk, management, and technical monitoring platform. Let me show you how."

**Key numbers to show:**
- 500 industrial assets → 15–30 min search time per lookup (before)
- After: < 30 seconds with spotlight global search
- €132,500/year in avoidable costs for a medium industrial plant

---

### SLIDE 2 — System Overview and Architecture (1:00–2:00)
**Speaker:** Mohanad Aref Ali Sultan  
**Title:** "What Industry Maintenance Platform Is — Architecture and Capabilities"

**Visual:** Three-tier architecture diagram (from ARCHITECTURE_DESIGN.md §1.1) + feature matrix

**Script:**
> "Industry Maintenance Platform is a three-tier web platform: FastAPI backend on Python, Vue.js 3 frontend, PostgreSQL 15 database — all running locally on Docker with zero cloud dependencies.
>
> The backend has 21 data models, 29 REST API routers, and 17 service modules — including an ICS-specific risk scoring engine that evaluates each asset by Purdue level, business criticality, physical access ease, and remote access exposure.
>
> We adapted this system in two key ways: I added the `/health/detailed` endpoint that makes the system technically observable — database status, response time, memory, CPU, all in one JSON response. And Zekeriya added the Technical Monitoring Dashboard that displays this data in real time."

**Key architecture points:**
- 21 models (assets, sites, areas, interfaces, connections, users, audit logs...)
- `/health` (basic) + `/health/detailed` (new — returns DB ping, CPU, memory, uptime)
- Immutable audit trail — every change recorded with user, timestamp, IP

---

### SLIDE 3 — Management Monitoring (2:00–3:00)
**Speaker:** Obada Abdulhakim Kharaz  
**Title:** "Managing the Project and the Product"

**Visual:** Gantt chart (simplified) + Earned Value table + dashboard screenshot

**Script:**
> "Management monitoring means making progress, schedule, cost, and team workload visible — both for the product and for our project.
>
> For the project: 16 weeks, 7 team members, 560 planned hours, 4 Agile sprints. At code freeze (Week 13):
> - Schedule Performance Index: 0.99 — essentially on schedule
> - Cost Performance Index: 0.99 — essentially on effort budget
> - All 8 milestones met
>
> For the product: the Management Dashboard shows total assets, risk distribution, assets by site, and the 5 most critical assets — all in one view, updated each time the page loads.
>
> Equal workload: each of the 7 team members contributed 80 hours. No hero culture — if someone got sick, two others had coverage built into the RACI matrix."

---

### SLIDE 4 — Technical Monitoring (3:00–4:30)
**Speaker:** Mohanad Aref Ali Sultan + Hamdi Alnaqeeb  
**Title:** "Making the System Observable" (Live Demo)

**Visual:** Browser showing live Industry Maintenance Platform instance

**Script (Mohanad — 3:00–3:50):**
> "Technical monitoring means the system can report on its own health — without someone having to log in and guess.
>
> [opens browser to https://localhost/monitoring]
>
> This is the Technical Monitoring Dashboard. It auto-refreshes every 30 seconds from our `/health/detailed` endpoint.
>
> Green badge — all systems healthy.
> Database response: 3ms, pool: 2 of 20 connections used.
> Memory: 38%, CPU: 12% — well below alert thresholds.
>
> [opens terminal]
> Here's the raw data behind the dashboard:
> `curl -k https://localhost/health/detailed`
>
> Database status, component health, system resources — all observable without logging into the server."

**Script (Hamdi — 3:50–4:30):**
> "And this observability is backed by Docker health checks. Every container has a health check configured. If the backend fails to respond to `/health` for 2 minutes — that's a P1 alert.
>
> Structured JSON logs flow from the application to Docker stdout. Nine alert rules are defined, from P1-Critical (API down, DB connection exhausted) to P3-Medium (slow dashboard, disk usage rising).
>
> The CI pipeline itself is a monitoring signal — a failing build means a quality regression was introduced. It blocks the merge. We don't bypass it."

---

### SLIDE 5 — Risk, Stakeholders, and Value (4:30–5:30)
**Speaker:** Abdulaziz Alyahya  
**Title:** "Managing What We Couldn't Predict"

**Visual:** Risk matrix + Power/Interest grid + ROI bar chart

**Script:**
> "Risk management is about making uncertainty visible and responding before it becomes an incident.
>
> I identified 11 risks across 5 categories. Four were rated High. The most dangerous: a database migration failure — low probability, but if it happens in production, it's critical. Our mitigation: test on dev first, take a backup before every migration, keep a rollback script ready.
>
> The most likely: scope creep, rated 4 out of 5 probability. Our mitigation: strict change control and a code freeze from Week 11. Zero critical incidents occurred.
>
> For stakeholders: our primary stakeholder is the course examiner — we engaged proactively with early document submissions and a Week 8 prototype. Our simulated industrial stakeholders — plant manager, IT security officer, technician, procurement, auditor — drove every feature requirement. Each feature traces to a user story.
>
> On value: total project cost €14,000 notional. Year 1 benefit for a medium plant: €96,500. ROI: 511%. Payback: 7 weeks."

---

### SLIDE 6 — CI/CD, Testing, and Course Concepts (5:30–6:00)
**Speaker:** Praise-God Tobby + Hamdi Alnaqeeb  
**Title:** "Delivery as a Quality System"

**Visual:** GitHub Actions screenshot with green checkmarks + testing pyramid diagram

**Script (Praise-God — 5:30–5:45):**
> "Testing is continuous, not just at the end. Every push to any branch triggers both pipelines. Backend: pytest against a real PostgreSQL 15 instance — no mocks, because mocked tests can pass while real migrations fail. Frontend: Vitest unit tests plus a full Vite production build.
>
> Coverage: 73% backend, 64% frontend — both above our minimum targets. If either pipeline fails, the PR is blocked."

**Script (Hamdi — 5:45–6:00):**
> "Delivery is one command: `make prod`. Full production system in under 5 minutes. Self-signed TLS, Nginx, PostgreSQL, demo data — all included. Zero paid services. Zero cloud dependencies."

---

### SLIDE 7 — Conclusion (6:00–7:00)
**Speaker:** Obada Abdulhakim Kharaz  
**Title:** "Industry Maintenance Platform: Running Right Now"

**Visual:** Live browser at https://localhost + team table

**Script:**
> "Industry Maintenance Platform is not a mockup. It's running right now.
>
> `make prod` — and any evaluator has a full production-grade industrial asset management platform in under 5 minutes. Demo data pre-loaded: 8 industrial assets, 3 sites, 4 manufacturers, complete network topology, risk scores calculated, audit trail recording every change.
>
> We built this as 7 students adapting an open-source system — but we managed it like a real project: sprint planning, earned value tracking, risk registers, stakeholder communication, and CI/CD as quality gates.
>
> The system makes industrial assets observable. Our project management made the project observable. Both are the same discipline.
>
> Thank you. We're happy to demo any specific feature or take questions."

---

## Timing Discipline

| Buffer | Allocation |
|--------|-----------|
| Hard limit | 7:00 |
| Natural end | 6:45 |
| Questions buffer | 0:15 |

**Practice schedule:**
- Each speaker rehearses their segment alone: 3× minimum
- Full team rehearsal: 2× minimum (once with live demo, once with fallback screenshots)
- Final dress rehearsal on the actual recording/presentation machine

---

## Fallback Plan

| Failure | Fallback |
|---------|----------|
| `make prod` fails | Show pre-recorded demo video clip (1:30 of the dashboard) |
| Browser is slow | Pre-loaded screenshots from `docs/ui-dashboard-design.md` |
| Health endpoint returns unhealthy | Show JSON sample from TECHNICAL_MONITORING.md §2.2 |
| Speaker absent | PM (Obada) covers; slides pre-loaded; all segments scripted |

---

## Visual Requirements (Fares — UX/UI Designer)

Fares reviews all slides before final recording for:
- [ ] Consistent color palette (blue/green/amber/red from ui-dashboard-design.md §5.3)
- [ ] Text minimum 28pt on slides (readable on projected screen)
- [ ] No slide has more than 5 bullet points
- [ ] Architecture diagram is readable at 1080p
- [ ] Dashboard screenshots are cropped to show the most important panel
- [ ] Slide 7 includes the team table from TEAM.md
