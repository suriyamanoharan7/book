from pydantic import BaseModel 

class DirectOrder(BaseModel):
    book_id :int
    quantity :int