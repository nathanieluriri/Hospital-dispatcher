from schemas.general_imports import *


class refreshedTokenRequest(BaseModel):
    refreshToken:str
    
class refreshedToken(BaseModel):
    userId:int
    dateCreated:Optional[str]=datetime.now(timezone.utc).isoformat()
    refreshToken:str
    accessToken:int
    @model_validator(mode='before')
    def set_dates(cls,values):
        now_str = datetime.now(timezone.utc).isoformat()
        values['dateCreated']= now_str
        return values

class AccessTokenBase(BaseModel):
    user_id:int

class AccessTokenCreate(AccessTokenBase):
    role:str

class AccessTokenOut(AccessTokenCreate):
    access_token: Optional[str] =None
    created_at:Optional[str]=None
    @model_validator(mode='before')
    def set_values(cls,values):
        from security.encrypting_jwt import create_jwt_token
        if values is None:
            values = {}
        values['access_token']= create_jwt_token(token=AccessTokenCreate(user_id=values['user_id'],role=values['role']))
        return values
    
class refreshTokenBase(BaseModel):
    userId:str
    previousAccessToken:str
  
class refreshTokenCreate(refreshTokenBase):
    dateCreated:Optional[str]=datetime.now(timezone.utc).isoformat()
    @model_validator(mode='before')
    def set_dates(cls,values):
        now_str = datetime.now(timezone.utc).isoformat()
        values['dateCreated']= now_str
        return values

    
class refreshTokenOut(refreshTokenCreate):
    refreshtoken: Optional[str] =None
    @model_validator(mode='before')
    def set_values(cls,values):
        if values is None:
            values = {}
        values['refreshtoken']= str(values.get('_id'))
        return values
    
    model_config = {
        'populate_by_name': True,
        'arbitrary_types_allowed': True,
    }


class TokenOut(BaseModel):
    userId:str
    accesstoken: Optional[str] =None
    refreshtoken: Optional[str] =None
    dateCreated:Optional[str]=datetime.now(timezone.utc).isoformat()
    @model_validator(mode='before')
    def set_dates(cls,values):
        now_str = datetime.now(timezone.utc).isoformat()
        values['dateCreated']= now_str
        return values    



class refreshTokenRequest(BaseModel):
    refreshToken:str