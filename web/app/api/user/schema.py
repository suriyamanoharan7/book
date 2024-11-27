from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email : EmailStr
    password :str
    role_id :int

class UserLogin(BaseModel):
    email: EmailStr
    password : str
