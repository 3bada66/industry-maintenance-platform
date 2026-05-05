# Risk Management Plan
## Industry Maintenance Platform — Industrial Asset, Risk, Management & Technical Monitoring Platform

**Course:** Software Project Management & Technical Monitoring  
**Version:** 1.0  
**Risk Owner:** Abdulaziz Alyahya (Risk Manager, 2309116441) with input from all team members

---

## 1. Risk Management Approach

### 1.1 Process
Risk management follows a four-step cycle applied throughout all 16 project weeks:

```
  IDENTIFY          ASSESS           MITIGATE          MONITOR
     │                 │                 │                 │
 What could       How likely?       What do we        Is it
 go wrong?        How bad?          do about it?      happening?
     │                 │                 │                 │
 Risk Register ──► Impact/Prob ──► Response Plan ──► Weekly Review
```

### 1.2 Risk Categories
| ID Prefix | Category |
|-----------|---------|
| T | Technical risks |
| M | Management risks |
| E | External/Environment risks |
| Q | Quality risks |
| S | Security risks |

### 1.3 Scoring Scale
| Score | Probability | Impact |
|-------|------------|--------|
| 1 | Very Low (< 10%) | Negligible |
| 2 | Low (10–25%) | Minor delay or rework |
| 3 | Medium (25–50%) | Moderate impact on schedule/quality |
| 4 | High (50–75%) | Major impact; milestone at risk |
| 5 | Very High (> 75%) | Project failure or critical quality failure |

**Risk Score = Probability × Impact**  
- 1–4: Low — monitor  
- 5–9: Medium — mitigate  
- 10–16: High — immediate action  
- 17–25: Critical — escalate immediately

---

## 2. Risk Register

### T1 — Database Migration Failure
| Field | Detail |
|-------|--------|
| **Description** | An Alembic migration fails in production, corrupting the schema or causing service outage |
| **Probability** | 2 (Low) |
| **Impact** | 5 (Critical) |
| **Risk Score** | 10 — High |
| **Owner** | Mohanad Aref Ali Sultan |
| **Response Type** | Mitigate + Contingency |
| **Mitigation** | All migrations tested on dev DB first; DB backup taken before every production migration; rollback script prepared |
| **Contingency** | Restore from backup (< 1 hour RTO); document incident; re-apply fixed migration |
| **Monitoring** | Check `alembic current` in CI after every merge to main |
| **Status** | Active monitoring |

---

### T2 — Docker Dependency Failure
| Field | Detail |
|-------|--------|
| **Description** | A Docker image version breaks compatibility (e.g., PostgreSQL 16 deprecations, Python base image changes) |
| **Probability** | 2 (Low) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 6 — Medium |
| **Owner** | Hamdi Alnaqeeb |
| **Response Type** | Mitigate |
| **Mitigation** | All Docker images use pinned version tags (e.g., `postgres:15`, not `postgres:latest`); `docker-compose.yml` versioned in git |
| **Contingency** | Roll back to previous pinned version; rebuild containers |
| **Monitoring** | Review pinned versions at start of each sprint |
| **Status** | Active monitoring |

---

### T3 — Frontend Build Failures in CI
| Field | Detail |
|-------|--------|
| **Description** | Vue.js or dependency update breaks the production build, blocking deployment |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 — Medium |
| **Owner** | Zekeriya Dulli |
| **Response Type** | Mitigate |
| **Mitigation** | `package-lock.json` committed; `npm ci` (not `npm install`) used in CI; Node.js version pinned to 18 in `.nvmrc`; build job in CI catches failures before merge |
| **Contingency** | Revert frontend PR; fix in hotfix branch |
| **Monitoring** | CI `frontend.yml` runs on every push; status badge in README |
| **Status** | Resolved — CI pipeline in place |

---

