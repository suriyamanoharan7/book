from api.cart.model import Cart
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from datetime import datetime
from api.user.model import User
from api.book.model import Book

def cart_create_service(request,db,user):
    book = db.query(Book).filter(Book.id==request.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Id Not Found")
    new_cart =Cart(
        user_id= user.id,
        book_id = book.id,
        quantity = request.quantity
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


def get_cart_id(cart_id,db):
    return db.query(Cart).filter(Cart.id == cart_id).first()

def get_cart_service(user_id,db):
    carts = db.query(Cart).filter(Cart.user_id== user_id,Cart.is_deleted == False).all()
    return [
        {
        "book_id":cart.book_id,
        "quantity":cart.quantity,
        "book_details": {
                "title": cart.book.title,
                "author": cart.book.author,
                "price": cart.book.price,
                "description": cart.book.description,
            }
        }
        for cart in carts
        ]

def update_cart_service(cart_id,request,db):
    cart = get_cart_id(cart_id,db)
    if cart:
        cart.quantity = request.quantity,
        cart.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

def delete_cart_service(cart_id,db):
    cart = get_cart_id(cart_id,db)
    if cart:
        cart.is_deleted = True
        db.commit()
        return True
    return False
