#!/usr/bin/env bash

# Create SSL directory for client files
mkdir -p /home/vagrant/client-ssl
cd /home/vagrant/client-ssl

sudo cp /vagrant/copies_of_certificates/ca-db-cert.pem .
sudo cp /vagrant/copies_of_keys/ca-db-key.pem .

# Generate client key and signing request using elliptic curve prime256v1
sudo openssl req -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -keyout client-key.pem -out client-req.pem -subj "/CN=MySQL_Client"

# Sign client cert with CA (use the same CA cert and key as the server)
sudo openssl x509 -req -in client-req.pem -days 365 -CA  ca-db-cert.pem -CAkey  ca-db-key.pem -set_serial 01 -out client-cert.pem

sudo chown -R vagrant:root /home/vagrant/client-ssl/*.pem




# Create SSL directory for server files
mkdir -p /home/vagrant/server-ssl
cd /home/vagrant/server-ssl

# Generate CA cert and key using elliptic curve prime256v1
sudo openssl ecparam -genkey -name prime256v1 -out ca-backend-key.pem
sudo openssl req -new -x509 -nodes -days 365 -key ca-backend-key.pem -out ca-backend-cert.pem -subj "/CN=Backend_CA"

sudo cp ca-backend-cert.pem /vagrant/copies_of_certificates/ca-backend-cert.pem
sudo cp ca-backend-key.pem /vagrant/copies_of_keys/ca-backend-key.pem

# Generate server key and signing request using elliptic curve prime256v1
sudo openssl req -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -keyout server-backend-key.pem -out server-backend-req.pem -subj "/CN=backend"

# Sign server cert with CA-backend
sudo openssl x509 -req -in server-backend-req.pem -days 365 -CA ca-backend-cert.pem -CAkey ca-backend-key.pem -set_serial 01 -out server-backend-cert.pem
