from schemas.general_imports import *
from security.hash import hash_password
from typing import Union


class PasswordResetTokenCreate(BaseModel):
    user_id:int
    token:str
    created_at:str= datetime.now()
    
    
class PasswordResetBase(BaseModel):
    email:EmailStr
    
    
class VerifyPasswordResetBase(BaseModel):
    email:EmailStr
    password:str
    token:str
    
class PasswordReset(BaseModel):
    email:EmailStr
    token:str
    password:str
