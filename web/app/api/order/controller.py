from api.order.service import *
from api.order.schema import *
from fastapi import HTTPException,status
from utils.auth_handler import decodeJWT
from api.user.model import User

def direct_order_book_controller(request,db,tokens):
    check = decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
    else:
        if user.role_id ==1:
            data = direct_order_book_service(request,db,user)
            return {"success":True,"records":data}
        else:
            return {"success":False,"message":"You have no permission to Purchase the books"}
        

def cart_order_book_controller(db,tokens):
    check =decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
    else:
        if user.role_id ==1:
            data = cart_order_book_service(db,user)
            return {"success":True,"records":data}
        else:
            return {"success":False,"message":"You have no permission to Purchase the books"}
        
def get_order_history_controller(db,tokens):
    check =decodeJWT(tokens)
    user_email = check.get('email')
    user = db.query(User).filter(User.email==user_email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
    else:
        if user.role_id ==1:
            data = get_order_history_service(db,user)
            return {"success":True,"records":data}
        else:
            return {"success":False,"message":"You have no permission to Purchase the books"}