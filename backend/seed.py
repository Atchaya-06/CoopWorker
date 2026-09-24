import os
from sqlalchemy.orm import Session
from app import models, database
from app.utils.security import get_password_hash

def seed_data():
    db = database.SessionLocal()
    
    # Check if we already seeded
    if db.query(models.Service).first():
        print("Database already seeded.")
        db.close()
        return

    print("Seeding Cooperatives...")
    coop1 = models.Cooperative(name="Coimbatore Labour Cooperative Society", location="Coimbatore", contact="contact@clc.coop")
    coop2 = models.Cooperative(name="Hosur Labour Cooperative Society", location="Hosur", contact="contact@hlc.coop")
    db.add_all([coop1, coop2])
    db.commit()

    print("Seeding Services...")
    services = [
        models.Service(name="Electrician", category="Electrical", description="Wiring, repairs, appliance installation", base_price=450),
        models.Service(name="Plumber", category="Plumbing", description="Leak fixing, pipe installation, unclogging", base_price=400),
        models.Service(name="Cleaning", category="Cleaning", description="Deep cleaning, dusting, sanitization", base_price=350),
        models.Service(name="Carpenter", category="Carpentry", description="Furniture repair, wood works, fittings", base_price=550),
        models.Service(name="Painting", category="Painting", description="Wall painting, touchups, polishing", base_price=600),
        models.Service(name="Caregiver", category="Care", description="Elderly care, nursing assistance", base_price=600),
        models.Service(name="Gardener", category="Gardening", description="Lawn care, pruning, landscaping", base_price=300),
        models.Service(name="Driver", category="Transport", description="Temporary drivers, outstation travel", base_price=500),
        models.Service(name="Technician", category="Repair", description="AC, fridge, washing machine repair", base_price=400)
    ]
    db.add_all(services)
    db.commit()

    print("Seeding Admin User...")
    admin = models.User(name="Admin", email="admin@coopconnect.com", phone="9999999999", password_hash=get_password_hash("admin123"), role="admin")
    db.add(admin)
    db.commit()

    print("Seeding Worker Users...")
    workers_data = [
        {"name": "Ravi Kumar", "email": "ravi@example.com", "skill": "Electrician", "rating": 4.8, "exp": "6 years", "coop": coop1},
        {"name": "Suresh Babu", "email": "suresh@example.com", "skill": "Plumber", "rating": 4.7, "exp": "5 years", "coop": coop1},
        {"name": "Meena Devi", "email": "meena@example.com", "skill": "Cleaning", "rating": 4.9, "exp": "7 years", "coop": coop2},
        {"name": "Arun Kumar", "email": "arun@example.com", "skill": "Carpenter", "rating": 4.6, "exp": "8 years", "coop": coop1},
        {"name": "Lakshmi", "email": "lakshmi@example.com", "skill": "Caregiver", "rating": 4.9, "exp": "5 years", "coop": coop2}
    ]

    for wd in workers_data:
        u = models.User(name=wd["name"], email=wd["email"], phone="98" + str(len(wd["name"])) + "000000", password_hash=get_password_hash("worker123"), role="worker")
        db.add(u)
        db.commit()
        db.refresh(u)
        
        w = models.Worker(user_id=u.id, cooperative_id=wd["coop"].id, experience=wd["exp"], rating=wd["rating"], verification_status="verified", service_area="Coimbatore")
        db.add(w)
        db.commit()
        db.refresh(w)
        
        # Skill mapping
        s = db.query(models.Service).filter(models.Service.name == wd["skill"]).first()
        if s:
            ws = models.WorkerSkill(worker_id=w.id, skill_name=str(s.id), skill_level="Expert")
            db.add(ws)
            db.commit()

    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed_data()
