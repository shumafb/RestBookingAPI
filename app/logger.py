import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger():
    # Создаем директорию для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("restaurant_api")
    logger.setLevel(logging.ERROR)  # Уровень логирования

    # Форматтер с поддержкой русского языка
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s [%(name)s] - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
    )

    # Обработчик для файла с ежедневной ротацией
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'restaurant_api.log'),
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Логируем запуск приложения
    logger.info("🚀 Сервис RestaurantAPI запущен")
    return logger

logger = setup_logger()