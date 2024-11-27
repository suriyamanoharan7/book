from api.user.service import * 
from api.user.schema import *
from fastapi import HTTPException
from utils.auth_handler import decodeJWT
   

# def approve_publisher_controller(publisher_id,db,tokens):
#     check = decodeJWT(tokens)
#     admin = check.get("role")
#     if admin == 'admin':
#         valide_data = approve_publisher_service(publisher_id,db)
#         if valide_data:
#             return {"success": True,"records":valide_data}
#         else:
#             raise HTTPException(status_code=404, detail={"success": False,'message': "Request doesn't exist."})
#     else:
#         raise HTTPException(status_code=403,detail="Invalid token or expired token")
    


def user_create_controller(db,request:UserCreate,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        valide_data = user_create_service(db,request)
        if valide_data:
            return {"success": True,"message":"Account created Successfully","records":valide_data}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Cannot create user."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
  

# To update user details by user ID
def user_update_controller(db,user_id,request:UserCreate,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    print(admin)
    if admin == 'admin':
        
        update_user = user_update_service(db,user_id,request)
        print(update_user)
        if update_user == True:
            return {"success": True,"message":"updated successfully","records":update_user}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"}) 
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")  
    
# To retrieve all user's details
def user_gets_controller(db,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin == "admin":
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
    admin=check.get('role')
    if admin == "admin":
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
    admin = check.get('role')
    if admin =="admin":
        delete_user = user_delete_service(db,user_id)
        if delete_user == True:
            return {"success": True,"message":"deleted Successfully"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    


def  get_all_publisher_requests_controller(db,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin =="admin":
        return get_all_publisher_requests_service(db)
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")


def approve_publisher_request_controller(db, user_id,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin =="admin":
        return approve_publisher_request_service(db, user_id)
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")

def deactivate_customer_controller(customer_id, db,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin =="admin":
        return deactivate_customer_service(customer_id, db)
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")