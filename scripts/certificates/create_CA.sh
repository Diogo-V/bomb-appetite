# Generate a private key
openssl genpkey -algorithm RSA -out ../../copies_of_keys/CA.key

# Generate a certificate signing request (CSR)
openssl req -new -key ../../copies_of_keys/CA.key -out ../../copies_of_certificates/CA.csr -subj "/C=PT/ST=Lisbon/L=Lisbon/O=IST-SIRS/CN=a24"

# Generate a self-signed certificate
openssl req -x509 -key ../../copies_of_keys/CA.key -in ../../copies_of_certificates/CA.csr -out ../../copies_of_certificates/CA.crt -days 365

# Verify the certificate
openssl x509 -in ../../copies_of_certificates/CA.crt -text -noout

# Create a CA database
echo 01 > ../../copies_of_certificates/CA.srl
