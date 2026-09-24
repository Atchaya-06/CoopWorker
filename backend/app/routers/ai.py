from fastapi import APIRouter, Depends
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
