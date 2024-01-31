from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec


def generate_key_pair() -> (ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey):
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()

    return private_key, public_key

