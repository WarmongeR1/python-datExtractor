# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup

__all__ = [
    'check_pypi',
    'check_github',
    'check_habrahabr',
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


def check_habrahabr(page: BeautifulSoup) -> bool:
    data = [
        ["meta", {'property': 'al:android:app_name', 'content': 'Habrahabr'}],
        ["meta", {'name': 'twitter:site', 'content': '@habrahabr'}]
    ]
    for x in data:
        if bool(page.findAll(*x)):
            return True
    return False
