"""Add sex field to Client model

Revision ID: add_sex_field_to_client
Revises: 4386c3ef7389
Create Date: 2024-03-23 10:12:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_sex_field_to_client'
down_revision = '4386c3ef7389'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('client', sa.Column('sex', sa.String(length=10), nullable=True))

def downgrade():
    op.drop_column('client', 'sex') 