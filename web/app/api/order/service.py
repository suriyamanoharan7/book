from api.order.model import Order,OrderStatus
from api.book.model import Book
from fastapi import HTTPException
from api.cart.model import Cart
from datetime import datetime

def direct_order_book_service(request,db,user):
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.stock < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    total_value = book.price * request.quantity
    new_order = Order(
        user_id=user.id,
        book_id=[request.book_id], 
        quantity=[request.quantity],
        order_type="direct",
        total_value=total_value,
        status=OrderStatus.pending
    )
    db.add(new_order)
    book.stock -= request.quantity
    db.commit()
    db.refresh(new_order)

    return new_order

def cart_order_book_service(db,user):
    cart_items = db.query(Cart).filter(Cart.user_id == user.id, Cart.is_deleted == False).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="User has no product in their cart")
    
    orders = []

    for item in cart_items:
        # Fetch the associated book details
        book = db.query(Book).filter(Book.id == item.book_id).first()
    
        if book.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for book '{book.title}' (ID: {book.id})"
            )

        total_value = book.price * item.quantity

        new_order = Order(
            user_id=user.id,
            book_id=[item.book_id],  
            quantity=[item.quantity],
            order_type="cart",
            total_value=total_value,
            status=OrderStatus.pending,
            order_date=datetime.utcnow()
        )
        db.add(new_order)
        print(new_order)
        orders.append(new_order)

        book.stock -= item.quantity

        
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()

    db.commit()
    return {"Purchase successfully"}


def get_order_history_service(db,user):
    orders = db.query(Order).filter(Order.user_id == user.id,).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No purchase history found for this user.")

    for order in orders:
        order.books = [
            {"id": book.id, "title": book.title, "price": book.price}
            for book_id in order.book_id
            for book in db.query(Book).filter(Book.id == book_id).all()
        ]

    return orders