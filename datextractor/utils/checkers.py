# -*- encoding: utf-8 -*-

from datetime import datetime
import re
import collections

__all__ = [
    'check_reg_exp_datetime',
    'find_24_time',
    'find_am_pm_time',
    'reg_exp_datetime',
]


def check_reg_exp_datetime(text: str):
    print(text)


def find_am_pm_time(text: str):
    return re.findall(r'(\d{2}):(\d{2}) ?((?:am|pm))', text, re.I)


def find_24_time(text: str):
    return re.findall(r'(\d{2}):(\d{2})', text, re.I)


def reg_exp_datetime(date: str):
    result = None
    regs_date = collections.OrderedDict([
        ('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})+|-(\d{2}):(\d{2})',
         "%Y %m %d %H %M"),
        ('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', "%Y %m %d %H %M"),
        ('(\d{2}).(\d{2}).(\d{4}) (\d{2}):(\d{2})', "%d %m %Y %H %M"),
        ('(\d{4})-(\d{2})-(\d{2})', "%Y %m %d"),
    ])
    for regex, pattern in regs_date.items():
        res = re.search(regex, date)
        if res:
            print(
                '%s: %s - regexp: %s' % (reg_exp_datetime.__name__, res, regex))
            result = datetime.strptime(' '.join(res.groups()[:5]), pattern)
            break
    return result
