# -*- encoding: utf-8 -*-

from datetime import datetime
import re
import collections

from funcy import merge

__all__ = [
    'check_reg_exp_datetime',
    'find_24_time',
    'extract_time',
    'reg_exp_datetime',
]


def _get_regex():
    return collections.OrderedDict([
        ('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})+|-(\d{2}):(\d{2})',
         "%Y %m %d %H %M"),
        ('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', "%Y %m %d %H %M"),
        ('(\d{2}).(\d{2}).(\d{4}) (\d{2}):(\d{2})', "%d %m %Y %H %M"),
        ('(\d{4})-(\d{2})-(\d{2})', "%Y %m %d"),
    ])


def check_reg_exp_datetime(elements: list) -> {}:
    result = {}
    for regex, pattern in _get_regex().items():
        for date in elements:
            res = _math_regex(regex, pattern, date)
            if res is not None:
                result[pattern] = res
                break
    return result


def extract_time(text: str):
    return merge(
        list(map(lambda x: datetime.strptime(' '.join(x), "%I %M %p"),
                 find_am_pm_time(text))),
        list(map(lambda x: datetime.strptime(' '.join(x), "%H %M"),
                 find_24_time(text)))
    )

def find_am_pm_time(text: str):
    return re.findall(r'(\d{2}):(\d{2}) ?((?:am|pm))', text, re.I)


def find_24_time(text: str):
    return re.findall(r'(\d{2}):(\d{2})', text, re.I)


def _math_regex(regex: str, pattern: str, date: str):
    _ = re.search(regex, date)
    return datetime.strptime(' '.join(_.groups()[:5]), pattern) if _ else None


def reg_exp_datetime(date: str):
    result = None
    for regex, pattern in _get_regex().items():
        result = _math_regex(regex, pattern, date)
        if result is not None:
            break
    return result
