"""add content column to table post

Revision ID: 57e40cf40f9d
Revises: 7b046b8f9c79
Create Date: 2025-03-23 06:33:05.552398

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "57e40cf40f9d"
down_revision: Union[str, None] = "7b046b8f9c79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
