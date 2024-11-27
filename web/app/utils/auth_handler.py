from datetime import datetime, timedelta
from typing import Optional
import time
import jwt 

REFRESH_SECRET_KEY = "REFRESH_SECRET"
ACCESS_SECRET_KEY = "ACCESS_SECRET"
API_ALGORITHM = "HS256"
API_ACCESS_TOKEN_EXPIRE_MINUTES =  30
API_REFRESH_TOKEN_EXPIRE_MINUTES =  60

def access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt

def refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt

def create_access_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'email': email}
    ac_token = access_token(payload, expires_delta=access_token_expires)
    return ac_token


def create_refresh_token(email):
    payload = {'email': email}
    expires = timedelta(minutes=API_REFRESH_TOKEN_EXPIRE_MINUTES)
    return refresh_token(payload, expires_delta=expires)

def decodeJWT(token: str) -> dict:
    decode_token = jwt.decode(token,ACCESS_SECRET_KEY, algorithms=[API_ALGORITHM])
    expires = decode_token.get("exp")
    if expires >= time.time():
        return decode_token
   
def JWTdecode(token: str) -> dict:
    decode_token = jwt.decode(token,REFRESH_SECRET_KEY, algorithms=[API_ALGORITHM])
    expires = decode_token.get("exp")
    if expires >= time.time():
        return decode_token