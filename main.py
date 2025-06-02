from fastapi import FastAPI,Depends
from security.auth import verify_admin_token,verify_user_token
# from api.v1 import 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Hospital FastAPI Backend",summary="""Backend for the "Mie Novel-app", providing RESTful endpoints to manage users, novel content (books, chapters, pages), bookmarks, and likes. Features JWT-based authentication supporting both traditional credentials and Google sign-in, including token refresh capabilities.""")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
    