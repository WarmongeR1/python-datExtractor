# -*- encoding: utf-8 -*-
from datetime import datetime
from functools import partial

from bs4 import BeautifulSoup
import bs4.element
from funcy import mapcat, merge
from parsedatetime import Calendar, Constants

from datextractor.utils import get_date_tags, prepare_date, check_reg_exp_datetime, SITE_CHECKERS, SITE_EXTRACTORS, \
    reg_exp_datetime, extract_time

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


def _check_sites(page: BeautifulSoup, verbose: bool = False):
    result = None
    for site, checker in SITE_CHECKERS.items():
        if verbose:
            print("Check of site '%s'..." % site)
        if checker(page):
            if verbose:
                print("Page is site - '%s'" % site)
            result = site
            break
    return result


def _extract_of_site(page: BeautifulSoup, site: str) -> datetime:
    assert site in SITE_EXTRACTORS, "Not found extractor for size '%s'" % site
    return SITE_EXTRACTORS[site](page)


def _extract_date_tags(page, verbose: bool = False):
    result = []
    _extract_func_date = partial(_extract_date, verbose=verbose)
    _tags = get_date_tags()
    for tag, tags_params in _tags.items():
        result = merge(
            result,
            list(mapcat(
                partial(_extract_func_date, tag),
                mapcat(page.findAll,
                       [tag] * len(tags_params), tags_params))))
    return list(map(prepare_date, result))


def _extract_date_with_regex(elements):
    _date = None
    _day = None

    _dates = check_reg_exp_datetime(elements)
    if _dates:
        if '%Y %m %d %H %M' in _dates:
            _date = _dates['%Y %m %d %H %M']
        if '%Y %m %d' in _dates:
            _day = _dates['%Y %m %d']
    return _date, _day


def extract(text: str, verbose: bool = False) -> datetime:
    result = None
    page = BeautifulSoup(text, "lxml")

    if verbose:
        print("Run site checkers...")
    _ = _check_sites(page, verbose)
    _date = _extract_of_site(page, _) if _ is not None else None
    if _date is not None:
        return _date

    if verbose:
        print("Extract tags from page")
        print('=' * 20)
        print(' ' * 20)
        print(' ' * 20)

    _date_lines = _extract_date_tags(page, verbose)

    if verbose:
        print(_date_lines)

    _date, _day = _extract_date_with_regex(_date_lines)
    if _date is not None:
        return _date

    _time = None
    _day = None

    cal = Calendar(Constants("en"))

    funcs = [
        cal.parseDateText,
        cal.parse,
        cal.parseDT,
    ]

    key_minutes = 'minutes_hour'
    data = []
    for x in _date_lines:
        if verbose:
            print('-' * 20)
            print("Parse: '%s'" % x)
            print('')

        _date = reg_exp_datetime(x)
        print(_date)
        if _date is not None:
            break

        date_info = {}

        _ = extract_time(x)
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

    if _date is not None:
        return _date

    for x in data:
        if all(func.__name__ in x for func in funcs) and _day is None:

            if verbose:
                print("Day", x.get('parse'))

            _day = datetime(*x.get('parse')[:6])
        elif x.get(key_minutes, None) is not None and _time is None:
            if verbose:
                print("Time", x.get(key_minutes))
            _time = x.get(key_minutes)

    if _day is None:
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
