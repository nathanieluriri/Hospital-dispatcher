from repositories.user_repo import create_user,find_user_by_email,update_password,update_user_details,find_user_by_id,delete_user_by_id
from repositories.token_repo import create_access_tokens,create_refresh_tokens
from schemas.user_schema import UserBase,UserType,RegisteredUser,UpdateUser
from schemas.token_schema import AccessTokenBase,RefreshTokenBase,TokenOut
from security.hash import check_password
import sqlite3
from fastapi import HTTPException,status
def sign_up_service(user_data:UserBase)->TokenOut:
    try:
        user_id = create_user(user_data)
        token_data = AccessTokenBase(user_id=user_id)
        token_dict = create_access_tokens(token_data)
        print(token_dict)
        token = token_dict['jwt']
        access_id = token_dict['access_token_id']
        refresh= RefreshTokenBase(user_id=user_id,previous_access_token=access_id)
        refresh_tokn= create_refresh_tokens(token_data=refresh)
        token_out=TokenOut(userId=user_id,accesstoken=token.access_token,refreshtoken=refresh_tokn.refreshToken)
        return token_out
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Already Exists")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because {e}")
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Server Couldn't Complete Your Request because {e}")
        
def login_service(user_data:RegisteredUser):
    user_details = find_user_by_email(email=user_data.email)
    if user_details:
        if check_password(password=user_data.password,hashed=user_details['hashed_password'])==True:
            user_id = user_details['id']
            token_data = AccessTokenBase(user_id=user_id)
            token_dict = create_access_tokens(token_data)
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
    
    
def update_service(user_id:int,user_data:UpdateUser):
    user_details = find_user_by_id(user_id=user_id)
    update_count= update_user_details(user_id=user_details['id'],update_data=user_data)
    return update_count


def change_password_service(user_id:int,password:str):
    user_details = find_user_by_id(user_id=user_id)
    update_count= update_password(user_id=user_details['id'],password=password)
    return update_count

def delete_service(user_id):
    delete_count = delete_user_by_id(user_id=user_id)
    return delete_count

