#!/usr/bin/env python

import argparse
import timeit
import os
import numpy as np
import yaml
from pysr import PySRRegressor


def get_argparser():
    parser = argparse.ArgumentParser(description='PySR baseline runner')
    parser.add_argument('--config', required=True, help='config file path')
    parser.add_argument('--train', required=True, help='training file path')
    parser.add_argument('--val', required=True, help='training file path')
    parser.add_argument('--test', required=True, help='test file path')
    parser.add_argument('--out', required=True, help='output table file path')
    return parser


def load_dataset(dataset_file_path, delimiter=' '):
    tabular_dataset = np.loadtxt(dataset_file_path, delimiter=delimiter)
    return tabular_dataset[:, :-1], tabular_dataset[:, -1]


def evaluate(model, output_filepath, eval_samples, eval_targets, eval_type='validation'):
    pred_equation = model.get_best()['equation']
    eval_preds = model.predict(eval_samples)
    relative_error = (((eval_targets - eval_preds) / eval_targets) ** 2).mean()
    with open(output_filepath, 'a') as fp:
        print(f'{relative_error}, {pred_equation}, {eval_type}', file=fp)
    return relative_error


def main(args):
    with open(args.config, 'r') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

    train_samples, train_targets = load_dataset(os.path.expanduser(args.train))
    val_samples, val_targets = load_dataset(args.val)
    model = PySRRegressor(**config['fit'])
    # start_time = timeit.default_timer()
    model.fit(train_samples, train_targets)
    # train_time = timeit.default_timer() - start_time
    evaluate(model, args.out, val_samples, val_targets)
    test_samples, test_targets = load_dataset(args.test)
    evaluate(model, args.out, test_samples, test_targets, eval_type='test')


if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
