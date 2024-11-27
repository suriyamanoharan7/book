from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from configuration.config import *  

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    role = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    users = relationship("User", back_populates="role")



class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name =Column(String, nullable=False)
    is_approved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="publisher")
    books = relationship("Book", back_populates="publisher")
