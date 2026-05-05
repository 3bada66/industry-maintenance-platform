# backend/services/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from typing import Optional
from app.config import settings
import time

# Inizializza il rate limiter
limiter = Limiter(key_func=get_remote_address)


def get_rate_limit_for_api_key(api_key) -> str:
    """Determina il rate limit per un'API Key specifica"""
    if api_key and hasattr(api_key, "rate_limit"):
        return api_key.rate_limit
    return settings.RATE_LIMIT_DEFAULT


def rate_limit_by_api_key(api_key=None):
    """
    Decorator per applicare rate limiting basato sull'API Key.
    Se non c'è API Key, usa il limite di default.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Determina il rate limit
            rate_limit = get_rate_limit_for_api_key(api_key)

            # Applica il rate limiting
            return limiter.limit(rate_limit)(func)(*args, **kwargs)

        return wrapper

    return decorator


def get_client_identifier(request: Request, api_key=None) -> str:
    """
    Genera un identificatore unico per il client.
    Se c'è un'API Key, usa quella, altrimenti usa l'IP.
    """
    if api_key:
        return f"api_key:{api_key.id}"
    return f"ip:{get_remote_address(request)}"


def check_rate_limit(request: Request, api_key=None) -> bool:
    """
    Verifica se il client ha superato il rate limit.
    Restituisce True se il limite non è stato superato.
    """
    identifier = get_client_identifier(request, api_key)
    rate_limit = get_rate_limit_for_api_key(api_key)

    # Implementazione semplificata del rate limiting
    # In produzione, usa Redis o un database per il tracking
    return True  # Per ora, sempre permesso


def get_remaining_requests(request: Request, api_key=None) -> dict:
    """
    Restituisce informazioni sui limiti di rate rimanenti.
    """
    identifier = get_client_identifier(request, api_key)
    rate_limit = get_rate_limit_for_api_key(api_key)

    # Parsing del rate limit (es: "100/hour", "10/minute")
    try:
        limit_str, period = rate_limit.split("/")
        limit = int(limit_str)

        # Calcolo semplificato - in produzione usa Redis
        return {
            "limit": limit,
            "period": period,
            "remaining": limit,  # Semplificato
            "reset_time": int(time.time()) + 3600,  # Semplificato
        }
    except:
        return {
            "limit": 100,
            "period": "hour",
            "remaining": 100,
            "reset_time": int(time.time()) + 3600,
        }


def add_rate_limit_headers(response: Response, request: Request, api_key=None):
    """Aggiunge headers di rate limiting alla risposta"""
    info = get_remaining_requests(request, api_key)

    response.headers["X-RateLimit-Limit"] = str(info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
    response.headers["X-RateLimit-Reset"] = str(info["reset_time"])

    return response
