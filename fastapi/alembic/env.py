from logging.config import fileConfig
import sys
import os
from dotenv import load_dotenv

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()  # loads .env automatically

# -------------------------------
# Add project root to path
# -------------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -------------------------------
# Import your models
# -------------------------------
from app.db.models.m_base import Base
from app.db.models import *
# import other old tables if needed
# this ensures autogenerate sees all tables
target_metadata = Base.metadata

# -------------------------------
# Alembic Config
# -------------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use DB URL from environment / settings
DATABASE_URL = os.getenv("PG_SYNC")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# -------------------------------
# Migration functions
# -------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table="alembic_version_wildfire",  # custom version table
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="alembic_version_wildfire",  # custom version table
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------
# Run appropriate mode
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
