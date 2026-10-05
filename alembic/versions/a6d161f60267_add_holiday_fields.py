"""add holiday fields

Revision ID: a6d161f60267
Revises: 851c3b4cb39c
Create Date: 2026-10-05 16:21:50.727774

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "a6d161f60267"
down_revision: Union[str, Sequence[str], None] = "851c3b4cb39c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Add day column temporarily as nullable
    op.add_column(
        "mst_holidays",
        sa.Column(
            "day",
            sa.String(length=10),
            nullable=True
        ),
        schema="EMS_DB"
    )

    # Create holiday enum type
    holiday_type_enum = postgresql.ENUM(
        "NATIONAL",
        "PUBLIC",
        "OTHER",
        name="holidaytype",
        schema="EMS_DB"
    )

    holiday_type_enum.create(
        op.get_bind(),
        checkfirst=True
    )

    # Add holiday_type column temporarily as nullable
    op.add_column(
        "mst_holidays",
        sa.Column(
            "holiday_type",
            holiday_type_enum,
            nullable=True
        ),
        schema="EMS_DB"
    )

    # Fill day for existing records
    op.execute("""
        UPDATE "EMS_DB".mst_holidays
        SET day = TRIM(TO_CHAR(date, 'Day'))
        WHERE day IS NULL
    """)

    # Set default holiday type for existing records
    op.execute("""
        UPDATE "EMS_DB".mst_holidays
        SET holiday_type = 'PUBLIC'
        WHERE holiday_type IS NULL
    """)

    # Make columns NOT NULL
    op.alter_column(
        "mst_holidays",
        "day",
        nullable=False,
        schema="EMS_DB"
    )

    op.alter_column(
        "mst_holidays",
        "holiday_type",
        nullable=False,
        schema="EMS_DB"
    )


def downgrade() -> None:

    op.drop_column(
        "mst_holidays",
        "holiday_type",
        schema="EMS_DB"
    )

    op.drop_column(
        "mst_holidays",
        "day",
        schema="EMS_DB"
    )

    holiday_type_enum = postgresql.ENUM(
        "NATIONAL",
        "PUBLIC",
        "OTHER",
        name="holidaytype",
        schema="EMS_DB"
    )

    holiday_type_enum.drop(
        op.get_bind(),
        checkfirst=True
    )