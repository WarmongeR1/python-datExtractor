# -*- encoding: utf-8 -*-

from datetime import datetime
import re
import collections

__all__ = [
    'check_reg_exp_datetime',
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
    reg_date = collections.OrderedDict(
    [
        (r'(\d{2}):(\d{2}):(\d{2}) ?((?:am|pm))', "%I %M %S %p"),
        (r'(\d{2}):(\d{2}) ?((?:am|pm))', "%I %M %p"),
        (r'(\d{2}):(\d{2})', "%H %M"),
    ])
    result = []

    for regex, pattern in reg_date.items():
        try:
            result.extend(
                list(
                    map(
                        lambda x: datetime.strptime(' '.join(x), pattern),
                        re.findall(regex, text, re.I))))
        except ValueError:
            pass

    return result


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
