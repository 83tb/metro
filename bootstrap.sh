#!/usr/bin/env bash


dpkg --configure -a

apt-get update
apt-get -y install redis-server python-pip

pip install -r requirements.txt


