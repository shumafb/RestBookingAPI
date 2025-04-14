from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Table(Base):
    """
    id - идентификатор стола, первичный ключ, индексация
    name - название стола
    seats - количество мест
    location - местоположение
    связь с таблицей Reservation, каскадное удаление
    """
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    seats = Column(Integer)
    location = Column(String(50))
    reservations = relationship("Reservation", back_populates="table", cascade="all, delete-orphan")

class Reservation(Base):
    """
    id - идентификатор брони, первичный ключ, индексация
    customer_name - имя клиента
    table_id - id стола, внешний ключ
    reservation_time - дата и время бронирования
    duration_minutes - продолжительность бронирования в минутах
    связь с таблицей Table
    """
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(50), index=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)

    table = relationship("Table", back_populates="reservations")