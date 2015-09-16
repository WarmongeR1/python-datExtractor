# -*- encoding: utf-8 -*-

import re
from warnings import warn

from bs4 import BeautifulSoup

__all__ = [
    'check_page_without_date',
    'get_text',
]


def check_page_without_date(text: str) -> bool:
    warn("deprecated", DeprecationWarning)

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
