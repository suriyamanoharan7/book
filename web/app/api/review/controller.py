from api.review.schema import *
from api.review.service import *
from fastapi import HTTPException,status
from utils.auth_handler import  decodeJWT
from api.user.model import User

def create_review_controller(book_id,request,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user.role_id ==1:
        data = cretae_review_service(book_id,request,db,user)
        return {"success":True,"records":data}
    else:
        return {"success":False,"message":"You have no permission to review the books"}
    
def get_reviews_controller(book_id,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user.role_id ==1 or user.role_id ==2:
        data = get_reviews_service(book_id,db)
        return {"success":True,"records":data}
    else:
        return {"success":False,"message":"You have no permission to review the books"}
    
def get_review_controller(book_id,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user.role_id ==1 or user.role_id ==2:
        data = get_review_service(book_id,db,user)
        return {"success":True,"records":data}
    else:
        return {"success":False,"message":"You have no permission to review the books"}

def update_reviews_by_book(book_id,request,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user.role_id ==1:
        data = updates_reviews_service(book_id,request,db,user)
        return {"success":True,"records":data}
    else:
        return {"success":False,"message":"You have no permission to review the books"}

def delete_review_controller(book_id,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user.role_id ==1:
        data = delete_reviews_service(book_id,db,user)
        return {"success":True,"records":data}
    else:
        return {"success":False,"message":"You have no permission to review the books"}
