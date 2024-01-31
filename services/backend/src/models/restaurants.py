from __future__ import annotations
from pydantic import BaseModel
from typing import List

from src.models.encryption import EncryptedData


class MenuItem(BaseModel):
    name: str
    category: str
    description: str
    price: float
    currency: str


class Vouchers(BaseModel):
    id: int
    restaurant_id: int
    user_id: int

    # This data field contains the "code", "discount" and "description" fields from the database
    # but is encrypted with the user's public key
    data: EncryptedData


class Reviews(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    review: str
    rating: int
    signature: str


class Restaurant(BaseModel):
    id: int
    owner: str
    restaurant: str
    address: str
    genre: List[str]
    menu: List[MenuItem] = None
    user_vouchers: List[Vouchers] = None
    reviews: List[Reviews] = None


class User(BaseModel):
    id: int
    name: str
