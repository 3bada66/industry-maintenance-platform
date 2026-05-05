import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role


def update_roles_timestamps():
    db: Session = SessionLocal()
    
    # Aggiorna tutti i ruoli esistenti
    roles = db.query(Role).all()
    current_time = datetime.utcnow()
    
    for role in roles:
        if not hasattr(role, 'created_at') or role.created_at is None:
            role.created_at = current_time
        
        if not hasattr(role, 'updated_at') or role.updated_at is None:
            role.updated_at = current_time
        
        # print(f"Updated role {role.name} with timestamps")
    
    db.commit()
    db.close()
    # print("Roles timestamps updated successfully!")


if __name__ == "__main__":
    update_roles_timestamps() 