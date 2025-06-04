from schemas.general_imports import *
from enum import Enum


class HospitalBase(BaseModel):
    Name:str
    email:EmailStr
    phone_number:str
    longitude:float
    latitude:float

        
     
class NewHospitalCreate(HospitalBase):
    created_at:str=f"{datetime.now()}"
    last_updated:str= f"{datetime.now()}"
    

class HospitalOut(HospitalBase):
    id:int


class UpdateHospitalBase(BaseModel):
    longitude:Optional[float]=None
    latitude:Optional[float]=None
    Name:Optional[str]=None
    email:Optional[EmailStr]=None
    phone_number:Optional[str]=None

    
class UpdateHospital(UpdateHospitalBase):

    last_updated:str=f"{datetime.now()}"

    
