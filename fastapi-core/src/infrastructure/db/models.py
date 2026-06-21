# fastapi-core/src/infrastructure/db/models.py
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Boolean, DateTime, text, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.db.session import Base


class UserTable(Base):
    """
    SQLAlchemy-модель для таблицы 'users' в PostgreSQL.
    Наследуется от Base, чтобы Alembic видел эту модель.
    """
    __tablename__ = "users"

    # Mapped[...] из SQLAlchemy 2.0 жестко задает тип колонки для Python (типизация)
    # mapped_column(...) настраивает свойства колонки прямо в базе данных (SQL)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    # Роль пользователя: client, courier, restaurant_admin, super_admin
    role: Mapped[str] = mapped_column(String(30), server_default="client", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)

    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)

    # server_default=text("TIMEZONE('utc', now())") заставляет саму базу Postgres
    # автоматически ставить текущее время при создании записи
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("TIMEZONE('utc', now())"),
        nullable=False
    )