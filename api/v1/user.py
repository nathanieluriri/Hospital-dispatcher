import sqlite3
from fastapi import APIRouter, HTTPException,Depends, Body,Request,status
from core.database import database_name
from services.user_service import sign_up_service,login_service, create_password_reset_token,set_new_password,logout_service,find_user_by_id,update_service
from schemas.user_schema import UserBase,RegisteredUser,UserOut,UpdateUser
from schemas.token_schema import TokenOut,ResfreshingToken
from schemas.password_reset_schema import VerifyPasswordResetBase,PasswordResetBase,PasswordReset
from schemas.success_response_schema import APISuccessResponse
from security.auth import verify_user_token
from security.tokens import refresh_access_token
router = APIRouter()

@router.post("/sign-up",status_code=status.HTTP_201_CREATED,summary="Register a new user account", description="Creates a new user, hashes password, and returns JWT access and refresh tokens for authentication.",response_description="Successfully created user account.User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def register_user(user:UserBase):
    """
    Registers a new user and returns JWT tokens.

    **Creates:** A new user account.
    **Returns:** `APISuccessResponse` with `user_id`, `access_token`, and `refresh_token`.
    **Raises:** `HTTPException` if user already exists or input is invalid.
    """
    tokens = sign_up_service(user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="User registered successfully.",
    data=tokens
)
    
    
    

@router.post("/sign-in",summary="Log in to a user account",description="Authenticates an existing user with their credentials and returns JWT access and refresh tokens for session management.", response_description="Successfully Logged Into users account. User Id, Access and refresh tokens returned for authentication.",response_model=APISuccessResponse[TokenOut])
def login_user(user:RegisteredUser):
    """
    Authenticates a user and returns JWT tokens.

    **Authenticates:** An existing user account.
    **Returns:** `APISuccessResponse` with `user_id`, `access_token`, and `refresh_token`.
    **Raises:** `HTTPException` if authentication fails (e.g., invalid credentials).
    """
    tokens =login_service (user_data=user)
    
    return APISuccessResponse[TokenOut](
    success=True,
    message="User Logged In successfully.",
    data=tokens
)
    
    
@router.get("/details",summary="Get authenticated user details",
    description="Retrieves the profile details for the currently authenticated user based on their valid JWT access token.",
   dependencies=[Depends(verify_user_token)],response_description="Successfully Retrieved User Account Details.Email, User Id, first name, last name and user type returned.", response_model=APISuccessResponse[UserOut])
def protected_route(token = Depends(verify_user_token)):
    """
    Retrieves the authenticated user's account details.

    **Requires:** Valid JWT access token in Authorization header.
    **Returns:** `APISuccessResponse` with `user_id`, `email`, `first_name`,
               `last_name`, and `user_type`.
    **Raises:** `HTTPException` if token is invalid or expired.
    """
    token['user'].pop('hashed_password')
    
    return APISuccessResponse[UserOut](
    success=True,
    message="User Details retrieved successfully.",
    data=UserOut(**token['user'])
)

    
    
@router.post("/refresh",summary="Refresh JWT Access and Refresh Tokens",    description="""
    Exchanges a valid refresh token for a new pair of access and refresh tokens.
    This mechanism allows users to maintain an authenticated session without
    needing to re-enter credentials, even after the access token expires.
    """,dependencies=[Depends(verify_user_token)],response_description="Successfully Refreshed User access tokens (access and refresh token refreshed successfully ). TokenOut Schema Object returned user_id, access_token, refresh_token.",response_model=APISuccessResponse[TokenOut])
def Refresh_Access_and_Refresh_tokens(refresh_token:ResfreshingToken,token = Depends(verify_user_token)):
    """
    Refreshes user's JWT access and refresh tokens.

    **Requires:** Valid, but potentially expired, access token in Authorization header
                  and a valid refresh token in the request body.
    **Returns:** `APISuccessResponse` with new `access_token` and `refresh_token`.
    **Raises:** `HTTPException` if refresh token is invalid, expired, or doesn't match.
    """
    new_token =refresh_access_token(refresh_token=refresh_token.refresh_token,access_token=token['token'])
    return APISuccessResponse[TokenOut](
        success=True,
        message="User Access Tokens Refreshed Successfully",
        data= new_token
    )
    
    

@router.post("/password/reset-token",summary="Initiate password reset (send OTP)",    description="""
    Starts the password recovery process.
    An One-Time Password (OTP) will be sent to the registered email address.
    This OTP is required for the next step of setting a new password.
    """,response_description="Successfully sent OTP to user Email",response_model=APISuccessResponse[str])
def initiate_change_of_user_password_process(email:PasswordResetBase):
    """
    Initiates the password reset process by sending an OTP to the user's email.

    **Sends:** An OTP (One-Time Password) to the provided email address.
    **Returns:** `APISuccessResponse` indicating successful OTP dispatch.
    **Raises:** `HTTPException` if the email is not found or sending fails.
    """
    create_password_reset_token(user_data=email)
    return APISuccessResponse[str](
        success=True,
        message="Successfully sent OTP",
        data="done"
    )
    
    

@router.post("/reset/password",summary="Complete password reset (set new password)",description="""
    Finalizes the password reset process.
    Requires the user's email, the OTP previously sent, and the new desired password.
    The OTP will be validated before the password is updated.
    """,response_description="Successfully Reset Password For This Email",response_model=APISuccessResponse[str])
def conclude_change_of_user_password_process(email:VerifyPasswordResetBase):
    """
    Completes the password reset process by setting a new password.

    **Requires:** User's email, the OTP received, and the new password.
    **Sets:** A new password for the specified user.
    **Returns:** `APISuccessResponse` indicating successful password reset.
    **Raises:** `HTTPException` if OTP is invalid/expired or email doesn't match.
    """
    reset = PasswordReset(email=email.email,token=email.token,password=email.password)
    set_new_password(password=reset)
    
    return APISuccessResponse[str](
        success=True,
        message="Successfully Reset Password",
        data="done"
    )
    
    

@router.patch("/update-details",summary="Update authenticated user's profile details",description="""
    Allows an authenticated user to update their own profile information,
    such as first name, last name, and email address.
    The user ID is extracted from the provided JWT access token.
    """,response_description="Successfully Updated  User",dependencies=[Depends(verify_user_token)],response_model=APISuccessResponse[UserOut])
def update(details:UpdateUser,token = Depends(verify_user_token)):
    """
    Updates the authenticated user's account details.

    **Requires:** Valid JWT access token in Authorization header.
    **Updates:** User's `first_name`, `last_name`, and/or `email`.
    **Returns:** `APISuccessResponse` with the updated `UserOut` data.
    **Raises:** `HTTPException` if token is invalid, user not found, or input is invalid.
    """
    user_id= token['user'].pop('id')
    update_service(user_id,user_data=details)
    admin_dict=find_user_by_id(user_id)
    admin = UserOut(**admin_dict)
    return APISuccessResponse[UserOut](
        success=True,
        message="Successfully Updated",
        data=admin
    )
    

@router.delete("/logout", responses={status.HTTP_204_NO_CONTENT: {"description": "User successfully Logged Out (no content returned)."
        }}, response_description="Successfully Logged Out User",    summary="Log out user session",
    description="""
    Invalidates the current JWT access token, effectively logging out the user from the current session.
    The token is typically added to a blacklist to prevent its reuse.
    """,dependencies=[Depends(verify_user_token)],response_model=APISuccessResponse[str])
def logout(token = Depends(verify_user_token)):
    """
    Logs out the current user by invalidating their access token.

    **Requires:** Valid JWT access token in Authorization header.
    **Invalidates:** The provided access token, preventing its further use.
    **Returns:** `APISuccessResponse` indicating successful logout.
    **Raises:** `HTTPException` if token is invalid or already blacklisted.
    """
  
    logout_service(access_token=token['token'])
    return APISuccessResponse[str](
        success=True,
        message="Successfully Logged Out",
        data="done"
    )
    
    
