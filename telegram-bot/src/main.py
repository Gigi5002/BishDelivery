# telegram-bot/main.py
import asyncio
import logging
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import settings

# Настраиваем логи, чтобы видеть, что происходит с ботом
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Хэндлер на команду /start"""
    await message.answer(
        f"Привет, {message.from_user.full_name}! 👋\n"
        f"Добро пожаловать в службу доставки **BishDelivery**!\n\n"
        f"Сейчас я проверю связь с нашим главным сервером..."
    )

    # Делаем запрос к нашему FastAPI бэкэнду! 🚀
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.API_BASE_URL}/healthcheck")
            if response.status_code == 200:
                data = response.json()
                await message.answer(
                    f"✅ Связь с сервером установлена!\n"
                    f"Статус бэкенда: {data['status']}\n"
                    f"База данных: {data['database']}\n"
                    f"Город обслуживания: {data['city']}"
                )
            else:
                await message.answer("❌ Сервер ответил ошибкой. Технические работы.")
    except Exception as e:
        await message.answer("❌ Не удалось достучаться до бэкенда. Убедись, что FastAPI запущен!")


async def main():
    print("Бот успешно запущен и вышел на охоту за заказами!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())