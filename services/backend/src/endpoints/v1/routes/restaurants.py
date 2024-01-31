from fastapi import APIRouter, Request

from src.db.calls import get_restaurants, get_restaurant, get_vouchers, get_reviews
from src.endpoints.v1.schemas.restaurants import *
from src.security.authenticity import sign_data
from src.utils.logger import logger

router = APIRouter()


@router.get("/")
def fetch_restaurants(request: Request) -> GetRestaurantsResponse:
    user_id = request.headers.get('UserId')
    logger.info(f"Fetching restaurants for user {user_id}")

    restaurants = get_restaurants()
    
    signature = sign_data([r.model_dump() for r in restaurants], user_id)
    response = GetRestaurantsResponse(
        data=restaurants,
        signature=signature
    )

    logger.info(f"Restaurant info: {response}")
    return response


@router.get("/{restaurant_id}")
def fetch_restaurant(request: Request, restaurant_id: int) -> GetRestaurantResponse:
    user_id = request.headers.get('UserId')
    logger.info(f"Fetching restaurant {restaurant_id} for user {user_id}")

    restaurant = get_restaurant(restaurant_id)

    vouchers = get_vouchers(restaurant_id, user_id)
    restaurant.user_vouchers = vouchers

    reviews = get_reviews(restaurant_id)
    restaurant.reviews = reviews

    signature = sign_data(restaurant.model_dump(), user_id)
    response = GetRestaurantResponse(
        data=restaurant,
        signature=signature
    )

    logger.info(f"Restaurant info: {response}")
    return response
