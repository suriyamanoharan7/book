from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean,JSON,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from configuration.config import *
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(JSON) 
    quantity = Column(JSON) 
    order_type = Column(String)  
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_value = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")