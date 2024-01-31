#!/usr/bin/env bash
# configure hosts file for the internal network
cat >> /etc/hosts <<EOL
# Vagrant environment nodes
192.168.1.3 web
192.168.1.2 backend 
EOL