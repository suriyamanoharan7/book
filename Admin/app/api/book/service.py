from utils.common_models import Book
from fastapi import HTTPException,status
from datetime import datetime

def create_book_service(request,db):
    new_book = Book(
        title = request.title,
        author = request.author,
        offer_price =request.offer_price,
        price = request.price,
        stock = request.stock,
        description = request.description,
        is_admin = True
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def book_get_id(db,book_id):
    turn = db.query(Book).filter(Book.id == book_id).first()
    if not turn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book doesn't exists.")
    if turn.is_delete == True:
        return False
    return turn


def book_gets(db):
    return db.query(Book).filter(Book.is_delete == False).all()


def book_update_service(db,book_id,request):
    update = book_get_id(db,book_id)
    if update:
        update.title = request.title,
        update.author = request.author,
        update.offer_price =request.offer_price,
        update.price = request.price,
        update.stock = request.stock,
        update.description = request.description
        update.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False


def book_delete_service(db,book_id):
    delete = book_get_id(db,book_id)
    if delete:
        delete.is_delete = True
        db.commit()
        return True
    return False
