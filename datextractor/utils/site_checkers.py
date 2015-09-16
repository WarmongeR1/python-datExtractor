# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup

__all__ = [
    'check_pypi',
]


def check_pypi(page: BeautifulSoup) -> bool:
    """
    Определяет является ли страница pypi по html коду
    :param page:
    :return:
    """
    if page.findAll("link",
                    {'href': 'https://pypi.python.org/pypi?:action=rss'}):
        return True
    else:
        return False
