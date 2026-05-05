# backend/app/reset_password.py

import sys
import secrets
import string
from app.database import SessionLocal
from app.models import User, Tenant
from app.services.auth import get_password_hash
from sqlalchemy.orm import joinedload


def reset_admin_password(tenant_slug, admin_email, new_password=None):
    """
    Reset password for an admin user in a specific tenant.
    
    Args:
        tenant_slug (str): The slug of the tenant
        admin_email (str): The email of the admin user
        new_password (str, optional): New password. If not provided, generates a secure one.
    
    Returns:
        tuple: (success: bool, message: str, password: str)
    """
    db = SessionLocal()
    try:
        # 1. Find the tenant
        tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
        if not tenant:
            return False, f"❌ Tenant with slug '{tenant_slug}' not found", None
        
        print(f"🏢 Found tenant: {tenant.name} (ID: {tenant.id})")
        
        # 2. Find the admin user in this tenant
        admin_user = db.query(User).filter(
            User.tenant_id == tenant.id,
            User.email == admin_email
        ).first()
        
        if not admin_user:
            return False, f"❌ Admin user with email '{admin_email}' not found in tenant '{tenant_slug}'", None
        
        print(f"👤 Found admin user: {admin_user.name} ({admin_user.email})")
        
        # 3. Generate new password if not provided
        if not new_password:
            # Generate a secure 12-character password
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            new_password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        # 4. Update the password
        admin_user.password_hash = get_password_hash(new_password)
        db.commit()
        
        print(f"✅ Password reset successfully for {admin_user.email}")
        return True, f"✅ Password reset successfully for {admin_user.email}", new_password
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        return False, f"❌ Error: {e}", None
    finally:
        db.close()


def list_tenants():
    """List all available tenants."""
    db = SessionLocal()
    try:
        tenants = db.query(Tenant).all()
        if not tenants:
            print("❌ No tenants found")
            return
        
        print("🏢 Available tenants:")
        for tenant in tenants:
            print(f"  - {tenant.name} (slug: {tenant.slug})")
            
    except Exception as e:
        print(f"❌ Error listing tenants: {e}")
    finally:
        db.close()


def list_admin_users(tenant_slug):
    """List all admin users in a specific tenant."""
    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()
        if not tenant:
            print(f"❌ Tenant with slug '{tenant_slug}' not found")
            return
        
        # Get users with admin role (assuming role name contains 'admin' or 'Admin')
        from app.models import Role
        admin_users = db.query(User).join(Role).filter(
            User.tenant_id == tenant.id,
            Role.name.ilike('%admin%')
        ).all()
        
        if not admin_users:
            print(f"❌ No admin users found in tenant '{tenant_slug}'")
            return
        
        print(f"👤 Admin users in tenant '{tenant.name}':")
        for user in admin_users:
            print(f"  - {user.name} ({user.email})")
            
    except Exception as e:
        print(f"❌ Error listing admin users: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python reset_password.py reset <tenant_slug> <admin_email> [new_password]")
        print("  python reset_password.py list-tenants")
        print("  python reset_password.py list-admins <tenant_slug>")
        print("")
        print("Examples:")
        print("  python reset_password.py reset my-company admin@mycompany.com")
        print("  python reset_password.py reset my-company admin@mycompany.com MyNewPassword123")
        print("  python reset_password.py list-tenants")
        print("  python reset_password.py list-admins my-company")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list-tenants":
        list_tenants()
    elif command == "list-admins":
        if len(sys.argv) < 3:
            print("❌ Please provide tenant slug")
            sys.exit(1)
        tenant_slug = sys.argv[2]
        list_admin_users(tenant_slug)
    elif command == "reset":
        if len(sys.argv) < 4:
            print("❌ Please provide tenant_slug and admin_email")
            sys.exit(1)
        tenant_slug = sys.argv[2]
        admin_email = sys.argv[3]
        new_password = sys.argv[4] if len(sys.argv) > 4 else None
        
        success, message, password = reset_admin_password(tenant_slug, admin_email, new_password)
        print(message)
        
        if success and password:
            print(f"🔐 New password: {password}")
            print(f"💾 Save this password securely!")
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
