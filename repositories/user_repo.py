from core.database import db
from schemas.user_schema import NewUserCreate,UserBase,UserOut,user_type


def create_user(user_data:UserBase):
    user_dict = user_data.model_dump()
    data= NewUserCreate(**user_dict)
    user_id = db.users.insert_one(data.model_dump()) 
    return user_id


   
# update_user_profile
# replace_password
# get_user_by_userId
# get_user_by_email


user_data = UserBase(username="nattyboi",user_type=user_type.Patients,email="uririnathaniel@gmail.com", hashed_password="helloo")

