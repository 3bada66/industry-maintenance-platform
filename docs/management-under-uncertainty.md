# Management Under Uncertainty
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring
**Version:** 1.0
**Owner:** Abdulaziz Alyahya (Risk Manager, 2309116441)
**Supporting:** Obada Abdulhakim Kharaz (Project Manager, 2309115277)

---

## 1. What This Document Covers

Software projects never execute exactly as planned. The question is not whether uncertainty will occur, but how the team responds when it does. This document describes how the Industry Maintenance Platform team manages eight specific uncertainty scenarios that arise in every real software project, using the risk register, change control, prioritization, milestone review, and other practical mechanisms.

The approach is grounded in one principle: **uncertainty is normal; unmanaged uncertainty is a failure of process, not a failure of luck.**

---

## 2. Sources of Uncertainty in This Project

Before describing responses, it is important to name where uncertainty comes from in this specific project:

| Source | Specific to This Project |
|--------|-------------------------|
| Scope | The project adapts an existing open-source platform; the boundary between "adaptation" and "new feature" is not always clear |
| Resource | 7 students with overlapping course obligations; unavailability is not exceptional — it is expected |
| Technical | Inherited codebase — some components are not fully understood at sprint start |
| Schedule | 16-week university term with fixed submission dates; no float available near week 16 |
| Quality | Test coverage on the inherited codebase was unknown at the start of the project |
| External | Course requirements may be interpreted or clarified by the instructor during the project |

---

## 3. Changing Requirements

### 3.1 How It Happens

Requirements change in two ways: the instructor clarifies or extends the course brief; or a team member proposes adding a feature beyond the agreed scope.

### 3.2 Response Strategy

**Change control board:** All scope changes are reviewed by the PM (Obada) before implementation begins. A request is not a commitment — it enters a backlog for evaluation.

**Assessment criteria:** A change is accepted if it (a) maps to a course deliverable, (b) can be completed within the current sprint without displacing committed stories, and (c) does not require significant rework of finished work.

**Documentation:** Every accepted scope change is recorded in the sprint backlog with its requester, date, and rationale. Rejected changes are also documented to prevent the same request appearing in a later sprint without context.

**Scope freezing near deadline:** From Week 13 onwards, no new features are accepted. Only bug fixes, documentation completion, and test writing are in scope. This is enforced even if a team member proposes a "small" addition — scope creep in the final three weeks is the most common cause of incomplete submissions.

### 3.3 In Practice

When the course brief required a Management Monitoring Dashboard (not part of the original Industry Maintenance Platform open-source codebase), the PM evaluated it against all criteria, assigned it to Sprint 4, and allocated it to the backend and frontend developers as a scoped task with a defined endpoint shape and dashboard layout. It was not added ad-hoc.

---

## 4. Delays

### 4.1 How It Happens

Delays occur when a task takes longer than estimated, when a dependency is late, or when a team member is unavailable (see §9).

### 4.2 Response Strategy

**Early detection:** The SPI (Schedule Performance Index) on the Management Monitoring Dashboard is recalculated each sprint. An SPI below 0.90 triggers a recovery conversation at the next stand-up — not at the end-of-sprint review when it is too late to act.

**Weekly progress reports:** Each Friday, the PM reviews sprint completion against the plan. The three questions are: (1) What was committed? (2) What is done? (3) What is blocked?

**Scope adjustment, not deadline extension:** When a sprint is running late, the response is to move lower-priority stories to the next sprint — not to extend the sprint boundary. This preserves the calendar structure while protecting committed deliverables.

**Milestone review:** Seven milestones are tracked (see `docs/monitoring-metrics.md`). Any milestone that moves from `in_progress` to `at_risk` is escalated to the PM the same day. Milestones are not allowed to stay `at_risk` for more than one week without a recovery plan.

### 4.3 Delay Categories and Responses

| Delay Type | Detection Signal | Immediate Response |
|-----------|-----------------|-------------------|
| Task takes longer than estimated | SPI < 0.90 at mid-sprint | Rescope: move lowest-priority stories to next sprint |
| Dependency from another team member not ready | Blocker reported in stand-up | PM reassigns or pair-programs to unblock |
| External blocker (library bug, course environment issue) | Stand-up blocker item | PM documents workaround; DevOps investigates alternative |
| CI/CD pipeline failing | Red CI badge on PR | Assigned to DevOps (Hamdi) within 24 hours |

