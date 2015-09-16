# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup

__all__ = [
    'check_pypi',
    'check_github',
]


def check_pypi(page: BeautifulSoup) -> bool:
    """
    Определяет является ли страница pypi по html коду
    :param page:
    :return:
    """
    return bool(page.findAll("link",
                             {'href': 'https://pypi.python.org/pypi?:action=rss'}))


def check_github(page: BeautifulSoup) -> bool:
    data = ["meta", {'name': 'hostname', 'content': 'github.com'}]
    return bool(page.findAll(*data))
