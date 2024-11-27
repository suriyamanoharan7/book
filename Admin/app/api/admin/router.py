from fastapi import APIRouter,Depends
from api.admin.controller import *
from api.admin.model import get_db
from sqlalchemy.orm import Session
from utils.auth_bearer import AdminJWT


router = APIRouter(prefix='/admin')

# Authenticate and Authorize by token
https_bearer = AdminJWT()

# To login as an admin
@router.post("/login",tags=["Auth"])
async def admin_login_router(ad: AdminLogin, database: Session = Depends(get_db)):
    return  admin_login_controller(database, ad.email, ad.password)

# To re-login with refresh token by admin
@router.post("/re-login",tags=["Auth"])
async def admin_refresh_router(token: str, database: Session = Depends(get_db)):
    return  admin_refresh_controller(database, token)

# To create a new admin account
@router.post("/register",tags=["Admin Management"])
async def admin_create_router(ad: Adminformat, database: Session = Depends(get_db)):
    return admin_create_controller(ad,database)


@router.get("",tags=["Admin Management"])
async def admin_get_by_token(database: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  admin_gets_controller(database,tokens)

@router.put("/{admin_id}",tags=["Admin Management"])
async def admin_update_details(admin_id: int, ad: Adminformat, database: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  admin_update_controller(database, admin_id, ad,tokens)

@router.get("/{admin_id}",tags=["Admin Management"])
async def admin_get_by_token(admin_id: int, database: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  admin_get_controller(database, admin_id,tokens)


@router.delete("/{admin_id}",tags=["Admin Management"])
async def admin_delete_details(admin_id: int, database: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  admin_delete_controller(database, admin_id,tokens)

@router.patch("/{admin_id}",tags=["Admin Management"])
async def admin_update_password(admin_id: int, ad: Adminpassword, db: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  admin_update_password_controller(db, admin_id, ad,tokens)

@router.get("/admin/report/sales",tags=['Repport and Sales'])
async def get_admin_sales_report(start_date: str, end_date: str, db: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return  get_admin_sales_report_controller(start_date,end_date,db,tokens)

@router.get("/admin/reports/customer",tags=['Repport and Sales'])    
async def  get_top_customers(db:Session=Depends(get_db),tokens:str = Depends(https_bearer)):
    return get_top_customers_controller(db,tokens)

@router.get("/admin/reports/top-selling-books/{limit}",tags=['Repport and Sales'])
async def get_top_selling(limit: int , db: Session = Depends(get_db), tokens: str = Depends(https_bearer)):
    return get_top_selling_books_controller(limit,db,tokens)

@router.get("/admin/reports/top-rated-books",tags=['Repport and Sales'])
async def get_top_rated_books(limit, db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return get_top_rated_books_controller(limit, db,tokens)