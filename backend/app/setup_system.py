import uuid
from app.database import SessionLocal
from app.models import Tenant, User, Role
from app.services.auth import get_password_hash
from app.init_roles import seed_roles
from app.init_print_template import init_default_templates
from app.init_manufacturers import seed_manufacturers
from app.init_asset_statuses import setup_asset_statuses
from app.init_asset_types import setup_asset_types

ADMIN_EMAIL = "admin@example.com"
EDITOR_EMAIL = "editor@example.com"
VIEWER_EMAIL = "viewer@example.com"
ADMIN_PASSWORD = "admin123"
EDITOR_PASSWORD = "editor123"
VIEWER_PASSWORD = "viewer123"
TENANT_NAME = "Default Tenant"
TENANT_SLUG = "default-tenant"


def setup_system():
    db = SessionLocal()
    # 1. Tenant
    tenant = db.query(Tenant).filter_by(slug=TENANT_SLUG).first()
    if not tenant:
        tenant = Tenant(
            id=uuid.uuid4(), name=TENANT_NAME, slug=TENANT_SLUG, settings={}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        # print(f"Tenant created: {TENANT_NAME}")
    else:
        # print(f"Tenant already exists: {TENANT_NAME}")
        pass
    tenant_id = tenant.id

    # 2. Roles
    seed_roles(tenant_id=tenant_id)
    roles = {r.name: r for r in db.query(Role).filter_by(tenant_id=tenant_id).all()}

    # 3. Base users
    users = [
        {
            "name": "Admin",
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "role": "admin",
        },
        {
            "name": "Editor",
            "email": EDITOR_EMAIL,
            "password": EDITOR_PASSWORD,
            "role": "editor",
        },
        {
            "name": "Viewer",
            "email": VIEWER_EMAIL,
            "password": VIEWER_PASSWORD,
            "role": "viewer",
        },
    ]
    for u in users:
        existing = db.query(User).filter_by(email=u["email"]).first()
        if not existing:
            user = User(
                id=uuid.uuid4(),
                tenant_id=tenant_id,
                email=u["email"],
                password_hash=get_password_hash(u["password"]),
                name=u["name"],
                role_id=roles[u["role"]].id,
                is_active=True,
            )
            db.add(user)
            # print(f"User created: {u['email']} ({u['role']})")
        else:
            # print(f"User already exists: {u['email']}")
            pass
    db.commit()

    # 4. Print templates
    init_default_templates(tenant_id=tenant_id)

    # 5. Manufacturers ICS/OT
    seed_manufacturers(tenant_id=tenant_id)

    # 6. Asset types and statuses
    setup_asset_statuses(tenant_id=tenant_id)
    setup_asset_types(tenant_id=tenant_id)

    # Add demo data if in development environment
    from app.config import settings
    if settings.ENVIRONMENT == "development":
        try:
            from app.init_demo_data import seed_demo_data
            print("🌱 Adding demo data for development environment...")
            seed_demo_data()
        except Exception as e:
            print(f"⚠️  Demo data seeding failed: {e}")
            import traceback
            traceback.print_exc()

    db.close()
    # print("\nSetup system completed!\nExample credentials:")
    # print(f"Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    # print(f"Editor: {EDITOR_EMAIL} / {EDITOR_PASSWORD}")
    # print(f"Viewer: {VIEWER_EMAIL} / {VIEWER_PASSWORD}")


if __name__ == "__main__":
    setup_system()
