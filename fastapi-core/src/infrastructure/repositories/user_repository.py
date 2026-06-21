# fastapi-core/src/infrastructure/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.infrastructure.db.models import UserTable
from src.presentation.schemas.user import UserCreateSchema
from src.infrastructure.security.password import hash_password
from typing import Optional


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> UserTable | None:
        """Ищет пользователя в БД по email (чтобы не было дубликатов)"""
        result = await self.db.execute(select(UserTable).where(UserTable.email == email))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[UserTable]:
        """Ищет пользователя в базе данных по его Telegram ID"""
        result = await self.db.execute(
            select(UserTable).where(UserTable.telegram_id == telegram_id)
        )
        return result.scalars().first()

    async def create_user(self, user_dto: UserCreateSchema) -> UserTable:
        """Создает и сохраняет нового пользователя в PostgreSQL"""
        # 1. Переводим Pydantic-схему в словарь и хешируем пароль
        user_data = user_dto.model_dump()
        user_data["hashed_password"] = hash_password(user_data.pop("password"))

        # 2. Создаем объект SQLAlchemy-модели таблицы
        new_user = UserTable(**user_data)

        # 3. Кладем в сессию базы данных и сохраняем
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)  # База данных сама сгенерирует ему ID
        return new_user