from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    review: str = Field(..., max_length=500)
    rating: float = Field(..., ge=0.0, le=5.0)
