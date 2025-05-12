#!/usr/bin/env bash

sudo apt-get update
wget https://gnu.c3sl.ufpr.br/ftp/gsl/gsl-2.8.tar.gz
tar xzvf gsl-2.8.tar.gz
cd gsl-2.8
./configure
make
sudo make install
sudo ldconfig
