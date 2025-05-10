#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install build-essential libssl-dev libffi-dev openssl zlib1g zlib1g-dev git-lfs
wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
tar xzvf Python-3.12.10.tgz
cd Python-3.12.10
./configure
make
sudo make install
