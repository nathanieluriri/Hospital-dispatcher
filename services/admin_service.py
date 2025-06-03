from repositories.admin_repo import create_admin,find_admin_by_email
from repositories.token_repo import create_access_tokens,create_refresh_tokens
from schemas.admin_schema import AdminBase,UserType,RegisteredAdmin
from schemas.token_schema import AccessTokenBase,RefreshTokenBase,TokenOut
from security.hash import check_password
import sqlite3
from fastapi import HTTPException,status


def sign_up_service(user_data:AdminBase):
    try:
        user_id = create_admin(user_data)
        token_data = AccessTokenBase(user_id=user_id)
        token_dict  = create_access_tokens(token_data,role="admin")
        token = token_dict['jwt']
        access_id = token_dict['access_token_id']
        refresh= RefreshTokenBase(user_id=user_id,previous_access_token=access_id)
        refresh_tokn= create_refresh_tokens(token_data=refresh)
        token_out=TokenOut(userId=user_id,accesstoken=token.access_token,refreshtoken=refresh_tokn.refreshToken)
        return token_out
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Admin Already Exists")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because-- {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because {e}")
       
       
       
def login_service(user_data:RegisteredAdmin):
    admin_details = find_admin_by_email(user_data=user_data)
    if admin_details:
        if check_password(password=user_data.password,hashed=admin_details['hashed_password'])==True:
            user_id = admin_details['id']
            token_data = AccessTokenBase(user_id=user_id)
            token_dict = create_access_tokens(token_data,role="admin")
            token = token_dict['jwt']
            access_id = token_dict['access_token_id']
            refresh= RefreshTokenBase(user_id=user_id,previous_access_token=access_id)
            refresh_tokn= create_refresh_tokens(token_data=refresh)
            token_out=TokenOut(userId=user_id,accesstoken=token.access_token,refreshtoken=refresh_tokn.refreshToken)
            return token_out
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or Password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Email or Password")
    
    
