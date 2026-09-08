import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

from app.core.config import settings
from app.core.database import Base, engine
from app.models import attendence, departments, designation, file, holiday
from app.models import leave_request, leave_type, notification, payroll_settings
from app.models import reference_type, reference_value, salary_record, salary_structure, user, user_lic


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
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from app.models.departments import Department