# -*- encoding: utf-8 -*-
from datetime import datetime
from functools import partial

from bs4 import BeautifulSoup
import bs4.element
from funcy import mapcat, merge
from parsedatetime import Calendar, Constants

from datextractor.utils import check_pypi, get_date_tags, prepare_date, check_reg_exp_datetime, reg_exp_datetime, \
    find_am_pm_time, find_24_time

__all__ = [
    'extract',
]


def _extract_date(tag: str, el: bs4.element.Tag, verbose: bool = False) -> list:
    result = []

    if len(el) > 500:
        return []

    # if verbose:
    #     print(el)

    if tag == 'meta' and el.has_attr('content'):
        result.append(el['content'])
    if tag == 'abbr' and all([el.has_attr('itemprop'), el.has_attr('title')]):
        result.append(el['title'])
    # if tag == 'time' and el.has_attr('datetime'):
    #     result.append(el['datetime'])

    _ = el.prettify()
    _ = BeautifulSoup(_, "lxml").getText()
    _ = _[:300]
    if _:
        result.append(_.lower().strip())
    #
    # if verbose:
    #     pprint.pprint(result)
    return result


def extract(text: str, verbose: bool = False) -> datetime:
    page = BeautifulSoup(text, "lxml")
    cal = Calendar(Constants("en"))
    _time = None
    _day = None
    _date = None

    funcs = [
        cal.parseDateText,
        cal.parse,
        cal.parseDT,
    ]

    all_dates = []

    if check_pypi(page):
        if verbose:
            print("Pypy page")
        _ = page.findAll('table', {"class": "list"})
        _ = _[0].findAll("tr")[1].findAll('td')[3].getText()  # date (from html)
        _day = datetime.strptime(_, "%Y-%m-%d")  # datetime
    else:
        _extract_func_date = partial(_extract_date, verbose=verbose)
        _tags = get_date_tags()
        for tag, tags_params in _tags.items():
            all_dates = merge(
                all_dates,
                list(mapcat(
                    partial(_extract_func_date, tag),
                    mapcat(page.findAll,
                           [tag] * len(tags_params), tags_params))))

        all_dates = list(map(prepare_date, all_dates))

        if verbose:
            print('=' * 20)
            print(' ' * 20)
            print(' ' * 20)
            print(all_dates)

        for x in all_dates:
            if check_reg_exp_datetime(x):
                print(x)

        key_minutes = 'minutes_hour'
        data = []
        for x in all_dates:

            _date = reg_exp_datetime(x)
            if _date is not None:
                break

            date_info = {}

            if verbose:
                print('-' * 20)
                print("Parse: '%s'" % x)
                print('')

            _ = merge(
                list(map(lambda x: datetime.strptime(' '.join(x), "%I %M %p"),
                         find_am_pm_time(x))),
                list(map(lambda x: datetime.strptime(' '.join(x), "%H %M"),
                         find_24_time(x)))
            )

            # print(_)
            date_info[key_minutes] = _[0] if _ else None

            for fun in funcs:
                try:
                    # if verbose:
                    #     print("Parse %s: %s" % (fun.__name__, fun(x)[0]))
                    date_info[fun.__name__] = fun(x)[0]
                except AttributeError as e:
                    # if verbose:
                    #     print("Run '%s', error - %s" % (fun.__name__, e))
                    pass
            data.append(date_info)

        for x in data:
            if all(func.__name__ in x for func in funcs) and _day is None:

                if verbose:
                    print("Day", x.get('parse'))

                _day = datetime(*x.get('parse')[:6])
            elif x.get(key_minutes, None) is not None and _time is None:
                if verbose:
                    print("Time", x.get(key_minutes))
                _time = x.get(key_minutes)

    print(_day, type(_day), type(_time), _date, type(_date))

    if _date is not None:
        result = _date
    elif _day is None:
        result = None
    else:
        result = datetime(
            _day.year,
            _day.month,
            _day.day,
            _time.hour if _time is not None else 0,
            _time.minute if _time is not None else 0,
            _time.second if _time is not None else 0,
        )

    print(' ' * 20)
    if verbose:
        print(' ' * 20)
        print('=' * 20)

    return result
