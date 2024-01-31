from pydantic import BaseModel

from src.models.encryption import EncryptedData
from src.models.restaurants import Vouchers


class GetRestaurantVoucherResponse(BaseModel):
    data: Vouchers
    signature: EncryptedData

class PutRestaurantVoucherResponse(BaseModel):
    data: dict
    signature: EncryptedData

class PostGiftRestaurantVoucherResponse(BaseModel):
    data: dict
    signature: EncryptedData
