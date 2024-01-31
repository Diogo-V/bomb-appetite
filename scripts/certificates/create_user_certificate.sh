
# Create key for user using input
user_key_name=$1

# Verify if the user key is empty
if [ -z "$user_key_name" ]; then
    echo "Expected user key name as argument. Usage: ./create_user_certificate.sh <user_key_name>"
    exit 1
fi

# Generate a user key
openssl genpkey -algorithm RSA -out ../../copies_of_keys/$user_key_name.key

# Generate a certificate signing request (CSR)
openssl req -new -key ../../copies_of_keys/$user_key_name.key -out ../../copies_of_certificates/$user_key_name.csr -subj "/C=PT/ST=Lisbon/L=Lisbon/O=IST-SIRS/CN=a24"

# Generate a certificate
openssl x509 -req -days 365 -in ../../copies_of_certificates/$user_key_name.csr -CA ../../copies_of_certificates/CA.crt -CAkey ../../copies_of_keys/CA.key -out ../../copies_of_certificates/$user_key_name.crt
