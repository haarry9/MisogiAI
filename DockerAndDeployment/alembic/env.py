import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

db_url = os.getenv("DATABASE_URL")

def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = AsyncEngine(
        poolclass=pool.NullPool,
        url=db_url
    )
    async def do_run_migrations(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=None,
        )
        async with context.begin_transaction():
            await context.run_migrations()
    async with connectable.connect() as connection:
        await do_run_migrations(connection)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())