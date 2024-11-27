from pydantic import BaseModel,EmailStr,conint
from typing import Optional
 

class Adminformat(BaseModel):
    name: Optional[str] = None 
    email:Optional[EmailStr] = None 
    password:Optional[str] = None 
    class Config:
        json_schema_extra={
            "example":{
                "name":"Admin",
                "email":"admin@gmail.com",
                "password":"Admin12@"
            }
        }

class AdminLogin(BaseModel):
    email:Optional[EmailStr] = None 
    password:Optional[str] = None  
    class Config:
        json_schema_extra={
            "example":{
                "email":"admin@gmail.com",
                "password":"Admin12@"
            }
        }

class Adminpassword(BaseModel):
    password :str
