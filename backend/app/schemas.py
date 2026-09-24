from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CustomerBase(BaseModel):
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    user_id: int
    user: UserResponse
    class Config:
        from_attributes = True

class WorkerBase(BaseModel):
    cooperative_id: Optional[int] = None
    experience: str
    service_area: str

class WorkerCreate(WorkerBase):
    pass

class WorkerResponse(WorkerBase):
    id: int
    user_id: int
    rating: float
    completed_jobs: int
    availability: bool
    verification_status: str
    insurance_status: str
    user: UserResponse
    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str
    description: str
    category: str
    base_price: float

class ServiceResponse(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    worker_id: int
    service_id: int
    booking_date: datetime
    booking_time: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    service_charge: float
    materials_cost: Optional[float] = 0.0
    cooperative_contribution: float
    tax: float
    total_amount: float

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    customer_id: int
    status: str
    payment_status: str
    created_at: datetime
    class Config:
        from_attributes = True

class BookingUpdateStatus(BaseModel):
    status: str

class PaymentBase(BaseModel):
    booking_id: int
    amount: float
    method: str

class PaymentCreate(PaymentBase):
    transaction_id: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    booking_id: int
    worker_id: int
    rating: float
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    customer_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AIMatchRequest(BaseModel):
    service_id: int
    latitude: float
    longitude: float

class AIMatchResponse(BaseModel):
    worker: WorkerResponse
    match_score: float
    skill_score: float
    distance_score: float
    availability_score: float
    rating_score: float
    experience_score: float
