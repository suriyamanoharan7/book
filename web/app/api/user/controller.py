from api.user.service import * 
from api.user.schema import *
from fastapi import HTTPException
from utils.auth_handler import decodeJWT
from utils.auth_handler import create_access_token,create_refresh_token


def user_login_controller(db,email,password):
   
    login = login_validate(db,email,password)
    if login:
        access_token = create_access_token(email)
        refresh_token = login.refresh_token
        return {"success": True,"message":"login Successfully","token_type": "bearer","access token": access_token,"refresh token": refresh_token}
    else:
        raise HTTPException(status_code=404, detail={"message": "Account doesn't exist. Enter a different account or create new account","success":False})


# To re-login with refresh token by user
def user_refresh_controller(db,token):
    login = login_token_validate(db,token)
    if login:
        access_token = create_access_token(login.email)
        refresh_token = create_refresh_token(login.email)
        refresh_admin = refresh_update_token(db,token,refresh_token)
        return {"success": True,"message":"login Successfully","admin record": refresh_admin,"access_token": access_token}
    else:
        raise HTTPException(status_code=404, detail={"message": "please enter a valid token","success":False})


def user_create_controller(db,request:UserCreate):
    try:
        access_token = create_access_token(request.email)
        refresh_token = create_refresh_token(request.email)
        valide_data = user_create_service(db,request,refresh_token)
        if valide_data:
            return {"success": True,"message":"Account created Successfully","records":valide_data,"access_token":access_token}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Cannot create user."})
    except Exception as e:
        raise HTTPException(status_code=403,detail=f"Invalid token or expired token {e}")
  

# To update user details by user ID
def user_update_controller(db,user_id,request:UserCreate,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1:
        update_user = user_update_service(db,user_id,request)
        if update_user == True:
            return {"success": True,"message":"updated successfully","records":update_user}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"}) 
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")  
    
# To retrieve all user's details
def user_gets_controller(db,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1:
        data = user_gets(db)
        if data:
            return {"success": True,"records":data}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
# To retrieve a single user's details by userID
def user_get_controller(db,user_id,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1:
        token = user_get_id(db,user_id)
        if token:
            return {"success": True,"records":token}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
# to delete a single user details by ID
def user_delete_controller(db,user_id,tokens):
    check = decodeJWT(tokens)
    role = check.get("email")
    user =db.query(User).filter(User.email== role).first()
    if user.role_id == 1:
        delete_user = user_delete_service(db,user_id)
        if delete_user == True:
            return {"success": True,"message":"deleted Successfully"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
