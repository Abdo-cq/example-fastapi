"""create user table

Revision ID: c32ebe22f855
Revises: 68e74f1d2e26
Create Date: 2025-03-06 21:38:12.738947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c32ebe22f855'
down_revision: Union[str, None] = '68e74f1d2e26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("users",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("email",sa.String(),unique=True,nullable=False),
                    sa.Column("password",sa.Integer(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False)
                    )
    pass


def downgrade():
    op.drop_table("users")
    pass
