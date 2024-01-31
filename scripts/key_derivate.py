import key_generate

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

debug: bool = False


def derive_key(private_key: ec.EllipticCurvePrivateKey, public_key: ec.EllipticCurvePublicKey) -> bytes:
    shared_secret = private_key.exchange(ec.ECDH(), public_key)

    return shared_secret


if __name__ == '__main__':
    alice_private_key, alice_public_key = key_generate.generate_key_pair()
    bob_private_key, bob_public_key = key_generate.generate_key_pair()

    alice_derived_key = derive_key(alice_private_key, bob_public_key)
    bob_derived_key = derive_key(bob_private_key, alice_public_key)

    if debug:
        print("alice_derived_key: ", alice_derived_key)
        print("bob_derived_key: ", bob_derived_key)
        print()

    assert alice_derived_key == bob_derived_key

    print("All tests passed.")

