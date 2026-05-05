"""
Management Monitoring Router
Exposes project management metrics for the Management Monitoring Dashboard.

Owner: Obada Abdulhakim Kharaz (Project Manager, 2309115277)
Supporting: Mohanad Aref Ali Sultan (Backend Developer, 2309115898)
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Asset
from app.services.auth import get_current_user
from app.models import User

router = APIRouter(
    prefix="/api/v1/management",
    tags=["management-monitoring"],
)


@router.get("/status")
def get_management_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return project management monitoring metrics.

    Combines static project-level data (sprints, milestones, EVM) with
    live database counts (assets currently managed) to give a complete
    management overview.
    """
    # Live data: total assets in this tenant's database
    try:
        assets_managed = db.query(func.count(Asset.id)).filter(
            Asset.tenant_id == current_user.tenant_id,
            Asset.deleted_at.is_(None),
        ).scalar() or 0
    except Exception:
        assets_managed = 0

    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),

        # --- Project overview ---
        "project": {
            "name": "Industry Maintenance Platform — Industrial Asset, Risk & Monitoring Platform",
            "course": "Software Project Management & Technical Monitoring",
            "current_sprint": 4,
            "total_sprints": 4,
            "current_phase": "Documentation & Submission",
            "week_current": 15,
            "week_total": 16,
            "assets_managed": assets_managed,
        },

        # --- Task breakdown ---
        "tasks": {
            "total": 32,
            "completed": 28,
            "pending": 3,
            "delayed": 1,
            "overdue": 0,
            "progress_percent": round(28 / 32 * 100, 1),
            # Estimated vs actual hours (story-point proxy: 1 SP ≈ 2 h)
            "estimated_hours": 302,
            "actual_hours": 289,
        },

        # --- Earned Value Management (story points as proxy currency) ---
        "schedule": {
            "planned_value_sp": 151,
            "earned_value_sp": 145,
            "spi": round(145 / 151, 2),         # Schedule Performance Index
            "variance_sp": 145 - 151,            # Negative = slightly behind
            "status": "on_track",                # on_track | at_risk | delayed
            "sprint_velocities": [45, 52, 54, 48],  # SP per sprint
        },

        # --- Cost tracking (open-source stack → €0 infra cost) ---
        "cost": {
            "estimated_eur": 0,
            "actual_eur": 0,
            "variance_eur": 0,
            "cpi": 1.0,                          # Cost Performance Index (N/A → 1.0)
            "currency": "EUR",
            "note": "All infrastructure tools are free and open-source (€0 cost).",
        },

        # --- Milestones ---
        "milestones": [
            {
                "id": "MS-1",
                "name": "Project Setup & Planning",
                "due_week": 2,
                "status": "completed",
                "deliverables": ["Git repo", "Project plan", "Team doc"],
            },
            {
                "id": "MS-2",
                "name": "Backend Foundation",
                "due_week": 5,
                "status": "completed",
                "deliverables": ["DB models", "Auth/RBAC", "Core API endpoints"],
            },
            {
                "id": "MS-3",
                "name": "Frontend & Dashboards",
                "due_week": 8,
                "status": "completed",
                "deliverables": ["Vue.js SPA", "Management dashboard", "Network map"],
            },
            {
                "id": "MS-4",
                "name": "Monitoring & Risk Features",
                "due_week": 11,
                "status": "completed",
                "deliverables": ["/health/detailed", "Technical monitoring dashboard", "Risk scoring"],
            },
            {
                "id": "MS-5",
                "name": "QA & Code Freeze",
                "due_week": 13,
                "status": "completed",
                "deliverables": ["70% backend coverage", "OWASP review", "Bug fixes"],
            },
            {
                "id": "MS-6",
                "name": "Documentation Package",
                "due_week": 14,
                "status": "in_progress",
                "deliverables": ["All 12 docs updated", "Monitoring metrics doc"],
            },
            {
                "id": "MS-7",
                "name": "Final Submission",
                "due_week": 16,
                "status": "pending",
                "deliverables": ["Submitted docs", "Recorded video", "Presentation"],
            },
        ],

        # --- Team workload (story points assigned vs completed) ---
        "team_workload": [
            {
                "name": "Obada Abdulhakim Kharaz",
                "role": "Project Manager",
                "student_id": "2309115277",
                "assigned_sp": 25,
                "completed_sp": 23,
                "load_percent": 92,
            },
            {
                "name": "Mohanad Aref Ali Sultan",
                "role": "Backend Developer",
                "student_id": "2309115898",
                "assigned_sp": 62,
                "completed_sp": 60,
                "load_percent": 97,
            },
            {
                "name": "Zekeriya Dulli",
                "role": "Frontend Developer",
                "student_id": "2309115377",
                "assigned_sp": 57,
                "completed_sp": 54,
                "load_percent": 95,
            },
            {
                "name": "Praise-God Tobby",
                "role": "QA/Test Engineer",
                "student_id": "2309116418",
                "assigned_sp": 23,
                "completed_sp": 21,
                "load_percent": 91,
            },
            {
                "name": "Fares Stouhi",
                "role": "UX/UI Designer",
                "student_id": "2309115179",
                "assigned_sp": 18,
                "completed_sp": 17,
                "load_percent": 94,
            },
            {
                "name": "Hamdi Alnaqeeb",
                "role": "DevOps/Operations Engineer",
                "student_id": "2309116178",
                "assigned_sp": 24,
                "completed_sp": 23,
                "load_percent": 96,
            },
            {
                "name": "Abdulaziz Alyahya",
                "role": "Risk Manager",
                "student_id": "2309116441",
                "assigned_sp": 20,
                "completed_sp": 19,
                "load_percent": 95,
            },
        ],

        # --- Risk summary (from risk register) ---
        "risks": {
            "total": 11,
            "by_severity": {"high": 4, "medium": 6, "low": 1},
            "by_status": {"active": 7, "mitigated": 3, "closed": 1},
            "top_open": [
                {"id": "T5", "name": "Security Vulnerability in Dependencies", "score": 12},
                {"id": "M2", "name": "Scope Creep", "score": 12},
                {"id": "T1", "name": "Database Migration Failure", "score": 10},
                {"id": "S1", "name": "Data Exposure via API", "score": 10},
            ],
        },
    }
