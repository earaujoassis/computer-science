#!/usr/bin/env bash

mkdir -p ./results
mkdir -p ./results/pysr

for srsd_category in easy medium hard; do
    RESULT_DIR=./results/pysr/srsd-feynman_${srsd_category}
    mkdir -p ${RESULT_DIR}
    echo "[SRSD category: ${srsd_category}]"
    for filepath in ./datasets/srsd-feynman_${srsd_category}/train/*; do
        echo "[Current file: ${filepath}]"
        PARENT_DIR=$(dirname $(dirname $filepath))
        FILE_NAME=$(basename $filepath)
        TRAIN_FILE=${PARENT_DIR}/train/${FILE_NAME}
        VAL_FILE=${PARENT_DIR}/val/${FILE_NAME}
        TEST_FILE=${PARENT_DIR}/test/${FILE_NAME}
        python ./runners/solution_pysr.py --config ./configs/config.pysr.yaml --train ${TRAIN_FILE} --val ${VAL_FILE} --test ${TEST_FILE} --out ${RESULT_DIR}/${FILE_NAME}.csv
    done
done
