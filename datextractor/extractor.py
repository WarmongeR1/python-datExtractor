# -*- encoding: utf-8 -*-
from datetime import datetime
from functools import partial
from random import shuffle

from bs4 import BeautifulSoup
import bs4.element
from funcy import mapcat, merge
from parsedatetime import Calendar, Constants

from datextractor import TAGS_PATH
from datextractor.utils import prepare_date, check_reg_exp_datetime, SITE_CHECKERS, SITE_EXTRACTORS, \
    reg_exp_datetime, extract_time, loadyaml

__all__ = [
    'extract',
]


def _extract_date(tag: str, el: bs4.element.Tag, verbose: bool = False) -> list:
    result = []

    if len(el) > 300:
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


def _extract_date_tags(page: BeautifulSoup, tags_file: str, verbose: bool = False):
    result = []
    _extract_func_date = partial(_extract_date, verbose=verbose)
    _tags = loadyaml(tags_file)
    for tag, tags_params in _tags.items():
        # if verbose:
        #     print("Processing tag - '%s'" % tag)
        result = merge(
            result,
            list(mapcat(
                partial(_extract_func_date, tag),
                mapcat(page.findAll,
                       [tag] * len(tags_params), tags_params))))
    return list(map(prepare_date, result))


def _create_datetime(day, time):
    if day is None:
        result = None
    else:
        result = datetime(
            day.year,
            day.month,
            day.day,
            time.hour if time is not None else 0,
            time.minute if time is not None else 0,
            time.second if time is not None else 0,
        )
    return result


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


def _get_date_info(funcs: list, key_minutes: str, date_line: str, verbose: bool = False) -> dict:
    result = {}
    _ = extract_time(date_line)
    result[key_minutes] = _[0] if _ else None

    if verbose:
        print('')

    for fun in funcs:
        try:
            if verbose:
                print("Parse %s: %s" % (fun.__name__, fun(date_line)[0]))
            result[fun.__name__] = fun(date_line)[0]
        except AttributeError:
            # if verbose:
            #     print("Run '%s', error - %s" % (fun.__name__, e))
            pass
    return result


def _extract_day_time(data: list, key_minutes: str, funcs_names: list, verbose: bool = False):
    _time, _day = None, None
    for x in data:
        if all(func in x for func in funcs_names) and _day is None:

            if verbose:
                print("Day", x.get('parse'))

            _day = datetime(*x.get('parse')[:6])
        elif x.get(key_minutes, None) is not None and _time is None:
            if verbose:
                print("Time", x.get(key_minutes))
            _time = x.get(key_minutes)

    return _day, _time


def extract(text: str, verbose: bool = False) -> datetime:
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

    _date_lines = _extract_date_tags(page, TAGS_PATH, verbose)
    shuffle(_date_lines)

    if verbose:
        print(_date_lines)

    _date, _day = _extract_date_with_regex(_date_lines)
    if _date is not None:
        return _date

    for x in _date_lines:
        _date = reg_exp_datetime(x)
        if _date is not None:
            return _date

    _cal = Calendar(Constants("en"))

    funcs = [
        _cal.parseDateText,
        _cal.parse,
        _cal.parseDT,
    ]

    key_minutes = 'minutes_hour'
    data = [_get_date_info(funcs, key_minutes, x, verbose) for x in _date_lines]
    result = _create_datetime(*_extract_day_time(data, key_minutes, [x.__name__ for x in funcs], verbose))

    print(' ' * 20)
    if verbose:
        print(' ' * 20)
        print('=' * 20)

    return result
