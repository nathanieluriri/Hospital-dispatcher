from core.database import db
from schemas.token_schema import AccessTokenOut,AccessTokenCreate,AccessTokenBase,RefreshTokenBase,RefreshTokenOut
from typing import Literal

def create_access_tokens(token_data:AccessTokenBase,role:Literal["admin", "user",]="user"):
    token = AccessTokenCreate(user_id=token_data.user_id,role=role)
    result = db.access_token.insert_one(token.model_dump())
    tokn =  db.access_token.find_one({"id":result})
    
    accessToken = AccessTokenOut(**tokn)
    return {"jwt":accessToken,"access_token_id":result }


    
def create_refresh_tokens(token_data:RefreshTokenBase)->RefreshTokenOut:
    token = token_data.model_dump()
    result = db.refresh_token.insert_one(token)
    tokn =  db.refresh_token.find_one({"id":result})
    refreshToken = RefreshTokenOut(**tokn)
    return refreshToken