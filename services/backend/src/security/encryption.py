import secrets
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.models.encryption import EncryptedData


def load_private_key(filepath: str) -> ec.EllipticCurvePrivateKey:
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            private_key = serialization.load_pem_private_key(
                data,
                password=None,
                backend=default_backend()
            )
        return private_key
    except IOError as e:
        raise IOError(f"Error reading private key: {e}. Please provide a valid PEM-encoded private key.")


def load_public_key(filepath: str) -> ec.EllipticCurvePublicKey:
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            public_key = serialization.load_pem_public_key(
                data,
                backend=default_backend()
            )
        return public_key
    except IOError as e:
        raise IOError(f"Error reading public key: {e}. Please provide a valid PEM-encoded public key.")
    

def derive_shared_key(private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey) -> bytes:
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    return shared_secret


def encrypt(private_key_encryptor: ec.EllipticCurvePrivateKey, public_key_decryptor: ec.EllipticCurvePublicKey, plaintext: bytes) -> EncryptedData:

    # Generate a symmetric key from public and private keys of both parties
    derived_key = derive_shared_key(private_key_encryptor, public_key_decryptor)

    # Select algorythm and mode for symmetric encryption
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the plaintext and get the associated ciphertext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    iv_base64 = base64.b64encode(iv).decode()
    tag_base64 = base64.b64encode(tag).decode()
    ciphertext_base64 = base64.b64encode(ciphertext).decode()

    return EncryptedData(
        iv=iv_base64,
        tag=tag_base64,
        ciphertext=ciphertext_base64
    )


def decrypt(private_key_decryptor: ec.EllipticCurvePrivateKey, public_key_encryptor: ec.EllipticCurvePublicKey, encrypted_data: EncryptedData) -> bytes:

    # Generate a symmetric key from public and private keys of both parties
    derived_key = derive_shared_key(private_key_decryptor, public_key_encryptor)

    # Decode the base64 encoded attributes
    try: 
        iv = base64.b64decode(encrypted_data.iv)
        tag = base64.b64decode(encrypted_data.tag)
        ciphertext = base64.b64decode(encrypted_data.ciphertext)
    except KeyError:
        raise ValueError("Invalid encrypted data format. Expected a json with keys 'iv', 'tag' and 'ciphertext, but got" + encrypted_data.keys().join(", "))

    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    try:
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    except InvalidTag:
        raise ValueError("Authentication failed. Invalid ciphertext or key.")

    return plaintext

def sign_asym(private_key: ec.EllipticCurvePrivateKey, data: str) -> bytes:
    signature = private_key.sign(
        data.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_asym(public_key: ec.EllipticCurvePublicKey, data: str, signature: bytes):
    try:
        public_key.verify(
            signature,
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False
