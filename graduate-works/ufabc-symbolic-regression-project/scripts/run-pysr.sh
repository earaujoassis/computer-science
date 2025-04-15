#!/usr/bin/env bash

mkdir -p ./results
mkdir -p ./results/pysr
mkdir -p ./results/pysr-eqs

for srsd_category in easy medium hard; do
    RESULT_DIR=./results/pysr/srsd-feynman_${srsd_category}
    EQ_DIR=./results/pysr-eqs/srsd-feynman_${srsd_category}
    mkdir -p ${RESULT_DIR}
    mkdir -p ${EQ_DIR}
    echo "[SRSD category: ${srsd_category}]"
    for filepath in ./datasets/srsd-feynman_${srsd_category}/train/*; do
        echo "[Current file: ${filepath}]"
        PARENT_DIR=$(dirname $(dirname $filepath))
        FILE_NAME=$(basename $filepath)
        TRAIN_FILE=${PARENT_DIR}/train/${FILE_NAME}
        python ./runners/solution_pysr.py --config ./configs/config.pysr.yaml --train ${TRAIN_FILE} --eq ${EQ_DIR}/${FILE_NAME}.pkl --table ${RESULT_DIR}/${FILE_NAME}.tsv
    done
done
