from core.database import db
from schemas.user_schema import NewUserCreate,UserBase,RegisteredUser,UpdateUser
from security.hash import hash_password


def create_user(user_data:UserBase):
    user_dict = user_data.model_dump()
    data= NewUserCreate(**user_dict)
    user_id = db.users.insert_one(data.model_dump()) 
    return user_id

def find_user_by_email(email:str):
    user_details = db.users.find_one(filter_dict={"email":email})
    return user_details

def find_user_by_id(user_id:int):
    user_details = db.users.find_one(filter_dict={"id":user_id})
    return user_details
   
def delete_user_by_id(user_id:int)->int:
    return db.users.delete_one({"id":user_id})
    
def update_password(user_id:int,password:str)->int:
    hashed_password =hash_password(password=password)
    return db.users.update_one(filter_dict={"id":user_id},data={"hashed_password":hashed_password})  
    
def update_user_details(user_id:int,update_data:UpdateUser)->int:
    return db.users.update_one(filter_dict={"id":user_id},data=update_data.model_dump(exclude_none=True))




