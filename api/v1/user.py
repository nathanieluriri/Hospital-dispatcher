import sqlite3
from fastapi import APIRouter, HTTPException,Depends, Body,Request
from core.database import database_name
from services.user_service import sign_up_service,login_service
from schemas.user_schema import UserBase,RegisteredUser,UserOut
from schemas.token_schema import TokenOut,ResfreshingToken
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_token
from security.tokens import refresh_access_token
router = APIRouter()

@router.post("/sign-up", response_description="Successfully created user account.User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def register_user(user:UserBase):
    tokens = sign_up_service(user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="User registered successfully.",
    data=tokens
)
    
    
    

@router.post("/sign-in", response_description="Successfully Logged Into users account. User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def login_user(user:RegisteredUser):
    tokens =login_service (user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="User Logged In successfully.",
    data=tokens
)
    
    
@router.get("/details",dependencies=[Depends(verify_token)],response_description="Successfully Retrieved User Account Details.Email, User Id, first name, last name and user type returned.", response_model=APISuccessResponse[UserOut])
def protected_route(token = Depends(verify_token)):
    token[0].pop('hashed_password')
    
    return APISuccessResponse[UserOut](
    success=True,
    message="User Details retrieved successfully.",
    data=UserOut(**token[0])
)

    
    
@router.post("/refresh",dependencies=[Depends(verify_token)],response_description="Successfully Refreshed User access tokens (access and refresh token refreshed successfully ). TokenOut Schema Object returned user_id, access_token, refresh_token.",response_model=APISuccessResponse[TokenOut])
def protected_route(refresh_token:ResfreshingToken,token = Depends(verify_token)):
    new_token =refresh_access_token(refresh_token=refresh_token.refresh_token,access_token=token[1])
    return APISuccessResponse[TokenOut](
        success=True,
        message="User Access Tokens Refreshed Successfully",
        data= new_token
    )