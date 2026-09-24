from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user
from typing import List

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.post("", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    customer = db.query(models.Customer).filter(models.Customer.user_id == current_user.id).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Only customers can book")
    
    new_booking = models.Booking(**booking.dict(), customer_id=customer.id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("", response_model=List[schemas.BookingResponse])
def get_bookings(db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    if current_user.role == 'customer':
        customer = db.query(models.Customer).filter(models.Customer.user_id == current_user.id).first()
        return db.query(models.Booking).filter(models.Booking.customer_id == customer.id).all()
    elif current_user.role == 'worker':
        worker = db.query(models.Worker).filter(models.Worker.user_id == current_user.id).first()
        return db.query(models.Booking).filter(models.Booking.worker_id == worker.id).all()
    return []

@router.patch("/{id}/status")
def update_booking_status(id: int, status_update: schemas.BookingUpdateStatus, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    booking = db.query(models.Booking).filter(models.Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = status_update.status
    db.commit()
    return {"message": "Status updated successfully"}
