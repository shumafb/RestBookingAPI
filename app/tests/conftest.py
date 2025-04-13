import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..main import app
from ..database import Base, get_db
from ..models import Base, Table, Reservation

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    """
    Создает тестовую базу данных
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Удаляем таблицы после завершения тестов
    
@pytest.fixture
def client(test_db):
    """
    Создает тестовый клиент FastAPI
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear() # Очищаем зависимости после завершения тестов

@pytest.fixture
def create_test_table(test_db):
    """
    Создает тестовую запись стола в базе данных
    """
    table = Table(name="Test Table", seats=4, location="Test Location")
    test_db.add(table)
    test_db.commit()
    test_db.refresh(table)
    yield table
    test.db.delete(table)
    test_db.commit()
