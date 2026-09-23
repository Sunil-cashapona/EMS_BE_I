import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config,pool,text 
from app.core.config import settings
from app.core.database import Base, engine

import app.models.department
import app.models.designation
import app.models.file
import app.models.holiday
import app.models.leave_request
import app.models.leave_type
import app.models.notification
import app.models.payroll_settings
import app.models.reference_type
import app.models.reference_value 
import app.models.salary_record
import app.models.salary_structure
import app.models.user
import app.models.user_lic
import app.models.address
import app.models.attendance
# Alembic Config object
config = context.config


# Configure logging
if config.config_file_name is not None and config.get_section("loggers"):
    fileConfig(config.config_file_name)


# IMPORTANT:
# Import all your SQLAlchemy models here.
# Example:
# from app.models.user import User


# Alembic will use this metadata to detect tables
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without connecting directly to the database."""

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a database connection."""

    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="EMS_DB",
            include_schemas=True,

        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


