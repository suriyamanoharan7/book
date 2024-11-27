from fastapi import APIRouter,Depends
from api.user.controller import *
from api.user.model import get_db
from sqlalchemy.orm import Session
from utils.auth_bearer import AdminJWT


router = APIRouter(prefix='/admin/user')
work =APIRouter(prefix='/admin/publisher')


https_bearer = AdminJWT()

@router.post("/",tags=["User Management"])
async def user_create_account(request:UserCreate,db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return user_create_controller(db,request,tokens)

@router.get("/",tags=["User Management"])
async def user_get_accounts(db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return user_gets_controller(db,tokens)

# to update user details by user ID
@router.put("/{user_id}",tags=["User Management"])
async def user_update_account(user_id:int,request:UserCreate, db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return user_update_controller(db,user_id,request,tokens)

# To retrieve a single user details by user ID
@router.get("/{user_id}",tags=["User Management"])
async def user_get_account(user_id:int,db:Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return user_get_controller(db,user_id,tokens)

# to delete a single user's details by user ID
@router.delete("/{user_id}",tags=["User Management"])
async def user_delete_account(user_id:int,db:Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return user_delete_controller(db,user_id,tokens)

@work.get('/',tags=["User Management"])
async def get_all_publisher_requests(db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return get_all_publisher_requests_controller(db,tokens)

# @router.patch("/publisher/{publisher_id}/approve",tags=["User Management"])
# def approve_publisher(publisher_id: int, db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
#     return approve_publisher_controller(publisher_id,db,tokens)

@work.put('/{user_id}/approve',tags=["User Management"])
def  approve_publisher_request(user_id,db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return approve_publisher_request_controller(db,user_id,tokens)

@router.put('/{customer_id}/deactivate',tags=["User Management"])
def deactivate_customer(customer_id, db:Session =Depends(get_db),tokens: str = Depends(https_bearer)):
    return deactivate_customer_controller(customer_id, db,tokens)
