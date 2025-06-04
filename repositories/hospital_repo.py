from core.database import db
from schemas.hospital_schema import HospitalBase,HospitalOut,NewHospitalCreate,UpdateHospital
from typing import List
from fastapi import HTTPException,status

def create_hospital(user_data:HospitalBase)->int:
    """Inserts into hospital table

    Args:
        user_data (HospitalBase): _description_

    Returns:
        int: Hospital Id
    """
    hospital_dict = user_data.model_dump()
    data= NewHospitalCreate(**hospital_dict)
    hospital_id = db.hospitals.insert_one(data.model_dump()) 
    return hospital_id



def find_hospital_by_id(hospital_id:int)->HospitalOut:
    """Searches Database for Hospital object

    Args:
        hospital_id (int): _description_

    Raises:
        HTTPException: _description_

    Returns:
        HospitalOut: HosptialObject
    """
    hospital_details = db.hospitals.find_one(filter_dict={"id":hospital_id})
    if hospital_details:
        hospital = HospitalOut(**hospital_details)
        return hospital
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Hospital not found")
    
    
def find_all_hospitals(skip:int,limit:int) -> List[HospitalOut]:
    hospitals = db.hospitals.find(skip=skip,limit=limit)
    if hospitals:
        return [HospitalOut(**hospital) for hospital in hospitals]
    else: return []
    
def update_hospital_details(hospital_id:int,update_data:UpdateHospital)->HospitalOut:
    db.hospitals.update_one(filter_dict={"id":hospital_id},data=update_data.model_dump(exclude_none=True))
    return find_hospital_by_id(hospital_id)
    
def delete_hospital_by_id(hospital_id:int):
    return db.hospitals.delete_one({"id":hospital_id})
    