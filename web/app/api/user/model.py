from configuration.config import *
from sqlalchemy import String,Integer,Column,ForeignKey,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from utils.common_models import *

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    is_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    refresh_token = Column(String)

    role = relationship("Role", back_populates="users")
    publisher = relationship("Publisher", back_populates="user", uselist=False)
    carts = relationship("Cart", back_populates="user")
    orders= relationship("Order",back_populates='user')
    reviews= relationship("Review",back_populates='user')
    
 