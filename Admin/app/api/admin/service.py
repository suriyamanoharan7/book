from sqlalchemy.orm import Session
from sqlalchemy import func,Integer,cast
from api.admin.model import Admin
from datetime import datetime
from fastapi import HTTPException,status
from utils.common_models import Order,User,Book,Review



def admin_token_validate(db:Session,token):
    return db.query(Admin).filter(Admin.refresh_token == token).first()

def admin_validate(db:Session,email,pwd):
    return db.query(Admin).filter(Admin.email == email,Admin.password == pwd).first()


def admin_get_by_id(db:Session,tk_id):
    turn = db.query(Admin).filter(Admin.id == tk_id).first()
    if not turn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    if turn.is_deleted == True:
        return False
    return turn

def admin_gets_service(db:Session):
    return db.query(Admin).filter(Admin.is_deleted == False).all()


def admin_create_service(request,db:Session,ref_token):
    add = Admin(
        name = request.name,
        email = request.email,
        password = request.password,
        refresh_token = ref_token
    )
    db.add(add)
    db.commit()
    db.refresh(add)
    return add

def admin_update_service(db:Session,admin_id,request):
    update = admin_get_by_id(db,admin_id)
    if update:
        update.name = request.name
        update.email = request.email
        update.password = request.password
        update.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(update)
        return update

def admin_update_password_service(db,admin_id,request):
    update = admin_get_by_id(db,admin_id)
    if update:
        update.password = request.password
        update.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(update)
        return update

def refresh_update_token(db:Session,token,refresh):
    update = admin_token_validate(db,token)
    if update:
        update.refresh_token = refresh
        update.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(update)
        return update


def admin_delete_service(db:Session,admin_id):
    delete = admin_get_by_id(db,admin_id)
    if delete:
        delete.is_deleted = True
        db.commit()
        return True
    return False

def get_admin_sales_report_service(start_date, end_date, db):
    total_sales = db.query(func.sum(Order.total_value).label("total_sales")) \
                    .filter(Order.order_date.between(start_date, end_date)) \
                    .scalar() or 0.0

    return total_sales

def get_top_customers_service(db):
    top_customers = db.query(User.id, User.name, func.sum(Order.total_value).label("total_spent")) \
                      .join(Order, User.id == Order.user_id) \
                      .group_by(User.id, User.name) \
                      .order_by(func.sum(Order.total_value).desc()) \
                      .limit(5) \
                      .all()
    return [
        {"user_id": customer.id, "name": customer.name, "total_spent": customer.total_spent}
        for customer in top_customers
    ]


def get_top_selling_books_service(limit, db):
    """
    Retrieve top-selling books based on total quantity sold.
    """
    try:
        expanded_orders = (
        db.query(
            func.json_array_elements_text(Order.book_id).label("book_id"),
            func.json_array_elements_text(Order.quantity).label("quantity"),
        )
        .subquery("expanded_orders")
    )

    # Aggregate and sort by total quantity sold
        books = (
            db.query(
                expanded_orders.c.book_id.label("book_id"),
                func.sum(cast(expanded_orders.c.quantity, Integer)).label("total_sold"),
            )
            .group_by(expanded_orders.c.book_id)
            .order_by(func.sum(cast(expanded_orders.c.quantity, Integer)).desc())
            .limit(limit)
            .all()
        )

        return [{"book_id": row.book_id, "total_sold": row.total_sold} for row in books]


    except Exception as e:
        return {"error": str(e)}

   
def get_top_rated_books_service(limit, db):
    """
    Retrieve products with the highest average ratings.
    """
    books = (
        db.query(Book.title, Book.avg_rating)  
        .filter(Book.avg_rating != None)     
        .order_by(Book.avg_rating.desc())     
        .limit(limit)                        
        .all()
    )
    return [{"title": book.title, "avg_rating": book.avg_rating} for book in books]

def get_order_id(order_id,db):
    return db.query(Order).filter(Order.id == order_id).first()

def mark_order_completed_service(order,db):
    order.status = "completed"
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated to completed", "order_id": order.id}

def mark_order_cancelled_service(order,db):
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated to cancelled", "order_id": order.id}