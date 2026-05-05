import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role, Tenant


def update_roles_tenant():
    db: Session = SessionLocal()
    
    # Ottieni il primo tenant (default)
    default_tenant = db.query(Tenant).first()
    if not default_tenant:
        # print("No tenant found! Please create a tenant first.")
        return
    
            # print(f"Using default tenant: {default_tenant.name} (ID: {default_tenant.id})")
    
    # Aggiorna tutti i ruoli esistenti
    roles = db.query(Role).all()
    
    for role in roles:
        if role.tenant_id is None:
            role.tenant_id = default_tenant.id
            # print(f"Updated role {role.name} with tenant_id: {default_tenant.id}")
    
    db.commit()
    db.close()
    # print("Roles tenant_id updated successfully!")


if __name__ == "__main__":
    update_roles_tenant() 