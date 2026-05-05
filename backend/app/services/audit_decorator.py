# backend/services/audit_decorator.py
from functools import wraps
from typing import Optional
from fastapi import Request
from app.services.audit_log import (
    create_audit_log,
    clean_dict,
    create_readable_description,
    get_entity_name_by_id,
)


def get_client_ip(request: Request) -> Optional[str]:
    if not request:
        return None
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


def audit_log_action(action: str, entity: str, model_class=None):
    """
    Decorator per aggiungere audit logging agli endpoint.

    L'endpoint deve avere parametri: db, current_user, request, e opzionalmente entity_id (es. asset_id)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db = kwargs.get("db")
            current_user = kwargs.get("current_user")
            request: Request = kwargs.get("request")

            # Prendi IP
            ip_address = get_client_ip(request)

            # Search for entity id from kwargs, e.g. asset_id, entity_id or id
            entity_id = (
                kwargs.get(f"{entity.lower()}_id")
                or kwargs.get("entity_id")
                or kwargs.get("id")
            )

            old_data = None
            if action in ("update", "delete") and entity_id and db and model_class:
                obj = db.query(model_class).filter(model_class.id == entity_id).first()
                if obj:
                    old_data = clean_dict(obj.__dict__)

            # Esegui la funzione
            result = func(*args, **kwargs)

            # Recupera dati nuovi da result, se action create o update
            new_data = None
            if action in ("create", "update") and result:
                # Gestisci oggetti SQLAlchemy
                if hasattr(result, '_sa_instance_state'):
                    # Per oggetti SQLAlchemy, usa clean_dict direttamente
                    new_data = clean_dict(result)
                elif hasattr(result, "__dict__"):
                    new_data = clean_dict(result.__dict__)
                elif isinstance(result, dict):
                    new_data = clean_dict(result)
                else:
                    # Prova a convertire in dict se possibile
                    try:
                        if hasattr(result, 'model_dump'):
                            new_data = clean_dict(result.model_dump())
                        elif hasattr(result, 'dict'):
                            new_data = clean_dict(result.dict())
                        else:
                            new_data = clean_dict(str(result))
                    except Exception as e:
                        new_data = clean_dict(str(result))

            # Usa id da result se entity_id non era definito
            if not entity_id and result and hasattr(result, "id"):
                entity_id = result.id

            # Get entity name for description
            entity_name = None
            if entity_id and db and current_user:
                entity_name = get_entity_name_by_id(
                    db, entity, entity_id, current_user.tenant_id
                )

            # Crea descrizione leggibile
            description = create_readable_description(
                action, entity, entity_id, entity_name, old_data, new_data
            )

            # Crea log audit con traduzione automatica
            if db and current_user:
                create_audit_log(
                    db=db,
                    user_id=current_user.id,
                    tenant_id=current_user.tenant_id,
                    action=action,
                    entity=entity,
                    entity_id=entity_id,
                    old_data=old_data,
                    new_data=new_data,
                    description=description,
                    ip_address=ip_address,
                    commit=True,
                )
            return result

        return wrapper

    return decorator
