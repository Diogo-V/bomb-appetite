#!/usr/bin/env bash

VERSION=3.10.13
# Updates system
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get -y install iptables iputils-ping gnupg software-properties-common  mysql-client-core-8.0
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y

wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz
tar -xf Python-$VERSION.tgz
cd  Python-$VERSION/

./configure # --enable-optimizations
make -j $(nproc) altinstall
sudo make altinstall
sudo pip3.10 install --upgrade pip
pip3.10 install -r /vagrant/services/backend/requirements.txt
sudo apt-get clean all

cd /home/vagrant/backend
sudo chown -R vagrant .

# Runs the app in development mode. Needs to be /home/vagrant to not be synced
PYTHONPATH=. python3.10 src/app.py > /home/vagrant/output.log 2>&1 &
