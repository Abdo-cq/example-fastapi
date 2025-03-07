"""create posts table

Revision ID: 989b2acf4f7d
Revises: 
Create Date: 2025-03-06 14:55:52.743706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '989b2acf4f7d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts",sa.Column("id",sa.Integer(),nullable=False,primary_key=True),sa.Column("title",sa.String(),nullable=False))
    pass
    


def downgrade() -> None:
    op.drop_table("posts")
    pass
