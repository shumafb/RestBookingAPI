from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reservations",
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
    existing_reservations = db.query(models.Reservation).filter(
        models.Reservation.table_id == table_id,
        models.Reservation.id != exclude_reservation_id if exclude_reservation_id else True).all()

    for existing in existing_reservations:
        existing_end = existing.reservation_time + timedelta(minutes=existing.duration_minutes)
        if not (reservation_time >= existing_end or reservation_end <= existing.reservation_time):
            return True
    return False

@router.get("/", response_model=List[schemas.Reservation])
def get_reservations(db: Session = Depends(get_db)):
    try:
        reservations = db.query(models.Reservation).all()
        return reservations
    except:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.post("/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """
    Создает новую бронь
    """

    table = db.query(models.Table).filter(models.Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail= "Стол не найден")

    if check_reservation_conflict(db, reservation.table_id, reservation.reservation_time, reservation.duration_minutes):
        raise HTTPException(status_code=400, detail="Стол уже забронирован на это время. Пожалуйста, выберите другой стол или забронируйте этот на другое время")

    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}", response_model=schemas.Reservation)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Удаляет бронь по ID
    """

    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    db.delete(reservation)
    db.commit()
    return {"message": "Бронь успешно удалена"}