"""Add modern email providers to SMTP config

Revision ID: add_modern_email_providers
Revises: 672b47e38787
Create Date: 2026-04-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_modern_email_providers'
down_revision = '672b47e38787'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns for modern email providers
    op.add_column('tenant_smtp_config', sa.Column('provider', sa.String(), nullable=True, server_default='smtp'))
    op.add_column('tenant_smtp_config', sa.Column('api_key', sa.String(), nullable=True))
    op.add_column('tenant_smtp_config', sa.Column('domain', sa.String(), nullable=True))
    op.add_column('tenant_smtp_config', sa.Column('region', sa.String(), nullable=True))
    op.add_column('tenant_smtp_config', sa.Column('credentials', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Make existing SMTP columns nullable
    op.alter_column('tenant_smtp_config', 'host', nullable=True)
    op.alter_column('tenant_smtp_config', 'port', nullable=True)
    op.alter_column('tenant_smtp_config', 'username', nullable=True)
    op.alter_column('tenant_smtp_config', 'password', nullable=True)


def downgrade():
    # Remove new columns
    op.drop_column('tenant_smtp_config', 'credentials')
    op.drop_column('tenant_smtp_config', 'region')
    op.drop_column('tenant_smtp_config', 'domain')
    op.drop_column('tenant_smtp_config', 'api_key')
    op.drop_column('tenant_smtp_config', 'provider')
    
    # Make SMTP columns non-nullable again
    op.alter_column('tenant_smtp_config', 'host', nullable=False)
    op.alter_column('tenant_smtp_config', 'port', nullable=False)
    op.alter_column('tenant_smtp_config', 'username', nullable=False)
    op.alter_column('tenant_smtp_config', 'password', nullable=False) 