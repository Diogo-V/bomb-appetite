#!/usr/bin/env bash

# Updates system
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get -y install iptables iputils-ping gnupg curl ca-certificates
sudo apt-get clean all

# Create SSL directory for client files
mkdir -p /home/vagrant/client-ssl
cd /home/vagrant/client-ssl

sudo cp /vagrant/copies_of_certificates/ca-backend-cert.pem .
sudo cp /vagrant/copies_of_keys/ca-backend-key.pem .

# Generate client key and signing request using elliptic curve prime256v1
sudo openssl req -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -keyout client-key.pem -out client-req.pem -subj "/CN=web-client"

# Sign client cert with CA (use the same CA cert and key as the server)
sudo openssl x509 -req -in client-req.pem -days 365 -CA  ca-backend-cert.pem -CAkey  ca-backend-key.pem -set_serial 01 -out client-cert.pem

sudo chown -R vagrant:root /home/vagrant/client-ssl/*.pem

# Create SSL directory for server files
mkdir -p /home/vagrant/server-ssl
cd /home/vagrant/server-ssl

# Generate CA cert and key using elliptic curve prime256v1
sudo openssl ecparam -genkey -name prime256v1 -out ca-web-key.pem
sudo openssl req -new -x509 -nodes -days 365 -key ca-web-key.pem -out ca-web-cert.pem -subj "/CN=WebServer_CA"

sudo cp ca-web-cert.pem /vagrant/copies_of_certificates/ca-web-cert.pem
sudo cp ca-web-key.pem /vagrant/copies_of_keys/ca-web-key.pem

# Generate server key and signing request using elliptic curve prime256v1
sudo openssl req -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -keyout server-web-key.pem -out server-web-req.pem -subj "/CN=A24 BombAppetit Web Server"

# Sign server cert with CA-web
sudo openssl x509 -req -in server-web-req.pem -days 365 -CA ca-web-cert.pem -CAkey ca-web-key.pem -set_serial 01 -out server-web-cert.pem

chmod 644 /home/vagrant/server-ssl/server-web-key.pem
