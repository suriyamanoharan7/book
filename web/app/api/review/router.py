from utils.auth_bearer import UserJWT
from api.review.model import get_db
from fastapi import APIRouter ,Depends
from api.review.controller import *
from sqlalchemy.orm import Session

router = APIRouter(tags=["Review"])
https_bearer = UserJWT()

@router.post("/books/{book_id}/review")
async def create_review_to_books(book_id:int,request:ReviewCreate,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return create_review_controller(book_id,request,db,tokens)


@router.get("/books/{book_id}/reviews")
async def get_reviews_by_books(book_id:int,db:Session=Depends(get_db),tokens:str =Depends(https_bearer)):
    return get_reviews_controller(book_id,db,tokens)

@router.get('/books/{book_id}/reviews/{user_id}')
async def get_review(book_id:int,db:Session=Depends(get_db),tokens:str = Depends(https_bearer)):
    return get_review_controller(book_id,db,tokens)


@router.put("/books/{book_id}/review")
async def update_review_to_books(book_id:int,request:ReviewCreate,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return update_reviews_by_book(book_id,request,db,tokens)

@router.delete("/books/{book_id}/review")
async def delete_review_book(book_id: int, db: Session = Depends(get_db),tokens:str=Depends(https_bearer)):
    return delete_review_controller(book_id,db,tokens)