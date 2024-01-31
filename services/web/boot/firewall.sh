
#!/usr/bin/env bash

# Drop all other connections 
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP

# Accept connections on port 22 (SSH) and ICMP packets 
sudo iptables -A INPUT -p icmp -m limit --limit 1/second -j ACCEPT
sudo iptables -A OUTPUT -p icmp -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

# Accept connections on port 3000
sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 3000 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Add a rule to accept outgoing connections on port 8000 to backend
sudo iptables -A INPUT -p tcp -s 192.168.1.2 --sport 8000 -j ACCEPT
sudo iptables -A OUTPUT -p tcp -d 192.168.1.2 --dport 8000 -j ACCEPT

#List all rules
sudo iptables -L  -v
ss -tlnu

#should not work because not using ssl
curl http://backend:8000/v1/restaurants/ || true

#should work because using ssl
curl --cacert /home/vagrant/client-ssl/ca-backend-cert.pem --cert /home/vagrant/client-ssl/client-cert.pem --key /home/vagrant/client-ssl/client-key.pem -H "userId: "1"" https://backend:8000/v1/restaurants/
