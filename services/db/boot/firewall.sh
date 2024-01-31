#!/usr/bin/env bash

# Drop all other connections 
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP

# Accept connections on port 22 (SSH) and ICMP packets 
sudo iptables -A INPUT -p icmp -m limit --limit 1/second -j ACCEPT
sudo iptables -A OUTPUT -p icmp -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Add a rule to accept connections on port 3306 from localhost
sudo iptables -A INPUT -p tcp -s localhost --dport 3306 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d localhost --sport 3306 -j ACCEPT

# Add a rule to accept connections on port 3306 from backend
sudo iptables -A INPUT -p tcp -s 192.168.0.2 --dport 3306 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d 192.168.0.2  --sport 3306 -j ACCEPT

#List all rules
sudo iptables -L  -v
ss -tlnu

#Should fail because not using SSL
mysql -u user -p -ppassword -e "USE db; SELECT * FROM restaurant;" || true
# Check if MySQL server is running
mysql -u root -p -proot_password -e "USE db; SELECT * FROM restaurant;"
