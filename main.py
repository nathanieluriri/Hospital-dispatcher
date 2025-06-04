from fastapi import FastAPI,Depends,Request,status
from security.auth import verify_token
from api.v1 import user,admin,ambulance,hospital,emergency_requests
from core.database import database_name
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()
import asyncio

# The long-running job (runs forever in interval)
def forever_retry_job():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        

      print("Nathaniel")

    except Exception as e:
        print(f"Error in background task: {e}")
    finally:
        loop.close()


# Schedule the job to run every few seconds (forever)

app = FastAPI( responses= {
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
    

    

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(
        forever_retry_job,
        'interval',
        seconds=5,
        id='forever-assign-checker',
        replace_existing=True
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




app.include_router(emergency_requests.router, prefix="/api/v1/emergency-requests", tags=["Emergency Requests"])
