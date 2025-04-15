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
    return parser


def load_dataset(dataset_file_path, delimiter=' '):
    tabular_dataset = np.loadtxt(dataset_file_path, delimiter=delimiter)
    return tabular_dataset[:, :-1], tabular_dataset[:, -1]


def main(args):
    train_samples, train_targets = load_dataset(os.path.expanduser(args.train))
    clr = TIRRegressor(100, 100, 1.0, 0.25, exponents=(-3,3), max_time=5, penalty=0.01, alg='GPTIR', error='RMSE')
    clr.fit(train_samples, train_targets)
    yhat = clr.predict(train_samples)

    mse = np.square(yhat - train_targets).mean()
    print('Fitness should be approx.: ', np.sqrt(mse))
    print(clr.expr)
    print(clr.len)
    for e in clr.front:
        print(e)
    print(sympy.sympify(clr.sympy))

    clr2 = clr.create_model_from(3)
    print('Tst:')
    print(clr2.expr)
    print(clr2.sympy)
    print(clr2.len)
    print(np.sqrt(np.square(clr2.predict(train_samples, train_targets)).mean()))


if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
