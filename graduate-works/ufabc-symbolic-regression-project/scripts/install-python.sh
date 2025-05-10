#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install libssl-dev openssl build-essential
wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
tar xzvf Python-3.12.10.tgz
cd Python-3.12.10
./configure
make
sudo make install
