from fastapi import APIRouter,status,Depends,BackgroundTasks
from fastapi.responses import JSONResponse
from schemas.emergency_request_schema import SubmitEmergencyRequestModel,EmergencyRequestOut,UnfinishedEmergencyRequestOut,SubmitEmergencyRequestModelBase
from typing import List
from services.emergency_request_service import add_emergency_request_service,get_user_emergency_request_service,get_all_emergency_request_service
from services.scheduler import background_assign
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_admin_token,verify_user_token
from datetime import datetime, timezone

router = APIRouter()


@router.post(
    "/submit",
    response_model_exclude_none=True,
    summary="Submit a new Emergency Request",
    description="""
    Adds a new Emergency Request to the system. Requires User privileges.
    
    """,
    response_description="Successfully added a new Emergency Request.",
    response_model=APISuccessResponse[UnfinishedEmergencyRequestOut],
    dependencies=[Depends(verify_user_token)],
    status_code=status.HTTP_201_CREATED,
   
)
def add_a_new_Emergency_request(background_tasks:BackgroundTasks,emergency: SubmitEmergencyRequestModelBase,token=Depends(verify_user_token)):
    """
    Adds a new Emergency request to the database.
    """
    user_id = token['user'].pop('id')
    data = emergency.model_dump()
    data['user_id']= user_id
    data['request_time']=int(datetime.now(timezone.utc).timestamp())
    emergency_request_data = SubmitEmergencyRequestModel(**data)
    new_emergency_request = add_emergency_request_service(emergency_request_data=emergency_request_data)
    background_tasks.add_task(background_assign, new_emergency_request)
    print("Started task")
    return APISuccessResponse[UnfinishedEmergencyRequestOut](
        success=True,
        message="Emergency Request added successfully.",
        data=new_emergency_request
    )
    
    
    
@router.get(
    "/user/submissions",
    response_model_exclude_none=True,
    summary="Submit a new Emergency Request",
    description="""
    gets Emergency Request from the system. Requires User privileges.
    
    """,
    response_description="Successfully added a new Emergency Request.",
    response_model=APISuccessResponse[List[UnfinishedEmergencyRequestOut]],
    dependencies=[Depends(verify_user_token)], 

   
)
def get_particular_users_Emergency_request(token=Depends(verify_user_token),skip: int = 0, limit: int = 10):
    """
    gets Emergency Request from the system.
    """
    user_id = token['user'].pop('id')
    
    new_emergency_request = get_user_emergency_request_service(user_id=user_id,skip=skip ,limit=limit)
    return APISuccessResponse[List[UnfinishedEmergencyRequestOut]](
        success=True,
        message="Emergency Request Retrieved successfully.",
        data=new_emergency_request
    )
    
    
@router.get(
    "/total/submissions",
    response_model_exclude_none=True,
    summary="Submit a new Emergency Request",
    description="""
    gets Emergency Request from the system. Requires Admin privileges.
    
    """,
    response_description="Successfully added a new Emergency Request.",
    response_model=APISuccessResponse[List[UnfinishedEmergencyRequestOut]],
    dependencies=[Depends(verify_user_token)], 

   
)
def get_particular_users_Emergency_request(token=Depends(verify_admin_token),skip: int = 0, limit: int = 10):
    """
    gets Emergency Request from the system. Requires Admin privileges.
    
    """

    
    new_emergency_request = get_all_emergency_request_service(skip=skip ,limit=limit)
    return APISuccessResponse[List[UnfinishedEmergencyRequestOut]](
        success=True,
        message="Emergency Request Retrieved successfully.",
        data=new_emergency_request
    )