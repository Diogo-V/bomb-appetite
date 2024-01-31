import hashlib
import json
import hmac
from typing import List, Dict

from src.models.encryption import EncryptedData
from src.security.encryption import encrypt, load_private_key, load_public_key, decrypt, verify_asym
from src.utils.config import config


def sign_data(data: Dict | List[Dict], user_id: int) -> EncryptedData:

    # Load keys
    server_private_key = load_private_key(config.SERVER_PRIVATE_KEY_PATH)
    user_public_key = load_public_key(config.USER_KEYS_TEMPLATE_PATH.format(id=user_id))

    # Convert data to bytes. To match JS's JSON.stringify, we need to remove trailing .0 from floats
    # and remove all whitespace
    data_bytes = json.dumps(data, separators=(',', ':')).replace(".0", "").encode()

    # Hash the data and encrypt it with the server's private key and the user's public key
    data_hash = hashlib.sha256(data_bytes).hexdigest()
    encrypted_data = encrypt(server_private_key, user_public_key, data_hash.encode())

    return encrypted_data

def verify_signature(data: Dict, user_id: int, signature: EncryptedData) -> bool:
    # Load keys
    user_public_key = load_public_key(config.USER_KEYS_TEMPLATE_PATH.format(id=user_id))
    server_private_key = load_private_key(config.SERVER_PRIVATE_KEY_PATH)

    # Convert data to bytes. To match JS's JSON.stringify, we need to remove trailing .0 from floats
    # and remove all whitespace
    data_bytes = json.dumps(data, separators=(',', ':')).replace(".0", "").encode()

    # Hash the data
    data_hash = hashlib.sha256(data_bytes).hexdigest()

    # Decrypt the signature
    try:
        decrypted_signature = decrypt(server_private_key, user_public_key, signature)

        # Compare the hashes
        is_valid = hmac.compare_digest(data_hash.encode(), decrypted_signature)
        return is_valid
    except:
        return False

def verify_asym_data(data: str, signature: str, user_id: int) -> bool:
    # Load keys
    user_public_key = load_public_key(config.USER_KEYS_TEMPLATE_PATH.format(id=user_id))

    # Convert signature to bytes
    signature_bytes = bytes.fromhex(signature)

    # verify the signature
    verified = verify_asym(user_public_key, data, signature_bytes)

    return verified
    
