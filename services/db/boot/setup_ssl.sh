#!/usr/bin/env bash

# Create SSL directory
sudo mkdir -p /etc/mysql/ssl
cd /etc/mysql/ssl

# Create copies of certificates and keys directories
sudo mkdir -p /vagrant/copies_of_certificates
sudo mkdir -p /vagrant/copies_of_keys

# Generate CA cert and key with elliptic curve
sudo openssl ecparam -genkey -name prime256v1 -out ca-db-key.pem
sudo openssl req -new -x509 -nodes -days 365 -key ca-db-key.pem -out ca-db-cert.pem -subj "/CN=MySQL_CA"

sudo cp ca-db-cert.pem /vagrant/copies_of_certificates/ca-db-cert.pem
sudo cp ca-db-key.pem /vagrant/copies_of_keys/ca-db-key.pem

# Generate server key and signing request with elliptic curve
sudo openssl ecparam -genkey -name prime256v1 -out server-db-key.pem
sudo openssl req -new -key server-db-key.pem -out server-req.pem -subj "/CN=db"

# Sign server cert with CA
sudo openssl x509 -req -in server-req.pem -days 365 -CA ca-db-cert.pem -CAkey ca-db-key.pem -set_serial 01 -out server-db-cert.pem
