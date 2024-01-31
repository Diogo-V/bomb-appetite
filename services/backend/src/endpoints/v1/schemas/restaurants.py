from pydantic import BaseModel
from typing import List

from src.models.encryption import EncryptedData
from src.models.restaurants import Restaurant


class GetRestaurantsResponse(BaseModel):
    data: List[Restaurant]
    signature: EncryptedData


class GetRestaurantResponse(BaseModel):
    data: Restaurant
    signature: EncryptedData
