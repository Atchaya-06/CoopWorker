from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(database.get_db), current_user = Depends(get_current_admin_user)):
    workers_count = db.query(models.Worker).count()
    verified_workers = db.query(models.Worker).filter(models.Worker.verification_status == 'verified').count()
    customers_count = db.query(models.Customer).count()
    return {
        "total_workers": workers_count,
        "verified_workers": verified_workers,
        "total_customers": customers_count
    }

@router.patch("/workers/{id}/verify")
def verify_worker(id: int, db: Session = Depends(database.get_db), current_user = Depends(get_current_admin_user)):
    worker = db.query(models.Worker).filter(models.Worker.id == id).first()
    if not worker:
        raise HTTPException(status_code=404)
    worker.verification_status = "verified"
    db.commit()
    return {"message": "Worker verified"}
