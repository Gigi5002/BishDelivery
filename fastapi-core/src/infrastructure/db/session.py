# fastapi-core/src/infrastructure/db/session.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


# Создаем асинхронный движок
engine = create_async_engine(
    settings.database_url_async,
    echo=True,  # Будет логировать все SQL-запросы в терминал (супер для разработки)
    future=True
)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Базовый класс для будущих ORM моделей
class Base(DeclarativeBase):
    pass

# Dependency Injection для эндпоинтов FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()