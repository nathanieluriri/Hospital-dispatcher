from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security.tokens import validate_access_token
from security.encrypting_jwt import decode_jwt_token

token_auth_scheme = HTTPBearer()

def verify_token(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    access_token = token.credentials
    result = validate_access_token(access_token=access_token)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    decoded_token = decode_jwt_token(access_token)

    return {
        "user": result,
        "token": access_token,
        "role": decoded_token.get("role")
    }

def verify_admin_token(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    verified = verify_token(token)
    if verified["role"] == "admin":
        return verified
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized Access Token"
    )

def verify_user_token(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    verified = verify_token(token)
    if verified["role"] == "user":
        return verified
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized Access Token"
    )
