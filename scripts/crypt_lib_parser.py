import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Secure Document Format (SDF) command-line interface")

    subparsers = parser.add_subparsers(title="functions", dest="function", required=True, help="Available functions")

    # Sub-command: help
    subparsers.add_parser("help", help="Display help message")

    # Sub-command: protect
    protect_parser = subparsers.add_parser("protect", help="Add security to a document")
    protect_parser.add_argument("input_file", type=str, help="Path to the input plaintext file")
    protect_parser.add_argument("output_file", type=str, help="Path to the output protected json file")
    protect_parser.add_argument("private_key_file", type=str, help="Path to the PEM-encoded private key file")
    protect_parser.add_argument("public_key_file", type=str, help="Path to the PEM-encoded public key file")

    # Sub-command: check
    check_parser = subparsers.add_parser("check", help="Verify security of a document")
    check_parser.add_argument("input_file", type=str, help="Path to the input file")
    check_parser.add_argument("private_key_file", type=str, help="Path to the PEM-encoded private key file")
    check_parser.add_argument("public_key_file", type=str, help="Path to the PEM-encoded public key file")

    # Sub-command: unprotect
    unprotect_parser = subparsers.add_parser("unprotect", help="Remove security from a document")
    unprotect_parser.add_argument("input_file", type=str, help="Path to the input protected json file")
    unprotect_parser.add_argument("output_file", type=str, help="Path to the output plaintext file")
    unprotect_parser.add_argument("private_key_file", type=str, help="Path to the PEM-encoded private key file")
    unprotect_parser.add_argument("public_key_file", type=str, help="Path to the PEM-encoded public key file")

    # Sub-command: generate-key
    generate_key_parser = subparsers.add_parser("generate-key-pair", help="Generate a new key pair")
    generate_key_parser.add_argument("private_key_file", type=str, help="Path to the output PEM-encoded private key file")
    generate_key_parser.add_argument("public_key_file", type=str, help="Path to the output PEM-encoded public key file")

    return parser

if __name__ == "__main__":
    arg_parser = create_parser()

    args = arg_parser.parse_args()

    if args.function == "help":
        arg_parser.print_help()
    elif args.function == "protect":
        print(f"Protecting document from {args.input_file} to {args.output_file} "
              f"using private key file {args.private_key_file} and public key file {args.public_key_file}")
        # Implement the logic for protecting the document
    elif args.function == "check":
        print(f"Checking security of document at {args.input_file}")
        # Implement the logic for checking the security of the document
    elif args.function == "unprotect":
        print(f"Unprotecting document from {args.input_file} to {args.output_file} "
              f"using private key file {args.private_key_file} and public key file {args.public_key_file}")
        # Implement the logic for unprotecting the document
    elif args.function == "generate-key-pair":
        print(f"Generating a new key pair: private key to {args.private_key_file} and public key to {args.public_key_file}")
        # Implement the logic for generating a new key pair


