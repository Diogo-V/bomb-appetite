import json
from typing import Any
from sqlalchemy import Column, String, ForeignKey, Text, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr

import src.models.restaurants as models
from src.utils.config import config
from src.security.encryption import encrypt, load_private_key, load_public_key


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    id = Column(Integer(), primary_key=True)
    name = Column(String(100))

    def to_model_user(self) -> models.User:
        return models.User(
            id=self.id,
            name=self.name,
        )


class MenuItem(Base):
    id = Column(String(36), primary_key=True)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'))
    name = Column(String(100))
    category = Column(String(100))
    description = Column(String(100))
    price = Column(Float())
    currency = Column(String(100))

    def to_model_menu_item(self) -> models.MenuItem:
        return models.MenuItem(
            id=self.id,
            restaurant_id=self.restaurant_id,
            name=self.name,
            category=self.category,
            description=self.description,
            price=self.price,
            currency=self.currency,
        )


class Restaurant(Base):
    id = Column(String(36), primary_key=True)
    owner = Column(String(100))
    restaurant = Column(String(100))
    address = Column(String(100))
    genre = Column(Text())
    menu = relationship("MenuItem")

    def to_model_restaurant(self) -> models.Restaurant:
        return models.Restaurant(
            id=self.id,
            owner=self.owner,
            restaurant=self.restaurant,
            address=self.address,
            genre=self.genre.split(","),
            menu=[m.to_model_menu_item() for m in self.menu],
        )
    

class Voucher(Base):
    id = Column(Integer(), primary_key=True)
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'))
    user_id = Column(Integer(), ForeignKey('user.id'))
    code = Column(String(100))
    discount = Column(Float())
    description = Column(String(100))
    is_deleted = Column(Integer(), default=0)

    def to_model_voucher(self) -> models.Vouchers:
        data = {
            "code": self.code,
            "discount": self.discount,
            "description": self.description,
        }

        # Load keys
        server_private_key = load_private_key(config.SERVER_PRIVATE_KEY_PATH)
        user_public_key = load_public_key(config.USER_KEYS_TEMPLATE_PATH.format(id=self.user_id))

        data_bytes = json.dumps(data).encode()
        encrypted_data = encrypt(server_private_key, user_public_key, data_bytes)

        return models.Vouchers(
            id=self.id,
            restaurant_id=self.restaurant_id,
            user_id=self.user_id,
            data=encrypted_data,
        )
    

class Reviews(Base):
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user.id'))
    restaurant_id = Column(String(36), ForeignKey('restaurant.id'))
    review = Column(String(255))
    rating = Column(Integer())
    signature = Column(String(255))  # User hashes the review and signs it with their private key

    def to_model_reviews(self) -> models.Reviews:
        return models.Reviews(
            id=self.id,
            user_id=self.user_id,
            restaurant_id=self.restaurant_id,
            review=self.review,
            rating=self.rating,
            signature=self.signature,
        )
