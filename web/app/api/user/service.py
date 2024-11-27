from utils.common_models import Publisher
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException,status
from api.user.model import User




def user_get_id(db:Session,user_id):
    turn = db.query(User).filter(User.id == user_id).first()
    if not turn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User doesn't exists.")
    if turn.is_delete == True:
        return False
    return turn


def user_gets(db:Session):
    return db.query(User).filter(User.is_delete == False).all()


def user_create_service(db,request,refresh):
    add = User(
            name = request.name,
            email = request.email,
            password = request.password,
            role_id =request.role_id,
            refresh_token = refresh
        )
    db.add(add)
    db.commit()
    db.refresh(add)
    return add
    

# To update user details by user ID
def user_update_service(db:Session,user_id,request):
    update = user_get_id(db,user_id)
    if update:
        update.name = request.name
        update.email = request.email
        update.password = request.password
        update.role_id =request.role_id
        update.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False



# to delete a single user details by ID
def user_delete_service(db:Session,user_id):
    delete = user_get_id(db,user_id)
    if delete:
        delete.is_delete = True
        db.commit()
        return True
    return False

def login_token_validate(db:Session,token):
    return db.query(User).filter(User.refresh_token == token).first()

# login user detail validation
def login_validate(db:Session,email,pwd):
    return db.query(User).filter(User.email == email,User.password == pwd).first()

def refresh_update_token(db:Session,token,refresh):
    update = login_token_validate(db,token)
    if update:
        update.refresh_token = refresh
        update.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(update)
        return update