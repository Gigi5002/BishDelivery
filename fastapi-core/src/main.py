# fastapi-core/src/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.infrastructure.db.session import get_db


app = FastAPI(
    title="BishDelivery Core API",
    description="Основной бэкенд-сервис доставки еды в Бишкеке",
    version="1.0.0"
)

@app.get("/healthcheck", tags=["System"])
async def healthcheck(db: AsyncSession = Depends(get_db)):
    """
    Проверяет статус работоспособности API и подключения к PostgreSQL
    """
    try:
        # Делаем ленивый тестовый запрос к БД
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "alive",
        "database": db_status,
        "city": "Bishkek"
    }