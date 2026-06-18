# fastapi-core/src/presentation/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    """
    Схема данных, которую мы ждем от фронтенда/клиента при регистрации.
    Pydantic автоматически проверит, что email похож на email, а телефон заполнен.
    """
    email: EmailStr
    password: str = Field(min_length=6, description="Пароль должен быть не менее 6 символов")
    full_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(description="Номер телефона в формате +996...")

class UserResponseSchema(BaseModel):
    """
    Схема данных, которую наше API вернет клиенту в ответ на успешную регистрацию.
    Мы НИКОГДА не возвращаем hashed_password назад пользователю в целях безопасности!
    """
    id: int
    email: EmailStr
    full_name: str
    phone: str
    role: str
    is_active: bool

    # Позволяет Pydantic автоматически читать данные из ORM-моделей SQLAlchemy
    model_config = {"from_attributes": True}