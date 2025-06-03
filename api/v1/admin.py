import sqlite3
from fastapi import APIRouter, HTTPException,Depends, Body,Request
from core.database import database_name
from services.admin_service import sign_up_service,login_service
from schemas.admin_schema import AdminBase,RegisteredAdmin,AdminOut
from schemas.token_schema import TokenOut,ResfreshingToken
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_token
from security.tokens import refresh_access_token
router = APIRouter()

@router.post("/sign-up", response_description="Successfully created Admin account. User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def register_admin(user:AdminBase):
    tokens = sign_up_service(user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="Admin registered successfully.",
    data=tokens
)
    
    
    

@router.post("/sign-in", response_description="Successfully Logged Into Admins account. User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def login_admin(user:RegisteredAdmin):
    tokens =login_service (user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="Admin Logged In successfully.",
    data=tokens
)
    
    

@router.get("/details",dependencies=[Depends(verify_token)],response_description="Successfully Retrieved Admin Account Details.Email, User Id, first name, last name and user type returned.", response_model=APISuccessResponse[AdminOut])
def protected_route(token = Depends(verify_token)):
    token[0].pop('hashed_password')
    return APISuccessResponse[AdminOut](
    success=True,
    message="Admin Details retrieved successfully.",
    data=AdminOut(**token[0])
)

    
@router.post("/refresh",dependencies=[Depends(verify_token)],response_description="Successfully Refreshed Admin access tokens (access and refresh token refreshed successfully ). TokenOut Schema Object returned user_id, access_token, refresh_token.",response_model=APISuccessResponse[TokenOut])
def protected_route(refresh_token:ResfreshingToken,token = Depends(verify_token)):
    new_token =refresh_access_token(refresh_token=refresh_token.refresh_token,access_token=token[1])
    return APISuccessResponse[TokenOut](
        success=True,
        message="Admin Access Tokens Refreshed Successfully",
        data= new_token
    )