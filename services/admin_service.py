from repositories.admin_repo import create_admin,find_admin_by_email,find_admin_by_id,update_admin_details,update_password,delete_admin_by_id
from repositories.token_repo import create_access_tokens,create_refresh_tokens
from schemas.admin_schema import AdminBase,UserType,RegisteredAdmin,UpdateAdmin
from schemas.token_schema import AccessTokenBase,RefreshTokenBase,TokenOut
from security.hash import check_password
from security.encrypting_jwt import decode_jwt_token_without_expiration

import sqlite3
from fastapi import HTTPException,status
from core.database import db
from schemas.password_reset_schema import VerifyPasswordResetBase,PasswordResetBase,PasswordReset,PasswordResetTokenCreate
import random
from services.email_service import send_change_of_password_otp_email


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
    admin_details = find_admin_by_email(email=user_data.email)
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
    
    

    
def update_service(user_id:int,user_data:UpdateAdmin):
    user_details = find_admin_by_id(user_id=user_id)
    update_count= update_admin_details(user_id=user_details['id'],update_data=user_data)
    return update_count


def change_password_service(user_id:int,password:str):
    user_details = find_admin_by_id(user_id=user_id)
    update_count= update_password(user_id=user_details['id'],password=password)
    return update_count

def delete_service(user_id):
    delete_count = delete_admin_by_id(user_id=user_id)
    return delete_count




def generate_random_six_integers_as_string(min_val=0, max_val=9, separator=""):

  if min_val > max_val:
    raise ValueError("min_val cannot be greater than max_val")

  random_integers = [random.randint(min_val, max_val) for _ in range(6)]

  # Convert each integer to a string and join them with the specified separator
  return separator.join(map(str, random_integers))

def create_password_reset_token(user_data:PasswordResetBase):
    OTP=generate_random_six_integers_as_string()
    
    admin_details = find_admin_by_email(email=user_data.email)
    if admin_details:
        password_reset_token = PasswordResetTokenCreate(user_id=admin_details['id'],token=OTP)
        db.password_reset_token.insert_one(data=password_reset_token.model_dump())
        send_change_of_password_otp_email(receiver_email=user_data.email,otp=OTP)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    
    
def verify_password_token(token:str):
    valid_token =db.password_reset_token.find_one(filter_dict={"token":token})

    if valid_token:
        from datetime import datetime, timedelta
        saved_time_str=valid_token['created_at']
        print(saved_time_str,type(saved_time_str))
        saved_time = datetime.strptime(saved_time_str, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()
        # Check if 10 minutes have passed
        ten_minutes_later = saved_time + timedelta(minutes=10)
        print(now,ten_minutes_later,now <= ten_minutes_later)
        if now <= ten_minutes_later:
            db.password_reset_token.delete_one(filter_dict={"token":token})
            return True
        else: return False
    else:
        return False
    
def set_new_password(password:PasswordReset):
    is_valid= verify_password_token(token=password.token)
    admin = find_admin_by_email(email=password.email)
    if is_valid==True:
        change_password_service(user_id=admin['id'],password=password.password)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Otp")
    
    
    
def logout_service(access_token:str):
    a_token = decode_jwt_token_without_expiration(token=access_token)
    db.access_token.delete_one(filter_dict={"id":a_token['token_id']})
    db.refresh_token.delete_many(filter_dict={"previous_access_token":a_token['token_id']})




