from schemas.general_imports import *

class AccessTokenBase(BaseModel):
    
    user_id:int

class AccessTokenCreate(AccessTokenBase):
    role:str
    
class AccessTokenProper(AccessTokenBase):
    id:int
    role:str


class AccessTokenOut(AccessTokenProper):
    access_token: Optional[str] =None
    created_at:Optional[str]=None
    id:int

    @model_validator(mode='before')
    def set_values(cls,values):
        from security.encrypting_jwt import create_jwt_token
        if values is None:
            values = {}
        jwt_token = AccessTokenProper(id=values['id'],user_id=values['user_id'],role=values['role'])
        values['access_token']= create_jwt_token(token=jwt_token)
        return values
    
class RefreshTokenBase(BaseModel):
    user_id:int
    previous_access_token:int
  

class RefreshTokenOut(RefreshTokenBase):
    id:int
    refreshToken:Optional[Any]=None
    @model_validator(mode='after')
    def set_values(self):
        from security.encrypting_jwt import create_jwt_token
        self.refreshToken= create_jwt_token(token=AccessTokenProper(id=self.id,user_id=self.user_id,role="refresh_token"))
        return self
    

class TokenOut(BaseModel):
    userId:int
    accesstoken: Optional[str] =None
    refreshtoken: Optional[str] =None
 


class ResfreshingToken(BaseModel):
    refresh_token:str