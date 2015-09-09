# -*- encoding: utf-8 -*-
from datetime import datetime
from time import mktime
import re

from bs4 import BeautifulSoup
from parsedatetime import Calendar, Constants


def get_date_tags() -> dict:
    return {
        "p": [
            {"class": "date"},
            {"class": "time"},
            {"class": "meta"},
            {"class": "blog-post-meta single"},
            {"class": "last-updated"},
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


def get_data_from_page(text: str) -> datetime:
    page = BeautifulSoup(text, "lxml")
    cal = Calendar(Constants("en"))

    result = None

    _tags = get_date_tags()

    date = None
    for key, html_tags in _tags.items():
        for tag in html_tags:
            if check_pypi(page):
                _ = page.findAll('table', {"class": "list"})
                date = _[0].findAll("tr")[1].findAll('td')[3].getText()
                break
            else:
                _ = page.findAll(key, tag)
                if _ and len(_[0]) < 500:
                    if key == 'meta':
                        date = _[0]['content']
                    elif key == 'time':
                        if 'datetime' in _[0]:
                            date = _[0]['datetime']
                        else:
                            date = _[0].prettify()
                            date = BeautifulSoup(date, "lxml").getText()
                            date = date[:300]
                    else:
                        date = _[0].prettify()
                        date = BeautifulSoup(date, "lxml").getText()
                        date = date[:300]
    #
    # if date is None:
    #     _, _2 = cal.parse(text)
    #     result = datetime.fromtimestamp(mktime(_))
    #     print("!!!!! %s" % result)

    if date is not None:
        _, _2 = cal.parse(remove_week_day(date))
        result = datetime.fromtimestamp(mktime(_))

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
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']
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
