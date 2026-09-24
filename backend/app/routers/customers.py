from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("/me", response_model=schemas.CustomerResponse)
def get_current_customer(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    customer = db.query(models.Customer).filter(models.Customer.user_id == current_user.id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer profile not found")
    return customer
