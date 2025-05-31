import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Use the app's database URL
instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'mindstoke.db')
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URI)

# add your model's MetaData object here
# for 'autogenerate' support
from app.models import db
target_metadata = db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    from sqlalchemy import create_engine
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
