# -*- encoding: utf-8 -*-
from datetime import datetime
from functools import partial
import pprint
import re
import langid
from bs4 import BeautifulSoup
import bs4.element
from funcy import mapcat, merge
from parsedatetime import Calendar, Constants, pdtLocales


def get_date_tags() -> dict:
    return {
        "p": [
            {"class": "date"},
            {"class": "time"},
            {"class": "meta"},
            {"class": "blog-post-meta single"},
            {"class": "last-updated"},
            {"class": "post-meta"},
        ],
        "h2": [
            {"class": "date-header"},
        ],
        "h4": [
            {"class": "entry-meta"},
        ],
        "h6": [
            {"class": "post-meta"},
        ],
        "time": [
            {"class": "post-time"},
            {"itemprop": "datePublished"},
            {},
        ],
        "div": [
            {"class": "FeatureByline"},
            {"class": "post-meta"},
            {"class": "author_date"},
            {"class": "marg__b_mid text-muted"},
            {"class": "entry entry-1"},
            {"class": "published"},
            {"class": "post-info"},
            {"class": "blog_date"},
            {"class": "user-action-time"},
            {"class": "data-title"},
            {"class": "italics"},
            {"class": "tutorial-date"},
            {"class": "post-author"},
            {"class": "Byline"},
            {"class": "date"},
            {"class": "time"},
            {"id": "last_updated"},
            {"id": "blogpost-info"},
            {"id": "bio_date"},
            {"class": "infos"},
            {"class": "row withgap"},
            {"class": "submitted"},
        ],
        "span": [
            {"class": "postMetaInline postMetaInline--supplemental"},
            {"class": "meta"},
            {"class": "date"},
            {"class": "event-page-date"},
            {"class": "label label-default"},
            {"class": "entry-date"},
            {"itemprop": "datePublished"},
            {"class": "postAuthor hideOnIndex"},
            {"style": "cursor:help;border-bottom: 1px dotted;"},
            {"class": "timestamp"},
            {"class": "created-date"},
            {"class": "wi_date"},
            {"class": "post-date"}
        ],
        "td": [
            {"align": "left", "valign": "middle"},
        ],
        "table": [
            {"class": "list"},
        ],
        "small": [
            {"class": "commentmetadata"},
        ],
        "meta": [
            {"name": "publishedDate"},
            {"itemprop": "publishedDate"},
            {"itemprop": "datePublished"},
            {"property": "article:published_time"},
            {"property": "og:article:modified_time"},
        ],
        "abbr": [
            {"class": "published"},
        ],
        "ul": [
            {"class": "post-info"},
            {"class": "post-date"},
        ],
        "li": [
            {"class": "time"},
            {"class": "date"},
            {"class": "node_submitted first"},
        ],
        "header": [
            {},
        ]
    }


def check_page_without_date(text: str) -> bool:
    result = True
    page = BeautifulSoup(text, "lxml")
    sites_without_date = {
        "github": ["meta", {'name': 'hostname', 'content': 'github.com'}],
        "theaigames": ["a",
                       {"id": "home-button", "href": "http://theaigames.com/"}
                       ],
        "python.org": ["a",
                       {"href": "https://www.python.org/", "id": "logolink",
                        "accesskey": "1"}
                       ],
        "opennet.ru": [
            "meta", {"property": "og:image",
                     "content": "http://www.opennet.ru/opennet_200x200.png"
                     }]
    }

    regs_date = [
        '(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})'
        '(((((0[13578])|([13578])|(1[02]))[\-\/\s]?((0[1-9])|([1-9])|([1-2][0-9])|(3[01])))|((([469])|(11))[\-\/\s]?((0[1-9])|([1-9])|([1-2][0-9])|(30)))|((02|2)[\-\/\s]?((0[1-9])|([1-9])|([1-2][0-9]))))[\-\/\s]?\d{4})(\s(((0[1-9])|([1-9])|(1[0-2]))\:([0-5][0-9])((\s)|(\:([0-5][0-9])\s))([AM|PM|am|pm]{2,2})))?',
        '(([0-1]?[0-9])|([2][0-3])):([0-5]?[0-9])(:([0-5]?[0-9]))?',
    ]

    text = text.replace('127.0.0.1', 'localhost')
    for reg in regs_date:
        if bool(re.search(reg, text)):
            _ = re.findall(reg, text)
            if len(_) > 5:
                continue
            result = False
            break

    if not result:
        for site, data in sites_without_date.items():
            if page.findAll(*data):
                result = True
                break

    # if not result:
    #     cal = Calendar(Constants("en"))
    #     _, _2 = cal.parse(text)
    #     _ = datetime.fromtimestamp(mktime(_))
    #     result = _.year <= 2015

    return result


