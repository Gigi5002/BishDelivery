# fastapi-core/alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

import asyncio
from alembic import context

import sys
from os.path import dirname, abspath

# Добавляем папку fastapi-core в пути, чтобы Python видел папку src
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from src.config import settings
from src.infrastructure.db.session import Base
# Обязательно импортируем файл моделей, чтобы Alembic узнал о существовании UserTable!
from src.infrastructure.db.models import UserTable

config = context.config

# 2. ПОДСТАВЛЯЕМ НАШ URL ИЗ CONFIG.PY В НАСТРОЙКИ ALEMBIC
config.set_main_option("sqlalchemy.url", settings.database_url_async)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. УКАЗЫВАЕМ METADATA НАШИХ МОДЕЛЕЙ
# Теперь Alembic сможет сравнивать наши Python-классы с реальными таблицами в Postgres
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()



def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме (с подключением к реальной БД)"""
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        # Создаем асинхронный движок для Alembic
        from sqlalchemy.ext.asyncio import create_async_engine
        connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    if isinstance(connectable, context.config.attributes.get("connection", ).__class__):
        # Если движок обычный синхронный
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()
    else:
        # Для нашего асинхронного движка
        async def do_run_migrations():
            async with connectable.connect() as connection:
                await connection.run_sync(do_run_all_migrations)

        def do_all_migrations(connection):
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()

        # Магия запуска асинхронного цикла для миграций
        from sqlalchemy.ext.asyncio import AsyncEngine
        if isinstance(connectable, AsyncEngine):
            def run_sync_migrations(sync_conn):
                context.configure(connection=sync_conn, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()

            async def run_async():
                async with connectable.connect() as connection:
                    await connection.run_sync(run_sync_migrations)

            asyncio.run(run_async())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
