import secrets
import key_generate
import key_derivate
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.asymmetric import ec

debug: bool = False


def encrypt(private_key_encryptor: ec.EllipticCurvePrivateKey, public_key_decryptor: ec.EllipticCurvePublicKey, plaintext: bytes) -> dict:
    if debug: print("Encrypting...")

    # Generate a symmetric key from public and private keys of both parties
    derived_key = key_derivate.derive_key(private_key_encryptor, public_key_decryptor)

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

    return {
        'iv': iv_base64,
        'tag': tag_base64,
        'ciphertext': ciphertext_base64
    }

def decrypt(private_key_decryptor: ec.EllipticCurvePrivateKey, public_key_encryptor: ec.EllipticCurvePublicKey, encrypted_data: dict) -> bytes:
    if debug: print("Decrypting...")

    # Generate a symmetric key from public and private keys of both parties
    derived_key = key_derivate.derive_key(private_key_decryptor, public_key_encryptor)

    # Decode the base64 encoded attributes
    try: 
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['tag'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
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


if __name__ == "__main__":
    alice_private_key, alice_public_key = key_generate.generate_key_pair()
    bob_private_key, bob_public_key = key_generate.generate_key_pair()

    plaintext = "Hello World!"
    ciphertext = encrypt(alice_private_key, bob_public_key, plaintext.encode())
    decrypted_plaintext = decrypt(bob_private_key, alice_public_key, ciphertext)
    decrypted_plaintext = decrypted_plaintext.decode()

    if debug: 
        print()
        print("plaintext:           ", plaintext)
        print("ciphertext:          ", ciphertext)
        print("decrypted_plaintext: ", decrypted_plaintext)
        print()

    assert plaintext == decrypted_plaintext

    print("All tests passed.")

