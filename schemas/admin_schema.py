from schemas.general_imports import *
from security.hash import hash_password
from typing import Union
from enum import Enum


class UserType(str, Enum):
    Dispatcher = "Dispatcher"
    Hospital_Staff = "Hospital_Staff"
    
 
class AdminBase(BaseModel):
    user_type:UserType
    email: EmailStr
    hashed_password:  str 

    
    
class RegisteredAdmin(BaseModel):
    email: EmailStr
    password:  str 

    
        
class NewAdminCreate(AdminBase):
    hashed_password: Union[str ,bytes]
    @model_validator(mode='after')
    def obscure_password(self):
        self.hashed_password=hash_password(self.hashed_password)
        return self

class AdminOut(BaseModel):
    id:int
    user_type:str
    email:EmailStr
    