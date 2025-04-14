# Restaurant API

API сервис для управления бронированием столиков в ресторане. Позволяет создавать, просматривать и управлять столами и их бронированием.

## Стек технологий

- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic для валидации данных
- Alembic для миграций
- Docker и Docker Compose
- pytest для тестирования
- Логирование с ротацией файлов

## Архитектура

Проект построен с использованием современных практик разработки и включает следующие компоненты:

### Структура проекта:
```
app/
├── models/      # Модели базы данных
├── schemas/     # Pydantic схемы для валидации
├── routers/     # Маршруты API
└── tests/       # Модульные тесты
```

### Основные компоненты:
- **Models** - SQLAlchemy модели для работы с базой данных
- **Schemas** - Pydantic модели для валидации входных/выходных данных
- **Routers** - Обработчики HTTP запросов
- **Database** - Конфигурация подключения к базе данных
- **Logger** - Настраиваемое логирование с поддержкой ротации файлов

## API Endpoints

### Столики (Tables)
- `GET /tables` - Получить список всех столиков
- `POST /tables` - Создать новый столик
- `DELETE /tables/{table_id}` - Удалить столик

### Бронирование (Reservations)
- `GET /reservations` - Получить список всех бронирований
- `POST /reservations` - Создать новое бронирование
- `DELETE /reservations/{reservation_id}` - Удалить бронирование

## Примеры запросов

### Создание столика
```http
POST /tables
Content-Type: application/json

{
    "name": "Столик у окна",
    "seats": 4,
    "location": "У окна"
}
```

### Создание бронирования
```http
POST /reservations
Content-Type: application/json

{
    "customer_name": "Иван Петров",
    "table_id": 1,
    "reservation_time": "2025-04-14T19:00:00",
    "duration_minutes": 120
}
```

## Установка и запуск

1. Клонировать репозиторий
2. Запустить с помощью Docker Compose:
```bash
docker-compose up -d
```

API будет доступно по адресу: `http://localhost:8000`

## Документация API

После запуска проекта документация доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Тестирование

Для запуска тестов используйте:
```bash
pytest
```