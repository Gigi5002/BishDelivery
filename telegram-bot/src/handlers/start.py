import httpx
from aiogram import Router, types
from aiogram.filters import CommandStart

# Наш config.py лежит в той же папке src/, что и main.py, поэтому импорт идет из родительского модуля/соседнего файла
from src.config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    telegram_id = message.from_user.id

    await message.answer("Секунду, проверяю ваш профиль в системе BishDelivery... 🔍")

    try:
        async with httpx.AsyncClient() as client:
            # Стучимся на бэкенд FastAPI
            response = await client.get(f"{settings.API_BASE_URL}/auth/check-telegram/{telegram_id}")

            if response.status_code == 200:
                user_data = response.json()

                if user_data:
                    # Пользователь найден в Postgres 🎉
                    await message.answer(
                        f"С возвращением, {user_data['full_name']}! 👋\n"
                        f"Рады видеть вас снова. Можете приступать к выбору ресторанов.\n"
                        f"Ваш телефон в системе: {user_data['phone']}"
                    )
                else:
                    # Пользователя нет в базе данных ❌
                    await message.answer(
                        f"Привет, {message.from_user.full_name}! Вы у нас впервые.\n"
                        f"Для заказа еды в Бишкеке необходимо зарегистрироваться.\n\n"
                        f"Пожалуйста, введите ваш email для начала регистрации:"
                    )
            else:
                await message.answer("❌ Ошибка сервера при проверке аккаунта. Попробуйте позже.")

    except Exception as e:
        await message.answer("❌ Не удалось связаться с бэкендом. Убедитесь, что сервер FastAPI запущен.")