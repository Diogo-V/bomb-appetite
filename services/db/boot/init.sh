#!/usr/bin/env bash

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get -y install iptables iputils-ping gnupg

# Install MySQL Server
echo "mysql-server mysql-server/root_password password root_password" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password root_password" | sudo debconf-set-selections
sudo apt install -y mysql-server

# Secure MySQL installation
sudo mysql_secure_installation

# Create a new database named 'db'
mysql -uroot -proot_password -e "CREATE DATABASE IF NOT EXISTS db;"

# Create the user 'user' and set the password
mysql -uroot -proot_password -e "CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'password' REQUIRE X509 ;"

# Grant all privileges on the database to the user from localhost
mysql -uroot -proot_password -e "GRANT ALL PRIVILEGES ON db.* TO 'user'@'localhost' ;"

# Create the user 'user' for '192.168.0.2' and set the password
mysql -uroot -proot_password -e "CREATE USER IF NOT EXISTS 'user'@'192.168.0.2' IDENTIFIED BY 'password' REQUIRE X509;"

# Grant SELECT, INSERT, UPDATE, DELETE privileges to 'user' from '192.168.0.2'
mysql -uroot -proot_password -e "GRANT SELECT, INSERT, UPDATE, DELETE ON db.* TO 'user'@'192.168.0.2';"

# Apply the privilege changes immediately
mysql -uroot -proot_password -e "FLUSH PRIVILEGES;"

# Import SQL file into the database
mysql -uroot -proot_password db < /vagrant/services/db/init.sql

sudo systemctl stop mysql

# Update MySQL configuration to enable SSL
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf

sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf > /dev/null <<EOF
[mysqld]
ssl-ca=/etc/mysql/ssl/ca-db-cert.pem
ssl-cert=/etc/mysql/ssl/server-db-cert.pem
ssl-key=/etc/mysql/ssl/server-db-key.pem
require_secure_transport=ON
EOF

sudo chown -R mysql:root /etc/mysql/ssl/*.pem

sudo systemctl start mysql

