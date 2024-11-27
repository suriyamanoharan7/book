from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from configuration.config import *

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    review = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime,)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean,default=False)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
