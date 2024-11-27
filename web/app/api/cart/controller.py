from api.cart.service import *
from api.cart.schema import *
from fastapi import HTTPException
from utils.auth_handler import decodeJWT


def cart_create_controller(request,db,tokens):
    check = decodeJWT(tokens)
    email = check.get('email')
    user = db.query(User).filter(User.email== email).first()
    if user.role_id == 1:
        data = cart_create_service(request,db,user)
        return {"success":True,'records':data}
    else:
        return {"success":False,"message":"You Can't create a cart"}

def get_cart_controller(user_id,db,tokens):
    check =decodeJWT(tokens)
    email = check.get('email')
    user_email = db.query(User).filter(User.email ==email).first()
    if user_email.id == user_id:

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
        if user.role_id ==1:
            data = get_cart_service(user_id,db)
            return {"success":True,"records":data}
        else:
            return {"success":False,"message":"Invalid Token"}
    else:
        return {"success":False,"message":"You did not see the other user cart"}


def update_cart_controller(cart_id,request,db,tokens):
    check =decodeJWT(tokens)
    email = check.get('email')
    user = db.query(User).filter(User.email ==email).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if cart is None:
        return {"success":False,"message":"You did not edit the other user cart"}
    else:
        if user.role_id ==1:
            data = update_cart_service(cart_id,request,db)
            return {"success":data,"message":'Updated successfully'}
        else:
            return {"success":False,"message":"You did not have a permission to edit cart"}

def delete_cart_controller(cart_id,db,tokens):
    check =decodeJWT(tokens)
    email = check.get('email')
    user = db.query(User).filter(User.email ==email).first()
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if cart is None:
        return {"success":False,"message":"You did not delete the other user cart"}
    else:
        if user.role_id ==1:
            data = delete_cart_service(cart_id,db)
            return {"success":data,"message":'Deleted successfully'}
        else:
            return {"success":False,"message":"You did not have a permission to delete cart"}