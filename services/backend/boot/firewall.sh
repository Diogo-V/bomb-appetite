#!/usr/bin/env bash

# Drop all other connections 
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP

# Accept connections on port 22 (SSH) and ICMP packets 
sudo iptables -A INPUT -p icmp -m limit --limit 1/second -j ACCEPT
sudo iptables -A OUTPUT -p icmp -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Add a rule to accept connections from localhost
sudo iptables -A INPUT -p tcp -s localhost -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d localhost -j ACCEPT

# Add a rule to accept connections from db
sudo iptables -A INPUT -p tcp -s 192.168.0.1 --sport 3306 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d 192.168.0.1 --dport 3306 -j ACCEPT

# Add a rule to accept connections on port 8000 from web
sudo iptables -A INPUT -p tcp -s 192.168.1.3 --dport 8000 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d 192.168.1.3 --sport 8000 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d 192.168.1.3 --dport 3000 -j ACCEPT

# List all rules
sudo iptables -L  -v
sleep 5
ss -tlnu

sudo chown -R vagrant:root /home/vagrant/client-ssl/*.pem

#should not work because not using ssl
mysql -h db -u user -ppassword -e "USE db; SELECT * FROM restaurant;" || true

#should work because using ssl
mysql -h db -u user -ppassword  --ssl-ca="/home/vagrant/client-ssl/ca-db-cert.pem" --ssl-cert="/home/vagrant/client-ssl/client-cert.pem" --ssl-key="/home/vagrant/client-ssl/client-key.pem" -e "USE db; SELECT * FROM restaurant;" || true