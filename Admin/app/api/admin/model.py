from sqlalchemy import Integer, String,Column,Boolean,DateTime
from configuration.config import *
from datetime import datetime


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    refresh_token = Column(String)
    is_active = Column(Boolean, default=True)