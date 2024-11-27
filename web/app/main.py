import uvicorn
from configuration.config import *
#from api.admin.router import router as admin_router
from api.user.router import router as user_router
from api.book.router import router as book_router
from api.cart.router import router as cart_router
from api.order.router import router as order_router
from api.review.router import router as review_router

Base.metadata.create_all(engine)

# execute admin router

app.include_router(user_router)
app.include_router(book_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(review_router)





if __name__ == "__main__":
    uvicorn.run("main:app", port=7000, reload=True)