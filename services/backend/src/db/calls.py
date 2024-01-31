from typing import List
from sqlalchemy import select, update

import src.models.restaurants as models
from src.utils.db import SessionLocal
from src.errors.restaurants import RestaurantNotFound
from src.db.models import Restaurant, Voucher, Reviews

db = SessionLocal()


def get_restaurants() -> List[models.Restaurant]:
    statement = select(Restaurant)
    restaurants = db.execute(statement).all()
    return [r[0].to_model_restaurant() for r in restaurants]


def get_restaurant(restaurant_id: str) -> models.Restaurant:
    statement = select(Restaurant).where(Restaurant.id == restaurant_id)
    result = db.execute(statement).first()

    if result is None or len(result) < 1:
        raise RestaurantNotFound()

    return result[0].to_model_restaurant()


def get_vouchers(restaurant_id: str, user_id: int) -> List[models.Vouchers]:
    statement = select(Voucher).where(Voucher.restaurant_id == restaurant_id).where(Voucher.user_id == user_id)
    result = db.execute(statement).all()
    return [r[0].to_model_voucher() for r in result if r[0].is_deleted == 0]


def get_voucher(code: str) -> models.Vouchers:
    statement = select(Voucher).where(Voucher.code == code)
    result = db.execute(statement).first()

    if result is None or len(result) < 1:
        return None

    return result[0].to_model_voucher()

def get_voucher(voucher_id: int, code: str) -> models.Vouchers:
    statement = select(Voucher).where(Voucher.code == code).where(Voucher.id == voucher_id)
    result = db.execute(statement).first()
    return result[0].to_model_voucher()


def get_voucher_by_code(code: str) -> models.Vouchers:
    statement = select(Voucher).where(Voucher.code == code)
    result = db.execute(statement).first()

    if result is None or len(result) < 1:
        return None

    return result[0].to_model_voucher()


def use_voucher(voucher_id: int, code: str) -> bool:
    statement = update(Voucher).where(Voucher.id == voucher_id and Voucher.code == code).values(is_deleted=1)
    result = db.execute(statement)

    db.flush()
    db.commit()

    voucher = select(Voucher).where(Voucher.id == voucher_id)
    result = db.execute(voucher).first()

    return result[0].is_deleted == 1


def gift_voucher(voucher_id: int, code: str, newOwner: int, newCode: str, newDiscount: str, newDescryption: str) -> bool:
    statement = update(Voucher).where(Voucher.code == code).where(Voucher.id == voucher_id).values(
        user_id=newOwner,
        code=newCode,
        discount=newDiscount,
        description=newDescryption
    )
    result = db.execute(statement)
    db.commit()
    db.flush()
    return result is not None

def get_voucher_user_id(voucher_id: int, code: str) -> int:
    statement = select(Voucher).where(Voucher.code == code).where(Voucher.id == voucher_id)
    result = db.execute(statement).first()
    return result[0].user_id


def get_reviews(restaurant_id: str) -> List[models.Reviews]:
    statement = select(Reviews).where(Reviews.restaurant_id == restaurant_id)
    result = db.execute(statement).all()
    return [r[0].to_model_reviews() for r in result]


def get_review(review_id: int) -> models.Reviews:
    statement = select(Reviews).where(Reviews.id == review_id)
    result = db.execute(statement).first()
    return result[0].to_model_reviews()


def create_review(restaurant_id: str, user_id: int, rating: int, review: str, signature: str) -> models.Reviews:
    review = Reviews(
        restaurant_id=restaurant_id,
        user_id=user_id,
        rating=rating,
        review=review,
        signature=signature,
    )
    db.add(review)
    db.flush()
    db.commit()
    return review.to_model_reviews()
