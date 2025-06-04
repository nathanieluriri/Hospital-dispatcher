from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from schemas.ambulance_schema import AmbulanceBase,AmbulanceOut,UpdateAmbulanceBase,UpdateAmbulance,ManualAssigningAmbulance,ManualAssigningAmbulanceBase
from typing import List
from services.ambulance_service import add_ambulance_service,update_ambulance_service,list_ambulances_service,find_ambulance_by_id_service,delete_ambulance_service
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_admin_token
router = APIRouter()


@router.post(
    "/add",
    summary="Add a new ambulance",
    description="""
    Adds a new ambulance to the system. Requires administrator privileges.
 
    """,
    response_description="Successfully added the new ambulance.",
    response_model=APISuccessResponse[AmbulanceOut],
    dependencies=[Depends(verify_admin_token)], # Only admins can add ambulances
    status_code=status.HTTP_201_CREATED,
   
)
def add_an_Ambulance(ambulance: AmbulanceBase):
    """
    Adds a new ambulance record to the database.
    """
    new_ambulance = add_ambulance_service(new=ambulance)
    return APISuccessResponse[AmbulanceOut](
        success=True,
        message="Ambulance added successfully.",
        data=new_ambulance
    )

@router.patch(
    "/{ambulance_id}",
    summary="Update ambulance details",
    description="""
    Updates specific details of an existing ambulance identified by its ID.
    This endpoint supports partial updates (PATCH method). Requires administrator privileges.
    """,
    response_description="Successfully updated the ambulance details.",
    response_model=APISuccessResponse[AmbulanceOut],
    dependencies=[Depends(verify_admin_token)], # Only admins can update ambulances
   
)
def update_ambulance_details(ambulance_id: int, details: UpdateAmbulanceBase):
    """
    Updates an existing ambulance record identified by `ambulance_id`.
    """
    details_dict = details.model_dump()
    data =UpdateAmbulance(**details_dict)
    updated_ambulance = update_ambulance_service(ambulance_id=ambulance_id, update=data)
    return APISuccessResponse[AmbulanceOut](
        success=True,
        message="Ambulance details updated successfully.",
        data=updated_ambulance
    )



@router.delete(
    "/{ambulance_id}",
    summary="Delete an ambulance",
    description="""
    Deletes an ambulance record from the system identified by its ID.
    This action is irreversible. Requires administrator privileges.
    """,
    response_description="Successfully deleted the ambulance.",
    response_model=APISuccessResponse[str], # Or just a 204 No Content response
    dependencies=[Depends(verify_admin_token)], # Only admins can delete ambulances
    status_code=status.HTTP_200_OK, # Use 200 OK for response body, or 204 No Content
    responses={
               status.HTTP_204_NO_CONTENT: { # Alternative if you just want to signal success with no body
            "description": "Ambulance successfully deleted (no content returned)."
        }
    }
)
def delete_ambulance(ambulance_id: int):
    """
    Deletes an ambulance record from the database by its ID.
    """
    number_of_deleted_rows = delete_ambulance_service(ambulance_id=ambulance_id)
    if number_of_deleted_rows>0:
        return APISuccessResponse[str](
            success=True,
            message="Ambulance deleted successfully.",
            data="done"
        )
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content="")

@router.get(
    "/details",
    summary="List all ambulances",
    description="""
    Retrieves a list of all registered ambulances in the system.
    Supports pagination through `skip` and `limit` query parameters.
    """,
    response_description="Successfully retrieved the list of ambulances.",
    response_model=APISuccessResponse[List[AmbulanceOut]],
    responses={
               status.HTTP_204_NO_CONTENT: { # Alternative if you just want to signal success with no body
            "description": "Ambulance successfully Retrieved But there are no current ambulances in the database (no content returned)."
        }
    }
   
)
def list_all_ambulances(skip: int = 0, limit: int = 10):
    """
    Retrieves a paginated list of all ambulances.
    """
    ambulances = list_ambulances_service(skip=skip, limit=limit)
    if len(ambulances)>0:
        return APISuccessResponse[List[AmbulanceOut]](
            success=True,
            message="Ambulances retrieved successfully.",
            data=ambulances
        )
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content="")
        
    
    


@router.get(
    "/{ambulance_id}",
    summary="Get ambulance by ID",
    description="""
    Retrieves detailed information for a single ambulance by its unique ID.
    """,
    response_description="Successfully retrieved ambulance details.",
    response_model=APISuccessResponse[AmbulanceOut],
    responses={
       
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found - Ambulance with the specified ID does not exist.",
            "content": {"application/json": {"example": {"detail": "Ambulance not found."}}}
        }
    }
)
def get_ambulance_by_id(ambulance_id: int):
    """
    Retrieves a single ambulance record by its ID.
    """
    ambulance = find_ambulance_by_id_service(ambulance_id)
    return APISuccessResponse[AmbulanceOut](
        success=True,
        message="Ambulance retrieved successfully.",
        data=ambulance
    )



@router.patch(
    "/manual-status-update/{ambulance_id}",
    summary="Manually Update ambulance details",
    description="""
    Updates specific details of an existing ambulance identified by its ID.
    This endpoint supports partial updates (PATCH method). Requires administrator privileges.
    """,
    response_description="Successfully updated the ambulance details.",
    response_model=APISuccessResponse[AmbulanceOut],
    dependencies=[Depends(verify_admin_token)], # Only admins can update ambulances
   
)
def manual_assigning_ambulance_status(ambulance_id: int, details: ManualAssigningAmbulanceBase):
    """
    Updates an existing ambulance record identified by `ambulance_id`.
    """
    update_details = ManualAssigningAmbulance(ambulance_status=details.ambulance_status)
    updated_ambulance = update_ambulance_service(ambulance_id=ambulance_id, update=update_details)
    return APISuccessResponse[AmbulanceOut](
        success=True,
        message="Ambulance details updated successfully.",
        data=updated_ambulance
    )

