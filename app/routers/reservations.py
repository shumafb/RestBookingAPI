from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.models.tables import Table, Reservation
from app import schemas
from app.database import get_db
from app.logger import logger

router = APIRouter(
    tags=["reservations"]
)

def check_reservation_time(db: Session,
                            table_id: int,
                            reservation_time: datetime,
                            duration_minutes: int,
                            exclude_reservation_id: int = None):
    """
    Проверяет, есть ли пересечение с существующими бронями
    """
    logger.info(f"🔍 Проверка доступности стола {table_id} на {reservation_time}")
    reservation_end = reservation_time + timedelta(minutes=duration_minutes)
    existing_reservations = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        Reservation.id != exclude_reservation_id if exclude_reservation_id else True).all()

    for existing in existing_reservations:
        existing_end = existing.reservation_time + timedelta(minutes=existing.duration_minutes)
        if not (reservation_time >= existing_end or reservation_end <= existing.reservation_time):
            logger.warning(f"⚠️ Обнаружено пересечение броней для стола {table_id}")
            return True
    logger.info(f"✅ Стол {table_id} свободен на запрошенное время")
    return False

@router.get("/", response_model=List[schemas.Reservation])
def get_reservations(db: Session = Depends(get_db)):
    logger.info("📋 Запрос на получение списка всех бронирований")
    try:
        reservations = db.query(Reservation).all()
        logger.info(f"✅ Успешно получен список бронирований. Количество: {len(reservations)}")
        return reservations
    except Exception as e:
        logger.error(f"❌ Ошибка при получении списка бронирований: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """
    Создает новую бронь
    """
    logger.info(f"➕ Попытка создания нового бронирования: стол {reservation.table_id} на {reservation.reservation_time}")

    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        logger.warning(f"❌ Стол {reservation.table_id} не найден")
        raise HTTPException(status_code=404, detail="Стол не найден")

    if check_reservation_time(db, reservation.table_id, reservation.reservation_time, reservation.duration_minutes):
        logger.warning(f"⚠️ Стол {reservation.table_id} уже забронирован на {reservation.reservation_time}")
        raise HTTPException(status_code=400, detail="Стол уже забронирован на это время. Пожалуйста, выберите другой стол или забронируйте этот на другое время")

    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    logger.info(f"✅ Бронирование успешно создано с ID: {db_reservation.id}")
    return db_reservation

@router.delete("/{reservation_id}", response_model=schemas.Reservation)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Удаляет бронь по ID
    """
    logger.info(f"🗑️ Попытка удаления бронирования с ID: {reservation_id}")

    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        logger.warning(f"❌ Бронирование с ID {reservation_id} не найдено")
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    db.delete(reservation)
    db.commit()
    logger.info(f"✅ Бронирование с ID {reservation_id} успешно удалено")
    return {"message": "Бронь успешно удалена"}