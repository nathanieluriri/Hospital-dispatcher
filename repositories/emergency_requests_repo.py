from core.database import db
from schemas.emergency_request_schema import SubmitEmergencyRequestModel,UnfinishedEmergencyRequestOut,AssignedEmergencyRequestModel,ResponedEmergencyRequestModel



def add_emergency_request_func(request_data:SubmitEmergencyRequestModel):
    data = request_data.model_dump()
    return db.emergency_request.insert_one(data)
     
def update_status_to_assigned_emergency_request_func(request_data:AssignedEmergencyRequestModel):
    ambulance_id =request_data.assigned_ambulance_id
    dispatch_time = request_data.dispatch_time
    dispatch_delay=request_data.dispatch_delay
    return db.emergency_request.update_one(filter_dict={"id":request_data.id},data={"assigned_ambulance_id":ambulance_id,"dispatch_time":dispatch_time,"dispatch_delay":dispatch_delay})
     

def find_unfinished_emergency_request_by_id(request_id:int):
    data = db.emergency_request.find_one(filter_dict={"id":request_id})
    return UnfinishedEmergencyRequestOut(**data)


def find_list_of_unfinished_emergency_request_by_user_id(user_id:int,skip,limit):
    requests = db.emergency_request.find(filter_dict={"user_id":user_id},skip=skip ,limit=limit)
    if requests:
        return [UnfinishedEmergencyRequestOut(**request) for request in requests]
    else: return []
    

def find_list_of_unfinished_emergency_request(skip,limit):
    requests = db.emergency_request.find(skip=skip ,limit=limit)
    if requests:
        return [UnfinishedEmergencyRequestOut(**request) for request in requests]
    else: return []
    
    
def final_status_update_emergency_request_func(arrival_time:int,id:int,request_time):
    response_duration = arrival_time-request_time
    return db.emergency_request.update_one(filter_dict={"id":id},data={"arrival_time":arrival_time,"response_duration":response_duration})
     
