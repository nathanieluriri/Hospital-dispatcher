from schemas.general_imports import *
from security.hash import hash_password
from typing import Union
from enum import Enum


class UserType(str, Enum):
    Patients = "Patients"
    Emergency_Contacts = "Emergency_Contacts"
    
    


class UserBase(BaseModel):
    first_name:str
    last_name:str
    user_type:UserType
    email: EmailStr
    password: str 

    
        
class NewUserCreate(UserBase):
    hashed_password: Union[str ,bytes]
    @model_validator(mode='after')
    def obscure_password(self):
        self.hashed_password=hash_password(self.password)
        return self

class UserOut(BaseModel):
    id:int
    first_name:str
    last_name:str
    user_type:str
    email:EmailStr
    
    

class RegisteredUser(BaseModel):
    email: EmailStr
    password:  str 

    
    
class UpdateUser(BaseModel):
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    user_type:Optional[UserType]=None   