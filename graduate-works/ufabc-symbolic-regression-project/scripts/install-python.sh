#!/usr/bin bash

sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
tar xzvf Python-3.12.10.tgz
cd Python-3.12.10
./configure
make
sudo make install
