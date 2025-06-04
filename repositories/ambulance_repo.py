from core.database import db
from schemas.ambulance_schema import AmbulanceBase,AmbulanceOut,AmbulanceStatus,AmbulanceType,NewAmbulanceCreate,UpdateAmbulance
from typing import List
from fastapi import HTTPException,status

def create_ambulance(user_data:AmbulanceBase)->int:
    """Inserts into ambulance table

    Args:
        user_data (AmbulanceBase): _description_

    Returns:
        int: Ambulance Id
    """
    ambulance_dict = user_data.model_dump()
    data= NewAmbulanceCreate(**ambulance_dict)
    ambulance_id = db.ambulances.insert_one(data.model_dump()) 
    return ambulance_id



def find_ambulance_by_id(ambulance_id:int)->AmbulanceOut:
    ambulance_details = db.ambulances.find_one(filter_dict={"id":ambulance_id})
    if ambulance_details:
        ambulance = AmbulanceOut(**ambulance_details)
        return ambulance
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Ambulance not found")
    
    
def find_all_ambulances() -> List[AmbulanceOut]:
    ambulances = db.ambulances.find()
    if ambulances:
        return [AmbulanceOut(**ambulance) for ambulance in ambulances]
    else: return []
    
def update_ambulance_details(ambulance_id:int,update_data:UpdateAmbulance)->AmbulanceOut:
    db.ambulances.update_one(filter_dict={"id":ambulance_id},data=update_data.model_dump(exclude_none=True))
    return find_ambulance_by_id(ambulance_id)
    
def delete_admin_by_id(ambulance_id:int):
    return db.ambulances.delete_one({"id":ambulance_id})
    