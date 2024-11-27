from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email : EmailStr
    password :str
    role_id :int

class UserBase(BaseModel):
    id: int
    username: str
    role_id: int

    class Config:
        from_attributes = True

class PublisherBase(BaseModel):
    id: Optional[int]
    user_id: int
    name: Optional[str]
    is_approved: bool = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PublisherRequestResponse(BaseModel):
    user: UserBase
    publisher: Optional[PublisherBase]  

    class Config:
        from_attributes = True

class ApprovePublisher(BaseModel):
    user_id: int
    class Config:
        from_attributes = True