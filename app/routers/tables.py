from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)

@router.get("/", response_model=List[schemas.Table])
def get_tables(db: Session = Depends(get_db)):
    """
    Возвращает содержимое таблицы Table
    """
    tables = db.query(models.Table).all()
    return tables

@router.post("/", response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    """
    Создает новую запись в таблице Table
    """
    db_table = models.Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete("/{table_id}", response_model=schemas.Table)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """
    Удаляет запись из таблицы Table
    """
    db_table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Стол не найден")
    db.delete(db_table)
    db.commit()
    return {"message": "Стол удален"}