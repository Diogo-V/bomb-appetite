from pydantic import BaseModel

from src.models.encryption import EncryptedData
from src.models.restaurants import Reviews


class GetReviewResponse(BaseModel):
    data: Reviews
    signature: EncryptedData


class PostReviewRequest(BaseModel):
    userId: int
    restaurantId: int
    stars: int 
    comment: str 
    signature: str


class PostReviewResponse(BaseModel):
    data: Reviews
    signature: EncryptedData
