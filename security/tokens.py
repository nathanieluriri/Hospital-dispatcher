from security.encrypting_jwt import decode_jwt_token,decode_jwt_token_without_expiration
from core.database import db
from repositories.token_repo import create_access_tokens,create_refresh_tokens
from schemas.token_schema import AccessTokenBase , RefreshTokenBase,TokenOut
import jwt
from fastapi import HTTPException


def validate_access_token(access_token:str):
    decoded_token =decode_jwt_token(access_token)
    print( decoded_token )
    if decoded_token['role']=="user":
        user_details = db.users.find_one(filter_dict={"id":decoded_token['user_id']})
        still_valid = db.access_token.find_one(filter_dict={'id':decoded_token['token_id']})
        if still_valid:
            return user_details
    elif decoded_token['role']=="admin":
        admin_details = db.admins.find_one(filter_dict={"id":decoded_token['user_id']})
        still_valid = db.access_token.find_one(filter_dict={'id':decoded_token['token_id']})
        if still_valid:
            return admin_details


def refresh_access_token(refresh_token:str,access_token:str):
    decoded_refresh_token = decode_jwt_token(token=refresh_token)
    if decoded_refresh_token:
        refresh_token_dict =db.refresh_token.find_one(filter_dict={"id":decoded_refresh_token['token_id']})

        decoded_access_token = decode_jwt_token_without_expiration(access_token)
        if decoded_access_token['role']=="user":
            try:
                if refresh_token_dict['previous_access_token']== decoded_access_token['token_id']:
                    db.access_token.delete_one(filter_dict={"id": decoded_access_token['token_id']})
                    db.refresh_token.delete_one(filter_dict={"id":refresh_token_dict['id']})
                    base_access_token = AccessTokenBase(user_id=refresh_token_dict['user_id'])
                    new_access_token_dict =create_access_tokens(base_access_token)
                    new_access_token = new_access_token_dict['jwt']
                    base_refresh_token = RefreshTokenBase(user_id=refresh_token_dict['user_id'],previous_access_token=new_access_token_dict['access_token_id'])
                    refreshed =create_refresh_tokens(token_data=base_refresh_token)
                    new_token =TokenOut(userId=new_access_token.user_id,accesstoken=new_access_token.access_token,refreshtoken=refreshed.refreshToken)
                    return new_token
                else:
                    raise  HTTPException(status_code=401,detail="Invalid Token")
            except:
                raise  HTTPException(status_code=401,detail="Invalid  Token")
        elif decoded_access_token['role']=="admin":
            try:
                if refresh_token_dict['previous_access_token']== decoded_access_token['token_id']:
                    db.access_token.delete_one(filter_dict={"id": decoded_access_token['token_id']})
                    db.refresh_token.delete_one(filter_dict={"id":refresh_token_dict['id']})
                    base_access_token = AccessTokenBase(user_id=refresh_token_dict['user_id'])
                    new_access_token_dict =create_access_tokens(base_access_token,role="admin")
                    new_access_token = new_access_token_dict['jwt']
                    base_refresh_token = RefreshTokenBase(user_id=refresh_token_dict['user_id'],previous_access_token=new_access_token_dict['access_token_id'])
                    refreshed =create_refresh_tokens(token_data=base_refresh_token)
                    new_token =TokenOut(userId=new_access_token.user_id,accesstoken=new_access_token.access_token,refreshtoken=refreshed.refreshToken)
                    return new_token
                else:
                    raise  HTTPException(status_code=401,detail="Invalid Token")
            except:
                raise  HTTPException(status_code=401,detail="Invalid  Token")
        
    else:
        raise HTTPException(status_code=401,detail="Refresh token has expired")