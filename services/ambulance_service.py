from schemas.ambulance_schema import AmbulanceBase,AmbulanceOut,AmbulanceStatus,AmbulanceType,NewAmbulanceCreate,UpdateAmbulance
from typing import List
from repositories.ambulance_repo import find_ambulance_by_id,create_ambulance,delete_ambulance_by_id,update_ambulance_details,find_all_ambulances
from datetime import datetime


def add_ambulance_service(new:AmbulanceBase)->AmbulanceOut:
    
    id =create_ambulance(user_data=new)
    return find_ambulance_by_id(id)

def update_ambulance_service(ambulance_id:int,update:UpdateAmbulance)->AmbulanceOut:
    if update.last_assigned_time==None and update.ambulance_status!=None:
        update.last_assigned_time = f"{datetime.now()}"
    return update_ambulance_details(ambulance_id=ambulance_id,update_data=update)

def list_ambulances_service(skip:int,limit:int)->List[AmbulanceOut]:
    return find_all_ambulances()

def find_ambulance_by_id_service(ambulance_id:int)->AmbulanceOut:
    return find_ambulance_by_id(ambulance_id=ambulance_id)

def delete_ambulance_service(ambulance_id:int)->int:
    return delete_ambulance_by_id(ambulance_id=ambulance_id)