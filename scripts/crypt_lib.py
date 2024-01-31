import os
import key_storage
import key_generate
import crypt_lib_parser
import json_storage
import storage_service as Storage_S
from encrypt_elliptic_curve import encrypt, decrypt

debug: bool = False

arg_parser = crypt_lib_parser.create_parser()
args = arg_parser.parse_args()

storage_service_plaintext = Storage_S.StorageServiceFactory.get_storage_service(Storage_S.StorageType.FILE)


def protect(input_filepath: str, output_filepath: str, private_key_encryptor_filepath: str, public_key_decryptor_filepath: str) -> dict:
    if debug: print("Protecting file...")

    # TODO: following calls can throw exceptions. Handle them or make error messages more specific

    plaintext = storage_service_plaintext.load(input_filepath)
    
    private_key_encryptor = key_storage.load_private_key(private_key_encryptor_filepath)
    public_key_decryptor = key_storage.load_public_key(public_key_decryptor_filepath)

    ciphertext = encrypt(private_key_encryptor, public_key_decryptor, plaintext)

    # Save the encrypted data to the output file
    json_storage.store_json(ciphertext, output_filepath)

    return ciphertext


def check(input_filepath: str, private_key_decryptor_filepath: str, public_key_encryptor_filepath: str) -> ():
    if debug: print("Checking file...")

    ciphertext = json_storage.load_json(input_filepath)

    private_key_decryptor = key_storage.load_private_key(private_key_decryptor_filepath)
    public_key_encryptor = key_storage.load_public_key(public_key_encryptor_filepath)

    decrypt(private_key_decryptor, public_key_encryptor, ciphertext)


def unprotect(input_filepath: str, output_filepath: str, private_key_decryptor_filepath: str, public_key_encryptor_filepath: str) -> bytes:
    if debug: print("Unprotecting file...")

    # TODO: following calls can throw exceptions. Handle them or make error messages more specific

    ciphertext = json_storage.load_json(input_filepath)

    private_key_decryptor = key_storage.load_private_key(private_key_decryptor_filepath)
    public_key_encryptor = key_storage.load_public_key(public_key_encryptor_filepath)

    plaintext = decrypt(private_key_decryptor, public_key_encryptor, ciphertext)

    # Save the plaintext to the output file
    storage_service_plaintext.store(plaintext, output_filepath)

    return plaintext


def generate_key_pair(private_key_filepath: str, public_key_filepath: str) -> ():
    if debug: print("Generating a new key pair...")

    private_key, public_key = key_generate.generate_key_pair()

    key_storage.store_private_key(private_key, private_key_filepath)
    key_storage.store_public_key(public_key, public_key_filepath)    


if __name__ == "__main__":

    if args.function == "help":
    
        arg_parser.print_help()

    elif args.function == "protect":

        print(f"Protecting document from {args.input_file} to {args.output_file} "
              f"using private key file {args.private_key_file} and public key file {args.public_key_file}")
        protect(args.input_file, args.output_file, args.private_key_file, args.public_key_file)

    elif args.function == "check":

        print(f"Checking security of document at {args.input_file}")
        try:
            check(args.input_file, args.private_key_file, args.public_key_file)
            print(f"Document security check passed!")
        except Exception as e:
            print(f"Document security check failed: {e}")

    elif args.function == "unprotect":

        print(f"Unprotecting document from {args.input_file} to {args.output_file} "
              f"using private key file {args.private_key_file} and public key file {args.public_key_file}")
        unprotect(args.input_file, args.output_file, args.private_key_file, args.public_key_file)

    elif args.function == "generate-key-pair":

            print(f"Generating a new key pair: private key to {args.private_key_file} and public key to {args.public_key_file}")
            generate_key_pair(args.private_key_file, args.public_key_file)

    else:
        raise ValueError("Invalid function. Expected help, protect, check, or unprotect")


