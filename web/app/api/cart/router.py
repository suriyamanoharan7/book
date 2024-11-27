from api.cart.model import get_db
from sqlalchemy.orm import Session
from utils.auth_bearer import UserJWT
from api.book.controller import *
from fastapi import APIRouter,Depends
from api.cart.controller import *

router = APIRouter(prefix="/cart",tags=["Cart Management"])
https_bearer = UserJWT()

@router.post('/')
async def create_cart_account(request:CartCreate,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return cart_create_controller(request,db,tokens)

@router.get('/{user_id}')
async def get_cart_account(user_id:int,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return get_cart_controller(user_id,db,tokens)

@router.patch('/{cart_id}')
async def update_cart_account(cart_id:int,request:CartQuantity,db:Session=Depends(get_db),tokens:str= Depends(https_bearer)):
    return update_cart_controller(cart_id,request,db,tokens)

@router.delete('/{cart_id}')
async def delete_cart_account(cart_id:int,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return delete_cart_controller(cart_id,db,tokens)