def prepare_date(date: str) -> str:
    result = remove_week_day(date)
    result = result.replace('\n', ' ').replace('\r', ' ')
    for x in range(4):
        result = result.replace('  ', ' ')
    return result


def _extract_date(tag: str, el: bs4.element.Tag, verbose: bool=False) -> list:
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

    if verbose:
        pprint.pprint(result)
    return result


def find_am_pm_time(text: str):
    return re.findall(r'(\d{2}):(\d{2}) ?((?:am|pm))', text, re.I)


def find_24_time(text: str):
    return re.findall(r'(\d{2}):(\d{2})', text, re.I)

def reg_exp_datetime(date: str):
    result = None
    regs_date = {
        "%Y %m %d %H %M": '(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})',
        "%d %m %Y %H %M": '(\d{2}).(\d{2}).(\d{4}) (\d{2}):(\d{2})',
    }
    for pattern, regex in regs_date.items():
        res = re.search(regex, date)
        if res:
            print('%s: %s' % (reg_exp_datetime.__name__, res))
            result = datetime.strptime(' '.join(res.groups()), pattern)
    return result


def get_data_from_page(text: str, verbose: bool=False) -> datetime:
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
                    if verbose:
                        print("Parse %s: %s" % (fun.__name__, fun(x)[0]))
                    date_info[fun.__name__] = fun(x)[0]
                except AttributeError as e:
                    if verbose:
                        print("Run '%s', error - %s" % (fun.__name__, e))
                    pass
            data.append(date_info)

        for x in data:
            if all(func.__name__ in x for func in funcs) and _day is None:

                # print("Day", x.get('parse'))

                _day = datetime(*x.get('parse')[:6])
            elif x.get(key_minutes, None) is not None and _time is None:
                # print("Time", x.get(key_minutes))
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


def validate_page(text: str) -> bool:
    result = True

    preps = [
        text == '{"error":"Not Found"}',
        "<title>Группы Google</title>" in text,
        '<title>Git and Mercurial code management for teams</title>' in text,
        "- Google Project Hosting" in text,
    ]

    if any(preps):
        result = False
    return result


def check_pypi(page: BeautifulSoup) -> bool:
    """
    Определяет является ли страница pypi по html коду
    :param page:
    :return:
    """
    if page.findAll("link",
                    {'href': 'https://pypi.python.org/pypi?:action=rss'}):
        return True
    else:
        return False


def remove_week_day(string: str) -> str:
    """

    :param string:
    :return:
    """
    short_months = ['mar', 'ma']
    weekdays = []
    for lang, obj in pdtLocales.items():
        if lang == 'en_US' or lang == 'ru_RU':
            try:
                _ = obj()
            except TypeError:
                _ = obj(None)
            weekdays.extend(_.Weekdays)
            weekdays.extend([x for x in _.shortWeekdays if x not in short_months])

    weekdays = list(set(weekdays))
    for x in weekdays:
        pattern = re.compile(x, re.IGNORECASE)
        string = pattern.sub("", string)
    return string


def get_text(text: str) -> str:
    """
    Возвращаем текст страницы без html тегов
    :param text:
    :return:
    """
    try:
        result = BeautifulSoup(text, "lxml").get_text()
        assert result, "Don't got text from html"
    except AssertionError:
        result = ''
    return result
