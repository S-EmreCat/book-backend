"""add publisher table

Revision ID: c0336501b51f
Revises: d80acdf23c07
Create Date: 2025-12-08 21:01:39.488974

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import Session

from app.database import seed_data
from app.enums import Status
from app.models import Publisher

# revision identifiers, used by Alembic.
revision: str = "78caaf37453d"
down_revision: Union[str, None] = "d80acdf23c07"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    db = Session(bind=op.get_bind())

    op.create_table(
        "publisher",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("status", sa.Enum(Status), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # NOTE: This seed data can be removed after deployment. If init_data is used, adjust this section accordingly.
    db.bulk_save_objects([Publisher(**c) for c in seed_data.publishers])
    db.commit()
    publisher_id = db.query(Publisher).order_by(Publisher.id.desc()).first().id

    op.add_column(
        "book", sa.Column("publisher_id", sa.Integer(), nullable=False, server_default=sa.text(str(publisher_id)))
    )
    op.create_foreign_key("fk_book_publisher", "book", "publisher", ["publisher_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_book_publisher", "book", type_="foreignkey")
    op.drop_column("book", "publisher_id")
    op.drop_table("publisher")
