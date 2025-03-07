"""add phone number to user table

Revision ID: 579af97bcdd9
Revises: b8246d793e35
Create Date: 2025-03-06 22:34:59.411840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '579af97bcdd9'
down_revision: Union[str, None] = 'b8246d793e35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users",sa.Column("phone_number",sa.String(),nullable=True))


def downgrade() :
    op.drop_column("users","phone_number")
