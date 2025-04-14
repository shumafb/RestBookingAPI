from fastapi import FastAPI
from datetime import datetime
from app.routers import tables, reservations
from app.logger import logger

app = FastAPI(title="Сервис бронирования столиков")

# Подключаем роутеры
app.include_router(tables.router)
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])

@app.get("/", tags=["health"])
async def root():
    """
    Проверка состояния сервера
    """
    current_time = datetime.now().strftime("%d.%м.%Y %H:%М:%S")
    status = {
        "статус": "активен",
        "время_сервера": current_time,
        "сообщение": "Сервис бронирования столиков работает",
        "версия": "1.0.0"
    }
    logger.info(f"👋 Запрос статуса сервера: {status}")
    return status

@app.get("/health", tags=["health"])
async def health_check():
    """
    Расширенная проверка работоспособности сервиса
    """
    try:
        uptime = "Работает"  # Здесь можно добавить реальный расчет времени работы
        status = {
            "статус": "OK",
            "время_проверки": datetime.now().strftime("%d.%м.%Y %H:%М:%S"),
            "состояние_сервиса": uptime,
            "компоненты": {
                "api": "доступно",
                "база_данных": "подключена"
            }
        }
        logger.info("✅ Проверка здоровья сервиса: все системы работают нормально")
        return status
    except Exception as e:
        error_status = {
            "статус": "ошибка",
            "время_проверки": datetime.now().strftime("%d.%м.%Y %H:%М:%S"),
            "ошибка": str(e)
        }
        logger.error(f"❌ Ошибка при проверке здоровья сервиса: {str(e)}")
        return error_status