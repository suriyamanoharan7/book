from api.admin.service import * 
from api.admin.schema import *
from fastapi import HTTPException
from utils.auth_handler import create_access_token,create_refresh_token
from utils.auth_handler import decodeJWT


# To login as an admin
def admin_login_controller(db,email,password):
    """test"""
    # login admin detail validation
    login = admin_validate(db,email,password)
    if login:
        access_token = create_access_token(email,"admin")
        refresh_token = login.refresh_token
        if access_token:
            return {"success": True,"message":"login Successfully","token_type": "bearer","access_token": access_token,"refresh_token":refresh_token}
        else:
            raise HTTPException(status_code=400, detail={"message":"You not valid person","success":False})
    else:
        raise HTTPException(status_code=404, detail={"message": "Account doesn't exist. Enter a different account or create new account","success":False})

def admin_refresh_controller(db,token):
    # login admin detail validation
    login = admin_token_validate(db,token)
    if login:
        access_token = create_access_token(login.email,"admin")
        refresh_token = create_refresh_token(login.email,"admin")
        # To update refresh token
        refresh_admin = refresh_update_token(db,token,refresh_token)
        return {"success": True,"message":"login Successfully","admin record": refresh_admin,"access_token": access_token}
    else:
        raise HTTPException(status_code=404, detail={"message": "please enter a valid token","success":False})




def admin_create_controller(request:Adminformat,db):
    try:
        access_token = create_access_token(request.email,"admin")
        refresh_token = create_refresh_token(request.email,"admin")
        token = admin_create_service(request,db,refresh_token)
    
        return {"success": True,"message":"Account created Successfully","records": token,"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=404, detail={"message": "cannot create new account","success":False,"error":f"{e}"})


def admin_update_controller(database,admin_id,ad:Adminformat,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        valide_update = admin_update_service(database,admin_id,ad)
        if valide_update:
            return {"success": True,"message":"updated successfully","records":valide_update}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
def admin_update_password_controller(db, admin_id, ad,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        valide_update = admin_update_password_service(db,admin_id,ad)
        if valide_update:
            return {"success": True,"message":"updated successfully","records":valide_update}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist. Enter a different account or create new account"})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")


def admin_gets_controller(db,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        data = admin_gets_service(db)
        if data:
            return {"success": True,"records":data}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token")
    


def admin_get_controller(db,admin_id,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        token = admin_get_by_id(db,admin_id)
        if token:
            return {"success": True,"records":token}
        else:
            raise HTTPException(status_code=404, detail={"success":False,'message':"Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    
def admin_delete_controller(db,admin_id,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        valide_delete = admin_delete_service(db,admin_id)
        if valide_delete:
            return {"success": True,"message":"deleted Successfully"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "Account doesn't exist."})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
 
def get_admin_sales_report_controller(start_date,end_date,db,tokens):
    check = decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        total_sales= get_admin_sales_report_service(start_date, end_date, db)
        if total_sales:
            return {"success": True,"total_sales": total_sales}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "No sales on that month"})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    

def get_top_customers_controller(db,tokens):
    check =decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        top_customers = get_top_customers_service(db)
        if top_customers:
            return {"success": True,"records":f"top 5 customers :{top_customers}"}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "No  top customers on that month"})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")


def get_top_selling_books_controller(limit,db,tokens):
    check =decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        top_selling_books = get_top_selling_books_service(limit,db)
        if top_selling_books:
            return {"success": True,"top_selling_books": top_selling_books}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "No top selling books "})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")
    

def get_top_rated_books_controller(limit, db,tokens):
    check =decodeJWT(tokens)
    admin = check.get("role")
    if admin == 'admin':
        top_rated_books = get_top_rated_books_service(limit, db)
        if top_rated_books:
            return {"success": True,"top_rated_books": top_rated_books}
        else:
            raise HTTPException(status_code=404, detail={"success": False,'message': "No top rated books "})
    else:
        raise HTTPException(status_code=403,detail="Invalid token or expired token")