from utils.common_models import Publisher,User
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException,status




def user_get_id(db:Session,user_id):
    turn = db.query(User).filter(User.id == user_id).first()
    if not turn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User doesn't exists.")
    if turn.is_delete == True:
        return False
    return turn


def user_gets(db:Session):
    return db.query(User).filter(User.is_delete == False).all()


def user_create_service(db,request):
    add = User(
            name = request.name,
            email = request.email,
            password = request.password,
            role_id =request.role_id
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

def get_all_publisher_requests_service(db):
    results = db.query(User).filter(User.role_id == 2).all()
    publisher_user_ids = db.query(Publisher.user_id).all()
    publisher_user_ids_set = {id[0] for id in publisher_user_ids}
    users_without_request = [
        user for user in results if user.id not in publisher_user_ids_set
    ]
    
    return users_without_request



def approve_publisher_request_service(db, user_id):
    user = db.query(User).filter(User.id == user_id, User.role_id == 2).first()
    if not user:
        raise HTTPException(status_code=400, detail="Only users with role_id 2 can send publisher requests.")

    publisher = db.query(Publisher).filter(Publisher.user_id == user_id).first()
    if publisher:
        return {"success": True, "message": "User is already an approved publisher."}
    else:

        new_publisher = Publisher(
            user_id=user.id,
            name=user.name,
            is_approved=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )
        db.add(new_publisher)
        db.commit()
        return {"success": True, "message": "Publisher request accepted and approved."}


def deactivate_customer_service(customer_id, db):
    customer = db.query(User).filter(User.id == customer_id, User.role_id == 1).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or not a valid customer.",
        )
    if not customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer account is already deactivated.",
        )
    customer.is_active = False
    db.commit()
    db.refresh(customer)

    return {"message": f"Customer '{customer.name}' has been successfully deactivated."}
