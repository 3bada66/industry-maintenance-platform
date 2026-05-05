# Stakeholder Management Plan
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Version:** 1.0  
**Owner:** Abdulaziz Alyahya (Risk Manager, 2309116441)

---

## 1. Stakeholder Identification

### 1.1 Internal Stakeholders

| ID | Name / Role | Organization | Interest | Influence |
|----|-------------|-------------|---------|-----------|
| IS-1 | Obada Abdulhakim Kharaz (PM) | Project Team | Project success, schedule, quality | High |
| IS-2 | Mohanad Aref Ali Sultan (Backend Dev) | Project Team | Backend quality, monitoring API | High |
| IS-3 | Zekeriya Dulli (Frontend Dev) | Project Team | UX quality, dashboard implementation | Medium |
| IS-4 | Praise-God Tobby (QA) | Project Team | System reliability, test coverage | Medium |
| IS-5 | Fares Stouhi (UX/UI Designer) | Project Team | Dashboard clarity, visual design | Medium |
| IS-6 | Hamdi Alnaqeeb (DevOps) | Project Team | Deployment stability, CI/CD | Medium |
| IS-7 | Abdulaziz Alyahya (Risk Manager) | Project Team | Risk visibility, stakeholder concerns | Medium |

### 1.2 External Stakeholders

| ID | Name / Role | Organization | Interest | Influence |
|----|-------------|-------------|---------|-----------|
| ES-1 | Course Supervisor / Examiner | University | Project quality, course alignment, academic integrity | High |
| ES-2 | Industrial Plant Manager (Simulated) | Fictitious Industrial Co. | Asset visibility, uptime, compliance reporting | High |
| ES-3 | IT Security Officer (Simulated) | Fictitious Industrial Co. | Data security, access control, audit trails | High |
| ES-4 | Maintenance Technician (Simulated) | Fictitious Industrial Co. | Easy asset lookup, mobile access, photo documentation | Medium |
| ES-5 | Procurement / Supply Chain (Simulated) | Fictitious Industrial Co. | Supplier and manufacturer data, asset lifecycle | Medium |
| ES-6 | Open-Source Community | GitHub / Industry Maintenance Platform | Code quality, license compliance, contributions | Low |
| ES-7 | Compliance Auditor (Simulated) | Regulatory Body | Audit trail completeness, data integrity | Medium |

*Note: ES-2 through ES-7 are simulated stakeholder personas used for requirements elicitation exercises. ES-1 is the real evaluating stakeholder.*

---

## 2. Stakeholder Analysis

### 2.1 Power / Interest Matrix

```
                    LOW INTEREST          HIGH INTEREST
                  ┌──────────────────────┬──────────────────────┐
HIGH POWER        │  KEEP SATISFIED       │  MANAGE CLOSELY       │
                  │  • ES-3 (IT Security) │  • ES-1 (Examiner)    │
                  │                       │  • ES-2 (Plant Mgr)   │
                  │                       │  • IS-1 (PM)          │
                  │                       │  • IS-2 (Tech Lead)   │
                  ├──────────────────────┼──────────────────────┤
LOW POWER         │  MONITOR              │  KEEP INFORMED        │
                  │  • ES-6 (Community)   │  • ES-4 (Technician)  │
                  │                       │  • ES-5 (Procurement) │
                  │                       │  • ES-7 (Auditor)     │
                  │                       │  • IS-3 to IS-7       │
                  └──────────────────────┴──────────────────────┘
```

### 2.2 Stakeholder Expectations

| Stakeholder | Primary Expectations | Success Criteria |
|------------|---------------------|-----------------|
| ES-1 (Course Examiner) | Demonstrates all course concepts; well-documented; runs locally | All 10 assignment requirements met; clear mapping to course concepts |
| ES-2 (Plant Manager) | Complete asset visibility across sites; risk overview; uptime | Dashboard shows all assets, risk scores, and system health in one view |
| ES-3 (IT Security) | Audit trail of all changes; role-based access; no data leakage | Every action logged; RBAC enforced; OWASP checklist passed |
| ES-4 (Technician) | Quick asset lookup by serial number or location; upload photos | Search returns results in < 200ms; photo upload < 5s |
| ES-5 (Procurement) | Supplier/manufacturer database linked to assets; lifecycle dates | Asset detail page shows supplier, manufacturer, warranty, purchase date |
| ES-7 (Auditor) | Immutable change log; who changed what and when | Audit logs are append-only, non-deletable, and exportable |

---

## 3. Communication Plan

### 3.1 Communication Matrix

| Audience | Message Type | Channel | Frequency | Owner |
|----------|-------------|---------|-----------|-------|
| IS-1 to IS-7 (Team) | Sprint planning, status, blockers | Stand-up meeting + GitHub | Weekly (Monday) | Obada |
| IS-1 to IS-7 (Team) | Technical decisions, code reviews | GitHub Pull Requests | Per PR | Mohanad |
| IS-1 to IS-7 (Team) | Risk and issue escalation | Email + meeting | As needed | Obada |
| ES-1 (Examiner) | Progress report, milestone updates | Formal email + submitted docs | Per milestone | Obada |
| ES-1 (Examiner) | Final submission | Course platform + USB/PDF | Week 16 | Obada |
| ES-1 (Examiner) | Presentation | In-person or recorded video | Week 16 | Obada |
| Simulated stakeholders | Requirements clarification | Written personas / use cases | Sprint 1 | Abdulaziz |

