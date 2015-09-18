# -*- encoding: utf-8 -*-
import re

from parsedatetime import pdtLocales

__all__ = [
    'prepare_date',
]


def prepare_date(date: str) -> str:
    # result = date.translate(str.maketrans("", "", string.punctuation))
    result = remove_bad_words(date)
    result = result.replace('\n', ' ').replace('\r', ' ').replace(',', '')
    for _ in range(6):
        result = result.replace('  ', ' ')
    return result


def remove_bad_words(string: str) -> str:
    """

    :param string:
    :return:
    """
    short_months = ['mar', 'ma']
    weekdays = ['th', 'at', 'г\.', '\(', '\)']
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
