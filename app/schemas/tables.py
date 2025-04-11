from pydantic import BaseModel, Fild
from datetime import datetime
from typing import  Optional

class TableBase(BaseModel):
    name: str
    seats: str
    location: str

class TableCreate(TableBase):
    seats: int = Field(..., gt=0, description="Количество мест за столиком, больше нуля")

class Table(TableBase):
    id: int

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    customer_name: str
    table_idL: int
    reservation_time: datetime
    duration_minutes: int

class ReservationCreate(ReservationBase):
    duration_minutes: int = Field(..., gt=0, description="Длительность бронирования в минутах, больше нуля")

class Reservation(ReservationBase):
    id: int

    class Config:
         orm_mode: True