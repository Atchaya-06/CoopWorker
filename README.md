# CoopConnect AI - Backend & Database

This is the backend for CoopConnect AI, built with FastAPI and PostgreSQL (using SQLAlchemy). It features JWT authentication, role-based access, and APIs for customers, workers, and admins.

## Prerequisites

- Python 3.9+
- PostgreSQL database (or Supabase)

## Installation

1. Create a virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```powershell
pip install -r backend/requirements.txt
```

3. Configure Environment Variables:
Copy `backend/.env.example` to `backend/.env` and update the `DATABASE_URL` with your Supabase PostgreSQL connection string. By default, it will fall back to SQLite for local development.
```powershell
cp backend/.env.example backend/.env
```

## Running the Application

1. Seed the database with initial data:
```powershell
cd backend
python seed.py
```

2. Start the FastAPI server:
```powershell
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can view the interactive API documentation at:
http://localhost:8000/docs

## Frontend Integration

The existing frontend is maintained. A new `api.js` file is located in `js/api.js` which handles the API calls to `localhost:8000`. Make sure to include `<script src="js/api.js"></script>` in your HTML files if you wish to use live data.

## Demo Accounts

You can log in to the backend using the following credentials (password is the same for their respective roles):
- **Admin**: admin@coopconnect.com / admin123
- **Worker**: ravi@example.com / worker123
- **Customer**: (You can register a new one via the API /docs page)