### T4 — Performance Degradation Under Load
| Field | Detail |
|-------|--------|
| **Description** | API response times exceed targets when multiple users query dashboards simultaneously |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 — Medium |
| **Owner** | Mohanad Aref Ali Sultan + Praise-God Tobby |
| **Response Type** | Mitigate |
| **Mitigation** | Redis caching layer on dashboard endpoints; PostgreSQL indexes on frequently queried columns (`add_performance_indexes.py` migration); rate limiting enabled (100 req/hour) |
| **Contingency** | Add `LIMIT` clauses; disable expensive endpoints temporarily |
| **Monitoring** | P95 response time tracked in `/health/detailed`; alert if > 500ms |
| **Status** | Mitigated — caching and indexes implemented |

---

### T5 — Security Vulnerability in Dependencies
| Field | Detail |
|-------|--------|
| **Description** | A known CVE is published for FastAPI, PyJWT, or a frontend dependency affecting system security |
| **Probability** | 3 (Medium) |
| **Impact** | 4 (High) |
| **Risk Score** | 12 — High |
| **Owner** | Mohanad Aref Ali Sultan |
| **Response Type** | Mitigate + Monitor |
| **Mitigation** | Dependency versions pinned in `requirements.txt` and `package-lock.json`; GitHub Dependabot enabled; OWASP checklist applied at code freeze |
| **Contingency** | Patch and redeploy within 24 hours for P1 CVEs; document in security log |
| **Monitoring** | GitHub Dependabot alerts; weekly `pip-audit` and `npm audit` in Sprint 3–4 |
| **Status** | Monitoring active |

---

### M1 — Team Member Unavailability
| Field | Detail |
|-------|--------|
| **Description** | A team member becomes unavailable for ≥ 1 week due to illness, exams, or other commitments |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 — Medium |
| **Owner** | Obada Abdulhakim Kharaz |
| **Response Type** | Accept + Mitigate |
| **Mitigation** | All code is reviewed by at least one other member (no single-person knowledge silos); tasks have at least one backup person identified in RACI matrix; 2-week schedule buffer in weeks 14–15 |
| **Contingency** | Redistribute tasks; defer lower-priority features; use buffer weeks |
| **Monitoring** | Weekly stand-up — anyone can flag capacity issues |
| **Status** | Buffer built in; RACI documented |

---

### M2 — Scope Creep
| Field | Detail |
|-------|--------|
| **Description** | Team adds features beyond the defined scope, causing schedule overrun |
| **Probability** | 4 (High) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 12 — High |
| **Owner** | Obada Abdulhakim Kharaz |
| **Response Type** | Mitigate |
| **Mitigation** | Strict change control process (see Project Management Plan §8); all new features require PM approval; code freeze enforced from Week 11 |
| **Contingency** | De-scope to backlog; label as "planned (future)" in documentation |
| **Monitoring** | Sprint review checks committed vs completed story points |
| **Status** | Active — code freeze applied Week 11 |

---

### M3 — Documentation Lag
| Field | Detail |
|-------|--------|
| **Description** | Documentation is left until the last week, resulting in incomplete or inaccurate reports |
| **Probability** | 4 (High) |
| **Impact** | 2 (Minor) |
| **Risk Score** | 8 — Medium |
| **Owner** | Abdulaziz Alyahya |
| **Response Type** | Mitigate |
| **Mitigation** | Documentation written incrementally — each sprint milestone includes a documentation task; Abdulaziz maintains living documents updated weekly |
| **Contingency** | Schedule documentation review session in Week 14 |
| **Monitoring** | Doc completeness checklist reviewed each sprint |
| **Status** | Actively managed |

---

### E1 — Tool/Service Unavailability
| Field | Detail |
|-------|--------|
| **Description** | GitHub, Docker Hub, or PyPI becomes temporarily unavailable, blocking CI/CD |
| **Probability** | 2 (Low) |
| **Impact** | 2 (Minor) |
| **Risk Score** | 4 — Low |
| **Owner** | Hamdi Alnaqeeb |
| **Response Type** | Accept |
| **Mitigation** | Docker images cached locally; pip packages cached in CI; local dev environment fully functional without external services |
| **Contingency** | Wait for service restoration; continue local development |
| **Monitoring** | GitHub status page awareness |
| **Status** | Accepted — low probability |

