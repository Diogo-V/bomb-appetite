from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    with open("../../copies_of_keys/user_1_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    public_key = private_key.public_key()
    return private_key, public_key

def sign(private_key, data):
    signature = private_key.sign(
        data.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify(public_key, data, signature):
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

if __name__ == "__main__":
    # Example usage
    private_key, public_key = generate_key_pair()

    # Data to be signed
    data_to_sign = "Hello World"

    signature = "3044022016a59c4d77fd917a7a99c38aebaad13e5255413e2cb149164b3e89fa36de3cd402201b67080c85a67a224cdb6cb7aa6a75bb824f351658c3cf61ee6e388be4ef0901"
    signature = bytes.fromhex(signature)
    print(f"Signature: {signature.hex()}")

    # Verify the signature
    if verify(public_key, data_to_sign, signature):
        print("Signature verification successful.")
    else:
        print("Signature verification failed.")