# backend/app/init_tenant.py

import uuid
from app.database import SessionLocal
from app.models import Tenant, User, Role
from app.services.auth import get_password_hash
from app.services.init_tenant_roles import init_tenant_roles, get_default_admin_role_id
from app.init_asset_types import setup_asset_types
from app.init_asset_statuses import setup_asset_statuses
from app.init_print_template import init_default_templates
from app.init_manufacturers import seed_manufacturers


def create_tenant_with_admin(
    tenant_name, tenant_slug, admin_email, admin_password, admin_name="Admin"
):
    db = SessionLocal()
    try:
        # 1. Create tenant
        print(f"🏗️ Creating tenant: {tenant_name}")
        tenant = Tenant(name=tenant_name, slug=tenant_slug, settings={})
        db.add(tenant)
        db.flush()  # Get tenant.id
        print(f"✅ Tenant created with ID: {tenant.id}")

        # 2. Initialize default roles for the tenant
        print("🔐 Initializing default roles...")
        created_roles = init_tenant_roles(tenant.id, db)
        print(f"✅ Created roles: {', '.join(created_roles) if created_roles else 'All roles already exist'}")

        # 3. Get the admin role ID
        admin_role_id = get_default_admin_role_id(tenant.id, db)
        if not admin_role_id:
            raise Exception("Admin role not found")

        # 4. Create admin user with proper role
        print(f"👤 Creating admin user: {admin_email}")
        admin_user = User(
            tenant_id=tenant.id,
            email=admin_email,
            password_hash=get_password_hash(admin_password),
            name=admin_name,
            role_id=admin_role_id,
        )
        db.add(admin_user)
        db.commit()
        
        print(f"✅ Admin user created with ID: {admin_user.id}")
        
        # 5. Initialize asset types, statuses, manufacturers and print templates
        print("🏷️ Initializing asset types, statuses, manufacturers and templates...")
        setup_asset_types(tenant.id)
        setup_asset_statuses(tenant.id)
        seed_manufacturers(tenant.id)
        init_default_templates(tenant.id)
        print("✅ Asset types, statuses, manufacturers and templates initialized")
        
        return tenant, admin_user
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        return None, None
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    # Check if parameters are provided
    if len(sys.argv) >= 4:
        tenant_name = sys.argv[1]
        tenant_slug = sys.argv[2]
        admin_email = sys.argv[3]
        admin_password = sys.argv[4] if len(sys.argv) > 4 else "admin123"
        admin_name = sys.argv[5] if len(sys.argv) > 5 else "Admin"
    else:
        # Default values
        tenant_name = "Nuovo Tenant"
        tenant_slug = "nuovo-tenant"
        admin_email = "admin@example.com"
        admin_password = "admin123"
        admin_name = "Super Admin"
    
    print(f"🏗️ Creating tenant: {tenant_name}")
    print(f"📧 Admin email: {admin_email}")
    
    tenant, admin = create_tenant_with_admin(
        tenant_name=tenant_name,
        tenant_slug=tenant_slug,
        admin_email=admin_email,
        admin_password=admin_password,
        admin_name=admin_name,
    )
    
    if tenant and admin:
        print(f"\n🎉 Tenant created successfully!")
        print(f"🔗 Access URL: http://localhost:3000")
        print(f"📧 Login with: {admin_email}")
        print(f"🔑 Password: {admin_password}")
