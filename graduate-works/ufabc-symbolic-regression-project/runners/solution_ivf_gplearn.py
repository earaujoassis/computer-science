#!/usr/bin/env python

import argparse
import timeit
import numpy as np
import yaml
from gplearn.functions import make_function
from gplearn.genetic import SymbolicRegressor

EXTRA_FUNC_DICT = {
    'exp': make_function(function=np.exp, name='exp', arity=1),
    'pow': make_function(function=np.power, name='pow', arity=2)
}

def get_argparser():
    parser = argparse.ArgumentParser(description='gplearn baseline runner')
    parser.add_argument('--config', required=True, help='yaml config file path')
    parser.add_argument('--train', required=True, help='training file path')
    parser.add_argument('--val', required=True, help='training file path')
    parser.add_argument('--test', required=True, help='test file path')
    parser.add_argument('--out', required=True, help='output file name')
    return parser


def load_dataset(dataset_file_path, delimiter=' '):
    tabular_dataset = np.loadtxt(dataset_file_path, delimiter=delimiter)
    return tabular_dataset[:, :-1], tabular_dataset[:, -1]


def update_function_list(function_set):
    if function_set is None:
        return None
    return [EXTRA_FUNC_DICT.get(func_str, func_str) for func_str in function_set]


def evaluate(model, output_filepath, eval_samples, eval_targets, eval_type='validation'):
    pred_equation = model._program
    eval_preds = model.predict(eval_samples)
    relative_error = (((eval_targets - eval_preds) / eval_targets) ** 2).mean()
    with open(output_filepath, 'a') as fp:
        print(f'{relative_error}, {pred_equation}, {eval_type}', file=fp)
    return relative_error


def main(args):
    with open(args.config, 'r') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

    train_samples, train_targets = load_dataset(args.train)
    val_samples, val_targets = load_dataset(args.val)
    model_config = config['model']
    model_config['kwargs']['function_set'] = update_function_list(model_config['kwargs']['function_set'])
    model = SymbolicRegressor(**model_config['kwargs'])
    # start_time = timeit.default_timer()
    model.fit(train_samples, train_targets)
    # train_time = timeit.default_timer() - start_time
    evaluate(model, args.out, val_samples, val_targets)
    test_samples, test_targets = load_dataset(args.test)
    evaluate(model, args.out, test_samples, test_targets, eval_type='test')


if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
