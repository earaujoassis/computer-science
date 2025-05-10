#!/usr/bin/env bash

mkdir -p ./results
mkdir -p ./results/tir

for srsd_category in easy medium hard; do
    RESULT_DIR=./results/tir/srsd-feynman_${srsd_category}
    mkdir -p ${RESULT_DIR}
    echo "[SRSD category: ${srsd_category}]"
    for filepath in ./datasets/srsd-feynman_${srsd_category}/train/*; do
        echo "[Current file: ${filepath}]"
        PARENT_DIR=$(dirname $(dirname $filepath))
        FILE_NAME=$(basename $filepath)
        TRAIN_FILE=${PARENT_DIR}/train/${FILE_NAME}
        python ./runners/solution_tir.py --config ./configs/config.pysr.yaml --train ${TRAIN_FILE} --out ${RESULT_DIR}/${FILE_NAME}
    done
done
