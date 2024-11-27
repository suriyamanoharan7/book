from sqlalchemy import String,Column,Integer,ForeignKey,Float,Boolean,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from configuration.config import *

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=True)
    offer_price = Column(Float)
    stock = Column(Integer, default=0)
    price = Column(Float, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False) 
    is_admin = Column(Boolean) 
    avg_rating = Column(Float, default=0.0)
    is_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    publisher = relationship("Publisher", back_populates="books")
    carts =relationship("Cart",back_populates='book')
    reviews = relationship("Review",back_populates='book')
