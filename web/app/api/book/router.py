from api.book.model import get_db
from sqlalchemy.orm import Session
from utils.auth_bearer import UserJWT
from api.book.controller import *
from fastapi import APIRouter,Depends

router = APIRouter(prefix='/book')
https_bearer = UserJWT()

@router.post('/',tags=["Book Management"])
def create_book(request:BookCreate,db:Session=Depends(get_db),tokens:str=Depends(https_bearer)):
    return create_book_controller(request,db,tokens)


@router.get("/",tags=["Book Management"])
async def book_get_accounts(db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return book_gets_controller(db,tokens)

# to update user details by user ID
@router.put("/{book_id}",tags=["Book Management"])
async def book_update_account(book_id:int,request:BookCreate, db: Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return book_update_controller(db,book_id,request,tokens)

# To retrieve a single user details by user ID
@router.get("/{book_id}",tags=["Book Management"])
async def book_get_account(book_id:int,db:Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return book_get_controller(db,book_id,tokens)

# to delete a single user's details by user ID
@router.delete("/{book_id}",tags=["Book Management"])
async def book_delete_account(book_id:int,db:Session = Depends(get_db),tokens: str = Depends(https_bearer)):
    return book_delete_controller(db,book_id,tokens)
