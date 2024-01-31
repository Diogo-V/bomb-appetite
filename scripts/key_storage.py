import os
import key_generate
import storage_service

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

debug: bool = False
key_storage_service = storage_service.StorageServiceFactory.get_storage_service(storage_service.StorageType.FILE)


def store_public_key(public_key: ec.EllipticCurvePublicKey, filepath: str) -> ():
    if debug: print("Storing public key...")

    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    try:
        key_storage_service.store(serialized_public_key, filepath)
    except IOError as e:
        raise IOError(f"Error writing public key: {e}")


def store_private_key(private_key: ec.EllipticCurvePrivateKey, filepath: str) -> ():
    if debug: print("Storing private key...")

    serialized_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    try:
        key_storage_service.store(serialized_private_key, filepath)
    except IOError as e:
        raise IOError(f"Error writing private key: {e}")


def load_public_key(filepath: str) -> ec.EllipticCurvePublicKey:
    if debug: print("Loading public key...")
    try:
        public_key = serialization.load_pem_public_key(
            key_storage_service.load(filepath),
            backend=default_backend()
        )
    except IOError as e:
        raise IOError(f"Error reading public key: {e}. Please provide a valid PEM-encoded public key.")
    return public_key


def load_private_key(filepath: str) -> ec.EllipticCurvePrivateKey:
    if debug: print("Loading private key...")
    try:
        private_key = serialization.load_pem_private_key(
            key_storage_service.load(filepath),
            password=None,
            backend=default_backend()
        )
    except IOError as e:
        raise IOError(f"Error reading private key: {e}. Please provide a valid PEM-encoded private key.")
    return private_key

if __name__ == "__main__":
    private_key, public_key = key_generate.generate_key_pair()

    store_public_key(public_key, "temp_public_key.pem")
    store_private_key(private_key, "temp_private_key.pem")

    public_key_read = load_public_key("temp_public_key.pem")
    private_key_read = load_private_key("temp_private_key.pem")

    # compare the keys
    assert public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ) == public_key_read.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    assert private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ) == private_key_read.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    os.remove("temp_public_key.pem")
    os.remove("temp_private_key.pem")

    print("All tests passed.")


