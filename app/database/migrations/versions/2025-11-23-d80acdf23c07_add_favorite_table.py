"""add favorite table

Revision ID: d80acdf23c07
Revises: a96062d82b60
Create Date: 2025-11-23 22:13:00.456878

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d80acdf23c07"
down_revision: Union[str, None] = "a96062d82b60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorite",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
        sa.Column("book_id", sa.Integer, sa.ForeignKey("book.id"), nullable=False),
        sa.Column("date_created", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime, nullable=False),
    )
    op.create_unique_constraint(
        "uq_favorite_user_book",
        "favorite",
        ["user_id", "book_id"],
    )


def downgrade() -> None:
    op.drop_table("favorite")
