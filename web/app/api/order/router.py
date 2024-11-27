from fastapi import APIRouter,Depends
from utils.auth_bearer import UserJWT
from api.order.model import get_db
from sqlalchemy.orm import Session
from api.order.controller import *


router = APIRouter(prefix='/order',tags=["Order"])
https_bearer = UserJWT()

@router.post('/directly')
async def DirectOrderBook(request:DirectOrder,db:Session= Depends(get_db),tokens:str = Depends(https_bearer)):
    return direct_order_book_controller(request,db,tokens)

@router.post('/from_cart')
async def OrderFromCart(db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return cart_order_book_controller(db,tokens)

@router.get('/history')
async def get_order_history(db:Session=Depends(get_db),tokens:str= Depends(https_bearer)):
    return get_order_history_controller(db,tokens)