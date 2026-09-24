from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
from typing import List

router = APIRouter(prefix="/api/services", tags=["services"])

@router.get("", response_model=List[schemas.ServiceResponse])
def get_services(db: Session = Depends(database.get_db)):
    return db.query(models.Service).all()

@router.get("/{id}", response_model=schemas.ServiceResponse)
def get_service(id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Service).filter(models.Service.id == id).first()
