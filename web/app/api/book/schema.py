from pydantic import BaseModel

class BookCreate(BaseModel):
    title :str
    author :str
    offer_price :float
    price :float
    stock :int
    description : str
