"""add user session table

Revision ID: 851c3b4cb39c
Revises: d5dcae10f313
Create Date: 2026-09-29 12:24:41.282571

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "851c3b4cb39c"
down_revision: Union[str, Sequence[str], None] = "d5dcae10f313"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "txn_user_session",

        sa.Column(
            "id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False
        ),

        sa.Column(
            "session_id",
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["EMS_DB.txn_user.id"]
        ),

        sa.PrimaryKeyConstraint("id"),

        schema="EMS_DB"
    )

    op.create_index(
        "ix_EMS_DB_txn_user_session_session_id",
        "txn_user_session",
        ["session_id"],
        unique=True,
        schema="EMS_DB"
    )


def downgrade() -> None:
    op.drop_index(
        "ix_EMS_DB_txn_user_session_session_id",
        table_name="txn_user_session",
        schema="EMS_DB"
    )

    op.drop_table(
        "txn_user_session",
        schema="EMS_DB"
    )