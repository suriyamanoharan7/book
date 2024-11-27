from fastapi import APIRouter,Depends
from api.user.controller import *
from api.user.model import get_db
from sqlalchemy.orm import Session
from utils.auth_bearer import UserJWT

router = APIRouter(prefix='/user')
https_bearer = UserJWT()

@router.post("/login")
async def user_login(tk:UserLogin,db: Session = Depends(get_db)):
    return user_login_controller(db,tk.email,tk.password)

# To re-login with refresh token by user
@router.post("/re-login")
async def user_refresh_router(token: str, database: Session = Depends(get_db)):
    return user_refresh_controller(database, token)


@router.post("/",tags=["User Management"])
async def user_create_account(request:UserCreate,db: Session = Depends(get_db)):
    return user_create_controller(db,request)

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