---

## 5. Cost Increases

### 5.1 Context

This project has no financial budget — costs are measured in person-hours. A "cost increase" means actual effort exceeds estimated effort, reducing the team's capacity for other tasks.

### 5.2 How It Happens

A task that was estimated at 3 hours turns out to require 8. This is common in projects working with inherited codebases — the existing code may be more complex than it appeared during estimation.

### 5.3 Response Strategy

**Early reporting:** Team members report effort variances when they reach 150 % of the estimate (not at 300 %). An early signal allows the PM to rescope rather than absorb the full overrun.

**Re-estimation at sprint start:** Estimates from the previous sprint are reviewed in the sprint planning session. Patterns of underestimation (e.g., backend tasks consistently taking 2× the estimate) are corrected prospectively.

**Effort reallocation:** If one team member is overloaded (load > 95 % on the Management Dashboard), the PM moves a task to another team member with available capacity.

**Contingency reserve:** The sprint plan deliberately holds 10–15 % of total story points as unassigned buffer. This buffer absorbs unexpected complexity without displacing committed deliverables.

### 5.4 Cost Management Table

| Scenario | Trigger | Action |
|----------|---------|--------|
| Actual hours 150–200 % of estimate | Team member reports | Re-estimate remaining work; adjust sprint scope |
| Actual hours > 200 % of estimate | Team member reports | PM escalates; task may be descoped to MVP only |
| CPI < 0.90 on Management Dashboard | PM review | Sprint retrospective focuses on estimation improvement |
| CPI < 0.80 | PM review | Scope reduction: defer one feature to a later sprint |

---

## 6. Scope Changes

### 6.1 Difference from Changing Requirements

Requirements change is driven externally (instructor, course brief). Scope changes are driven internally — a team member proposes additional work.

### 6.2 Response Strategy

**Change control process:**

```
Team member proposes a scope addition
              │
              ▼
PM receives the proposal (written, not verbal)
              │
              ▼
PM evaluates: maps to course requirement? fits in current sprint? no rework?
              │
         ┌────┴────┐
         │ Yes     │ No
         ▼         ▼
   Add to sprint  Add to backlog for Sprint N+1
   with explicit   or reject with documented reason
   story points
```

**Backlog management:** Proposals that are not accepted for the current sprint go into the product backlog. At the start of each sprint, the backlog is reviewed — some items are promoted, others are retired.

**Scope freeze:** From Week 13, the backlog is locked. No new items are considered for implementation.

### 6.3 Scope Freeze — Why It Works

The instinct near a deadline is to add "one more thing." The problem is that each addition requires testing, documentation, and integration — all of which take time that is no longer available. A hard scope freeze removes the decision from the team and makes "no" the default. This is not inflexibility — it is protection of what has already been built.

---

## 7. Technical Unknowns

### 7.1 What They Are

Technical unknowns are components of the codebase that are not fully understood at the time of estimation. In an adaptation project, this is especially common — the team may not know how the existing authentication system works until they try to modify it.

### 7.2 Response Strategy

**Time-boxed investigation:** When a technical unknown is discovered, the team member is given a fixed time (typically 2 hours) to investigate and produce a finding. The finding is: (a) "I understand it now, here is the estimate"; (b) "I need help, can someone pair with me"; or (c) "This is more complex than expected, here is a reduced scope alternative."

**Spike tasks:** For high-risk unknowns (e.g., "will the existing PCAP analysis module conflict with our new health endpoint?"), a spike task is added to the sprint. A spike is a time-boxed research task whose output is knowledge, not working code.

**Documentation of discovered complexity:** When a technical unknown is resolved, the finding is written into the sprint notes. This prevents the same unknown from consuming time again in a future sprint.

**Architecture review:** The `docs/software-design-analysis.md` document was created specifically to map the existing codebase before committing to any adaptation. This reduced the number of technical unknowns encountered during implementation.

### 7.3 Examples from This Project

