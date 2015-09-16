# -*- encoding: utf-8 -*-

import csv

import yaml

__all__ = [
    'read_csv',
    'loadyaml',
]


def read_csv(filepath: str) -> list:
    with open(filepath, 'r') as fio:
        return [row for row in csv.reader(fio)]


def loadyaml(filepath: str) -> object:
    with open(filepath, 'r') as fio:
        return yaml.load(fio.read())

