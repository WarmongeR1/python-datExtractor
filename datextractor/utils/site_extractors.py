# -*- encoding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

__all__ = [
    'extract_pypi',
]


def extract_pypi(page: BeautifulSoup) -> datetime:
    _ = page.findAll('table', {"class": "list"})
    _ = _[0].findAll("tr")[1].findAll('td')[3].getText()  # date (from html)
    return datetime.strptime(_, "%Y-%m-%d")  # datetime
