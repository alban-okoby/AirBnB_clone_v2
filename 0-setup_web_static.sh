#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y install nginx

sudo mkdir -p data/web_static/releases/test
sudo mkdir -p data/web_static/shared

echo "<html><head></head><body>Hello, this is a fake HTML file!</body></html>" | sudo tee data/web_static/releases/test/index.html > /dev/null

# Create or recreate the symbolic link
sudo ln -sf data/web_static/releases/test data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '/location \/hbnb_static {/ {N;s/\(\n.*alias.*\)\n/\1\n\t\talias \data\/web_static\/current\/;\n/}}' "$nginx_config"

service nginx restart
