from core.database import db
from schemas.token_schema import AccessTokenOut,AccessTokenCreate,AccessTokenBase
from typing import Literal

def create_access_tokens(token_data:AccessTokenBase,role:Literal["admin", "user",]="user")->AccessTokenOut:
    token = AccessTokenCreate(user_id=token_data.user_id,role=role)
    result = db.access_token.insert_one(token.model_dump())
    tokn =  db.access_token.find_one({"id":result})

    accessToken = AccessTokenOut(**tokn)
    return accessToken 


    
# def create_refresh_tokens(token_data:refreshTokenCreate)->refreshTokenOut:
#     token = token_data.model_dump()
#     result = await db.refreshToken.insert_one(token)
#     tokn = await db.refreshToken.find_one({"_id":result.inserted_id})
#     refreshToken = refreshTokenOut(**tokn)
#     return refreshToken