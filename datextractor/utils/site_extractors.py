# -*- encoding: utf-8 -*-

from datetime import datetime

from parsedatetime import Calendar, Constants
from bs4 import BeautifulSoup

__all__ = [
    'extract_pypi',
    'extract_github',
    'extract_habrahabr',
]


def extract_pypi(page: BeautifulSoup) -> datetime:
    _ = page.findAll('table', {"class": "list"})
    _ = _[0].findAll("tr")[1].findAll('td')[3].getText()  # date (from html)
    return datetime.strptime(_, "%Y-%m-%d")  # datetime


def extract_github(page: BeautifulSoup) -> datetime:
    try:
        _ = page.findAll('div', {"class": 'commit-meta'})[0]
        return datetime.strptime(_.findAll('time')[0]['datetime'], "%Y-%m-%dT%H:%M:%Sz")
    except IndexError:
        return None


def extract_habrahabr(page: BeautifulSoup) -> datetime:
    try:
        _ = page.findAll('div', {"class": 'published'})[0]
        return datetime(*Calendar(Constants("ru_RU")).parse(_.text)[0][:5])
    except IndexError:
        return None