### 3.2 Meeting Schedule

| Meeting | Participants | Duration | Frequency | Output |
|---------|-------------|----------|-----------|--------|
| Weekly Stand-up | All team (IS-1..7) | 20 min | Weekly | Blocker list, task updates |
| Sprint Planning | All team | 1 hour | Every 3 weeks | Sprint backlog, assignments |
| Sprint Review | All team | 45 min | Every 3 weeks | Demo, acceptance criteria review |
| Sprint Retrospective | All team | 30 min | Every 3 weeks | Process improvements |
| Architecture Review | IS-2, IS-3, IS-4 | 1 hour | Weeks 2, 8, 13 | Architecture sign-off |
| Milestone Review | IS-1 + IS-2 | 30 min | Per milestone | Milestone acceptance |

### 3.3 Documentation Communication

All project documents are maintained in the `docs/` folder of the Git repository and are:
- Version-controlled alongside the source code
- Updated incrementally each sprint
- Formally submitted as a package in Week 16

---

## 4. Stakeholder Engagement Strategy

### 4.1 Course Examiner (ES-1) — Manage Closely
**Strategy:** Full transparency and early alignment.

| Action | Timing |
|--------|--------|
| Submit Project Management Plan for feedback | Week 3 |
| Demonstrate working prototype at mid-point | Week 8 |
| Share documentation draft for review | Week 14 |
| Final submission with video backup | Week 16 |

**Key Message to Examiner:** "This project demonstrates all 10 course requirements through a working system, not just documentation. Every concept — value creation, monitoring, CI/CD, risk management, design quality — is evidenced in both the running code and the documentation package."

### 4.2 Industrial Stakeholders (ES-2, ES-4, ES-5) — Keep Informed
**Strategy:** Use simulated requirements to drive realistic features.

Each industrial persona has a user story:
- **Plant Manager:** "As a plant manager, I want to see all assets and their risk scores on a single dashboard so I can prioritize maintenance."
- **Technician:** "As a maintenance technician, I want to search for an asset by location and see its photos and last maintenance date."
- **Procurement:** "As procurement, I want to see all assets linked to a specific supplier with their purchase dates and warranty expiry."

These user stories map directly to implemented features in Industry Maintenance Platform.

### 4.3 IT Security Officer (ES-3) — Keep Satisfied
**Strategy:** Demonstrate security posture proactively.

| Security Feature | Status |
|-----------------|--------|
| JWT Authentication | ✅ Implemented |
| Role-Based Access Control | ✅ Implemented |
| Audit Trail (all changes) | ✅ Implemented |
| Input Validation (Pydantic) | ✅ Implemented |
| HTML Sanitization | ✅ Implemented |
| Rate Limiting | ✅ Implemented |
| Multi-tenant Data Isolation | ✅ Implemented |
| HTTPS/TLS in Production | ✅ Configured |

---

## 5. Conflict Handling

### 5.1 Team-Internal Conflicts

The team follows a structured escalation process for disagreements:

**Level 1 — Direct Resolution (< 1 day)**  
Two parties discuss and reach consensus directly. Preferred for technical preferences with low impact.

**Level 2 — Facilitated Discussion (1–2 days)**  
Obada (PM) facilitates a structured discussion. Both sides present evidence (not opinion). Outcome documented in meeting notes.

**Level 3 — Backend/Tech Lead Decides (Same day)**  
For technical disputes (architecture, technology choices), Mohanad (Backend Developer) makes the final call after hearing both sides. His decision is final and not revisited during the project.

**Level 4 — PM Decision (Same day)**  
For scope, schedule, or resource disputes, Obada makes the final call.

### 5.2 Known Conflict Scenarios and Resolutions

| Scenario | Resolution Approach |
|----------|-------------------|
| "We should add feature X but we're running out of time" | PM evaluates scope change; defer to backlog if not critical |
| "This architecture approach is wrong" | Tech Lead facilitates design review with data; decision documented |
| "The test coverage is not good enough to ship" | QA engineer has veto power on P1 quality gates |
| "This UI doesn't match the mockup" | Frontend Dev and PM agree on acceptable delta; document deviation |
| "A team member is not contributing" | PM addresses in 1:1 first; then escalates to course supervisor if unresolved |

### 5.3 Escalation to Course Supervisor

Escalate to ES-1 (course supervisor) only if:
- A team member drops out and workload cannot be redistributed
- A fundamental scope misunderstanding with the course requirements is discovered
- Academic integrity concerns arise

*No escalations were required during this project.*

---

## 6. Stakeholder Feedback Log

| Date | Stakeholder | Feedback | Action Taken |
|------|------------|---------|-------------|
| Week 3 | ES-1 (Examiner) | "Ensure technical monitoring is clearly distinguished from management monitoring" | Added separate `/health/detailed` endpoint; created separate Technical Monitoring Dashboard |
| Week 6 | IS-4 (QA/Praise-God) | "Test coverage targets should be set explicitly, not left vague" | Added 70%/60% targets to definition of done |
| Week 9 | IS-3 (Zekeriya) | "Risk dashboard should show trends over time, not just current scores" | Added time-series risk chart to sprint 3 backlog |
| Week 13 | IS-2 (Lina) | "Architecture document needs explicit cohesion/coupling metrics, not just diagrams" | Added metrics section to Architecture Design document |
