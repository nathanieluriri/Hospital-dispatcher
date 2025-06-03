from schemas.general_imports import *


class HospitalBase(BaseModel):
    Name:str
    phone_number:str
    email: EmailStr
    longitude:float
    latitude:float
    
        
class NewHospitalCreate(HospitalBase):
    pass

class HospitalOut(HospitalBase):
    id:int
