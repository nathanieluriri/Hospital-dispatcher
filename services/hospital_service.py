from schemas.hospital_schema import HospitalBase,HospitalOut,UpdateHospital,NewHospitalCreate
from typing import List
from repositories.hospital_repo import find_hospital_by_id,create_hospital,update_hospital_details,find_all_hospitals,delete_hospital_by_id
from datetime import datetime


def add_hospital_service(new:HospitalBase)->HospitalOut:
    new_data = new.model_dump()
    data= NewHospitalCreate(**new_data)
    id =create_hospital(user_data=data)
    return find_hospital_by_id(id)

def update_hospital_service(hospital_id:int,update:UpdateHospital)->HospitalOut:
    return update_hospital_details(hospital_id=hospital_id,update_data=update)

def list_hospitals_service(skip:int,limit:int)->List[HospitalOut]:
    return find_all_hospitals(skip=skip,limit=limit)

def find_hospital_by_id_service(hospital_id:int)->HospitalOut:
    return find_hospital_by_id(hospital_id=hospital_id)

def delete_hospital_service(hospital_id:int)->int:
    return delete_hospital_by_id(hospital_id=hospital_id)