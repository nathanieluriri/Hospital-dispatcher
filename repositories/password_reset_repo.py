from core.database import db
from schemas.password_reset_schema import PasswordResetTokenCreate,PasswordResetBase,PasswordReset
import random
from fastapi import HTTPException,status
from schemas.success_response_schema import APISuccessResponse
from services.email_service import send_change_of_password_otp_email
from services.user_service import change_password_service

def generate_random_six_integers_as_string(min_val=0, max_val=9, separator=""):

  if min_val > max_val:
    raise ValueError("min_val cannot be greater than max_val")

  random_integers = [random.randint(min_val, max_val) for _ in range(6)]

  # Convert each integer to a string and join them with the specified separator
  return separator.join(map(str, random_integers))

def create_password_reset_token(user_data:PasswordResetBase):
    OTP=generate_random_six_integers_as_string()
    user_details = db.users.find_one(filter_dict={"email":user_data.email})
    if user_details:
        password_reset_token = PasswordResetTokenCreate(user_id=user_details['id'],token=OTP)
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
    user = db.users.find_one(filter_dict={"email":password.email})
    if is_valid==True:
        change_password_service(user_id=user['id'],password=password.password)
 
         
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Otp")