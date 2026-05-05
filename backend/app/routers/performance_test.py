"""
Endpoint per testare le performance delle query ottimizzate
"""
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.auth import get_current_user
from app.services.dashboard_cache import get_dashboard_stats_cached, dashboard_cache

router = APIRouter(
    prefix="/performance",
    tags=["performance"],
)


@router.get("/dashboard-stats-benchmark")
def benchmark_dashboard_stats(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Test delle performance delle statistiche dashboard"""
    
    # Test 1: Query senza cache (cold start)
    start_time = time.time()
    stats_cold = get_dashboard_stats_cached(str(current_user.tenant_id), db)
    cold_time = time.time() - start_time
    
    # Test 2: Query con cache (warm)
    start_time = time.time()
    stats_warm = get_dashboard_stats_cached(str(current_user.tenant_id), db)
    warm_time = time.time() - start_time
    
    # Test 3: Cache hit diretto
    start_time = time.time()
    cached_stats = dashboard_cache.get_cached_stats(str(current_user.tenant_id))
    cache_hit_time = time.time() - start_time
    
    return {
        "tenant_id": str(current_user.tenant_id),
        "results": {
            "cold_start_time_ms": round(cold_time * 1000, 2),
            "warm_query_time_ms": round(warm_time * 1000, 2),
            "cache_hit_time_ms": round(cache_hit_time * 1000, 2),
            "performance_improvement": f"{round((cold_time - warm_time) / cold_time * 100, 1)}%",
            "cache_effectiveness": f"{round((cold_time - cache_hit_time) / cold_time * 100, 1)}%"
        },
        "stats_summary": {
            "total_assets": stats_cold.get("total_assets", 0),
            "critical_assets": stats_cold.get("critical_assets", 0),
            "assets_at_risk": stats_cold.get("assets_at_risk", 0),
            "status_count": len(stats_cold.get("status_stats", [])),
            "type_count": len(stats_cold.get("type_stats", []))
        }
    }


@router.get("/cache-status")
def get_cache_status(
    current_user: User = Depends(get_current_user)
):
    """Stato della cache per il tenant corrente"""
    cache_key = f"dashboard_stats_{current_user.tenant_id}"
    cache_entry = dashboard_cache._cache.get(cache_key)
    
    if cache_entry:
        cached_at = cache_entry.get('cached_at')
        if isinstance(cached_at, str):
            from datetime import datetime
            cached_at = datetime.fromisoformat(cached_at.replace('Z', '+00:00'))
        
        return {
            "tenant_id": str(current_user.tenant_id),
            "cache_status": "valid" if dashboard_cache._is_cache_valid(cache_entry) else "expired",
            "cached_at": cache_entry.get('cached_at'),
            "ttl_seconds": dashboard_cache._cache_ttl,
            "cache_size": len(dashboard_cache._cache)
        }
    else:
        return {
            "tenant_id": str(current_user.tenant_id),
            "cache_status": "empty",
            "cache_size": len(dashboard_cache._cache)
        }


@router.post("/clear-cache")
def clear_cache(
    current_user: User = Depends(get_current_user)
):
    """Pulisce la cache per il tenant corrente"""
    dashboard_cache.invalidate_cache(str(current_user.tenant_id))
    return {
        "message": "Cache cleared for tenant",
        "tenant_id": str(current_user.tenant_id)
    }

