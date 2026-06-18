# fastapi-core/src/presentation/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import get_db
from src.presentation.schemas.user import UserCreateSchema, UserResponseSchema
from src.infrastructure.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для регистрации нового пользователя в системе BishDelivery
    """
    user_repo = UserRepository(db)

    # 1. Проверяем, не занят ли email
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )

    # 2. Создаем пользователя
    new_user = await user_repo.create_user(user_data)
    return new_user