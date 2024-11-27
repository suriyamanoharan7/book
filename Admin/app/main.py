import uvicorn
from configuration.config import *
from api.admin.router import router as admin_router
from api.user.router import router as user_router,work 
from api.book.router import router as book_router


Base.metadata.create_all(engine)

# execute admin router
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(work)
app.include_router(book_router)



# Run with server use and reload 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)