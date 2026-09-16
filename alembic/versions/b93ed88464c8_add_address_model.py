"""add address model

Revision ID: b93ed88464c8
Revises: 31768bd751de
Create Date: 2026-09-16 17:32:14.461120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b93ed88464c8"
down_revision: Union[str, Sequence[str], None] = "31768bd751de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "mst_address",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False
        ),
        sa.Column(
            "address",
            sa.String(length=100),
            nullable=False
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False
        ),
        sa.Column(
            "city",
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            "state",
            sa.String(length=50),
            nullable=False
        ),
        sa.Column(
            "pincode",
            sa.String(length=20),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["EMS_DB.txn_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="EMS_DB"
    )


def downgrade() -> None:
    op.drop_table(
        "mst_address",
        schema="EMS_DB"
    )