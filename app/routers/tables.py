from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.tables import Table
from app import schemas
from app.database import get_db
from app.logger import logger

router = APIRouter(
    tags=["tables"],
    prefix="/tables",
)

@router.get("/", response_model=List[schemas.Table])
def get_tables(db: Session = Depends(get_db)):
    """
    Возвращает содержимое таблицы Table
    """
    logger.info("📋 Запрос на получение списка всех столов")
    tables = db.query(Table).all()
    logger.info(f"✅ Успешно получен список столов. Количество: {len(tables)}")
    return tables

@router.post("/", response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    """
    Создает новую запись в таблице Table
    """
    logger.info(f"➕ Попытка создания нового стола: {table.dict()}")
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    logger.info(f"✅ Стол успешно создан с ID: {db_table.id}")
    return db_table

@router.delete("/{table_id}", response_model=dict)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """ 
    Удаляет запись из таблицы Table
    """
    logger.info(f"🗑️ Попытка удаления стола с ID: {table_id}")
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        logger.warning(f"❌ Стол с ID {table_id} не найден")
        raise HTTPException(status_code=404, detail="Стол не найден")
    db.delete(db_table)
    db.commit()
    logger.info(f"✅ Стол с ID {table_id} успешно удален")
    return {"message": "Стол удален"}