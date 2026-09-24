from fastapi import FastAPI
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
