import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role


def update_roles_permissions():
    db: Session = SessionLocal()
    
    # Aggiorna il ruolo admin
    admin_role = db.query(Role).filter_by(name="admin").first()
    if admin_role:
        if "roles" not in admin_role.permissions:
            admin_role.permissions["roles"] = 3  # Full access
                    # print("Updated admin role with roles permission")
    else:
        # print("Admin role already has roles permission")
        pass
    
    # Aggiorna il ruolo editor
    editor_role = db.query(Role).filter_by(name="editor").first()
    if editor_role:
        if "roles" not in editor_role.permissions:
            editor_role.permissions["roles"] = 1  # Read only
                    # print("Updated editor role with roles permission")
    else:
        # print("Editor role already has roles permission")
        pass
    
    # Aggiorna il ruolo viewer
    viewer_role = db.query(Role).filter_by(name="viewer").first()
    if viewer_role:
        if "roles" not in viewer_role.permissions:
            viewer_role.permissions["roles"] = 1  # Read only
                    # print("Updated viewer role with roles permission")
    else:
        # print("Viewer role already has roles permission")
        pass
    
    db.commit()
    db.close()
    # print("Roles permissions updated successfully!")


if __name__ == "__main__":
    update_roles_permissions() 