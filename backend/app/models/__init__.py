from app.database import Base
from .tenant import Tenant
from .user import User
from .site import Site
from .area import Area
from .asset_type import AssetType
from .location import Location, LocationFloorplan
from .manufacturer import Manufacturer
from .asset_communication import AssetCommunication
from .asset_interface import AssetInterface
from .asset_document import AssetDocument
from .asset_photo import AssetPhoto
from .asset_connection import AssetConnection
from .audit_log import AuditLog
from .asset_status import AssetStatus
from .contact import Contact
from .tenant_smtp_config import TenantSMTPConfig
from .print_template import PrintTemplate
from .print_history import PrintHistory
from .api_key import ApiKey

# Questi modelli dipendono dagli altri (devono venire dopo)
from .supplier import Supplier, SupplierDocument
from .asset import Asset
from .role import Role
