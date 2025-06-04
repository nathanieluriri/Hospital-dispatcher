from schemas.ambulance_schema import AmbulanceBase,AmbulanceOut,AmbulanceStatus,AmbulanceType,NewAmbulanceCreate,UpdateAmbulance
from typing import List
from schemas.emergency_request_schema import ResponedEmergencyRequestModel
from repositories.ambulance_repo import find_ambulance_by_id,create_ambulance,delete_ambulance_by_id,update_ambulance_details,find_all_ambulances
from datetime import datetime,timezone
from  repositories.emergency_requests_repo import final_status_update_emergency_request_func


def add_ambulance_service(new:AmbulanceBase)->AmbulanceOut:
    
    id =create_ambulance(user_data=new)
    return find_ambulance_by_id(id)

def update_ambulance_service(ambulance_id:int,update:UpdateAmbulance)->AmbulanceOut:
    if update.last_assigned_time==None and update.ambulance_status!=None:
        update.last_assigned_time = f"{datetime.now()}"
    return update_ambulance_details(ambulance_id=ambulance_id,update_data=update)


def set_ambulance_to_available(ambulance:AmbulanceOut,emergency_request_id:int,emergency_request_time:int):
    update =UpdateAmbulance(ambulance_status=AmbulanceStatus.Available)
    update_ambulance_service(ambulance_id=ambulance.id,update=update)
    
    final_status_update_emergency_request_func(arrival_time=int(datetime.now(timezone.utc).timestamp()),id=emergency_request_id,request_time=emergency_request_time)
   
    
    
def list_ambulances_service(skip:int,limit:int)->List[AmbulanceOut]:
    return find_all_ambulances(skip=skip,limit=limit)

def find_ambulance_by_id_service(ambulance_id:int)->AmbulanceOut:
    return find_ambulance_by_id(ambulance_id=ambulance_id)

def delete_ambulance_service(ambulance_id:int)->int:
    return delete_ambulance_by_id(ambulance_id=ambulance_id)