# -*- encoding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

__all__ = [
    'extract_pypi',
    'extract_github',
]


def extract_pypi(page: BeautifulSoup) -> datetime:
    _ = page.findAll('table', {"class": "list"})
    _ = _[0].findAll("tr")[1].findAll('td')[3].getText()  # date (from html)
    return datetime.strptime(_, "%Y-%m-%d")  # datetime


def extract_github(page: BeautifulSoup) -> bool:
    try:
        _ = page.findAll('div', {"class": 'commit-meta'})[0]
        return datetime.strptime(_.findAll('time')[0]['datetime'], "%Y-%m-%dT%H:%M:%Sz")
    except IndexError:
        return None
