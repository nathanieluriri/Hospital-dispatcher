from fastapi import APIRouter,status,Depends
from fastapi.responses import JSONResponse
from schemas.hospital_schema import HospitalBase,HospitalOut,UpdateHospitalBase,UpdateHospital
from typing import List
from services.hospital_service import add_hospital_service,update_hospital_service,list_hospitals_service,find_hospital_by_id_service,delete_hospital_service
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_admin_token
router = APIRouter()


@router.post(
    "/add",
    summary="Add a new hospital",
    description="""
    Adds a new hospital to the system. Requires administrator privileges.
    
    """,
    response_description="Successfully added the new hospital.",
    response_model=APISuccessResponse[HospitalOut],
    dependencies=[Depends(verify_admin_token)], # Only admins can add hospitals
    status_code=status.HTTP_201_CREATED,
   
)
def add_a_new_Hospital(hospital: HospitalBase):
    """
    Adds a new hospital record to the database.
    """
    new_hospital = add_hospital_service(new=hospital)
    return APISuccessResponse[HospitalOut](
        success=True,
        message="Hospital added successfully.",
        data=new_hospital
    )

@router.patch(
    "/{hospital_id}",
    summary="Update hospital details",
    description="""
    Updates specific details of an existing hospital identified by its ID.
    This endpoint supports partial updates (PATCH method). Requires administrator privileges.
    """,
    response_description="Successfully updated the hospital details.",
    response_model=APISuccessResponse[HospitalOut],
    dependencies=[Depends(verify_admin_token)], # Only admins can update hospitals
   
)
def update_hospital_details(hospital_id: int, details: UpdateHospitalBase):
    """
    Updates an existing hospital record identified by `hospital_id`.
    """
    details_dict = details.model_dump()
    data =UpdateHospital(**details_dict)
    updated_hospital = update_hospital_service(hospital_id=hospital_id, update=data)
    return APISuccessResponse[HospitalOut](
        success=True,
        message="Hospital details updated successfully.",
        data=updated_hospital
    )



@router.delete(
    "/{hospital_id}",
    summary="Delete a hospital",
    description="""
    Deletes  hospital record from the system identified by its ID.
    This action is irreversible. Requires administrator privileges.
    """,
    response_description="Successfully deleted the hospital.",
    response_model=APISuccessResponse[str], # Or just a 204 No Content response
    dependencies=[Depends(verify_admin_token)], # Only admins can delete hospitals
    status_code=status.HTTP_200_OK, # Use 200 OK for response body, or 204 No Content
    responses={
               status.HTTP_204_NO_CONTENT: { # Alternative if you just want to signal success with no body
            "description": "Hospital successfully deleted (no content returned)."
        }
    }
)
def delete_hospital(hospital_id: int):
    """
    Deletes  hospital record from the database by its ID.
    """
    number_of_deleted_rows = delete_hospital_service(hospital_id=hospital_id)
    if number_of_deleted_rows>0:
        return APISuccessResponse[str](
            success=True,
            message="Hospital deleted successfully.",
            data="done"
        )
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content="")

@router.get(
    "/details",
    summary="List all hospitals",
    description="""
    Retrieves a list of all registered hospitals in the system.
    Supports pagination through `skip` and `limit` query parameters.
    """,
    response_description="Successfully retrieved the list of hospitals.",
    response_model=APISuccessResponse[List[HospitalOut]],
    responses={
               status.HTTP_204_NO_CONTENT: { # Alternative if you just want to signal success with no body
            "description": "Hospital successfully Retrieved But there are no current hospitals in the database (no content returned)."
        }
    }
   
)
def list_all_hospitals(skip: int = 0, limit: int = 10):
    """
    Retrieves a paginated list of all hospitals.
    """
    hospitals = list_hospitals_service(skip=skip, limit=limit)
    if len(hospitals)>0:
        return APISuccessResponse[List[HospitalOut]](
            success=True,
            message="Hospitals retrieved successfully.",
            data=hospitals
        )
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,content="")
        
    
    


@router.get(
    "/{hospital_id}",
    summary="Get hospital by ID",
    description="""
    Retrieves detailed information for a single hospital by its unique ID.
    """,
    response_description="Successfully retrieved hospital details.",
    response_model=APISuccessResponse[HospitalOut],
    responses={
       
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found - Hospital with the specified ID does not exist.",
            "content": {"application/json": {"example": {"detail": "Hospital not found."}}}
        }
    }
)
def get_hospital_by_id(hospital_id: int):
    """
    Retrieves a single hospital record by its ID.
    """
    hospital = find_hospital_by_id_service(hospital_id)
    return APISuccessResponse[HospitalOut](
        success=True,
        message="Hospital retrieved successfully.",
        data=hospital
    )


