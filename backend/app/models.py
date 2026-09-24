from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String) # customer, worker, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(Text)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

class Cooperative(Base):
    __tablename__ = "cooperatives"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), nullable=True)
    experience = Column(String)
    rating = Column(Float, default=0.0)
    completed_jobs = Column(Integer, default=0)
    availability = Column(Boolean, default=True)
    verification_status = Column(String, default="pending")
    service_area = Column(String)
    insurance_status = Column(String, default="inactive")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")
    cooperative = relationship("Cooperative")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    base_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkerSkill(Base):
    __tablename__ = "worker_skills"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    skill_name = Column(String)
    skill_level = Column(String)

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    name = Column(String)
    issuer = Column(String)
    certificate_number = Column(String)
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime, nullable=True)
    verification_status = Column(String, default="pending")

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    date = Column(DateTime)
    start_time = Column(String)
    end_time = Column(String)
    status = Column(String, default="available")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    worker_id = Column(Integer, ForeignKey("workers.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    booking_date = Column(DateTime)
    booking_time = Column(String)
    address = Column(Text)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    service_charge = Column(Float)
    materials_cost = Column(Float, default=0.0)
    cooperative_contribution = Column(Float)
    tax = Column(Float)
    total_amount = Column(Float)
    status = Column(String, default="pending") # pending, accepted, on_the_way, arrived, started, completed, cancelled
    payment_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer")
    worker = relationship("Worker")
    service = relationship("Service")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    amount = Column(Float)
    method = Column(String)
    status = Column(String, default="pending")
    transaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    worker_id = Column(Integer, ForeignKey("workers.id"))
    rating = Column(Float)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Welfare(Base):
    __tablename__ = "welfare"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    insurance_status = Column(String, default="inactive")
    insurance_amount = Column(Float, default=0.0)
    health_support = Column(String, default="available")
    emergency_support = Column(String, default="available")
    training_status = Column(String, default="none")
    benefits = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(Text)
    type = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    priority = Column(String, default="high")
    assigned_worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    status = Column(String, default="pending")
    estimated_arrival = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIForecast(Base):
    __tablename__ = "ai_forecasts"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    location = Column(String)
    forecast_date = Column(DateTime)
    predicted_demand = Column(Integer)
    available_workers = Column(Integer)
    worker_gap = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    service = relationship("Service")

class AllocationRecommendation(Base):
    __tablename__ = "allocation_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    from_cooperative_id = Column(Integer, ForeignKey("cooperatives.id"))
    to_location = Column(String)
    workers_required = Column(Integer)
    reason = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    service = relationship("Service")
    from_cooperative = relationship("Cooperative")
