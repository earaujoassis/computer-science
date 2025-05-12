#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install build-essential libopenblas-dev libgsl-dev libssl-dev libffi-dev openssl zlib1g zlib1g-dev git-lfs sqlite3 libsqlite3-dev
wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
tar xzvf Python-3.12.10.tgz
cd Python-3.12.10
./configure
make
sudo make install
