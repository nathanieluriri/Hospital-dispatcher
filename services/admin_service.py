from repositories.admin_repo import create_admin
from repositories.token_repo import create_access_tokens
from schemas.admin_schema import AdminBase,user_type
from schemas.token_schema import AccessTokenBase
import sqlite3
from fastapi import HTTPException,status


def sign_up_service(user_data:AdminBase):
    try:
        user_id = create_admin(user_data)
        token_data = AccessTokenBase(user_id=user_id)
        token = create_access_tokens(token_data,role="admin")
        print(token)
        return token
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Admin Already Exists")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because-- {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because {e}")
        
        
user_data = AdminBase(user_type=user_type.Dispatcher,email="uririnathaniel@gmail.com",hashed_password="helloo")

sign_up_service(user_data)
        