| Unknown | How Resolved |
|---------|-------------|
| Does `SidebarMenu.vue` use `App.vue`'s `menuItems` array or build its own? | Code inspection in sprint 2 revealed it builds its own `menuSections` computed; documented in adaptation plan |
| Does `GET /health` require authentication? | Endpoint inspection confirmed it does not; test added to `test_health.py` |
| What does `getRiskOverview()` return? | API call traced to backend router; response shape documented |

---

## 8. Failed Tests

### 8.1 Response Strategy

A failing test is not a failure of the team — it is the CI/CD system working correctly. The response protocol is:

**Step 1 — Assign immediately:** The team member who introduced the breaking change is responsible for fixing it. If the cause is unclear, the QA engineer (Praise-God) investigates.

**Step 2 — Do not merge:** No PR is merged while a CI check is red. The red badge is visible on the PR page; the team is expected to check before requesting review.

**Step 3 — Fix, do not skip:** Tests are never disabled or marked `xfail` to make the pipeline green without fixing the underlying problem. Skipping a test removes the protection it provides.

**Step 4 — Root cause, not just fix:** If a test fails because the implementation changed (e.g., the health endpoint response shape changed from `"healthy"` to `"ok"`), the test is updated to reflect the new contract — but only after confirming the contract change was intentional.

**Step 5 — Document:** If a fix requires more than 30 minutes, the root cause and fix are recorded in the sprint log.

### 8.2 Test Failure Categories

| Category | Example | Response |
|----------|---------|---------|
| Regression | Previously passing test now fails after a code change | Revert or fix the code change |
| Contract mismatch | Test asserts old response shape after endpoint update | Update test to reflect new documented contract |
| Environment issue | Test fails only in CI due to missing env variable | Fix CI environment config |
| Flaky test | Test sometimes passes, sometimes fails with no code change | Investigate and fix timing/isolation issue; do not ignore |

---

## 9. Deployment Problems

### 9.1 Response Strategy

**Pre-deployment checklist:**
- All CI checks pass on the branch being deployed
- `make status` confirms all containers are stopped before a rebuild
- `.env` is present and contains the required variables

**Step-by-step deployment with validation:**
```bash
git checkout main && git pull
make stop
make prod
make status          # All services must show "Up (healthy)"
curl -k https://localhost/health  # Must return "ok"
```

**If deployment fails:**

```
make prod fails
    │
    ├──► Container build failure
    │         → Check: docker build error in make logs
    │         → Fix: missing dependency, broken Dockerfile
    │
    ├──► Database migration failure
    │         → Check: alembic error in backend logs (make logs)
    │         → Fix: revert migration OR run make reset-db (destructive)
    │
    ├──► Port conflict
    │         → Check: port 80 or 443 already bound
    │         → Fix: stop conflicting process; re-run make prod
    │
    └──► Backend unhealthy after start
              → Check: curl -k https://localhost/health
              → Fix: check backend logs; likely a config or migration issue
```

**Rollback:** Documented in `docs/ci-cd-testing.md §3.3`. Previous image or git tag restores the last known-good state.

### 9.2 Three-Level Monitoring After Deployment

After `make prod`, the team confirms stability at three levels:

| Level | Check | Tool |
|-------|-------|------|
| Container level | All containers healthy | `make status` / `docker ps` |
| Application level | `/health` returns `"ok"` | `curl -k https://localhost/health` |
| System level | CPU, memory, disk within normal range | `/monitoring` dashboard |

If all three levels confirm normal, the deployment is declared stable.

---

## 10. Unavailable Team Members

### 10.1 How It Happens

A team member may be unavailable due to illness, exam conflicts, or personal circumstances. In a 7-person student team over 16 weeks, at least one instance of significant unavailability is expected.

### 10.2 Response Strategy

**Backup role assignments:** Every critical role has a documented backup:

| Primary Role | Primary Member | Backup Member |
|-------------|---------------|--------------|
| Project Manager | Obada (2309115277) | Abdulaziz (2309116441) |
| Backend Developer | Mohanad (2309115898) | Obada (PM can review backend) |
| Frontend Developer | Zekeriya (2309115377) | Fares (UX → can implement simple Vue pages) |
| QA/Test Engineer | Praise-God (2309116418) | Mohanad (Backend can run tests) |
| DevOps Engineer | Hamdi (2309116178) | Mohanad (Backend can manage Docker) |
| Risk Manager | Abdulaziz (2309116441) | Obada (PM owns risk register) |
| UX/UI Designer | Fares (2309115179) | Zekeriya (Frontend can adapt design) |

