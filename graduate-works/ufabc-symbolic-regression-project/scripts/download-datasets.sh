#!/usr/bin bash

mkdir -p datasets
git lfs install
git clone https://huggingface.co/datasets/yoshitomo-matsubara/srsd-feynman_easy datasets/srsd-feynman_easy
git clone https://huggingface.co/datasets/yoshitomo-matsubara/srsd-feynman_medium datasets/srsd-feynman_medium
git clone https://huggingface.co/datasets/yoshitomo-matsubara/srsd-feynman_hard datasets/srsd-feynman_hard
