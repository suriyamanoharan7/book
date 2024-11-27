from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.auth_handler import decodeJWT,JWTdecode



class AdminJWT(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AdminJWT,self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(AdminJWT, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Not a right token")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Token Missing")
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken) 
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    

class UserJWT(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(UserJWT,self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(UserJWT, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Not a right token")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Token Missing")
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            load = JWTdecode(jwtoken)
        except:
            load = None
        if load:
            isTokenValid = True
        return isTokenValid