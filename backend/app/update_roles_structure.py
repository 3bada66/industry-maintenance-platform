import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Role


def update_roles_structure():
    db: Session = SessionLocal()
    
    # Aggiorna tutti i ruoli esistenti
    roles = db.query(Role).all()
    
    for role in roles:
        # Aggiungi campi mancanti se non esistono
        if not hasattr(role, 'description') or role.description is None:
            role.description = f"Ruolo {role.name}"
        
        if not hasattr(role, 'is_inheritable') or role.is_inheritable is None:
            role.is_inheritable = True
        
        if not hasattr(role, 'is_active') or role.is_active is None:
            role.is_active = True
        
        if not hasattr(role, 'parent_role_id') or role.parent_role_id is None:
            role.parent_role_id = None
        
        # Assicurati che il permesso roles sia presente
        if 'roles' not in role.permissions:
            if role.name == 'admin':
                role.permissions['roles'] = 3
            else:
                role.permissions['roles'] = 1
        
        # print(f"Updated role {role.name} with new fields")
    
    db.commit()
    db.close()
    # print("Roles structure updated successfully!")


if __name__ == "__main__":
    update_roles_structure() 