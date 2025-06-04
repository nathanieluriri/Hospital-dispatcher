from schemas.emergency_request_schema import SubmitEmergencyRequestModel,UnfinishedEmergencyRequestOut
from schemas.ambulance_schema import AmbulanceOut,AmbulanceStatus
from repositories.emergency_requests_repo import add_emergency_request_func,find_unfinished_emergency_request_by_id,find_list_of_unfinished_emergency_request_by_user_id,find_list_of_unfinished_emergency_request
from repositories.ambulance_repo import find_all_ambulances
from heapq import heappush, heappop
from math import radians, cos, sin, sqrt, atan2
from typing import List
import asyncio

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def find_nearest_ambulance(emergency_location:UnfinishedEmergencyRequestOut, ambulances:List[AmbulanceOut]):
    heap = []
    for ambulance in ambulances:
        if ambulance.ambulance_status == AmbulanceStatus.Available:
            dist = haversine(emergency_location.latitude, emergency_location.longitude,
                             ambulance.latitude, ambulance.longitude)
            heappush(heap, (dist, ambulance))
    
    return heappop(heap)[1] if heap else None

async def assign_nearest_ambulance(emergency_location:UnfinishedEmergencyRequestOut):
    ambulances = find_all_ambulances()
    nearest_ambulance = find_nearest_ambulance(emergency_location=emergency_location,ambulances=ambulances)
    await asyncio.sleep(2)
    return nearest_ambulance
    

def add_emergency_request_service(emergency_request_data:SubmitEmergencyRequestModel):
 
    emergency_request_id =add_emergency_request_func(request_data=emergency_request_data)
    emergency_request =find_unfinished_emergency_request_by_id(emergency_request_id)

    # TODO:  SETUP BACKGROUND TASK TO ASSIGN THE CLOSEST AMBULANCE
    # TODO:  AFTER THE CLOSEST AMBULANCE HAS BEEN ASSIGNED SETUP ANOTHER BACKGROUND TASK TO COUNTDOWN 30MINS 
    
    return emergency_request
    
    
def get_user_emergency_request_service(user_id,skip ,limit):
    return find_list_of_unfinished_emergency_request_by_user_id(user_id=user_id,skip=skip ,limit=limit)

def get_all_emergency_request_service(skip,limit):
    return find_list_of_unfinished_emergency_request(skip=skip,limit=limit)