---

### Q1 — Insufficient Test Coverage
| Field | Detail |
|-------|--------|
| **Description** | Code coverage falls below targets (70% backend, 60% frontend), allowing regressions to ship |
| **Probability** | 3 (Medium) |
| **Impact** | 3 (Moderate) |
| **Risk Score** | 9 — Medium |
| **Owner** | Praise-God Tobby |
| **Response Type** | Mitigate |
| **Mitigation** | Coverage thresholds enforced in `pytest.ini` and CI; coverage reports generated in every CI run; test tasks assigned story points in every sprint |
| **Contingency** | Sprint 4 dedicated to closing coverage gaps |
| **Monitoring** | pytest-cov report in every CI run; coverage badge in README |
| **Status** | Target met — see Test Report |

---

### S1 — Data Exposure via API
| Field | Detail |
|-------|--------|
| **Description** | An API endpoint inadvertently exposes sensitive asset data or user credentials |
| **Probability** | 2 (Low) |
| **Impact** | 5 (Critical) |
| **Risk Score** | 10 — High |
| **Owner** | Mohanad Aref Ali Sultan |
| **Response Type** | Mitigate |
| **Mitigation** | All endpoints require JWT authentication; Pydantic schemas control which fields are returned (no `SELECT *`); RBAC enforced via dependency injection; HTML sanitized with bleach; multi-tenant data isolation tested |
| **Contingency** | Revoke API keys; force re-login; patch endpoint; notify affected tenant admin |
| **Monitoring** | Security review at code freeze (Week 13); automated linting for common patterns |
| **Status** | Mitigated — OWASP checklist completed |

---

## 3. Risk Matrix (Summary)

```
    Impact →    1-Negligible  2-Minor   3-Moderate  4-Major   5-Critical
Probability ↓
5-Very High  |     5            10         15          20         25
4-High       |     4             8         12          16         20
3-Medium     |     3             6          9          12         15
2-Low        |     2             4          6           8         10
1-Very Low   |     1             2          3           4          5

Current Risks:
🔴 HIGH (10+):   T1(DB Migration), T5(Security CVE), M2(Scope Creep), S1(Data Exposure)
🟡 MEDIUM (5-9): T2(Docker), T3(Build), T4(Performance), M1(Unavailability), M3(Docs), Q1(Coverage)
🟢 LOW (1-4):    E1(Tool Unavailability)
```

---

## 4. Risk Monitoring Schedule

| Activity | Frequency | Owner |
|----------|-----------|-------|
| Risk Register review | Weekly (Monday stand-up) | Obada |
| CI pipeline status | Every push (automated) | Hamdi |
| Security dependency scan | Every sprint start | Mohanad |
| Test coverage review | Every sprint end | Praise-God |
| DB migration check | Every deployment | Mohanad |
| Scope review | Every sprint planning | Obada |

---

## 5. Risk Closure Criteria

A risk is marked **Closed** when:
- The triggering condition is permanently eliminated (e.g., code freeze closes M2)
- The sprint affected by the risk has ended without the risk materializing
- A permanent mitigation has been implemented and verified

**Residual Risk Acceptance:** The team accepts that any risk with score ≤ 4 is monitored but no further mitigation is applied.

---

## 6. Risks to Product (Runtime)

Beyond project risks, the *deployed platform* faces operational risks documented here for completeness:

| Risk | Mitigation Built Into System |
|------|------------------------------|
| Unauthorized access | JWT auth + RBAC + API rate limiting |
| Data loss | PostgreSQL ACID transactions; backup scripts included |
| Industrial asset data manipulation | Immutable audit trail in `audit_logs` table |
| Denial of service | Rate limiting (slowapi: 100 req/hr, 10/min strict) |
| SQL injection | Parameterized queries via SQLAlchemy ORM |
| XSS | Input sanitization via bleach; Content-Security-Policy headers |
| SSRF/Command injection | No user-controlled external calls; Pydantic strict validation |
