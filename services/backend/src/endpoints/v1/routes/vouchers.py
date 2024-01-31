import json
from fastapi import APIRouter, Request, HTTPException

from src.db.calls import use_voucher, gift_voucher, get_voucher, get_voucher_user_id, get_voucher_by_code
from src.endpoints.v1.schemas.vouchers import *
from src.security.authenticity import sign_data, verify_signature, verify_asym_data
from src.security.encryption import load_public_key, load_private_key, decrypt
from src.utils.config import config
from src.utils.logger import logger
from src.models.encryption import EncryptedData

router = APIRouter()


@router.get("/{voucher_id}")
async def get_restaurant_voucher(request: Request, voucher_id: int) -> GetRestaurantVoucherResponse:
    user_id = request.headers.get('UserId')
    code = request.headers.get('Code')

    data = get_voucher(voucher_id, code)

    signature = sign_data(data.model_dump(), user_id)

    return GetRestaurantVoucherResponse(
        data=data,
        signature=signature
    )

@router.put("/")
async def put_use_restaurant_voucher(request: Request) -> PutRestaurantVoucherResponse:
    user_id = request.headers.get('UserId')

    body = await request.body()
    parsed_body = json.loads(body)

    code = parsed_body["code"]
    signature = parsed_body["signature"]
    signature = EncryptedData(**signature)

    logger.info(f"Using code {code} for user {user_id}")

    # Get voucher from code
    voucher = get_voucher_by_code(code)
    if voucher is None:
        data = { "is_used": False }
        signature = sign_data(data, user_id)
        response = PutRestaurantVoucherResponse(
            data=data,
            signature=signature
        )
        return response

    print(f"user_id: {user_id} and user in voucher: {voucher.user_id}")

    # Verifies if the use of this voucher is valid
    data = {
        "code": code,
    }
    is_valid = verify_signature(data, voucher.user_id, signature)
    if not is_valid:
        data = {
            "can_use_voucher": False,
        }

        signature = sign_data(data, user_id)
        response = PutRestaurantVoucherResponse(
            data=data,
            signature=signature
        )
        return response

    is_used = use_voucher(voucher.id, code)
    
    data = { "is_used": is_used }
    signature = sign_data(data, user_id)
    response = PutRestaurantVoucherResponse(
        data=data,
        signature=signature
    )

    logger.info(f"Voucher info: {response}")
    return response

@router.post("/{voucher_id}")
async def post_gift_restaurant_voucher(request: Request, voucher_id: int) -> PostGiftRestaurantVoucherResponse:
    user_id = request.headers.get('UserId')

    body = await request.body()
    parsed_body = json.loads(body)

    if int(user_id) != get_voucher_user_id(voucher_id, parsed_body["code"]):
        raise HTTPException(status_code=403, detail="User is not voucher owner")

    valid_signature = verify_asym_data(parsed_body["newOwner"], parsed_body["signature"], user_id)

    if not valid_signature:
        raise HTTPException(status_code=500, detail="Invalid signature for new owner")

    new_voucher_data_iv = parsed_body["newVoucherDataIv"]
    new_voucher_data_tag = parsed_body["newVoucherDataTag"]
    new_voucher_data_cyphertext = parsed_body["newVoucherDataCiphertext"]

    new_voucher_data = EncryptedData(
        iv=new_voucher_data_iv,
        tag=new_voucher_data_tag,
        ciphertext=new_voucher_data_cyphertext
    )

    new_owner_public_key = load_public_key(config.USER_KEYS_TEMPLATE_PATH.format(id=parsed_body["newOwner"]))
    server_private_key = load_private_key(config.SERVER_PRIVATE_KEY_PATH)

    try:
        decrypted_new_voucher_data_bytes = decrypt(server_private_key, new_owner_public_key, new_voucher_data)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid new voucher data")

    decrypted_new_voucher_data = json.loads(decrypted_new_voucher_data_bytes)

    is_gifted = gift_voucher(
        voucher_id, 
        parsed_body["code"], 
        parsed_body["newOwner"], 
        decrypted_new_voucher_data["code"], 
        decrypted_new_voucher_data["discount"], 
        decrypted_new_voucher_data["description"]
    )

    data = { "is_gifted": is_gifted }
    signature = sign_data(data, user_id)

    return PutRestaurantVoucherResponse(
        data=data,
        signature=signature
    )
