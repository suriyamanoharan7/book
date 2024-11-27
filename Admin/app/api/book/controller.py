from api.book.service import *
from api.book.schema import *
from fastapi import HTTPException,status
from utils.auth_bearer import decodeJWT

def create_book_controller(request,db,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin == "admin":
        valide_data= create_book_service(request,db)
        return {"success": True,"message":"Book created Successfully","records":valide_data}
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")


# To update user details by user ID
def book_update_controller(db,book_id,request,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        
        update_book = book_update_service(db,book_id,request)
    
        if update_book == True:
            return {"success": True,"message":"updated successfully","records":update_book}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"}) 
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")  
    
# To retrieve all user's details
def book_gets_controller(db,tokens):
    check = decodeJWT(tokens)
    admin = check.get('role')
    if admin == "admin":
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
    admin=check.get('role')
    if admin == "admin":
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
    admin = check.get('role')
    if admin =="admin":
        delete_book = book_delete_service(db,book_id)
        if delete_book == True:
            return {"success": True,"message":"deleted Successfully"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
   