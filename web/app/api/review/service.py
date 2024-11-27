from api.review.model import Review
from api.order.model import Order
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import cast
from sqlalchemy.orm import Session
from api.book.service import book_get_id

def cretae_review_service(book_id,request,db,user):
    order = db.query(Order).filter(
        Order.user_id == user.id,
        cast(Order.book_id, JSONB).op("@>")([book_id])
    ).first()
    if not order:
        raise HTTPException(
            status_code=403,
            detail="You can only review books you have purchased."
        )

    existing_review = db.query(Review).filter(
        Review.user_id == user.id,
        Review.book_id == book_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400,detail="You have already reviewed this book.")
    new_review = Review(
        user_id=user.id,
        book_id=book_id,
        review=request.review,
        rating=request.rating,
    )
    db.add(new_review)
    
    db.commit()
    update_book_rating(db, book_id)
    db.refresh(new_review)

    return new_review

def get_reviews_service(book_id,db):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this book.")
    return reviews

def get_review_service(book_id,db,user):
    review = db.query(Review).filter(Review.book_id == book_id,Review.user_id ==user.id,Review.is_deleted==False).first()
    if not review:
        raise HTTPException(status_code=404, detail=f"No reviews found for this book by {user.name}.")
    return review


def updates_reviews_service(book_id,request,db,user):
    order = db.query(Order).filter(
            Order.user_id == user.id,
            cast(Order.book_id, JSONB).op("@>")([book_id])
        ).first()
    if not order:
        raise HTTPException(status_code=403, detail="You can only update reviews for books you have purchased.")
    existing_review = db.query(Review).filter(
        Review.user_id == user.id,
        Review.book_id == book_id
    ).first()

    if not existing_review:
        raise HTTPException(status_code=404, detail="Review not found.")

    existing_review.review = request.review
    existing_review.rating = request.rating
    db.commit()
    update_book_rating(db, book_id)
    db.refresh(existing_review)

    return existing_review

def  delete_reviews_service(book_id,db,user):
    review = db.query(Review).filter(
        Review.book_id == book_id,
        Review.user_id == user.id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")

    review.is_deleted=True
    db.commit()

    return True

def calculate_average_rating(db: Session, book_id: int):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews: 
        return 0.0

    total_rating = sum(review.rating for review in reviews)
    avg_rating= total_rating / len(reviews)

    return avg_rating

def update_book_rating(db: Session, book_id: int):
    book = book_get_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    average_rating = calculate_average_rating(db, book_id)
    book.avg_rating = average_rating
    db.commit()
    db.refresh(book)
    return book