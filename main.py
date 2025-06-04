from fastapi import FastAPI,Depends,Request,status
from security.auth import verify_token
from api.v1 import user,admin,ambulance,hospital
from core.database import database_name
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

stop_event = asyncio.Event()

async def periodic_task():
    
    while not stop_event.is_set():
        try:

            await asyncio.sleep(2) 
        except asyncio.CancelledError:
       
            break
        except Exception as e:
            pass
        finally:
            pass
            await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(periodic_task())
    app.state.periodic_task = task # Store the task reference to cancel it later
    yield
    stop_event.set()  # Signal the task to stop
    await app.state.periodic_task 






app = FastAPI(lifespan=lifespan, responses= {
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Missing or invalid token.",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        },
       
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error - Invalid input data.",
            "content": {"application/json": {"example": {"detail": [{"loc": ["body", "license_plate"], "msg": "field required"}]}}}
        }},title="Hospital FastAPI Backend",summary="""API Documentation for the "Hospital Dispatcher system", providing RESTful endpoints to manage users, admins, Ambulances updates (location, status), hospitals, and Emergency requests. Features JWT-based authentication including token refresh capabilities.""",description="This API documentation outlines the comprehensive set of RESTful endpoints for the Hospital Dispatcher System. It details operations for managing various core components: users, administrators, ambulance updates (including real-time location and status), hospitals, and emergency requests. The system features robust JWT-based authentication, ensuring secure access to all resources, and includes token refresh capabilities for continuous, uninterrupted authorization")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
    

    



app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(ambulance.router, prefix="/api/v1/ambulance", tags=["Ambulance"],responses={
     status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - User does not have admin privileges.",
            "content": {"application/json": {"example": {"detail": "Not authorized to perform this action"}}}
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflict - Ambulance with this ID already exists.",
            "content": {"application/json": {"example": {"detail": "Ambulance already exists."}}}
        },
})

app.include_router(hospital.router, prefix="/api/v1/hospital", tags=["Hospital"],responses={
     status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - User does not have admin privileges.",
            "content": {"application/json": {"example": {"detail": "Not authorized to perform this action"}}}
        },
        status.HTTP_409_CONFLICT: {
            "description": "Conflict - .",
            "content": {"application/json": {"example": {"detail": "Hospital already exists."}}}
        },
})




