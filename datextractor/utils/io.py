# -*- encoding: utf-8 -*-

__all__ = [
    'read_csv',
]

import csv


def read_csv(filepath: str):
    with open(filepath, 'r') as fio:
        return [row for row in csv.reader(fio)]
