from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user
from typing import List

router = APIRouter(prefix="/api/workers", tags=["workers"])

@router.get("", response_model=List[schemas.WorkerResponse])
def get_workers(db: Session = Depends(database.get_db)):
    return db.query(models.Worker).all()

@router.get("/{id}", response_model=schemas.WorkerResponse)
def get_worker(id: int, db: Session = Depends(database.get_db)):
    worker = db.query(models.Worker).filter(models.Worker.id == id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.put("/{id}", response_model=schemas.WorkerResponse)
def update_worker(id: int, worker_update: schemas.WorkerCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    worker = db.query(models.Worker).filter(models.Worker.id == id).first()
    if not worker or worker.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in worker_update.dict(exclude_unset=True).items():
        setattr(worker, key, value)
    db.commit()
    db.refresh(worker)
    return worker
