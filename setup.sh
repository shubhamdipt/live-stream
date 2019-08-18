#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3-pip -y
sudo apt-get install unzip -y
sudo apt-get install virtualenv -y
sudo virtualenv -p python3 /home/ubuntu/.env
sudo apt-get install nginx -y