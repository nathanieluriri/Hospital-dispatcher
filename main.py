from fastapi import FastAPI,Depends,Request
from security.auth import verify_token
from api.v1 import user,admin
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






app = FastAPI(lifespan=lifespan,itle="Hospital FastAPI Backend",summary="""API Documentation for the "Hospital Dispatcher system", providing RESTful endpoints to manage users, admins, Ambulances updates (location, status), hospitals, and Emergency requests. Features JWT-based authentication including token refresh capabilities.""")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
    
    



app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