**Documentation as a buffer:** All work is documented in `docs/`. If a team member is unavailable, their replacement can read the relevant document rather than starting from zero. The `docs/software-design-analysis.md` and `docs/ci-cd-testing.md` documents are written specifically to allow a team member to pick up another's work.

**Task redistribution:** When a team member is unavailable for more than two days, the PM redistributes their open sprint tasks. Tasks are divided among members with available capacity — not concentrated on one backup person.

**Scope adjustment:** If the unavailability is prolonged (> 5 business days), the PM descopes the lowest-priority stories for that sprint. The priority is to protect committed deliverables, not to maintain the original scope.

**Communication:** The unavailable team member notifies the PM as early as possible. Last-minute notice of unavailability (the day of a deadline) is treated as a risk event in the sprint retrospective.

---

## 11. Risk Register as the Uncertainty Management Tool

The risk register in `docs/risk-management.md` is the central tool for managing uncertainty proactively — before it becomes a problem.

### 11.1 How the Risk Register Reduces Uncertainty

| Register Column | How It Reduces Uncertainty |
|----------------|---------------------------|
| **Risk** | Names the uncertainty explicitly — you cannot manage what you have not named |
| **Category** | Groups risks so the PM can see if one category (e.g., Technical) is disproportionately risky |
| **Probability × Impact = Score** | Prioritises which uncertainties deserve attention first |
| **Owner** | Assigns responsibility — unowned risks are always forgotten |
| **Mitigation** | Defines what will be done to reduce probability BEFORE the risk occurs |
| **Contingency** | Defines what will be done AFTER the risk occurs — removes the need to improvise under pressure |
| **Monitoring Method** | Defines how the team knows the risk is materialising — converts uncertainty into a detectable signal |

### 11.2 Risk Monitoring Schedule

| Frequency | Activity | Output |
|-----------|---------|--------|
| Weekly (PM) | Review top 5 open risks in register | Update status: active/mitigated/closed |
| Each sprint start | Risk scoring review; new risks added if identified | Updated register |
| Each milestone | Full register review; closed risks retired | Milestone risk summary |
| Sprint retrospective | Discuss risks that materialised; update contingency plans | Retrospective notes |

### 11.3 When a Risk Materialises

A risk materialising is not a surprise if it was in the register with a mitigation plan. The response is:

```
Risk materialises (e.g., team member unavailable for sprint)
                │
                ▼
Owner activates contingency plan from register
  (e.g., Backup role assignment; scope reduction)
                │
                ▼
PM updates risk status to "active — contingency applied"
                │
                ▼
Risk discussed at next stand-up; team confirms stability
                │
                ▼
If resolved: risk status updated to "mitigated" or "closed"
```

---

## 12. Summary — Uncertainty Response Matrix

| Scenario | Detection | Response | Tool |
|----------|-----------|---------|------|
| Changing requirements | Team member proposes change | Change control process; PM approval required | Sprint backlog |
| Delays | SPI < 0.90 | Rescope sprint; protect committed stories | Management Dashboard |
| Cost overrun | Effort > 150 % of estimate | Re-estimate; redistribute tasks | Weekly report |
| Scope addition | Proposal received | Change control process; defer if sprint full | Backlog |
| Technical unknown | Investigation shows complexity | Time-box spike; report finding; adjust estimate | Sprint notes |
| Failed test | CI badge red | Investigate root cause; fix, do not skip | CI pipeline |
| Deployment problem | `make status` unhealthy | Follow deployment runbook; rollback if needed | Makefile + health endpoint |
| Unavailable member | Member reports absence | Activate backup role; redistribute tasks; adjust scope | Backup role table |

The common thread across all scenarios is **early detection + pre-defined response**. The tools — risk register, CI/CD, Management Dashboard, backup assignments — exist so that the team does not need to invent a response in the moment. The uncertainty is managed by the process, not by heroics.
