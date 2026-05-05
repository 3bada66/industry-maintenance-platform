"""
Servizio di caching per le statistiche della dashboard
Ottimizza le performance riducendo le query al database
"""
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import User, Asset, AssetStatus, AssetType
from app.database import get_db


class DashboardCache:
    """Cache in-memory per le statistiche dashboard"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 300  # 5 minuti
    
    def _get_cache_key(self, tenant_id: str) -> str:
        """Genera una chiave di cache unica per il tenant"""
        return f"dashboard_stats_{tenant_id}"
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Verifica se la cache è ancora valida"""
        if not cache_entry:
            return False
        
        cached_at = cache_entry.get('cached_at')
        if not cached_at:
            return False
        
        # Converti stringa ISO in datetime se necessario
        if isinstance(cached_at, str):
            cached_at = datetime.fromisoformat(cached_at.replace('Z', '+00:00'))
        
        return datetime.utcnow() - cached_at < timedelta(seconds=self._cache_ttl)
    
    def get_cached_stats(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """Recupera le statistiche dalla cache se valide"""
        cache_key = self._get_cache_key(tenant_id)
        cache_entry = self._cache.get(cache_key)
        
        if self._is_cache_valid(cache_entry):
            return cache_entry.get('data')
        
        # Cache scaduta o inesistente
        if cache_key in self._cache:
            del self._cache[cache_key]
        
        return None
    
    def set_cached_stats(self, tenant_id: str, stats: Dict[str, Any]) -> None:
        """Salva le statistiche nella cache"""
        cache_key = self._get_cache_key(tenant_id)
        self._cache[cache_key] = {
            'data': stats,
            'cached_at': datetime.utcnow().isoformat()
        }
    
    def invalidate_cache(self, tenant_id: str) -> None:
        """Invalida la cache per un tenant specifico"""
        cache_key = self._get_cache_key(tenant_id)
        if cache_key in self._cache:
            del self._cache[cache_key]
    
    def clear_all_cache(self) -> None:
        """Pulisce tutta la cache"""
        self._cache.clear()


# Istanza globale del cache
dashboard_cache = DashboardCache()


def get_dashboard_stats_cached(tenant_id: str, db: Session) -> Dict[str, Any]:
    """
    Recupera le statistiche dashboard con caching
    Se la cache è valida, restituisce i dati cached
    Altrimenti esegue la query e aggiorna la cache
    """
    # Prova a recuperare dalla cache
    cached_stats = dashboard_cache.get_cached_stats(tenant_id)
    if cached_stats:
        return cached_stats
    
    # Cache miss - esegui la query ottimizzata
    from datetime import datetime, timedelta
    from sqlalchemy import func, and_, case
    
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    # Query unificata per tutte le statistiche base
    base_stats = db.query(
        func.count(Asset.id).label('total_assets'),
        func.count(case(
            (Asset.business_criticality.in_(['critical', 'high']), Asset.id)
        )).label('critical_assets'),
        func.count(case(
            (Asset.risk_score >= 5, Asset.id)
        )).label('assets_at_risk'),
        func.count(case(
            (Asset.updated_at >= yesterday, Asset.id)
        )).label('recent_changes'),
        func.count(case(
            (AssetStatus.name == "Active", Asset.id)
        )).label('active_assets')
    ).select_from(Asset).outerjoin(AssetStatus, Asset.status_id == AssetStatus.id)\
     .filter(
        and_(
            Asset.tenant_id == tenant_id,
            Asset.deleted_at == None
        )
     ).first()
    
    # Query unificata per statistiche per status
    status_stats = db.query(
        AssetStatus.id,
        AssetStatus.name,
        AssetStatus.color,
        func.count(Asset.id).label('count')
    ).outerjoin(Asset, and_(
        Asset.status_id == AssetStatus.id,
        Asset.tenant_id == tenant_id,
        Asset.deleted_at == None
    )).filter(AssetStatus.tenant_id == tenant_id)\
     .group_by(AssetStatus.id, AssetStatus.name, AssetStatus.color)\
     .all()
    
    # Query unificata per statistiche per tipo
    type_stats = db.query(
        AssetType.id,
        AssetType.name,
        func.count(Asset.id).label('asset_count')
    ).outerjoin(Asset, and_(
        Asset.asset_type_id == AssetType.id,
        Asset.tenant_id == tenant_id,
        Asset.deleted_at == None
    )).filter(AssetType.tenant_id == tenant_id)\
     .group_by(AssetType.id, AssetType.name)\
     .all()
    
    stats = {
        "total_assets": base_stats.total_assets or 0,
        "critical_assets": base_stats.critical_assets or 0,
        "assets_at_risk": base_stats.assets_at_risk or 0,
        "recent_changes": base_stats.recent_changes or 0,
        "active_assets": base_stats.active_assets or 0,
        "inactive_assets": (base_stats.total_assets or 0) - (base_stats.active_assets or 0),
        "status_stats": [
            {
                "status_id": str(status.id),
                "name": status.name,
                "color": status.color,
                "count": status.count or 0,
            }
            for status in status_stats
        ],
        "type_stats": [
            {
                "type_id": str(asset_type.id),
                "name": asset_type.name,
                "asset_count": asset_type.asset_count or 0,
            }
            for asset_type in type_stats
        ]
    }
    
    # Salva nella cache
    dashboard_cache.set_cached_stats(tenant_id, stats)
    
    return stats


def invalidate_dashboard_cache(tenant_id: str) -> None:
    """Invalida la cache dashboard per un tenant"""
    dashboard_cache.invalidate_cache(tenant_id)

