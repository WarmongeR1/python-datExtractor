# -*- encoding: utf-8 -*-

from glob import glob
from os.path import exists, basename

import yaml

from six.moves.cPickle import load, dump

__all__ = [
    'load_pickle',
    'save_pickle',
    'read',
    'get_texts_info',
    'dict2yaml',
]


def dict2yaml(data: dict, filepath: str):
    with open(filepath, 'w') as outfile:
        outfile.write(yaml.dump(data))


def load_pickle(path: str) -> object:
    if exists(path):
        with open(path, 'rb') as f:
            result = load(f)
    else:
        result = None
    return result


def save_pickle(path: str, data: object) -> None:
    with open(path, 'wb') as f:
        dump(data, f)


def read(filepath: str) -> str:
    """
    Возвращает текст из файла
    :param filepath:
    :return:
    """
    with open(filepath, 'r') as fio:
        return fio.read()


def get_texts_info(filepath: str, folder: str) -> list:
    print("Check exist %s" % basename(filepath))
    if exists(filepath):
        print("Load texts from file")
        all_texts = load_pickle(filepath)
    else:
        print("Parse html texts")
        all_texts = list(map(read, glob(folder + '/*.html')[:1000]))

        print("Save all text ")
        save_pickle(filepath, all_texts)
    return all_texts
