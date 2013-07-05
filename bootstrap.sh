#!/usr/bin/env bash

#apt-get update
#apt-get install -y apache2
#rm -rf /var/www
#ln -fs /vagrant /var/www

dpkg --configure -a
apt-get update
apt-get -y install redis-server python-pip

pip install -r /vagrant/requirements.txt


