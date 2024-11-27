from api.book.service import *
from api.book.schema import *
from fastapi import HTTPException,status
from utils.auth_bearer import decodeJWT
from api.user.model import User
from utils.common_models import *


def create_book_controller(request,db,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    publisher = db.query(Publisher).filter(Publisher.user_id ==user.id).first()
    if publisher:
        valide_data= create_book_service(request,db,publisher)
        return {"success": True,"message":"Book created Successfully","records":valide_data}
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")


# To update user details by user ID
def book_update_controller(db,book_id,request,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    publisher = db.query(Publisher).filter(Publisher.user_id ==user.id).first()
    if publisher:
        
        update_book = book_update_service(db,book_id,request,publisher)
    
        if update_book == True:
            return {"success": True,"message":"updated successfully","records":update_book}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"}) 
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")  
    
# To retrieve all user's details
def book_gets_controller(db,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1 or user.role_id ==2:
        data = book_gets(db)
        if data:
            return {"success": True,"records":data}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Book doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
# To retrieve a single user's details by userID
def book_get_controller(db,book_id,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1 or user.role_id ==2:
        token = book_get_id(db,book_id)
        if token:
            return {"success": True,"records":token}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Book doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
# to delete a single user details by ID
def book_delete_controller(db,book_id,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    publisher = db.query(Publisher).filter(Publisher.user_id ==user.id).first()
    if publisher:
        delete_book = book_delete_service(db,book_id)
        if delete_book == True:
            return {"success": True,"message":"deleted Successfully"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
   