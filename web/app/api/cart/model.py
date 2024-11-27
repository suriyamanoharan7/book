from configuration.config import *
from sqlalchemy import String,Integer,Column,ForeignKey,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from utils.common_models import *


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, unique=True) 
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)  
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="carts")
    book = relationship("Book", back_populates="carts")
