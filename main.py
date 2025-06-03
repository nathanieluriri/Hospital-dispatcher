from fastapi import FastAPI,Depends,Request
from security.auth import verify_token
from api.v1 import user,admin
from core.database import database_name
from fastapi.middleware.cors import CORSMiddleware
import sqlite3



app = FastAPI(title="Hospital FastAPI Backend",summary="""API Documentation for the "Hospital Dispatcher system", providing RESTful endpoints to manage users, admins, Ambulances updates (location, status), hospitals, and Emergency requests. Features JWT-based authentication including token refresh capabilities.""")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
    
    



app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
