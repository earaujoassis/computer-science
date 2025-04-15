#!/usr/bin bash

mkdir -p vendor
git lfs install
git clone https://github.com/folivetti/tir.git vendor/tir
rm -rf vendor/tir/.git
cd vendor/tir
bash -c install_stack.sh
