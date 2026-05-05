# backend/schemas/__init__.py

"""
Schemas package for the backend application.
Imports all schemas to maintain backward compatibility.
"""

# Core schemas
from .tenant import Tenant
from .user import UserCreate, UserUpdate, UserRead
from .auth import Token, TokenData

# Location related schemas
from .site import Site, SiteCreate, SiteUpdate
from .area import AreaBase, AreaCreate, AreaUpdate, AreaRead, AreaList
from .location import (
    Location,
    LocationCreate,
    LocationRead,
    LocationFloorplanBase,
    LocationFloorplanCreate,
    LocationFloorplanRead,
    PositionUpdate,
)

# Asset related schemas
from .asset_type import AssetType, AssetTypeBase, AssetTypeCreate, AssetTypeUpdate
from .asset import (
    AssetBase,
    AssetCreate,
    AssetUpdate,
    AssetRead,
    AssetSummary,
    AssetCustomFieldUpdate,
)
from .asset_photo import AssetPhoto, AssetPhotoBase, AssetPhotoCreate
from .asset_document import AssetDocument, AssetDocumentBase, AssetDocumentCreate
from .asset_connection import (
    AssetConnection,
    AssetConnectionCreate,
    AssetConnectionUpdate,
)

# Supplier related schemas
from .supplier import (
    Supplier,
    SupplierBase,
    SupplierCreate,
    SupplierUpdate,
    SupplierDocument,
    SupplierDocumentBase,
    SupplierDocumentCreate,
)

# Manufacturer schemas
from .manufacturer import (
    Manufacturer,
    ManufacturerBase,
    ManufacturerCreate,
    ManufacturerUpdate,
)

# API Key schemas
from .api_key import (
    ApiKeyBase,
    ApiKeyCreate,
    ApiKeyUpdate,
    ApiKeyRead,
    ApiKeyResponse,
    ApiKeyUsage,
)

__all__ = [
    # Core
    "Tenant",
    "UserRead",
    "UserCreate",
    "UserUpdate",
    "Token",
    "TokenData",
    # Location
    "Site",
    "SiteCreate",
    "SiteUpdate",
    "AreaBase",
    "AreaCreate",
    "AreaUpdate",
    "AreaRead",
    "AreaList",
    "Location",
    "LocationCreate",
    "LocationRead",
    "LocationFloorplanBase",
    "LocationFloorplanCreate",
    "LocationFloorplanRead",
    "PositionUpdate",
    # Asset
    "AssetType",
    "AssetTypeBase",
    "AssetTypeCreate",
    "AssetTypeUpdate",
    "AssetBase",
    "AssetCreate",
    "AssetUpdate",
    "AssetRead",
    "AssetSummary",
    "AssetCustomFieldUpdate",
    "AssetPhoto",
    "AssetPhotoBase",
    "AssetPhotoCreate",
    "AssetDocument",
    "AssetDocumentBase",
    "AssetDocumentCreate",
    "AssetConnection",
    "AssetConnectionCreate",
    "AssetConnectionUpdate",
    # Supplier
    "Supplier",
    "SupplierBase",
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierDocument",
    "SupplierDocumentBase",
    "SupplierDocumentCreate",
    # Manufacturer
    "Manufacturer",
    "ManufacturerBase",
    "ManufacturerCreate",
    "ManufacturerUpdate",
    # API Key
    "ApiKeyBase",
    "ApiKeyCreate",
    "ApiKeyUpdate",
    "ApiKeyRead",
    "ApiKeyResponse",
    "ApiKeyUsage",
]
