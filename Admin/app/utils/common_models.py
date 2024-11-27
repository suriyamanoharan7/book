from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime,JSON,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from configuration.config import *  
from enum import Enum as PyEnum
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
    orders = relationship("Order",back_populates="user")
    reviews= relationship("Review",back_populates='user')


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
    reviews = relationship("Review",back_populates='book')



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