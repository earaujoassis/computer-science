#!/usr/bin/env python

import os
import argparse
import sympy

import numpy as np
from pyTIR import TIRRegressor


def get_argparser():
    parser = argparse.ArgumentParser(description='TIR baseline runner')
    parser.add_argument('--config', required=True, help='config file path')
    parser.add_argument('--train', required=True, help='training file path')
    parser.add_argument('--val', required=True, help='training file path')
    parser.add_argument('--test', required=True, help='test file path')
    parser.add_argument('--out', required=True, help='output file name')
    return parser


def load_dataset(dataset_file_path, delimiter=' '):
    tabular_dataset = np.loadtxt(dataset_file_path, delimiter=delimiter)
    return tabular_dataset[:, :-1], tabular_dataset[:, -1]


def main(args):
    train_samples, train_targets = load_dataset(os.path.expanduser(args.train))
    model = TIRRegressor(1000, 100, 1.0, 0.25, exponents=(-3,3), max_time=5, penalty=0.01, alg='GPTIR', error='RMSE')
    model.fit(train_samples, train_targets)
    output_filepath = args.out

    val_samples, val_targets = load_dataset(args.val)
    val_preds = model.predict(val_samples)
    relative_error = (((val_targets - val_preds) / val_targets) ** 2).mean()
    mse = np.square(val_preds - val_targets).mean()
    with open(output_filepath, "w") as fp:
        print(f'{relative_error}, {model.expr}, validation', file=fp)

    test_samples, test_targets = load_dataset(args.test)
    test_preds = model.predict(test_samples)
    relative_error = (((val_targets - val_preds) / val_targets) ** 2).mean()
    mse = np.square(test_preds - test_targets).mean()
    with open(output_filepath, "w") as fp:
        print(f'{relative_error}, {model.expr}, test', file=fp)


if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
