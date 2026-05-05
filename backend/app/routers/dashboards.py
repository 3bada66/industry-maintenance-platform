import math
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Asset, AssetStatus
from app.services.audit_decorator import audit_log_action
from app.services.auth import get_current_user
from app.services.audit_log import create_audit_log

def clean_float_values(data):
    """Clean float values to prevent JSON serialization errors"""
    if isinstance(data, dict):
        return {k: clean_float_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_float_values(item) for item in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
        return data
    else:
        return data

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


# Dashboard endpoints
@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Ottimizzato con caching e query unificate"""
    from app.services.dashboard_cache import get_dashboard_stats_cached
    
    # Usa il servizio di cache per le statistiche
    return get_dashboard_stats_cached(str(current_user.tenant_id), db)


@router.get("/risky-assets")
def get_risky_assets(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    limit: int = 10
):
    """
    Ottieni gli asset più a rischio
    PERFORMANCE: Usa selectinload per evitare N+1 queries
    """
    from sqlalchemy import and_
    from sqlalchemy.orm import selectinload
    
    from app.models import AssetType, Site, Manufacturer
    
    # PERFORMANCE: Limita il numero massimo di risultati
    limit = min(limit, 50)
    
    risky_assets = (
        db.query(Asset)
        .options(
            selectinload(Asset.interfaces),  # Query separate ottimizzata
            selectinload(Asset.asset_type),
            selectinload(Asset.site),
            selectinload(Asset.status),
            selectinload(Asset.manufacturer)
        )
        .filter(
            and_(
                Asset.tenant_id == current_user.tenant_id,
                Asset.deleted_at == None,  # Non mostrare asset eliminati
                Asset.risk_score >= 5
            )
        )
        .order_by(Asset.risk_score.desc())
        .limit(limit)
        .all()
    )
    
    return [
        {
            "id": str(asset.id),
            "name": asset.name,
            "risk_score": clean_float_values(asset.risk_score),
            "business_criticality": asset.business_criticality,
            "asset_type_name": asset.asset_type.name if asset.asset_type else "N/A",
            "status_name": asset.status.name if asset.status else "N/A",
            "site_name": asset.site.name if asset.site else "N/A",
            "manufacturer_name": asset.manufacturer.name if asset.manufacturer else "N/A",
            "ip_address": asset.interfaces[0].ip_address if asset.interfaces else None,
            "created_at": asset.created_at.isoformat() if asset.created_at else None,
            "updated_at": asset.updated_at.isoformat() if asset.updated_at else None
        }
        for asset in risky_assets
    ]
