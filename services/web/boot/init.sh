#!/usr/bin/env bash

# Updates system
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get -y install iptables iputils-ping gnupg curl ca-certificates
sudo apt-get clean all

# Install Node.js
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=18
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update -y
sudo apt-get install nodejs -y

# Check Node.js and npm versions
echo "Node.js version:"
node -v
echo "npm version:"
npm -v

cd /home/vagrant/web
sudo chown -R vagrant .

npm i

#  Needs to be /home/vagrant to not be synced
nohup npm run dev > /home/vagrant/output.log 2>&1 &

# Check if Node.js server is running.
echo "Checking if Node.js server is running:"
pgrep -fl node
