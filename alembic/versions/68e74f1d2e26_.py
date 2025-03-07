"""empty message

Revision ID: 68e74f1d2e26
Revises: 989b2acf4f7d
Create Date: 2025-03-06 21:33:17.195730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68e74f1d2e26'
down_revision: Union[str, None] = '989b2acf4f7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
