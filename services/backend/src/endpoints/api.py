from fastapi import APIRouter

from src.endpoints.v1.routes import (
    restaurants,
    reviews,
    vouchers
)

v1_api_router = APIRouter(prefix="/v1")
v1_api_router.include_router(restaurants.router, tags=["restaurants"], prefix="/restaurants")
v1_api_router.include_router(reviews.router, tags=["reviews"], prefix="/reviews")
v1_api_router.include_router(vouchers.router, tags=["vouchers"], prefix="/vouchers")
