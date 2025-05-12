#!/usr/bin/env bash

mkdir -p vendor
git lfs install
git clone https://github.com/folivetti/tir.git vendor/tir
rm -rf vendor/tir/.git
cd vendor/tir && ./install_stack.sh
