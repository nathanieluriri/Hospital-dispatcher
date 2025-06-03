from core.database import db
from schemas.admin_schema import AdminBase,AdminOut,NewAdminCreate,user_type


def create_admin(user_data:AdminBase):
    user_dict = user_data.model_dump()
    data= NewAdminCreate(**user_dict)
    user_id = db.admins.insert_one(data.model_dump()) 
    return user_id


   