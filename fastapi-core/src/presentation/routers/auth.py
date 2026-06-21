from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import get_db
from src.presentation.schemas.user import UserCreateSchema, UserResponseSchema
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password import hash_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)

    # 1. Проверяем, не занят ли email
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )

    # ХЭШИРУЕМ ПАРОЛЬ ПРЕДВАРИТЕЛЬНО
    user_data.password = hash_password(user_data.password)

    # 2. Создаем пользователя (туда улетит уже захэшированный пароль)
    new_user = await user_repo.create_user(user_data)
    return new_user


@router.get("/check-telegram/{telegram_id}", response_model=UserResponseSchema | None)
async def check_telegram_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """
    Проверяет, зарегистрирован ли пользователь с таким telegram_id в системе.
    Если нет — возвращает null (None).
    """
    user_repo = UserRepository(db)
    user = await user_repo.get_by_telegram_id(telegram_id)
    return user