from core.database import db
from schemas.admin_schema import AdminBase,AdminOut,NewAdminCreate,UserType,RegisteredAdmin
from security.hash import hash_password

def create_admin(user_data:AdminBase):
    user_dict = user_data.model_dump()
    data= NewAdminCreate(**user_dict)
    user_id = db.admins.insert_one(data.model_dump()) 
    return user_id


   
def find_admin_by_email(user_data:RegisteredAdmin):
    admin_details = db.admins.find_one(filter_dict={"email":user_data.email})
    return admin_details


def delete_admin_by_id(user_id:int):
    db.admin.delete_one({"id":user_id})
    
def update_password(user_id:int,password:str):
    hashed_password =hash_password(password=password)
    db.users.update_one(filter_dict={"id":user_id},data={"hashed_password":hashed_password})  
    