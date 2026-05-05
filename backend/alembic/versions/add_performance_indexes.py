"""Add performance indexes for dashboard queries

Revision ID: add_performance_indexes
Revises: add_modern_email_providers
Create Date: 2026-04-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_performance_indexes'
down_revision = 'add_modern_email_providers'
branch_labels = None
depends_on = None


def upgrade():
    # Enable pg_trgm extension for trigram indexes (required for gin_trgm_ops)
    # The extension should be created by init-db.sql script, but we try here as well
    try:
        op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    except Exception:
        # If extension creation fails, we'll use regular indexes instead
        # This is a fallback for cases where the extension can't be created
        pass
    
    # Indici compositi per le query asset più frequenti
    # Questi indici migliorano drasticamente le performance con 5000+ device
    op.create_index('idx_assets_tenant_deleted', 'assets', ['tenant_id', 'deleted_at'])
    op.create_index('idx_assets_tenant_criticality', 'assets', ['tenant_id', 'business_criticality'])
    op.create_index('idx_assets_tenant_risk', 'assets', ['tenant_id', 'risk_score'])
    op.create_index('idx_assets_tenant_updated', 'assets', ['tenant_id', 'updated_at'])
    op.create_index('idx_assets_tenant_status', 'assets', ['tenant_id', 'status_id'])
    op.create_index('idx_assets_tenant_type', 'assets', ['tenant_id', 'asset_type_id'])
    op.create_index('idx_assets_tenant_site', 'assets', ['tenant_id', 'site_id'])
    op.create_index('idx_assets_tenant_location', 'assets', ['tenant_id', 'location_id'])
    op.create_index('idx_assets_tenant_area', 'assets', ['tenant_id', 'area_id'])
    
    # Indici per ricerca globale (ILIKE queries)
    # Try to create trigram indexes if pg_trgm is available, otherwise use regular indexes
    try:
        # Check if pg_trgm extension is available
        connection = op.get_bind()
        from sqlalchemy import text
        result = connection.execute(text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm')"))
        has_pg_trgm = result.scalar()
        
        if has_pg_trgm:
            # Use trigram indexes for better text search performance
            op.execute('CREATE INDEX idx_assets_name_trgm ON assets USING gin (name gin_trgm_ops)')
            op.execute('CREATE INDEX idx_assets_tag_trgm ON assets USING gin (tag gin_trgm_ops)')
            op.execute('CREATE INDEX idx_assets_serial_trgm ON assets USING gin (serial_number gin_trgm_ops)')
        else:
            # Fallback to regular indexes for text search
            op.create_index('idx_assets_name_search', 'assets', ['name'])
            op.create_index('idx_assets_tag_search', 'assets', ['tag'])
            op.create_index('idx_assets_serial_search', 'assets', ['serial_number'])
    except Exception:
        # If trigram indexes fail, use regular indexes as fallback
        op.create_index('idx_assets_name_search', 'assets', ['name'])
        op.create_index('idx_assets_tag_search', 'assets', ['tag'])
        op.create_index('idx_assets_serial_search', 'assets', ['serial_number'])
    
    # Indici per le tabelle correlate
    op.create_index('idx_asset_statuses_tenant', 'asset_statuses', ['tenant_id'])
    op.create_index('idx_asset_types_tenant', 'asset_types', ['tenant_id'])
    op.create_index('idx_sites_tenant', 'sites', ['tenant_id'])
    op.create_index('idx_locations_tenant', 'locations', ['tenant_id'])
    op.create_index('idx_areas_tenant', 'areas', ['tenant_id'])
    op.create_index('idx_manufacturers_tenant', 'manufacturers', ['tenant_id'])
    
    # Indici per le interfacce (usato nella network map)
    op.create_index('idx_asset_interfaces_asset', 'asset_interfaces', ['asset_id'])
    op.create_index('idx_asset_interfaces_ip', 'asset_interfaces', ['ip_address'])
    op.create_index('idx_asset_interfaces_mac', 'asset_interfaces', ['mac_address'])
    
    # Indici per audit logs (spesso query pesanti)
    op.create_index('idx_audit_logs_tenant_timestamp', 'audit_logs', ['tenant_id', 'timestamp'])
    op.create_index('idx_audit_logs_entity', 'audit_logs', ['entity', 'entity_id'])


def downgrade():
    # Rimuovi gli indici in ordine inverso
    op.drop_index('idx_audit_logs_entity', 'audit_logs')
    op.drop_index('idx_audit_logs_tenant_timestamp', 'audit_logs')
    op.drop_index('idx_asset_interfaces_mac', 'asset_interfaces')
    op.drop_index('idx_asset_interfaces_ip', 'asset_interfaces')
    op.drop_index('idx_asset_interfaces_asset', 'asset_interfaces')
    op.drop_index('idx_manufacturers_tenant', 'manufacturers')
    op.drop_index('idx_areas_tenant', 'areas')
    op.drop_index('idx_locations_tenant', 'locations')
    op.drop_index('idx_sites_tenant', 'sites')
    op.drop_index('idx_asset_types_tenant', 'asset_types')
    op.drop_index('idx_asset_statuses_tenant', 'asset_statuses')
    
    # Drop trigram indexes if they exist, otherwise drop regular indexes
    try:
        op.execute('DROP INDEX IF EXISTS idx_assets_serial_trgm')
        op.execute('DROP INDEX IF EXISTS idx_assets_tag_trgm')
        op.execute('DROP INDEX IF EXISTS idx_assets_name_trgm')
    except Exception:
        pass
    
    # Drop regular indexes if they exist
    try:
        op.drop_index('idx_assets_serial_search', 'assets')
        op.drop_index('idx_assets_tag_search', 'assets')
        op.drop_index('idx_assets_name_search', 'assets')
    except Exception:
        pass
    op.drop_index('idx_assets_tenant_area', 'assets')
    op.drop_index('idx_assets_tenant_location', 'assets')
    op.drop_index('idx_assets_tenant_site', 'assets')
    op.drop_index('idx_assets_tenant_type', 'assets')
    op.drop_index('idx_assets_tenant_status', 'assets')
    op.drop_index('idx_assets_tenant_updated', 'assets')
    op.drop_index('idx_assets_tenant_risk', 'assets')
    op.drop_index('idx_assets_tenant_criticality', 'assets')
    op.drop_index('idx_assets_tenant_deleted', 'assets')

