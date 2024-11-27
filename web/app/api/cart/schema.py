from pydantic import BaseModel

class CartCreate(BaseModel):
    book_id : int
    quantity : int
    class config:
        from_attributes = True

class CartQuantity(BaseModel):
    quantity: int