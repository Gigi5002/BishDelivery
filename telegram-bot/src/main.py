import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import settings
# Добавляем src. к импорту хэндлера, чтобы путь шел от корня проекта
from src.handlers.start import router as start_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)

    print("Бот успешно запущен через модульную структуру!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())