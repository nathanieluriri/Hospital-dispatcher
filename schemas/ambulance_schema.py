from schemas.general_imports import *
from enum import Enum


class AmbulanceStatus(str, Enum):
    Available = "Available"
    Busy = "Busy"
    Offline="Offline"
    
class AmbulanceType(str, Enum):
    Basic_Life_Support = "Basic_Life_Support"                
    Advanced_Life_Support = "Advanced_Life_Support"         
    Critical_Care = "Critical_Care"                          
    Patient_Transport = "Patient_Transport"                 
    Neonatal_Ambulance = "Neonatal_Ambulance"                
    Air_Ambulance = "Air_Ambulance"                         
    Bariatric_Ambulance = "Bariatric_Ambulance"             
    Disaster_Response_Unit = "Disaster_Response_Unit"        
    Military_Ambulance = "Military_Ambulance"              
    Water_Ambulance = "Water_Ambulance"
 

class AmbulanceBase(BaseModel):
    longitude:float
    latitude:float
    associated_hospital:int
    ambulance_status:AmbulanceStatus
    ambulance_type:AmbulanceType
class NewAmbulanceCreate(AmbulanceBase):
    created_at:str= datetime.now()
    pass

class AmbulanceOut(AmbulanceBase):
    id:int


class UpdateAmbulanceBase(BaseModel):
    longitude:Optional[float]=None
    latitude:Optional[float]=None
    associated_hospital:Optional[int]=None
    ambulance_status:Optional[AmbulanceStatus]=None
    ambulance_type:Optional[AmbulanceType]=None


class UpdateAmbulance(UpdateAmbulanceBase):
    last_updated:str= f"{datetime.now()}"
    last_assigned_time:Optional[str]=None
    
class ManualAssigningAmbulanceBase(BaseModel):
    ambulance_status:Optional[AmbulanceStatus]=None
class ManualAssigningAmbulance(ManualAssigningAmbulanceBase):

    last_updated:str= f"{datetime.now()}"
    last_assigned_time:Optional[str]=f"{datetime.now()}"