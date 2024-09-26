"""migration_3

Revision ID: bc4c1b41fb1d
Revises: 640027d9347a
Create Date: 2024-09-25 10:24:41.261819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc4c1b41fb1d'
down_revision: Union[str, None] = '640027d9347a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'google_oauth',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('project_id', sa.String, nullable=False),
        sa.Column('private_key_id', sa.String, nullable=False),
        sa.Column('private_key', sa.String, nullable=False), 
        sa.Column('client_email', sa.String, nullable=False),
        sa.Column('client_id', sa.String, nullable=False),
        sa.Column('auth_uri', sa.String, nullable=False),
        sa.Column('token_uri', sa.String, nullable=False),
        sa.Column('auth_provider_x509_cert_url', sa.String, nullable=False),
        sa.Column('client_x509_cert_url', sa.String, nullable=False),
        sa.Column('universe_domain', sa.String, nullable=False),
    )

def downgrade():
    op.drop_table('google_oauth')