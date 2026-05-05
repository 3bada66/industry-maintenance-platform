import uuid
from datetime import datetime
from sqlalchemy import Column, String, JSON, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)  # Multi-tenancy support
    name = Column(String(50), nullable=False)  # No longer globally unique, but per tenant
    description = Column(String(255), nullable=True)
    permissions = Column(JSON, nullable=False, default=dict)
    is_inheritable = Column(Boolean, default=True)  # Se i permessi sono ereditabili
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    users = relationship("User", back_populates="role")
    
    # Relationship for child roles (inheritance)
    child_roles = relationship("Role", 
                              backref="parent_role",
                              remote_side=[id],
                              cascade="all")
    
    def get_effective_permissions(self):
        """
        Ottiene i permessi effettivi includendo l'ereditarietà
        """
        effective_permissions = self.permissions.copy() if self.permissions else {}
        
        # If it has a parent role and inheritance is enabled
        if self.parent_role and self.is_inheritable:
            parent_permissions = self.parent_role.get_effective_permissions()
            # Unisce i permessi del padre con quelli del figlio (il figlio ha precedenza)
            for section, level in parent_permissions.items():
                if section not in effective_permissions or effective_permissions[section] < level:
                    effective_permissions[section] = level
        
        return effective_permissions
    
    def has_permission(self, section, min_level=1):
        """
        Verifica se il ruolo ha un permesso specifico
        """
        effective_permissions = self.get_effective_permissions()
        return effective_permissions.get(section, 0) >= min_level
    
    def can_read(self, section):
        """Verifica permesso di lettura"""
        return self.has_permission(section, 1)
    
    def can_write(self, section):
        """Verifica permesso di scrittura"""
        return self.has_permission(section, 2)
    
    def can_delete(self, section):
        """Verifica permesso di eliminazione"""
        return self.has_permission(section, 3)
    
    def can_bulk_operate(self, section):
        """Verifica permesso di operazioni massive"""
        return self.has_permission(section, 4)
