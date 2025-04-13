import pytest
from datetime import datetime, timedelta
from ..models import Reservation

def test_create_table_with_negative_seats(client):
    """
    Проверка создания стола с отрицательным количеством мест
    """

    table_data = {
        "name": "Test Table",
        "seats": -5,°
        "location": "Test Location"
    }

    response = client.post("/tables/", json=table_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "по умолчанию должно быть больше 0"

def test_create_table_with_zero_seats(client):
    """
    Проверка создания стола с нулевым количеством мест
    """

    table_data = {
        "name": "Test Table",
        "seats": 0,
        "location": "Test Location"
    }

    response = client.post("/tables/", json=table_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "по умолчанию должно быть больше 0"

def test_create_reservation(client, test_db, sample_table):
    """
    Проверка создания бронирования
    """

    table_id = sample_table.id
    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": table_id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 120
    }

    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == reservation_data["customer_name"]
    assert data["table_id"] == table_id

def test_create_reservation_nonexistent_table(client):
    """
    Проверка создания бронирования на несуществующий стол
    """
    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": 999,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 120
    }
    
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 404

def test_create_reservation_with_negative_duration(client, sample_table):
    """
    Проверка создания бронирования с отрицательной продолжительностью
    """
    
    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": sample_table.id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": -30
    }

    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "по умолчанию должно быть больше 0"

def test_create_reservation_with_zero_duration(client, sample_table):
    """
    Проверка создания бронирования с нулевой продолжительностью
    """

    reservation_data = {
        "customer_name": "Test Customer",
        "table_id": sample_table.id,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 0
    }

    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "по умолчанию должно быть больше 0"

def test_create_conflicting_reservation(client, test_db, sample_table):
    """
    Проверка создания конфликта бронирования
    """
    
    reservation_time = datetime.now() + timedelta(days=1) # Создаем первое бронирование
    reservation1 = Reservation(
        customer_name="First Customer",
        table_id=sample_table.id,
        reservation_time=reservation_time,
        duration_minutes=120
    )
    test_db.add(reservation1)
    test_db.commit()

    reservation_data = {
        "customer_name": "Second Customer",
        "table_id": sample_table.id,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 120
    } # Пытаемся создать второе бронирование на то же время
    
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 400

def test_get_reservations(client, test_db, sample_table):
    """
    Проверка получения списка бронирований
    """
    
    reservation = Reservation(
        customer_name="Test Customer",
        table_id=sample_table.id,
        reservation_time=datetime.now() + timedelta(days=1),
        duration_minutes=120
    ) # Создаем тестовое бронирование
    test_db.add(reservation)
    test_db.commit()

    response = client.get("/reservations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_name"] == "Test Customer"

def test_delete_reservation(client, test_db, sample_table):
    """
    Проверка удаления бронирования
    """

    reservation = Reservation(
        customer_name="Test Customer",
        table_id=sample_table.id,
        reservation_time=datetime.now() + timedelta(days=1),
        duration_minutes=120
    ) # Создаем тестовое бронирование
    test_db.add(reservation)
    test_db.commit()

    response = client.delete(f"/reservations/{reservation.id}")
    assert response.status_code == 200

    response = client.get("/reservations/") # Проверяем, что бронирование удалено
    assert len(response.json()) == 0

def test_delete_nonexistent_reservation(client):
    """
    Проверка удаления несуществующего бронирования
    """
    
    response = client.delete("/reservations/999")
    assert response.status_code == 404