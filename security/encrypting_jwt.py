import jwt
import datetime
from datetime import timezone
from core.database import db
from schemas.token_schema import AccessTokenCreate
from functools import lru_cache

@lru_cache()
def get_secret_dict()->dict:
    result =db.secret_keys.find_one({"id":1})
    result.pop('id')
    return result



def get_secret_and_header():
    
    import random
    
    secrets =  get_secret_dict()
    
    random_key = random.choice(list(secrets.keys()))
    random_secret = secrets[random_key]
    SECRET_KEYS={random_key:random_secret}
    HEADERS = {"kid":random_key}
    result = {
        "SECRET_KEY":SECRET_KEYS,
        "HEADERS":HEADERS
    }
    
    return result



def create_jwt_token(token:AccessTokenCreate):
    """function generates a JWT (JSON Web Token) for a member, using dynamic secret keys and a key ID (kid) for key rotation support.

    Args:
        token (AccessTokenCreate): AccessTokenCreate Object

    Returns:
        token: Returns the signed JWT token
    """
    secrets = get_secret_and_header()
    SECRET_KEYS= secrets['SECRET_KEY']
    headers= secrets['HEADERS']
    
    payload = {
        'user_id': token.user_id,
        'role':token.role,
      
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=20)
    }
    
    
    token = jwt.encode(payload, SECRET_KEYS[headers['kid']], algorithm='HS256', headers=headers)

    return token


async def decode_jwt_token(token):
    
    """function verifies and decodes a JWT (JSON Web Token) using a dynamic secret identified by the token’s kid (key ID) in the header. It supports secret rotation and handles common token errors.

    Args:
        token (jwt): the jwt token used

    Raises:
        Exception: expired token or invalid signature

    Returns:
        if decoded true: {'accessToken': '682c99f395ff4782fbea010f', 'role': 'admin',created_at: , 'exp': 1747825460}
    """
    SECRET_KEYS =  get_secret_dict()
    # Decode header to extract the `kid`
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header['kid']

    # Look up the correct key
    key = SECRET_KEYS.get(kid)

    if not key:
        raise Exception("Unknown key ID")

    # Now decode and verify
    try:
        decoded = jwt.decode(token, key, algorithms=['HS256'])
        return decoded
    except jwt.exceptions.ExpiredSignatureError:
        print("expired token")
        return None
    except jwt.exceptions.InvalidSignatureError:
        print("invalid signature")
        return None

async def decode_jwt_token_without_expiration(token):
    """This async function decodes and verifies a JWT, but with one key difference:
👉 If the token is expired, it still decodes the payload by explicitly skipping the expiration check.

    Args:
        token (jwt): the jwt token used

    Raises:
        Exception: expired token or invalid signature

    Returns:
        if_decoded_true: {'accessToken': '682c99f395ff4782fbea010f', 'role': 'admin',created_at: , 'exp': 1747825460}
    """
    SECRET_KEYS =  get_secret_dict()
    # Decode header to extract the `kid`
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header['kid']

    # Look up the correct key
    key = SECRET_KEYS.get(kid)

    if not key:
        raise Exception("Unknown key ID")

    # Now decode and verify
    try:
        decoded = jwt.decode(token, key, algorithms=['HS256'])
        return decoded
    except jwt.exceptions.ExpiredSignatureError:
        print("expired token")
        payload = decoded = jwt.decode(token, key, algorithms=['HS256'],options={"verify_exp": False})
        return payload
    except jwt.exceptions.InvalidSignatureError:
        print("invalid signature")
        return None





