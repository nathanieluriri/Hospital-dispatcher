from apscheduler.schedulers.background import BackgroundScheduler
from typing import Any
from apscheduler.jobstores.base import JobLookupError
from schemas.emergency_request_schema import UnfinishedEmergencyRequestOut,AssignedEmergencyRequestModel
from services.emergency_request_service import assign_nearest_ambulance
from schemas.ambulance_schema import UpdateAmbulance,AmbulanceStatus
from repositories.emergency_requests_repo import update_status_to_assigned_emergency_request_func
from repositories.ambulance_repo import update_ambulance_details
scheduler = BackgroundScheduler()
scheduler.start()

def retry_assign_ambulance(emergency_location: UnfinishedEmergencyRequestOut, job_id: str):
    import asyncio
    try:
    
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

     
        nearest_ambulance = loop.run_until_complete(assign_nearest_ambulance(emergency_location))

        if nearest_ambulance:
            print(f"Ambulance assigned: {nearest_ambulance}")
            try:
                from datetime import datetime,timezone
                scheduler.remove_job(job_id)
               
                old_data = emergency_location.model_dump(exclude_none=True)
                
                old_data['dispatch_time']=int(datetime.now(timezone.utc).timestamp())
                old_data['dispatch_delay'] = old_data['dispatch_time']-old_data['request_time']
                old_data['assigned_ambulance_id']=nearest_ambulance.id
                new_data = AssignedEmergencyRequestModel(**old_data)
                
                update_ambulance_details(ambulance_id=nearest_ambulance.id,update_data=UpdateAmbulance(ambulance_status=AmbulanceStatus.Busy,last_assigned_time=f"{datetime.now()}"))
                update_status_to_assigned_emergency_request_func(request_data=new_data)
                print(f"Stopped retry job: {job_id}")
            except JobLookupError:
                pass
    finally:
 
        loop.close()


def schedule_retry_assign(emergency_location:UnfinishedEmergencyRequestOut):
    job_id = f"retry-{emergency_location.id}"   

    scheduler.add_job(
        retry_assign_ambulance,
        'interval',
        seconds=2,
        args=[emergency_location, job_id],
        id=job_id,
        replace_existing=True   
    )


def background_assign(emergency_location: UnfinishedEmergencyRequestOut):
    schedule_retry_assign(emergency_location)

