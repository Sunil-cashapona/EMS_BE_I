"""remove address column from user

Revision ID: d5dcae10f313
Revises: b93ed88464c8
Create Date: 2026-09-23 12:22:45.155607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5dcae10f313'
down_revision: Union[str, Sequence[str], None] = 'b93ed88464c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.drop_column(
        "txn_user",
        "address",
        schema="EMS_DB"
    )



def downgrade() -> None:
    pass