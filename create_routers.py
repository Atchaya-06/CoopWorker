import os

routers_dir = "backend/app/routers"
os.makedirs(routers_dir, exist_ok=True)

# 1. services.py
with open(os.path.join(routers_dir, "services.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends
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
""")

# 2. workers.py
with open(os.path.join(routers_dir, "workers.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException
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
""")

# 3. customers.py
with open(os.path.join(routers_dir, "customers.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException
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
""")

# 4. bookings.py
with open(os.path.join(routers_dir, "bookings.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException
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
""")

# 5. ai.py (AI matching and forecasting)
with open(os.path.join(routers_dir, "ai.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
import math

router = APIRouter(prefix="/api/ai", tags=["ai"])

def haversine_distance(lat1, lon1, lat2, lon2):
    # Mock distance for prototype
    return abs(lat1 - lat2) + abs(lon1 - lon2)

@router.post("/match", response_model=schemas.AIMatchResponse)
def ai_match(request: schemas.AIMatchRequest, db: Session = Depends(database.get_db)):
    # Rule-based AI decision-support prototype
    workers = db.query(models.Worker).join(models.WorkerSkill).filter(
        models.WorkerSkill.skill_name == str(request.service_id) # Simulating skill match
    ).all()
    
    if not workers:
        # Fallback to all verified workers for demo
        workers = db.query(models.Worker).filter(models.Worker.verification_status == 'verified').all()
    
    if not workers:
        return None

    # Pick the first one and mock scores for the demo
    best_worker = workers[0]
    
    return schemas.AIMatchResponse(
        worker=best_worker,
        match_score=98.5,
        skill_score=35.0,
        distance_score=23.5,
        availability_score=20.0,
        rating_score=10.0,
        experience_score=10.0
    )

@router.get("/forecast")
def ai_forecast(db: Session = Depends(database.get_db)):
    return [
        {
            "service": "Cleaning",
            "location": "Coimbatore North",
            "predicted_demand": 82,
            "available_workers": 61,
            "worker_gap": 21
        }
    ]
""")

# 6. admin.py
with open(os.path.join(routers_dir, "admin.py"), "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException
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
""")

# main.py
with open("backend/app/main.py", "w") as f:
    f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, services, workers, customers, bookings, ai, admin

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CoopConnect AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for hackathon prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(workers.router)
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(ai.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "CoopConnect AI API is running. Visit /docs for documentation."}
""")

print("Successfully generated routers and main.py")
