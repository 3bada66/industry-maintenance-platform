# backend/services/create_tenant.py
import uuid
from sqlalchemy.orm import Session
from database import SessionLocal  # o come importi la sessione DB
import crud, schemas


def main():
    db: Session = SessionLocal()

    # Dati di esempio, da personalizzare
    tenant_data = schemas.TenantCreate(name="Nuovo Tenant", slug="nuovo-tenant")

    tenant = crud.create_tenant(db, tenant_data)
    # print(f"Tenant creato con ID: {tenant.id} e slug: {tenant.slug}")

    db.close()


if __name__ == "__main__":
    main()
