#!/usr/bin/env bash
# configure hosts file for the internal network
cat >> /etc/hosts <<EOL
# Vagrant environment nodes
192.168.0.1 db 
192.168.1.3 web
EOL